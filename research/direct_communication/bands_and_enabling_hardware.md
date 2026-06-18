# Non-Traditional Frequency Bands and the Enabling Silicon, plus a Consolidated RF-vs-Laser Comparison

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:**
- `research/laser_comms/rf_satcom.md` (existing RF-vs-laser matrix, the conventional band table Ku/Ka/V/W, and the spectrum-access constraint). This doc does not repeat the regulatory-burden argument made there; it cites it and extends the band table upward into the non-traditional bands.
- `research/rocket_lab/space_hardware_capabilities.md` (Rocket Lab Frontier software-defined radios at L/S/C/X/Ka, Geost optical terminals and ground stations, Mynaric CONDOR optical inter-satellite terminals). This doc treats those as the in-house baseline and does not re-describe them.

The NEW contribution here is the **band-enabling-chip analysis**: for each newer or non-traditional band, what silicon and hardware actually make it usable today, and whether off-the-shelf or only emerging parts exist.

---

## Summary / Verdict

The communications frontier is moving upward in frequency for one reason: **the traditional bands (Ku, Ka) are congested and the good spectrum is already filed**, a point established in `rf_satcom.md`. The industry response is a ladder of newer bands, each trading regulatory and physical difficulty for raw bandwidth: V-band (37 to 51 GHz) is now being licensed and flown (SpaceX Gen2), E-band (71 to 86 GHz) is in commercial point-to-point use on the ground and now authorized for Starlink feeder links, W-band (92 to 114 GHz) is the subject of an active FCC inquiry with Starlink already implementing capability there, and sub-THz / D-band (110 to 170 GHz) and the 300 GHz band sit at the research and early-standards edge (IEEE 802.15.3d). Free-space optical sits outside this ladder entirely: it is effectively an **unlicensed "band"** with the most bandwidth of all and no spectrum coordination, which is exactly why `rf_satcom.md` lands on optical as the primary backbone.

