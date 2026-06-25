# Spectrum and Capacity Physics for Satellite Direct-to-Cell: A Sourced Primer in Plain Language

**Research date:** 2026-06-23
**Status:** Reference primer. The AUTHORITATIVE, sourced explanation of the radio physics behind a satellite direct-to-cell (DTC) business, written so a smart non-engineer can trust each fact independent of any prior claim made in conversation. No go/no-go verdict. Every hard claim carries 2+ independent sources, an inline citation with URL, and a tag (FACT / DERIVED / ESTIMATE / UNKNOWN). New claim IDs COMM-426..450.

> **Why this document exists.** The corpus already pins the numbers (per-phone rate, per-cell capacity, per-satellite supply, the saturation ceiling). What it has NOT done is lay out the underlying physics in plain language with the textbook and measurement sources attached, so a non-specialist founder can verify each concept from first principles and from independent authorities, NOT from a chain of in-house derivations. A prior conversation also asserted some framings (notably "a 25 MHz channel can do about 75 Mbps total" as a fixed ceiling) that need to be evaluated honestly: confirmed where right, corrected where overstated. This primer is that verification layer. It answers seven questions, each with a one-line verdict the founder can trust.

> **Grounds in and does NOT re-derive (this doc adds the PHYSICS-EXPLANATION-AND-EXTERNAL-SOURCING layer; the in-house numbers it points to are owned elsewhere):**
> - [`dtc_capacity_supply.md`](dtc_capacity_supply.md) (COMM-406..425): owns the supply-side identity (per-satellite = beams x per-cell x reuse), the per-cell ~50-75 Mbps figure (COMM-409), and the spectrum-saturation ceiling (COMM-413..416). This doc explains the physics under those numbers and sources it externally.
> - [`dtc_per_phone_rate_and_latency.md`](dtc_per_phone_rate_and_latency.md) (COMM-336..378): owns the per-cell-vs-per-phone split, the scheduler mechanism (COMM-340), and the single-phone rate (~25-50 Mbps). This doc explains the OFDMA/scheduler physics and the carrier-aggregation physics under it.
> - [`dtc_antenna_aperture_tradeoff.md`](dtc_antenna_aperture_tradeoff.md) (COMM-293..314): owns the aperture-to-gain physics (G = 4 pi eta A / lambda^2) and the aperture ladder. This doc explains gain-vs-beamwidth and the gain-to-SNR-to-bits/Hz chain.
> - [`dtc_system_model.md`](dtc_system_model.md) (COMM-315..335, 356..370): owns the governing rule (four levers; count is not a per-phone-rate lever). This doc restates the Shannon basis of that rule with external textbook sourcing.
> - [`spectrum_generations_and_availability.md`](spectrum_generations_and_availability.md) (COMM-108, COMM-114) and [`leo_constellation_coverage_minimums.md`](leo_constellation_coverage_minimums.md) (COMM-224, COMM-226): own the spatial-reuse / Shannon-x-beams framework. This doc explains frequency reuse from the cellular textbook.

> **Tagging.** **[FACT]** sourced (2+ independent sources unless flagged single-source), **[DERIVED]** computed in this doc from sourced inputs, **[ESTIMATE]** a third-party model/projection, **[UNKNOWN]** a named gap (not invented). New claims use **COMM-426..450**. No em-dashes anywhere. Math is inline: `^2` squared, `x` multiply, `->` arrow, `log2` base-2 log.

---

## 0. Answer first (the seven verdicts on one screen)

1. **Frequency vs bandwidth vs data rate.** They are three different things that get confused because two of them are quoted in "MHz." FREQUENCY (the band, e.g. 700 MHz vs 28 GHz) is WHERE on the dial you sit, and it sets reach: low frequency penetrates atmosphere, walls, and distance to reach a phone. BANDWIDTH (the channel WIDTH, e.g. 25 MHz) is HOW WIDE your slice is, and it sets the data ceiling. DATA RATE (Mbps) is the actual delivered speed, which is bandwidth times an efficiency the link quality sets. **Verdict: band = reach, bandwidth = capacity ceiling, data rate = what you actually get; do not conflate the band number with the bandwidth number.**

2. **Shannon-Hartley law and spectral efficiency.** The hard physics ceiling is `rate = bandwidth x log2(1 + SNR)`. Dividing out bandwidth gives spectral efficiency in bits/sec/Hz, which depends only on link quality (SNR) and grows only logarithmically with it. Real values: terrestrial LTE averages ~1.5 bps/Hz and peaks ~15; 5G averages a few bps/Hz and peaks ~23-30; satellite DTC to a phone runs LOW, ~0.5 bps/Hz measured for Starlink up to ~3 bps/Hz claimed for AST, because the terminal is a weak phone and the SNR is near 0 dB. **Verdict: spectral efficiency is the bits you wring from each hertz; it is low for satellite-to-phone because a phone is a tiny, weak antenna and the signal arrives barely above noise.**

3. **The contested "25 MHz -> 75 Mbps" claim.** It is NOT a hard cap. It is bandwidth times a link-dependent efficiency: 25 MHz x ~3 bps/Hz = 75 Mbps, but at higher SNR you get MORE, and at the LOW real DTC efficiencies you get LESS. At Starlink's measured ~0.5-0.8 bps/Hz, the same 25 MHz yields only ~13-20 Mbps. **Verdict: 75 Mbps is the optimistic (AST-class ~3 bps/Hz) end of a conditional per-cell number, not a ceiling; the honest range on a real phone link is ~13 Mbps (Starlink-measured) to ~75 Mbps (AST-claimed), and at the very high SNR a big antenna could buy, even more.** The prior conversational framing of ~75 Mbps as a FIXED ceiling was wrong in both directions: it is neither a floor that DTC reliably hits nor a cap it can never beat.

4. **Carrier aggregation (splitting one download across many channels).** Confirmed and standard: one user can be assigned many sub-channels (resource blocks, or whole component carriers) at once and the rates SUM, up to the full block the scheduler can hand them. LTE-Advanced aggregates up to 5 carriers (100 MHz); 5G goes wider. **Verdict: yes, one user's download can be spread across many channels and summed; the only ceiling is the total bandwidth pool and how much of it the scheduler gives that user.**

5. **Subcarriers within one beam (OFDM/OFDMA) are MULTIPLE ACCESS, not capacity creation.** Splitting a beam into thousands of subcarriers is a way to SHARE the block among users cleanly; it does not add bits. The total is still bandwidth x efficiency no matter how finely you slice it. **Verdict: subcarriers divide the pie, they do not enlarge it; carving a beam into more subcarriers serves more users but adds zero total capacity.**

6. **Spatial reuse across cells/beams is how total SYSTEM capacity multiplies.** The same band reused in non-overlapping cells means total = bandwidth x efficiency x number-of-cells. This is the entire reason a few hundred frequencies serve millions of phones on the ground. The number of cells is set by cell SIZE (smaller cells -> more of them in an area), which for a satellite is set by antenna aperture and altitude, NOT by satellite count past the point where beams already tile the ground. **Verdict: capacity multiplies by reusing the same spectrum in many separate cells; you make more cells by making each one smaller (bigger antenna / lower orbit), and adding satellites past full coverage stops helping.**

