# Rocket Lab Acquires Iridium: The Deal, the Asset, and the Hooks for the Cellular Thesis

*Research date: June 29, 2026 (day-of announcement). Communications research-wiki effort (shared library). No go/no-go verdict: this doc pulls the verified facts so the build-vs-buy and the spectrum assumption can be re-assessed.*

**Why this doc exists.** The Rocket Lab direct-to-cell thesis holds SPECTRUM out as a large, separate cost (the corpus prices a competitive owned cellular position at tens of billions; see grounding below). On June 29, 2026, Rocket Lab announced a definitive agreement to acquire Iridium Communications. If that closes, Rocket Lab would own an operating LEO constellation, a globally coordinated L-band spectrum position, a real subscriber and government and IoT business, and the ground infrastructure, all in-house. This doc verifies the deal and catalogs Iridium as an asset, then states the factual hooks (and the explicit non-hooks) for the cellular thesis. It renders no verdict.

**Builds on / does not duplicate (cite, do not repeat):**
- [`../direct_communication/dtc_spectrum_access.md`](../direct_communication/dtc_spectrum_access.md) (COMM-313 and the spectrum-access block): owns the "you cannot use any spectrum" answer, the unmodified-phone radio-set gate (a bare handset has front-end filters and PAs for ~600 MHz to ~2.1 GHz cellular bands and NO L-band MSS radio), the SCS band list (600/700/800 MHz, PCS ~1.9 GHz, AWS H-block ~2 GHz), and the three acquisition routes (SCS lease near-zero capex, outright buy tens of billions, 6G/FR3 not a near-term door). This doc USES that gate to draw the Iridium-L-band-vs-cellular distinction; it does not re-derive it.
- [`../direct_communication/spectrum_purchase_and_6g.md`](../direct_communication/spectrum_purchase_and_6g.md) (COMM-229..248): owns the quantity benchmark (GSMA ~80-100 MHz to launch, ~100-200 MHz to match an incumbent), the secondary-market $/MHz-POP prices, the total-dollar US-plus-Europe translation (~$32-46B for 100 MHz, ~$65-90B for 200 MHz), and the EchoStar/Ligado MSS-holder path. This doc cites those anchors; it does not re-compute them.
- [`../direct_communication/leo_constellation_coverage_minimums.md`](../direct_communication/leo_constellation_coverage_minimums.md) (COMM-209..228) and [`../direct_communication/dtc_coverage_geography.md`](../direct_communication/dtc_coverage_geography.md) (COMM-380..405): own the Iridium-66 Walker-Star validation (86.4 deg, 780 km, 66/6/2), the polar-vs-53-deg inclination signature, and the coverage-floor counts. This doc treats Iridium's constellation as the now-owned instance of that geometry; it does not re-derive the floor math.
- [`../economics/comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) (COMM-141..154): owns the EchoStar ~$17B / ~65 MHz and AST/Ligado ~45 MHz "own dedicated D2D spectrum" deals as comparable spectrum-value precedents.

> **Reading guide.** Every hard number is tagged **[FACT]** (2+ independent sources), **[FACT, single-source]**, **[DERIVED]** (arithmetic on cited inputs), **[ESTIMATE]** (reasoned), or **[UNKNOWN]** (named gap). The June 29 deal is **CONFIRMED** (the announcement is real, carried by the joint press release, both companies' SEC filings, and major financial press). China is excluded. No verdict on the Rocket Lab business is rendered.

---

## Answer First

**1. The deal is real and confirmed.** On June 29, 2026, Rocket Lab Corporation (Nasdaq: RKLB) and Iridium Communications Inc. (Nasdaq: IRDM) announced a definitive agreement for Rocket Lab to acquire Iridium for **$54.00 per share**, a **cash-and-stock** transaction (**$27.00 cash** plus Rocket Lab stock per share) at an **enterprise value of ~$8.0 billion** [FACT]. The cash-and-stock is a ~**24%** premium to Iridium's June 26 close of $43.52 [FACT, DERIVED]. The stock half rides an exchange-ratio collar (RKLB $67.50 to $112.50, ratio 0.4000 to 0.2400) [FACT]. Rocket Lab lined up a **$3.6B 364-day senior secured bridge term loan** (Deutsche Bank, Wells Fargo) [FACT]. Both boards approved unanimously; Iridium directors signed voting agreements; an Iridium termination fee of **$223.62M** applies [FACT]. Expected close: **mid-2027**, subject to Iridium stockholder approval, HSR antitrust, **FCC transfer-of-control** of Iridium's licenses, and foreign-investment clearances [FACT].

**2. What Iridium IS (the asset Rocket Lab is buying).** An operating, cash-generative LEO satellite-communications company:
- **Constellation:** the Iridium NEXT network, **66 operational satellites** plus on-orbit spares (the corpus's validated Walker-Star **86.4 deg / 780 km / 66 in 6 planes**), unique for its **Ka-band inter-satellite cross-links** (a self-relaying mesh that needs no ground station underfoot) and true **pole-to-pole global coverage** [FACT].
- **Spectrum:** a **globally coordinated L-band Mobile-Satellite Service (MSS) allocation** at **~1616-1626.5 MHz** for the user links (a rare worldwide MSS position), plus Ka-band feeder and cross-link spectrum [FACT]. This is **narrowband mobile-satellite** spectrum, NOT terrestrial cellular low-band.
- **Business (FY2025):** revenue **$871.659M**, operational EBITDA **$495.330M (56.8% margin)**, net income **$114.372M**, **2,537,000 billable subscribers** (the IoT line alone is 1,998,000) [FACT]. The U.S. government EMSS airtime contract is a **$738.5M, 7-year** fixed-price deal (~$107M/yr) [FACT].
- **Services:** satellite voice and data, **Short Burst Data (SBD)** IoT messaging (the volume engine), **Certus** L-band broadband (low hundreds of kbps up to ~1.4 Mbps class), and a new **Iridium NTN / direct-to-device** offering (3GPP NB-IoT NTN over L-band, IoT/SOS messaging, not broadband voice/data to phones).

**3. The hooks for the RKLB cellular thesis (factual, no verdict).** Owning Iridium would give Rocket Lab, in-house: (a) **an operating constellation and the manufacture-to-operate skill set** (it already builds and launches; now it would run a live network), (b) a **globally coordinated spectrum position** that it owns rather than rents, (c) **ground infrastructure** (gateways, the dedicated DoD gateway, teleport, network operations), (d) a **paying customer base** of 2.5M-plus across government, maritime, aviation, and IoT, and (e) an **NTN / direct-to-device standards path** already in motion. It also changes the build-vs-buy frame: ~$8B EV buys a real, profitable, spectrum-holding satcom operator, against the corpus's ~$32-90B spectrum-ONLY cost for an owned cellular position.

**4. What it does NOT give (the load-bearing distinction).** Iridium's spectrum is **L-band MSS at ~1.6 GHz**, which is **not the cellular low-band an unmodified phone uses**. Per the corpus gate ([`dtc_spectrum_access.md`](../direct_communication/dtc_spectrum_access.md), COMM-313): a standard 3GPP handset has radios for ~600 MHz to ~2.1 GHz **cellular** bands and **no L-band MSS radio**, so Iridium's network talks to **purpose-built Iridium terminals** (sat phones, modems, IoT chipsets), NOT to an ordinary smartphone over Iridium's native band. Iridium's direct-to-device path is **narrowband NB-IoT NTN** (messaging, SOS), not the broadband 3GPP cellular voice/data-to-phone that AST SpaceMobile and Starlink Direct-to-Cell deliver by leasing a partner MNO's terrestrial cellular spectrum. So owning Iridium delivers spectrum, a constellation, ground, customers, and an NTN foothold, but **it does not by itself hand Rocket Lab the cellular low-band, the partner-MNO spectrum, or a broadband-to-unmodified-phone capability** the direct-to-cell thesis is built on. Those remain a separate question.

**Confidence: high on the deal terms** (joint press release plus both companies' SEC filings plus CNBC/SpaceNews, fully consistent). **High on Iridium's FY2025 financials and constellation** (primary press release and 2+ independent sources, plus the corpus's own prior validation). **High on the L-band-vs-cellular distinction** (the corpus gate is multi-source FACT; Iridium's L-band frequency is multi-source FACT). The spectrum-value implication is a framing, not a verdict.

---

## 1. The Deal (June 29, 2026): Confirmed, with Terms

### 1.1 It is real

The acquisition is confirmed, not a rumor. The same terms appear in the **joint press release** (issued through both companies), in **Rocket Lab's and Iridium's SEC filings** (Form 8-K and Form 425), and in independent financial press (CNBC, SpaceNews, Reuters-syndicated coverage). All sources agree on the headline numbers.

- Announced **June 29, 2026** by Rocket Lab Corporation (Nasdaq: RKLB) and Iridium Communications Inc. (Nasdaq: IRDM) [FACT] ([Iridium investor release, Jun 29 2026](https://investor.iridium.com/2026-06-29-Rocket-Lab-to-Acquire-Iridium-in-Historic-Deal,-Creating-A-Fully-Vertically-Integrated-Space-Powerhouse-Primed-for-Growth); [PR Newswire, Jun 29 2026](https://www.prnewswire.com/news-releases/rocket-lab-to-acquire-iridium-in-historic-deal-creating-a-fully-vertically-integrated-space-powerhouse-primed-for-growth-302813075.html); [SpaceNews, Jun 29 2026](https://spacenews.com/rocket-lab-to-acquire-iridium/); [CNBC, Jun 29 2026](https://www.cnbc.com/2026/06/29/rocket-lab-buys-iridium.html)).

### 1.2 The terms

| Term | Value | Tag |
|---|---|---|
| Structure | Definitive merger agreement, cash-and-stock | [FACT] |
| Price per Iridium share | $54.00 | [FACT] |
| Cash component | $27.00 per share | [FACT] |
| Stock component | RKLB shares per exchange ratio, collar $67.50-$112.50 (ratio 0.4000 to 0.2400) | [FACT] |
| Enterprise value | ~$8.0 billion | [FACT] |
| Premium | ~24% over Iridium's June 26, 2026 close of $43.52 | [FACT] / [DERIVED] |
| Bridge financing | $3.6B 364-day senior secured term loan (Deutsche Bank, Wells Fargo) | [FACT] |
| Iridium termination fee | $223.62 million | [FACT] |
| Board approval | Unanimous, both boards; Iridium director voting agreements (~1.6% of shares) | [FACT] |
| Expected close | Mid-2027 | [FACT] |
| Closing conditions | Iridium stockholder vote; HSR antitrust; FCC transfer-of-control of Iridium telecom authorizations; foreign-investment clearances; Form S-4 effectiveness; Nasdaq listing of the new RKLB shares | [FACT] |

Sources for the table: [Rocket Lab 8-K summary, StockTitan, Jun 29 2026](https://www.stocktitan.net/sec-filings/RKLB/8-k-rocket-lab-corp-reports-material-event-45990394fdac.html) (collar, termination fee, FCC transfer-of-control, HSR, bridge lenders verbatim); [PR Newswire joint release, Jun 29 2026](https://www.prnewswire.com/news-releases/rocket-lab-to-acquire-iridium-in-historic-deal-creating-a-fully-vertically-integrated-space-powerhouse-primed-for-growth-302813075.html) (price, cash split, EV, bridge, boards); [Yahoo Finance, Jun 29 2026](https://finance.yahoo.com/markets/stocks/articles/rocket-lab-acquires-iridium-8-123239082.html) (premium 24.1%, mid-2027 close, 2.55M subscribers); [Iridium IRDM market cap / June 26 close $43.52, Macrotrends/stockanalysis, Jun 26 2026](https://www.macrotrends.net/stocks/charts/IRDM/iridium-communications-inc/market-cap).

**Premium check [DERIVED]:** $54.00 / $43.52 - 1 = 24.1%, matching the reported figure. Iridium's pre-deal market cap was ~$4.6-5.5B and its pre-deal enterprise value ~$7.1B, so the ~$8.0B EV is a genuine control premium over the standalone enterprise value [FACT, market-data sources above].

### 1.3 The stated rationale

The framing from both sides is **vertical integration**: a single company that designs, builds, launches, AND operates its own constellations.

- Sir Peter Beck (Rocket Lab CEO): "This is a defining moment for the space industry ... Iridium has built the gold standard in secure, safety-critical global satellite connectivity ... we have the capability to unlock entirely new markets." Beck also framed the combination as "a fully integrated self-launching space superpower," citing Iridium's "rare spectrum" explicitly [FACT, single-source on each verbatim quote] ([PR Newswire, Jun 29 2026](https://www.prnewswire.com/news-releases/rocket-lab-to-acquire-iridium-in-historic-deal-creating-a-fully-vertically-integrated-space-powerhouse-primed-for-growth-302813075.html); [SpaceNews, Jun 29 2026](https://spacenews.com/rocket-lab-to-acquire-iridium/)).
- Matt Desch (Iridium CEO): "Success will come from those who can bring new innovations to space quickly ... as part of Rocket Lab, a fully integrated, end-to-end space company" [FACT, single-source quote] ([PR Newswire](https://www.prnewswire.com/news-releases/rocket-lab-to-acquire-iridium-in-historic-deal-creating-a-fully-vertically-integrated-space-powerhouse-primed-for-growth-302813075.html)).
- Rocket Lab's stated plans for the asset: deploy **direct-to-device (D2D / Iridium NTN Direct)** services, develop a **next-generation constellation**, expand **IoT and PNT** (position, navigation, timing), and **leverage the spectrum** for new defense and commercial applications [FACT, single-source on the plan list] ([PR Newswire](https://www.prnewswire.com/news-releases/rocket-lab-to-acquire-iridium-in-historic-deal-creating-a-fully-vertically-integrated-space-powerhouse-primed-for-growth-302813075.html)).

Market reaction on announcement day: Iridium shares jumped (~20%, toward the deal price) and Rocket Lab rose (~9%) [FACT] ([CNBC, Jun 29 2026](https://www.cnbc.com/2026/06/29/rocket-lab-buys-iridium.html); [StockTitan RKLB news, Jun 29 2026](https://www.stocktitan.net/news/RKLB/rocket-lab-to-acquire-iridium-in-historic-deal-creating-a-fully-k1sa3qghi3kz.html)).

---

## 2. Iridium, What It Is

### 2.1 History (brief)

Iridium was conceived at **Motorola** (Chandler, Arizona) in 1987-1988 and developed 1993-1998 as a 66-plus satellite global voice system (the name "Iridium," element 77, reflects the original 77-satellite plan, later reduced to 66). Commercial service began **November 1, 1998**. The first-generation operating company (Iridium LLC) filed **Chapter 11 in August 1999**, after spending ~$5 billion against only ~10,000 subscribers, one of the largest commercial failures of its era. The assets were bought for ~$25M by investors led by Dan Colussy (Dec 2000, Iridium Satellite LLC), with the DoD as anchor customer. The company **relisted in September 2009 via the GHL Acquisition Corp. SPAC** as Iridium Communications Inc. (Nasdaq: IRDM) [FACT, multi-source; see ledger].

### 2.2 The constellation (Iridium NEXT)

The headline, corroborated by our own corpus and confirmed in the deal coverage:
- **66 operational satellites** plus **15 spares (9 on-orbit + 6 ground), 81 total NEXT satellites built**, in a **Walker-Star polar** arrangement: **86.4 deg inclination, ~780 km altitude, 66 satellites in 6 planes** (11 per plane, planes ~30 deg apart, Walker designation 66/6/2), validated in [`leo_constellation_coverage_minimums.md`](../direct_communication/leo_constellation_coverage_minimums.md) (COMM-211, COMM-213) and [`dtc_coverage_geography.md`](../direct_communication/dtc_coverage_geography.md) (COMM-396) [FACT, multi-source: Wikipedia + eoPortal, accessed Jun 2026]. (Deal-day press cited "66 operational + 14 on-orbit spares"; the cross-validated primary references give 9 on-orbit + 6 ground = 15 spares, 81 built.)
- Orbital period ~100-101 minutes. The **Walker-Star polar** geometry (planes intersecting at the poles) gives true **pole-to-pole global coverage including the poles**, distinct from the Walker-Delta pattern of GPS/Starlink [FACT].
- **Distinctive feature: 4 Ka-band inter-satellite cross-links per satellite** (2 fore/aft in-plane, 2 to adjacent planes) form a self-relaying space mesh, so Iridium routes a call or packet across the constellation and down at a distant gateway without a ground station under every satellite. This is what gives it the global, oceans-and-poles reach the populated-mid-latitude 53-deg systems do not have [FACT, multi-source: eoPortal + Wikipedia].
- Each satellite carries a **48-beam** L-band phased array (~4,700 km footprint) supporting on the order of **~1,100 concurrent calls** at 2.4 kbps [FACT on 48 beams (Gunter's + eoPortal); ~1,100 calls is single-strong-source (Wikipedia)].
- **Satellite mass ~860 kg**, design life **10 years (15-year planned mission life)** [FACT, multi-source: Gunter's + eoPortal].
- **Hosted payloads:** Aireon space-based ADS-B aviation surveillance receivers (hardware by Harris / L3Harris) on all 81 satellites, plus maritime AIS; the hosted-payload allocation is ~50 kg / ~50 W per satellite [FACT, multi-source: eoPortal + Aireon].

### 2.3 The operator and manufacturer

- **Iridium NEXT** (the current generation) was built by **Thales Alenia Space** (prime, ELiTeBus-1000 bus), integrated by **Orbital ATK / Northrop Grumman** at Gilbert, Arizona, and launched by **SpaceX Falcon 9** from Vandenberg across **8 missions (75 satellites, January 2017 to January 2019)**, at a program cost of **~$3 billion** [FACT, multi-source: SpaceNews + eoPortal + Iridium investor PR + Gunter's].
- Iridium operates its own ground network (commercial gateways plus a dedicated U.S. government gateway at **Wahiawa, Hawaii** for the DoD), so the acquisition brings **in-house ground infrastructure**, not just satellites [FACT].

---

## 3. Iridium Spectrum

**The user-link band (the valuable, rare part):** Iridium holds a **globally coordinated L-band Mobile-Satellite Service (MSS) allocation at 1616-1626.5 MHz (10.5 MHz span)**, used with a **hybrid TDMA/FDMA, time-division-duplex (TDD)** air interface (90 ms frames, 2.4 kbps per channel, QPSK) to Iridium terminals [FACT, multi-source: Wikipedia + mobitex.org + apollosat]. Within that band, Iridium has **exclusive use of 7.775 MHz (1618.725-1626.5 MHz)** and **shares 0.95 MHz with Globalstar**, plus a globally allocated 500 kHz simplex/ring-alert band (1626.0-1626.5 MHz) [FACT, multi-source: Wikipedia + FCC/Federal Register]. A worldwide, harmonized MSS L-band position is rare: most spectrum is licensed country-by-country, whereas Iridium's allocation is coordinated globally through the ITU and is primary worldwide on the MSS uplink. The deal materials describe it as "globally coordinated L-band spectrum" [FACT] ([PR Newswire, Jun 29 2026](https://www.prnewswire.com/news-releases/rocket-lab-to-acquire-iridium-in-historic-deal-creating-a-fully-vertically-integrated-space-powerhouse-primed-for-growth-302813075.html); [Aerospace Global News, Jun 29 2026](https://aerospaceglobalnews.com/news/rocket-lab-iridium-acquisition-space-communications/)).

**The feeder and cross-link bands (Ka-band):** Iridium uses **Ka-band** for gateway feeder links (**feeder uplink 29.1-29.3 GHz, feeder downlink 19.4-19.6 GHz**) and for the **inter-satellite cross-links at ~23 GHz** (commonly cited 22.55-23.55 GHz) [FACT, multi-source: FCC IBFS engineering statement + apollosat + eoPortal].

**The critical distinction for our study (the load-bearing point):**
- Iridium's L-band sits at **~1.6 GHz** and is **MSS (mobile-satellite service)**, a band reserved for satellite-to-terminal links. It is **not** the **terrestrial cellular low-band** (600/700/800/850/900 MHz) or lower-mid-band (PCS ~1.9 GHz, AWS ~2 GHz) that the FCC's Supplemental Coverage from Space (SCS) rules authorize for direct-to-cell, and that the corpus identifies as the only spectrum an unmodified phone can receive ([`dtc_spectrum_access.md`](../direct_communication/dtc_spectrum_access.md), COMM-313) [FACT].
- A standard 3GPP smartphone has front-end filters and power amplifiers for the cellular bands and **carries no L-band MSS radio** (nor the Iridium TDMA/FDMA/TDD waveform). So Iridium's network, by design, talks to **purpose-built Iridium terminals** (satellite phones, Certus modems, SBD/IoT transceivers like the 9603), NOT to an ordinary handset on Iridium's native L-band [FACT, corpus gate is multi-source; Iridium air-interface multi-source].
- The contrast with AST SpaceMobile / Starlink Direct-to-Cell is exact: they transmit on **terrestrial cellular low-band (~600 MHz to ~3 GHz) licensed to their MNO partners**, so an **unmodified LTE/5G phone** connects to the satellite as if it were a cell tower. They ride a carrier's terrestrial spectrum; Iridium owns its own narrowband MSS band but reaches only Iridium-specific hardware over it [FACT, multi-source].
- Iridium's newer **direct-to-device** path (Iridium NTN Direct, "Project Stardust," announced Jan 10, 2024) software-upgrades the existing 66-satellite L-band fleet to the **3GPP Release-19 NB-IoT NTN** standard so standards-based chipsets can reach Iridium's L-band. Iridium frames it explicitly as **narrowband "messaging and SOS"** for smartphones, tablets, and cars (NB-IoT), NOT broadband voice or data to phones. Testing 2025, service targeted **2026**; partners include **Nordic Semiconductor** (chipsets), **Gatehouse Satcom** (the NTN RAN NodeB), and roaming partners **Deutsche Telekom** and **Vodafone IoT**. (Iridium's earlier proprietary **Qualcomm Snapdragon Satellite** partnership, announced Jan 2023, was terminated Nov 2023 when OEMs favored standards-based satellite connectivity; Stardust is the standards-based replacement.) [FACT, multi-source: Iridium investor PR + datacenterdynamics + comsoc + CNBC]

---

## 4. Iridium Capabilities (Services)

| Service | What it is | Note for our study |
|---|---|---|
| Voice and data | Satellite phones (Iridium 9555, Extreme 9575) and data modems over L-band; Iridium GO! Wi-Fi hotspot | Narrowband, to Iridium handsets, not to ordinary phones [FACT] |
| **SBD (Short Burst Data)** | Two-way short-message IoT/M2M, ~340 bytes max per message (~5-20 s delivery) | The volume engine: ~2.0M of 2.5M subs are IoT [FACT] |
| **Certus** | L-band "broadband": Certus 9810 up to 352 kbps up / **704 kbps down**; Certus 350; Certus 100 (~88 kbps); midband 9770 (22/88 kbps) | "Broadband" only by satphone standards (peak ~704 kbps, NOT 1.4 Mbps); maritime/aviation/land mobile [FACT] |
| **Iridium NTN Direct** | 3GPP NB-IoT NTN to chipsets over L-band (Project Stardust, announced Jan 2024), 2026 target | Narrowband IoT/SOS messaging, NOT broadband cellular to phones [FACT] |
| **Government (EMSS)** | Unlimited-use DoD airtime via the dedicated Wahiawa, Hawaii gateway | $738.5M, 7-year fixed-price Space Force contract (~$107M/yr); FY2025 gov service revenue $108.0M [FACT] |
| **Aviation (Aireon)** | Space-based ADS-B aircraft surveillance (~190,000 flights/day), hosted on Iridium NEXT | Iridium agreed (May 14, 2026) to fully acquire Aireon (~$520M for the ~61% it did not own) [FACT] |

Markets served: **maritime, aviation, land-mobile, IoT/M2M, and government/defense** [FACT].

**Certus note (correction):** the often-quoted "~1.4 Mbps" Certus figure is outdated; Iridium's current published peak is **704 kbps receive / 352 kbps transmit** (Certus 9810), with three simultaneous voice lines [FACT, multi-source: iridium.com product pages + Blue Sky Network + SkyTrac]. This keeps Certus firmly in the satphone "broadband" tier, two to three orders of magnitude below terrestrial broadband.

**Government detail:** the EMSS contract is a **seven-year, $738.5M fixed-price airtime** deal with the U.S. Space Force (signed Sep 2019), providing unlimited-use airtime for DoD and federal subscribers, at a fixed annual rate stepping to **$110.5M** in the final year (ending Sep 2026) [FACT, multi-source] ([Iridium 2025 results, Feb 12 2026](https://www.prnewswire.com/news-releases/iridium-announces-2025-results-issues-2026-outlook-302685852.html); [Iridium 10-K, FY2024, SEC](https://www.sec.gov/Archives/edgar/data/1418819/000162828025005302/irdm-20241231.htm)).

---

## 5. Iridium Business and Financials (FY2025)

All figures from Iridium's official FY2025 results (Feb 12, 2026), cross-checked against the deal materials and independent press.

| Metric (FY2025) | Value | Source tag |
|---|---|---|
| Total revenue | $871.659M | [FACT] |
| Service revenue | $633.958M | [FACT] |
| Equipment revenue | $81.109M | [FACT] |
| Engineering and support revenue | $156.592M | [FACT] |
| Operational EBITDA (OEBITDA) | $495.330M | [FACT] |
| OEBITDA margin | 56.8% | [FACT] |
| Net income | $114.372M | [FACT] |
| Total billable subscribers (YE2025) | 2,537,000 | [FACT] |
| Commercial subscribers | 2,416,000 (IoT 1,998,000; voice/data 402,000; broadband 16,100) | [FACT] |
| Government subscribers | 121,000 | [FACT] |
| Net subscriber additions (2025) | 77,000 | [FACT] |
| Commercial IoT ARPU | $7.78 / mo | [FACT] |
| Commercial voice/data ARPU | $47 / mo | [FACT] |
| Commercial broadband ARPU | $259 / mo | [FACT] |
| 2026 OEBITDA guidance | $480-490M | [FACT] |

FY2025 service revenue splits by segment: Commercial Voice and Data $232.2M; Commercial IoT Data $181.4M; Commercial Broadband $50.7M; Hosted Payload and Other $61.6M; Government Service $108.0M [FACT]. FY2025 capex was $100.3M; company-stated pro forma free cash flow ~$304M; the quarterly dividend is $0.15/share [FACT / FACT-company-stated]. Latest quarter (Q1 2026): revenue $219.1M, OEBITDA $116.3M, net income $21.6M ($0.20/share), net debt $1.663B, 2,555,000 subscribers [FACT].

Sources: [Iridium "Announces 2025 Results", PR Newswire / investor.iridium.com, Feb 12 2026](https://www.prnewswire.com/news-releases/iridium-announces-2025-results-issues-2026-outlook-302685852.html); [Iridium investor relations, 2025 results, Feb 12 2026](https://investor.iridium.com/2026-02-12-Iridium-Announces-2025-Results-Issues-2026-Outlook); [Iridium Q1 2026 results, PR Newswire, Apr 22 2026](https://www.prnewswire.com/news-releases/iridium-announces-first-quarter-2026-results-302751025.html); revenue and subscriber headline corroborated by [SpaceNews, Jun 29 2026](https://spacenews.com/rocket-lab-to-acquire-iridium/) and the deal press release ([PR Newswire, Jun 29 2026](https://www.prnewswire.com/news-releases/rocket-lab-to-acquire-iridium-in-historic-deal-creating-a-fully-vertically-integrated-space-powerhouse-primed-for-growth-302813075.html), which cites $871.7M revenue, $495M OEBITDA at 57% margin, 2.55M subscribers).

**Financial profile read [DERIVED]:** Iridium is a **profitable, high-margin, cash-generative** satcom operator (a 56.8% OEBITDA margin on ~$872M revenue, ~78% if measured against service revenue as Iridium frames it; ~$304M free cash flow), with subscriber growth driven overwhelmingly by **low-ARPU IoT** ($7.78/mo) at huge volume rather than by high-ARPU voice. The government EMSS line (~$108M/yr) is a stable, high-credit anchor. This is structurally different from a speculative pre-revenue constellation: it throws off cash today.

**Ownership before the deal [FACT]:** Iridium was a widely held public company (Nasdaq: IRDM) with no single controlling shareholder (directors collectively held ~1.6%), having emerged from the 1999 Motorola-era bankruptcy and relisted via the GHL Acquisition SPAC in 2009. Pre-deal market cap ~$4.6-5.5B; pre-deal enterprise value ~$7.1B ([Macrotrends IRDM, Jun 2026](https://www.macrotrends.net/stocks/charts/IRDM/iridium-communications-inc/market-cap); [stockanalysis IRDM, Jun 2026](https://stockanalysis.com/stocks/irdm/market-cap/)).

---

## 6. Implications for the RKLB Cellular Thesis (Factual Hooks, No Verdict)

This section states what owning Iridium **does** and **does not** give the direct-to-cell thesis. It draws no conclusion about whether Rocket Lab should pursue D2C; it supplies the factual hooks for that re-assessment.

### 6.1 What owning Iridium WOULD give (the hooks)

1. **An operating constellation and the operate-it muscle.** Rocket Lab already designs, builds, and launches; Iridium adds **running a live, safety-of-life global network** (66 sats, mesh cross-links, gateways, NOC). The build-vs-buy on "stand up a constellation" shifts: one side of it is now owned and operating [FACT].
2. **A spectrum position Rocket Lab OWNS, not rents.** A **globally coordinated L-band MSS** allocation (~10.5 MHz at ~1.6 GHz) is a rare worldwide asset. The corpus's spectrum-access doc frames an entrant's choices as "lease an MNO's band (SCS) or buy a distressed MSS block for billions"; this deal makes Rocket Lab an **MSS spectrum holder** outright [FACT, corpus COMM-313 / COMM-141..154].
3. **Ground infrastructure in-house.** Gateways, the dedicated DoD gateway, teleport, and network operations come with the company [FACT].
4. **A real, paying, diversified customer base.** ~2.5M subscribers across **government/defense (EMSS), maritime, aviation, IoT** (plus the Aireon ADS-B relationship). This is revenue and distribution from day one, not a market to be built [FACT].
5. **An NTN / direct-to-device standards foothold.** Iridium's **NB-IoT NTN (Project Stardust)** path is already in motion, giving Rocket Lab a standards-based direct-to-device program (narrowband) and the regulatory/standards relationships that go with it [FACT].
6. **A build-vs-buy datapoint on spectrum value.** ~$8.0B EV buys a profitable, spectrum-holding, constellation-operating company, against the corpus's **~$32-46B (100 MHz) to ~$65-90B (200 MHz) spectrum-ONLY** cost for an owned competitive cellular position (COMM-245, COMM-246), and against the EchoStar ~$17B / ~65 MHz D2D-spectrum precedent (COMM-141..154). The comparison is not apples-to-apples (L-band MSS is not cellular low-band; see 6.2), but it reframes "what does a real spectrum-plus-constellation asset cost" [DERIVED].

### 6.2 What it does NOT give (the non-hooks, load-bearing)

1. **It does NOT give cellular low-band.** Iridium's spectrum is **L-band MSS at ~1.6 GHz**, not the **600 MHz to ~2 GHz terrestrial cellular** bands that the SCS rules authorize and that an unmodified phone can receive ([`dtc_spectrum_access.md`](../direct_communication/dtc_spectrum_access.md), COMM-313) [FACT].
2. **It does NOT give direct-to-UNMODIFIED-PHONE capability.** A standard 3GPP handset has **no L-band MSS radio**, so Iridium's L-band cannot reach an ordinary phone on its native band. Iridium serves **purpose-built terminals**; AST/Starlink D2C serves **existing phones** by leasing a **partner MNO's terrestrial cellular** spectrum. Owning Iridium does not collapse that gap [FACT].
3. **It does NOT give broadband-to-phone.** Iridium's direct-to-device is **narrowband NB-IoT NTN** (messaging, SOS), not the broadband cellular voice/data the D2C thesis models. Certus "broadband" is hundreds-of-kbps-class to purpose-built modems, not phone-grade cellular data [FACT].
4. **It does NOT remove the partner-MNO question.** A broadband direct-to-cell play to ordinary phones still needs **cellular low-band**, which still comes only via an **MNO partnership (SCS lease)** or a **multi-billion cellular-spectrum purchase** (COMM-313). Iridium's L-band does not substitute for that [FACT].

### 6.3 The net factual hook (no verdict)

Owning Iridium would make Rocket Lab a **vertically integrated satcom operator with a global narrowband MSS spectrum position, a live constellation, ground, customers, and an NB-IoT NTN program**. That materially changes the "stand up a constellation and hold spectrum" side of the build-vs-buy. It does **not**, on its own, deliver the **cellular low-band, partner-MNO spectrum, or broadband-to-unmodified-phone** capability the direct-to-cell thesis is built on. The two are adjacent but distinct: Iridium is a narrowband L-band MSS network; the D2C thesis is a broadband 3GPP cellular network to ordinary phones. Whether the constellation, spectrum coordination experience, ground, and customer base de-risk a SEPARATE D2C build is the open question this doc sets up but does not answer.

---

## Open Questions

1. **Closing risk.** Mid-2027 close is conditioned on Iridium stockholder vote, HSR, **FCC transfer-of-control** of Iridium's licenses, and foreign-investment review. Iridium's DoD/EMSS role and the L-band MSS licenses make the FCC and national-security reviews non-trivial. Status: pending, no closing certainty [UNKNOWN until cleared].
2. **What Rocket Lab actually does with the L-band.** The deal materials say "leverage the spectrum for new applications" and "next-generation constellation," but give no engineering specifics. Whether the L-band gets repurposed toward any phone-reachable use (it cannot reach an unmodified handset today) is unstated [UNKNOWN].
3. **Cellular low-band acquisition, still separate.** Nothing in this deal addresses how a broadband D2C-to-phone play would obtain **cellular** spectrum (SCS partner vs purchase). That remains the COMM-313 question [UNKNOWN].
4. **NB-IoT NTN (Project Stardust) status.** Exact partners, chipset support, commercial timeline, and whether it materially overlaps the D2C IoT market need their own verification pass [partially UNKNOWN, pending].
5. **Aireon 61% stake.** Iridium's ~$520M agreement (May 2026) to take a controlling stake in Aireon adds an aviation-surveillance business to the asset; its interaction with the Rocket Lab deal terms is not detailed [UNKNOWN].

---

## Claims Ledger

Claim IDs use the next free contiguous block above the prior global max (COMM-560). Block COMM-601..COMM-624 used here. (Note: a concurrent agent was reported to be using ~COMM-561+, so this doc intentionally starts at COMM-601 to avoid collision; gaps COMM-561..600 left for that work.)

**The deal:**
- **[COMM-601]** Rocket Lab announced a definitive agreement to acquire Iridium Communications on June 29, 2026; the deal is confirmed (joint press release plus both companies' SEC filings plus major financial press). [FACT] Sources: [PR Newswire, Jun 29 2026](https://www.prnewswire.com/news-releases/rocket-lab-to-acquire-iridium-in-historic-deal-creating-a-fully-vertically-integrated-space-powerhouse-primed-for-growth-302813075.html); [SpaceNews, Jun 29 2026](https://spacenews.com/rocket-lab-to-acquire-iridium/); [CNBC, Jun 29 2026](https://www.cnbc.com/2026/06/29/rocket-lab-buys-iridium.html).
- **[COMM-602]** Price: $54.00 per Iridium share, cash-and-stock, $27.00 cash plus RKLB stock, enterprise value ~$8.0 billion. [FACT] Sources: [PR Newswire, Jun 29 2026](https://www.prnewswire.com/news-releases/rocket-lab-to-acquire-iridium-in-historic-deal-creating-a-fully-vertically-integrated-space-powerhouse-primed-for-growth-302813075.html); [StockTitan 8-K, Jun 29 2026](https://www.stocktitan.net/sec-filings/RKLB/8-k-rocket-lab-corp-reports-material-event-45990394fdac.html).
- **[COMM-603]** ~24% premium over Iridium's June 26, 2026 close of $43.52 (54.00/43.52 - 1 = 24.1%). [FACT / DERIVED] Sources: [Yahoo Finance, Jun 29 2026](https://finance.yahoo.com/markets/stocks/articles/rocket-lab-acquires-iridium-8-123239082.html); [Macrotrends IRDM, Jun 2026](https://www.macrotrends.net/stocks/charts/IRDM/iridium-communications-inc/market-cap).
- **[COMM-604]** Stock-half exchange-ratio collar: RKLB $67.50 to $112.50 (ratio 0.4000 to 0.2400). [FACT] Source: [StockTitan 8-K, Jun 29 2026](https://www.stocktitan.net/sec-filings/RKLB/8-k-rocket-lab-corp-reports-material-event-45990394fdac.html).
- **[COMM-605]** $3.6B 364-day senior secured bridge term loan from Deutsche Bank and Wells Fargo. [FACT] Sources: [StockTitan 8-K, Jun 29 2026](https://www.stocktitan.net/sec-filings/RKLB/8-k-rocket-lab-corp-reports-material-event-45990394fdac.html); [PR Newswire, Jun 29 2026](https://www.prnewswire.com/news-releases/rocket-lab-to-acquire-iridium-in-historic-deal-creating-a-fully-vertically-integrated-space-powerhouse-primed-for-growth-302813075.html).
- **[COMM-606]** Expected close mid-2027; conditions: Iridium stockholder vote, HSR antitrust, FCC transfer-of-control of Iridium telecom authorizations, foreign-investment clearances, S-4 effectiveness, Nasdaq listing. Iridium termination fee $223.62M. Both boards unanimous; director voting agreements (~1.6%). [FACT] Source: [StockTitan 8-K, Jun 29 2026](https://www.stocktitan.net/sec-filings/RKLB/8-k-rocket-lab-corp-reports-material-event-45990394fdac.html).
- **[COMM-607]** Stated rationale is vertical integration (design, build, launch, AND operate constellations); Beck cited Iridium's "rare spectrum"; Rocket Lab plans direct-to-device (Iridium NTN), a next-gen constellation, IoT and PNT expansion, and leveraging the spectrum for defense/commercial. [FACT, single-source on quotes] Source: [PR Newswire, Jun 29 2026](https://www.prnewswire.com/news-releases/rocket-lab-to-acquire-iridium-in-historic-deal-creating-a-fully-vertically-integrated-space-powerhouse-primed-for-growth-302813075.html).

**Iridium constellation and spectrum:**
- **[COMM-608]** Iridium NEXT: 66 operational satellites plus on-orbit spares (deal coverage cites 14 on-orbit spares), Walker-Star 86.4 deg / ~780 km / 66 in 6 planes. [FACT] Sources: [SpaceNews, Jun 29 2026](https://spacenews.com/rocket-lab-to-acquire-iridium/); cross-ref corpus COMM-211/COMM-396 ([eoPortal Iridium NEXT](https://www.eoportal.org/satellite-missions/iridium-next)).
- **[COMM-609]** Distinctive Ka-band inter-satellite cross-links form a self-relaying mesh enabling pole-to-pole global coverage without a ground station under every satellite. [FACT] Source: [eoPortal Iridium NEXT](https://www.eoportal.org/satellite-missions/iridium-next); cross-ref corpus COMM-209..228.
- **[COMM-610]** Iridium NEXT built by Thales Alenia Space (prime, ELiTeBus-1000), integrated by Orbital ATK/Northrop Grumman (Gilbert, AZ), launched by SpaceX Falcon 9 across 8 missions (75 sats, Jan 2017 to Jan 2019), ~$3B program. Each satellite ~860 kg, 10-yr design / 15-yr planned life, 48-beam L-band array. [FACT, multi-source] Sources: [eoPortal Iridium NEXT](https://www.eoportal.org/satellite-missions/iridium-next); [SpaceNews "SpaceX completes Iridium Next constellation"](https://spacenews.com/spacex-completes-iridium-next-constellation/); [Gunter's Space Page Iridium-NEXT](https://space.skyrocket.de/doc_sdat/iridium-next.htm).
- **[COMM-611]** Iridium holds a globally coordinated L-band MSS user-link allocation at 1616-1626.5 MHz (10.5 MHz span; 7.775 MHz exclusive, 0.95 MHz shared with Globalstar), TDMA/FDMA/TDD (90 ms, 2.4 kbps/channel) to Iridium terminals; a rare worldwide MSS position. [FACT, multi-source] Sources: [Wikipedia Iridium satellite constellation](https://en.wikipedia.org/wiki/Iridium_satellite_constellation); [mobitex.org 1614-1626 MHz](https://www.mobitex.org/1614-1626-mhz/); [apollosat Iridium frequency bands](https://apollosat.com/iridium-satellite-frequency-bands/).
- **[COMM-612]** Iridium Ka-band: feeder downlink 19.4-19.6 GHz, feeder uplink 29.1-29.3 GHz, inter-satellite crosslinks ~23 GHz (22.55-23.55 GHz). [FACT, multi-source] Sources: [FCC IBFS Iridium NEXT engineering statement](https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf); [apollosat Iridium frequency bands](https://apollosat.com/iridium-satellite-frequency-bands/); [eoPortal Iridium NEXT](https://www.eoportal.org/satellite-missions/iridium-next).
- **[COMM-613]** CRITICAL DISTINCTION: Iridium's L-band (~1.6 GHz MSS) is NOT terrestrial cellular low-band; a standard 3GPP phone has no L-band MSS radio, so Iridium serves purpose-built terminals, NOT unmodified phones on its native band. By contrast AST/Starlink D2C use partner-MNO terrestrial cellular (~600 MHz-3 GHz) that ordinary phones already carry. [FACT] Sources: corpus gate COMM-313 ([`dtc_spectrum_access.md`](../direct_communication/dtc_spectrum_access.md)); Iridium L-band per COMM-611; [New Space Economy D2D/AST](https://newspaceeconomy.ca/2026/03/31/direct-to-device-ast-spacemobile).
- **[COMM-614]** Iridium's direct-to-device (Iridium NTN Direct / Project Stardust, announced Jan 10 2024) targets 3GPP NB-IoT NTN over L-band for narrowband IoT/SOS messaging (target 2026; partners Nordic Semiconductor, Gatehouse Satcom, Deutsche Telekom, Vodafone), NOT broadband cellular to phones; the earlier proprietary Qualcomm Snapdragon Satellite partnership (Jan 2023) was terminated Nov 2023. [FACT, multi-source] Sources: [Iridium Project Stardust PR, Jan 10 2024](https://investor.iridium.com/2024-01-10-Iridium-Unveils-Project-Stardust); [DatacenterDynamics Iridium NB-IoT D2D](https://www.datacenterdynamics.com/en/news/iridium-plans-new-direct-to-device-nb-iot-satellite-service/); [CNBC Iridium-Qualcomm end, Nov 9 2023](https://www.cnbc.com/2023/11/09/iridium-announces-end-of-qualcomm-satellite-to-phone-partnership.html).

**Iridium services, business, financials (FY2025 unless noted):**
- **[COMM-615]** FY2025 total revenue $871.659M (service $633.958M; equipment $81.109M; engineering/support $156.592M). [FACT] Sources: [Iridium 2025 results, PR Newswire, Feb 12 2026](https://www.prnewswire.com/news-releases/iridium-announces-2025-results-issues-2026-outlook-302685852.html); deal release cites $871.7M.
- **[COMM-616]** FY2025 OEBITDA $495.330M (56.8% margin); net income $114.372M. [FACT] Sources: [Iridium 2025 results, Feb 12 2026](https://www.prnewswire.com/news-releases/iridium-announces-2025-results-issues-2026-outlook-302685852.html); deal release cites ~$495M / 57%.
- **[COMM-617]** Total billable subscribers YE2025 = 2,537,000 (commercial 2,416,000: IoT 1,998,000, voice/data 402,000, broadband 16,100; government 121,000); net adds 77,000. [FACT] Sources: [Iridium 2025 results, Feb 12 2026](https://www.prnewswire.com/news-releases/iridium-announces-2025-results-issues-2026-outlook-302685852.html); deal release / [Yahoo, Jun 29 2026](https://finance.yahoo.com/markets/stocks/articles/rocket-lab-acquires-iridium-8-123239082.html) cite 2.55M.
- **[COMM-618]** ARPU: commercial IoT $7.78/mo, commercial voice/data $47/mo, commercial broadband $259/mo. [FACT] Source: [Iridium 2025 results, Feb 12 2026](https://www.prnewswire.com/news-releases/iridium-announces-2025-results-issues-2026-outlook-302685852.html).
- **[COMM-619]** Government EMSS: seven-year, $738.5M fixed-price airtime contract with U.S. Space Force (signed Sep 2019), unlimited-use DoD airtime, ~$107M/yr stepping to $110.5M in the final year (Sep 2026). [FACT] Sources: [Iridium 2025 results, Feb 12 2026](https://www.prnewswire.com/news-releases/iridium-announces-2025-results-issues-2026-outlook-302685852.html); [Iridium 10-K FY2024, SEC](https://www.sec.gov/Archives/edgar/data/1418819/000162828025005302/irdm-20241231.htm).
- **[COMM-620]** Iridium services: voice/data (sat phones), SBD short-burst-data IoT (~340-byte messages, the volume engine), Certus L-band broadband (peak 704 kbps down / 352 kbps up, Certus 9810; NOT 1.4 Mbps), Iridium NTN Direct; markets maritime, aviation, land-mobile, IoT, government. [FACT, multi-source] Sources: [Iridium Certus 9810 product page](https://www.iridium.com/products/iridium-certus-9810); [Blue Sky Network midband Certus](https://blueskynetwork.com/midband-service-class-introduced-new-iridium-certus-transceiver/); [Iridium SBD service page](https://www.iridium.com/services/iridium-sbd/).
- **[COMM-621]** Aireon space-based ADS-B aviation surveillance (~190,000 flights/day, EASA-certified) is hosted on Iridium NEXT; Iridium announced (May 14, 2026) an agreement to fully acquire Aireon (~$520M for the ~61% stake it did not already hold). [FACT, multi-source] Sources: [Aireon "Iridium to Acquire Aireon", May 14 2026](https://aireon.com/iridium-to-acquire-aireon-advancing-its-strategy-to-lead-the-future-of-aviation-safety/); [Iridium investor "to Acquire Aireon", May 14 2026](https://investor.iridium.com/2026-05-14).
- **[COMM-622]** Pre-deal ownership: Iridium was a widely held public company (Nasdaq: IRDM), no single controlling shareholder, emerged from the 1999 Motorola-era bankruptcy and relisted via the GHL Acquisition SPAC in 2009. [FACT] Sources: [Macrotrends IRDM, Jun 2026](https://www.macrotrends.net/stocks/charts/IRDM/iridium-communications-inc/market-cap); standard Iridium corporate history.
- **[COMM-623]** Pre-deal market cap ~$4.6-5.5B; pre-deal enterprise value ~$7.1B; the ~$8.0B EV is a genuine control premium. [FACT / DERIVED] Sources: [Macrotrends IRDM, Jun 2026](https://www.macrotrends.net/stocks/charts/IRDM/iridium-communications-inc/market-cap); [stockanalysis IRDM, Jun 2026](https://stockanalysis.com/stocks/irdm/market-cap/).

**Implication framing (cross-track):**
- **[COMM-624]** Owning Iridium gives Rocket Lab a constellation, a globally coordinated L-band MSS spectrum position, ground, ~2.5M customers, and an NB-IoT NTN foothold, at ~$8.0B EV vs the corpus's ~$32-90B spectrum-only cost for an owned cellular position (COMM-245/246) and the EchoStar ~$17B/~65 MHz precedent (COMM-141..154); but it does NOT give cellular low-band, partner-MNO spectrum, or broadband-to-unmodified-phone capability (COMM-313, COMM-613). [DERIVED, framing; component facts FACT] Sources: this doc COMM-601..623; corpus COMM-313, COMM-245, COMM-246, COMM-141..154.

---

*Provenance: deal terms from the joint press release and both companies' SEC 8-K/425 filings (June 29, 2026), cross-checked against CNBC, SpaceNews, Yahoo Finance, and StockTitan. Iridium financials from Iridium's official FY2025 results (February 12, 2026) and FY2024 10-K. Constellation geometry cross-validated against the project corpus (COMM-209..228, COMM-380..405). The L-band-vs-cellular distinction rests on the corpus spectrum-access gate (COMM-313). No verdict rendered.*