The decisive finding for the chip question: **the silicon is not the bottleneck up through W-band.** Off-the-shelf or near-off-the-shelf parts already exist for the whole upper-microwave ladder: silicon (SiGe/CMOS) beamformer ICs in volume production for Ku/K/Ka phased arrays (Anokiwave at GlobalFoundries, Renesas) [FACT], commercial GaN and GaAs power-amplifier MMICs through V-band (a 47 to 52 GHz, 3.5 W GaN PA is a catalog part) [FACT], and demonstrated GaN and GaAs PA MMICs at W-band (88 to 98 GHz) in the lab and in NASA hardware [FACT]. Above W-band the parts become research-grade: sub-THz and 300 GHz links are demonstrated (NTT's 160 Gbps at 300 GHz on InP) but not productized [FACT]. On the optical side, the enabling silicon is **silicon photonics**, and it is the most mature high-rate technology of all because it is borrowed wholesale from the terrestrial data-center transceiver industry (800G and 1.6T coherent modules), the same fiber-coupled coherent transceivers NASA's TBIRD used to hit a 200 Gbps space-to-ground downlink [FACT].

**Consolidated bottom line (medium-high confidence):** for a new entrant the choice is not "wait for chips." Through W-band the chips exist; the binding constraint is spectrum coordination (covered in `rf_satcom.md`), rain fade that worsens steeply with frequency, and pointing. Optical wins on bandwidth and on having no spectrum fight, at the cost of weather and pointing. The honest framing is a portfolio: optical for the high-rate backbone, an upper-microwave RF band (V or E) as the all-weather complement, with the silicon for both already available.

**Confidence: medium-high** on the chip-availability mapping (catalog parts and peer-reviewed/NASA results are well sourced); **medium** on the highest-band figures (several are single-demo or single-vendor); **low-to-medium** on forward-looking sub-THz productization timelines.

---

## 1. The Band Ladder: What Each Non-Traditional Band Offers and Why It Is Not Traditionally Used

This table extends the conventional Ku/Ka/V/W table in `rf_satcom.md` upward and adds the "why not traditionally used" column and the regulatory status as of mid-2026. China is excluded from this analysis (see the China aside at the end).

| Band | Frequency | What it offers | Why NOT traditionally used | Regulatory / deployment status (2026) |
|---|---|---|---|---|
| **Upper microwave / V-band** | 37 to 40, 40 to 42, 47 to 50.2, 50.4 to 51.4 GHz | Large contiguous bandwidth; feeder-link and user-link capacity; aggregate >1 Tbps per VHTS satellite | Severe rain fade (at 50 GHz, 25 mm/hr rain gives >15 dB attenuation) [FACT]; needs gateway diversity; harder PA efficiency | **Live.** SpaceX Gen2 authorized in exactly these V-band segments; Eutelsat KONNECT VHTS and ViaSat-3 use Q/V feeder links [FACT]. FCC overhauling UMFUS sharing (24/28/37/39/47/50 GHz) Oct 2025 NPRM [FACT] |
| **E-band** | 71 to 76 (down), 81 to 86 (up) GHz | 10 GHz of spectrum, the most ever allocated at once; "wireless fiber," 10 Gbps+ point-to-point | Very short range terrestrially (2 to 3 km); rain-limited; needs tight beams | **Live & light-licensed.** Light-licensed worldwide for terrestrial backhaul since 2003; FCC authorized SpaceX E-band for Gen2 satellite-to-gateway links (March 2024) [FACT] |
| **W-band** | ~92 to 94, 94.1 to 100, 102 to 109.5, 111.8 to 114.25 GHz | Huge unused swathes; very high data rate at altitude / in space where air is thin | Atmospheric absorption near the surface; immature hardware; pointing | **Inquiry + first-mover.** FCC seeking comment on commercial satellite use; "largely unused for non-Federal services"; Starlink has implemented W-band capability [FACT]. Framed by FCC as a U.S. "first-mover" opportunity |
| **D-band** | 110 to 170 GHz | 6G candidate band; wide bandwidth for ultra-high-rate point-to-point | Pre-standard for satcom; severe propagation; research-grade hardware | **Research.** Active 6G research band; not a satcom allocation |
| **Sub-THz / 300 GHz band** | ~252 to 325 GHz (IEEE 802.15.3d); broadly 100 to 300 GHz | 100 Gbps to ~1 Tbps demonstrated point-to-point; the first practical THz step | Extreme path loss; tens of cm to few-hundred-m range; lab-grade ICs | **Early standard.** IEEE 802.15.3d-2017 defines a 100 Gb/s PHY at 252 to 325 GHz [FACT]; NTT demo 160 Gbps at 300 GHz (2024) [FACT] |
| **Free-space optical (treated as an unlicensed "band")** | ~193 THz (1550 nm) | Highest bandwidth of all; no spectrum license; narrow secure beam; 100 to 200 Gbps proven, Tbps roadmap | Cloud/fog/rain break the link; microradian pointing; ground-station diversity needed | **Live.** No spectrum coordination required; TBIRD 200 Gbps space-to-ground; Mynaric/Starlink inter-satellite links operational [FACT] (see `rf_satcom.md` and `space_hardware_capabilities.md`) |

**The unifying logic.** Every band above Ka is non-traditional for the same two reasons: (1) **physics gets harder with frequency** (atmospheric and rain attenuation rise steeply, beams must be narrower, PA efficiency drops), and (2) until recently there was no need, because lower bands had room. Both have changed. Lower bands are full, and the hardware (next section) has caught up through W-band. The trade is always the same: more bandwidth and (for the higher bands) easier-to-get spectrum, paid for in weather margin and pointing precision.

**Note on "easier-to-get spectrum."** This doc deliberately does not re-argue the spectrum-coordination barrier; `rf_satcom.md` covers ITU first-come-first-served, the years-long coordination, and a new entrant's junior priority. The relevant addition here is that the *higher* the band, the *less congested and more recently opened* it is, which is precisely why the FCC frames W-band as a "first-mover" opportunity. The barrier softens as you climb, but never to zero, and rain fade rises as the barrier softens.

---

## 2. The Enabling Silicon and Hardware, Band by Band

This is the new contribution. For each rung, the question is: what chip actually makes it work, and can you buy it?

### 2.1 Ku / K / Ka (the baseline, for reference)

Mature silicon. **Phased-array beamformer ICs** are in volume production:
- **Anokiwave** Gen-2 Ku and K/Ka-band silicon beamformer ICs (e.g. AWMF-0132 K-band Rx, AWMF-0133 Ka-band Tx, quad-channel dual-polarization) are in **large-scale production at GlobalFoundries** [FACT]. These are silicon (SiGe/CMOS) core chips, not exotic III-V.
- **Renesas** offers a 2nd-generation Tx/Rx/LNA family for Ku-Satcom and K/Ka-Satcom, including the **F6202** 8-channel Ka-band Rx beamforming multi-chip module for planar phased arrays [FACT].

This matters because it sets the reference: at Ka and below, beamforming is a commodity silicon problem. Rocket Lab's **Frontier** SDRs already cover up to Ka-band (`space_hardware_capabilities.md`), so the baseline is in-house.

### 2.2 V-band (37 to 51 GHz): off-the-shelf today

- **Power amplifiers:** commercial GaN MMICs exist as catalog parts. **NxBeam NPA4010-DE**: 47 to 52 GHz, **3.5 W** saturated output, **23% PAE**, **24 dB** linear gain, sold with a datasheet for satcom ground terminals and point-to-point links [FACT, single-vendor]. Qorvo, Wolfspeed, MACOM (GaN-on-SiC and GaN-on-Si, "DC to over 100 GHz"), and Europe's UMS/OMMIC supply this band [FACT].
- **GaN-on-Si for Q-band HTS** PA MMICs are published for next-generation high-throughput-satellite systems [FACT].
- **Beamforming** at V-band reuses the same silicon-core-chip approach proven at Ka; the harder part is the PA, and GaN solves it.

Verdict: **V-band is a "buy it" band.** The hardware is not the constraint; rain fade and spectrum coordination are.

### 2.3 E-band (71 to 86 GHz): commercial, GaAs/SiGe chipsets

- E-band is the most commercially mature of the >50 GHz bands because of terrestrial 5G backhaul. **Analog Devices** and others ship E-band radio chipsets and **system-in-package (SiP)** modules with integrated waveguide transitions, eliminating die-bonding assembly problems [FACT].
- Huawei, Ceragon, and Cablefree sell complete E-band radios. The chips are GaAs and SiGe; the modulators and basebands are mature.
- For space, SpaceX's authorization to run E-band satellite-to-gateway links (March 2024) shows the band is now considered flight-viable for feeders [FACT].

Verdict: **E-band hardware is a productized commodity** for point-to-point; the open question is space-qualification and rain, not chip existence.

### 2.4 W-band (92 to 114 GHz): emerging, lab-and-NASA-grade PAs

This is the frontier where chips exist but are not yet catalog commodities:
- **GaN PA MMICs at W-band:** NASA demonstrated a **W-band spatial power-combining amplifier using GaN MMICs** (1 W single chips combined to ~2 W, 9 dB gain, 15% PAE) [FACT]. Peer-reviewed GaN PA designs target high power and efficiency specifically for W-band [FACT].
- **GaAs pHEMT PA MMICs at W-band:** a published part shows >20 dB linear gain across **88 to 98 GHz**, **23.8 to 24.1 dBm** output, **24% PAE** at 94 GHz [FACT].
- The trendline is explicit in the literature: GaN MMIC PAs have "continuously increased in operating frequency," making GaN the mainstream technique for W-band solid-state PAs [FACT].

Verdict: **W-band silicon is real but pre-commodity.** You can build a W-band PA today from GaN or GaAs MMICs, but you are integrating research-grade or low-volume parts, not buying a datasheet part off a distributor shelf the way you can at V-band. This is the band to watch: the FCC "first-mover" framing plus Starlink's implemented capability suggests it productizes next.

### 2.5 Sub-THz / D-band / 300 GHz: research-grade ICs

- **InP (Indium Phosphide) HEMT** is the leading technology at the very top. **NTT achieved 160 Gbps at 300 GHz using InP-HEMT integrated-circuit front-ends** (2024) [FACT, single-source/single-demo].
- **CMOS** transmitters at 300 GHz have been demonstrated (Tokyo Tech) [FACT]; CMOS suffers severe parasitics and limited fmax at sub-THz, partly solved by architecture and node scaling [FACT].
- **SiGe BiCMOS** is the workhorse for D-band (110 to 170 GHz) transceivers in the 6G research community [FACT].
- Standardization is nascent: **IEEE 802.15.3d-2017** defines a 100 Gb/s PHY at 252 to 325 GHz [FACT].

Verdict: **No off-the-shelf satcom parts.** These are 6G research ICs (InP, SiGe BiCMOS, advanced CMOS) demonstrated over short links. For a satellite communications business in the near term, sub-THz is a watch-item, not a buildable band.

### 2.6 Free-space optical: silicon photonics is the enabling silicon

Treated here as the unlicensed "band." The enabling silicon is **silicon photonics (SiPh)**: optical waveguides, modulators, multiplexers, and photodetectors integrated on a silicon substrate using CMOS-derived processes [FACT].
- **Maturity is borrowed from the data-center industry.** SiPh coherent transceivers are in volume at **400G, 800G, and 1.2T/1.6T**, driven by AI GPU-cluster interconnect demand (200G/channel SiPh + advanced DSP) [FACT]. This is the single most mature high-rate transceiver technology in existence.
- **It is already flight-proven for space links by reuse.** NASA's **TBIRD** hit a **200 Gbps** space-to-ground downlink (and moved up to 4.8 TB in a single pass) using **fiber-coupled coherent transceivers routinely used in terrestrial fiber telecom** [FACT]. Coherent FSO can raise link capacity 10 to 100x over RF [FACT].
- **Silicon optical phased arrays** enable chip-scale beam steering (the same technology family as LiDAR), relevant to non-mechanical pointing [FACT].
- **Modems:** coherent optical modems borrow the terrestrial DSP/PAM4/coherent stack directly.

The one caveat the searches surfaced: published SiPh modules are data-center parts; **explicit space-grade radiation-hardened SiPh module datasheets were not found** in this pass. Space use today is via fiber-coupled coherent transceivers adapted for space (TBIRD approach) and purpose-built terminals (Mynaric CONDOR, per `space_hardware_capabilities.md`), not a radiation-hardened commercial SiPh module line. Flag this as an open question.

### 2.7 Summary: chip availability by band

| Band | Enabling silicon / hardware | Off-the-shelf? |
|---|---|---|
| Ku/K/Ka | Silicon (SiGe/CMOS) beamformer ICs (Anokiwave, Renesas) | **Yes, volume production** [FACT] |
| V-band (37 to 51 GHz) | GaN PA MMICs (NxBeam, Qorvo, Wolfspeed, MACOM, UMS); silicon beamformers | **Yes, catalog parts** [FACT] |
| E-band (71 to 86 GHz) | GaAs/SiGe chipsets + SiP modules (Analog Devices, Huawei, Ceragon) | **Yes, productized for P2P** [FACT] |
| W-band (92 to 114 GHz) | GaN and GaAs pHEMT PA MMICs (NASA, peer-reviewed) | **Emerging, lab/low-volume** [FACT] |
| D-band / sub-THz / 300 GHz | InP-HEMT, SiGe BiCMOS, advanced CMOS | **No, research-grade only** [FACT] |
| Free-space optical | Silicon photonics coherent transceivers + DSP; optical phased arrays | **Yes (data-center parts); space-grade hardened modules: open question** [FACT] |

---

## 3. Consolidated RF-vs-Laser Pros and Cons

This consolidates and slightly extends the head-to-head matrix in `rf_satcom.md` (which should be read as the primary version). The addition here is a single clean table across the seven dimensions the assignment names, with the upper-microwave bands folded in.

| Dimension | RF (Ka through W-band) | Laser / Free-space optical | Edge |
|---|---|---|---|
| **Bandwidth (per link)** | Ka HTS ~500 Gbps/satellite shared; V-band VHTS >1 Tbps/satellite shared; E-band ~10 Gbps point-to-point; per-link share for a new entrant is far smaller | 100 to 200 Gbps proven dedicated point-to-point (TBIRD 200 Gbps); Tbps-class roadmap; 10 to 100x RF capacity | **Optical** for dedicated links |
| **Regulation / spectrum burden** | Severe and band-dependent: Ka/V coordinated and contested (see `rf_satcom.md`); E-band light-licensed; W-band an open FCC inquiry; burden eases as you climb but never to zero | **None** for the optical carrier; no ITU/FCC spectrum coordination | **Optical** (decisive) |
| **Weather** | Robust at low bands; rain fade rises steeply with frequency (>15 dB at 50 GHz in 25 mm/hr rain); degrades gracefully, does not drop; mitigated by gateway diversity | Cloud/fog/rain **break** the link; needs optical-ground-station diversity and/or an RF weather backup | **RF** |
| **Mass / power** | Higher mass and power for equivalent capacity; GaN improves PA efficiency at mmWave but antennas/arrays are heavier | Lower; receivers and apertures far smaller than equivalent RF antennas | **Optical** |
| **Pointing** | Wide beams at low bands (easy acquisition); narrows toward W-band and E-band (tighter pointing needed but still far easier than optical) | Microradian pointing, multi-second acquisition, adaptive optics, moving parts (or optical phased arrays) | **RF** |
| **Security / interference** | Wider beams: more interference-prone, easier to intercept/jam (improves as beams narrow at higher bands) | Narrow beam: no RF interference, very hard to intercept, low probability of detect | **Optical** |
| **Maturity** | Decades of heritage at Ka and below; V-band flying (SpaceX Gen2); E-band productized terrestrially; W-band emerging; sub-THz research-grade | Proven at scale (Starlink ISLs, TBIRD, Mynaric 100+ terminals) but ground-link operations still maturing | **RF** at the high bands; **optical** proven for ISLs; both flight-proven at the core |

**Reading of the table.** Optical wins decisively on the two dimensions that dominate for a new entrant: **bandwidth per dedicated link** and **no spectrum burden** (the same conclusion `rf_satcom.md` reaches). RF wins on **weather, pointing, and high-band maturity**. The upper-microwave RF bands (V, E) are the natural all-weather complement to an optical backbone, and crucially their **enabling silicon is already off-the-shelf** (Section 2), so adding an RF complement is not gated by chip development. The honest architecture is a portfolio, not a winner-take-all.

---

## 4. Sources

W-band and upper-microwave spectrum:
- [FCC, Looks to Unleash More Spectrum for Satellite Spectrum Abundance](https://www.fcc.gov/document/fcc-looks-unleash-more-spectrum-satellite-spectrum-abundance)
- [Federal Register, Satellite Spectrum Abundance (W-band segments)](https://www.federalregister.gov/documents/2025/06/27/2025-11966/satellite-spectrum-abundance)
- [Federal Register, Facilitating More Intensive Use of Upper Microwave Spectrum (Dec 2025)](https://www.federalregister.gov/documents/2025/12/03/2025-21805/facilitating-more-intensive-use-of-upper-microwave-spectrum)
- [DLA Piper, FCC proposes licensing reforms for UMFUS bands](https://www.dlapiper.com/en-us/insights/publications/2025/11/fcc-proposes-reforms-facilitating-spectrum-sharing-in-upper-microwave-bands)
- [Holland & Knight, FCC Rulemaking on Space Station Licensing and Spectrum Sharing](https://www.hklaw.com/en/insights/publications/2025/11/fcc-rulemaking-on-space-station-licensing-and-spectrum-sharing)
- [Wikipedia, W band](https://en.wikipedia.org/wiki/W_band)

GaN / GaAs / V-band / W-band power amplifiers:
- [NxBeam, V-Band GaN Power Amplifier MMIC (47 to 52 GHz, 3.5 W)](https://www.nxbeam.com/v-band-power-amplifier-mmic/)
- [Microwave Journal, 3.5 W V-Band GaN Power Amplifier MMIC](https://www.microwavejournal.com/articles/39629-35-w-v-band-gan-power-amplifier-mmic)
- [NASA NTRS, W-Band Spatial Power-Combining Amplifier using GaN MMICs](https://ntrs.nasa.gov/citations/20210008525)
- [NCBI/PMC, W-Band GaAs pHEMT Power Amplifier MMIC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11767286/)
- [NCBI/PMC, High-Power, High-Efficiency GaN PA for W-Band](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12472057/)
- [EurekAlert, GaN transistors and high-power amplifiers for mmWave satcom](https://www.eurekalert.org/news-releases/1056739)
- [MACOM, GaN MMICs (DC to >100 GHz)](https://www.macom.com/products/rf-microwave-mmwave/gan-mmics)
- [ScienceDirect, Advances in GaN Devices at Higher mm-Wave Frequencies](https://www.sciencedirect.com/science/article/pii/S2772671123000724)

Phased-array beamformer ICs:
- [Anokiwave, Gen-2 Ka/Ku-band silicon beamformer ICs in production at GlobalFoundries](https://www.semiconductor-today.com/news_items/2020/mar/anokiwave-120320.shtml)
- [Anokiwave, SATCOM Products](https://www.anokiwave.com/satcom/index.html)
- [Renesas, Phased Array Beamformers](https://www.renesas.com/us/en/products/rf-products/phased-array-beamformers)
- [Renesas, F6202 Ka-Band SATCOM Rx Beamforming IC](https://www.renesas.com/en/products/rf-products/phased-array-beamformers/f6202-8-channel-single-beam-rx-active-beamforming-ic-module-ka-band-satcom)

E-band:
- [SpaceNews, SpaceX gets E-band radio waves to boost Starlink broadband](https://spacenews.com/spacex-gets-e-band-radio-waves-to-boost-starlink-broadband/)
- [E-Band Communications, 70/80 GHz Overview](https://www.e-band.com/70-80-GHz-Overview)
- [Analog Devices, E-Band Wireless Radio Links for 5G Backhaul](https://www.analog.com/en/resources/technical-articles/e-band-wireless-radio-links.html)
- [Ceragon, Wireless Backhaul Spectrum (E-band light licensing)](https://www.ceragon.com/blog/wireless-backhaul-spectrum)

Starlink V-band / E-band / W-band authorizations:
- [Via Satellite, FCC Gives SpaceX Approval for 7,500 More Starlink Gen2 Satellites](https://www.satellitetoday.com/connectivity/2026/01/12/fcc-gives-spacex-approval-for-7500-more-starlink-gen2-satellites/)
- [Broadband Breakfast, FCC Approves 7,500 More Starlink Gen2 Satellites](https://broadbandbreakfast.com/fcc-approves-7-500-more-starlink-gen2-satellites/)

Q/V-band feeder links and rain fade:
- [RF Essentials, Why Q/V Band Is the Hottest Investment in RF](https://rfessentials.com/industry-news/mmwave-5g/qv-band-investment-satellite-communications/)
- [MDPI Electronics, Forward Link Optimization for VHTS Satellite Networks](https://www.mdpi.com/2079-9292/9/3/473)
- [Wiley, Advanced Fade Mitigation Techniques for Q/V Band SATCOM (2026)](https://onlinelibrary.wiley.com/doi/full/10.1002/sat.70007)

Sub-THz / 300 GHz / D-band:
- [NTT, 160 Gbps in the 300 GHz band using InP integrated IC technology](https://group.ntt/en/newsrelease/2024/10/28/241028b.html)
- [Tokyo Tech, 300 GHz band CMOS transmitter](https://www.titech.ac.jp/english/news/2024/068396)
- [ScienceDirect, 6G via sub-THz CMOS power amplifiers: challenges and trends](https://www.sciencedirect.com/science/article/pii/S2405844025017773)
- [MDPI Electronics, Review of Circuits for Advanced Sub-THz Transceivers](https://www.mdpi.com/2079-9292/14/5/861)
- [IEEE Xplore, IEEE 802.15.3d: First Standardization for Sub-THz toward 6G](https://ieeexplore.ieee.org/document/9269931/)

Silicon photonics and optical:
- [Nature Scientific Reports, 100 Gbps coherent free-space optical at LEO tracking rates](https://www.nature.com/articles/s41598-022-22027-0)
- [NASA NTRS, On-Orbit Demonstration of 200-Gbps Laser Communication Downlink (TBIRD)](https://ntrs.nasa.gov/citations/20230000434)
- [NASA, Record-Breaking Laser Demo Completes Mission (TBIRD)](https://www.nasa.gov/directorates/somd/space-communications-navigation-program/nasas-record-breaking-laser-demo-completes-mission/)
- [PMC, Free-Space Applications of Silicon Photonics: A Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC9322159/)
- [Nokia, C-STAR silicon photonics for coherent transport](https://www.nokia.com/optical-networks/cstar-silicon-photonics/)
- [Naddod, Silicon Photonics 800G to 1.6T optical modules](https://www.naddod.com/blog/market-insights-800g-1-6t-silicon-photonics-optical-modules)

---

## 5. Confidence

**Overall: medium-high**, with the level varying sharply by band.

- **High confidence:** the band ladder itself (which bands, what frequencies, the rain-fade-vs-bandwidth trade), the existence of off-the-shelf silicon beamformers at Ka and below, off-the-shelf GaN PA MMICs at V-band, productized E-band chipsets, and silicon photonics maturity. These rest on catalog parts, FCC documents, peer-reviewed papers, and NASA reports, each with 2+ sources.
- **Medium confidence:** the W-band PA figures (peer-reviewed and NASA, but specific numbers come from individual papers, not a market of catalog parts); the NxBeam V-band part specs (single vendor, though the band's commercial maturity is corroborated by Qorvo/Wolfspeed/MACOM presence); the 160 Gbps / 300 GHz NTT result (a single demonstration, widely reported but one team).
- **Low-to-medium confidence:** anything forward-looking on sub-THz productization timing, and the precise state of space-grade radiation-hardened silicon photonics modules (not found in this pass).

The consolidated RF-vs-laser conclusion is **medium-high** and consistent with `rf_satcom.md`; this doc adds the chip-availability dimension, which strengthens rather than changes that conclusion.

---

## 6. Open Questions

1. **Space-grade silicon photonics.** Are there radiation-hardened, space-qualified SiPh coherent-transceiver modules as catalog products, or is every space optical link still a purpose-built terminal (Mynaric CONDOR) or an adapted fiber-telecom transceiver (TBIRD)? Not resolved here.
2. **W-band productization timeline.** W-band PA MMICs exist in the lab and in NASA hardware, and Starlink has implemented W-band capability, but when does a catalog W-band satcom front-end appear? This determines whether W-band is a 2027 or a 2030+ option.
3. **Rain-fade economics at V/W-band for a new entrant.** The >15 dB fade at 50 GHz is established; the gateway-diversity cost to make a V or W feeder link reliable is not quantified here and should be modeled before any RF-complement scenario.
4. **Single-vendor figures to double-check.** The NxBeam V-band PA specs (47 to 52 GHz, 3.5 W, 23% PAE, 24 dB) and the NTT 160 Gbps / 300 GHz record are each effectively single-source and should be re-verified against a second independent source before being relied on.
5. **Per-link vs shared capacity.** As `rf_satcom.md` flags, the >1 Tbps VHTS and ~500 Gbps Ka headline numbers are shared across beams/users; the dedicated per-link RF capacity a new entrant could field is much smaller and is the apples-to-apples comparator against a dedicated optical link.
6. **Optical phased arrays for non-mechanical pointing.** Chip-scale optical beam steering exists (LiDAR lineage); whether it is mature enough to replace mechanical gimbals on a space optical terminal (removing the moving-parts liability) is unresolved.

---

## China aside (excluded from main analysis)

Per the effort's scope, China is excluded from the main analysis and noted only here. GalaxySpace's YINHE-1 (cited in `rf_satcom.md`) was an early V/Ka LEO broadband demonstrator (~24 Gbps), and Chinese groups are active in sub-THz / 300 GHz research and in their own LEO constellations (Guowang, Qianfan). These are noted for completeness only and are not factored into the band, chip-availability, or RF-vs-laser assessments above.

---

## 7. Claims Table

| Claim ID | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-001 | FCC seeking comment on commercial satellite use of W-band segments | 92 to 94, 94.1 to 100, 102 to 109.5, 111.8 to 114.25 GHz | [FACT] | FCC Satellite Spectrum Abundance; Federal Register |
| COMM-002 | FCC UMFUS NPRM bands under review for more intensive use | 24, 28, 37, 39, 47, 50 GHz (NPRM adopted Oct 28 2025) | [FACT] | Federal Register (Dec 2025); DLA Piper; Holland & Knight |
| COMM-003 | SpaceX Gen2 authorized V-band segments | 37.5 to 42 GHz (down), 47.2 to 51.4 GHz (up) | [FACT] | Via Satellite; Broadband Breakfast; FCC |
| COMM-004 | SpaceX authorized E-band for satellite-to-gateway links (March 2024) | 71 to 76 GHz (down), 81 to 86 GHz (up) | [FACT] | SpaceNews; FCC |
| COMM-005 | E-band spectrum allocated at once (light-licensed worldwide since 2003) | 10 GHz total; ~10 Gbps point-to-point over 2 to 3 km | [FACT] | E-Band Communications; Analog Devices; Ceragon |
| COMM-006 | Rain attenuation at 50 GHz, 25 mm/hr rain rate | >15 dB | [FACT] | RF Essentials; MDPI Electronics |
| COMM-007 | VHTS aggregate throughput using Q/V feeder links (KONNECT VHTS, ViaSat-3) | >1 Tbps per satellite (shared) | [FACT] | RF Essentials; MDPI |
| COMM-008 | NxBeam NPA4010-DE V-band GaN PA MMIC spec | 47 to 52 GHz, 3.5 W, 23% PAE, 24 dB gain | [FACT] (single vendor) | NxBeam; Microwave Journal |
| COMM-009 | NASA W-band GaN MMIC spatial power-combining amplifier | ~2 W combined (1 W chips), 9 dB gain, 15% PAE | [FACT] | NASA NTRS |
| COMM-010 | W-band GaAs pHEMT PA MMIC performance | >20 dB gain 88 to 98 GHz; 23.8 to 24.1 dBm out; 24% PAE @ 94 GHz | [FACT] | NCBI/PMC |
| COMM-011 | Anokiwave Gen-2 Ku/K/Ka silicon beamformer ICs production status | Large-scale production at GlobalFoundries | [FACT] | Semiconductor Today; Anokiwave |
| COMM-012 | NTT sub-THz wireless record (2024) | 160 Gbps at 300 GHz on InP-HEMT ICs | [FACT] (single demo) | NTT |
| COMM-013 | IEEE 802.15.3d sub-THz PHY | 100 Gb/s at 252 to 325 GHz | [FACT] | IEEE Xplore; IEEE 802.15.3d-2017 |
| COMM-014 | NASA TBIRD optical space-to-ground downlink | 200 Gbps; up to 4.8 TB per pass; fiber-coupled coherent transceivers | [FACT] | NASA NTRS; NASA |
| COMM-015 | Coherent FSO capacity advantage over RF | 10 to 100x | [FACT] | Nature Sci Reports; SPIE/EffectPhotonics |
| COMM-016 | Silicon photonics coherent transceiver volume rates (terrestrial data center) | 400G, 800G, 1.2T/1.6T (200G/channel) | [FACT] | Naddod; Nokia |
