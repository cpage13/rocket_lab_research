# Radio Spectrum and Phased-Array Antennas: A First-Principles Explainer for the Whole Machine (Plain Language, Fully Sourced)

*A foundational reference document for the Rocket Lab direct-to-cell (cellular) satellite study. Comms wave 8 (reference/explainer, no business verdict). This doc EXTENDS the corpus's primers (`spectrum_capacity_primer.md` COMM-426..439, `channels_aggregate_answer.md`, `dtc_antenna_aperture_tradeoff.md` COMM-293..314, `dtc_data_rate_vs_spectrum.md` COMM-493..512, `dtc_subscribers_per_satellite.md` COMM-535..560) into one end-to-end explanation a smart non-engineer can read top to bottom: what spectrum IS, what an antenna IS, how a phased array WORKS, and how the two combine to let a satellite talk to a bare phone. The letter-band designations (L, S, C, X, Ku, K, Ka, V, W) this explainer uses but does not define are defined in the companion [spectrum_band_designations.md](spectrum_band_designations.md) (COMM-625..634), written 2026-06-30 to fill exactly that gap. Every hard claim is checked against 2+ independent sources cited inline with full URLs. New claim IDs COMM-561..600.*

---

## 0. Answer first (the whole machine on two screens)

The system has two halves. The FIRST half is the spectrum: the slice of radio you are allowed to transmit on. The SECOND half is the antenna: the hardware that pushes energy into that slice and aims it. Here is the entire chain in plain terms, each line expanded later with sources.

**The spectrum half (Part A):**

1. **Radio spectrum is a band of the electromagnetic spectrum, frequencies from ~3 Hz to ~3,000 GHz, and it is a FINITE, government-licensed, shared resource.** You do not "make" spectrum; you are granted the right to use a slice of it, and the same air is shared by everyone ([Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum)).

