# The Radio-Frequency Band Designations: L, S, C, X, Ku, K, Ka, V, W (and the Three Vocabularies People Confuse)

*A reference document for the Rocket Lab direct-to-cell (cellular) satellite study. Comms wave 9 (reference/explainer, no business verdict). This is the COMPANION to [`spectrum_and_phased_array_fundamentals.md`](spectrum_and_phased_array_fundamentals.md) (COMM-561..573): that explainer uses "L-band," "S-band," "Ku," and "Ka" repeatedly but never defines them. This doc supplies exactly those definitions, the letter-band table, the naming origin, and the naming confusions, so a smart non-engineer can place ANY band on the dial, state its frequency and wavelength, name what uses it, and explain why the naming is confusing. Every hard fact is cited inline to 2+ independent sources where possible. New claim IDs COMM-625..634.*

**Grounds on / does not duplicate (cite, do not repeat):**
- [`spectrum_and_phased_array_fundamentals.md`](spectrum_and_phased_array_fundamentals.md) (COMM-561..573): owns what spectrum IS (`c = f x lambda`, the 3 Hz-3,000 GHz radio range), the ITU numeric band table (VHF/UHF/SHF/EHF), the frequency-vs-bandwidth-vs-data-rate distinction, and the antenna/phased-array machine. This doc does NOT restate the ITU table or re-derive the wave physics; it cross-references them and adds the LETTER-band layer the fundamentals doc omitted.
- [`dtc_spectrum_access.md`](dtc_spectrum_access.md) (COMM-482/484 and the SCS block): owns the unmodified-phone radio-set gate (COMM-482: a bare handset has front-ends for ~600 MHz to ~2.1 GHz cellular bands and NO L-band MSS or Ku/Ka radio) and the SCS cellular band menu (COMM-484: 600/700/800 MHz, PCS ~1.9 GHz, AWS ~2 GHz). This doc USES that gate to draw the L-band-MSS-vs-cellular distinction in Section 4c; it does not re-derive it.
- [`iridium_acquisition.md`](../rocket_lab/iridium_acquisition.md) (COMM-611..613): owns the Iridium L-band (1616-1626.5 MHz) and Ka cross-link (~23 GHz) facts and the load-bearing "Iridium L-band is not cellular low-band" point. This doc maps Iridium to its letter bands in Section 5 and reuses that distinction; it does not re-verify the Iridium numbers.
- [`../competitors/starlink_v3_v4_spectrum_incorporation.md`](../competitors/starlink_v3_v4_spectrum_incorporation.md) (COMM-178..190): owns the Starlink Ku user / Ka feeder / E-band backhaul / V/W inventory. This doc maps Starlink to its letter bands in Section 5; it does not re-derive the MHz totals.
- [`bands_and_enabling_hardware.md`](bands_and_enabling_hardware.md) (COMM-001..016 of that doc): owns the band LADDER ABOVE Ka (V/E/W/sub-THz/optical) and the enabling silicon. This doc defines the letter bands themselves up through W and cites that doc for the upper-band hardware and the E-band placement; it does not repeat the chip mapping.

> **Reading guide.** Every hard fact is tagged **[FACT]** (2+ independent sources), **[FACT-SS]** (single-source), **[DERIVED]** (arithmetic here, e.g. wavelength = c/f), **[ESTIMATE]**, or **[UNKNOWN]**. No go/no-go verdict is rendered. China is excluded. The full claims ledger is at the end.

---

## 0. Answer first (the whole dial on one screen)

**There are three different vocabularies for naming "where you are on the radio dial," and the same dial position can be named three ways. That triple-naming is the root of every band confusion.**

