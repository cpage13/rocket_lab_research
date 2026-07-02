# Iridium L-Band Capacity and Modernization: How Capacity-Small the As-Built Fleet Is, When It Needs Replacing, and How Much a Modern Digital-Beamforming Satellite on the SAME 8-10.5 MHz Would Carry

*Comms wave 9, Iridium max-outcome inputs (understanding-building, no business verdict). Research date: 2026-07-01.*

**Why this doc exists.** Rocket Lab is acquiring Iridium (the June 29, 2026 deal, CONFIRMED, terms in [`iridium_acquisition.md`](iridium_acquisition.md) COMM-601..624; not re-researched here). The founder wants the MAXIMUM-OUTCOME picture: if a replacement fleet is deployed as fast as possible on Iridium's OWNED L-band spectrum, how many customers could be reached, and how much spectrum is the wall. This doc supplies the CAPACITY PHYSICS layer that the deal doc, the coverage docs, and the D2C capacity docs do not: (1) the technical detail of the Iridium NEXT fleet AS BUILT and how capacity-SMALL it is relative to what its own spectrum could support, (2) WHEN the fleet needs replacement anyway (the natural Neutron hook), (3) the MODERNIZATION PHYSICS: how capacity scales if the same 8-10.5 MHz of L-band flies on a modern large-aperture digital-beamforming satellite instead of the 1990s 48-beam design, (4) the REGULATORY constraints on a much larger fleet on the same band, and (5) the NARROWBAND HEADROOM: how many devices a modernized fleet could hold at Iridium's actual service rates. No go/no-go verdict is rendered.

**Grounds in and does NOT re-derive (cite, do not repeat):**
- [`iridium_acquisition.md`](iridium_acquisition.md) (COMM-601..624): owns the deal, the 66-satellite Walker-Star fleet at 780 km, the L-band allocation (1616-1626.5 MHz = 10.5 MHz total, 7.775 MHz exclusive, 0.95 MHz shared with Globalstar), Certus 704 kbps, NB-IoT Project Stardust, and the 2.537M-subscriber business (FY2025). This doc USES all of those as the starting asset and adds the capacity-physics layer; it does not re-verify the deal or the business.
- [`../direct_communication/dtc_capacity_supply.md`](../direct_communication/dtc_capacity_supply.md) (COMM-406..425): owns the per-satellite supply identity (per-sat capacity = beams x per-cell x spatial-reuse, capped by owned spectrum), the ~5-15 Gbps-on-25-MHz result (COMM-410), the spectrum-binds-not-processor finding (COMM-411), and the spectrum-saturation ceiling (COMM-413..416). This doc SCALES that 25 MHz result down to Iridium's 8 MHz (spectrum-bound, linear in held MHz) for the modernization number; it does not re-derive the identity.
- [`../direct_communication/dtc_subscribers_per_satellite.md`](../direct_communication/dtc_subscribers_per_satellite.md) (COMM-535..560): owns the subscribers-per-satellite result (~50,000-100,000 attached at 25 MHz, the ~75,000 central), the busy-hour concurrency band (~1-5%, central ~2-3%, COMM-543), and the capacity fleet = subscribers / attached-per-sat (COMM-550). This doc CHECKS the model rule (linear in held MHz) against these and applies them at 8 MHz; it does not re-derive them.
- [`../direct_communication/spectrum_capacity_primer.md`](../direct_communication/spectrum_capacity_primer.md) (COMM-426..439): owns Shannon, spectral efficiency, carrier aggregation, and the spatial-reuse-multiplies-system-capacity physics. This doc uses those as the underlying physics; it does not re-explain them.
- [`../direct_communication/dtc_data_rate_vs_spectrum.md`](../direct_communication/dtc_data_rate_vs_spectrum.md) (COMM-493..512): owns the rate-vs-owned-bandwidth curve and the power-limited saturation past ~50-100 MHz. Relevant here only as a boundary: Iridium's 8-10.5 MHz is far BELOW the power knee, so on this thin a band the system is firmly spectrum-bound (bandwidth is the wall, not power).
- [`../direct_communication/spectrum_band_designations.md`](../direct_communication/spectrum_band_designations.md) (COMM-625..634): owns the L-band definition (1-2 GHz) and the three-lanes distinction (Iridium L-band MSS is a different allocation from cellular low-band and from broadband Ku/Ka). This doc keeps CELLULAR / BROADBAND / MSS strictly separate: Iridium is the MSS lane.

> **Reading guide.** Every hard number is tagged **[FACT]** (2+ independent sources, cited inline with URLs), **[FACT-SS]** (single source), **[DERIVED]** (arithmetic on cited inputs), **[ESTIMATE]** (reasoned), or **[UNKNOWN]** (a named gap, never invented). China is excluded (corpus convention). No em-dashes. Inline math: `^2` squared, `x` multiply, `->` arrow. New claim IDs use the RESERVED block **COMM-635..660** (current global max before this doc is COMM-634; not exceeded). No go/no-go verdict.

> **The lane, kept straight (load-bearing).** Iridium's spectrum is **L-band MSS at ~1.6 GHz**, reached by **purpose-built terminals** (sat phones, Certus modems, SBD/NB-IoT chipsets), NOT by an unmodified cellular phone on its native band ([`iridium_acquisition.md`](iridium_acquisition.md) COMM-613, [`spectrum_band_designations.md`](../direct_communication/spectrum_band_designations.md) COMM-633). This whole doc is about the **MSS lane** (Iridium's own band and terminals). "Subscribers" here are PEOPLE or DEVICES on Iridium-type terminals. The 25 MHz D2C numbers from the corpus are borrowed only as a per-aperture, per-beam CAPACITY-PHYSICS benchmark (the physics of beams x reuse x MHz is the same regardless of band or terminal); they are NOT a claim that Iridium's band reaches unmodified phones.

---

## 0. Answer first (the whole capacity story on one screen)

**The Iridium NEXT fleet as built is astonishingly capacity-small relative to what its own spectrum could support, because it is a 1990s architecture: each of the 66 satellites carries a fixed 48-beam L-band phased array (120 elements, a 4,700 km footprint tiled into ~600 km cells) running 252 FDMA carriers of 41.667 kHz each in a hybrid TDMA/TDD frame, and it supports on the order of ~1,100 concurrent 2.4 kbps voice calls, which is only about ~2.6 Mbps of user payload PER SATELLITE, or roughly ~174 Mbps of voice-grade payload across the entire 66-satellite fleet (a theoretical channelized ceiling near ~86 Mbps per satellite, ~5.7 Gbps fleet-wide, once the 48-beam frequency reuse of the 10.5 MHz is counted). That fleet serves 2.537M billable subscribers today, but the overwhelming majority (1.998M) are LOW-DUTY-CYCLE IoT devices sending tiny Short Burst Data messages, so the fleet is subscriber-FULL in device count while running at a trickle of actual bits, which is exactly the point: the current fleet uses its rare L-band spectrum at a small fraction of what modern hardware could wring from it. The replacement window is now pinned: Iridium NEXT launched 2017-2019 with a 12.5-year Thales design life, which a 2024 engineering reassessment extended to ~17.5 years, so the fleet is expected to perform well to AT LEAST 2035, and Iridium has publicly said it will decide on a third-generation constellation to take advantage of the latest technology at the most favorable moment, which is precisely the Neutron-launched-replacement hook. The modernization physics is the core result: if the SAME ~8 MHz of exclusive L-band (or the full ~10.5 MHz) flew on a MODERN large-aperture digital-beamforming satellite (flat ~25 m^2-class panel, hundreds of digitally-formed beams, low orbit ~400-600 km) instead of the fixed 48-beam Iridium NEXT design, aggregate per-satellite capacity would rise by roughly THREE orders of magnitude, to about ~1.6-4.8 Gbps per satellite (central ~2.9 Gbps), because many more, smaller beams reuse the same fixed MHz many more times (spatial frequency reuse is the multiplier, not raw bandwidth, since L-band is narrow), giving fleet aggregates of about ~1.0 Tbps at 340 satellites, ~2.9 Tbps at 1,000, and ~5.8 Tbps at 2,000. Checked against the model rule the founder wants, video-grade broadband subscribers scale linearly with held MHz: the corpus's ~75,000 attached at 25 MHz implies ~24,000 attached per satellite at 8 MHz (exactly ~3,000 subscribers per satellite per MHz, at a ~2.5 Mbps active rate and 2-3% busy-hour concurrency), which totals ~8M subscribers at 340 satellites, ~24M at 1,000, and ~48M at 2,000, all in the SAME order of magnitude as a US-scale subscriber base. The rule holds cleanly BECAUSE the system is spectrum-bound at L-band (linear in held MHz), and it breaks only if power or reuse cannot hold the assumed spectral efficiency, or if subscribers pile into dense cells the fleet cannot densify (the density caveat). Regulatorily, the same-band-larger-fleet path has direct precedent (Iridium NEXT itself replaced the Block 1 fleet under the identical spectrum authorization via a license modification, and the FCC replacement-satellite rule 25.165(e) explicitly contemplates same-band, same-coverage replacements), but a MUCH larger fleet raises open questions on power-flux-density limits, on the Globalstar sharing boundary in 1616-1618.725 MHz (Iridium is actively petitioning the FCC for more of the band as of late 2025, and Globalstar opposes), and on whether a VLEO orbit at a different altitude requires fresh ITU/FCC coordination. Finally, narrowband headroom is effectively UNLIMITED relative to any plausible subscriber base: at Iridium's actual service rates (SBD ~340-byte bursts, voice ~2.4 kbps, NB-IoT kbps-class), a low-duty-cycle device averages a fraction of a bit per second, so a modernized fleet on 8 MHz would hold BILLIONS of narrowband devices, confirming that capacity is NOT the constraint for narrowband IoT or messaging at tens of millions of devices; the constraints there are the business, the terminals, and (for anything broadband or phone-reaching) the spectrum lane and the regulatory questions, none of which this doc resolves.**

Ten findings, each sourced and derived below:

1. **Iridium NEXT as built (Section 1):** 66 satellites, 780 km, 48-beam L-band phased array (120-element, 12x10), 4,700 km footprint (~600 km/beam), 252 FDMA carriers of 41.667 kHz (31.5 kHz occupied, 10.17 kHz guard), DEQPSK, 90 ms TDMA/TDD frame, ~1,100 concurrent 2.4 kbps voice calls per satellite. [FACT]
2. **How capacity-small (Section 1.4):** ~2.6 Mbps voice payload per satellite, ~174 Mbps fleet voice payload, ~86 Mbps/sat theoretical channelized ceiling (~5.7 Gbps fleet) once 48-beam reuse is counted. Tiny relative to the ~1 Tbps a modern fleet on the same band could reach. [DERIVED]
3. **How full today (Section 1.5):** 2.537M billable subscribers, but 1.998M are low-duty-cycle IoT; the fleet is device-full at a trickle of bits, using its rare spectrum at a small fraction of capacity. Even the as-built fleet's ~72,600-172,000 concurrent circuits back out to ~2.4M-17M voice-class subscribers at ~1-3% busy-hour concurrency, so today's base is nowhere near even the OLD fleet's narrowband wall. [FACT + DERIVED]
4. **The replacement window (Section 2):** launched 2017-2019, 12.5-year Thales design life, extended in 2024 to ~17.5 years, performs well to at least 2035; Iridium publicly frames a third-generation constellation as a "latest and greatest at the most favorable moment" decision. The Neutron hook. [FACT]
5. **Modernization per-satellite (Section 3):** the same ~8 MHz on a modern large-aperture DBF satellite yields ~1.6-4.8 Gbps/sat (central ~2.9), roughly ~1,100x the Iridium NEXT voice payload and ~33x its theoretical raw, scaled from the corpus's spectrum-bound 25 MHz result. [DERIVED]
6. **Modernization fleet aggregate (Section 3.4):** ~1.0 Tbps at 340 satellites, ~2.9 Tbps at 1,000, ~5.8 Tbps at 2,000, on 8 MHz. [DERIVED]
7. **The model rule CONFIRMED (Section 3.5):** video-grade subscribers scale linearly with held MHz; ~75,000 at 25 MHz -> ~24,000 at 8 MHz = ~3,000 subs/sat/MHz (2.5 Mbps active, 2-3% concurrency). Fleet: ~8M at 340, ~24M at 1,000, ~48M at 2,000. Holds because L-band is spectrum-bound; breaks on power/reuse shortfall or dense-cell pile-up. [DERIVED, checked]
8. **Why more beams is the lever (Section 3.2):** at narrow L-band, aggregate = MHz x spectral-efficiency x non-overlapping-beam-count; you cannot add MHz (the band is fixed and rare), so the modernization lever is MORE, SMALLER BEAMS (spatial reuse) via a bigger aperture and a lower orbit, plus higher spectral efficiency via ACM. [FACT + DERIVED]
9. **Regulatory (Section 4):** same-band replacement has direct precedent (Iridium NEXT replaced Block 1 under the same authorization; FCC 25.165(e)); open questions are PFD limits, the Globalstar sharing boundary (active 2025-2026 dispute), and fresh coordination if the orbit/altitude changes. [FACT + UNKNOWN]
10. **Narrowband headroom effectively unlimited (Section 5):** a low-duty-cycle SBD/NB-IoT device averages a fraction of a bit per second, so a modernized 8 MHz fleet holds BILLIONS of narrowband devices; capacity is NOT the narrowband constraint at tens of millions of devices. The real narrowband limiter is random-access contention per beam (~57-1,650 devices per access window by mode, a design parameter, not a population cap), plus coverage/revisit, terminals, and business. [DERIVED + FACT-SS]

The rest sources and derives each.

---

## 1. Iridium NEXT as built: the 1990s architecture, quantified

The whole point of this section is to show, with primary-source numbers, that the current fleet is a fixed, low-beam-count, narrowband voice-and-messaging design that uses its rare L-band spectrum at a small fraction of what modern hardware could.

### 1.1 The constellation and the satellite (cross-referenced, not re-derived)