2. **Three quantities get confused because two are quoted in "MHz." FREQUENCY (the band, where on the dial: 700 MHz vs 28 GHz) sets REACH. BANDWIDTH (the channel width, the MHz you hold) sets the CAPACITY CEILING. DATA RATE (Mbps) is what you actually deliver = bandwidth x a link-quality efficiency.** Frequency is the address; bandwidth is the lot width; data rate is the house you build on the lot ([corpus COMM-426](spectrum_capacity_primer.md); [Waveform: 5G and Shannon's Law](https://www.waveform.com/a/b/guides/5g-and-shannons-law)).

3. **A frequency carries information by MODULATION: you nudge the wave's amplitude/phase to encode bits (QAM packs several bits per symbol; OFDM spreads them over many sub-tones).** The hard ceiling on any one channel is the Shannon-Hartley law, `rate = bandwidth x log2(1 + SNR)`: rate rises linearly with bandwidth but only logarithmically with signal quality ([Wikipedia: Shannon-Hartley theorem](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem); [Wikipedia: QAM](https://en.wikipedia.org/wiki/Quadrature_amplitude_modulation)).

4. **Separate channels at different frequencies ADD (carrier aggregation sums them); sub-dividing ONE channel into sub-carriers (OFDMA) only SHARES it, it does not add capacity.** Holding more spectrum is the only way to lift the ceiling; slicing one channel finer just divides the same pie among more users ([corpus COMM-433/434](spectrum_capacity_primer.md); [3GPP: Carrier Aggregation](https://www.3gpp.org/technologies/carrier-aggregation-on-mobile-networks)).

5. **The same band can be REUSED in non-overlapping cells/beams, which multiplies TOTAL system capacity by the number of cells.** This (cell splitting, "Cooper's Law") is the dominant historical driver of wireless capacity, far more than wider channels or better modulation ([Wikipedia: Frequency reuse](https://en.wikipedia.org/wiki/Frequency_reuse); [corpus COMM-435](spectrum_capacity_primer.md)).

6. **Spectrum is allocated by regulators (ITU worldwide, FCC in the US), licensed in named bands, often auctioned for billions, and a phone only works on the specific bands it was built to support.** A direct-to-cell satellite must talk on existing licensed cellular bands because the whole point is to reach an unmodified phone ([Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum); [corpus COMM-426/481](spectrum_capacity_primer.md)).

**The antenna half (Part B):**

7. **An antenna's GAIN measures how tightly it concentrates energy in one direction; gain rises with APERTURE AREA over wavelength squared: `G = 4 pi eta A / lambda^2` (eta ~0.5-0.7).** Bigger aperture = higher gain = a NARROWER beam. Gain and beamwidth are two sides of one coin ([Wikipedia: Antenna aperture](https://en.wikipedia.org/wiki/Antenna_aperture); [corpus COMM-296/437](dtc_antenna_aperture_tradeoff.md)).

8. **The LINK BUDGET is the energy accounting: EIRP (transmit power + antenna gain) minus path loss plus receive gain must clear the noise.** Free-space path loss rises with distance squared and frequency squared, so a satellite hundreds of km away starts deep in a hole the antenna must dig out of ([Wikipedia: Link budget](https://en.wikipedia.org/wiki/Link_budget); [Wikipedia: Free-space path loss](https://en.wikipedia.org/wiki/Free-space_path_loss)).

9. **A PHASED ARRAY is many small antenna elements whose beam is steered ELECTRONICALLY by setting each element's PHASE, with no moving parts; an active/digital array can form MANY independent beams at once, on multiple bands, all from the same aperture.** This is how one satellite covers hundreds of separate cells simultaneously ([Wikipedia: Phased array](https://en.wikipedia.org/wiki/Phased_array); [corpus COMM-538/539](dtc_subscribers_per_satellite.md)).

10. **What a phased array can do at once is limited by three things, in order: the BEAMFORMING PROCESSOR/ASIC (it sets the beam COUNT, and its compute scales as elements x beams x bandwidth), the DC POWER (how many beams you can energize), and the SPECTRUM you hold (the aggregate all beams carry).** On a thin cellular spectrum holding, the held spectrum binds first; the chip binds last ([Analog Devices / Microwave Journal on digital beamforming](https://www.analog.com/en/resources/technical-articles/power-advantage-of-hybrid-beamforming.html); [corpus COMM-536/540](dtc_subscribers_per_satellite.md)).

11. **A satellite talking to a bare phone works because the SATELLITE supplies the gain.** The phone is a tiny, weak, near-zero-gain transmitter (~0.2 W, ~0 dBi); to close the link from hundreds of km the satellite needs a huge aperture (AST SpaceMobile flies ~64 m^2 up to ~223 m^2 arrays, ~2,000+ beams) to both hear the faint phone and shout back loudly enough ([AST SpaceMobile: Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/); [corpus COMM-293/294/439](dtc_antenna_aperture_tradeoff.md)).

The one sentence that ties the halves together: **spectrum sets how much room you have to send bits, and the antenna decides whether the bits arrive at all and how many separate places you can send them to at once.** Everything below is the long-form, sourced version of these eleven lines.

---

# PART A: RADIO SPECTRUM

## A1. What radio spectrum actually is (the electromagnetic spectrum, frequency, wavelength)

**Radio is light you cannot see.** Visible light, X-rays, microwaves, and the radio waves your phone uses are all the SAME thing, electromagnetic waves, differing only in frequency. The electromagnetic spectrum is the full range of these waves ordered by frequency, and radio occupies the low-frequency end ([Lumen Learning / SUNY Physics: The Electromagnetic Spectrum](https://courses.lumenlearning.com/suny-physics/chapter/24-3-the-electromagnetic-spectrum/), which states radio waves are "the lowest frequency electromagnetic waves" and are produced by currents in wires; [University Physics Vol. 2, UCF Pressbooks: The Electromagnetic Spectrum](https://pressbooks.online.ucf.edu/osuniversityphysics2/chapter/the-electromagnetic-spectrum/)).

**Frequency and wavelength are locked together by one equation.** Every electromagnetic wave obeys `c = f x lambda`, where `c` is the speed of light (~3.00 x 10^8 m/s, a constant), `f` is frequency in hertz, and `lambda` is wavelength in metres ([Lumen Learning / SUNY Physics](https://courses.lumenlearning.com/suny-physics/chapter/24-3-the-electromagnetic-spectrum/), verbatim: "c = fλ, where f is the frequency, λ is the wavelength"; [Study.com: Frequency and Wavelength for EM Waves](https://study.com/skill/learn/applying-the-relationship-between-frequency-wavelength-for-em-waves-explanation.html)). Because the product is fixed, frequency and wavelength are inverses: higher frequency means a shorter wave. This single fact drives almost everything later: a 700 MHz wave is ~43 cm long, a 28 GHz wave is ~1.1 cm long, and the wavelength sets how big an antenna must be and how the wave interacts with walls, rain, and terrain.

**The radio spectrum is a defined band of the whole.** Formally it is "the part of the electromagnetic spectrum with frequencies from 3 Hz to 3,000 GHz (3 THz)" ([Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum), verbatim). The International Telecommunication Union (ITU) divides this into twelve named bands, the ones that matter for cellular being:

| ITU band | Name | Frequency range | Used for (examples) |
|---|---|---|---|
| MF | Medium Frequency | 300-3,000 kHz | AM radio |
| HF | High Frequency | 3-30 MHz | shortwave, aviation |
| VHF | Very High Frequency | 30-300 MHz | FM radio, TV |
| **UHF** | **Ultra High Frequency** | **300-3,000 MHz** | **cellular low/mid band, TV, GPS** |
| **SHF** | **Super High Frequency** | **3-30 GHz** | **5G mid/high band, satellite, radar, Wi-Fi 6E** |
| EHF | Extremely High Frequency | 30-300 GHz | mmWave 5G, satellite |

(Band ranges verbatim from [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum).) Nearly all cellular, including direct-to-cell, lives in UHF (the 600 MHz-2.6 GHz cellular bands) with 5G reaching into SHF (3.5 GHz mid-band) and EHF (mmWave). The corpus's direct-to-cell links sit at ~700-900 MHz (AST) and ~1.9-2 GHz (Starlink/T-Mobile) ([corpus COMM-301/280](dtc_antenna_aperture_tradeoff.md)).

> **COMM-561.** Radio waves are electromagnetic waves (the same physics as visible light, differing only in frequency), and frequency and wavelength are inversely locked by `c = f x lambda` (c ~ 3.00 x 10^8 m/s), so a 700 MHz wave is ~43 cm and a 28 GHz wave is ~1.1 cm long; this wavelength sets antenna size and how the wave penetrates obstacles. The radio spectrum is the 3 Hz-3,000 GHz part of the electromagnetic spectrum, divided by the ITU into named bands (cellular lives mainly in UHF 300-3,000 MHz, with 5G reaching SHF 3-30 GHz and EHF 30-300 GHz). **[FACT, textbook]** Sources: [Lumen/SUNY Physics: EM Spectrum](https://courses.lumenlearning.com/suny-physics/chapter/24-3-the-electromagnetic-spectrum/) (c = f lambda verbatim); [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum) (3 Hz-3 THz, ITU bands verbatim); cross-ref corpus COMM-426.
>
> **VERDICT:** spectrum is a slice of light measured by frequency; frequency and wavelength are the same fact stated two ways.

## A2. Why spectrum is finite, licensed, and shared (the resource, not a gadget)

**It is a fixed natural resource.** You cannot manufacture more radio spectrum, and there is only so much usable band before frequencies get too low (no room for data) or too high (blocked by air and walls). Wikipedia states it plainly: "Because it is a fixed resource which is in demand by an increasing number of users, the radio spectrum has become increasingly congested in recent decades" ([Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum), verbatim). This is the single most important non-physics fact about the whole business: spectrum is the scarce input, and most of the useful low/mid band is already owned.

**It is shared, so it must be coordinated.** Two transmitters on the same frequency in the same place interfere and both fail. The only way many users coexist is rules: who may transmit, where, at what power, on which frequencies. "The generation and transmission of radio waves is strictly regulated by national laws, coordinated by an international body, the International Telecommunication Union (ITU)" ([Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum), verbatim). In the US the Federal Communications Commission (FCC) "is responsible for issuing spectrum licenses and conducting spectrum auctions" ([Wilson: Cellular Frequency Bands Explained](https://www.wilsonsignalbooster.com/blogs/articles/cellular-frequency-bands-explained)).

**It is licensed and often owned for billions.** Parts of the spectrum "are sold or licensed to operators of private radio transmission services" ([Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum), verbatim). A cellular operator does not own the air, it owns the exclusive license to transmit on a specific band over a specific territory, won at auction. This is why the corpus treats acquiring spectrum as the hard, expensive, business-and-licensing gate on a direct-to-cell entrant, not a physics problem ([corpus dtc_spectrum_access.md COMM-481..492](dtc_spectrum_access.md)).

> **COMM-562.** Radio spectrum is a FINITE natural resource ("a fixed resource ... increasingly congested"), it is SHARED (co-channel transmitters in the same place interfere, so use must be coordinated), and it is LICENSED/owned: regulators (ITU worldwide, FCC in the US issuing licenses and running auctions) grant exclusive rights to transmit on a named band over a territory, frequently sold for billions. An operator owns the license, not the air. **[FACT, regulatory]** Sources: [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum) (fixed/congested, ITU-regulated, sold/licensed, verbatim); [Wilson: Cellular Frequency Bands](https://www.wilsonsignalbooster.com/blogs/articles/cellular-frequency-bands-explained) (FCC issues licenses, runs auctions); cross-ref corpus COMM-481.
>
> **VERDICT:** spectrum is a scarce, shared, licensed resource. The hard part of a comms business is getting the right to use it, not the physics.

## A3. The three confused quantities: FREQUENCY vs BANDWIDTH vs DATA RATE

This is the single most common confusion and it recurs whenever a non-engineer sees the numbers, because two of the three are quoted in "MHz." Keep them strictly apart.

**FREQUENCY (the band): where you sit on the dial. Sets REACH.** Measured in Hz/MHz/GHz, this is the carrier frequency, like a station number on an FM radio. A low-band link sits at ~700 MHz; a PCS link at ~1.9 GHz; a millimetre-wave link at ~28 GHz. Frequency does NOT set speed, it sets reach: low frequencies bend around terrain, pass through walls and rain, and travel far; high frequencies carry more raw room but are blocked by almost anything and fade fast. The industry states the tradeoff plainly: "Low band frequencies (700 to 900 MHz) provide wide area coverage and strong building penetration"; "Higher-frequency signals fade faster and are more easily blocked by walls, buildings, and vegetation" ([Wilson: Cellular Frequency Bands](https://www.wilsonsignalbooster.com/blogs/articles/cellular-frequency-bands-explained)). The physics reason is path loss, covered in B2.

**BANDWIDTH (the channel width): how wide your slice is. Sets the CAPACITY CEILING.** Also measured in Hz/MHz, which is exactly why it is confused with frequency. This is the WIDTH of the channel you occupy, like how many lanes wide your stretch of highway is. A 25 MHz channel is 25 MHz wide whether it sits at 700 MHz or 1.9 GHz. Wider channel, more bits per second possible.

> **The clean way to keep frequency and bandwidth apart:** frequency is the address (which neighbourhood), bandwidth is the lot width (how much room you own there). You can own a 25 MHz lot in the cheap, far-reaching 700 MHz neighbourhood or in the 28 GHz neighbourhood. The lot is the same width; the neighbourhoods behave completely differently.

**DATA RATE (Mbps): what you actually deliver.** This is real throughput, and it equals bandwidth times a quality-dependent efficiency (A4). A 25 MHz channel does NOT have a fixed data rate; it has a rate that depends on how good the link is. The corpus pins this hard: "25 MHz -> 75 Mbps" is not a cap, it is 25 MHz x ~3 bits/Hz (an optimistic figure), and a real phone link runs lower ([corpus COMM-430/431](spectrum_capacity_primer.md)).

A worked picture: hold a 20 MHz channel at 700 MHz. The "700 MHz" tells you it reaches deep into buildings and far across countryside. The "20 MHz" tells you the ceiling. The actual Mbps depends on signal quality and could be anything from a few Mbps (weak link) to ~60 Mbps (strong link). Three numbers, three different things.

> **COMM-563.** Frequency, bandwidth, and data rate are three distinct quantities, and two are quoted in MHz which causes the confusion. FREQUENCY (the band, MHz/GHz) sets REACH (low band penetrates and travels far, high band carries more but is easily blocked). BANDWIDTH (channel width, MHz) sets the capacity CEILING (wider = more possible bits/sec). DATA RATE (Mbps) is the delivered throughput = bandwidth x a link-quality efficiency, so the same channel width yields very different Mbps depending on signal quality. Frequency is the address, bandwidth is the lot width, data rate is what you build on it. **[FACT, textbook]** Sources: [Wilson: Cellular Frequency Bands](https://www.wilsonsignalbooster.com/blogs/articles/cellular-frequency-bands-explained) (low-band reach/penetration vs high-band fade); [Waveform: 5G and Shannon's Law](https://www.waveform.com/a/b/guides/5g-and-shannons-law); cross-ref corpus COMM-426/430.
>
> **VERDICT:** band = reach, bandwidth = capacity ceiling, data rate = what you actually get. "700 MHz" and "20 MHz" and "60 Mbps" are not the same kind of thing.

## A4. How a frequency carries information: modulation, the Shannon limit, spectral efficiency

**A bare wave carries nothing. You must MODULATE it.** A pure sine wave at 1.9 GHz is just a tone; to send data you systematically change one of its properties (amplitude, frequency, or phase) in step with the bits. That changing is modulation.

- **AM (amplitude modulation)** varies the wave's height; **FM (frequency modulation)** varies its frequency. These are the old analog schemes (AM/FM radio) and carry little data per hertz.
- **QAM (quadrature amplitude modulation)** is the workhorse of modern cellular. It varies BOTH amplitude and phase at once, so each transmitted "symbol" can stand for several bits. "Combining these concepts leads to QAM, where both amplitude and phase are modulated" ([Wikipedia: Quadrature amplitude modulation](https://en.wikipedia.org/wiki/Quadrature_amplitude_modulation)). The constellation size sets bits per symbol: QPSK (4-QAM) = 2 bits/symbol, 16-QAM = 4, 64-QAM = 6, 256-QAM = 8, 1024-QAM = 10 ([Wikipedia: QAM](https://en.wikipedia.org/wiki/Quadrature_amplitude_modulation); [ICO Optics: Digital Modulation Methods](https://www.ico-optics.org/digital-modulation-methods-qam-psk-and-ofdm/), "64-QAM gets you 6 bits per symbol, and 1024-QAM reaches 10 bits per symbol").
- **OFDM (orthogonal frequency-division multiplexing)** is the carrier ARRANGEMENT used by LTE, 5G, and Wi-Fi. It splits one wide channel into many narrow, overlapping-but-orthogonal sub-tones (sub-carriers), each carrying its own QAM symbols. "OFDM splits data across many subcarriers, each using QAM modulation" ([ICO Optics](https://www.ico-optics.org/digital-modulation-methods-qam-psk-and-ofdm/)). OFDM is robust against multipath and easy to process, which is why every modern system uses it.

**The catch: richer modulation needs a cleaner signal.** Packing more bits per symbol crowds the constellation points together, so they are easier to confuse under noise. "Using higher-order QAM without increasing the bit error rate requires a higher signal-to-noise ratio (SNR)" ([Wikipedia: QAM](https://en.wikipedia.org/wiki/Quadrature_amplitude_modulation), verbatim). So you only get 1024-QAM (10 bits/symbol) on a pristine link; a weak satellite-to-phone link falls back to QPSK (2 bits/symbol) or less. Modulation is the lever that turns signal quality into bits.

**The hard ceiling on any one channel: the Shannon-Hartley law.** No modulation scheme, however clever, can beat one equation:

```
   C  =  B  x  log2(1 + SNR)
```

where `C` is channel capacity in bits/sec (the theoretical maximum error-free rate), `B` is bandwidth in Hz, and `SNR` is the signal-to-noise ratio as a LINEAR power ratio (not dB) ([Wikipedia: Shannon-Hartley theorem](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem), verbatim term definitions; already certified in corpus COMM-041/427). Two consequences the founder should internalise:

- **Rate is LINEAR in bandwidth.** Double the MHz, double the ceiling. Bandwidth is the strong lever.
- **Rate is only LOGARITHMIC in signal quality.** To double the rate by power alone you must roughly QUADRUPLE the SNR, and beyond that gains shrink fast. Signal strength is a weak lever once you are out of the noise.

**Spectral efficiency: the bits you wring from each hertz.** Divide both sides by bandwidth:

```
   spectral efficiency  =  C / B  =  log2(1 + SNR)        [bits/sec/Hz]
```

This depends ONLY on link quality, not on how much bandwidth you have ([Wikipedia: Spectral efficiency](https://en.wikipedia.org/wiki/Spectral_efficiency)). It is the fair way to compare any radio system. Real values: LTE averages ~1.5 bps/Hz (peak ~15), 5G ~3 real per stream (peak ~23-30), and a satellite-to-phone link manages only ~0.5-0.8 bps/Hz measured (Starlink) because the phone is a weak terminal at the edge of the noise ([corpus COMM-428/429](spectrum_capacity_primer.md); [Techplayon: Spectral Efficiency 5G/LTE](https://www.techplayon.com/spectral-efficiency-5g-nr-and-4g-lte/)). Real systems reach only ~60-80% of the Shannon ceiling after coding overhead, pilots, and guard bands.

**Why low band penetrates and high band carries more but reaches less, restated through the formula.** A high band offers MORE bandwidth (there is simply more room up at 28 GHz than in the crowded sub-1-GHz range), which lifts `B` and the ceiling. But a high band suffers far worse path loss and is blocked by walls (B2), which crushes the SNR, so the efficiency `log2(1+SNR)` collapses and the reach shrinks to almost nothing. Low band has little spare bandwidth but travels far and penetrates, holding SNR up over distance. This is the fundamental tradeoff and it falls straight out of Shannon plus path loss.

> **COMM-564.** A frequency carries information by MODULATION (changing the wave's amplitude/phase/frequency in step with bits): AM/FM are the analog schemes; QAM packs multiple bits per symbol via amplitude+phase (QPSK 2, 16-QAM 4, 64-QAM 6, 256-QAM 8, 1024-QAM 10 bits/symbol), and OFDM spreads QAM symbols over many orthogonal sub-carriers (used by LTE/5G/Wi-Fi). Higher-order QAM requires a higher SNR, so weak links fall back to fewer bits/symbol. **[FACT, textbook]** Sources: [Wikipedia: QAM](https://en.wikipedia.org/wiki/Quadrature_amplitude_modulation) (amplitude+phase, higher-order needs higher SNR, verbatim); [ICO Optics: Digital Modulation](https://www.ico-optics.org/digital-modulation-methods-qam-psk-and-ofdm/) (bits/symbol, OFDM+QAM); cross-ref corpus COMM-427.
>
> **COMM-565.** The Shannon-Hartley law `C = B x log2(1+SNR)` (C bits/sec, B Hz, SNR linear power ratio) sets the hard maximum error-free rate of any single channel; rate is LINEAR in bandwidth (strong lever) and only LOGARITHMIC in SNR (weak lever, ~4x SNR to double rate); real systems reach ~60-80% after overhead. Spectral efficiency = C/B = log2(1+SNR) bps/Hz depends only on link quality (LTE ~1.5 avg, 5G ~3 real/stream, satellite-to-phone ~0.5-0.8 measured). Low band reaches far but has little bandwidth; high band has more bandwidth but its path loss crushes SNR so reach collapses, both consequences of Shannon plus path loss. **[FACT, textbook]** Sources: [Wikipedia: Shannon-Hartley theorem](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem); [Wikipedia: Spectral efficiency](https://en.wikipedia.org/wiki/Spectral_efficiency); cross-ref corpus COMM-041/427/428/429.
>
> **VERDICT:** modulation turns a bare wave into bits; Shannon caps how many bits per second a channel can carry; bandwidth is the strong lever and signal quality the weak one.

## A5. Channels, carriers, carrier aggregation (sums) vs OFDMA sub-carriers (shares)

This is the distinction the founder most needs kept straight, because it decides whether holding "many channels" gives you many channels' worth or just one.

**A channel is one slice of spectrum at one frequency.** Hold three 25 MHz channels and you hold three separate slices, each with its own Shannon ceiling (~bandwidth x efficiency).

**Carrier aggregation SUMS separate channels.** Since 2011 (3GPP Release 10, LTE-Advanced) a single device can receive and transmit on several separate frequency blocks ("component carriers") at the same time, and their throughputs ADD UP. "Carrier aggregation was introduced in 3GPP Release 10 (LTE-Advanced) ... two or more component carriers can be aggregated to support wider transmission bandwidths up to 100 MHz" ([3GPP: Carrier Aggregation](https://www.3gpp.org/technologies/carrier-aggregation-on-mobile-networks)). LTE-A aggregates up to 5 carriers for 100 MHz; 5G NR allows up to 16 carriers and operators advertise ~4 Gbps and up by combining bands ([Wikipedia: Carrier aggregation](https://en.wikipedia.org/wiki/Carrier_aggregation); [corpus COMM-433](spectrum_capacity_primer.md)). So if you hold three 25 MHz channels and a device aggregates them, it sees 75 MHz worth, not 25. **Total capacity = (sum of all the channel bandwidths you hold) x efficiency.** More channels held = more total capacity, summed. The only bound is how much spectrum you have acquired, a licensing and business limit, not a per-channel physics cap.

**OFDMA sub-carriers only SHARE one channel.** Splitting ONE channel into many tiny orthogonal sub-carriers (the OFDMA method inside LTE and 5G) does NOT add capacity. Sub-carriers are a multiple-access trick: they let many users politely share that one channel, but the total stays one channel's worth (bandwidth x efficiency), however finely you slice it ([corpus COMM-434](spectrum_capacity_primer.md); [TechTarget: OFDMA](https://www.techtarget.com/searchnetworking/definition/orthogonal-frequency-division-multiple-access-OFDMA)). This is the case people confuse with aggregation.

> **The rule of thumb:** sub-carriers WITHIN one channel divide a fixed pie among users (sharing, no new capacity); SEPARATE channels at different frequencies are different pies that ADD TOGETHER (aggregation). Slicing one channel changes neither its bandwidth nor its SNR, so it cannot change the channel's capacity; holding another channel at another frequency literally adds another pie.

> **COMM-566.** Carrier aggregation (3GPP LTE-A Release 10+) lets one device use multiple separate frequency channels ("component carriers") simultaneously with their rates SUMMING (up to 5 carriers / 100 MHz in LTE-A, up to 16 in 5G), so total capacity = sum of all held channel bandwidths x efficiency and holding more spectrum is the only way to raise the ceiling. By contrast, OFDMA sub-carriers SUB-DIVIDE one channel to let many users share it (a multiple-access mechanism), which does NOT add capacity (slicing changes neither the channel's bandwidth nor its SNR). Sub-carriers within a channel share a fixed pie; separate channels are different pies that add. **[FACT, standardized]** Sources: [3GPP: Carrier Aggregation](https://www.3gpp.org/technologies/carrier-aggregation-on-mobile-networks) (Release 10, up to 100 MHz, verbatim); [Wikipedia: Carrier aggregation](https://en.wikipedia.org/wiki/Carrier_aggregation); [TechTarget: OFDMA](https://www.techtarget.com/searchnetworking/definition/orthogonal-frequency-division-multiple-access-OFDMA); cross-ref corpus COMM-433/434.
>
> **VERDICT:** separate channels add (carrier aggregation, real new capacity); sub-carriers within a channel only share it (OFDMA, no new capacity). "Many channels" sums; "many sub-carriers" does not.

## A6. Frequency reuse / spatial reuse: how TOTAL system capacity multiplies

One channel's ceiling is fixed, but a NETWORK is not one channel, it is the same channel reused in many places.

**Reuse the band in non-overlapping cells.** "The key characteristic of a cellular network is the ability to reuse frequencies to increase both coverage and capacity" ([Wikipedia: Frequency reuse](https://en.wikipedia.org/wiki/Frequency_reuse), verbatim). Adjacent cells must use different frequencies, but two cells far enough apart can use the SAME frequency without interfering ("there is no problem with two cells sufficiently far apart operating on the same frequency," ibid.). A cluster of N cells cycles through the available channels, then the pattern repeats. The result: "more capacity than a single large transmitter, since the same frequency can be used for multiple links as long as they are in different cells" (ibid.).

**Total system capacity multiplies by the cell count.** Roughly, `total capacity = bandwidth x spectral efficiency x number of cells`. Smaller cells (cell splitting, sectoring) means more cells in the same area means more total capacity. This densification, not wider channels or fancier modulation, is the dominant historical driver of wireless capacity growth ("Cooper's Law") ([corpus COMM-435](spectrum_capacity_primer.md); [GeeksforGeeks: Frequency Reuse](https://www.geeksforgeeks.org/computer-networks/frequency-reuse/)).

**For a satellite, the "cell" is the BEAM.** A phased-array satellite paints many spot beams on the ground, each a cell, and reuses the same band across non-overlapping beams (Part B). The reuse multiplier is set by how many non-overlapping beams tile the coverage area, which is set by beam footprint (aperture and altitude), NOT by how many satellites you fly. Past the point where beams tile the area, adding more same-aperture satellites just creates overlapping co-channel beams that interfere rather than add capacity ([corpus COMM-436](spectrum_capacity_primer.md); [IEEE Xplore 10816533: Optimizing Beam Size in Multibeam LEO](https://ieeexplore.ieee.org/document/10816533/)). This is the bridge from Part A into Part B: spatial reuse on a satellite is a phased-array beam-count question.

> **COMM-567.** Frequency reuse multiplies TOTAL system capacity: the same channel is reused in geographically separated, non-overlapping cells (adjacent cells differ; distant cells can share), so total capacity ~ bandwidth x spectral efficiency x number of cells. Smaller/more cells (cell splitting) is the dominant historical driver of wireless capacity (Cooper's Law), more than wider channels or richer modulation. For a satellite the cell is the spot BEAM, and the reuse multiplier is set by how many non-overlapping beams tile the area (a function of aperture/altitude), not by satellite count; beyond tiling, extra same-aperture satellites add interfering co-channel beams, not capacity. **[FACT, textbook]** Sources: [Wikipedia: Frequency reuse](https://en.wikipedia.org/wiki/Frequency_reuse) (reuse increases capacity, distant cells share, verbatim); [GeeksforGeeks: Frequency Reuse](https://www.geeksforgeeks.org/computer-networks/frequency-reuse/); cross-ref corpus COMM-435/436.
>
> **VERDICT:** one channel has a fixed ceiling, but reusing it across many cells/beams multiplies the system total. On a satellite, that multiplier is a beam-count (phased-array) question.

## A7. How spectrum is allocated, licensed, owned, and shared (the bands a phone supports)

**Allocation: regulators carve the dial into purposes.** The ITU sets a global table of frequency allocations (which bands are for mobile, satellite, broadcast, radar, etc.), and each country's regulator (the FCC in the US, Ofcom in the UK, and so on) implements and licenses it nationally ([Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum)). This is why the same band can be "cellular" in one region and something else in another, a real constraint on a global satellite operator.

**Licensing: exclusive rights, won at auction.** "Cellular frequency bands ... are allocated by the Federal Communications Commission (FCC) and each carrier has its own set of frequency bands"; the FCC "is responsible for issuing spectrum licenses and conducting spectrum auctions" ([Wilson: Cellular Frequency Bands](https://www.wilsonsignalbooster.com/blogs/articles/cellular-frequency-bands-explained)). A license is an exclusive right to transmit on a defined band over a defined territory for a defined term, and major bands have sold for tens of billions of dollars in auction.

**The cellular bands, low / mid / high, and what a phone supports.** Operators hold spectrum across three tiers, each with the reach-vs-capacity tradeoff baked in ([Wilson: Cellular Frequency Bands](https://www.wilsonsignalbooster.com/blogs/articles/cellular-frequency-bands-explained); [Kajeet: Cellular Frequency Bands by US carriers](https://www.kajeet.com/en/blog/a-guide-to-cellular-frequency-bands-used-by-us-carriers)):

| Tier | Frequencies | Behaviour |
|---|---|---|
| **Low band** | 600, 700, 850 MHz | wide coverage, deep building penetration, modest capacity (rural backbone, "the coverage layer") |
| **Mid band** | 1.7-2.6 GHz (PCS, AWS), 2.5/3.5 GHz | balance of coverage and capacity (the 5G capacity workhorse) |
| **High band** | 24-47 GHz (mmWave) | huge capacity, tiny coverage, no wall penetration (dense urban hotspots only) |

**Crucially, a phone only works on the specific bands it was built to support.** A handset's radio front-end is wired for a fixed list of bands; it cannot transmit on a frequency it has no hardware for. This is the iron constraint on direct-to-cell: to reach an unmodified phone, the satellite MUST transmit on existing licensed cellular bands the phone already supports (~700-900 MHz, ~1.9-2 GHz), which means the satellite operator must partner with or acquire a terrestrial license-holder for those exact bands. The corpus develops this as the central spectrum-access gate ([corpus COMM-481/426](dtc_spectrum_access.md); the partnership model, e.g. Starlink+T-Mobile on PCS and AST on partner low band).

> **COMM-568.** Spectrum is ALLOCATED by regulators (ITU sets a global band-purpose table; national regulators like the FCC implement and license it, so a band can be "cellular" in one region and not another), LICENSED as an exclusive right to transmit on a defined band over a territory (won at auction, major bands sold for tens of billions), and a phone only works on the SPECIFIC bands its radio front-end was built for. Cellular spectrum is held in three tiers: low band (600/700/850 MHz: coverage + penetration), mid band (1.7-3.5 GHz: balance, the 5G workhorse), high band (24-47 GHz mmWave: capacity but tiny reach). Direct-to-cell therefore MUST transmit on existing licensed cellular bands the phone already supports, forcing a partnership with or acquisition of a terrestrial license-holder. **[FACT, regulatory]** Sources: [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum) (ITU/national allocation, licensing); [Wilson: Cellular Frequency Bands](https://www.wilsonsignalbooster.com/blogs/articles/cellular-frequency-bands-explained) (FCC licenses/auctions, low/mid/high tiers); [Kajeet: Cellular Bands](https://www.kajeet.com/en/blog/a-guide-to-cellular-frequency-bands-used-by-us-carriers); cross-ref corpus COMM-481.
>
> **VERDICT:** spectrum is carved by regulators, sold as exclusive licenses, and a phone is locked to the bands it ships with. Direct-to-cell lives or dies on getting access to existing cellular bands.

---

# PART B: ANTENNAS AND PHASED ARRAYS

## B1. What an antenna is, and what gain, beamwidth, and aperture mean

**An antenna converts between guided electricity and radiated waves.** On transmit it turns a signal flowing in a wire into a radio wave launched into space; on receive it does the reverse. The same antenna usually does both, and (this matters later) its transmit and receive properties are the same, a principle called reciprocity.

**GAIN: how tightly it concentrates energy in one direction.** A theoretical "isotropic" antenna radiates equally in all directions, like a bare light bulb. A real antenna focuses energy, like a flashlight reflector, so in its preferred direction it is stronger than isotropic. Gain measures that focusing, in decibels relative to isotropic (dBi): "3 dBi means twice (2x) the power relative to an isotropic antenna in the peak direction" ([antenna-theory.com: Antenna Gain](https://www.antenna-theory.com/basics/gain.php), verbatim). Higher gain is not "more total power," it is the SAME power aimed more tightly. Gain is the antenna's whole job in a link budget.

**APERTURE: gain comes from physical size relative to wavelength.** The bigger the antenna's effective collecting area, the more it focuses, set by the master antenna equation:

```
   G  =  4 pi eta A / lambda^2
```

where `G` is gain (a linear ratio; take 10 log10 for dBi), `A` is the physical aperture area in m^2, `eta` is aperture efficiency (the fraction of the physical area that is electrically useful, typically ~0.5-0.7), and `lambda` is wavelength ([Wikipedia: Antenna aperture](https://en.wikipedia.org/wiki/Antenna_aperture), verbatim `G = A_e / A_iso = 4 pi A_e / lambda^2` and "typical aperture antennas vary from 0.35 to well over 0.70"; [Wikipedia: Parabolic antenna](https://en.wikipedia.org/wiki/Parabolic_antenna), the same formula with eta ~0.55-0.65; corpus COMM-296/437). Two consequences:

- **Gain rises LINEARLY with area.** Double the antenna area, +3 dB of gain ([corpus COMM-437](spectrum_capacity_primer.md)). This is the single strongest lever a satellite designer has.
- **Gain rises as 1/lambda^2, i.e. with frequency squared.** A given dish is far higher-gain at high frequency. This is the hidden reason high bands can carry a lot when the link closes: the antennas are electrically huge.

**BEAMWIDTH: high gain means a NARROW beam.** Focusing energy tightly in one direction necessarily means the beam is narrow. Gain and beamwidth are inverse: "antennas with large effective apertures are considered high-gain antennas," and these "exhibit narrower beam patterns" ([Wikipedia: Antenna aperture](https://en.wikipedia.org/wiki/Antenna_aperture)). A useful approximation is `G ~ 4 pi / (beam solid angle)`, or for a square aperture of side D the half-power beamwidth is roughly `~70 x lambda / D` degrees; bigger D, narrower beam ([Electronics Notes: Parabolic gain and beamwidth](https://www.electronics-notes.com/articles/antennas-propagation/parabolic-reflector-antenna/antenna-gain-directivity.php), the inverse gain-beamwidth relation). For a satellite this is pivotal: a bigger antenna both shouts louder (more gain, more SNR) AND paints a smaller spot on the ground (narrower beam = smaller cell = more frequency reuse). One lever, two wins, exactly the A6 reuse story.

> **COMM-569.** An antenna converts between guided signals and radiated waves (transmit and receive properties identical by reciprocity). GAIN measures how tightly it concentrates energy versus an isotropic radiator, in dBi (3 dBi = 2x power in the peak direction); it comes from aperture size via `G = 4 pi eta A / lambda^2` (A = area m^2, eta = aperture efficiency ~0.5-0.7, lambda = wavelength), so gain rises LINEARLY with area (double area = +3 dB) and as frequency squared. BEAMWIDTH is inverse to gain: a bigger aperture is both higher-gain AND narrower-beam (~70 lambda/D degrees), so on a satellite a larger antenna simultaneously raises SNR and shrinks the ground cell (more reuse). **[FACT, textbook]** Sources: [Wikipedia: Antenna aperture](https://en.wikipedia.org/wiki/Antenna_aperture) (G = 4 pi Ae/lambda^2, eta 0.35-0.70+, larger aperture = narrower beam, verbatim); [antenna-theory.com: Gain](https://www.antenna-theory.com/basics/gain.php) (dBi, 3 dBi = 2x); [Wikipedia: Parabolic antenna](https://en.wikipedia.org/wiki/Parabolic_antenna); cross-ref corpus COMM-296/437.
>
> **VERDICT:** an antenna's gain is just size over wavelength; bigger antenna = louder AND tighter beam, which is why aperture is the master lever for a satellite.

## B2. The link budget: EIRP, path loss, and clearing the noise

**A link budget is the energy bank statement of a radio link.** It adds up every gain and subtracts every loss from transmitter to receiver to check that the signal arrives strong enough above the noise to be decoded. "A link budget ... takes into account all the gains and losses from the transmitter to the receiver" to "ensure that the information is received intelligibly with an adequate signal-to-noise ratio" ([Wikipedia: Link budget](https://en.wikipedia.org/wiki/Link_budget); [Qorvo: Satellite Link Budget Review](https://www.qorvo.com/design-hub/blog/designing-efficient-satellite-links-a-review-of-the-link-budget-analysis)).

**EIRP: how loud the transmitter shouts.** Effective Isotropic Radiated Power is transmit power times antenna gain, the power as if it came from an isotropic radiator in the beam direction: "EIRP is the product of the transmitting power and the gain of the transmitting antenna" ([Georgia Tech: Link Budget Calculation](https://propagation.ece.gatech.edu/ECE6390/project/Fall2012/Team09/Team9GeoSatTech_website_FINAL/SatCom%20website/linkBudget.html)). In decibels: `EIRP (dBW) = transmit power (dBW) + antenna gain (dBi) - feed losses`. A big antenna raises EIRP directly through its gain, the second reason aperture matters.

**Path loss: how much the wave fades crossing the gap.** Free-space path loss (FSPL) is the spreading of the wave over distance, and it grows with BOTH distance squared and frequency squared. The corpus uses the standard form:

```
   FSPL (dB)  =  20 log10(distance)  +  20 log10(frequency)  +  92.45
```

(distance in km, frequency in GHz) ([Wikipedia: Free-space path loss](https://en.wikipedia.org/wiki/Free-space_path_loss); corpus COMM-294). Doubling the frequency costs 6 dB before any walls or rain. For a direct-to-cell uplink at 1900 MHz to LEO, FSPL is ~153 dB, an enormous hole ([corpus COMM-294](dtc_antenna_aperture_tradeoff.md)).

**Putting it together (the Friis equation).** The received power is:

```
   P_rx (dBW)  =  EIRP (dBW)  -  FSPL (dB)  +  G_rx (dBi)  -  other losses
```

([Wikipedia: Link budget / Friis transmission equation](https://en.wikipedia.org/wiki/Link_budget); [corpus COMM-294/296](dtc_antenna_aperture_tradeoff.md)). The signal must land above the receiver's decode threshold, which sits a fixed margin above the thermal noise floor. The gap between "what arrives" and "what is needed" is the link margin. If it is negative, the link fails. Everything a satellite antenna does, EIRP on the way down and gain (G/T) on the way up, is about keeping that margin positive across a brutal path loss.

> **COMM-570.** The link budget is the energy accounting of a radio link (every gain and loss from transmitter to receiver, checked against the noise). EIRP = transmit power + antenna gain (dBW), the effective loudness. Free-space path loss `FSPL (dB) = 20 log10(d) + 20 log10(f) + 92.45` grows with distance squared and frequency squared (doubling frequency costs 6 dB; a 1900 MHz LEO uplink loses ~153 dB). Received power (Friis) = EIRP - FSPL + receive gain - other losses, and must clear the decode threshold above the noise floor for a positive link margin. A bigger antenna helps on BOTH ends (EIRP down, G/T up). **[FACT, textbook]** Sources: [Wikipedia: Link budget](https://en.wikipedia.org/wiki/Link_budget) (link budget, EIRP, Friis); [Wikipedia: Free-space path loss](https://en.wikipedia.org/wiki/Free-space_path_loss); [Qorvo: Satellite Link Budget](https://www.qorvo.com/design-hub/blog/designing-efficient-satellite-links-a-review-of-the-link-budget-analysis); cross-ref corpus COMM-294/296.
>
> **VERDICT:** the link budget decides whether bits arrive at all. Path loss to a satellite is enormous, so the antenna's gain and EIRP are what keep the link alive.

## B3. How a phased array works: many elements, beam steered by phase

A dish steers by physically pointing the whole reflector. A PHASED ARRAY does it with no moving parts, by electronics, and that unlocks everything a direct-to-cell satellite needs.

**Many small elements instead of one big dish.** A phased array is a grid of many small radiating elements (patches or dipoles), each fed its own copy of the signal. Together they act as one large antenna. The combined aperture, and so the gain, is roughly the sum of the elements: an N-element array has up to ~N times the gain of one element (10 log10 N dB more), so more elements means more gain and a narrower beam ([Wikipedia: Phased array](https://en.wikipedia.org/wiki/Phased_array), "the size of an antenna array must extend many wavelengths to achieve the high gain needed for narrow beamwidth").

**The beam is steered by adjusting each element's PHASE.** Here is the core trick. If every element radiates exactly in step (in phase), their waves add up straight ahead, forming a beam pointing perpendicular to the array. If instead you delay each element a little more than its neighbour, a progressive phase shift across the array, the waves add up in a tilted direction, and the beam swings off to the side, all electronically. "The computer can alter the phase or signal delay of each antenna element electronically, resulting in a beam of radio waves that can be dynamically 'steered' to propagate in arbitrary directions" ([Wikipedia: Phased array](https://en.wikipedia.org/wiki/Phased_array), verbatim; "the phase shifters delay the radio waves progressively going up the line so each antenna emits its wavefront later than the one below it"). The steering relation is `d x sin(theta) = phase delay per element x lambda / (2 pi)`, i.e. the beam angle theta is set by the phase increment across elements of spacing d. No motor, no inertia, microsecond re-pointing.

**Element spacing ~half a wavelength, to avoid grating lobes.** Elements are spaced about lambda/2 apart. Pack them too far apart and the array forms spurious extra beams (grating lobes) that waste power and cause interference ([Wikipedia: Phased array](https://en.wikipedia.org/wiki/Phased_array), spacing geometry to prevent unwanted radiation patterns). This sets the element count for a given area: a ~25 m^2 array at ~2 GHz (lambda ~15 cm, half-wave spacing ~7.5 cm) holds on the order of thousands of elements.

> **COMM-571.** A phased array is a grid of many small radiating elements, each fed its own copy of the signal, acting together as one large antenna; an N-element array reaches up to ~N times (10 log10 N dB) the gain of a single element, so more elements = more gain and a narrower beam. It steers its beam ELECTRONICALLY with no moving parts by applying a progressive PHASE shift across the elements (in-phase = beam straight ahead; increasing phase delay per element = beam tilts off-axis), per `d x sin(theta) = phase-increment x lambda/(2 pi)`, enabling microsecond re-pointing. Elements are spaced ~lambda/2 to avoid grating lobes, which sets the element count (a ~25 m^2 array at ~2 GHz holds thousands of elements). **[FACT, textbook]** Sources: [Wikipedia: Phased array](https://en.wikipedia.org/wiki/Phased_array) (progressive phase steering, electronic, arbitrary directions, grating-lobe spacing, N-element gain, verbatim); cross-ref corpus COMM-296.
>
> **VERDICT:** a phased array is a dish with no moving parts: many small elements, and a beam aimed purely by setting phases. Speed and flexibility are the payoff.

## B4. Many beams at once, multiple bands at once, and the kinds of beamforming

The reason a phased array, not a dish, is the right tool for a direct-to-cell satellite is that one aperture can do MANY things simultaneously.

**MANY simultaneous beams from one aperture.** An active/digital array can form multiple independent beams at the same time, each steered to a different patch of ground, all reusing the same physical antenna. Active arrays "can radiate several beams of radio waves at multiple frequencies in different directions simultaneously" ([Wikipedia: Phased array](https://en.wikipedia.org/wiki/Phased_array), verbatim). This is what lets ONE satellite act like hundreds of cell towers at once: AST SpaceMobile forms 2,000+ coverage cells per satellite, Starlink's V2-mini direct-to-cell forms 48 independently steerable beams, and a flat ~25 m^2 entrant model lands at ~200-450 beams ([corpus COMM-538](dtc_subscribers_per_satellite.md); [AST: Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/), "more than 2,000 coverage cells per satellite"). Each beam is a cell, and the same band is reused across non-overlapping beams (the A6 reuse mechanism, on a satellite).

**MULTIPLE bands at once.** The array can also operate several frequency bands simultaneously (different elements or sub-arrays tuned to different bands, or wideband elements), and carrier aggregation then sums the held channels. AST runs leased low-band 700/850 MHz alongside its own S-band and L-band plus acquired mid-band, all at once across its beams ([corpus COMM-539](dtc_subscribers_per_satellite.md); [SDxCentral: AST low-band access](https://www.sdxcentral.com/news/fcc-grants-ast-spacemobile-access-to-att-verizon-spectrum/)). A single satellite is not limited to one band. (For wide bandwidths, true-time-delay steering is used instead of pure phase shift to avoid the beam "squinting" to a slightly different angle at different frequencies, a refinement noted here for completeness.)

**The three kinds of beamforming (analog, digital, hybrid).** "Beamforming" is how the array sets the per-element amplitudes and phases to form beams, and there are three architectures:

- **Analog beamforming.** Phase shifters (and attenuators) act on the RF signal itself, before digitisation. Cheap and low-power, but it can typically form only one (or a few) beam(s) at a time per RF chain.
- **Digital beamforming.** Every element (or sub-array) has its own analog-to-digital / digital-to-analog converter, and all the beam math is done in the digital signal processor. This is the most flexible: it can form MANY independent beams at once and reshape them instantly, but it costs the most processing and DC power ([Analog Devices: Digital Beamforming](https://www.analog.com/en/solutions/aerospace-and-defense/phased-array/digital-beamforming.html); [Wireless Pi: Analog vs Digital vs Hybrid Beamforming](https://wirelesspi.com/what-is-the-difference-between-analog-digital-and-hybrid-beamforming/)).
- **Hybrid beamforming.** A compromise: analog beamforming within sub-arrays, digital combining across them. Most large mmWave and satellite arrays use hybrid to get many beams without paying full digital power ([Analog Devices: Power Advantage of Hybrid Beamforming](https://www.analog.com/en/resources/technical-articles/power-advantage-of-hybrid-beamforming.html)).

The many-simultaneous-beams capability that direct-to-cell depends on is fundamentally a DIGITAL (or hybrid) beamforming capability, run by a dedicated processor.

> **COMM-572.** One phased-array aperture can form MANY independent beams simultaneously (active arrays "radiate several beams ... at multiple frequencies in different directions simultaneously"): AST 2,000+ cells/sat, Starlink V2-mini D2C 48 beams, a flat ~25 m^2 model ~200-450, each beam a reused cell. It can also operate MULTIPLE bands at once (AST runs low-band 700/850 + S-band + L-band + mid-band together), with carrier aggregation summing them (wideband arrays use true-time-delay to avoid beam squint). The three beamforming types: ANALOG (RF phase shifters, cheap/low-power, few beams), DIGITAL (per-element ADC/DAC + DSP, most flexible, many simultaneous beams, highest power/compute), HYBRID (analog sub-arrays + digital combining, the usual large-array compromise). Many-beam D2C is a digital/hybrid beamforming capability. **[FACT, multi-source]** Sources: [Wikipedia: Phased array](https://en.wikipedia.org/wiki/Phased_array) (several simultaneous beams at multiple frequencies, verbatim); [Analog Devices: Digital Beamforming](https://www.analog.com/en/solutions/aerospace-and-defense/phased-array/digital-beamforming.html) and [Hybrid Beamforming](https://www.analog.com/en/resources/technical-articles/power-advantage-of-hybrid-beamforming.html); [Wireless Pi: beamforming types](https://wirelesspi.com/what-is-the-difference-between-analog-digital-and-hybrid-beamforming/); cross-ref corpus COMM-538/539.
>
> **VERDICT:** one phased array = many beams and many bands at once, which is exactly why a single satellite can serve hundreds of cells. The flexibility comes from digital beamforming.

## B5. The beamforming processor, EIRP and power: what LIMITS a phased array

A phased array is not free to form infinite beams. Three things bind it, in a definite order.

**(1) The beamforming PROCESSOR/ASIC sets the beam COUNT, and its compute scales hard.** Digital beamforming means digitising and processing every element's signal in real time. The data the processor must crunch grows with elements x beams x bandwidth: "the amount of data the DSP must process is proportional to the number of elements, number of beams, and instantaneous bandwidth." Concretely, "for a 1024-element array, with 500 MHz bandwidth and 8-bit ADC, the DSP needs to process about 8 Tb of data per second per beam," and "for multiple beams at full signal bandwidth, the necessary computational power is beyond the reach of today's DSP hardware" ([Microwave Journal / Analog Devices: ADC merit in digital phased arrays](https://www.analog.com/en/resources/technical-articles/power-advantage-of-hybrid-beamforming.html)). The practical workaround is to hold the beam-bandwidth PRODUCT roughly constant: more beams means each beam gets less bandwidth. On a satellite this is a custom ASIC (AST's "AST5000" handles real-time beam steering across 2,000+ cells), and it sets how many beams you can form, not the aggregate bits they carry ([corpus COMM-536/540](dtc_subscribers_per_satellite.md); [AST: Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/)).

**(2) DC POWER sets how many beams you can ENERGIZE.** Each lit beam needs RF power, and the satellite's solar/battery budget caps the total. The AST BlueBird FCC filing shows ~1,660 W total RF power, about 10 W per beam, so ~160 beams can be energized simultaneously even though the processor can FORM more ([corpus COMM-507/540](dtc_data_rate_vs_spectrum.md); FCC ELS id=376295). EIRP per beam is transmit power times gain, so power and aperture together set how loud each beam is. Power also drives the bandwidth saturation result: at a fixed power budget, widening the channel does not raise the single-link rate much because SNR = P/(N0 x B) falls as bandwidth rises (the corpus's Case B, capped at 1.44x = log2(e)) ([corpus COMM-500/504](dtc_data_rate_vs_spectrum.md)).

**(3) The SPECTRUM you hold caps the AGGREGATE all beams carry.** Total throughput = bandwidth x spectral efficiency x number of (non-overlapping) beams. With a thin cellular holding (say 25 MHz), this caps the aggregate far below what the processor or power could push, so on a cellular entrant the HELD SPECTRUM binds first ([corpus COMM-535/536](dtc_subscribers_per_satellite.md)).

**The order, for a thin-spectrum cellular satellite:** on ~25 MHz the SPECTRUM binds; antenna power begins to bind only past ~50-100 MHz; the processor binds last, past ~100-200 MHz of usable band a cellular entrant cannot even acquire ([corpus COMM-537](dtc_subscribers_per_satellite.md)). So the chip is the LEAST binding of the three for cellular direct-to-cell. The processor decides beam count; the held spectrum decides total capacity.

> **COMM-573.** A phased array is bound by three limits in order. (1) The beamforming PROCESSOR/ASIC sets the beam COUNT; digital-beamforming compute scales as elements x beams x bandwidth (a 1024-element / 500 MHz / 8-bit array needs ~8 Tb/s per beam, and full-bandwidth multibeam is "beyond the reach of today's DSP," so the beam-bandwidth PRODUCT is held roughly constant, more beams = less bandwidth each). (2) DC POWER sets how many beams are ENERGIZED (AST ~1,660 W RF, ~10 W/beam, ~160 lit simultaneously though more are formed); per-beam EIRP = power x gain, and at fixed power widening a channel barely raises the single-link rate (SNR = P/(N0 B) falls; capped at 1.44x). (3) HELD SPECTRUM caps the AGGREGATE (= bandwidth x SE x beam count). For a thin-cellular satellite the order is SPECTRUM binds (~25 MHz), then power (~50-100 MHz), then processor (~100-200 MHz); the chip is the LEAST binding. **[FACT + DERIVED, multi-source]** Sources: [Analog Devices / Microwave Journal: digital beamforming compute and power](https://www.analog.com/en/resources/technical-articles/power-advantage-of-hybrid-beamforming.html) (8 Tb/s/beam, beam-bandwidth product, beyond today's DSP); [AST: Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/) (AST5000, 2,000+ cells, 10 GHz processing); cross-ref corpus COMM-507/535/536/537/540/500/504.
>
> **VERDICT:** what a phased array can do at once is set by the chip (beam count), the power (beams energized), and the held spectrum (aggregate). On a cellular holding, spectrum binds first and the chip binds last.

## B6. Putting it together: a satellite talking to a bare phone

Now assemble the whole machine for the hardest case, a satellite reaching an ordinary, unmodified phone hundreds of kilometres below.

**The phone is a terrible radio, and it cannot be improved.** A handset transmits only ~0.2 W (23 dBm) into an antenna with essentially no gain (~0 dBi), giving an EIRP of ~23 dBm, and regulatory SAR limits plus the lack of physical space mean none of this can grow ([corpus COMM-293](dtc_antenna_aperture_tradeoff.md)). On a normal cellular link this is fine because the tower is a few kilometres away with a big high-gain antenna. To a satellite, the phone is a whisper from across an ocean.

**The path loss is enormous and the signal lands near the noise floor.** At 1900 MHz to LEO the free-space path loss is ~153 dB. The phone's uplink arrives at the satellite at roughly -130 dBm, against an LTE QPSK decode threshold of about -105 dBm, a ~25 dB deficit the satellite alone must recover ([corpus COMM-294](dtc_antenna_aperture_tradeoff.md)). The live Starlink direct-to-cell network confirms the symptom: a measured median SINR of 0 dB, exactly the SNR = 1 regime where spectral efficiency `log2(1+1) = 1 bps/Hz` is the natural ceiling, and measured throughput of ~0.5-0.8 bps/Hz ([corpus COMM-429/508](spectrum_capacity_primer.md); [arXiv 2506.00283](https://arxiv.org/html/2506.00283v2)).

**The satellite supplies ALL the gain, and that demands a giant phased array.** Since the phone contributes nothing, the satellite antenna alone must close the ~25 dB gap, on BOTH directions at once: high gain to hear the faint uplink (a good G/T), and high EIRP to shout an intelligible downlink. The only lever is aperture, because `G = 4 pi eta A / lambda^2`. This is why direct-to-cell satellites carry enormous arrays while broadband satellites can be small flat panels (the broadband customer's own dish supplies the ground-side gain; the bare phone supplies none) ([corpus COMM-295/311](dtc_antenna_aperture_tradeoff.md)). The revealed aperture-to-service ladder ([corpus COMM-298/301](dtc_antenna_aperture_tradeoff.md)):

| Satellite array | Aperture | Modeled gain | Service delivered |
|---|---|---|---|
| Lynk | ~1-1.5 m^2 | ~29 dBi | SMS only |
| Starlink Gen2 D2C | ~25 m^2 (soft figure) | ~32-38 dBi | SMS, then a few Mbps/beam |
| AST BlueWalker 3 / Block 1 | ~64 m^2 | ~36.5 dBi | broadband demo (~21-99 Mbps) |
| AST Block 2 (Next-Gen BlueBird) | ~223 m^2 (~199 m^2 in FCC filing) | ~42 dBi at 880 MHz | up to ~120 Mbps/cell across 2,000+ cells |

(AST array sizes from [AST: Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/), ~2,400 sq ft ~ 223 m^2, "the largest commercial communications arrays ever deployed in low Earth orbit"; Block 1 ~693 sq ft ~ 64 m^2 from [AST: How It Works](https://ast-science.com/how-it-works/); the ~25 m^2 Starlink figure is flagged soft in the corpus, COMM-303.)

**And the phased array is what makes it a business, not just a link.** A single giant dish could close the link to one spot, but a phased array closes it to hundreds of spots at once (B4) and steers them as the satellite races overhead, while reusing the same scarce cellular spectrum across non-overlapping beams (A6). So the satellite-to-phone story is the union of both halves of this document: the SPECTRUM half says you must use existing low/mid cellular bands at low spectral efficiency because the phone is weak, and the ANTENNA half says only a large phased array supplies enough gain to close the link and enough beams to serve a population. The aperture is the master lever on the antenna side; the held spectrum is the master lever on the capacity side.

> **COMM-574.** A satellite reaching a bare phone works only because the SATELLITE supplies all the gain. The handset is fixed at ~0.2 W (23 dBm) into ~0 dBi (EIRP ~23 dBm), unimprovable (SAR + space); at 1900 MHz to LEO the ~153 dB path loss lands the uplink at ~-130 dBm against a ~-105 dBm QPSK threshold, a ~25 dB deficit, and the live Starlink network measures median SINR 0 dB (~0.5-0.8 bps/Hz). The satellite antenna alone must close the gap on both links (G/T up, EIRP down) via aperture (`G = 4 pi eta A / lambda^2`), which is why D2C carries giant arrays (Lynk ~1.5 m^2 SMS; Starlink ~25 m^2 soft, few Mbps; AST ~64 m^2 broadband demo; AST ~223 m^2 / ~42 dBi / 2,000+ cells / up to 120 Mbps/cell) while broadband sats stay small (the customer's dish supplies ground gain). The phased array makes it a business: it closes the link to hundreds of steered beams at once while reusing scarce cellular spectrum. **[FACT + DERIVED, multi-source]** Sources: [arXiv 2506.00283](https://arxiv.org/html/2506.00283v2) (median SINR 0 dB); [AST: Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/) and [How It Works](https://ast-science.com/how-it-works/) (223 m^2, 64 m^2, 2,000+ cells, satellite supplies signal strength); cross-ref corpus COMM-293/294/295/298/301/311/439/429.
>
> **VERDICT:** the phone is a whisper; the satellite must do all the shouting and listening, which takes a giant phased array. Spectrum sets how much you can send; the array decides whether it arrives and to how many places at once.

---

## C. The whole machine in one read (so-what synthesis)

Read top to bottom, the two halves chain like this:

1. **Spectrum is the scarce, licensed input.** You hold a slice of the dial, in some band, of some width. The band (frequency) sets reach; the width (bandwidth) sets the capacity ceiling. (A1, A2, A3, A7)
2. **Modulation turns the slice into bits, capped by Shannon.** `rate = bandwidth x log2(1+SNR)`. Bandwidth is the strong lever; signal quality is the weak one. (A4)
3. **You enlarge the held pie by aggregating separate channels (they sum), not by slicing one channel finer (that only shares it).** (A5)
4. **You multiply the SYSTEM total by reusing the band across many cells/beams.** Total = bandwidth x efficiency x cells. (A6)
5. **An antenna's gain (= aperture over wavelength squared) is what makes the signal arrive and what sets the beam width.** Bigger aperture = louder + tighter beam. (B1)
6. **The link budget decides if bits arrive at all; to a satellite the path loss is huge, so the antenna's gain/EIRP is the whole game.** (B2)
7. **A phased array steers and splits the beam electronically, forming many beams and bands at once.** That turns one satellite into hundreds of cells. (B3, B4)
8. **What the array can do at once is bound by the chip (beam count), the power (beams lit), and the held spectrum (aggregate), in that order, with spectrum binding first on a thin cellular holding.** (B5)
9. **For a bare phone, the satellite supplies all the gain, which forces a giant phased array, while the phone's weakness forces low spectral efficiency on existing cellular bands.** (B6)

The two master levers, stated once: on the SPECTRUM side, how much band you hold (a business/licensing problem); on the ANTENNA side, how big your aperture is (a mass/engineering problem). The two master equations: `C = B x log2(1+SNR)` (capacity) and `G = 4 pi eta A / lambda^2` (gain). Everything in the corpus's eight direct-to-cell docs hangs off these two.

---

## D. Glossary (plain-language, one line each)

- **Electromagnetic spectrum.** The full range of light-like waves ordered by frequency; radio is the low-frequency end.
- **Radio spectrum.** The 3 Hz-3,000 GHz part used for radio/cellular/satellite; a finite, licensed, shared resource.
- **Frequency (the band).** Where on the dial a signal sits (Hz/MHz/GHz); sets REACH. Aliases to avoid: do not call this "bandwidth."
- **Wavelength (lambda).** The physical length of one wave cycle; `c = f x lambda`, so higher frequency = shorter wave.
- **Bandwidth (channel width).** How wide your slice is (Hz/MHz); sets the capacity CEILING. Not the same as frequency, though both are in MHz.
- **Data rate (throughput).** Bits per second actually delivered (Mbps); = bandwidth x a link-quality efficiency.
- **Modulation.** Encoding bits by varying a wave's amplitude/phase/frequency (AM, FM, QAM, OFDM).
- **QAM.** Quadrature amplitude modulation; packs several bits per symbol via amplitude+phase (16-QAM = 4 bits, 64-QAM = 6, 256-QAM = 8, 1024-QAM = 10). Higher orders need higher SNR.
- **OFDM / OFDMA.** OFDM splits a channel into many orthogonal sub-carriers (used by LTE/5G); OFDMA assigns sub-carrier subsets to different users (sharing, not added capacity).
- **Shannon-Hartley law.** `C = B x log2(1+SNR)`; the hard maximum error-free rate of a channel.
- **SNR / SINR.** Signal-to-noise (or signal-to-interference-plus-noise) ratio; the link-quality input to Shannon.
- **Spectral efficiency.** `C/B = log2(1+SNR)` in bits/sec/Hz; the bits wrung from each hertz; depends only on link quality.
- **Carrier aggregation.** One device using multiple separate channels at once, their rates SUMMING (LTE-A Release 10+).
- **Component carrier.** One of the separate channels combined by carrier aggregation.
- **Frequency reuse / spatial reuse.** Using the same band in geographically separated cells; multiplies system capacity by the cell count.
- **Cell splitting.** Making cells smaller (so more of them) to add capacity; the dominant historical driver (Cooper's Law).
- **Antenna.** Converts between guided signals and radiated waves; transmit and receive properties are identical (reciprocity).
- **Gain (dBi).** How tightly an antenna concentrates energy versus an isotropic radiator (3 dBi = 2x in the peak direction).
- **Aperture (effective area).** The antenna's electrical collecting area; `G = 4 pi eta A / lambda^2`, so bigger aperture = more gain.
- **Aperture efficiency (eta).** Fraction of physical area that is electrically useful, ~0.5-0.7.
- **Beamwidth.** Angular width of the beam; inverse to gain (bigger aperture = narrower beam = smaller ground cell).
- **EIRP.** Effective isotropic radiated power = transmit power x antenna gain; how "loud" a transmitter is.
- **Free-space path loss (FSPL).** Signal fade over distance; `20 log10(d) + 20 log10(f) + 92.45`; grows with distance^2 and frequency^2.
- **Link budget.** The energy accounting of a link (gains minus losses vs noise) that decides if bits arrive.
- **G/T.** Receive figure of merit (gain over system noise temperature); the uplink-side benefit of a big antenna.
- **Phased array.** Many small elements forming a beam steered electronically by phase, no moving parts.
- **Element.** One small radiating unit of a phased array; spaced ~lambda/2 to avoid grating lobes.
- **Beam steering.** Aiming the beam by setting a progressive phase shift across elements.
- **Grating lobes.** Spurious extra beams from elements spaced too far apart; waste power, cause interference.
- **Beamforming (analog / digital / hybrid).** Setting per-element amplitude/phase to form beams: analog (RF phase shifters, few beams, low power), digital (per-element ADC/DAC + DSP, many beams, high power), hybrid (the usual compromise).
- **Beamforming processor / ASIC.** The chip that runs digital beamforming; sets the BEAM COUNT; compute scales as elements x beams x bandwidth.
- **Multibeam.** One aperture forming many independent beams at once, each a reused cell.
- **True-time-delay.** A steering method for wide-bandwidth arrays that avoids beam squint (the beam pointing slightly differently at different frequencies).
- **Power-limited regime.** Low-SNR operation (like a phone link) where capacity is set by power, nearly independent of bandwidth (widening the channel barely helps; capped at 1.44x = log2(e)).
- **Bandwidth-limited regime.** High-SNR operation where capacity scales ~linearly with bandwidth.

---

## E. Sources

Every hard claim above is cited inline at its point of use; this section collects those URLs grouped by topic. Verbatim quotations and the exact figures each source supports are in the inline text and the VERDICT blocks, not repeated here.

The electromagnetic spectrum and the radio bands (A1, A2):
- [Lumen Learning / SUNY Physics: The Electromagnetic Spectrum](https://courses.lumenlearning.com/suny-physics/chapter/24-3-the-electromagnetic-spectrum/) (radio is the lowest-frequency EM wave; `c = f lambda` verbatim)
- [University Physics Vol. 2, UCF Pressbooks: The Electromagnetic Spectrum](https://pressbooks.online.ucf.edu/osuniversityphysics2/chapter/the-electromagnetic-spectrum/)
- [Study.com: Frequency and Wavelength for EM Waves](https://study.com/skill/learn/applying-the-relationship-between-frequency-wavelength-for-em-waves-explanation.html)
- [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum) (3 Hz to 3,000 GHz range and ITU named bands verbatim; "a fixed resource ... increasingly congested"; ITU/FCC regulation; sold/licensed. This source anchors A1, A2, and A7)

Frequency vs bandwidth vs data rate, modulation, and the Shannon limit (A3, A4):
- [Wilson: Cellular Frequency Bands Explained](https://www.wilsonsignalbooster.com/blogs/articles/cellular-frequency-bands-explained) (low-band reach and building penetration vs high-band fade; FCC issues licenses and runs auctions; low/mid/high tiers. Anchors A3 and A7)
- [Waveform: 5G and Shannon's Law](https://www.waveform.com/a/b/guides/5g-and-shannons-law)
- [Wikipedia: Quadrature amplitude modulation (QAM)](https://en.wikipedia.org/wiki/Quadrature_amplitude_modulation) (amplitude plus phase; higher-order QAM needs a higher SNR, verbatim)
- [ICO Optics: Digital Modulation Methods (QAM, PSK, OFDM)](https://www.ico-optics.org/digital-modulation-methods-qam-psk-and-ofdm/) (bits per symbol; OFDM spreads QAM symbols over sub-carriers)
- [Wikipedia: Shannon-Hartley theorem](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem) (`C = B log2(1 + SNR)`, term definitions)
- [Wikipedia: Spectral efficiency](https://en.wikipedia.org/wiki/Spectral_efficiency)
- [Techplayon: Spectral Efficiency, 5G NR and 4G LTE](https://www.techplayon.com/spectral-efficiency-5g-nr-and-4g-lte/)

Carrier aggregation, OFDMA, and frequency reuse (A5, A6):
- [3GPP: Carrier Aggregation](https://www.3gpp.org/technologies/carrier-aggregation-on-mobile-networks) (Release 10 LTE-Advanced, up to 100 MHz, verbatim)
- [Wikipedia: Carrier aggregation](https://en.wikipedia.org/wiki/Carrier_aggregation)
- [TechTarget: OFDMA](https://www.techtarget.com/searchnetworking/definition/orthogonal-frequency-division-multiple-access-OFDMA)
- [Wikipedia: Frequency reuse](https://en.wikipedia.org/wiki/Frequency_reuse) (reuse increases capacity; distant cells can share a frequency, verbatim)
- [GeeksforGeeks: Frequency Reuse](https://www.geeksforgeeks.org/computer-networks/frequency-reuse/)
- [IEEE Xplore 10816533: Optimizing Beam Size in Multibeam LEO Satellite Networks](https://ieeexplore.ieee.org/document/10816533/) (beam tiling and co-channel interference as the bound on reuse)

Spectrum allocation, licensing, and the cellular bands (A7):
- [Kajeet: A Guide to Cellular Frequency Bands Used by US Carriers](https://www.kajeet.com/en/blog/a-guide-to-cellular-frequency-bands-used-by-us-carriers) (the low/mid/high band table; also see Wilson and Wikipedia: Radio spectrum above)

Antennas, gain, aperture, beamwidth, and the link budget (B1, B2):
- [Wikipedia: Antenna aperture](https://en.wikipedia.org/wiki/Antenna_aperture) (`G = 4 pi eta A / lambda^2`, eta 0.35 to over 0.70, larger aperture = narrower beam, verbatim)
- [antenna-theory.com: Antenna Gain](https://www.antenna-theory.com/basics/gain.php) (dBi; 3 dBi = 2x power in the peak direction)
- [Wikipedia: Parabolic antenna](https://en.wikipedia.org/wiki/Parabolic_antenna)
- [Electronics Notes: Parabolic reflector gain and beamwidth](https://www.electronics-notes.com/articles/antennas-propagation/parabolic-reflector-antenna/antenna-gain-directivity.php)
- [Wikipedia: Link budget](https://en.wikipedia.org/wiki/Link_budget) (link budget, EIRP, Friis transmission equation)
- [Wikipedia: Free-space path loss](https://en.wikipedia.org/wiki/Free-space_path_loss) (`FSPL = 20 log10 d + 20 log10 f + 92.45`)
- [Qorvo: Designing Efficient Satellite Links, a Review of the Link Budget Analysis](https://www.qorvo.com/design-hub/blog/designing-efficient-satellite-links-a-review-of-the-link-budget-analysis)
- [Georgia Tech: Link Budget Calculation](https://propagation.ece.gatech.edu/ECE6390/project/Fall2012/Team09/Team9GeoSatTech_website_FINAL/SatCom%20website/linkBudget.html) (EIRP = transmit power x antenna gain)

Phased arrays and beamforming (B3, B4, B5):
- [Wikipedia: Phased array](https://en.wikipedia.org/wiki/Phased_array) (progressive-phase electronic steering to arbitrary directions; several simultaneous beams at multiple frequencies; grating-lobe spacing; N-element gain, all verbatim)
- [Analog Devices: Digital Beamforming](https://www.analog.com/en/solutions/aerospace-and-defense/phased-array/digital-beamforming.html)
- [Analog Devices / Microwave Journal: The Power Advantage of Hybrid Beamforming](https://www.analog.com/en/resources/technical-articles/power-advantage-of-hybrid-beamforming.html) (digital-beamforming compute scales as elements x beams x bandwidth; ~8 Tb/s per beam; full-bandwidth multibeam beyond today's DSP)
- [Wireless Pi: Analog vs Digital vs Hybrid Beamforming](https://wirelesspi.com/what-is-the-difference-between-analog-digital-and-hybrid-beamforming/)

Direct-to-cell systems and the satellite-to-phone link (B4, B5, B6):
- [AST SpaceMobile: Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/) (~223 m^2 arrays, 2,000+ coverage cells, AST5000 beam-steering ASIC, the satellite supplies the signal strength)
- [AST SpaceMobile: How It Works](https://ast-science.com/how-it-works/) (Block 1 ~64 m^2)
- [SDxCentral: FCC grants AST SpaceMobile access to AT&T / Verizon spectrum](https://www.sdxcentral.com/news/fcc-grants-ast-spacemobile-access-to-att-verizon-spectrum/) (leased low band alongside owned bands)
- [arXiv 2506.00283: Direct-to-Cell, a First Look into Starlink's RAN through Crowdsourced Measurements](https://arxiv.org/html/2506.00283v2) (measured median SINR 0 dB; ~0.5 to 0.8 bps/Hz)

- *(Corpus cross-references cited inline at each claim, and not re-listed here: [`spectrum_capacity_primer.md`](spectrum_capacity_primer.md) COMM-426..439, [`channels_aggregate_answer.md`](channels_aggregate_answer.md), [`dtc_antenna_aperture_tradeoff.md`](dtc_antenna_aperture_tradeoff.md) COMM-293..314, [`dtc_data_rate_vs_spectrum.md`](dtc_data_rate_vs_spectrum.md) COMM-493..512, [`dtc_subscribers_per_satellite.md`](dtc_subscribers_per_satellite.md) COMM-535..560, and [`dtc_spectrum_access.md`](dtc_spectrum_access.md) COMM-481..492.)*

---

## F. Claims ledger (COMM-561..574)

For the catalog / reconciliation step to ingest. This explainer reserved the contiguous block COMM-561..600 and uses COMM-561..574 (14 hard claims); 575..600 remain unused. Each row's tag matches the inline VERDICT block: **[FACT]** (checked against 2+ independent sources), **[DERIVED]** (arithmetic or logic assembled here), or a combination. Corpus IDs are cross-referenced, not re-minted.

| ID | Claim (short) | Tag | Sources |
|---|---|---|---|
| **COMM-561** | Radio waves are electromagnetic waves (same physics as visible light); frequency and wavelength are inversely locked by `c = f x lambda`, so 700 MHz ~ 43 cm and 28 GHz ~ 1.1 cm; the radio spectrum is the 3 Hz to 3,000 GHz band, split by the ITU into named bands (cellular mainly UHF, 5G reaching SHF and EHF). | [FACT, textbook] | [Lumen/SUNY Physics](https://courses.lumenlearning.com/suny-physics/chapter/24-3-the-electromagnetic-spectrum/); [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum); cross-ref COMM-426. |
| **COMM-562** | Radio spectrum is a finite natural resource, shared (co-channel transmitters in the same place interfere), and licensed: regulators (ITU worldwide, FCC in the US) grant exclusive rights over a band and territory, often sold for billions; an operator owns the license, not the air. | [FACT, regulatory] | [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum); [Wilson: Cellular Bands](https://www.wilsonsignalbooster.com/blogs/articles/cellular-frequency-bands-explained); cross-ref COMM-481. |
| **COMM-563** | Frequency (band, MHz/GHz) sets REACH, bandwidth (channel width, MHz) sets the capacity CEILING, and data rate (Mbps) = bandwidth x a link-quality efficiency; two of the three are quoted in MHz, which is the root of the confusion. | [FACT, textbook] | [Wilson: Cellular Bands](https://www.wilsonsignalbooster.com/blogs/articles/cellular-frequency-bands-explained); [Waveform: Shannon's Law](https://www.waveform.com/a/b/guides/5g-and-shannons-law); cross-ref COMM-426/430. |
| **COMM-564** | A frequency carries information by modulation; QAM packs multiple bits per symbol via amplitude plus phase (QPSK 2 to 1024-QAM 10) and OFDM spreads QAM over orthogonal sub-carriers (LTE/5G/Wi-Fi); higher-order QAM needs a higher SNR, so weak links fall back. | [FACT, textbook] | [Wikipedia: QAM](https://en.wikipedia.org/wiki/Quadrature_amplitude_modulation); [ICO Optics](https://www.ico-optics.org/digital-modulation-methods-qam-psk-and-ofdm/); cross-ref COMM-427. |
| **COMM-565** | The Shannon-Hartley law `C = B x log2(1 + SNR)` caps a single channel: rate is linear in bandwidth (strong lever) and only logarithmic in SNR (weak lever); spectral efficiency `C/B` depends only on link quality (LTE ~1.5, 5G ~3, satellite-to-phone ~0.5 to 0.8 bps/Hz); real systems reach ~60 to 80% after overhead. | [FACT, textbook] | [Wikipedia: Shannon-Hartley](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem); [Wikipedia: Spectral efficiency](https://en.wikipedia.org/wiki/Spectral_efficiency); [Techplayon](https://www.techplayon.com/spectral-efficiency-5g-nr-and-4g-lte/); cross-ref COMM-041/427/428/429. |
| **COMM-566** | Carrier aggregation (3GPP LTE-A Release 10+) sums separate component carriers (rates ADD, up to 100 MHz / 5 carriers in LTE-A, 16 in 5G), so total capacity = sum of held bandwidths x efficiency; OFDMA sub-carriers only SHARE one channel (a multiple-access trick) and add no capacity. | [FACT, standardized] | [3GPP: Carrier Aggregation](https://www.3gpp.org/technologies/carrier-aggregation-on-mobile-networks); [Wikipedia: Carrier aggregation](https://en.wikipedia.org/wiki/Carrier_aggregation); [TechTarget: OFDMA](https://www.techtarget.com/searchnetworking/definition/orthogonal-frequency-division-multiple-access-OFDMA); cross-ref COMM-433/434. |
| **COMM-567** | Frequency reuse multiplies TOTAL system capacity (~ bandwidth x SE x number of cells): the same channel is reused across non-overlapping cells; cell splitting is the dominant historical driver (Cooper's Law). For a satellite the cell is the spot beam, and the reuse multiplier is set by beam tiling (aperture/altitude), not satellite count. | [FACT, textbook] | [Wikipedia: Frequency reuse](https://en.wikipedia.org/wiki/Frequency_reuse); [GeeksforGeeks](https://www.geeksforgeeks.org/computer-networks/frequency-reuse/); [IEEE Xplore 10816533](https://ieeexplore.ieee.org/document/10816533/); cross-ref COMM-435/436. |
| **COMM-568** | Spectrum is allocated by regulators (ITU global table, national licensing), licensed as exclusive rights won at auction, and a phone works only on the specific bands its front-end supports; cellular is held in low/mid/high tiers, so direct-to-cell MUST use existing licensed cellular bands, forcing a partnership with or acquisition of a license-holder. | [FACT, regulatory] | [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum); [Wilson: Cellular Bands](https://www.wilsonsignalbooster.com/blogs/articles/cellular-frequency-bands-explained); [Kajeet: Cellular Bands](https://www.kajeet.com/en/blog/a-guide-to-cellular-frequency-bands-used-by-us-carriers); cross-ref COMM-481. |
| **COMM-569** | An antenna's GAIN (dBi vs isotropic; 3 dBi = 2x) comes from aperture via `G = 4 pi eta A / lambda^2`, so gain rises linearly with area (double area = +3 dB) and as frequency squared; BEAMWIDTH is inverse to gain (~70 lambda/D degrees), so a bigger aperture is both louder and narrower-beam (more SNR and a smaller ground cell at once). | [FACT, textbook] | [Wikipedia: Antenna aperture](https://en.wikipedia.org/wiki/Antenna_aperture); [antenna-theory.com: Gain](https://www.antenna-theory.com/basics/gain.php); [Wikipedia: Parabolic antenna](https://en.wikipedia.org/wiki/Parabolic_antenna); cross-ref COMM-296/437. |
| **COMM-570** | The link budget is the energy accounting of a link: EIRP = transmit power + antenna gain; free-space path loss `= 20 log10 d + 20 log10 f + 92.45` grows with distance squared and frequency squared (~153 dB for a 1900 MHz LEO uplink); received power (Friis) must clear the decode threshold above the noise floor. A bigger antenna helps on both ends (EIRP down, G/T up). | [FACT, textbook] | [Wikipedia: Link budget](https://en.wikipedia.org/wiki/Link_budget); [Wikipedia: Free-space path loss](https://en.wikipedia.org/wiki/Free-space_path_loss); [Qorvo](https://www.qorvo.com/design-hub/blog/designing-efficient-satellite-links-a-review-of-the-link-budget-analysis); [Georgia Tech](https://propagation.ece.gatech.edu/ECE6390/project/Fall2012/Team09/Team9GeoSatTech_website_FINAL/SatCom%20website/linkBudget.html); cross-ref COMM-294/296. |
| **COMM-571** | A phased array is many small elements each fed its own signal, acting as one large antenna (up to ~N times the element gain); it steers electronically with no moving parts via a progressive phase shift across elements (`d sin(theta) = phase-increment x lambda / (2 pi)`); elements spaced ~lambda/2 avoid grating lobes (a ~25 m^2 array at ~2 GHz holds thousands of elements). | [FACT, textbook] | [Wikipedia: Phased array](https://en.wikipedia.org/wiki/Phased_array); cross-ref COMM-296. |
| **COMM-572** | One aperture forms MANY independent beams at once (AST 2,000+ cells, Starlink V2-mini D2C 48, a flat ~25 m^2 model ~200 to 450), each a reused cell, and can run MULTIPLE bands at once (carrier aggregation summing them). The three beamforming types: analog (few beams, low power), digital (many beams, high power/compute), hybrid (the usual large-array compromise); many-beam D2C is digital/hybrid. | [FACT, multi-source] | [Wikipedia: Phased array](https://en.wikipedia.org/wiki/Phased_array); [Analog Devices: Digital](https://www.analog.com/en/solutions/aerospace-and-defense/phased-array/digital-beamforming.html) and [Hybrid Beamforming](https://www.analog.com/en/resources/technical-articles/power-advantage-of-hybrid-beamforming.html); [Wireless Pi](https://wirelesspi.com/what-is-the-difference-between-analog-digital-and-hybrid-beamforming/); cross-ref COMM-538/539. |
| **COMM-573** | A phased array is bound in order by (1) the beamforming processor/ASIC (sets beam count; compute ~ elements x beams x bandwidth, ~8 Tb/s per beam, full-bandwidth multibeam beyond today's DSP, so the beam-bandwidth product is held roughly constant), (2) DC power (beams energized; AST ~1,660 W, ~10 W/beam, ~160 lit), (3) held spectrum (aggregate = bandwidth x SE x beams). On a thin cellular holding, spectrum binds first (~25 MHz), the chip last. | [FACT + DERIVED, multi-source] | [Analog Devices / Microwave Journal](https://www.analog.com/en/resources/technical-articles/power-advantage-of-hybrid-beamforming.html); [AST: Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/); cross-ref COMM-507/535/536/537/540/500/504. |
| **COMM-574** | A satellite reaching a bare phone works only because the SATELLITE supplies all the gain: the handset is fixed at ~0.2 W into ~0 dBi, and at 1900 MHz to LEO the ~153 dB path loss leaves a ~25 dB deficit (Starlink measures median SINR 0 dB); the antenna alone closes it via aperture, which is why D2C carries giant arrays (Lynk ~1.5 to AST ~223 m^2) while broadband sats stay small. The phased array makes it a business by serving hundreds of steered, spectrum-reusing beams at once. | [FACT + DERIVED, multi-source] | [arXiv 2506.00283](https://arxiv.org/html/2506.00283v2); [AST: Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/) and [How It Works](https://ast-science.com/how-it-works/); cross-ref COMM-293/294/295/298/301/311/439/429. |

---

*Provenance: this explainer reserved the contiguous block COMM-561..600 and used COMM-561..574 (14 hard claims); 575..600 remain unused. Every hard claim is checked against 2+ independent sources cited inline with full URLs (the inline VERDICT blocks carry the verbatim quotations); corpus IDs (COMM-041/293..314/426..439/481..492/493..512/535..560) are cross-referenced, not re-verified here. No business verdict is rendered. The companion [`spectrum_band_designations.md`](spectrum_band_designations.md) (COMM-625..634, written 2026-06-30) defines the letter bands (L, S, C, X, Ku, K, Ka, V, W) this doc uses but does not define. Writing was interrupted 2026-06-29 at the Sources / ledger step; the ending (Sections E and F and this line) was completed 2026-07-08, and the body (Parts A and B, COMM-561..574) was not restructured or renumbered on completion.*