7. **Antenna aperture.** A bigger antenna does two things at once: more GAIN (a stronger, more focused signal -> higher SNR -> more bits/Hz, so a bigger antenna can effectively USE more bandwidth) and a NARROWER beam (a smaller cell -> more reuse). Its gain is also what lets a satellite fly HIGHER and still close the link to a phone, buying more coverage per satellite. **Verdict: aperture is the master lever; size buys signal strength (more bits/Hz), smaller cells (more reuse), and the altitude headroom for wider coverage, all at once.**

The rest explains and sources each.

---

## 1. Frequency vs bandwidth vs data rate: three different things, two of them in "MHz"

This is the most common confusion, and it matters because the founder will see "700 MHz," "25 MHz," and "75 Mbps" and they are three unrelated quantities.

**FREQUENCY (the band): where you sit on the radio dial.** Measured in Hz / MHz / GHz. This is the carrier frequency, like the station number on an FM radio. A DTC link on the PCS band sits at ~1.9 GHz; a low-band link sits at ~700 MHz; a millimeter-wave link sits at ~28 GHz. Frequency sets REACH, not speed. Low frequencies bend around terrain, pass through walls and rain, and travel far; high frequencies carry more raw room but are blocked by almost anything and fade fast.

The physics reason low frequency reaches better: free-space path loss rises with frequency. The standard link-budget formula is `FSPL(dB) = 20 log10(distance) + 20 log10(frequency) + 92.45`, so doubling the frequency costs 6 dB before anything else, and higher bands also suffer far worse atmospheric, foliage, and wall losses ([Wikipedia: Free-space path loss](https://en.wikipedia.org/wiki/Free-space_path_loss); the corpus's own link budget uses ~1900 MHz and ~153 dB to LEO, COMM-294). The mobile industry states the tradeoff plainly: low-band (<1 GHz) buys reach and building penetration but little bandwidth; mmWave (24 GHz+) buys peak speed but tiny coverage and no wall penetration ([Waveform: 5G and Shannon's Law](https://www.waveform.com/a/b/guides/5g-and-shannons-law)).

**BANDWIDTH (the channel width): how wide your slice is.** Also measured in Hz / MHz, which is why it gets confused with frequency. This is the WIDTH of the channel you occupy, like how many lanes wide your stretch of highway is. A 25 MHz channel is 25 MHz wide regardless of whether it sits at 700 MHz or 1.9 GHz. Bandwidth sets the CAPACITY CEILING: wider channel, more bits per second possible.

> **The clean way to keep them apart:** frequency is the address (which neighborhood), bandwidth is the lot width (how much room you own there). You can own a 25 MHz lot in the cheap, far-reaching 700 MHz neighborhood or in the 28 GHz neighborhood; the lot is the same width, but the neighborhoods behave completely differently.

**DATA RATE (Mbps): what you actually deliver.** This is the real throughput, and it is bandwidth times a quality-dependent efficiency (Section 2). A 25 MHz channel does NOT have a fixed data rate; it has a rate that depends on how good the link is.

**The bands DTC actually uses** are existing cellular bands, because the whole point is to talk to an unmodified phone:
- Starlink / T-Mobile: PCS G-block, 2x5 MHz, ~1.9 GHz (the measured SMS service), moving to ~65 MHz of owned AWS-4 / H-block spectrum near ~2 GHz via the EchoStar acquisition ([corpus COMM-280/324/337](dtc_per_phone_rate_and_latency.md)).
- AST SpaceMobile: 700-900 MHz cellular bands; BlueWalker 3 demoed on AT&T's ~850 MHz and FirstNet Band 14 / 700 MHz ([corpus COMM-301/111](dtc_antenna_aperture_tradeoff.md)).

> **COMM-426.** Frequency (the band, in MHz/GHz), channel bandwidth (the slice width, also in MHz), and data rate (Mbps) are three distinct quantities; frequency sets reach (low band penetrates atmosphere/walls and travels far because free-space and material path loss rise with frequency, `FSPL = 20 log10(d) + 20 log10(f) + 92.45`), bandwidth sets the capacity ceiling, and data rate is bandwidth times a link-dependent efficiency. **[FACT, textbook]** Sources: [Wikipedia: Free-space path loss](https://en.wikipedia.org/wiki/Free-space_path_loss); [Waveform: 5G and Shannon's Law](https://www.waveform.com/a/b/guides/5g-and-shannons-law) (low-band reach vs mmWave speed tradeoff); cross-ref corpus COMM-294 (DTC link budget at 1900 MHz).
>
> **VERDICT:** band = reach, bandwidth = capacity ceiling, data rate = what you actually get. The "700 MHz" and "25 MHz" numbers are not the same kind of thing.

---

## 2. The Shannon-Hartley law and spectral efficiency: the hard physics ceiling

**The law.** Every radio channel obeys one equation that sets the absolute maximum error-free data rate:

```
   C  =  B  x  log2(1 + SNR)
```

where `C` is channel capacity in bits per second (the theoretical upper bound on the net bit rate), `B` is the channel bandwidth in Hz, and `SNR` is the signal-to-noise ratio at the receiver expressed as a LINEAR power ratio (not in dB) ([Wikipedia: Shannon-Hartley theorem](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem), verbatim definitions of each term; [RF Essentials: calculating link capacity with Shannon-Hartley](https://rfessentials.com/rf-knowledge-base/how-do-i-calculate-the-capacity-of-a-wireless-link-using-the-shannon-hartley-the/)). It is standard textbook physics and is already tagged `certified` in the corpus (COMM-041).

Two consequences the founder should internalize:
- **Rate scales LINEARLY with bandwidth.** Double the MHz, double the ceiling. Bandwidth is the strong lever.
- **Rate scales only LOGARITHMICALLY with signal quality.** To double the rate by power alone, you must roughly QUADRUPLE the SNR (and beyond that, gains shrink fast). Signal strength is a weak lever once you are out of the noise. This is why the corpus says owned spectrum (bandwidth) is the strong lever and gain/altitude are trims (COMM-320).

**Spectral efficiency.** Divide both sides by bandwidth and you get the quantity that compares any radio system fairly:

```
   spectral efficiency  =  C / B  =  log2(1 + SNR)        [bits per second per hertz, bps/Hz]
```

This depends ONLY on link quality (SNR), not on how much bandwidth you have. It tells you how many bits you extract from each hertz of spectrum ([True Geometry / Shannon calculator references](https://blog.truegeometry.com/calculators/How_do_you_calculate_the_channel_capacity_using_the_formula_C_B_log2_1_SNR_where_C_is_the_channel_ca.html)). Real systems achieve roughly 60-80% of the Shannon ceiling after coding overhead, pilots, and guard bands ([Shannon-Hartley search synthesis, multiple references](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem)).

**Real spectral-efficiency values** (the numbers that turn the formula into Mbps):

| System | Spectral efficiency (bps/Hz) | Note | Sources |
|---|---|---|---|
| 4G LTE, average across spectrum | **~1.5** | real network average | [Waveform](https://www.waveform.com/a/b/guides/5g-and-shannons-law); corpus COMM-114 |
| 4G LTE, peak (4x4 MIMO, 64-QAM) | **~15** | best-case one cell | [Techplayon: 5G NR and 4G LTE](https://www.techplayon.com/spectral-efficiency-5g-nr-and-4g-lte/) |
| 5G NR, real-world per stream | **~3** | measured | [arXiv 2312.00957: real-world 5G eval](https://arxiv.org/pdf/2312.00957) (up to 3.14 bps/Hz/stream) |
| 5G NR, peak | **~23-30** | best-case, 100 MHz | [Techplayon](https://www.techplayon.com/spectral-efficiency-5g-nr-and-4g-lte/) (23 bps/Hz DL) |
| **Starlink DTC, MEASURED** | **~0.5-0.8** | weak phone, ~0 dB SINR | [arXiv 2506.00283](https://arxiv.org/html/2506.00283v2) (mean 0.79 / median 0.64 bps/Hz); corpus COMM-337 (SMS-phase 0.52-0.61) |
| AST DTC, claimed commercial | **~3** | 120 Mbps / 40 MHz | [arXiv 2506.18672](https://arxiv.org/html/2506.18672v1); corpus COMM-301/344 |

**Why satellite-to-phone spectral efficiency is LOW.** The phone is the bottleneck. A handset transmits ~0.2 W (23 dBm) into an antenna with essentially no gain (~0 dBi), and it is hundreds of kilometers from the satellite. The signal arrives near or below the noise floor. The corpus's own link budget shows the signal landing at ~-130 dBm against a ~-105 dBm decode threshold, a ~25 dB deficit the satellite alone must close (COMM-293/294). The independent Starlink measurement study confirms the symptom directly: the median SINR observed in the live network is **0 dB** with a wide spread, which is exactly the SNR=1 regime where `log2(1+1) = 1 bps/Hz` is the natural ceiling ([arXiv 2506.00283](https://arxiv.org/html/2506.00283v2), verbatim: "the SINR measurements reveal a median value of 0 dB"). Terrestrial cells achieve more because the tower is close, has a big high-gain antenna, and runs MIMO; a satellite talking to a bare phone gets none of that.

> **A precision note the founder should know:** the most-cited Starlink measurement paper (arXiv 2506.00283) actually reports mean **0.79** / median **0.64** bps/Hz at median SINR 0 dB. The corpus elsewhere cites **0.52-0.61** bps/Hz from the SMS-only phase of the same service. Both are "about half a bit per hertz," and both come from the same study at different readings. The honest, defensible statement is **~0.5 to 0.8 bps/Hz measured for Starlink DTC today**, rising toward 1-3 bps/Hz only with better SINR and cleaner owned spectrum. This is flagged because the single "0.5" figure is sometimes quoted as if it were the only number.

> **COMM-427.** The Shannon-Hartley law `C = B x log2(1 + SNR)` (C in bits/sec, B in Hz, SNR a linear power ratio) sets the hard maximum error-free rate of any channel; rate scales linearly in bandwidth and only logarithmically in SNR, and real systems reach ~60-80% of it. **[FACT, textbook]** Sources: [Wikipedia: Shannon-Hartley theorem](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem); [RF Essentials](https://rfessentials.com/rf-knowledge-base/how-do-i-calculate-the-capacity-of-a-wireless-link-using-the-shannon-hartley-the/); cross-ref corpus COMM-041/315.
>
> **COMM-428.** Spectral efficiency = C/B = log2(1+SNR) in bits/sec/Hz, depends only on link quality, and the real values are: LTE ~1.5 average (peak ~15), 5G ~3 real per-stream (peak ~23-30), and satellite DTC ~0.5-0.8 measured (Starlink) to ~3 claimed (AST). **[FACT, multi-source]** Sources: [Techplayon](https://www.techplayon.com/spectral-efficiency-5g-nr-and-4g-lte/); [Waveform](https://www.waveform.com/a/b/guides/5g-and-shannons-law); [arXiv 2312.00957](https://arxiv.org/pdf/2312.00957) (5G ~3.14 bps/Hz/stream); cross-ref corpus COMM-114/409.
>
> **COMM-429.** Satellite-to-phone spectral efficiency is LOW (~0.5-0.8 bps/Hz measured for Starlink) because the terminal is a weak handset (~0.2 W into ~0 dBi) hundreds of km away, so the signal arrives near the noise floor; the live Starlink network shows a MEASURED median SINR of 0 dB, the SNR=1 regime where ~1 bps/Hz is the natural ceiling. The most-cited measurement (arXiv 2506.00283) reports mean 0.79 / median 0.64 bps/Hz; the corpus's SMS-phase 0.52-0.61 is the same service at a lower reading, so the honest range is ~0.5-0.8 bps/Hz today. **[FACT, measured; spread FLAGGED]** Sources: [arXiv 2506.00283](https://arxiv.org/html/2506.00283v2) (median SINR 0 dB, mean 0.79 / median 0.64 bps/Hz, verbatim); cross-ref corpus COMM-293/294 (link-budget deficit), COMM-337.
>
> **VERDICT:** spectral efficiency is the bits you wring from each hertz; it is set by link quality, and it is low for satellite-to-phone (~0.5-0.8 bps/Hz) because a phone is a tiny weak antenna and the signal arrives barely above noise.

---

## 3. The contested claim: "a 25 MHz channel can do about 75 Mbps total"

This is the single claim the founder most needs evaluated honestly, because a prior conversation asserted ~75 Mbps as a fixed ceiling. The honest answer has three parts.

**Is it a hard cap? No.** The 75 Mbps figure is not a law of physics. It is the Shannon relationship applied with one specific efficiency assumption:

```
   rate  =  bandwidth  x  spectral efficiency
   75 Mbps  =  25 MHz  x  3 bps/Hz
```

The 3 bps/Hz is the AST-claimed commercial DTC efficiency (their "up to 120 Mbps per cell" is exactly 40 MHz x 3 bps/Hz, [arXiv 2506.18672](https://arxiv.org/html/2506.18672v1); corpus COMM-344). So "25 MHz -> 75 Mbps" is a CONDITIONAL per-cell number that holds ONLY at ~3 bps/Hz, which is the optimistic, big-antenna, clean-spectrum end of the DTC range.

**Where the truth sits, honestly.** Because rate = bandwidth x efficiency, and DTC efficiency runs from Starlink's measured ~0.5-0.8 bps/Hz up to AST's claimed ~3, the SAME 25 MHz channel delivers a RANGE, not a point:

| Spectral efficiency (bps/Hz) | Source of the efficiency | 25 MHz channel delivers |
|---|---|---|
| 0.5-0.8 (Starlink measured today) | [arXiv 2506.00283](https://arxiv.org/html/2506.00283v2) | **~13-20 Mbps** |
| 1.5 (4G-average grade) | [Waveform](https://www.waveform.com/a/b/guides/5g-and-shannons-law) | **~37.5 Mbps** |
| 2 (conservative data-grade) | corpus COMM-409 | **50 Mbps** |
| 3 (AST claimed) | [arXiv 2506.18672](https://arxiv.org/html/2506.18672v1) | **75 Mbps** |
| higher (more SNR than AST) | possible with bigger aperture | **MORE than 75** |

So the contested number is real but it is the TOP of a band that has a much lower bottom. A useful sanity check from the measurement data: the same Starlink paper implies ~15.5 Mbps from a 2x25 MHz beam at its SMS-grade ~0.6 bps/Hz efficiency (corpus per-phone doc), which is far below 75 precisely because the efficiency was ~0.6, not 3.

**Two further honesty caveats, both important:**
1. **75 Mbps is PER CELL, not per user under load.** It is the capacity of the whole beam, which a single phone sees only when it is alone in the cell. Split among active users it falls: ~25 active users share it down to ~1-3 Mbps each (corpus COMM-418). The headline is a lightly-loaded number.
2. **It assumes you OWN 25 MHz cleanly.** Starlink's measured service runs on 2x5 MHz (10 MHz) of shared PCS, not 25 MHz, which is part of why its real beam numbers are single-digit Mbps.

> **Where the prior conversational framing was wrong or overstated:** asserting ~75 Mbps as a FIXED CEILING is wrong in both directions. It is not a ceiling DTC can never beat (more SNR or more bandwidth beats it), and it is not a floor DTC reliably hits (at real measured efficiency a 25 MHz beam does ~13-20 Mbps, less than a third of 75). The correct statement is: **75 Mbps is the optimistic (3 bps/Hz, AST-class) end of a conditional per-cell number on 25 MHz; the honest range for a real phone link is roughly 13 Mbps (Starlink-measured) to 75 Mbps (AST-claimed), and it can exceed 75 only with a stronger link than AST assumes.**

> **COMM-430.** "A 25 MHz channel can do about 75 Mbps" is NOT a hard cap; it is rate = bandwidth x spectral efficiency evaluated at ~3 bps/Hz (25 MHz x 3 = 75 Mbps), the AST-claimed commercial end. At higher SNR the same 25 MHz yields more; at the low measured DTC efficiencies it yields less. **[DERIVED]** Sources: [arXiv 2506.18672](https://arxiv.org/html/2506.18672v1) (AST 120 Mbps / 40 MHz = 3 bps/Hz); cross-ref corpus COMM-344/409.
>
> **COMM-431.** The honest per-cell range on 25 MHz for a real DTC phone link is ~13-20 Mbps at Starlink's measured ~0.5-0.8 bps/Hz, ~37.5 Mbps at 4G-grade ~1.5, ~50 Mbps at ~2, and ~75 Mbps at AST's claimed ~3; the efficiency assumption is the entire swing, and 75 Mbps is the optimistic top, not a ceiling or a floor. **[DERIVED]** Sources: [arXiv 2506.00283](https://arxiv.org/html/2506.00283v2) (0.5-0.8 measured); [arXiv 2506.18672](https://arxiv.org/html/2506.18672v1) (3 claimed); cross-ref corpus COMM-409/418.
>
> **COMM-432.** The 75 Mbps figure is PER CELL (the single-phone-alone peak), not per user under load, and it assumes 25 MHz of cleanly owned spectrum; Starlink's measured service runs on 2x5 MHz of shared PCS, which is why its real beam throughput is single-digit Mbps, far below 75. Asserting 75 Mbps as a fixed ceiling is wrong in both directions. **[DERIVED, corrects prior framing]** Sources: cross-ref corpus COMM-337/418; [arXiv 2506.00283](https://arxiv.org/html/2506.00283v2).
>
> **VERDICT:** NO, 25 MHz is not capped at 75 Mbps. 75 Mbps is the optimistic (3 bps/Hz) end of a conditional per-cell number; the honest real-phone range is ~13 to 75 Mbps depending on link quality, and a single phone gets the top of that only when alone in the cell.

---

## 4. Carrier aggregation: one download split across many channels, summed

**The question:** can one user be handed many sub-channels at once and have their rates add up? Yes, and it is a deployed, standardized feature.

**Carrier aggregation (CA)** lets a single device receive and transmit on multiple component carriers (separate frequency blocks) at the same time, and the throughput SUMS across them. It was introduced in LTE-Advanced (3GPP Release 10) specifically to raise per-user peak rate by gluing channels together ([3GPP: Carrier Aggregation on mobile networks](https://www.3gpp.org/technologies/carrier-aggregation-on-mobile-networks); [Wikipedia: Carrier aggregation](https://en.wikipedia.org/wiki/Carrier_aggregation)).

The specifics confirm the founder's mental model exactly:
- A capable device "can simultaneously receive and/or transmit on multiple component carriers corresponding to multiple serving cells" ([3GLTEInfo: Carrier Aggregation in LTE-Advanced](https://www.3glteinfo.com/carrier-aggregation-in-lte-advanced/)).
- LTE-Advanced aggregates up to 5 carriers in Release 10 (8 from Release 11), each up to 20 MHz, for up to 100 MHz combined ([Wikipedia: Carrier aggregation](https://en.wikipedia.org/wiki/Carrier_aggregation)). 5G NR extends this further.
- The stated purpose is "higher peak user throughput" by widening the per-user transmission bandwidth ([3GLTEInfo](https://www.3glteinfo.com/carrier-aggregation-in-lte-advanced/)).

At a finer grain, even within a single carrier the scheduler can assign one user MANY resource blocks at once (a resource block is 12 subcarriers); a lightly loaded cell hands nearly the whole channel to one phone. This is exactly why demonstrated single-device DTC speeds equal the full per-beam capacity (corpus COMM-340): the scheduler gave that one phone the whole pool.

**The ceiling on aggregation** is simply the total bandwidth available and how much of it the scheduler chooses to give one user. You can sum sub-channels up to the full block, but no further; aggregation moves bits a user could already have been given, it does not exceed the bandwidth x efficiency total.

> **COMM-433.** Carrier aggregation (LTE-Advanced Release 10+) lets ONE user receive and transmit on multiple component carriers simultaneously, and the rates SUM, up to 5 carriers / 100 MHz in LTE-A (more in 5G); within a single carrier the scheduler can also assign one user many resource blocks at once, which is why a lightly loaded cell's demonstrated single-device speed equals the full per-beam capacity. The ceiling is the total bandwidth pool, not the number of channels. **[FACT, standardized]** Sources: [3GPP: Carrier Aggregation](https://www.3gpp.org/technologies/carrier-aggregation-on-mobile-networks); [Wikipedia: Carrier aggregation](https://en.wikipedia.org/wiki/Carrier_aggregation); [3GLTEInfo](https://www.3glteinfo.com/carrier-aggregation-in-lte-advanced/); cross-ref corpus COMM-340.
>
> **VERDICT:** YES, one user's download can be spread across many sub-channels and summed for a higher rate, up to the full block. This is standard LTE/5G carrier aggregation; the only limit is total bandwidth and how much the scheduler allocates.

---

## 5. Subcarriers within one beam (OFDM/OFDMA) are multiple access, not capacity creation

**The question:** if a beam is split into thousands of subcarriers, does that create more capacity? No. Subcarriers are a way to SHARE one block cleanly among users; the total stays bandwidth x efficiency.

**OFDM** (orthogonal frequency-division multiplexing) divides one channel into many closely spaced, mutually non-interfering subcarriers. **OFDMA** (the multiple-access version used in LTE/5G/Wi-Fi 6 downlinks) assigns different SUBSETS of those subcarriers to different users at the same time ([TechTarget: OFDMA definition](https://www.techtarget.com/searchnetworking/definition/orthogonal-frequency-division-multiple-access-OFDMA); [Mini-Circuits: Basics of OFDM](https://blog.minicircuits.com/the-basics-of-orthogonal-frequency-division-multiplexing-ofdm/)).

The key physics, stated plainly by the sources: OFDMA "dynamically assigns subsets of subcarriers to different users, enabling simultaneous transmissions" and lets "each user occupy a distinct portion of the spectrum while SHARING the overall bandwidth" ([OFDMA search synthesis, multiple references](https://www.techtarget.com/searchnetworking/definition/orthogonal-frequency-division-multiple-access-OFDMA)). In LTE the subcarriers are grouped into resource blocks (12 subcarriers each), and the network allocates resource blocks to users ([LTE physical-layer references](https://helpfiles.keysight.com/csg/89600B/Webhelp/Subsystems/lte/content/lte_overview.htm)).

The conclusion follows directly from Shannon: the total error-free bits/sec across a channel is `B x log2(1+SNR)` regardless of how you partition `B`. Slicing the same 25 MHz into 1,000 subcarriers instead of 100 does not raise `B` and does not raise the SNR, so it cannot raise the total. It only lets more users share the block at finer granularity. The corpus states the same mechanism as a time-division scheduler: "a satellite DTC beam serves users by a time-division scheduler, one phone per resource block at an instant; a lightly-loaded cell hands the near-full beam to one phone, a busy cell splits it" (COMM-340/359). Frequency-domain (OFDMA subcarriers) and time-domain (scheduler slots) are two faces of the same fact: the beam is ONE shared pool, divided, never enlarged.

> **The trap to avoid:** "more subcarriers" sounds like "more channels" and therefore "more capacity." It is not. Subcarriers are how you DIVIDE a fixed pool among many users without them stepping on each other. The pool's size is fixed by bandwidth x efficiency.

> **COMM-434.** OFDM splits one channel into many orthogonal subcarriers, and OFDMA assigns different subsets of subcarriers (grouped into resource blocks) to different users simultaneously; this is a MULTIPLE-ACCESS / sharing mechanism, not capacity creation. Total error-free bits/sec stays bandwidth x spectral efficiency no matter how finely the band is sliced, because slicing changes neither B nor SNR. **[FACT, textbook]** Sources: [TechTarget: OFDMA](https://www.techtarget.com/searchnetworking/definition/orthogonal-frequency-division-multiple-access-OFDMA); [Mini-Circuits: OFDM basics](https://blog.minicircuits.com/the-basics-of-orthogonal-frequency-division-multiplexing-ofdm/); cross-ref corpus COMM-340/359 (the same beam-is-one-shared-pool scheduler statement) and COMM-427 (Shannon).
>
> **VERDICT:** subcarriers divide the pie, they do not enlarge it. Carving a beam into more subcarriers (OFDMA) serves more users cleanly but adds zero total capacity; the total is bandwidth x efficiency regardless.

---

## 6. Spatial reuse across cells/beams: how total SYSTEM capacity multiplies

**The question:** if one cell's spectrum is fixed, how does a whole network serve millions? By reusing the SAME band in many separate cells. This is the single most important multiplier in all of wireless.

**Frequency reuse** is using the same radio frequencies in non-adjacent cells. Because cells far enough apart do not interfere, the same channel can carry independent traffic in each, and "allowing many thousands of subscribers to be served by a system of only several hundred frequency bands" ([cellular frequency-reuse references, multiple](https://www.geeksforgeeks.org/computer-networks/frequency-reuse/)). The total system capacity is therefore:

```
   total system capacity  =  bandwidth  x  spectral efficiency  x  number of cells
```

This is the corpus's area-capacity identity exactly (COMM-413): over a fixed ground area on a fixed owned bandwidth, max capacity = `B x SE x N_reuse`, where `N_reuse` = ground area / beam area is the number of non-overlapping co-channel cells that tile the area.

**You make more cells by making each one SMALLER.** This is cell splitting, and it has been the dominant driver of wireless capacity growth for decades. "Cell splitting divides a geographic area into smaller cells, which increases the channel capacity," and "the creation of new smaller cells increases the capacity of the system as a whole" ([GeeksforGeeks: cell splitting and sectoring](https://www.geeksforgeeks.org/computer-networks/cell-splitting-and-cell-sectoring/)). Martin Cooper's observation (Cooper's Law) is that the bulk of the ~million-fold growth in wireless capacity over the last century came from spatial reuse / densification, NOT from more bandwidth or better coding ([Cooper's Law / network densification references](https://www.researchgate.net/figure/Martin-Coopers-assessment-of-Spectral-Efficiency-of-Wireless-Systems-Source_fig2_236410000)).

**For a satellite, the cell is the beam, and the cell size is set by aperture and altitude, NOT by satellite count.** This is the crux the founder cares about. A satellite forms many beams (AST's 223 m^2 array forms ~2,500 beams covering ~324 km^2 each at ~20.3 km diameter; Starlink V2-mini forms 48; [arXiv 2506.18672](https://arxiv.org/html/2506.18672v1); corpus COMM-407/408/412). Each beam is one cell. The number of non-overlapping cells that fit over a target area is set by how SMALL each beam footprint is, which is set by antenna aperture (bigger aperture -> narrower beam -> smaller cell -> more of them) and altitude (lower -> smaller footprint).

**Crucially, adding satellites stops helping once the ground is tiled.** Once every patch of the target is already covered by one beam on the owned spectrum, more satellites add OVERLAPPING co-channel beams that interfere rather than add capacity. The corpus documents this saturation from multiple independent sources: full frequency reuse "leads to severe inter-beam co-channel interference and degrades the SINR, limiting system performance," and "overlaps of multiple co-channel beams can reduce the communication capacity" ([IEEE Xplore 10816533](https://ieeexplore.ieee.org/document/10816533/); [arXiv 2501.02750](https://arxiv.org/html/2501.02750v3); corpus COMM-414). So a satellite system's capacity multiplies with the number of NON-OVERLAPPING beams its geometry allows, which is set by aperture and altitude, not by flying more of the same satellite past the tiling point.

> **The contrast that defines the DTC business:** the same 25 MHz a satellite beam spends ONCE over ~324 km^2 is spent ~100+ times by terrestrial cell-splitting over that same area (towers every ~1-2 km). That is why terrestrial area capacity is ~30x to thousands-x above DTC, and why the satellite's edge is COVERAGE (reaching what nothing else reaches), not capacity (corpus COMM-422).

> **COMM-435.** Total system capacity multiplies by frequency reuse: the same band carried in non-overlapping cells gives total = bandwidth x spectral efficiency x number of cells, which is how a few hundred frequencies serve millions of phones. You make more cells by making each smaller (cell splitting), the dominant driver of wireless capacity growth (Cooper's Law). **[FACT, textbook]** Sources: [GeeksforGeeks: frequency reuse](https://www.geeksforgeeks.org/computer-networks/frequency-reuse/) and [cell splitting](https://www.geeksforgeeks.org/computer-networks/cell-splitting-and-cell-sectoring/); [Cooper's Law / densification](https://www.researchgate.net/figure/Martin-Coopers-assessment-of-Spectral-Efficiency-of-Wireless-Systems-Source_fig2_236410000); cross-ref corpus COMM-413.
>
> **COMM-436.** For a satellite the cell is the beam, and the number of non-overlapping co-channel beams that tile a target area (and thus the reuse multiplier) is set by beam FOOTPRINT (aperture and altitude), NOT by satellite count; a satellite forms many beams (AST ~2,500 at 223 m^2 / ~324 km^2 each; Starlink V2-mini 48), and once the ground is tiled, adding more same-aperture satellites adds overlapping co-channel beams that interfere rather than add capacity. **[FACT for the mechanism, multi-source; structure from corpus]** Sources: [arXiv 2506.18672](https://arxiv.org/html/2506.18672v1) (AST 2,500 beams, 324 km^2); [IEEE Xplore 10816533](https://ieeexplore.ieee.org/document/10816533/) and [arXiv 2501.02750](https://arxiv.org/html/2501.02750v3) (co-channel overlap reduces capacity); cross-ref corpus COMM-407/414/415.
>
> **VERDICT:** capacity multiplies by reusing the same spectrum in many separate cells (total = bandwidth x efficiency x number of cells). You make more cells by making each smaller, which for a satellite means a bigger antenna or lower orbit, NOT more satellites once the ground is already covered.

---

## 7. Antenna aperture: gain, beamwidth, SNR, and the altitude it unlocks

**The question:** what does a bigger antenna actually buy? Three things at once, all of which help.

**Aperture sets GAIN (signal strength and reach).** The gain of an aperture antenna is:

```
   G  =  4 pi eta A / lambda^2
```

where `A` is the physical aperture area, `eta` is the efficiency (typically ~0.55-0.65 for a real dish), and `lambda` is the wavelength ([Wikipedia: Parabolic antenna](https://en.wikipedia.org/wiki/Parabolic_antenna); [Electronics Notes: parabolic reflector gain](https://www.electronics-notes.com/articles/antennas-propagation/parabolic-reflector-antenna/antenna-gain-directivity.php)). Gain rises linearly with area: double the antenna area, double the gain (add 3 dB). This is the same formula stated in SpaceX/AST FCC filings and used throughout the corpus (COMM-296). More gain means a stronger, more concentrated signal, which directly raises SNR at the receiver.

**Aperture sets BEAMWIDTH (cell size).** "There is an inverse relation between gain and beamwidth": a bigger aperture concentrates energy into a NARROWER beam ([antenna beamwidth references, multiple](https://www.electronics-notes.com/articles/antennas-propagation/parabolic-reflector-antenna/antenna-gain-directivity.php)). A narrower beam means a smaller footprint on the ground, which means a smaller cell, which means more non-overlapping cells fit over an area, which (Section 6) means more total system capacity. So aperture helps capacity twice: once through SNR (more bits/Hz per cell) and once through reuse (more cells).

**The chain that matters for the founder: more gain -> more SNR -> more bits/Hz -> can use more bandwidth effectively.** Because spectral efficiency = log2(1+SNR), raising SNR raises the bits you extract from each hertz, climbing toward the Shannon ceiling. The corpus quantifies the sensitivity (corrected): +1 dB of link gain is ~1.26x rate (10^0.1), +2 dB is ~1.585x (10^0.2) (COMM-349/356; note the corpus corrected an earlier "+1 dB = 1.58x" error, do not reintroduce it). So a bigger antenna's extra gain lets a DTC system push its efficiency up from the ~0.5-0.8 bps/Hz floor toward the ~2-3 bps/Hz that makes wider bandwidth worth owning. A weak link cannot use wide bandwidth efficiently; a strong link can.

**Aperture is what ENABLES higher altitude, which buys coverage.** A higher orbit means each satellite sees more of the Earth, so fewer satellites cover the globe, but the link is longer and weaker (path loss rises with distance). The only way to fly higher and still close the link to a weak phone is to bring more gain, which means more aperture. The corpus quantifies that altitude itself is a WEAK trim (dropping 550 km to 350 km buys only ~3.5-3.9 dB at useful elevations) while aperture is the strong lever (25 m^2 to 223 m^2 spans ~9.5 dB), so AST uses a huge ~223 m^2 array specifically so it can operate at a PLANNED ~725-740 km AND still deliver broadband to a phone (corpus COMM-316/346/357). Aperture buys the gain budget that altitude spends.

The aperture ladder, with the coverage and rate it buys (all from the corpus, externally sourced there):

| System | Aperture | Gain | Cell on ground | Altitude | Per-cell rate |
|---|---|---|---|---|---|
| Lynk Global | ~1-1.5 m^2 | ~29 dBi | (wide) | low LEO | SMS only |
| Starlink Gen2 DTC | ~25 m^2 | ~32.5 dBi @ 880 MHz | (wide) | ~340-360 km | ~3-4 Mbps/beam measured |
| AST BlueBird Block 1 / BW3 | ~64 m^2 | ~36.5 dBi | (demo) | demo ~507-527 km | ~21 Mbps demonstrated to a phone |
| **AST BlueBird Block 2** | **~223 m^2** | **~42 dBi @ 880 MHz** | **~20.3 km / ~324 km^2** | **planned ~725-740 km** | **up to ~120 Mbps/cell** |

([arXiv 2506.18672](https://arxiv.org/html/2506.18672v1) for AST aperture/gain/beam/rate; corpus COMM-297..303/357 for the full ladder and the altitude correction.)

> **COMM-437.** Antenna gain follows `G = 4 pi eta A / lambda^2` (aperture area A, efficiency eta ~0.55-0.65, wavelength lambda), so gain rises linearly with aperture area (double area = +3 dB), and there is an inverse relation between gain and beamwidth (bigger aperture = narrower beam = smaller ground cell). A bigger antenna therefore raises both SNR (more gain) and reuse (smaller cells) at once. **[FACT, textbook]** Sources: [Wikipedia: Parabolic antenna](https://en.wikipedia.org/wiki/Parabolic_antenna); [Electronics Notes: parabolic gain/beamwidth](https://www.electronics-notes.com/articles/antennas-propagation/parabolic-reflector-antenna/antenna-gain-directivity.php); cross-ref corpus COMM-296.
>
> **COMM-438.** More gain -> more SNR -> more bits/Hz (since spectral efficiency = log2(1+SNR)), so a bigger antenna can effectively USE more bandwidth, climbing from the ~0.5-0.8 bps/Hz DTC floor toward ~2-3 bps/Hz; the sensitivity is +1 dB ~ 1.26x rate, +2 dB ~ 1.585x (corpus-corrected from an earlier 1.58x/+1 dB error). **[DERIVED + FACT]** Sources: [Wikipedia: Shannon-Hartley](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem) (efficiency = log2(1+SNR)); cross-ref corpus COMM-349/356.
>
> **COMM-439.** Aperture's gain is what ENABLES higher altitude: a higher orbit covers more Earth (fewer satellites) but the longer link is weaker, and only more gain (more aperture) closes it to a weak phone; altitude is a weak trim (~3.5-3.9 dB from 550->350 km) while aperture is the strong lever (~9.5 dB from 25->223 m^2), which is why AST uses a ~223 m^2 array to operate at a planned ~725-740 km and still deliver broadband. **[FACT, sourced in corpus]** Sources: [arXiv 2506.18672](https://arxiv.org/html/2506.18672v1) (AST 223 m^2 / 42 dBi); cross-ref corpus COMM-316/346/357.
>
> **VERDICT:** aperture is the master lever. A bigger antenna buys signal strength (more SNR -> more bits/Hz -> can use more bandwidth), smaller cells (more reuse -> more system capacity), and the gain budget to fly higher (more coverage per satellite), all at once.

---

## 8. So what (the seven verdicts assembled into one picture)

Putting the physics together, here is the chain a non-engineer can carry:

- A DTC link to a phone is bandwidth-starved and SNR-starved at once. Frequency choice (low band) buys the REACH to get to the phone at all. Bandwidth buys the capacity CEILING. Link quality (set mostly by antenna aperture) buys the EFFICIENCY that turns that ceiling into real Mbps.
- The hard ceiling is Shannon: rate = bandwidth x log2(1+SNR). Per hertz, DTC to a phone yields ~0.5-0.8 bps/Hz today (measured, Starlink), up to ~3 claimed (AST), versus ~1.5 average for terrestrial 4G. The phone is the bottleneck.
- "25 MHz -> 75 Mbps" is the optimistic end of a band, not a cap. Real range ~13-75 Mbps per cell depending on link quality, and the top only when one phone is alone in the cell.
- Carrier aggregation lets one user sum many channels up to the full block (real, helps peak rate). OFDMA subcarriers SHARE the block among users (does not add capacity). These are opposite-direction tools on the same fixed pool.
- System capacity multiplies by spatial reuse: total = bandwidth x efficiency x number of cells. More cells come from smaller cells, which for a satellite means bigger aperture or lower orbit, NOT more satellites once the ground is tiled.
- Aperture is the lever that touches everything: SNR (bits/Hz), cell size (reuse), and the altitude headroom for coverage.

The business consequence (owned by the economics docs, stated here only as the physics conclusion): the satellite spends its 25 MHz once over ~324 km^2 where a terrestrial network spends it ~100+ times, so DTC's structural edge is COVERAGE, not capacity, and the levers to raise capacity are owned spectrum and aperture, not airframe count. No verdict.

---

## 9. Open questions and flagged uncertainties

- **The exact Starlink DTC spectral efficiency has a documented spread:** mean 0.79 / median 0.64 bps/Hz from the live-network measurement (arXiv 2506.00283) versus 0.52-0.61 from the SMS-only phase (same study, corpus COMM-337). Both round to "about half a bit per hertz." This primer uses ~0.5-0.8 bps/Hz as the honest band. [FLAGGED]
- **AST's ~3 bps/Hz is a claimed/derived commercial figure** (120 Mbps / 40 MHz from their own filing), not an independently measured operational value at scale. Treat it as the optimistic anchor. [ESTIMATE, single-origin]
- **The per-cell number is a single-phone-alone peak;** the per-user-under-load number depends on concurrency and active-user density per beam, which the corpus flags as an UNKNOWN the founder must set (COMM-421). This primer does not resolve it.
- **Real-world fraction of Shannon achieved (~60-80%)** is a general engineering rule, not a DTC-specific measurement; the measured Starlink number already bakes in real losses, so do not discount it twice. [FLAGGED]

---

## Sources

**Shannon-Hartley and spectral efficiency (textbook):**
- [Wikipedia: Shannon-Hartley theorem](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem) (formula and verbatim term definitions)
- [RF Essentials: calculating link capacity with Shannon-Hartley](https://rfessentials.com/rf-knowledge-base/how-do-i-calculate-the-capacity-of-a-wireless-link-using-the-shannon-hartley-the/)
- [True Geometry: Shannon channel-capacity calculator](https://blog.truegeometry.com/calculators/How_do_you_calculate_the_channel_capacity_using_the_formula_C_B_log2_1_SNR_where_C_is_the_channel_ca.html)

**LTE / 5G spectral efficiency values:**
- [Techplayon: Spectral Efficiency, 5G NR and 4G LTE](https://www.techplayon.com/spectral-efficiency-5g-nr-and-4g-lte/) (LTE peak ~15, 5G peak ~23 bps/Hz)
- [Waveform: 5G and Shannon's Law](https://www.waveform.com/a/b/guides/5g-and-shannons-law) (LTE ~1.5 bps/Hz average; low-band vs mmWave reach tradeoff)
- [arXiv 2312.00957: A Comprehensive Real-World Evaluation of 5G](https://arxiv.org/pdf/2312.00957) (5G ~3.14 bps/Hz/stream real-world)

**Starlink direct-to-cell measurement (primary):**
- [arXiv 2506.00283: Direct-to-Cell, a First Look into Starlink's DS2D RAN through Crowdsourced Measurements](https://arxiv.org/html/2506.00283v2) (mean 0.79 / median 0.64 bps/Hz; median SINR 0 dB; 4 Mbps/beam on 2x5 MHz; single-user-occupies-full-beam)

**AST SpaceMobile capacity / aperture (primary):**
- [arXiv 2506.18672: Spectrum Opportunities for the Wireless Future](https://arxiv.org/html/2506.18672v1) (AST 2,500 beams, 42 dBi at 223 m^2 / 880 MHz, 40 MHz/beam -> 120 Mbps = 3 bps/Hz, 20.3 km / 324 km^2 beam)

**Carrier aggregation:**
- [3GPP: Carrier Aggregation on mobile networks](https://www.3gpp.org/technologies/carrier-aggregation-on-mobile-networks)
- [Wikipedia: Carrier aggregation](https://en.wikipedia.org/wiki/Carrier_aggregation) (up to 5 carriers / 100 MHz LTE-A)
- [3GLTEInfo: Carrier Aggregation in LTE-Advanced](https://www.3glteinfo.com/carrier-aggregation-in-lte-advanced/)

**OFDM / OFDMA as multiple access:**
- [TechTarget: OFDMA definition](https://www.techtarget.com/searchnetworking/definition/orthogonal-frequency-division-multiple-access-OFDMA)
- [Mini-Circuits: The Basics of OFDM](https://blog.minicircuits.com/the-basics-of-orthogonal-frequency-division-multiplexing-ofdm/)
- [Keysight: LTE Physical Layer Overview](https://helpfiles.keysight.com/csg/89600B/Webhelp/Subsystems/lte/content/lte_overview.htm) (resource block = 12 subcarriers)

**Frequency reuse / cell splitting (textbook):**
- [GeeksforGeeks: Frequency Reuse](https://www.geeksforgeeks.org/computer-networks/frequency-reuse/)
- [GeeksforGeeks: Cell Splitting and Cell Sectoring](https://www.geeksforgeeks.org/computer-networks/cell-splitting-and-cell-sectoring/)
- [Cooper's Law / network densification (ResearchGate)](https://www.researchgate.net/figure/Martin-Coopers-assessment-of-Spectral-Efficiency-of-Wireless-Systems-Source_fig2_236410000)

**Satellite co-channel saturation (multi-source, via corpus):**
- [IEEE Xplore 10816533: Optimizing Beam Size in Multibeam LEO Satellite Networks](https://ieeexplore.ieee.org/document/10816533/) (full reuse -> severe inter-beam interference, degrades SINR)
- [arXiv 2501.02750: Spectrum Sharing in Satellite-Terrestrial Integrated Networks](https://arxiv.org/html/2501.02750v3) (overlapping co-channel beams reduce capacity)

**Antenna aperture / gain / beamwidth (textbook):**
- [Wikipedia: Parabolic antenna](https://en.wikipedia.org/wiki/Parabolic_antenna) (G = 4 pi eta A / lambda^2; aperture efficiency ~0.55-0.65)
- [Electronics Notes: Parabolic Reflector Antenna Gain and Directivity](https://www.electronics-notes.com/articles/antennas-propagation/parabolic-reflector-antenna/antenna-gain-directivity.php) (inverse gain-beamwidth relation)
- [RF Essentials: Aperture Efficiency of Parabolic Antennas](https://rfessentials.com/rf-knowledge-base/how-does-aperture-efficiency-affect-the-realized-gain-of-a-parabolic-dish-antenn/)

**Path loss (textbook):**
- [Wikipedia: Free-space path loss](https://en.wikipedia.org/wiki/Free-space_path_loss) (FSPL rises with frequency and distance)

---

## Claims ledger (COMM-426..450)

For the catalog/reconciliation step to ingest. Each hard claim with sources and tag. IDs COMM-426 through COMM-450 reserved for this doc (only COMM-426..439 used; COMM-440..450 held unused). Cross-references existing IDs heavily; this doc adds the external-sourcing-and-plain-language layer over numbers owned in the DTC corpus.

- **COMM-426**, Frequency (band, MHz/GHz) sets reach, channel bandwidth (slice width, MHz) sets the capacity ceiling, and data rate (Mbps) is bandwidth times a link-dependent efficiency; they are three distinct quantities, two quoted in MHz, and low frequency reaches better because path loss rises with frequency (FSPL = 20 log10(d) + 20 log10(f) + 92.45). [FACT, textbook] Sources: Wikipedia Free-space path loss; Waveform (low-band reach vs mmWave); cross-ref COMM-294.
- **COMM-427**, Shannon-Hartley C = B x log2(1+SNR) (C bits/sec, B Hz, SNR linear) sets the hard max error-free rate; rate is linear in bandwidth and only logarithmic in SNR; real systems reach ~60-80%. [FACT, textbook] Sources: Wikipedia Shannon-Hartley; RF Essentials; cross-ref COMM-041/315.
- **COMM-428**, Spectral efficiency = C/B = log2(1+SNR) bps/Hz depends only on link quality; real values LTE ~1.5 avg (peak ~15), 5G ~3 real/stream (peak ~23-30), DTC ~0.5-0.8 measured (Starlink) to ~3 claimed (AST). [FACT, multi-source] Sources: Techplayon; Waveform; arXiv 2312.00957; cross-ref COMM-114/409.
- **COMM-429**, Satellite-to-phone spectral efficiency is low (~0.5-0.8 bps/Hz Starlink-measured) because the phone is a weak terminal (~0.2 W into ~0 dBi) far away; the live network shows MEASURED median SINR 0 dB (SNR=1, ~1 bps/Hz natural ceiling). Most-cited measurement reports mean 0.79 / median 0.64; SMS-phase 0.52-0.61 is the same service at a lower reading; honest band ~0.5-0.8. [FACT, measured; spread flagged] Sources: arXiv 2506.00283 (median SINR 0 dB, mean 0.79 / median 0.64 verbatim); cross-ref COMM-293/294/337.
- **COMM-430**, "25 MHz -> 75 Mbps" is NOT a hard cap; it is rate = bandwidth x spectral efficiency at ~3 bps/Hz (25 x 3 = 75), the AST-claimed end; higher SNR yields more, lower DTC efficiency yields less. [DERIVED] Sources: arXiv 2506.18672 (AST 120 Mbps/40 MHz = 3 bps/Hz); cross-ref COMM-344/409.
- **COMM-431**, Honest per-cell range on 25 MHz for a real phone link: ~13-20 Mbps at ~0.5-0.8 bps/Hz (Starlink measured), ~37.5 at 1.5, ~50 at 2, ~75 at 3 (AST claimed); efficiency is the entire swing and 75 Mbps is the optimistic top, not a ceiling or floor. [DERIVED] Sources: arXiv 2506.00283; arXiv 2506.18672; cross-ref COMM-409/418.
- **COMM-432**, The 75 Mbps figure is PER CELL (single-phone-alone peak), not per user under load, and assumes 25 MHz cleanly owned; Starlink's measured service is 2x5 MHz shared PCS, hence single-digit Mbps beams; asserting 75 Mbps as a fixed ceiling is wrong in both directions. [DERIVED, corrects prior framing] Sources: cross-ref COMM-337/418; arXiv 2506.00283.
- **COMM-433**, Carrier aggregation (LTE-A Release 10+) lets ONE user receive/transmit on multiple component carriers simultaneously with rates SUMMING, up to 5 carriers / 100 MHz LTE-A (more in 5G); within a carrier the scheduler can assign one user many resource blocks, so a lightly loaded cell's single-device speed equals the full per-beam capacity; ceiling is total bandwidth. [FACT, standardized] Sources: 3GPP Carrier Aggregation; Wikipedia Carrier aggregation; 3GLTEInfo; cross-ref COMM-340.
- **COMM-434**, OFDM splits a channel into orthogonal subcarriers and OFDMA assigns subsets (resource blocks) to different users simultaneously: a MULTIPLE-ACCESS/sharing mechanism, NOT capacity creation; total bits/sec stays bandwidth x efficiency regardless of slicing (slicing changes neither B nor SNR). [FACT, textbook] Sources: TechTarget OFDMA; Mini-Circuits OFDM; cross-ref COMM-340/359/427.
- **COMM-435**, Total system capacity multiplies by frequency reuse: total = bandwidth x spectral efficiency x number of cells; more cells come from smaller cells (cell splitting), the dominant historical driver of wireless capacity (Cooper's Law). [FACT, textbook] Sources: GeeksforGeeks frequency reuse and cell splitting; Cooper's Law/densification; cross-ref COMM-413.
- **COMM-436**, For a satellite the cell is the beam, and the reuse multiplier (number of non-overlapping co-channel beams tiling an area) is set by beam footprint (aperture/altitude), NOT satellite count (AST ~2,500 beams at 223 m^2 / ~324 km^2; Starlink V2-mini 48); past tiling, more same-aperture satellites add overlapping co-channel beams that interfere rather than add capacity. [FACT mechanism, multi-source; structure from corpus] Sources: arXiv 2506.18672; IEEE Xplore 10816533; arXiv 2501.02750; cross-ref COMM-407/414/415.
- **COMM-437**, Antenna gain G = 4 pi eta A / lambda^2 (area A, efficiency ~0.55-0.65, wavelength lambda) rises linearly with area (double area = +3 dB), with an inverse gain-beamwidth relation (bigger aperture = narrower beam = smaller cell), so a bigger antenna raises both SNR and reuse at once. [FACT, textbook] Sources: Wikipedia Parabolic antenna; Electronics Notes parabolic gain/beamwidth; cross-ref COMM-296.
- **COMM-438**, More gain -> more SNR -> more bits/Hz (efficiency = log2(1+SNR)), so a bigger antenna can effectively use more bandwidth, climbing from the ~0.5-0.8 bps/Hz floor toward ~2-3; sensitivity +1 dB ~ 1.26x rate, +2 dB ~ 1.585x (corpus-corrected from an earlier 1.58x/+1 dB error). [DERIVED + FACT] Sources: Wikipedia Shannon-Hartley (efficiency = log2(1+SNR)); cross-ref COMM-349/356.
- **COMM-439**, Aperture's gain ENABLES higher altitude: a higher orbit covers more Earth (fewer satellites) but the longer link is weaker, and only more aperture closes it to a weak phone; altitude is a weak trim (~3.5-3.9 dB, 550->350 km) vs aperture's strong lever (~9.5 dB, 25->223 m^2), which is why AST uses ~223 m^2 to operate at a planned ~725-740 km and still deliver broadband. [FACT, sourced in corpus] Sources: arXiv 2506.18672 (223 m^2 / 42 dBi); cross-ref COMM-316/346/357.

---

*COMM-426..450 reserved for this doc (COMM-426..439 used; COMM-440..450 held unused). Catalog rows for LIBRARY.md / RESEARCH_TRACKER.md / SOURCE_INDEX.md are returned to the catalog/reconciliation agent, not edited here. This doc is not committed by this pass.*