66 operational satellites plus spares, Walker-Star **86.4 deg / 780 km / 66 in 6 planes (11 per plane)**, unique Ka-band inter-satellite cross-links, satellite mass ~860 kg, 10-year design / 15-year planned mission life (see Section 2 for the revised life), built by Thales Alenia Space, launched by SpaceX 2017-2019 ([`iridium_acquisition.md`](iridium_acquisition.md) COMM-608/610; FCC engineering statement below). The orbital parameters are confirmed verbatim in the FCC filing: "66 NEXT SVs, 11 equally spaced SV/Plane, 6 Planes ... nominal circular altitude of 780km ... Inclination = 86.4 deg" [FACT] ([Iridium NEXT FCC Engineering Statement, SAT-MOD-20131227-00148](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf); [eoPortal Iridium NEXT](https://www.eoportal.org/satellite-missions/iridium-next)).

### 1.2 The L-band payload: 48 fixed beams, a 4,700 km footprint

Each satellite carries a **single 48-beam L-band phased-array main mission antenna**, used in **Time Division Duplex (TDD)** for the forward and return service links [FACT]. The FCC filing states it directly: "48 Mobile Satellite Service (MSS) L band beams per satellite to be used in a Time Division Duplex manner for the forward and return service links" [FACT] ([FCC Engineering Statement](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf)). Independent sources add the array and footprint geometry:
- **120-element array, 12-by-10 uniform rectangular array (URA)** [FACT-SS on the element count] ([MathWorks Iridium spot-beam example](https://www.mathworks.com/help/phased/ug/iridium-satellite-spot-beam-coverage-on-map-of-us.html); [MATLAB/Airport-Technology Iridium NEXT project](https://www.airport-technology.com/projects/iridium-next-satellite-constellation/)).
- **48 beams tile a ~4,700 km-diameter footprint, ~600 km per beam** [FACT], arranged as 16 beams in each of 3 sectors ([Wikipedia Iridium satellite constellation](https://en.wikipedia.org/wiki/Iridium_satellite_constellation); [eoPortal Iridium NEXT](https://www.eoportal.org/satellite-missions/iridium-next)).
- Plus **2 Ka-band feeder beams** (20/30 GHz, gateway links) and **4 Ka-band inter-satellite crosslinks** (~23 GHz, 2 fixed fore/aft in-plane + 2 steerable cross-plane), the crosslinks running at **~10 Mbit/s** each [FACT] ([FCC Engineering Statement](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf); [Wikipedia Iridium satellite constellation](https://en.wikipedia.org/wiki/Iridium_satellite_constellation); [eoPortal Iridium NEXT](https://www.eoportal.org/satellite-missions/iridium-next)).

The load-bearing contrast: **48 beams** is a FIXED, hardware-defined cellular pattern from a 120-element array. A modern L-band digital-beamforming satellite forms HUNDREDS to THOUSANDS of beams from a far larger aperture (Section 3). The beam count is the master capacity lever at a fixed, narrow band, and Iridium NEXT is at the very low end of it. [FACT + DERIVED]

### 1.3 The channelization: 252 carriers of 41.667 kHz, DEQPSK, a 90 ms frame

This is the crux of "how the 10.5 MHz is used," and the FCC filing pins it exactly:

> "There are 252 carriers in the 1616-1626.5 MHz band in both the uplink and downlink with carrier spacings of 41.667 KHz. The necessary bandwidth for each of these carriers is 35 or 36 kHz. These carriers can be combined to provide wider bandwidth signals with necessary bandwidth up to 288 KHz ... These 252 carrier frequencies can be grouped into sub bands of 8 carriers. The 32nd sub group has 4 carriers." [FACT] ([FCC Engineering Statement, Section G](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf))

The air-interface detail, from independent signal-analysis sources:
- **Modulation: Differentially Encoded QPSK (DEQPSK), 2 bits/symbol**, occupied bandwidth **31.5 kHz** per carrier, guard **10.17 kHz** (31.5 + 10.17 ~= 41.667 kHz spacing) [FACT] ([SigidWiki Iridium](https://www.sigidwiki.com/wiki/Iridium); [Wikipedia Iridium satellite constellation](https://en.wikipedia.org/wiki/Iridium_satellite_constellation)).
- **Frame: 90 ms TDMA/TDD frame, 8.28 ms time slots, 4 TDMA slots per FDMA carrier in each direction**; burst rate **50 kbps** (25,000 baud), duty cycle ~9.2% per slot [FACT] ([SigidWiki Iridium](https://www.sigidwiki.com/wiki/Iridium); [Overview of IRIDIUM satellite network, ResearchGate](https://www.researchgate.net/publication/3622510_Overview_of_IRIDIUM_satellite_network)).
- **Voice codec: 2.4 kbps AMBE (Advanced Multi-Band Excitation) vocoder** [FACT] ([SigidWiki Iridium](https://www.sigidwiki.com/wiki/Iridium); [Wikipedia Iridium satellite constellation](https://en.wikipedia.org/wiki/Iridium_satellite_constellation)).
- **Any of the 252 carriers can be assigned to any of the 48 beams at any time**, and carriers combine (up to ~288 kHz) for wider Certus channels [FACT] ([FCC Engineering Statement](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf); [MathWorks](https://www.mathworks.com/help/phased/ug/iridium-satellite-spot-beam-coverage-on-map-of-us.html)).

The gross channel spectral efficiency is **~1.2 bps/Hz** (50 kbps burst / 41.667 kHz spacing), and net user efficiency is lower after framing, coding, and guard overhead. This is a NARROWBAND, robust, low-efficiency waveform, tuned for reliable global voice and messaging to tiny terminals, not for throughput. [DERIVED]

**The Certus 704 kbps service chain** rides exactly this carrier combining: IF the ~704 kbps Certus peak (COMM-620; [Iridium Certus 700](https://www.iridium.com/services/iridium-certus-700)) rides a combined channel near the FCC filing's ~288 kHz maximum combined necessary bandwidth, the implied efficiency is ~2.4 bps/Hz (704/288), modern-ACM class on the combined channel. That is a consistency inference, not a published link budget, but it supports the ~2-3 bps/Hz assumed for a modern array in Section 3: the NEXT payload already sustains that class of efficiency on its widest channel. [DERIVED, inference on cited inputs]

### 1.4 How capacity-small: ~2.6 Mbps per satellite, ~174 Mbps fleet

Two honest anchors on per-satellite user capacity:

**(a) The voice-payload anchor (the clean, sourced number).** An Iridium satellite supports on the order of **~1,100 concurrent phone calls** [FACT-SS, single strong source] ([HighSpeedSat Iridium](https://www.highspeedsat.com/iridium-satellite.php); consistent with the corpus COMM-610 note). At the 2.4 kbps AMBE vocoder rate:

```
Per-satellite voice payload  =  1,100 calls  x  2.4 kbps  =  ~2.64 Mbps
Fleet (66 satellites)        =  66  x  2.64 Mbps          =  ~174 Mbps  (~0.17 Gbps)
```
[DERIVED, from cited inputs]

The ~1,100 figure is structurally consistent with the channel plan: **252 carriers x 4 duplex TDMA slots = ~1,008 satellite-wide duplex circuits** (the carrier pool is the satellite-level cap) [DERIVED, from COMM-637/638], while the beam-level provisioning is higher, **~80 voice circuits per beam x 48 beams = 3,840 beam-slots** [FACT-SS on the ~80/beam] ([eoPortal Iridium NEXT](https://www.eoportal.org/satellite-missions/iridium-next)). So the binding per-satellite count is the carrier pool, not the beams. Constellation-wide, sourced figures put concurrent capacity at **~172,000 calls** [FACT] ([Wikipedia Iridium](https://en.wikipedia.org/wiki/Iridium_satellite_constellation); [HighSpeedSat](https://www.highspeedsat.com/iridium-satellite.php)), versus the conservative per-satellite product 66 x ~1,100 = ~72,600 [DERIVED]; the spread reflects channelization-versus-operational accounting, and Section 5.2 carries both ends honestly.

**(b) The theoretical channelized ceiling (the generous number).** Across the full 10.5 MHz at ~1.2 bps/Hz gross, a single-beam-equivalent is ~12.6 Mbps; reused across the 48 beams at a realistic ~7-color frequency-reuse pattern (~7x), the per-satellite theoretical channel sum is:

```
Per-satellite raw channelized  ~=  10.5 MHz  x  1.2 bps/Hz  x  ~7 (reuse)  =  ~86 Mbps
Fleet raw channelized          ~=  66  x  86 Mbps                          =  ~5.7 Gbps
```
[DERIVED, ESTIMATE on the reuse factor]

Both anchors say the same thing: **the current 66-satellite fleet moves on the order of a few hundred Mbps of user voice payload, and at most a few Gbps of raw channelized capacity, across the ENTIRE globe.** That is the honest measure of how capacity-small a 1990s 48-beam narrowband architecture is. For scale, a single modern satellite on the same band could match the whole fleet's raw capacity (Section 3), and a single terrestrial 5G cell on ~100 MHz outruns the entire Iridium fleet's user payload. The rare asset is the SPECTRUM and the global coordination, not the throughput the current hardware extracts from it. [DERIVED]

### 1.5 How full today: device-full, bit-empty

Iridium serves **2,537,000 billable subscribers (YE2025)**, of which **1,998,000 are commercial IoT** (Short Burst Data devices), 402,000 voice/data, 16,100 broadband, and 121,000 government ([`iridium_acquisition.md`](iridium_acquisition.md) COMM-617) [FACT]. The IoT line is the volume engine at **$7.78/mo ARPU** (COMM-618), and SBD messages are **~340 bytes maximum, delivered in ~5-20 s** (COMM-620) [FACT].

The reconciliation of "2.5M subscribers" with "~2.6 Mbps/satellite" is the duty cycle: **an SBD IoT device is idle almost all the time**, sending a tiny burst occasionally. A device sending ten 340-byte messages a day averages ~0.3 bits per second (Section 5). So 2M IoT devices spread across 66 satellites and their many passes represent a trickle of aggregate bits, well within the ~2.6 Mbps voice-grade payload per satellite even though the device COUNT is large. **The fleet is subscriber-full in device count and bit-empty in throughput**, which is precisely why the current architecture, capacity-small as it is, still serves millions: narrowband IoT asks almost nothing of the pipe (Section 5 quantifies the headroom). [FACT + DERIVED]

Quantified: even the AS-BUILT fleet's concurrent-circuit capacity (~72,600-172,000 circuits constellation-wide, Section 1.4) at the industry ~1-3% busy-hour concurrency (corpus COMM-543) supports roughly **~2.4M-17M voice-class subscribers on today's hardware** (Section 5.2), so the 2.537M base sits at the very bottom of even the OLD fleet's narrowband holding capacity. The fleet is not full in any capacity sense; it is full only in the sense that its architecture cannot offer more than narrowband. [DERIVED]

---

## 2. The replacement window: when the fleet needs replacing anyway (the Neutron hook)

The natural hook for a Neutron-launched fleet is that Iridium NEXT will need replacement regardless, and the timing is now on the public record.

### 2.1 Launch and design life

- **Iridium NEXT launched across 8 SpaceX Falcon 9 missions, January 2017 to January 2019** (75 satellites; 81 built including spares; 5 additional spares launched 2023), a ~$3B program ([`iridium_acquisition.md`](iridium_acquisition.md) COMM-610) [FACT].
- **Original design life: 12.5 years** from prime contractor Thales Alenia Space [FACT] ([SpaceNews, "Iridium adds five years to constellation lifetime estimate"](https://spacenews.com/iridium-adds-five-years-to-constellation-lifetime-estimate/); [SDxCentral, "Iridium extends satellite lifespans by five years"](https://www.sdxcentral.com/news/iridium-extends-satellite-lifespans-by-five-years/); [DatacenterDynamics](https://www.datacenterdynamics.com/en/news/iridium-extends-satellite-lifespans-by-five-years/)).

### 2.2 The 2024 life extension: to ~2035 at least

On its **February 15, 2024 earnings call**, Iridium announced an engineering reassessment that **extended the estimated satellite life from 12.5 years to ~17.5 years**, so the constellation is now expected to **perform well to at least 2035** [FACT] ([SpaceNews](https://spacenews.com/iridium-adds-five-years-to-constellation-lifetime-estimate/); [SDxCentral](https://www.sdxcentral.com/news/iridium-extends-satellite-lifespans-by-five-years/); [DatacenterDynamics](https://www.datacenterdynamics.com/en/news/iridium-extends-satellite-lifespans-by-five-years/)). The precedent supports the optimism: the first-generation (1990s) Iridium satellites, of similar design life, **lasted more than 20 years in LEO before running out of fuel** [FACT] ([SpaceNews](https://spacenews.com/iridium-adds-five-years-to-constellation-lifetime-estimate/)).

### 2.3 What Iridium has said about the next generation

CEO Matt Desch framed the extended life as buying OPTIONALITY on the timing of a third generation:

> the extended lifetime "gives us an opportunity to take advantage of the latest and greatest at the most favorable moment" before ordering a third-generation constellation. [FACT-SS on the verbatim quote] ([SpaceNews](https://spacenews.com/iridium-adds-five-years-to-constellation-lifetime-estimate/))

So as of the deal, Iridium had NO committed next-generation build and NO fixed replacement date, only a "decide when it is most favorable, need it by ~2035" posture. The Rocket Lab deal materials explicitly cite developing Iridium's **next-generation constellation** as a rationale ([`iridium_acquisition.md`](iridium_acquisition.md) COMM-607) [FACT]. **The window is therefore: replacement not forced before ~2035, decision timing open, next-gen design not yet chosen.** That is the clean hook for a Neutron-launched modern fleet: the replacement is coming, the architecture is a blank sheet, and Rocket Lab now owns both the launch vehicle and the spectrum. [FACT + framing]

### 2.4 The replacement-satellite regulatory posture is already friendly (bridges to Section 4)

Iridium NEXT itself was licensed as a **replacement** for the Block 1 fleet, "authorized to be operated at the same orbit location, in the same frequency bands, and with the same coverage area" under FCC rule **25.165(e)**, and the filing notes Iridium was "not required to post a bond ... for the Iridium NEXT second generation satellite system" because it used "the same orbital parameters ... using the same frequency bands as the current Block 1 Iridium satellite constellation" [FACT] ([FCC Engineering Statement, Section B](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf)). This is the license-modification precedent: a same-band, same-coverage generational replacement is a well-trodden FCC path (Section 4 handles what changes for a much LARGER or DIFFERENT-ALTITUDE fleet). [FACT]

---

## 3. The modernization physics: the same 8-10.5 MHz on a modern digital-beamforming satellite

This is the core question. Hold the spectrum fixed (Iridium's ~8 MHz exclusive, up to ~10.5 MHz total) and swap the 1990s 48-beam design for a MODERN large-aperture digital-beamforming satellite. How does capacity scale?

### 3.1 The identity, and why beam count is the only lever at a fixed narrow band

From the corpus supply identity ([`dtc_capacity_supply.md`](../direct_communication/dtc_capacity_supply.md) COMM-406):

```
Per-satellite aggregate  =  MHz_held  x  spectral_efficiency  x  N_reuse
                            (bounded by owned spectrum, not the processor, at this thin a band)

  N_reuse = number of non-overlapping co-channel beams that tile the footprint
          = footprint_area / beam_area   (set by aperture and altitude, NOT satellite count)
```

At L-band the term you CANNOT grow is `MHz_held`: the band is only ~8-10.5 MHz and it is rare and globally coordinated (that is the whole reason Iridium is valuable). So the modernization levers are the other two:
1. **N_reuse (dominant):** MORE, SMALLER beams reusing the same 8 MHz many more times. A modern digital-beamforming array forms hundreds-to-thousands of beams versus Iridium's 48, and a lower orbit shrinks each beam's footprint, adding still more reuse slots per unit ground area.
2. **spectral_efficiency:** a modern adaptive-coding-and-modulation (ACM) waveform to a better terminal reaches ~2-3 bps/Hz versus Iridium's ~1.2 bps/Hz gross DEQPSK.

Because the band is fixed, **capacity scales with BEAM COUNT x SPECTRAL EFFICIENCY, and beam count is the big multiplier.** This is the corpus's spectrum-bound finding (COMM-411) applied to L-band: on 8-10.5 MHz the system is firmly spectrum-limited (far below the ~50-100 MHz power knee of COMM-509), so the way to extract more from the fixed band is to reuse it more times spatially. [FACT + DERIVED]

### 3.2 Beam count and reuse: modern DBF versus Iridium NEXT

*(The beam-count anchors are the corpus's own, cross-referenced below; the beam count of a purpose-built modern L-band MSS array is a named gap, Section 7.)*

The modern digital-beamforming benchmarks the corpus already owns:
- **AST SpaceMobile Block 2: ~2,000-2,500 beams on a ~223 m^2 array** ([`dtc_capacity_supply.md`](../direct_communication/dtc_capacity_supply.md) COMM-408, arXiv 2506.18672) [FACT].
- **Starlink V2-mini Direct-to-Cell: 48 independently-steerable beams on a ~25 m^2-class array** ([`dtc_capacity_supply.md`](../direct_communication/dtc_capacity_supply.md) COMM-408) [FACT].
- **A flat ~25 m^2 entrant array: ~200-450 beams** (the corpus's scaled central figure, UNKNOWN-grade, COMM-408) [DERIVED].

Against Iridium NEXT's **48 fixed beams**, a modern flat ~25 m^2-class array at ~200-450 beams is a **~4x-9x increase in beam count** at similar aperture class, and an AST-scale ~223 m^2 array at ~2,000-2,500 beams is a **~40x-50x increase**. Each extra non-overlapping beam reuses the same 8 MHz again, so aggregate capacity rises roughly in proportion to beam count (until the reuse becomes interference-limited, the saturation ceiling of COMM-414). The lower orbit (~400-600 km versus Iridium's 780 km) shrinks the beam footprint further, adding reuse slots per unit ground area at the cost of needing more satellites for continuous coverage (Section 4 / the coverage docs). [FACT + DERIVED]

### 3.3 Per-satellite aggregate on 8 MHz: ~1.6-4.8 Gbps (central ~2.9)

The honest way to get the modern per-satellite number is to SCALE the corpus's spectrum-bound 25 MHz result down to 8 MHz, since the system is spectrum-bound and therefore linear in held MHz (COMM-411). The corpus pins a flat ~25 m^2 modern array at **~5-15 Gbps on 25 MHz (central ~8-10)** ([`dtc_capacity_supply.md`](../direct_communication/dtc_capacity_supply.md) COMM-410):

```
Modern per-satellite on 8 MHz  =  (8 / 25)  x  (corpus 25 MHz result)
                               =  0.32  x  [5 to 15 Gbps]   =  ~1.6 to ~4.8 Gbps   (central ~2.9)
```
[DERIVED, scaled from COMM-410]

The per-BEAM view of the same number: **8 MHz x ~0.5-3 bps/Hz = ~4-24 Mbps per co-channel beam** (~16-24 Mbps at the modern ~2-3 bps/Hz ACM point; Iridium's ~1.2 bps/Hz DEQPSK would give ~9.6 Mbps), and the per-satellite aggregate is per-beam capacity x the number of simultaneously-lit non-overlapping co-channel beams. The ~2.9 Gbps central figure implies ~120-180 effective co-channel reuses of the 8 MHz, consistent with the corpus's reuse accounting on the 25 MHz case (COMM-411/424). [DERIVED]

At the full 10.5 MHz the central figure is ~3.8 Gbps. The load-bearing comparison against the as-built fleet:

| Metric | Iridium NEXT (as built) | Modern DBF on same ~8 MHz | Multiple |
|---|---|---|---|
| Beams per satellite | 48 (fixed) | ~200-450 (flat class) to ~2,500 (AST class) | ~4x-50x |
| Per-satellite user capacity | ~2.6 Mbps (voice payload) | ~1.6-4.8 Gbps (central ~2.9) | **~1,100x** |
| Per-satellite theoretical raw | ~86 Mbps (channelized, 48-beam reuse) | ~1.6-4.8 Gbps | **~33x** |
| Spectral efficiency | ~1.2 bps/Hz (DEQPSK) | ~2-3 bps/Hz (ACM) | ~2x |

[DERIVED; per-satellite modern figure scaled from COMM-410, Iridium figures from Section 1.4]

**So modernization on the SAME spectrum buys roughly THREE orders of magnitude in per-satellite aggregate** (~1,100x versus the voice payload, ~33x versus the generous theoretical raw), overwhelmingly from beam count (spatial reuse), secondarily from spectral efficiency. This is the founder's max-outcome headline: the rare L-band asset is being used by the current fleet at a small fraction of its potential, and modern hardware unlocks the rest without needing one extra MHz. [DERIVED]

### 3.4 Fleet aggregate at 340 / 1,000 / 2,000 satellites

Multiplying the central ~2.9 Gbps/sat (8 MHz) by the fleet sizes the founder specified:

| Fleet size | Aggregate on 8 MHz (central ~2.9 Gbps/sat) | Note |
|---|---|---|
| 340 satellites | **~1.0 Tbps** | ~coverage-floor fleet (corpus COMM-215/224) |
| 1,000 satellites | **~2.9 Tbps** | |
| 2,000 satellites | **~5.8 Tbps** | capacity-driven |

[DERIVED, central figure; the ~1.6-4.8 Gbps/sat range scales these by roughly 0.55x-1.65x]

For scale: the CURRENT 66-satellite fleet moves ~0.17 Gbps of voice payload (~5.7 Gbps raw). A 340-satellite modern fleet on the same band is **~170x-6,000x the current fleet's throughput**, depending on which anchor you compare. The spectrum did not change; the architecture did. [DERIVED]

### 3.5 THE MODEL RULE, checked: video-grade subscribers linear in held MHz

The founder's rule to test:

> "video-grade subscribers per satellite scale linearly with held MHz: 75,000 attached at 25 MHz implies ~24,000 attached at 8 MHz (roughly 3,000 subscribers per satellite per MHz) at ~2.5 Mbps active rate and 2-3% concurrency."

**Checked and CONFIRMED, exactly.** The corpus pins ~50,000-100,000 attached video-grade subscribers per flat ~25 m^2 satellite at 25 MHz (central ~75,000), at ~2.5 Mbps active sessions and ~1-3% busy-hour concurrency ([`dtc_subscribers_per_satellite.md`](../direct_communication/dtc_subscribers_per_satellite.md) COMM-545). Scaling linearly with held MHz:

```
Subscribers per satellite per MHz  =  75,000 / 25 MHz  =  3,000 subs/sat/MHz
At 8 MHz                           =  3,000  x  8       =  24,000 attached per satellite
```
[DERIVED, matches the rule to the digit]

Fleet video-grade subscribers at 8 MHz:

| Fleet size | Video-grade subscribers at 8 MHz (24,000/sat) |
|---|---|
| 340 satellites | **~8.2 million** |
| 1,000 satellites | **~24 million** |
| 2,000 satellites | **~48 million** |

[DERIVED]

**Why the rule HOLDS:** the linearity is a direct consequence of the system being SPECTRUM-BOUND at L-band (COMM-411). Per-satellite aggregate = MHz x SE x reuse; holding SE and reuse (aperture, beams, orbit) fixed, aggregate is linear in MHz, and since subscribers = aggregate / per-subscriber-demand, subscribers are linear in MHz too. At 8-10.5 MHz the system is far below the ~50-100 MHz power knee, so bandwidth (not power) is the binding term, exactly the regime where "linear in held MHz" is valid ([`dtc_data_rate_vs_spectrum.md`](../direct_communication/dtc_data_rate_vs_spectrum.md) COMM-509). [DERIVED]

**Where the rule BREAKS (stated honestly):**
1. **If reuse or power cannot hold the assumed spectral efficiency.** The 3,000-subs/sat/MHz constant assumes ~2.5 Mbps active sessions at the corpus's ~2-3 bps/Hz and the assumed reuse fraction. A modern L-band array on 8 MHz should hold this (it is spectrum-bound, with power headroom at narrow bandwidth), but if the aperture, beam isolation, or power budget fall short, per-satellite subscribers fall with them. The beam count and reuse fraction are the corpus's UNKNOWN-grade soft inputs (COMM-408/424). [UNKNOWN, inherited]
2. **The density caveat (the binding real-world limiter).** The per-satellite and fleet subscriber counts assume subscribers are SPREAD across the coverage footprint. A satellite beam is a fixed pool over a fixed footprint that cannot densify; subscribers piled into a few dense cells (a city) cannot be served by adding satellites (the spectrum-saturation ceiling, COMM-414/553). The MSS use case (remote, maritime, aviation, rural, spread) fits the spread assumption; dense urban demand does not. [DERIVED, ties to corpus]
3. **The lane caveat (kept straight).** These are MSS-terminal, MSS-band subscribers (Iridium-type terminals on L-band), NOT unmodified cellular phones. The video-grade rate is achievable to a PURPOSE-BUILT terminal on the owned band; it is NOT a claim that an ordinary smartphone gets 2.5 Mbps from Iridium's L-band (COMM-613). If the target is broadband to a real terminal (Certus-successor class), the rule applies; if the target is direct-to-unmodified-phone, that is the separate cellular-lane question the corpus keeps distinct. [FACT, lane distinction]

### 3.6 Modern software-defined payloads: the enabling technology

The reason a modern satellite on the same band vastly outperforms Iridium NEXT is the shift from a FIXED-beam analog payload to a DIGITALLY-BEAMFORMED, software-defined one: dynamic beam placement, flexible power and spectrum allocation, and capacity steering to where the demand is. The corpus owns the flying anchor: the AST5000 ASIC forms ">2,000 coverage cells, up to 2,500 beams," explicitly trading beam count against power (COMM-538/540) [FACT], against Iridium NEXT's fixed 48-beam, 120-element 1990s array (Section 1.2). A dedicated multi-source survey of modern software-defined MSS payloads (beam counts on Inmarsat-6/ELERA-class L-band, Ligado SkyTerra-class large reflectors, and the commercial software-defined platform generation) did not complete in this pass and is a named follow-up (Section 7); the beam-count case here rests on the corpus's digital-beamforming anchors, which are the same DBF hardware physics regardless of band (COMM-408/538/540). [UNKNOWN on the MSS-specific survey, named]

The practical implication: a modern replacement fleet is not just "more beams," it is beams that can be CONCENTRATED where subscribers are (maritime lanes, flight corridors, remote regions), which raises the EFFECTIVE served-subscriber count above a fixed-grid design at the same aggregate, and softens (though does not remove) the density caveat. [FACT + DERIVED]

---

## 4. Regulatory constraints on a much larger, modernized fleet

Can Iridium's licenses support a totally different, much larger fleet on the same band? The answer splits into what is SETTLED (same-band replacement precedent) and what is OPEN (a larger fleet, a different orbit, the Globalstar boundary, PFD).

### 4.1 Settled: same-band, same-coverage generational replacement

Iridium NEXT replaced the Block 1 fleet under the IDENTICAL spectrum authorization (FCC Call Sign S2110, Big LEO MSS license) via a **modification of the existing license**, qualifying as a "replacement satellite" under **FCC rule 25.165(e)** ("same orbit location ... same frequency bands ... same coverage area," brought into use "at approximately the same time as, but no later than, the existing satellite is retired"), which is why no replacement bond was required [FACT] ([FCC Engineering Statement, Section B](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf)). So a **like-for-like generational replacement on the same L-band is a well-established, low-friction FCC path.** Rocket Lab inherits this license via the FCC transfer-of-control that is a closing condition of the deal ([`iridium_acquisition.md`](iridium_acquisition.md) COMM-606). [FACT]

### 4.2 The Big LEO band plan and the Globalstar sharing boundary

The 2007 FCC Big LEO band plan fixed the L-band MSS shares [FACT] ([Federal Register, "Review of the Spectrum Sharing Plan ... 1.6/2.4 GHz Bands," 2007](https://www.federalregister.gov/documents/2007/12/13/E7-24104/review-of-the-spectrum-sharing-plan-among-non-geostationary-satellite-orbit-mobile-satellite-service); [FCC DA-26-398](https://docs.fcc.gov/public/attachments/DA-26-398A1.pdf)):
- **Globalstar exclusive: 1610-1617.775 MHz (7.775 MHz)**, CDMA.
- **Iridium exclusive: 1618.725-1626.5 MHz (7.775 MHz)**, TDMA.
- **Shared: 1617.775-1618.725 MHz (0.95 MHz)** between the two.

This matches the corpus (COMM-611: 7.775 MHz exclusive, 0.95 MHz shared). The **modern Iridium NEXT satellites can physically operate across the full 1616-1626.5 MHz**, but Iridium's AUTHORIZATION is limited to its exclusive 1618.725-1626.5 MHz plus the shared sliver [FACT] ([Communications Daily, "Fight Seen Brewing Over 1.6 GHz as Iridium Petitions FCC for Greater Access," Dec 2025](https://communicationsdaily.com/news/2025/12/30/fight-seen-brewing-over-16-ghz-as-iridium-petitions-fcc-for-greater-access-2512290021); [Broadband Breakfast, "Globalstar Opposed to Other Satellite Operators in 1.6 GHz"](https://broadbandbreakfast.com/globalstar-opposed-to-other-satellite-operators-in-1-6-ghz/)).

### 4.3 Open: the active 2025-2026 spectrum-access dispute

As of late 2025, **Iridium has petitioned the FCC for greater access to the 1.6 GHz band** (to operate in 1616-1618.725 MHz, and to share an additional ~6 MHz at 1610-1616 MHz with Globalstar's system), and **Globalstar opposes**, arguing co-frequency operation would cause harmful interference and that the existing framework has worked [FACT] ([Communications Daily, Dec 2025](https://communicationsdaily.com/news/2025/12/30/fight-seen-brewing-over-16-ghz-as-iridium-petitions-fcc-for-greater-access-2512290021); [Fierce Network, "Globalstar not interested in Iridium's latest spectrum sharing proposal"](https://www.fierce-network.com/tech/globalstar-not-interested-iridium-s-latest-spectrum-sharing-proposal); [Broadband Breakfast](https://broadbandbreakfast.com/globalstar-opposed-to-other-satellite-operators-in-1-6-ghz/)). So whether the modernized fleet gets to use ~8 MHz (exclusive today) or something closer to the full ~10.5 MHz (or more) is an OPEN regulatory question that predates the Rocket Lab deal and is being actively litigated at the FCC. This matters directly to the max-outcome model: the subscriber count is linear in held MHz (Section 3.5), so the exclusive-8 versus full-10.5 versus expanded question moves the answer proportionally. [FACT on the dispute; UNKNOWN on the outcome]

### 4.4 Open: a much larger fleet, a different altitude, and PFD

Three things change if the replacement is not like-for-like but a MUCH larger fleet at a DIFFERENT orbit:
1. **Power-flux-density (PFD) limits.** MSS downlinks in this band are subject to PFD limits to protect co-frequency services (the FCC filing devotes a section, "K. PFD REQUIREMENTS," 25.114(d)(5)/(c)(8), to demonstrating compliance) [FACT] ([FCC Engineering Statement, Section K](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf)). A larger fleet with many more, higher-power beams would have to re-demonstrate PFD compliance, and aggregate PFD from many overlapping satellites is a harder case than a 66-satellite fleet. [FACT + UNKNOWN on whether a large fleet clears it]
2. **A different altitude requires fresh coordination.** The replacement-satellite rule 25.165(e) protection is for the SAME orbit and coverage. A VLEO orbit at ~400-600 km (versus 780 km) is a different altitude, changing the footprint, the coverage geometry, and the interference environment, which would require new ITU filings and FCC coordination rather than a clean 25.165(e) replacement. [DERIVED from the rule text; UNKNOWN on the process burden]
3. **Number of satellites.** The current authorization is for 66 + 15 spares (81). A fleet of hundreds-to-thousands is a materially different NGSO authorization (a new/modified license, orbital-debris and collision-risk showings, larger constellation review), not a same-count replacement. [DERIVED; UNKNOWN]

**Net regulatory read:** a same-band, same-orbit, similar-count modern replacement is a well-established path (Section 4.1). A much LARGER fleet, or a DIFFERENT altitude, or more MHz than the exclusive 8, each opens a real regulatory question (PFD, coordination, constellation authorization, the Globalstar boundary), none of which is settled and several of which are being actively contested at the FCC as of 2026. The spectrum is owned and globally coordinated (the hard part), but "own the band" does not automatically mean "fly any fleet you like on it." [FACT + UNKNOWN, honest]

---

## 5. Narrowband headroom: capacity is not the constraint

For Iridium's ACTUAL service rates (SBD messaging, low-bit-rate voice, NB-IoT, Certus), how many devices could a modernized fleet on 8-10.5 MHz support? The expected answer is that capacity is effectively NOT the constraint for narrowband at tens of millions of devices. Confirmed, with arithmetic.

### 5.1 The per-device average bit rate is tiny

Iridium's narrowband services and their rates:
- **SBD (Short Burst Data): ~340-byte maximum messages** (COMM-620) [FACT].
- **Voice: 2.4 kbps AMBE** (Section 1.3) [FACT].
- **NB-IoT NTN (Project Stardust): kbps-class narrowband messaging/SOS** ([`iridium_acquisition.md`](iridium_acquisition.md) COMM-614) [FACT].

A low-duty-cycle IoT device sends occasional tiny bursts. The average bit rate per device:

```
Device sending N messages/day of 340 bytes  =  340 x 8 x N  bits/day  =  (2,720 x N) / 86,400  bits/s
```

| Messages/day/device | Average bits/s per device |
|---|---|
| 1 | ~0.031 bps |
| 10 | ~0.315 bps |
| 48 (one every 30 min) | ~1.51 bps |

[DERIVED]

The per-CHANNEL view says the same thing: **one 2.4 kbps Iridium channel moves ~26 MB/day if run continuously** (2.4 kbps x 86,400 s), while a 4-message/day SBD device needs only **~14 KB/day including protocol overhead**, so ONE narrowband channel time-shares across **~1,900 such devices**. This is the mechanism by which 2M IoT devices already fit in a ~2.6 Mbps/satellite fleet. [DERIVED, arithmetic on cited rates]

### 5.2 Devices per modern satellite and per fleet: today's fleet holds millions, a modern one holds billions

**Today's fleet already holds millions.** The AS-BUILT fleet's concurrent-circuit capacity is ~72,600 (66 x ~1,100, the per-satellite product) up to the sourced ~172,000 concurrent calls constellation-wide (Section 1.4) [FACT anchors]. At the industry ~1-3% busy-hour concurrency (corpus COMM-543), that backs out to roughly **~2.4M-7.3M (conservative product) up to ~5.7M-17M (constellation-wide figure) voice-class subscribers ON TODAY'S HARDWARE** [DERIVED]. Today's 2.537M billable subscribers (2.0M of them trickle-rate IoT) are therefore nowhere near even the old fleet's narrowband wall, which is the cleanest possible statement of "how full is it": not full at all, in capacity terms.

**A modern fleet holds billions.** Take the modern per-satellite aggregate on 8 MHz (~2.9 Gbps central, Section 3.3) and a conservative ~20% MAC/protocol efficiency for bursty narrowband traffic (random-access overhead, guard, retransmission):

```
Narrowband devices per satellite  =  (2.9 Gbps  x  0.20)  /  (avg bits/s per device)
```

| Messages/day/device | Devices per satellite | Fleet of 340 |
|---|---|---|
| 1 | ~18,000 million (~18B) | ~6,200 billion |
| 10 | ~1,800 million (~1.8B) | ~620 billion |
| 48 | ~380 million | ~130 billion |

[DERIVED, ESTIMATE on the 20% efficiency]

Even at the AGGRESSIVE end (48 messages/device/day, 20% efficiency, a single satellite), one modern satellite holds **~380 million narrowband devices**, and a 340-satellite fleet holds **~130 billion**. At the realistic SBD IoT duty cycle (a few messages/day), the numbers are in the trillions. **Narrowband capacity is not remotely the binding constraint at tens of millions of devices; it is not the constraint at billions.** [DERIVED]

### 5.3 The honest caveats on the narrowband number

This is a CAPACITY-ceiling statement, not a system-design statement. The real narrowband limits are elsewhere:
1. **Random-access contention, not raw bits.** At extreme device densities the binding limit becomes the random-access channel (collisions when many idle devices wake at once), signaling overhead, and scheduling, not the aggregate bit ceiling. NB-IoT NTN analysis puts contention capacity at **~57 to ~1,650 devices per random-access window depending on the access mode** (a per-opportunity contention figure, NOT a population cap; idle attached devices do not consume access windows), and 3GPP Release 19 adds subcarrier multiplexing to raise access capacity [FACT-SS] ([arXiv 2406.14107, NB-IoT NTN random access](https://arxiv.org/abs/2406.14107)). The ~20% efficiency haircut gestures at this, but a true massive-IoT design has its own per-beam access dimensioning that this doc does not model. [ESTIMATE; UNKNOWN on the access-limited ceiling]
2. **Coverage and revisit, not capacity.** For messaging, the constraint is that a satellite is overhead when the device wants to send (revisit time), which is a COVERAGE/constellation-geometry question (the coverage docs), not a capacity question. Iridium's cross-linked global mesh already solves this; a VLEO replacement would need enough satellites for continuous coverage. [DERIVED]
3. **The business, the terminals, the spectrum lane.** Whether tens of millions of narrowband devices is a good BUSINESS (ARPU, terminal cost, competition from terrestrial NB-IoT and other NTN players), and whether any of this reaches ordinary phones (it does not, on Iridium's L-band, COMM-613), are separate questions this doc does not touch. [FACT, lane; out of scope for verdict]

**Net:** for narrowband IoT and messaging, the modernized fleet's spectrum is effectively unlimited relative to any plausible subscriber base; the constraints are access design, coverage, terminals, and business, not capacity. The founder's expected answer is confirmed. [DERIVED]

---

## 6. So what (for the Iridium max-outcome model)

1. **The current fleet is capacity-small by design:** 66 satellites, 48 fixed beams each, 252 narrowband DEQPSK carriers, ~2.6 Mbps voice payload per satellite, ~174 Mbps fleet voice payload (~5.7 Gbps raw). It serves 2.5M subscribers only because 2M are trickle-rate IoT. The rare asset is the SPECTRUM and its global coordination, not the throughput the 1990s hardware extracts. [DERIVED]
2. **The replacement window is ~2035, decision-timing open, next-gen design a blank sheet.** Launched 2017-2019, 12.5-year design life extended to ~17.5 years in 2024, "perform well to at least 2035," Desch framing a third generation as a "most favorable moment" decision. The clean Neutron hook. [FACT]
3. **Modernization on the same 8 MHz buys ~three orders of magnitude per satellite:** ~1.6-4.8 Gbps/sat (central ~2.9) versus ~2.6 Mbps voice payload today, overwhelmingly from beam count (spatial reuse), secondarily from spectral efficiency. Fleet aggregate ~1.0 Tbps (340), ~2.9 Tbps (1,000), ~5.8 Tbps (2,000). [DERIVED]
4. **The model rule holds exactly:** video-grade subscribers are linear in held MHz, ~3,000 subs/sat/MHz -> ~24,000/sat at 8 MHz -> ~8M (340), ~24M (1,000), ~48M (2,000) subscribers, a US-scale range. It holds because L-band is spectrum-bound; it breaks on a power/reuse shortfall, on dense-cell pile-up (the density caveat), and it is an MSS-terminal number, not an unmodified-phone number. [DERIVED, checked]
5. **Regulatory: same-band replacement is settled, a larger/different fleet is open.** Iridium NEXT replaced Block 1 under the same license (25.165(e)); a much larger fleet, a VLEO altitude, more than the exclusive 8 MHz, and PFD compliance each open a real, currently-contested question (the Globalstar 1.6 GHz dispute is live at the FCC as of 2026). [FACT + UNKNOWN]
6. **Narrowband capacity is not the constraint:** even the as-built fleet backs out to ~2.4M-17M voice-class subscribers at industry busy-hour concurrency (today's 2.537M is nowhere near the wall), and a modern 8 MHz fleet holds billions of low-duty-cycle devices; the real narrowband limits are random-access design (~57-1,650 devices per access window by mode), coverage/revisit, terminals, and business, none assessed here. [DERIVED + FACT-SS]
7. **No verdict.** This doc supplies the capacity physics (how small the current fleet is, when it needs replacing, how much a modern fleet on the same band would carry, the regulatory frame, the narrowband headroom). Whether Rocket Lab should build such a fleet, at what cost, into what market, on which spectrum lane, is not assessed. [DERIVED]

---

## 7. Open questions / named gaps

1. **The modern L-band beam count is the load-bearing soft input.** The ~200-450 (flat class) to ~2,500 (AST class) beam range, inherited from the corpus (COMM-408, UNKNOWN-grade), drives the whole per-satellite aggregate and subscriber count. A firmer beam count for a purpose-built modern L-band MSS array would tighten the ~1.6-4.8 Gbps/sat band. The wave-9 multi-source survey of modern MSS software-defined payloads (Inmarsat-6/ELERA beam counts, Ligado SkyTerra-class reflectors) did not complete; re-run it as the follow-up that firms this input. [UNKNOWN, inherited; survey follow-up named]
2. **The reuse fraction and spectral efficiency at L-band to a modern terminal are estimates.** The linear-in-MHz scaling and the 3,000-subs/sat/MHz constant assume the modern array holds ~2-3 bps/Hz at the assumed reuse; the realized figures for an L-band MSS array at ~400-600 km are not pinned. [ESTIMATE]
3. **The held-MHz question is regulatorily live.** Exclusive ~8 MHz today, up to ~10.5 MHz physically, more contested; the Globalstar dispute outcome moves the subscriber count proportionally. [UNKNOWN, active FCC proceeding]
4. **Whether a much larger fleet clears PFD and coordination at a new altitude is unresolved.** The same-count/same-orbit path is clean; the large-fleet/VLEO path is not, and the aggregate-PFD and constellation-authorization burden is unquantified here. [UNKNOWN]
5. **The narrowband access-limited ceiling is not modeled.** The billions-of-devices figure is a raw-bit ceiling; the true massive-IoT limit (random-access contention per beam) is lower and unquantified. [ESTIMATE; UNKNOWN]
6. **The density caveat is the binding real-world limiter on the video-grade fleet.** The subscriber counts assume spread subscribers; the geographic spread of a target MSS subscriber base is unset (a founder assumption per the corpus rule). [UNKNOWN, founder assumption]
7. **The lane is kept straight but the target service is a founder choice.** The video-grade numbers are to purpose-built MSS terminals; whether the max-outcome target is broadband-to-terminal (Certus-successor), narrowband-to-device (NB-IoT), or something reaching phones (the separate cellular lane) determines which of these numbers is the relevant one. [FACT, lane; founder choice on target]

---

## 8. Sources

Iridium NEXT as-built (primary + technical):
- [Iridium NEXT FCC Engineering Statement, SAT-MOD-20131227-00148 (primary): 66 SVs / 780 km / 86.4 deg, 48 MSS L-band beams TDD, 252 carriers at 41.667 kHz / 35-36 kHz necessary / up to 288 kHz combined / 8-carrier subbands, 2 feeder + 4 ISL Ka beams, replacement under 25.165(e), PFD section, insertion 625 km / storage 700-750 km](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf)
- [eoPortal Iridium NEXT: 48-beam L-band phased array, ~80 voice circuits per beam, ~860 kg, 10-yr design / 15-yr mission life, four 23 GHz crosslinks (2 steerable/2 fixed), two 20/30 GHz feeder links, Certus up to 704 kbit/s](https://www.eoportal.org/satellite-missions/iridium-next)
- [Wikipedia Iridium satellite constellation: 48 spot beams (16 x 3 sectors), 240 main + 12 messaging = 252 channels at 41.667 kHz, 31.5 kHz occupied, DEQPSK, 2.4 kbps AMBE, crosslinks 10 Mbit/s, ~1,100 calls per satellite, ~172,000 concurrent calls constellation-wide](https://en.wikipedia.org/wiki/Iridium_satellite_constellation)
- [SigidWiki Iridium: DEQPSK 2 bits/symbol, 31.5 kHz occupied, 41.667 kHz spacing, 8.28 ms slot / 90 ms frame, 4 TDMA slots/carrier/direction, 50 kbps burst / 25000 baud, 9.2% duty, 2.4 kbps AMBE vocoder](https://www.sigidwiki.com/wiki/Iridium)
- [MathWorks Iridium spot-beam coverage: 120-element (12x10) L-band URA, 48-beam pattern, any of 252 carriers assignable to any of 48 beams](https://www.mathworks.com/help/phased/ug/iridium-satellite-spot-beam-coverage-on-map-of-us.html)
- [HighSpeedSat Iridium: ~1,100 concurrent calls per satellite, 4,700 km footprint](https://www.highspeedsat.com/iridium-satellite.php)
- [Overview of IRIDIUM satellite network (ResearchGate): FDMA/TDMA hybrid, 90 ms TDD frame, 240 FDMA channels of 41.67 kHz](https://www.researchgate.net/publication/3622510_Overview_of_IRIDIUM_satellite_network)

Replacement window:
- [SpaceNews, "Iridium adds five years to constellation lifetime estimate": 12.5 -> 17.5 years, perform well to at least 2035, Feb 15 2024 call, first-gen lasted 20+ years, Desch "latest and greatest at the most favorable moment"](https://spacenews.com/iridium-adds-five-years-to-constellation-lifetime-estimate/)
- [SDxCentral, "Iridium extends satellite lifespans by five years": 80 sats launched 2017-2019, 12.5-yr Thales design life, +5 years](https://www.sdxcentral.com/news/iridium-extends-satellite-lifespans-by-five-years/)
- [DatacenterDynamics, "Iridium extends satellite lifespans by five years"](https://www.datacenterdynamics.com/en/news/iridium-extends-satellite-lifespans-by-five-years/)

Regulatory / Big LEO band plan / Globalstar dispute:
- [Federal Register, "Review of the Spectrum Sharing Plan Among NGSO MSS Systems in the 1.6/2.4 GHz Bands" (2007): the Big LEO band plan](https://www.federalregister.gov/documents/2007/12/13/E7-24104/review-of-the-spectrum-sharing-plan-among-non-geostationary-satellite-orbit-mobile-satellite-service)
- [FCC DA-26-398: 1.6 GHz MSS band shares (Globalstar 7.775 MHz exclusive, Iridium 7.775 MHz exclusive, 0.95 MHz shared at 1617.775-1618.725 MHz)](https://docs.fcc.gov/public/attachments/DA-26-398A1.pdf)
- [Communications Daily, "Fight Seen Brewing Over 1.6 GHz as Iridium Petitions FCC for Greater Access" (Dec 2025): Iridium seeks 1616-1618.725 MHz and to share 1610-1616 MHz](https://communicationsdaily.com/news/2025/12/30/fight-seen-brewing-over-16-ghz-as-iridium-petitions-fcc-for-greater-access-2512290021)
- [Broadband Breakfast, "Globalstar Opposed to Other Satellite Operators in 1.6 GHz"](https://broadbandbreakfast.com/globalstar-opposed-to-other-satellite-operators-in-1-6-ghz/)
- [Fierce Network, "Globalstar not interested in Iridium's latest spectrum sharing proposal"](https://www.fierce-network.com/tech/globalstar-not-interested-iridium-s-latest-spectrum-sharing-proposal)

Certus service rates:
- [Iridium Certus 700 (official): up to 704 kbit/s L-band broadband](https://www.iridium.com/services/iridium-certus-700)
- [Ground Control, "What is Iridium Certus": service classes 88 kbps to 704 kbps, eventual 1.4 Mbps](https://www.groundcontrol.com/blog/what-is-iridium-certus-and-what-speeds-are-available-infographic/)

Narrowband access capacity:
- [arXiv 2406.14107 (NB-IoT NTN random access): ~57 to ~1,650 devices per random-access window depending on access mode; 3GPP Release 19 subcarrier multiplexing raises access capacity](https://arxiv.org/abs/2406.14107)

*(The corpus capacity-physics anchors (COMM-408/410/411/414/424/543/545/550) are cross-referenced, not re-listed. A multi-source survey of modern software-defined MSS payload beam counts, e.g. Inmarsat-6/ELERA and Ligado SkyTerra-class, did not complete in this pass and is a named follow-up, Section 7.)*

---

## 9. Claims ledger (COMM-635..660)

For the catalog/reconciliation step. Each hard claim with sources and tag; single-source, estimate, and unknown claims flagged. IDs COMM-635 through COMM-660 (the reserved block; the current global max before this doc is COMM-634; not exceeded). Cross-references existing IDs heavily.

- **COMM-635**, Iridium NEXT: 66 satellites, 780 km, 86.4 deg, 6 planes x 11, each carrying a single 48-beam L-band phased-array main mission antenna used in TDD for forward/return service links, plus 2 Ka feeder beams and 4 Ka (~23 GHz) inter-satellite crosslinks running ~10 Mbit/s each. [FACT] Sources: [FCC Engineering Statement SAT-MOD-20131227-00148](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf); [eoPortal Iridium NEXT](https://www.eoportal.org/satellite-missions/iridium-next); [Wikipedia Iridium satellite constellation](https://en.wikipedia.org/wiki/Iridium_satellite_constellation); cross-ref COMM-608/610.
- **COMM-636**, The 48-beam L-band array is a 120-element (12x10) uniform rectangular array tiling a ~4,700 km footprint into ~600 km per-beam cells (16 beams x 3 sectors); it is a FIXED, hardware-defined cellular pattern, at the low end of the beam-count lever. [FACT] Sources: [MathWorks Iridium spot-beam example](https://www.mathworks.com/help/phased/ug/iridium-satellite-spot-beam-coverage-on-map-of-us.html); [Airport-Technology Iridium NEXT](https://www.airport-technology.com/projects/iridium-next-satellite-constellation/); [Wikipedia Iridium](https://en.wikipedia.org/wiki/Iridium_satellite_constellation); [eoPortal](https://www.eoportal.org/satellite-missions/iridium-next).
- **COMM-637**, Channelization: 252 carriers across 1616-1626.5 MHz (uplink and downlink), carrier spacing 41.667 kHz, necessary bandwidth 35-36 kHz (31.5 kHz occupied + 10.17 kHz guard), grouped into subbands of 8 (32nd has 4), combinable up to ~288 kHz for wider Certus channels; any carrier assignable to any of the 48 beams. [FACT] Sources: [FCC Engineering Statement Section G](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf); [SigidWiki Iridium](https://www.sigidwiki.com/wiki/Iridium); [Wikipedia Iridium](https://en.wikipedia.org/wiki/Iridium_satellite_constellation).
- **COMM-638**, Air interface: DEQPSK (2 bits/symbol), hybrid FDMA/TDMA, 90 ms TDD frame with 8.28 ms slots, 4 TDMA slots per FDMA carrier per direction, 50 kbps burst (25,000 baud), ~9.2% per-slot duty; voice via 2.4 kbps AMBE vocoder; gross channel efficiency ~1.2 bps/Hz. [FACT] Sources: [SigidWiki Iridium](https://www.sigidwiki.com/wiki/Iridium); [Wikipedia Iridium](https://en.wikipedia.org/wiki/Iridium_satellite_constellation); [ResearchGate Overview of IRIDIUM](https://www.researchgate.net/publication/3622510_Overview_of_IRIDIUM_satellite_network).
- **COMM-639**, Per-satellite user capacity is small: on the order of ~1,100 concurrent 2.4 kbps voice calls = ~2.64 Mbps voice payload per satellite, ~174 Mbps (~0.17 Gbps) across the 66-satellite fleet. [DERIVED; ~1,100 calls FACT-SS] Sources: [HighSpeedSat Iridium](https://www.highspeedsat.com/iridium-satellite.php); voice rate per COMM-638; cross-ref COMM-610.
- **COMM-640**, Per-satellite theoretical channelized ceiling ~86 Mbps (10.5 MHz x ~1.2 bps/Hz x ~7-color reuse across 48 beams), ~5.7 Gbps fleet-wide; this is the generous upper anchor, versus the ~2.6 Mbps voice-payload lower anchor. Both show a 1990s narrowband architecture uses its rare L-band at a small fraction of modern potential. [DERIVED; reuse factor ESTIMATE] Sources: this doc Section 1.4; efficiency per COMM-638.
- **COMM-641**, The current fleet is device-full and bit-empty: 2.537M billable subscribers (YE2025) of which 1.998M are low-duty-cycle IoT (SBD, ~340-byte messages); millions of idle-most-of-the-time devices fit within ~2.6 Mbps/sat because each averages a fraction of a bit per second. [FACT + DERIVED] Sources: cross-ref COMM-617/620; duty-cycle math per COMM-659; per-channel math per COMM-653.
- **COMM-642**, Iridium NEXT launched across 8 Falcon 9 missions Jan 2017-Jan 2019 (75 sats; 81 built; +5 spares 2023); original design life 12.5 years from Thales Alenia Space. [FACT] Sources: [SDxCentral](https://www.sdxcentral.com/news/iridium-extends-satellite-lifespans-by-five-years/); [SpaceNews](https://spacenews.com/iridium-adds-five-years-to-constellation-lifetime-estimate/); cross-ref COMM-610.
- **COMM-643**, A Feb 15, 2024 engineering reassessment extended the estimated satellite life from 12.5 to ~17.5 years; the constellation is now expected to perform well to at least 2035; the first-generation (1990s) satellites lasted more than 20 years before running out of fuel. [FACT] Sources: [SpaceNews](https://spacenews.com/iridium-adds-five-years-to-constellation-lifetime-estimate/); [SDxCentral](https://www.sdxcentral.com/news/iridium-extends-satellite-lifespans-by-five-years/); [DatacenterDynamics](https://www.datacenterdynamics.com/en/news/iridium-extends-satellite-lifespans-by-five-years/).
- **COMM-644**, As of the deal Iridium had no committed next-generation build and no fixed replacement date: CEO Desch framed a third-generation constellation as taking advantage of "the latest and greatest at the most favorable moment," need-by ~2035; the Rocket Lab deal cites developing the next-gen constellation as a rationale. The clean Neutron-launched-replacement hook. [FACT; quote FACT-SS] Sources: [SpaceNews](https://spacenews.com/iridium-adds-five-years-to-constellation-lifetime-estimate/); cross-ref COMM-607.
- **COMM-645**, At a fixed narrow band, per-satellite aggregate = MHz x spectral efficiency x N_reuse (non-overlapping co-channel beams), bounded by owned spectrum (not the processor) far below the ~50-100 MHz power knee; since MHz is fixed and rare at L-band, the modernization levers are MORE, SMALLER BEAMS (spatial reuse via bigger aperture + lower orbit) and higher spectral efficiency (ACM), with beam count the dominant multiplier. [FACT + DERIVED] Sources: cross-ref COMM-406/411/509; this doc Section 3.1.
- **COMM-646**, Beam-count contrast: Iridium NEXT 48 fixed beams versus modern digital-beamforming ~200-450 beams (flat ~25 m^2 class) to ~2,000-2,500 (AST ~223 m^2 class), a ~4x-50x increase at similar-to-larger aperture; each extra non-overlapping beam reuses the same 8 MHz again, so aggregate rises ~proportionally to beam count until interference-limited (the saturation ceiling). [FACT + DERIVED] Sources: cross-ref COMM-408/414; this doc Section 3.2.
- **COMM-647**, Modern per-satellite aggregate on 8 MHz ~= (8/25) x the corpus 25 MHz result (spectrum-bound, linear in held MHz) = ~1.6-4.8 Gbps/sat (central ~2.9); at 10.5 MHz central ~3.8 Gbps. This is ~1,100x the Iridium NEXT ~2.6 Mbps voice payload and ~33x its ~86 Mbps theoretical raw. [DERIVED] Sources: cross-ref COMM-410/411; this doc Section 3.3; Iridium figures COMM-639/640.
- **COMM-648**, Modern fleet aggregate on 8 MHz (central ~2.9 Gbps/sat): ~1.0 Tbps at 340 satellites, ~2.9 Tbps at 1,000, ~5.8 Tbps at 2,000 (the ~1.6-4.8 Gbps/sat range scales these ~0.55x-1.65x). This is ~170x-6,000x the current 66-satellite fleet's throughput on the same spectrum. [DERIVED] Sources: this doc Section 3.4; per-sat COMM-647.
- **COMM-649**, THE MODEL RULE CONFIRMED: video-grade subscribers scale linearly with held MHz; the corpus's ~75,000 attached at 25 MHz = 3,000 subs/sat/MHz -> ~24,000 attached/sat at 8 MHz (2.5 Mbps active, 2-3% concurrency), totaling ~8.2M (340 sats), ~24M (1,000), ~48M (2,000). Matches the founder's rule exactly. [DERIVED, checked] Sources: cross-ref COMM-545/543/550; this doc Section 3.5.
- **COMM-650**, The rule HOLDS because L-band is spectrum-bound (linear in MHz below the power knee); it BREAKS if (a) power/reuse cannot hold ~2-3 bps/Hz (beam count/reuse are UNKNOWN-grade), (b) subscribers pile into dense cells the fleet cannot densify (the density caveat), or (c) the target is unmodified phones rather than purpose-built MSS terminals (the lane distinction: this is an MSS-terminal number, not a cellular-phone number). [DERIVED + FACT] Sources: cross-ref COMM-408/424/414/553/613; this doc Section 3.5.
- **COMM-651**, Modern software-defined / digitally-beamformed payloads (the AST5000 ASIC anchor: >2,000 cells / up to 2,500 beams, explicitly trading beam count against power) replace fixed-beam 1990s designs with dynamic beam placement and flexible power/spectrum allocation, letting capacity be steered to demand (maritime lanes, flight corridors, remote regions), which raises effective served-subscribers above a fixed-grid design at the same aggregate and softens (not removes) the density caveat. A multi-source survey of modern MSS-specific software-defined payloads (Inmarsat-6/ELERA, Ligado SkyTerra-class) did not complete in this pass and is a named follow-up. [FACT capability anchor; DERIVED implication; UNKNOWN on the MSS survey] Sources: cross-ref COMM-538/540 (AST5000); this doc Section 3.6 / Section 7.
- **COMM-652**, TODAY'S-FLEET narrowband holding capacity: per-beam provisioning ~80 voice circuits (x 48 beams = 3,840 beam-slots/sat), satellite-wide carrier pool 252 carriers x 4 duplex TDMA slots = ~1,008 circuits (structurally consistent with the sourced ~1,100 concurrent calls/sat), constellation-wide ~72,600 (66 x ~1,100, the product) up to a sourced ~172,000 concurrent calls; at the industry ~1-3% busy-hour concurrency that backs out to ~2.4M-17M voice-class subscribers on the AS-BUILT fleet, so today's 2.537M base is nowhere near even the old fleet's narrowband wall. [DERIVED back-out; ~80/beam FACT-SS; ~1,100 and ~172,000 FACT] Sources: [eoPortal Iridium NEXT](https://www.eoportal.org/satellite-missions/iridium-next); [Wikipedia Iridium](https://en.wikipedia.org/wiki/Iridium_satellite_constellation); [HighSpeedSat](https://www.highspeedsat.com/iridium-satellite.php); concurrency per corpus COMM-543; this doc Sections 1.4/1.5/5.2.
- **COMM-653**, The per-channel narrowband arithmetic: one 2.4 kbps Iridium channel moves ~26 MB/day run continuously (2.4 kbps x 86,400 s); a 4-message/day SBD device (~340-byte messages) needs ~14 KB/day including protocol overhead, so ONE narrowband channel time-shares ~1,900 such devices. This is the mechanism by which 2M IoT devices already fit within a ~2.6 Mbps/satellite fleet. [DERIVED, arithmetic on cited rates] Sources: rates per COMM-637/638 and COMM-620; this doc Section 5.1.
- **COMM-654**, The binding narrowband constraint at extreme device densities is RANDOM-ACCESS CONTENTION plus beam count, not aggregate bandwidth: NB-IoT NTN analysis gives ~57 to ~1,650 devices per random-access window depending on the access mode (a per-opportunity contention figure, NOT a population cap; idle attached devices do not consume access windows), and 3GPP Release 19 adds subcarrier multiplexing to raise access capacity. [FACT-SS] Sources: [arXiv 2406.14107, NB-IoT NTN random access](https://arxiv.org/abs/2406.14107); cross-ref COMM-660.
- **COMM-655**, Same-band, same-orbit, same-coverage generational replacement is a settled FCC path: Iridium NEXT replaced Block 1 under the identical Big LEO MSS authorization (Call Sign S2110) as a "replacement satellite" under FCC rule 25.165(e), requiring no replacement bond; Rocket Lab inherits this license via the deal's FCC transfer-of-control. [FACT] Sources: [FCC Engineering Statement Section B](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf); cross-ref COMM-606.
- **COMM-656**, The 2007 Big LEO band plan: Globalstar exclusive 1610-1617.775 MHz (7.775 MHz, CDMA), Iridium exclusive 1618.725-1626.5 MHz (7.775 MHz, TDMA), shared 1617.775-1618.725 MHz (0.95 MHz). Iridium NEXT satellites can physically operate across the full 1616-1626.5 MHz but Iridium's authorization is limited to its exclusive slice plus the shared sliver. [FACT] Sources: [Federal Register 2007 sharing plan](https://www.federalregister.gov/documents/2007/12/13/E7-24104/review-of-the-spectrum-sharing-plan-among-non-geostationary-satellite-orbit-mobile-satellite-service); [FCC DA-26-398](https://docs.fcc.gov/public/attachments/DA-26-398A1.pdf); cross-ref COMM-611.
- **COMM-657**, OPEN regulatory question (live 2025-2026): Iridium has petitioned the FCC for greater 1.6 GHz access (1616-1618.725 MHz, plus sharing ~6 MHz at 1610-1616 MHz with Globalstar), and Globalstar opposes (harmful-interference argument). Held MHz (exclusive ~8 vs full ~10.5 vs expanded) is unresolved and moves the max-outcome subscriber count proportionally (linear in MHz). [FACT on the dispute; UNKNOWN on outcome] Sources: [Communications Daily Dec 2025](https://communicationsdaily.com/news/2025/12/30/fight-seen-brewing-over-16-ghz-as-iridium-petitions-fcc-for-greater-access-2512290021); [Broadband Breakfast](https://broadbandbreakfast.com/globalstar-opposed-to-other-satellite-operators-in-1-6-ghz/); [Fierce Network](https://www.fierce-network.com/tech/globalstar-not-interested-iridium-s-latest-spectrum-sharing-proposal).
- **COMM-658**, OPEN regulatory question: a MUCH larger fleet, a DIFFERENT altitude (VLEO ~400-600 km vs 780 km), or more than the exclusive 8 MHz each break the clean 25.165(e) replacement path and open PFD-compliance, ITU/FCC coordination, and NGSO constellation-authorization questions (the FCC filing devotes a section to PFD limits); none is settled for a large modern fleet. "Own the band" does not automatically mean "fly any fleet on it." [FACT on the rule structure; UNKNOWN on clearance] Sources: [FCC Engineering Statement Sections B, K](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf); this doc Section 4.4.
- **COMM-659**, NARROWBAND HEADROOM effectively unlimited: a low-duty-cycle device (SBD ~340-byte messages, voice 2.4 kbps, NB-IoT kbps-class) averages ~0.03-1.5 bits/s (1-48 messages/day); a modern 8 MHz fleet at ~2.9 Gbps/sat and ~20% MAC efficiency holds ~380M-18B narrowband devices per satellite and ~130B-6,200B fleet-wide (340 sats). Narrowband capacity is NOT the binding constraint at tens of millions of devices; it is not the constraint at billions. [DERIVED; 20% efficiency ESTIMATE] Sources: this doc Section 5; rates per COMM-620/638/COMM-614.
- **COMM-660**, The real narrowband constraints are elsewhere: random-access contention per beam (not raw bits) at extreme densities, coverage/revisit geometry (a satellite overhead when the device sends), and terminals/business/spectrum-lane, none assessed here; the billions-of-devices figure is a raw-bit ceiling, and the true massive-IoT access-limited ceiling is lower and unquantified. [DERIVED + UNKNOWN] Sources: this doc Section 5.3; cross-ref coverage docs.

---

*COMM-635..660 created by this doc (the reserved block, the next free contiguous range above the global max COMM-634; not exceeded). Catalog rows for LIBRARY.md / RESEARCH_TRACKER.md / SOURCE_INDEX.md are returned to the catalog/reconciliation agent, not edited here. This doc is not committed by this pass.*