1. **IEEE letter bands (L / S / C / X / Ku / K / Ka / V / W).** The satellite-and-radar convention, and the PRIMARY language of this study. Each letter is a fixed slab of frequency: **L = 1-2 GHz, S = 2-4, C = 4-8, X = 8-12, Ku = 12-18, K = 18-27, Ka = 27-40, V = 40-75, W = 75-110 GHz** ([Wikipedia: Radio spectrum, IEEE table](https://en.wikipedia.org/wiki/Radio_spectrum); [Microwaves101: Frequency Letter Bands, citing IEEE Std 521-2002](https://www.microwaves101.com/encyclopedias/frequency-letter-bands)).

2. **ITU numeric bands (VHF / UHF / SHF / EHF).** By decade of frequency (UHF = 300-3,000 MHz, SHF = 3-30 GHz, EHF = 30-300 GHz). Already defined in [`spectrum_and_phased_array_fundamentals.md`](spectrum_and_phased_array_fundamentals.md) (COMM-561); not restated here.

3. **Cellular naming (low / mid / high band, plus named bands PCS, AWS, "C-band," and 3GPP n-numbers).** The mobile-industry language. "Low band" ~600-900 MHz, "mid band" ~1.7-4 GHz, "high band" 24-47 GHz mmWave; the named bands (PCS ~1.9 GHz, AWS ~1.7-2.1 GHz) and the 3GPP "n2/n5/n71" numbers sit INSIDE the IEEE letter bands but use a totally separate naming system. Defined in [`dtc_spectrum_access.md`](dtc_spectrum_access.md) and [`spectrum_generations_and_availability.md`](spectrum_generations_and_availability.md) (COMM-104); summarized here.

The same slice of dial has three names at once. Example: **1.9 GHz** is "**L-band** (just inside, since L runs to 2 GHz)" to a radar engineer, "**UHF**" to the ITU (UHF runs to 3 GHz), and "**Broadband PCS / mid-band / 3GPP n2**" to a cellular engineer. All three are correct; all three name the same frequency. Whoever you are talking to is using a different word for the same place.

**The letter-band table (the core deliverable), each band defined below:**

| Band | Frequency | Wavelength* | Principal uses | Propagation character |
|---|---|---|---|---|
| **L** | 1-2 GHz | 30-15 cm | GPS/GNSS, **Iridium/Inmarsat/Globalstar MSS sat-phone**, aircraft ADS-B, some military | Penetrates, reaches far, weather-robust; little bandwidth |
| **S** | 2-4 GHz | 15-7.5 cm | Weather/airport/ship radar, 2.4 GHz Wi-Fi/Bluetooth/microwave ovens, NASA near-Earth (ISS/JWST), some 5G mid-band | Good reach, modest weather loss; the "balanced" low microwave |
| **C** | 4-8 GHz | 7.5-3.75 cm | Satellite-TV downlinks (big-dish FSS), microwave relay, weather radar, 5 GHz Wi-Fi | Rain-robust vs higher bands; the classic FSS workhorse |
| **X** | 8-12 GHz | 3.75-2.5 cm | Military satcom and radar, fire-control/tracking radar, weather radar, deep-space | Tighter beams, more rain loss; defense-heavy |
| **Ku** | 12-18 GHz | 2.5-1.67 cm | **Starlink/VSAT broadband DOWNLINK to dishes**, satellite TV (DBS), backhaul | Good capacity, noticeable rain fade; the broadband user band |
| **K** | 18-27 GHz | 1.67-1.11 cm | Police radar (24 GHz), some satellite; CENTER avoided (water-vapor absorption) | Center near 22 GHz heavily absorbed by water vapor: short range only |
| **Ka** | 27-40 GHz | 1.11-0.75 cm | **Starlink/HTS broadband FEEDER/gateway, Iridium cross-links (~23 GHz K/Ka edge)**, high-throughput satcom, 5G mmWave (~28/39 GHz) | High capacity, strong rain fade; the HTS feeder/mmWave band |
| **V** | 40-75 GHz | 7.5-4 mm | Short-range high-capacity, 60 GHz WiGig (802.11ad/ay), satellite feeder/ISL, mmWave research | 60 GHz oxygen-absorption notch; huge bandwidth, tiny reach |
| **W** | 75-110 GHz | 4-2.7 mm | Automotive radar (77 GHz), mmWave imaging (94 GHz), the 71-76/81-86 GHz satellite "E-band" segment | Very high bandwidth, atmosphere-limited near ground, hard hardware |

\* *Wavelengths are [DERIVED] from `lambda = c/f` with `c = 2.998 x 10^8 m/s` (the relation lives in COMM-561). Worked once below; each band's span is the wavelength at its two frequency edges, so the wavelength shrinks as frequency rises.*

**The four load-bearing confusions (each sourced in Section 4):**
- (a) "**C-band**" means BOTH satellite-TV C-band (4-8 GHz, downlinks at 3.7-4.2 GHz) AND 5G "C-band" (~3.7-3.98 GHz). Same word, two different (overlapping) things.
- (b) The **IEEE letter system is NOT the NATO/EU/ECM letter system** (which relabels the same dial A through M). A "C-band" or "I-band" in a defense context is a different frequency from the IEEE one.
- (c) **THE ONE THAT MATTERS MOST HERE: L-band MSS (~1.6 GHz, Iridium) sits adjacent to cellular mid-band (PCS ~1.9 GHz) but is a DIFFERENT regulatory allocation, and a standard phone has radios for the cellular bands and NOT for L-band MSS.** So "Iridium has spectrum near 1.6-2 GHz" does NOT mean it owns the cellular band a phone uses. This is why owning Iridium does not deliver the direct-to-cell cellular spectrum (COMM-482/COMM-613).
- (d) The letters are **non-sequential by design** (WWII radar secrecy), which is why "K-under" (Ku) and "K-above" (Ka) bracket K, and why the order is L, S, C, X, not A, B, C, D.

**The map to our systems (Section 5):** broadband rides the HIGH satellite letter-bands (Ku user, Ka feeder, plus V/E/W); direct-to-cell rides LOW terrestrial cellular UHF (600-900 MHz low-band, PCS ~1.9 GHz mid-band, which is NOT a satellite letter-band at all); and L/S-band MSS (Iridium) is a THIRD, separate thing (narrowband satellite-to-terminal, not cellular, not broadband). Keep those three lanes apart and the whole study's spectrum picture stays straight.

Everything below is the long-form, sourced version of this screen.

---

## 1. The three vocabularies, stated plainly

People say "what band is that?" and get three different answers because three naming systems run in parallel over the same electromagnetic dial. None is wrong; they answer different questions. Keeping them apart is the single most useful thing this document does.

### 1.1 IEEE letter bands (the satellite/radar convention, our primary language)

The IEEE letter bands divide the microwave region into lettered slabs: L, S, C, X, Ku, K, Ka, V, W (with HF/VHF/UHF below L and "mm/G" above W). The authoritative definition is **IEEE Standard 521** (the radar-bands standard, current edition IEEE Std 521-2002), and the ranges are reproduced identically by the general references ([Wikipedia: Radio spectrum, "IEEE radar bands" table](https://en.wikipedia.org/wiki/Radio_spectrum); [Microwaves101: Frequency Letter Bands, "IEEE Standard 521-2002"](https://www.microwaves101.com/encyclopedias/frequency-letter-bands)) [FACT]. This is the language of satellite communications, radar, and RF engineering, and therefore the primary vocabulary for this study: when the corpus says "Ku user link" or "Ka feeder" or "L-band MSS," these letters are the IEEE letters. Section 2 is the full table, band by band.

### 1.2 ITU numeric bands (by decade of frequency, already defined elsewhere)

The ITU divides the whole radio spectrum (3 Hz to 3,000 GHz) into twelve numbered bands, each a decade of frequency, with names VLF, LF, MF, HF, VHF, UHF, SHF, EHF, and so on. The cellular-relevant ones are **UHF (300-3,000 MHz), SHF (3-30 GHz), and EHF (30-300 GHz)**. This table is already given in full in [`spectrum_and_phased_array_fundamentals.md`](spectrum_and_phased_array_fundamentals.md) (COMM-561), so it is NOT restated here. The point for this doc is only the OVERLAP: UHF (to 3 GHz) covers all of IEEE L (1-2) and S (2-4 dips into SHF at 3 GHz); SHF (3-30 GHz) covers C/X/Ku/K and most of Ka; EHF (30-300 GHz) covers the top of Ka plus V and W. So one ITU band spans several IEEE letter bands, and vice versa: they are two different rulers laid over the same dial.

### 1.3 Cellular naming (low/mid/high band, PCS/AWS/"C-band," and 3GPP n-numbers)

The mobile industry uses its OWN third vocabulary, and it does not use the IEEE letters at all (except, confusingly, by reusing "C-band," Section 4a). Cellular spectrum is grouped as:
- **Low band** (~600/700/800/850/900 MHz): coverage and building penetration. Inside ITU UHF; below IEEE L-band.
- **Mid band** (~1.7-2.6 GHz core, plus 3.5 GHz): the capacity workhorse. Straddles the top of ITU UHF and into IEEE L (to 2 GHz) and S (2-4 GHz).
- **High band** (~24-47 GHz mmWave): huge capacity, tiny reach. Sits in IEEE K/Ka.

On top of those tiers sit NAMED bands (PCS ~1.9 GHz, AWS ~1.7-2.1 GHz, "C-band" ~3.7-4.0 GHz) and the **3GPP "n-number"** identifiers (n71 = 600 MHz, n2 = PCS, n5 = 850 MHz, n41 = 2.5 GHz, n77/n78 = 3.3-4.2 GHz, etc.). A cellular engineer says "n2" or "PCS"; a radar engineer would call that same 1.9 GHz "L-band" (it is just inside L's 1-2 GHz). The cellular and 3GPP naming is defined in [`dtc_spectrum_access.md`](dtc_spectrum_access.md) (the SCS band table) and [`spectrum_generations_and_availability.md`](spectrum_generations_and_availability.md) (COMM-104, "a generation is a standard not a frequency"); this doc only needs the fact that it is a third, separate naming system.

> **COMM-625.** Three parallel vocabularies name the same radio dial, which is the root of band confusion: (a) IEEE letter bands (L/S/C/X/Ku/K/Ka/V/W, from IEEE Std 521, the satellite/radar convention and this study's primary language), (b) ITU numeric bands (VHF/UHF/SHF/EHF by decade of frequency, defined in COMM-561), and (c) cellular naming (low/mid/high band plus PCS, AWS, "C-band," and 3GPP n-numbers). The SAME frequency carries all three names at once: e.g. 1.9 GHz is "L-band" to a radar engineer (L = 1-2 GHz), "UHF" to the ITU (UHF to 3 GHz), and "PCS / mid-band / n2" to a cellular engineer. None is wrong; they answer different questions. **[FACT]** Sources: [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum) (IEEE radar bands + ITU bands tables); [Microwaves101: Frequency Letter Bands](https://www.microwaves101.com/encyclopedias/frequency-letter-bands) (IEEE Std 521-2002); cross-ref corpus COMM-561, COMM-104.
>
> **VERDICT:** there are three names for every spot on the dial. Always ask which vocabulary a number is in before comparing two "bands."

---

## 2. The letter-band table (the core deliverable)

This is the band-letter definition the fundamentals explainer omitted. The ranges are IEEE Std 521, identical across two independent references ([Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum); [Microwaves101: Frequency Letter Bands](https://www.microwaves101.com/encyclopedias/frequency-letter-bands)) [FACT]. Wavelengths are computed once and then read off each band's edges.

**The wavelength relation, worked once [DERIVED].** Every band's wavelength comes from `lambda = c / f`, with `c = 2.998 x 10^8 m/s` (the `c = f x lambda` relation is certified in COMM-561). At a band's LOW frequency edge the wave is LONGEST; at its HIGH edge it is shortest. Worked examples used in the table:
- 1 GHz -> `lambda = 2.998e8 / 1e9 = 0.300 m = 30 cm` (L-band low edge).
- 2 GHz -> 15 cm (L-band high edge = S-band low edge).
- 4 GHz -> 7.5 cm; 8 GHz -> 3.75 cm; 12 GHz -> 2.5 cm; 18 GHz -> 1.67 cm; 27 GHz -> 1.11 cm; 40 GHz -> 0.75 cm = 7.5 mm; 75 GHz -> 4.0 mm; 110 GHz -> 2.7 mm.

So the dial runs from ~30 cm waves at the bottom of L to ~2.7 mm waves at the top of W: a hand-span down to a grain of rice. Shorter waves mean smaller antennas, tighter beams, more bandwidth available, and worse penetration and rain tolerance. That single trend (COMM-561 / COMM-563 in the fundamentals doc) is what makes each band good for what it is good for.

| Band | Frequency (IEEE 521) | Wavelength [DERIVED] | Principal uses | Propagation character |
|---|---|---|---|---|
| **L** | **1-2 GHz** | **30-15 cm** | GPS/GNSS (L1 1575.42, L2 1227.60, L5 1176.45 MHz), Iridium MSS (1616-1626.5 MHz), Inmarsat/Ligado (1525-1646.5 MHz), aircraft ADS-B (1090/978 MHz), radio astronomy (1400-1427 MHz protected) | Long reach, good penetration, weather-robust; LITTLE bandwidth. The "reaches everywhere but narrow" band |
| **S** | **2-4 GHz** | **15-7.5 cm** | Weather/airport/surface-ship radar, 2.4 GHz Wi-Fi (802.11b/g), Bluetooth, microwave ovens (~2.45 GHz), NASA near-Earth (ISS, JWST 2 GHz), some 5G mid-band (2.3-2.6 GHz) | Good reach, modest weather loss; the balanced low-microwave band |
| **C** | **4-8 GHz** | **7.5-3.75 cm** | Satellite-TV / FSS downlinks (3.7-4.2 GHz, "big-dish"), terrestrial microwave relay, weather radar, 5 GHz Wi-Fi (802.11a, 5.7 GHz) | Rain-robust relative to Ku/Ka; the classic fixed-satellite-service workhorse |
| **X** | **8-12 GHz** | **3.75-2.5 cm** | Military satcom and radar, fire-control / target-tracking radar, weather radar, deep-space/Earth-observation | Tighter beams, more rain loss than C; defense-dominated |
| **Ku** | **12-18 GHz** | **2.5-1.67 cm** | Starlink/VSAT broadband user DOWNLINK to dishes (10.7-12.7 GHz region), direct-broadcast satellite TV, backhaul | Good capacity, noticeable rain fade; the broadband USER band |
| **K** | **18-27 GHz** | **1.67-1.11 cm** | Police radar (24 GHz), some satellite; the CENTER (~22 GHz) is avoided | Center near 22.235 GHz heavily absorbed by water vapor: short range only (Section 3) |
| **Ka** | **27-40 GHz** | **1.11-0.75 cm** | Starlink/HTS broadband FEEDER/gateway links, Iridium inter-satellite cross-links (~23 GHz, K/Ka edge), high-throughput satcom, 5G mmWave (~28/39 GHz) | High capacity, strong rain fade; the HTS feeder + mmWave band |
| **V** | **40-75 GHz** | **7.5-4 mm** | Short-range high-capacity links, 60 GHz unlicensed WiGig (802.11ad/ay), satellite feeder and inter-satellite links, mmWave research | 60 GHz OXYGEN-absorption notch (secure short-range); huge bandwidth, tiny reach |
| **W** | **75-110 GHz** | **4-2.7 mm** | Automotive cruise-control radar (77 GHz), mmWave imaging/security (94 GHz), the 71-76/81-86 GHz "E-band" satellite segment, radio astronomy | Very high bandwidth, atmosphere-limited near the ground, hardest hardware |

Sources for the use lists: [Wikipedia: L band](https://en.wikipedia.org/wiki/L_band) (GPS/Iridium/Inmarsat/ADS-B frequencies), [Wikipedia: S band](https://en.wikipedia.org/wiki/S_band) (radar/Wi-Fi/NASA/microwave-oven), [Wikipedia: C band (IEEE)](https://en.wikipedia.org/wiki/C_band_(IEEE)) (FSS downlink/relay/Wi-Fi), [Wikipedia: V band](https://en.wikipedia.org/wiki/V_band) (60 GHz oxygen, WiGig, satellite), [Wikipedia: W band](https://en.wikipedia.org/wiki/W_band) (77 GHz auto radar, 94 GHz imaging, 71-76/81-86 GHz satellite), and the IEEE ranges from [Microwaves101](https://www.microwaves101.com/encyclopedias/frequency-letter-bands) and [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum) [FACT]. (E-band, the 71-76/81-86 GHz part of W used for satellite feeder/backhaul, is covered in [`bands_and_enabling_hardware.md`](bands_and_enabling_hardware.md); see Section 5.)

### 2.1 L-band, defined clearly (the load-bearing band, part 1)

**L-band is 1 to 2 GHz** ([Wikipedia: L band, "1 gigahertz (GHz) to 2 GHz"](https://en.wikipedia.org/wiki/L_band); [Microwaves101](https://www.microwaves101.com/encyclopedias/frequency-letter-bands)) [FACT], wavelengths **30 to 15 cm** [DERIVED]. It is the LOWEST microwave letter band, and its character is "long reach, deep penetration, weather-robust, but little bandwidth": low enough to bend around terrain and pass through obstacles, but so narrow there is almost no room for high data rates. That is why L-band is the home of services that need to reach anywhere on Earth with a small antenna and a tiny data budget: **GPS and all GNSS** (L1 at 1575.42 MHz, L2 at 1227.60 MHz, L5 at 1176.45 MHz), **mobile-satellite-service (MSS) sat-phone and messaging** (Iridium at 1616-1626.5 MHz, Inmarsat/Ligado at 1525-1646.5 MHz, Globalstar, Thuraya), and **aircraft surveillance** (ADS-B at 1090 MHz) ([Wikipedia: L band](https://en.wikipedia.org/wiki/L_band)) [FACT]. The load-bearing fact for THIS study: **Iridium's spectrum is L-band MSS** (COMM-611), a satellite-to-terminal allocation, and Section 4c shows precisely why that is NOT the cellular spectrum a phone uses, even though it sits right next to the cellular mid-band on the dial.

### 2.2 S-band, defined clearly (the load-bearing band, part 2)

**S-band is 2 to 4 GHz** ([Wikipedia: S band, "2 to 4 gigahertz (GHz)"](https://en.wikipedia.org/wiki/S_band); [Microwaves101](https://www.microwaves101.com/encyclopedias/frequency-letter-bands)) [FACT], wavelengths **15 to 7.5 cm** [DERIVED]. It sits just above L and is the "balanced low-microwave" band: still good reach and only modest weather loss, but with more room than L. Its uses are a grab-bag that explains why "S-band" can mean very different things to different people: **radar** (airport-surveillance, weather, surface-ship), the entire **2.4 GHz unlicensed ISM band** (Wi-Fi 802.11b/g, Bluetooth, cordless phones, microwave ovens at ~2.45 GHz), **NASA near-Earth links** (the ISS and JWST use 2 GHz S-band), and **some 5G mid-band** (2.3-2.6 GHz) ([Wikipedia: S band](https://en.wikipedia.org/wiki/S_band)) [FACT]. For the corpus, S-band matters because AST SpaceMobile holds some S-band spectrum (noted in the fundamentals doc, COMM-572) and because the 2.4 GHz Wi-Fi most readers know IS S-band, which makes it a useful anchor: "S-band is the band your home Wi-Fi and microwave oven live in."

> **COMM-626.** IEEE letter bands (IEEE Std 521): L = 1-2 GHz, S = 2-4, C = 4-8, X = 8-12, Ku = 12-18, K = 18-27, Ka = 27-40, V = 40-75, W = 75-110 GHz. Wavelengths (lambda = c/f, c = 2.998e8 m/s) run from ~30 cm at the bottom of L to ~2.7 mm at the top of W; shorter waves -> smaller antennas, tighter beams, more bandwidth, worse penetration/rain tolerance. **[FACT for ranges (2 independent sources); DERIVED for wavelengths]** Sources: [Microwaves101: Frequency Letter Bands](https://www.microwaves101.com/encyclopedias/frequency-letter-bands) (IEEE Std 521-2002, verbatim ranges); [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum) (IEEE radar bands table, identical ranges); wavelength relation cross-ref COMM-561.
>
> **COMM-627.** L-band = 1-2 GHz (30-15 cm): the lowest microwave letter band, long reach + good penetration + weather-robust but little bandwidth; home of GPS/GNSS (L1 1575.42, L2 1227.60, L5 1176.45 MHz), mobile-satellite-service sat-phone/messaging (Iridium 1616-1626.5 MHz, Inmarsat/Ligado 1525-1646.5 MHz, Globalstar, Thuraya), and aircraft ADS-B (1090 MHz). Iridium's spectrum is L-band MSS (satellite-to-terminal), the load-bearing band for the Iridium-vs-cellular distinction (Section 4c, COMM-611/613). **[FACT]** Sources: [Wikipedia: L band](https://en.wikipedia.org/wiki/L_band) (1-2 GHz verbatim, GPS/Iridium/Inmarsat/ADS-B frequencies); [Microwaves101](https://www.microwaves101.com/encyclopedias/frequency-letter-bands); cross-ref corpus COMM-611.
>
> **COMM-628.** S-band = 2-4 GHz (15-7.5 cm): the balanced low-microwave band just above L; uses span radar (airport/weather/ship), the 2.4 GHz unlicensed ISM band (Wi-Fi 802.11b/g, Bluetooth, microwave ovens ~2.45 GHz), NASA near-Earth links (ISS, JWST at 2 GHz), and some 5G mid-band (2.3-2.6 GHz). A useful anchor: S-band is where home Wi-Fi and microwave ovens live. **[FACT]** Sources: [Wikipedia: S band](https://en.wikipedia.org/wiki/S_band) (2-4 GHz verbatim, radar/Wi-Fi/NASA/oven uses); [Microwaves101](https://www.microwaves101.com/encyclopedias/frequency-letter-bands).
>
> **VERDICT:** the letter table is the dial. L (1-2 GHz) reaches everywhere with little bandwidth and is where Iridium and GPS live; S (2-4 GHz) is the balanced band of Wi-Fi and radar; capacity rises and reach falls as you climb to W.

---

## 3. Why the letters are non-sequential (the WWII naming origin)

The obvious question on first sight of the table is: **why L, S, C, X, Ku, K, Ka and not A, B, C, D?** The answer is wartime secrecy, and it is well documented.

**The letters were deliberately scrambled during WWII to confuse the enemy.** Radar was the first microwave application, developed under wartime secrecy, and the band letters were "originally contrived during World War II to confuse the enemy," with engineers at Fort Monmouth, New Jersey assigning non-obvious letter codes rather than a tidy A/B/C sequence ([Microwaves101: Frequency Letter Bands](https://www.microwaves101.com/encyclopedias/frequency-letter-bands)) [FACT-SS on the Fort Monmouth attribution; the "WWII secrecy" origin is corroborated by [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum), "This convention began around World War II with military designations for frequencies used in radar"]. The letters were picked to be MEANINGLESS to an interceptor, which is exactly why they look random today.

**The mnemonics behind each letter (the standard etymology):**
- **L = "Long" wave** (the lowest, longest-wavelength microwave band).
- **S = "Short" wave** (above L; shorter waves than L).
- **C = "Compromise"** between S and X (it sits between them at 4-8 GHz).
- **X = "cross"** (as in crosshair): X-band was used in WWII for fire-control / targeting radar, hence "X for cross."
- **K = "Kurz"** (German for "short"): the original short-wavelength band around 22 GHz.
- **Ku = "K-under"** (just BELOW K, 12-18 GHz) and **Ka = "K-above"** (just ABOVE K, 27-40 GHz).
- **V = "Very"** high frequency band (40-75 GHz).

([Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum) gives L=long, S=short, K=kurz, Ku=kurz-under, Ka=kurz-above, X=cross-for-crosshair; [Microwaves101](https://www.microwaves101.com/encyclopedias/frequency-letter-bands) gives the same set plus C=compromise and V=very) [FACT, 2 independent sources on L/S/X/K/Ku/Ka; C and V single-source-class].

The Ku/K/Ka structure is not arbitrary: it brackets the original K-band, and there is a PHYSICAL reason K-band's center is split off and avoided.

**Why K-band is split into Ku and Ka: the water-vapor absorption peak.** The middle of K-band, near **22.235 GHz**, is the location of a strong **atmospheric water-vapor absorption line** (a molecular resonance of H2O). Frequencies right around there are heavily attenuated by water vapor in the air and "cannot be used for long-distance applications," so the usable spectrum was effectively split into a piece BELOW the absorption (Ku, "K-under," 12-18 GHz) and a piece ABOVE it (Ka, "K-above," 27-40 GHz), leaving the absorbed center (~18-27 GHz K-band) for short-range uses like police radar at 24 GHz ([search-corroborated: "the K-band between 18 and 26.5 GHz are absorbed by water vapor ... due to its resonance peak at 22.24 GHz ... cannot be used for long-distance applications"; the 22.235 GHz water-vapor line is a standard atmospheric constant: at 1-300 GHz, gaseous absorption is dominated by water-vapor lines at 22 and 183 GHz and oxygen near 60 GHz]; cross-ref [Wikipedia: K band (IEEE)](https://en.wikipedia.org/wiki/K_band_(IEEE))) [FACT]. So the naming (K-under / K-above) and the physics (avoid the water-vapor peak in the middle of K) are the same story: the band was split around an atmospheric hole. This is the same atmospheric-absorption physics the band-ladder doc invokes for the bands above Ka ([`bands_and_enabling_hardware.md`](bands_and_enabling_hardware.md)), and it explains the analogous notch at 60 GHz in V-band (oxygen, not water vapor; [Wikipedia: V band](https://en.wikipedia.org/wiki/V_band)).

> **COMM-629.** The IEEE band letters are non-sequential by design: they were contrived during WWII (radar, the first microwave application; engineers at Fort Monmouth, NJ) to confuse the enemy, so the order is L, S, C, X, ... not A, B, C, D. The mnemonics: L = "long," S = "short," C = "compromise" (between S and X), X = "cross" (WWII fire-control crosshair), K = "kurz" (German "short"), Ku = "K-under" (below K), Ka = "K-above" (above K), V = "very" high. **[FACT for L/S/X/K/Ku/Ka (2 sources); FACT-SS for C/V and the Fort Monmouth attribution]** Sources: [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum) (WWII origin; L=long, S=short, K=kurz, Ku/Ka under/above, X=cross); [Microwaves101: Frequency Letter Bands](https://www.microwaves101.com/encyclopedias/frequency-letter-bands) (Fort Monmouth, "to confuse the enemy"; C=compromise, V=very).
>
> **COMM-630.** K-band is split into Ku ("K-under," 12-18 GHz) and Ka ("K-above," 27-40 GHz) around a PHYSICAL feature: the center of K-band near 22.235 GHz is a strong atmospheric WATER-VAPOR absorption line (an H2O molecular resonance), so ~18-27 GHz is heavily attenuated and useful only at short range (e.g. 24 GHz police radar). At 1-300 GHz, gaseous absorption is dominated by water-vapor lines at 22 and 183 GHz and oxygen near 60 GHz (which gives V-band its 60 GHz notch). The naming and the physics are one story: split the band around the atmospheric hole. **[FACT]** Sources: [Wikipedia: K band (IEEE)](https://en.wikipedia.org/wiki/K_band_(IEEE)) and atmospheric-absorption references (22.235 GHz water-vapor line; "K-band ... absorbed by water vapor ... resonance peak at 22.24 GHz"); [Wikipedia: V band](https://en.wikipedia.org/wiki/V_band) (60 GHz oxygen absorption); cross-ref [`bands_and_enabling_hardware.md`](bands_and_enabling_hardware.md).
>
> **VERDICT:** the scrambled letters are a WWII secrecy artifact, and Ku/Ka bracket an atmospheric water-vapor hole at ~22 GHz. The naming looks random but the K-split is physics.

---

## 4. The load-bearing confusions

Four specific naming collisions cause real errors. Each is its own subsection, with sources.

### 4a. "C-band" means satellite-TV C-band AND 5G "C-band" (same word, two things)

**Satellite C-band** is the IEEE letter band 4-8 GHz, with the famous satellite-TV downlinks at **3.7-4.2 GHz** (the "big-dish" television-receive-only band) and uplinks at 5.925-6.425 GHz ([Wikipedia: C band (IEEE)](https://en.wikipedia.org/wiki/C_band_(IEEE)), "4.0 to 8.0 gigahertz," downlinks "3.7-4.2 GHz") [FACT].

**5G "C-band"** is a DIFFERENT, narrower thing: in the US the FCC's C-band 5G proceeding and December 2020 auction (Auction 107, the ~$81B one in COMM-026/COMM-040) repurposed the LOWER part of that satellite downlink range, **3.7-3.98 GHz**, for terrestrial 5G mobile, with a 20 MHz guard band at 3.98-4.0 GHz protecting the satellite users who kept 4.0-4.2 GHz ([Wikipedia: C band (IEEE)](https://en.wikipedia.org/wiki/C_band_(IEEE)), "5G terrestrial C-band: 3.7-3.98 GHz ... a 20-megahertz guard band at 3.98-4.0 GHz") [FACT]. So when a satellite engineer says "C-band" they mean 4-8 GHz (with TV at 3.7-4.2); when a cellular engineer says "C-band" they mean the 3.7-3.98 GHz 5G mid-band carved out of the bottom of it. Same word, overlapping-but-different ranges, two industries. This is a live source of confusion in any "is C-band cellular or satellite?" question: the answer is BOTH, depending on who is speaking.

> **COMM-631.** "C-band" names two different (overlapping) things. SATELLITE C-band = IEEE 4-8 GHz, with TV/FSS downlinks at 3.7-4.2 GHz ("big-dish") and uplinks 5.925-6.425 GHz. 5G "C-band" = the narrower 3.7-3.98 GHz carved from the bottom of the satellite downlink range for terrestrial 5G (US Auction 107, Dec 2020), with a 20 MHz guard band at 3.98-4.0 GHz protecting satellite users above 4.0 GHz. Same word, two industries: "is C-band satellite or cellular?" answers BOTH, depending on the speaker. **[FACT]** Sources: [Wikipedia: C band (IEEE)](https://en.wikipedia.org/wiki/C_band_(IEEE)) (4-8 GHz; 3.7-4.2 satellite; 3.7-3.98 5G + guard band, verbatim); cross-ref corpus COMM-026/COMM-040 (the ~$81B C-band auction).
>
> **VERDICT:** "C-band" is two different bands sharing one name (satellite 4-8 GHz vs 5G 3.7-3.98 GHz). Always pin the frequency.

### 4b. The IEEE letter system is NOT the NATO/EU/ECM letter system

There is a SECOND, completely separate letter system for the radio dial: the **NATO / EU / US-military electronic-warfare (ECM) band letters**, which run **A through M** and assign letters to frequencies DIFFERENTLY from IEEE. In the NATO system, band "A" runs all the way up to ~250 MHz and the higher bands are a near-logarithmic progression, so the NATO letters do NOT line up with the IEEE letters at all ([Microwaves101: Frequency Letter Bands](https://www.microwaves101.com/encyclopedias/frequency-letter-bands), which lists a separate "EW letter bands" A-M table with "entirely different frequency ranges") [FACT].

Concrete mismatches: the **NATO I-band is 8-10 GHz** (the lower part of IEEE X-band, 8-12 GHz); the **NATO J-band is 10-20 GHz** (spanning the top of IEEE X plus all of IEEE Ku); and NATO "M-band" (60-100 GHz) overlaps IEEE V/W ([Wikipedia: W band](https://en.wikipedia.org/wiki/W_band) notes W "overlaps NATO's M band (60-100 GHz)"; search-corroborated NATO I = 8-10 GHz, J = 10-20 GHz) [FACT]. The practical hazard: **a "C-band" or "I-band" in a defense or electronic-warfare context is a different frequency from the IEEE one.** When reading a radar or EW source, you must know which letter system it uses. For this study the rule is simple: the corpus uses IEEE letters throughout (Ku user, Ka feeder, L-band MSS), and any defense-sourced band letter must be checked against the NATO table before it is compared to an IEEE band.

> **COMM-632.** The IEEE radar-band letters are NOT the NATO/EU/US-military electronic-warfare (ECM) band letters, a separate A-through-M system with different assignments (NATO "A" runs to ~250 MHz; the higher bands are near-logarithmic). Mismatches: NATO I-band = 8-10 GHz (lower IEEE X); NATO J-band = 10-20 GHz (top of IEEE X + all IEEE Ku); NATO M-band 60-100 GHz overlaps IEEE V/W. So a "C-band" or "I-band" in a defense/EW context is a DIFFERENT frequency from the IEEE one; defense-sourced band letters must be checked against the NATO table before comparing to IEEE. This study uses IEEE letters throughout. **[FACT]** Sources: [Microwaves101: Frequency Letter Bands](https://www.microwaves101.com/encyclopedias/frequency-letter-bands) (separate EW A-M table); [Wikipedia: W band](https://en.wikipedia.org/wiki/W_band) (W overlaps NATO M 60-100 GHz); NATO band references (I = 8-10, J = 10-20 GHz).
>
> **VERDICT:** two letter systems exist (IEEE and NATO/EW) and they disagree. A defense "C-band" is not an IEEE C-band; confirm the frequency.

### 4c. L-band MSS is adjacent to cellular mid-band but is a DIFFERENT allocation (the one that matters most)

This is the most decision-relevant confusion in the entire study, because it is why owning Iridium does NOT hand Rocket Lab the direct-to-cell cellular spectrum.

**On the dial, they are neighbors.** Iridium's L-band MSS sits at **1616-1626.5 MHz (~1.6 GHz)** (COMM-611). The cellular mid-band sits just above it: Broadband PCS at **1850-1995 MHz (~1.9 GHz)** and AWS at **~1.7-2.1 GHz** (COMM-484, the SCS band table). They are within a few hundred MHz of each other, both "just under 2 GHz," both technically inside or at the edge of IEEE L-band (which runs to 2 GHz). A naive reading is: "Iridium has spectrum near 1.6-2 GHz, and cellular is near 1.9-2 GHz, so Iridium has roughly the cellular band." **That reading is wrong.**

**They are different regulatory allocations, and a phone has a radio for one and not the other.** Adjacency on the frequency axis does NOT mean interchangeable. Two things separate them:
1. **Different allocation / service.** L-band MSS (Mobile-Satellite Service) is spectrum reserved for SATELLITE-to-terminal links; cellular PCS/AWS is spectrum allocated for TERRESTRIAL mobile. They are different lines in the regulator's table of allocations, licensed to different holders for different purposes, and a satellite cannot simply transmit cellular traffic on an MSS allocation or vice versa without a regulatory change.
2. **Different radio in the phone (the decisive one).** A standard 3GPP smartphone has front-end filters, duplexers, and power amplifiers for the CELLULAR bands (~600 MHz to ~2.1 GHz: 600/700/800/850/900 MHz, PCS, AWS, etc.) and **carries no L-band MSS radio** and no Iridium waveform (COMM-482/COMM-613). So even though 1.6 GHz (Iridium) and 1.9 GHz (PCS) are close on the dial, **the phone can tune the 1.9 GHz cellular band and physically cannot receive the 1.6 GHz MSS band**, because it has no radio for it. Iridium's network therefore talks to PURPOSE-BUILT Iridium terminals (sat phones, IoT modems), not to ordinary smartphones on its native L-band.

**The consequence for the study (stated correctly).** "Iridium has globally coordinated L-band spectrum near 1.6 GHz" is true and valuable, but it is NOT the same as "Iridium has the cellular band a phone uses for direct-to-cell." Owning Iridium delivers a constellation, ground, customers, and an owned narrowband MSS spectrum position, but it does NOT deliver the **cellular low/mid-band** that the direct-to-cell thesis needs, because that band is a different allocation the phone is built for and the MSS band is not (COMM-613, COMM-624). The direct-to-cell cellular spectrum remains a separate acquisition (SCS lease of a carrier's band, or a multi-billion cellular-spectrum purchase; COMM-491). This is the exact, correct reason the "buy Iridium = get D2C spectrum" shortcut fails.

> **COMM-633.** L-band MSS (Iridium, 1616-1626.5 MHz, ~1.6 GHz) is ADJACENT on the dial to cellular mid-band (PCS 1850-1995 MHz ~1.9 GHz; AWS ~1.7-2.1 GHz), all near/under 2 GHz and at the edge of IEEE L-band, but they are DIFFERENT regulatory allocations: MSS is satellite-to-terminal spectrum, PCS/AWS is terrestrial cellular, licensed separately for different services. Decisively, a standard 3GPP phone has radios for the cellular bands (~600 MHz-2.1 GHz) and NO L-band MSS radio (COMM-482), so it can tune 1.9 GHz cellular but physically cannot receive 1.6 GHz MSS. Therefore "Iridium has spectrum near 1.6-2 GHz" does NOT mean it has the cellular band a phone uses; owning Iridium does not deliver direct-to-cell cellular spectrum (the cellular band stays a separate SCS-lease-or-buy acquisition, COMM-491). **[FACT]** Sources: corpus gate COMM-482 ([`dtc_spectrum_access.md`](dtc_spectrum_access.md), phone has no L-band MSS radio) and the SCS band list COMM-484 (same doc), and COMM-611/613/624 ([`iridium_acquisition.md`](../rocket_lab/iridium_acquisition.md), Iridium L-band and the distinction); [Wikipedia: L band](https://en.wikipedia.org/wiki/L_band) (1.6 GHz Iridium, MSS allocations).
>
> **VERDICT:** L-band MSS (1.6 GHz) and cellular PCS (1.9 GHz) are dial-neighbors but different allocations, and a phone has a radio for the cellular one and not the MSS one. Adjacency is not interchangeability; this is exactly why Iridium L-band is not the D2C cellular band.

### 4d. (Recap) The non-sequential letters and the K-split

Covered in Section 3 and folded in for completeness: the letters are scrambled (WWII secrecy), and Ku/K/Ka bracket the ~22 GHz water-vapor hole. Listed here only so the "load-bearing confusions" list is complete; no separate claim ID (see COMM-629/630).

---

## 5. The map to our systems

This ties every system in the study to its bands, and makes explicit the THREE separate lanes: high satellite letter-bands for broadband, low terrestrial cellular UHF for direct-to-cell, and L/S-band MSS as a third thing.

| System | Link | Band(s) | Frequency | Lane |
|---|---|---|---|---|
| **Iridium** (MSS) | User links (to Iridium terminals) | **L-band** | 1616-1626.5 MHz (~1.6 GHz) | L/S-band MSS (lane 3) |
| **Iridium** (MSS) | Inter-satellite cross-links | **Ka-band** (~K/Ka edge) | ~23 GHz (22.55-23.55) | (feeder/ISL) |
| **Iridium** (MSS) | Gateway feeder links | **Ka-band** | 19.4-19.6 / 29.1-29.3 GHz | (feeder) |
| **Starlink BROADBAND** | User links (to dishes) | **Ku-band** | ~10.7-12.7 (down) / 14.0-14.5 (up) GHz | High satellite letter-bands (lane 1) |
| **Starlink BROADBAND** | Gateway/feeder links | **Ka-band** | ~17.8-19.3 / 27.5-30 GHz | High satellite letter-bands (lane 1) |
| **Starlink BROADBAND** | Backhaul (Gen2) | **E-band** (in W) | 71-76 / 81-86 GHz | High satellite letter-bands (lane 1) |
| **Starlink BROADBAND** | Additional (Gen2) | **V-band / W-band** | 37.5-51.4 GHz (V); >75 GHz (W) | High satellite letter-bands (lane 1) |
| **Starlink DIRECT-TO-CELL** | To unmodified phones | **terrestrial cellular** (PCS) | 1910-1915 / 1990-1995 MHz (T-Mobile G-block) | Low terrestrial cellular UHF (lane 2) |
| **AST DIRECT-TO-CELL** | To unmodified phones | **terrestrial cellular** (700/850) | ~700/850 MHz (AT&T/Verizon, FirstNet 700) | Low terrestrial cellular UHF (lane 2) |
| **Neutron Flatellite DIRECT-TO-CELL (ours)** | To unmodified phones | **terrestrial cellular** low/mid | ~600-900 MHz low-band, PCS/AWS ~1.9-2 GHz mid-band | Low terrestrial cellular UHF (lane 2) |

Sources: Iridium L-band/Ka per COMM-611/612 ([`iridium_acquisition.md`](../rocket_lab/iridium_acquisition.md)); Starlink Ku/Ka/E/V/W per COMM-178..190 ([`../competitors/starlink_v3_v4_spectrum_incorporation.md`](../competitors/starlink_v3_v4_spectrum_incorporation.md)); Starlink/AST D2C cellular bands and the Neutron D2C band set per COMM-484 ([`dtc_spectrum_access.md`](dtc_spectrum_access.md), SCS band table) [FACT].

**The three lanes, stated explicitly (the takeaway of this whole doc):**

1. **Broadband rides the HIGH satellite letter-bands (Ku/Ka, plus V/E/W).** Starlink's broadband user link is **Ku** (12-18 GHz, used at ~10.7-12.7 down), its feeder is **Ka** (27-40 GHz region), and Gen2 adds **E-band** (71-76/81-86 GHz, the satellite-feeder slice of W) and **V/W**. Why high? Because the customer has a DISH (high gain, can point), so the link closes at high-order modulation on wide high-band channels (the aperture-and-spectrum asymmetry, COMM-313 in [`dtc_antenna_aperture_tradeoff.md`](dtc_antenna_aperture_tradeoff.md)). Broadband is a HIGH-band, wide-channel, dish-terminal story.

2. **Direct-to-cell rides LOW terrestrial cellular UHF, which is NOT a satellite letter-band at all.** Starlink D2C, AST D2C, and our Neutron Flatellite D2C all transmit on **terrestrial cellular spectrum** the phone already supports: low-band 600-900 MHz and lower-mid-band PCS ~1.9 GHz / AWS ~2 GHz. This is BORROWED terrestrial cellular spectrum (leased from a carrier under SCS, or bought), and in IEEE letter terms it sits at the very bottom of the dial (ITU UHF, below or just into IEEE L), NOT in any satellite letter-band. Why low? Because the phone supplies NO gain and has ONLY the cellular radios, so the satellite must use a low cellular band the phone can both reach (link budget) and tune (it has the radio). Direct-to-cell is a LOW-band, thin-channel, bare-phone story.

3. **L/S-band MSS (Iridium) is a THIRD, separate thing.** Iridium's L-band (~1.6 GHz) is neither the high broadband bands nor the borrowed cellular bands: it is a narrowband MOBILE-SATELLITE-SERVICE allocation for satellite-to-terminal links to purpose-built Iridium hardware. It is owned and globally coordinated (rare and valuable), but it talks to Iridium terminals, not to unmodified phones, and not at broadband rates. MSS is its own lane: owned satellite spectrum, narrowband, purpose-built terminals.

**Keeping the three lanes apart is the point.** A great deal of confusion in the study dissolves once you hold these three lanes separate: broadband = high satellite letter-bands to a dish; direct-to-cell = low terrestrial cellular UHF to a bare phone; Iridium MSS = owned L-band to a sat-phone. They use different parts of the dial, different terminals, and different business and regulatory paths, even though two of them (Iridium L-band and cellular mid-band) happen to be dial-neighbors near 2 GHz (Section 4c).

> **COMM-634.** The study's systems map to three SEPARATE band lanes. (1) BROADBAND rides the HIGH satellite letter-bands: Starlink broadband uses Ku user downlink (~10.7-12.7 GHz, IEEE Ku 12-18), Ka feeder (27-40 GHz region), plus Gen2 E-band (71-76/81-86 GHz) and V/W; it works because the dish has gain and can point (high-band, wide-channel, dish terminal). (2) DIRECT-TO-CELL rides LOW terrestrial cellular UHF (NOT a satellite letter-band): Starlink D2C on PCS ~1.9 GHz (T-Mobile G-block 1910-1915/1990-1995 MHz), AST D2C on 700/850 MHz, and our Neutron Flatellite D2C on ~600-900 MHz low-band + PCS/AWS ~1.9-2 GHz, all borrowed terrestrial cellular spectrum the phone already supports (low-band, thin-channel, bare phone). (3) L/S-band MSS (Iridium, ~1.6 GHz L-band) is a THIRD lane: owned narrowband mobile-satellite spectrum to purpose-built terminals, neither broadband nor cellular. **[FACT]** Sources: Iridium per COMM-611/612; Starlink per COMM-178..190 ([`../competitors/starlink_v3_v4_spectrum_incorporation.md`](../competitors/starlink_v3_v4_spectrum_incorporation.md)); D2C cellular bands per COMM-484 ([`dtc_spectrum_access.md`](dtc_spectrum_access.md)); aperture-and-spectrum asymmetry COMM-313 ([`dtc_antenna_aperture_tradeoff.md`](dtc_antenna_aperture_tradeoff.md)).
>
> **VERDICT:** three lanes, three parts of the dial: broadband on HIGH satellite Ku/Ka (to a dish), direct-to-cell on LOW cellular UHF (to a bare phone, borrowed spectrum), Iridium on owned L-band MSS (to a sat-phone). Hold them apart and the spectrum picture is clean.

---

## 6. How to use this document

- **Placing any band:** read its row in Section 2. You get its frequency, its wavelength, what uses it, and how it propagates. L (1-2 GHz, Iridium/GPS, far reach) and S (2-4 GHz, Wi-Fi/radar) are featured in 2.1-2.2.
- **Translating between vocabularies:** Section 1. A cellular "mid-band / PCS / n2" number is an IEEE "L-band" frequency and an ITU "UHF" frequency, all at once.
- **Avoiding the four traps:** Section 4. "C-band" is two things (4a); IEEE letters are not NATO letters (4b); Iridium L-band is not the cellular band (4c, the load-bearing one); the letters are scrambled and Ku/Ka bracket a water-vapor hole (4d/Section 3).
- **Mapping our systems:** Section 5. Three lanes: broadband on high Ku/Ka, direct-to-cell on low cellular UHF, Iridium on owned L-band MSS.
- **What this doc does NOT cover (by design, cross-referenced):** what spectrum IS and the wave physics, the ITU numeric table, the frequency-vs-bandwidth-vs-data-rate distinction, and antennas/phased arrays all live in [`spectrum_and_phased_array_fundamentals.md`](spectrum_and_phased_array_fundamentals.md) (COMM-561..573). The upper-band hardware/silicon and the V/E/W/optical ladder live in [`bands_and_enabling_hardware.md`](bands_and_enabling_hardware.md). The cellular generations and the SCS access mechanism live in [`spectrum_generations_and_availability.md`](spectrum_generations_and_availability.md) and [`dtc_spectrum_access.md`](dtc_spectrum_access.md).

---

## 7. Open questions / caveats

1. **Band-edge variation across systems.** IEEE 521 gives clean letter-band edges (L = 1-2 GHz, etc.), but real systems use sub-ranges that sometimes straddle a letter boundary (Iridium's ~23 GHz cross-links sit at the K/Ka edge; satellite C-band TV at 3.7-4.2 GHz dips just below the IEEE 4 GHz C-band floor). The letter is a label for a region, not a hard wall a system stays inside. Always confirm the actual MHz. [Noted, not a defect.]
2. **C/V single-source mnemonics.** The "C = compromise" and "V = very" etymologies are single-source-class (Microwaves101); the L/S/X/K/Ku/Ka mnemonics are 2-source. The frequency RANGES are all 2-source FACT; only those two letter-meaning stories are softer. [FACT-SS flagged.]
3. **Exact K-split edges.** Sources state K-band as 18-27 GHz (IEEE) but the "absorbed center" is variously given as ~18-26.5 or ~22-24 GHz depending on the reference; the 22.235 GHz water-vapor line itself is a firm constant. The split RATIONALE is solid; the exact "avoid" window edges are soft. [Noted.]
4. **NATO band table not reproduced in full.** This doc establishes that the NATO/EW A-M system differs from IEEE and gives example mismatches (I = 8-10, J = 10-20, M = 60-100 GHz), but does not reproduce the full NATO table; if a defense source must be reconciled band-by-band, pull the full NATO table then. [Scoped out.]

---

## 8. Claims Ledger

Claim IDs use the next free contiguous block above the prior global maximum (COMM-624, held by [`iridium_acquisition.md`](../rocket_lab/iridium_acquisition.md)). This doc uses **COMM-625..634** (10 hard claims). The fundamentals companion reserved COMM-561..600 and used 561..573; the Iridium doc used 601..624; no collision.

| ID | Claim (short) | Tag | Sources |
|---|---|---|---|
| **COMM-625** | Three parallel vocabularies name the same dial (IEEE letter / ITU numeric / cellular), which is the root of band confusion; the same frequency (e.g. 1.9 GHz) is "L-band," "UHF," and "PCS/mid-band/n2" at once. | [FACT] | [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum); [Microwaves101: Frequency Letter Bands](https://www.microwaves101.com/encyclopedias/frequency-letter-bands); cross-ref COMM-561, COMM-104. |
| **COMM-626** | IEEE 521 letter bands: L 1-2, S 2-4, C 4-8, X 8-12, Ku 12-18, K 18-27, Ka 27-40, V 40-75, W 75-110 GHz; wavelengths ~30 cm (L) to ~2.7 mm (W) via lambda = c/f. | [FACT ranges (2 src); DERIVED wavelengths] | [Microwaves101](https://www.microwaves101.com/encyclopedias/frequency-letter-bands) (IEEE Std 521-2002); [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum); wavelength cross-ref COMM-561. |
| **COMM-627** | L-band = 1-2 GHz (30-15 cm): long reach, penetrating, weather-robust, little bandwidth; GPS (L1 1575.42, L2 1227.60, L5 1176.45 MHz), MSS sat-phone (Iridium 1616-1626.5, Inmarsat/Ligado 1525-1646.5 MHz), ADS-B (1090 MHz). Iridium's band; the load-bearing band for the cellular distinction. | [FACT] | [Wikipedia: L band](https://en.wikipedia.org/wiki/L_band); [Microwaves101](https://www.microwaves101.com/encyclopedias/frequency-letter-bands); cross-ref COMM-611. |
| **COMM-628** | S-band = 2-4 GHz (15-7.5 cm): balanced low-microwave; radar (airport/weather/ship), 2.4 GHz Wi-Fi/Bluetooth/microwave ovens, NASA near-Earth (ISS/JWST 2 GHz), some 5G mid-band. Anchor: S-band is home Wi-Fi and microwave ovens. | [FACT] | [Wikipedia: S band](https://en.wikipedia.org/wiki/S_band); [Microwaves101](https://www.microwaves101.com/encyclopedias/frequency-letter-bands). |
| **COMM-629** | The IEEE band letters are non-sequential by WWII-radar secrecy design (Fort Monmouth, "to confuse the enemy"): L=long, S=short, C=compromise, X=cross (fire-control crosshair), K=kurz (German "short"), Ku=K-under, Ka=K-above, V=very. | [FACT L/S/X/K/Ku/Ka (2 src); FACT-SS C/V + Fort Monmouth] | [Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum); [Microwaves101: Frequency Letter Bands](https://www.microwaves101.com/encyclopedias/frequency-letter-bands). |
| **COMM-630** | K-band is split into Ku (K-under, 12-18) and Ka (K-above, 27-40 GHz) around the ~22.235 GHz atmospheric water-vapor absorption line (H2O resonance), which makes the ~18-27 GHz center short-range only (24 GHz police radar); gaseous absorption at 1-300 GHz is dominated by water vapor at 22/183 GHz and oxygen at 60 GHz (V-band notch). | [FACT] | [Wikipedia: K band (IEEE)](https://en.wikipedia.org/wiki/K_band_(IEEE)) + atmospheric-absorption refs (22.235 GHz line); [Wikipedia: V band](https://en.wikipedia.org/wiki/V_band) (60 GHz O2); cross-ref [`bands_and_enabling_hardware.md`](bands_and_enabling_hardware.md). |
| **COMM-631** | "C-band" = two things: satellite C-band (IEEE 4-8 GHz; TV downlinks 3.7-4.2 GHz) AND 5G "C-band" (3.7-3.98 GHz carved from the bottom for terrestrial 5G, US Auction 107 Dec 2020, 20 MHz guard band at 3.98-4.0). | [FACT] | [Wikipedia: C band (IEEE)](https://en.wikipedia.org/wiki/C_band_(IEEE)); cross-ref COMM-026/040. |
| **COMM-632** | IEEE radar-band letters are NOT the NATO/EU/ECM letters (separate A-M system, different assignments: NATO A to ~250 MHz; I = 8-10, J = 10-20, M = 60-100 GHz). A defense "C-band"/"I-band" is a different frequency from the IEEE one. | [FACT] | [Microwaves101: Frequency Letter Bands](https://www.microwaves101.com/encyclopedias/frequency-letter-bands); [Wikipedia: W band](https://en.wikipedia.org/wiki/W_band) (W overlaps NATO M); NATO band refs. |
| **COMM-633** | L-band MSS (Iridium 1616-1626.5 MHz ~1.6 GHz) is ADJACENT to cellular mid-band (PCS ~1.9 GHz, AWS ~1.7-2.1 GHz) but a DIFFERENT allocation (satellite MSS vs terrestrial cellular); a phone has cellular radios (~600 MHz-2.1 GHz) and NO L-band MSS radio, so "Iridium spectrum near 1.6-2 GHz" is NOT the cellular band a phone uses, and owning Iridium does not deliver D2C cellular spectrum. | [FACT] | corpus COMM-482/484 ([`dtc_spectrum_access.md`](dtc_spectrum_access.md)); COMM-611/613/624 ([`iridium_acquisition.md`](../rocket_lab/iridium_acquisition.md)); [Wikipedia: L band](https://en.wikipedia.org/wiki/L_band). |
| **COMM-634** | The systems map to three lanes: broadband on HIGH satellite letter-bands (Starlink Ku user ~10.7-12.7 GHz, Ka feeder, Gen2 E/V/W, to a dish); direct-to-cell on LOW terrestrial cellular UHF (Starlink PCS ~1.9 GHz, AST 700/850 MHz, Neutron ~600-900 MHz + PCS/AWS, borrowed, to a bare phone); Iridium on owned L-band MSS ~1.6 GHz (to a sat-phone). | [FACT] | COMM-611/612; COMM-178..190 ([`../competitors/starlink_v3_v4_spectrum_incorporation.md`](../competitors/starlink_v3_v4_spectrum_incorporation.md)); COMM-484 ([`dtc_spectrum_access.md`](dtc_spectrum_access.md)). |

---

*Provenance: IEEE 521 letter-band ranges verified verbatim against two independent references ([Wikipedia: Radio spectrum](https://en.wikipedia.org/wiki/Radio_spectrum) and [Microwaves101: Frequency Letter Bands](https://www.microwaves101.com/encyclopedias/frequency-letter-bands), citing IEEE Std 521-2002). Per-band uses from the Wikipedia band pages (L/S/C/V/W band). Naming origins from Wikipedia (Radio spectrum) and Microwaves101. The K-band water-vapor split, C-band confusion, and NATO-vs-IEEE distinction are each 2-source. The L-band-MSS-vs-cellular distinction, the Iridium facts, the Starlink inventory, and the SCS cellular band menu are carried from the corpus (COMM-482/484 for the phone-radio gate and SCS band menu, COMM-611/613 for Iridium, COMM-178..190 for Starlink) and not re-verified here. Wavelengths are DERIVED via lambda = c/f. This doc is the band-letter companion to the spectrum_and_phased_array_fundamentals.md explainer (COMM-561..573), which omitted these definitions. No business verdict rendered. China excluded.*
