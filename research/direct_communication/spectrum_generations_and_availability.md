# Spectrum: the Cellular Generations, Refarming, Availability, and the Capacity Limit

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:**
- [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md): what spectrum is and why it is scarce, the speed-vs-connections (Shannon-plus-propagation) tradeoff, the low/mid/mmWave band tiers, the real US and European auction dollar figures (C-band $80.9B at ~$0.94/MHz-POP, mmWave near a floor), who holds which US tier, and the verdict that buying terrestrial cellular spectrum outright is closed to a new entrant. This doc does not re-derive those; it cites them.
- [`bands_and_enabling_hardware.md`](bands_and_enabling_hardware.md): the band ladder above Ka (V/E/W/sub-THz/optical) and the enabling silicon. This doc does not repeat the upper-band hardware mapping.

**The NEW contribution here** is four things those docs do not cover: (1) what a cellular "generation" actually is (a standard and a capability set, not a frequency) and why "5G = 5 GHz" is wrong; (2) whether the *same* spectrum carries one generation to the next (refarming and dynamic spectrum sharing) and how fixed allocations really are; (3) what is left for 5G now and 6G next (FR3 / 7 to 15 GHz, WRC-27); and (4) the capacity-gating math: users-per-MHz, how terrestrial scales past Shannon by reuse and small cells while a satellite beam cannot, and the **buy-vs-partner** spectrum-access question for a space entrant (AST with AT&T/Verizon, Starlink with T-Mobile), the single most decision-relevant finding for the model.

---

## Summary / Verdict

**The "G" is a generation: a set of standards and capabilities, not a number of gigahertz.** Each generation is defined by an ITU requirements vision (IMT-2000 for 3G, IMT-Advanced for 4G, IMT-2020 for 5G) and realized by a 3GPP radio technology (UMTS, LTE, NR), not by a frequency [FACT, see Section 1]. "5G means a 5 GHz band" is a myth: 5G NR is standardized across roughly **67 bands in FR1 (410 MHz to 7.125 GHz) and 11 in FR2 (24.25 to 71 GHz)** as of 3GPP Release 18, spanning everything from 600 MHz low-band to 39 GHz mmWave [FACT]. 5G has nothing to do with the 5 GHz Wi-Fi band, which is a separate, unlicensed, non-interoperable thing [FACT].

**The same spectrum often does carry forward, but with a cost and a limit.** A band can be refarmed from an old generation to a new one two ways: hard refarming (clear all the old users off, then turn the band on for the new generation: slow, takes years) or dynamic spectrum sharing (DSS), a software feature that lets 4G LTE and 5G NR share the *same* channel millisecond-by-millisecond, so 5G launches with no hard clear-out [FACT]. DSS carries a real efficiency tax (roughly 15 to 25% overhead) and US carriers have largely *sunset* it in favor of dedicated 5G channels once they could afford to clear the band [FACT]. The deeper point for the model: a *radio standard* is portable across a band, but a *band* is still an exclusive, government-granted, single-occupant license. Allocations are quite fixed; refarming changes the air interface on a band you already hold, it does not create new spectrum.

**What is left:** for 5G, the prime mid-band (3.3 to 3.8 GHz core, plus 2.5 GHz and the contested 6 GHz) is largely identified and, in the US, already auctioned and owned (see [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md)). The next greenfield is the **upper mid-band, FR3, 7.125 to 24.25 GHz**, with WRC-23 having teed up **4.4 to 4.8, 7.125 to 8.4, and 14.8 to 15.35 GHz** as IMT study bands for identification at **WRC-27**; the 7 to 15 GHz range is the consensus "golden band" for early 6G because it can offer >400 MHz per operator versus ~100 MHz in today's mid-band [FACT, Section 3].

**The capacity limit is the heart of the matter, and it cuts hard against satellite.** Shannon caps a single channel at `capacity = bandwidth x log2(1 + SNR)` (the equation is in [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md)). Terrestrial networks beat that per-channel cap *not* by breaking Shannon but by **reusing the same MHz in cell after cell** (frequency reuse) and by **shrinking cells** (small-cell densification), which multiplies area capacity roughly linearly with cell count [FACT]. A modern mid-band macro with massive MIMO already delivers ~7.5 to 9 bps/Hz in typical use and 50+ bps/Hz in a 16-layer demo [FACT]. A satellite beam cannot do this: one LEO direct-to-cell beam is **tens of kilometers wide (roughly 50 to 80 km)** and shares one channel across that whole footprint [FACT], versus a terrestrial cell a few kilometers across, so the same megahertz that a satellite spends once over a ~4,000 km² beam is spent ~100+ times over by terrestrial cells in the same area [DERIVED]. The result, measured: Starlink Direct-to-Cell delivers about **3.1 Mbps per beam at ~0.52 to 0.61 bps/Hz** today on a 2x5 MHz channel [FACT]; AST SpaceMobile's next-gen BlueBird targets **up to 120 Mbps per cell on 40 MHz** across ~5,600 US cells [FACT]. Converting to area capacity, terrestrial mid-band delivers on the order of **30x to many-thousand-x more bits/s per km²** than direct-to-cell satellite [DERIVED, Section 4]. **Satellite direct-to-cell is therefore a coverage/fill-in layer, not a capacity layer**, exactly because a beam is Shannon-and-footprint-gated and cannot densify.

**Buy or partner? Overwhelmingly partner, with a deep-pocketed exception.** The two leading direct-to-cell entrants both reach phones by **using a terrestrial carrier's licensed low/mid-band spectrum under the FCC's Supplemental Coverage from Space (SCS) framework**, via a spectrum *lease*, not by buying their own cellular band:
- **AST SpaceMobile** operates on **AT&T's and Verizon's 850 MHz** (plus FirstNet Band 14 at 700 MHz) under SCS, coordinated as a gap-filler to the carriers' networks; the partnerships are commercial agreements (Verizon a $100M commitment, AST also holding ~45 MHz of its own L-band MSS spectrum) [FACT].
- **Starlink Direct-to-Cell** operates on **T-Mobile's PCS G-block (1910 to 1915 MHz up, 1990 to 1995 MHz down)** under SCS, explicitly "pursuant to a lease arrangement with T-Mobile" per the FCC grant [FACT].

The exception that proves the rule: SpaceX is *also* buying spectrum outright for its next-gen direct-to-cell system, agreeing to acquire **EchoStar's AWS-4 and H-block licenses for ~$17 billion** (cash plus stock) and its AWS-3 portfolio for ~$2.6 billion more [FACT]. That is a SpaceX-scale move, not a template for a smaller entrant. **The realistic path for a new space entrant is the SCS partner/lease model: ride a carrier's existing licensed band, which also gives instant handset compatibility, rather than spending tens of billions to own cellular spectrum.** This confirms and sharpens the [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md) conclusion that the terrestrial-auction door is the wrong one to knock on.

**Confidence: medium-high.** The generation/standard definitions, the band-count debunk, the refarming/DSS mechanics, the FR3/WRC-27 roadmap, and the AST/Starlink/SCS partner structure are each carried by 2+ independent sources. The measured per-beam satellite numbers and the terrestrial massive-MIMO efficiency figures are well-sourced. The area-capacity ratios are my own [DERIVED] arithmetic from sourced inputs and are order-of-magnitude, not precise.

---

## 1. What the "G" Means: a Generation Is a Standard and a Capability, Not a Frequency

**The single most important correction.** The "G" in 2G/3G/4G/5G/6G stands for **generation**, and the number is the generation index. A generation is "a change in the nature of the system" (speed, technology, latency, capacity, architecture), not a frequency assignment ([Data Alliance - cellular wireless technologies](https://www.data-alliance.net/blog/cellular-wireless-technologies-5g-lte-4g-gsm-3g-2g-and-6g), [Commsbrief - what 1G to 5G really mean](https://commsbrief.com/what-do-the-terms-1g-2g-3g-4g-and-5g-really-mean/)).

Each generation is anchored by an **ITU requirements vision** and realized by a **3GPP radio technology**:

| Gen | ITU requirements framework | 3GPP radio technology | Defining capability (the headline requirement) |
|---|---|---|---|
| 1G | (pre-ITU-IMT) | analog (AMPS etc.) | analog voice; first cellular |
| 2G | (pre-IMT) | GSM | digital voice, SMS |
| 3G | **IMT-2000** | UMTS | 144 kbps mobile / 384 kbps pedestrian / 2 Mbps indoor [FACT] |
| 4G | **IMT-Advanced** | LTE | 100 Mbps mobile / 1 Gbps fixed [FACT] |
| 5G | **IMT-2020** (ITU-R M.2083) | NR | three usage scenarios: eMBB, URLLC, mMTC [FACT] |
| 6G | **IMT-2030** (in study) | NR-successor (TBD) | (under definition; FR3 upper mid-band central) |

Sources: 3G IMT-2000 throughput targets and 4G IMT-Advanced 1 Gbps/100 Mbps targets ([Data Alliance](https://www.data-alliance.net/blog/cellular-wireless-technologies-5g-lte-4g-gsm-3g-2g-and-6g), [Commsbrief](https://commsbrief.com/what-do-the-terms-1g-2g-3g-4g-and-5g-really-mean/)); 5G IMT-2020 / M.2083 three scenarios eMBB, URLLC, mMTC ([Data Alliance](https://www.data-alliance.net/blog/cellular-wireless-technologies-5g-lte-4g-gsm-3g-2g-and-6g), and the eMBB/URLLC/mMTC trio is also documented in [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md) citing Verizon and Cambridge Wireless).

The key fact: **the cellular technologies GSM, UMTS, LTE and NR enable 2G, 3G, 4G and 5G respectively** ([Data Alliance](https://www.data-alliance.net/blog/cellular-wireless-technologies-5g-lte-4g-gsm-3g-2g-and-6g)). A generation is the *standard plus the capability bar*, not a band.

### 1.1 Debunking "5G means a 5 GHz band"

This is a common myth and it is simply false. **5G does not refer to any specific frequency.** 5G NR is standardized across a huge swath of spectrum:

- 3GPP defines every 5G NR band in **TS 38.101-1 (FR1, 410 MHz to 7.125 GHz)** and **TS 38.101-2 (FR2, 24.25 to 71 GHz)**. As of **Release 18 (2024) there are roughly 67 bands in FR1 and 11 in FR2** [FACT] ([Wikipedia - 5G NR frequency bands](https://en.wikipedia.org/wiki/5G_NR_frequency_bands), [RF Page - LTE and 5G NR bands](https://www.rfpage.com/lte-and-5g-nr-frequency-bands-explained/)).
- Real 5G runs on **low-band (n5 850 MHz, n71 600 MHz, n28 700 MHz), mid-band (n77/n78 C-band ~3.3 to 4.2 GHz, n41 2.5 GHz, n79 4.4 to 5.0 GHz), and mmWave (n257/n258/n260/n261 at 24/28/37/39 GHz)** [FACT] ([Wikipedia - 5G NR frequency bands](https://en.wikipedia.org/wiki/5G_NR_frequency_bands)). This is the same low/mid/high tiering documented in [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md).
- 5G "operates at various frequency bands, including sub-6 GHz spectrum as well as mmWave frequencies above 24 GHz" ([Arrow - 5G vs 5GHz](https://www.arrow.com/en/research-and-events/articles/5g-vs-5ghz-differences), [Allconnect - 5G vs 5 Gbps vs 5 GHz](https://www.allconnect.com/blog/5g-5-gbps-5-ghz)).

Three different things are routinely confused, and the confusion is worth stating plainly for the model's audience ([Lumos - 5G vs 5 Gig vs 5 GHz](https://www.lumosfiber.com/blog/2024/02/20/5g-vs-5-gig-vs-5-ghz/), [Allconnect](https://www.allconnect.com/blog/5g-5-gbps-5-ghz)):

| Term | What it is | Relation to cellular 5G |
|---|---|---|
| **5G** | fifth-generation cellular standard (NR) | the actual thing; spans ~600 MHz to 39 GHz |
| **5 Gbps** | a data *speed* (5 gigabits/sec) | a throughput number, often a fiber/marketing figure |
| **5 GHz** | a *Wi-Fi frequency band* (~5 GHz, unlicensed) | unrelated; different radios/chipsets; not interoperable with cellular 5G at any level [FACT] |

5 GHz Wi-Fi and 5G cellular "cannot intercommunicate; they don't use the same radios or chipsets and they aren't interoperable at any level or in any way" ([Peplink - is a 5 GHz router the same as 5G](https://www.peplink.com/resources/5g-routers/is-a-5ghz-router-the-same-as-5g/), [Two River Computer](https://www.tworivercomputer.com/can-someone-explain-5g/)).

**One-line takeaway for the model:** when this work says "RF is the spine" and talks about bands, the generation label (4G/5G/6G) tells you the *air interface and capability*, and the band label (n5, n77, FR3) tells you the *frequency*. They are orthogonal. A direct-to-cell satellite can speak 4G LTE or 5G NR (a standards choice) over whatever band it leases from a carrier (a frequency choice).

---

## 2. Can the Same Spectrum Carry One Generation to the Next? Refarming and DSS

**Yes, a band can be re-used by a newer generation, and this happens constantly, but it does not create new spectrum and it is not free.** There are two mechanisms.

### 2.1 Hard refarming (clear it, then re-light it)

"Spectrum refarming is done by draining all previous-generation users from a frequency band and reutilizing the same band for the next generation; it is generally a slow process that can take many years" ([Tweet4Technology - DSS](https://tweet4technology.blogspot.com/2023/04/dynamic-spectrum-sharing-dss.html), [Celona - DSS](https://www.celona.io/5g-lan/dynamic-spectrum-sharing-how-it-works-why-it-matters)). This is how 2G/3G bands (850, 1900 MHz, AWS) get turned into 4G and then 5G: migrate the old traffic off, shut the old carrier down, stand the new one up. Slow because you cannot strand existing customers.

### 2.2 Dynamic Spectrum Sharing (DSS): the soft path

DSS is a **software feature that lets 4G LTE and 5G NR occupy the same channel simultaneously**, allocating resources between them dynamically (at ~1 ms LTE-subframe granularity) based on demand ([Devopedia - 5G DSS](https://devopedia.org/5g-dynamic-spectrum-sharing), [Samsung - DSS white paper](https://images.samsung.com/is/content/samsung/assets/global/business/networks/insights/white-papers/0122_dynamic-spectrum-sharing/Dynamic-Spectrum-Sharing-Technical-White-Paper-Public.pdf)). The advantage: "an existing LTE carrier can operate 5G NR and LTE simultaneously with a simple software upgrade, eliminating the need for dedicated spectrum refarming" ([Celona](https://www.celona.io/5g-lan/dynamic-spectrum-sharing-how-it-works-why-it-matters), [Nokia - DSS](https://www.nokia.com/thought-leadership/articles/dynamic-spectrum-sharing-could-be-5g-solution-wireless-operators-looking-for/)). It is how Verizon and AT&T launched nationwide 5G fast, on day one, without waiting to clear bands.

**The cost and the reversal (the nuance that matters):**
- DSS carries an overhead penalty: it "slightly impacts the performance of both 4G LTE and 5G NR by approximately 25% and 15% respectively" [FACT, single-source] ([Tweet4Technology - DSS](https://tweet4technology.blogspot.com/2023/04/dynamic-spectrum-sharing-dss.html)).
- US carriers used DSS as a *bridge* and have been **sunsetting it** as they cleared bands for dedicated 5G. Verizon deployed DSS across ~2,700 cities for "5G Nationwide," mostly on 850 MHz 10 MHz channels; **AT&T shuttered most of its DSS during 2021** and flipped its 850 MHz to a dedicated 5G channel instead [FACT] ([Fierce Network - Verizon relies on DSS more than AT&T](https://www.fierce-network.com/operators/verizon-relies-dynamic-spectrum-sharing-more-widely-than-at-t-report), [Light Reading - the quiet sunset of DSS](https://www.lightreading.com/5g/the-quiet-sunset-of-5g-dynamic-spectrum-sharing)).

### 2.3 How fixed are allocations, really?

The honest answer for the model: **the air interface on a band is flexible; the band's ownership and its service allocation are not.**

- **Flexible:** which generation runs on a band you already hold. Refarming and DSS let a license-holder move a band from 3G to 4G to 5G, even run two generations at once, by software and traffic migration. A new generation reuses old spectrum routinely.
- **Fixed:** the license itself. A band is still an exclusive, single-occupant, government-granted right (Section 1 and 6 of [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md)). Refarming does not let two operators share a band, and it does not conjure new bandwidth: total Shannon capacity of the band is unchanged by which generation uses it. Reallocating a band from one *service* to another (satellite to mobile, as with C-band) is the slow, political, years-long process documented in [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md), not a refarming software toggle.

**Implication for a space entrant:** refarming is why an SCS partner can let a satellite ride a band the carrier currently uses for 4G or 5G, and why the satellite can speak whichever standard the partner's handsets expect. But it does not give the entrant a *new* band; the entrant still rides someone's existing exclusive license (Section 5).

---

## 3. What Is Allocated vs Open vs Being-Opened: What Is Left for 5G Now and 6G Next

This extends the band-tier and "who holds it" picture in [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md) with the *forward* allocation pipeline, which that doc flagged as an open question.

### 3.1 What is left for 5G now

- **Low-band and the core mid-band are essentially allocated and (in the US) owned.** 600/700/850 MHz low-band and the 2.5 GHz, 3.45 GHz, and C-band (3.7 to 3.98 GHz) mid-band were auctioned and are held by T-Mobile/Verizon/AT&T (full ownership table in [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md)). Globally, WRC-23 harmonized the core 5G mid-band **3.3 to 3.8 GHz** (3300 to 3400 MHz identified for IMT in Regions 1 and 2; 3600 to 3800 MHz in Region 2) [FACT] ([CTU - WRC-23 outcome for mobile/IMT](https://ctu.int/wp-content/uploads/2024/02/WRC-23-outcome-for-Mobile-service-and-IMT.pdf), [FedSoc - what happened at the WRC](https://fedsoc.org/commentary/fedsoc-blog/what-happened-at-the-world-radiocommunication-conference)).
- **The contested frontier within reach of 5G is 6 GHz (5.925 to 7.125 GHz).** WRC-23 identified the **upper 6 GHz (6425 to 7125 MHz)** for IMT in Region 1 (and parts of Region 3, plus Mexico and Brazil in the Americas), but it is shared/contested with Wi-Fi/RLAN use, which is why [`bands_and_enabling_hardware.md`](bands_and_enabling_hardware.md) calls it "the unresolved battle for 6 GHz" [FACT] ([CTU - WRC-23 outcome](https://ctu.int/wp-content/uploads/2024/02/WRC-23-outcome-for-Mobile-service-and-IMT.pdf), [IIC Intermedia - WRC-23 and the battle for 6 GHz](https://iicintermedia.org/vol-52-issue-1/wrc-23-and-the-unresolved-battle-for-6-ghz/)).
- **Net:** there is little unencumbered greenfield left *below ~7 GHz*. The remaining 5G headroom is mostly capacity-side (densification, massive MIMO, mmWave hotspots), not new clean bands.

### 3.2 What is being opened for 6G next: FR3, the 7 to 15 GHz "golden band"

The next greenfield is the **upper mid-band**, christened **FR3 (7.125 to 24.25 GHz)** in 3GPP, sitting between today's FR1 (410 MHz to 7.125 GHz) and FR2 mmWave (24.25 to 71 GHz) [FACT] ([Samsung Research - upper mid-band for 6G](https://research.samsung.com/blog/Upper-Mid-Band-Spectrum-for-6G-Opportunities-and-Key-Enablers), [Nokia - 6G mid-band spectrum](https://www.nokia.com/6g/6g-mid-band-spectrum-technology-explained/)).

- **WRC-23 agreed the IMT study bands for identification at WRC-27**, the bands "mainly considered for 6G": **4.4 to 4.8 GHz, 7.125 to 8.4 GHz, and 14.8 to 15.35 GHz** [FACT] ([Samsung Research](https://research.samsung.com/blog/Upper-Mid-Band-Spectrum-for-6G-Opportunities-and-Key-Enablers), [Enterprise IT World - decoding the 6G spectrum landscape](https://www.enterpriseitworld.com/decoding-the-spectrum-landscape-of-6g/)).
- **Why FR3 is the prize:** the **7 to 15 GHz** range is the "most likely candidate for initial 6G deployments" and is called "golden spectrum" because it balances capacity and coverage, and crucially it can offer **>400 MHz per operator versus ~100 MHz in FR1** [FACT] ([Nokia - 6G mid-band](https://www.nokia.com/6g/6g-mid-band-spectrum-technology-explained/), [BackITapp - FR3 the new mmWave](https://consulting.backitapp.com/spectrum-for-6g/fr3/)). That is the same speed-vs-connections logic from [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md): climb in frequency to find room for wide channels, paid for in reach and harder hardware.
- **Status: study/identification, not yet auctioned.** These are WRC-27 candidate bands under further study; nobody owns FR3 for IMT yet. That makes FR3 the one place where the "all the good spectrum is already filed" wall is *not yet* built, the forward-looking opening this ten-years-out model cares about.

**For the model's timeline:** today (5G era) the usable cellular spectrum is owned and a space entrant must partner (Section 5). The next opening (FR3 / 6G, ~2027 to 2030+) is a genuine greenfield, but it is upper mid-band (7 to 15 GHz), which is harder for a wide-footprint satellite beam (narrower beams, more path loss) and is being shaped now in the WRC-27 cycle.

---

## 4. The Capacity Limit: Shannon, Users-per-MHz, and Why a Satellite Beam Is Gated

The Shannon relation `capacity = bandwidth x log2(1 + SNR)` is stated and sourced in [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md). This section does the thing that doc flagged as missing: turn it into **users-per-MHz and area-capacity**, and show the structural reason a satellite beam cannot keep up with the ground.

### 4.1 The per-channel ceiling (what one slice of spectrum can carry)

Shannon caps a *single channel in a single place*. Practical spectral efficiency per channel:

- **4G LTE:** ~1.5 bps/Hz average ([Techplayon - spectral efficiency](https://www.techplayon.com/spectral-efficiency-5g-nr-and-4g-lte/), [5G-networks.net](https://www.5g-networks.net/spectral-efficiency-5g-nr-and-4g-lte-compared/)).
- **5G NR (single-stream):** ~3 bps/Hz typical, with a higher peak ([Techplayon](https://www.techplayon.com/spectral-efficiency-5g-nr-and-4g-lte/), [Telcoma - 5G spectral efficiency](https://www.telcomaglobal.com/p/5g-spectral-efficiency)).
- **5G with massive MIMO (multi-user, spatial multiplexing):** this is how the ground gets far past the single-stream cap *without* breaking Shannon, by sending many parallel spatial streams. T-Mobile in real 2.5 GHz deployment reports **~7.5 to 9.0 bps/Hz** (vs 2.5 to 3.0 for its 4G), and in a 16-layer MU-MIMO demo with a 64-antenna radio hit **5.6 Gbps on one 100 MHz channel, ~50+ bps/Hz** [FACT] ([Light Reading - T-Mobile/Ericsson 5.6 Gbit/s](https://www.lightreading.com/5g/t-mobile-ericsson-squeeze-56-gbits-out-of-5g-in-25ghz/d/d-id/763817), [Fierce Network - T-Mobile MU-MIMO demo](https://www.fierce-network.com/tech/t-mobile-pulls-more-out-2-5-ghz-mu-mimo-5g-demo-ericsson), [T-Mobile newsroom - MU-MIMO](https://www.t-mobile.com/news/network/t-mobile-achieves-mind-blowing-5g-speeds-with-mu-mimo)).
- **The MIMO "beyond Shannon" caveat:** the record ~145.6 bps/Hz figure (176 bps/Hz raw, 17% lost) only *appears* to beat Shannon because it uses ~128 antennas in parallel; each spatial stream still obeys Shannon [FACT, single-source] ([Wireless Future blog - how much does massive MIMO improve SE](https://ma-mimo.ellintech.se/2016/10/18/how-much-does-massive-mimo-improve-spectral-efficiency/)). The honest ceiling per *stream* is single-digit bps/Hz; MIMO multiplies streams, it does not repeal Shannon.

### 4.2 Users-per-MHz: it is the spatial reuse, not the channel, that scales

A single channel's bits/s is fixed by Shannon, so **"users per MHz" is meaningless without saying over what area**. The terrestrial trick is to **reuse the same MHz in every cell**:

- **Frequency reuse:** in a reuse-1 network "the number of users per unit area increases linearly with the number of cells" because each cell re-uses the whole band; cell densification directly multiplies throughput [FACT] ([arXiv - ultra-dense small cells](https://arxiv.org/pdf/1503.03912), [ScienceDirect - frequency reuse overview](https://www.sciencedirect.com/topics/computer-science/frequency-reuse)).
- **Small-cell densification:** "network densification has the potential to linearly increase network capacity with the number of deployed cells" (cell-splitting gain), and smaller cells also give each user a larger share of the band and lower path loss [FACT] ([arXiv - small cell densification](https://arxiv.org/pdf/1503.03912), [researchgate - small cells in HetNets](https://www.researchgate.net/publication/265911120_Small_Cells_in_Cellular_Networks_Challenges_of_Future_HetNets)).
- **The concrete consequence:** the *same* 100 MHz that yields ~750 Mbps in one macro cell (at ~7.5 bps/Hz) yields ~750 Mbps **per cell, in every cell**. Put 100 cells over a city and you have ~75 Gbps of area capacity from 100 MHz. That is how terrestrial serves millions: it spends each MHz over and over in space.

So "users-per-MHz" for terrestrial is effectively **unbounded in principle**: keep adding cells and you keep multiplying capacity from the same megahertz (until interference and cost bite). The 5G IMT-2020 target codifies the extreme of this: **1,000,000 devices per km²** for mMTC (cited in [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md)), reachable precisely because of dense reuse.

### 4.3 Why a satellite beam is capacity-gated (the crux)

A satellite cannot densify. Its "cell" is a beam footprint set by orbit altitude and antenna size, and it is **enormous** compared to a terrestrial cell:

- A **LEO direct-to-cell beam is roughly 50 to 80 km wide** (spot beams "at least 50 to 80 km wide"; LEO at ~600 km can range 50 to 1000 km) [FACT] ([techneconomyblog - LEO satellites](https://techneconomyblog.com/category/leo-satellites/)). For AST-class systems, a ~1,660 km footprint is tiled into ~725 hexagonal cells each ~**78.7 km across** [FACT, single-source] ([NewSpaceTracker - direct-to-smartphone satellites](https://newspacetracker.com/articles/direct-to-smartphone-satellites/)).
- A **terrestrial macro cell is ~1.6 to 5 km radius** (low/mid-band) [FACT] ([Dgtl Infra - cell tower range](https://dgtlinfra.com/cell-tower-range-how-far-reach/), and cell radii are consistent with [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md)).
- Satellites *do* reuse frequency across beams (beam isolation by angular separation and sidelobe control, e.g. southern England and northern Scotland on the same channel) [FACT] ([techneconomyblog](https://techneconomyblog.com/category/leo-satellites/)), but the reuse count is set by how many ~50 to 80 km beams the satellite can form, **orders of magnitude fewer than terrestrial cells over the same ground**, and the satellite cannot add beams by building towers.

**The measured per-beam reality (the numbers that anchor the model):**

| System | Channel | Per-beam/per-cell capacity | Spectral efficiency | Cell size | Source |
|---|---|---|---|---|---|
| **Starlink Direct-to-Cell** (now, SMS/early data) | 2x5 MHz PCS G-block | **~3.1 Mbps/beam** (median; up to ~18.6 Mbps if all spectrum aggregated) | **~0.52 to 0.61 bps/Hz** | ~tens of km | [arXiv 2506.00283](https://arxiv.org/html/2506.00283v7) |
| **AST SpaceMobile** next-gen BlueBird (target) | up to 40 MHz/cell | **up to 120 Mbps/cell**, ~5,600 US cells, 10 GHz total processing | ~3 bps/Hz peak (120 Mbps / 40 MHz) [DERIVED] | ~78.7 km | [AST SpaceMobile network](https://ast-science.com/spacemobile-network/), [AST next-gen BlueBird](https://ast-science.com/next-gen-bluebird/) |
| **Terrestrial 5G mid-band macro** (massive MIMO) | 100 MHz | **~750 Mbps to 5.6 Gbps/cell** | **~7.5 to 50+ bps/Hz** | ~1.6 to 5 km | [Light Reading](https://www.lightreading.com/5g/t-mobile-ericsson-squeeze-56-gbits-out-of-5g-in-25ghz/d/d-id/763817), [T-Mobile](https://www.t-mobile.com/news/network/t-mobile-achieves-mind-blowing-5g-speeds-with-mu-mimo) |

Note Starlink's ~0.52 bps/Hz is **lower than even 4G's ~1.5 bps/Hz**, because the link operates at ~0 dB median SINR from orbit (vs ~5 dB for T-Mobile terrestrial), confirming the SNR term in Shannon is squeezed hard for a phone-to-LEO link [FACT] ([arXiv 2506.00283](https://arxiv.org/html/2506.00283v7)).

### 4.4 Area capacity: the 30x-to-thousands-x gap [DERIVED]

Normalizing to **bits/s per km²** (the apples-to-apples measure of a coverage layer's capacity), using the sourced inputs above:

- **Starlink DTC:** ~3.1 Mbps over a ~78.7 km-wide cell (~4,000 km² hexagon) ≈ **~0.0008 Mbps/km²** [DERIVED].
- **AST BlueBird:** 120 Mbps over ~5,600 US cells across ~8.08M km² CONUS (~1,440 km²/cell) ≈ **~0.083 Mbps/km²** [DERIVED].
- **Terrestrial mid-band macro:** ~750 Mbps over a ~3 km-radius cell (~28 km²) ≈ **~27 Mbps/km²** [DERIVED]; small cells push this into the hundreds-to-thousands of Mbps/km².

That is roughly **300x (vs AST) to ~30,000x (vs Starlink DTC) more area capacity for terrestrial** than direct-to-cell satellite, before terrestrial densification is even counted [DERIVED]. The ratios are order-of-magnitude, but the direction is unambiguous and structural.

**The conclusion the math forces:** a satellite beam is **capacity-gated** by Shannon-times-footprint and cannot be densified, so direct-to-cell satellite is a **coverage / dead-zone-fill layer, not a capacity layer**. This matches how the deployments are positioned: AST and Starlink DTC are sold as **supplemental** coverage where towers do not reach (Section 5), not as a replacement for terrestrial capacity. For the model: per-subscriber economics of a space layer are driven by *how many subscribers you can pack under a fixed-capacity beam*, the inverse of the terrestrial story where you add capacity by adding cells. This is the central structural asymmetry the cost-per-subscriber model must encode.

---

## 5. Ownership and Acquisition: Buy Spectrum, or Partner With a Carrier?

This is the most decision-relevant section for the model. [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md) established *who owns* terrestrial spectrum (the three US carriers) and that *buying it is closed* to a new entrant. Here is the mechanism a space entrant actually uses instead: **the FCC Supplemental Coverage from Space (SCS) framework**, under which a satellite operator **leases/uses a carrier's already-licensed band** rather than buying its own.

### 5.1 The SCS framework (the legal door)

The FCC adopted SCS in early 2024 ("Single Network Future"; rules effective May 30, 2024). It "authorizes satellite operators to partner with terrestrial wireless providers to develop hybrid satellite-terrestrial networks," with the satellite acting as a **gap-filler** using "spectrum previously allocated exclusively to terrestrial service" [FACT] ([Federal Register - Single Network Future / SCS](https://www.federalregister.gov/documents/2024/04/30/2024-06669/single-network-future-supplemental-coverage-from-space-space-innovation), [Inside Global Tech - SCS rules take effect](https://www.insideglobaltech.com/2024/04/30/fcc-acts-to-expand-satellite-to-smartphone-coverage-supplemental-coverage-from-space-rules-will-enable-partnerships-between-satellite-operators-and-wireless-network-providers-in-the/)).

The licensing rule is the key constraint: **the FCC authorizes SCS only where terrestrial licensees holding all licenses on the relevant channel across a geographically independent area lease access to their spectrum rights** [FACT] ([Federal Register - SCS](https://www.federalregister.gov/documents/2024/04/30/2024-06669/single-network-future-supplemental-coverage-from-space-space-innovation)). In plain terms: **the satellite does not get its own cellular license; it rides a carrier's license, by lease, on a cleared channel.** SCS is built on 3GPP Release 17 non-terrestrial-network specs ([US Mobile - Starlink satellite calls](https://www.usmobile.com/blog/starlink-satellite-phone-calls/)).

### 5.2 AST SpaceMobile: uses AT&T and Verizon licensed low-band

- AST "uses 850 MHz spectrum from AT&T and Verizon, plus Band 14 (700 MHz) for FirstNet," operating "a segment of both AT&T and Verizon's 850 MHz spectrum" under SCS for nationwide US coverage [FACT] ([Wikipedia - AST SpaceMobile](https://en.wikipedia.org/wiki/AST_SpaceMobile), [SDxCentral - FCC grants AST access to AT&T/Verizon spectrum](https://www.sdxcentral.com/news/fcc-grants-ast-spacemobile-access-to-att-verizon-spectrum/), [DCD - AST pairs with AT&T and Verizon](https://www.datacenterdynamics.com/en/news/ast-spacemobile-pairs-with-att-and-verizon-for-satellite-broadband/)).
- The FCC granted AST SCS authorization "in low-band frequencies between 700 MHz and 900 MHz" coordinated with "strategic partners Verizon, AT&T, and FirstNet" [FACT] ([Broadband Breakfast - FCC grants AST direct-to-cell](https://broadbandbreakfast.com/fcc-grants-ast-spacemobiles-direct-to-cell-request/), [Inside Global Tech](https://www.insideglobaltech.com/2024/04/30/fcc-acts-to-expand-satellite-to-smartphone-coverage-supplemental-coverage-from-space-rules-will-enable-partnerships-between-satellite-operators-and-wireless-network-providers-in-the/)).
- It is structured as **commercial agreements**, not a spectrum purchase: Verizon a **$100M commitment**, plus prepayments from others (stc $175M); AST additionally holds **~45 MHz of its own lower-mid-band (including ~40 MHz of L-band MSS)** [FACT] ([Wikipedia - AST SpaceMobile](https://en.wikipedia.org/wiki/AST_SpaceMobile), [Via Satellite - Verizon deepens AST ties](https://www.satellitetoday.com/connectivity/2025/10/08/verizon-deepens-ast-spacemobile-ties-with-commercial-agreement/)).

### 5.3 Starlink Direct-to-Cell: leases T-Mobile's PCS G-block

- Starlink DTC operates on **T-Mobile's mid-band PCS G-block: 1910 to 1915 MHz (Earth-to-space) and 1990 to 1995 MHz (space-to-Earth)**, a 2x5 MHz channel [FACT] ([arXiv 2506.00283](https://arxiv.org/html/2506.00283v7), [Grokipedia - Starlink Direct to Cell](https://grokipedia.com/page/Starlink_Direct_to_Cell)).
- The FCC grant is explicit that this is a **lease**: SpaceX is authorized "pursuant to a lease arrangement with T-Mobile USA, Inc.," granted Nov 26, 2024, for SCS using up to 7,500 NGSO satellites [FACT] ([FCC DA-24-1193](https://docs.fcc.gov/public/attachments/DA-24-1193A1.pdf), [Inside Global Tech - FCC authorizes SpaceX/T-Mobile SCS](https://www.insideglobaltech.com/2024/12/09/fcc-issues-filing-guidelines-for-supplemental-coverage-from-space-scs-applications-authorizes-spacex-and-t-mobile-to-premier-scs-deployment/)).
- It is a coverage/dead-zone fill service (T-Satellite launched July 2025); detailed revenue-share terms are not publicly disclosed [FACT, partial] ([DCD - T-Mobile launches nationwide satellite with Starlink](https://www.datacenterdynamics.com/en/news/t-mobile-launches-nationwide-satellite-service-with-starlink/)).

### 5.4 The exception: SpaceX is also buying spectrum outright (the EchoStar deal)

For its *next-generation* direct-to-cell system SpaceX is not only partnering, it is **buying its own cellular spectrum** at a scale only a giant can:

- **~$17 billion for EchoStar's AWS-4 and H-block licenses** (up to $8.5B cash + up to $8.5B SpaceX stock, plus ~$2B funding EchoStar interest), announced Sept 2025, "to develop and deploy a next-generation Starlink direct-to-cell constellation" [FACT] ([EchoStar 8-K / SEC](https://www.sec.gov/Archives/edgar/data/0001415404/000141540425000041/tmb-20250907xex99d1.htm), [Broadband Breakfast - SpaceX buying EchoStar spectrum for $17B](https://broadbandbreakfast.com/spacex-buying-echostar-satellite-spectrum-for-17-billion/), [PBS - SpaceX pays $17B for EchoStar spectrum](https://www.pbs.org/newshour/nation/spacex-pays-17-billion-to-acquire-spectrum-licenses-from-echostar)).
- Plus **~$2.6 billion** for EchoStar's AWS-3 portfolio (SpaceX stock), Nov 2025 [FACT] ([EchoStar 8-K Nov 2025 / SEC](https://www.sec.gov/Archives/edgar/data/0001415404/000141540425000049/tmb-20251106xex99.htm), [DCD - SpaceX acquires AWS-4 and H-block](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/)).

### 5.5 The verdict: partner/lease, not buy

| Path | Mechanism | Who does it | Cost shape | Handset compatibility |
|---|---|---|---|---|
| **Partner / lease (SCS)** | Use a carrier's existing licensed band under an SCS spectrum lease; satellite is a gap-filler | **AST** (AT&T/Verizon 850 MHz), **Starlink DTC** (T-Mobile PCS G-block) | Commercial deal / revenue share; near-zero spectrum capex | **Instant**: phones already support the band/standard |
| **Buy outright** | Acquire your own cellular licenses on the secondary market | **SpaceX next-gen** ($17B+ EchoStar AWS-4/H/AWS-3) | Tens of billions; SpaceX-scale only | Must align bands/handsets yourself |

**The realistic conclusion for a Rocket-Lab-scale entrant:** the SCS partner/lease model is the door. It avoids the tens-of-billions spectrum bill (consistent with [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md)), and it solves handset compatibility for free because the satellite speaks the carrier's existing standard on the carrier's existing band, to unmodified phones. Buying spectrum outright is what a hyperscale incumbent (SpaceX) does to remove dependence on a partner; it is not the entry path. **The spectrum question for the model is therefore not "what does a cellular band cost to buy" but "what are the commercial terms of an SCS partnership, and what fraction of a carrier's band do you get to ride."** The capacity that band delivers from orbit is then gated as in Section 4: a few Mbps to ~120 Mbps per large beam, a coverage layer, not a capacity layer.

---

## 6. What This Adds to the Model

1. **Generation vs band are orthogonal.** A direct-to-cell satellite chooses a *standard* (4G LTE or 5G NR, an air-interface decision) and rides a *band* (whatever the carrier leases it). "5G" in the model means the capability tier, never a frequency.
2. **Refarming is portability of the air interface on a held band, not new spectrum.** It is why an SCS satellite can speak the partner's current generation on the partner's current band, but it gives the entrant no new bandwidth.
3. **The forward spectrum opening is FR3 / 7 to 15 GHz at WRC-27**, the one greenfield not yet filed; but it is upper mid-band, harder for wide satellite beams, and a decade-scale regulatory process.
4. **Capacity is the binding asymmetry.** Terrestrial scales area capacity ~linearly by reuse and densification; a satellite beam is Shannon-times-footprint gated and cannot densify. Measured: ~3.1 Mbps/beam (Starlink DTC) to ~120 Mbps/cell (AST), versus ~750 Mbps to 5.6 Gbps/cell terrestrial, i.e. ~300x to ~30,000x more bits/s/km² on the ground [DERIVED]. **Space direct-to-cell is a coverage layer; the model must price it per-subscriber under a fixed-capacity beam, not as a terrestrial-style capacity build.**
5. **Acquisition is partner-and-lease (SCS), not buy.** AST rides AT&T/Verizon 850 MHz; Starlink leases T-Mobile's PCS G-block. The realistic entrant cost is a commercial partnership, not a spectrum auction. (SpaceX's $17B EchoStar buy is the hyperscale exception, not the entry path.)

---

## 7. Sources

Generations / standards / the 5G-vs-5GHz debunk:
- [Data Alliance - Cellular Wireless Technologies: 5G, LTE/4G, GSM/3G, 2G and 6G](https://www.data-alliance.net/blog/cellular-wireless-technologies-5g-lte-4g-gsm-3g-2g-and-6g)
- [Commsbrief - What do the terms 1G, 2G, 3G, 4G and 5G really mean?](https://commsbrief.com/what-do-the-terms-1g-2g-3g-4g-and-5g-really-mean/)
- [Peplink - Is a 5 GHz Router the same as a 5G Router?](https://www.peplink.com/resources/5g-routers/is-a-5ghz-router-the-same-as-5g/)
- [Two River Computer - Can Someone Explain 5G? (5 GHz Wi-Fi vs 5G Cellular)](https://www.tworivercomputer.com/can-someone-explain-5g/)
- [Lumos - Understanding 5G, 5 Gig, and 5 GHz](https://www.lumosfiber.com/blog/2024/02/20/5g-vs-5-gig-vs-5-ghz/)
- [Allconnect - Understanding the difference between 5G, 5 Gbps and 5 GHz](https://www.allconnect.com/blog/5g-5-gbps-5-ghz)
- [Arrow - 5G vs 5 GHz: What is the Difference?](https://www.arrow.com/en/research-and-events/articles/5g-vs-5ghz-differences)

5G NR band list:
- [Wikipedia - 5G NR frequency bands](https://en.wikipedia.org/wiki/5G_NR_frequency_bands)
- [RF Page - LTE and 5G NR Frequency Bands: Complete Band List with FR1 and FR2](https://www.rfpage.com/lte-and-5g-nr-frequency-bands-explained/)

Refarming / DSS:
- [Tweet4Technology - Dynamic Spectrum Sharing: DSS](https://tweet4technology.blogspot.com/2023/04/dynamic-spectrum-sharing-dss.html)
- [Celona - Dynamic Spectrum Sharing: How It Works & Why It Matters](https://www.celona.io/5g-lan/dynamic-spectrum-sharing-how-it-works-why-it-matters)
- [Devopedia - 5G Dynamic Spectrum Sharing](https://devopedia.org/5g-dynamic-spectrum-sharing)
- [Samsung - Dynamic Spectrum Sharing Technical White Paper](https://images.samsung.com/is/content/samsung/assets/global/business/networks/insights/white-papers/0122_dynamic-spectrum-sharing/Dynamic-Spectrum-Sharing-Technical-White-Paper-Public.pdf)
- [Nokia - Dynamic spectrum sharing could be the 5G solution operators are looking for](https://www.nokia.com/thought-leadership/articles/dynamic-spectrum-sharing-could-be-5g-solution-wireless-operators-looking-for/)
- [Fierce Network - Verizon relies on DSS more widely than AT&T](https://www.fierce-network.com/operators/verizon-relies-dynamic-spectrum-sharing-more-widely-than-at-t-report)
- [Light Reading - The quiet sunset of 5G dynamic spectrum sharing](https://www.lightreading.com/5g/the-quiet-sunset-of-5g-dynamic-spectrum-sharing)

Spectrum allocation / FR3 / WRC:
- [Samsung Research - Upper Mid-Band Spectrum for 6G: Opportunities and Key Enablers](https://research.samsung.com/blog/Upper-Mid-Band-Spectrum-for-6G-Opportunities-and-Key-Enablers)
- [Nokia - 6G mid-band spectrum technology explained](https://www.nokia.com/6g/6g-mid-band-spectrum-technology-explained/)
- [BackITapp - FR3: Is the upper midband the new FR2/mmWave?](https://consulting.backitapp.com/spectrum-for-6g/fr3/)
- [Enterprise IT World - Decoding the Spectrum Landscape of 6G](https://www.enterpriseitworld.com/decoding-the-spectrum-landscape-of-6g/)
- [CTU - WRC-23 outcome for Mobile service and IMT](https://ctu.int/wp-content/uploads/2024/02/WRC-23-outcome-for-Mobile-service-and-IMT.pdf)
- [FedSoc - What Happened at the World Radiocommunication Conference?](https://fedsoc.org/commentary/fedsoc-blog/what-happened-at-the-world-radiocommunication-conference)
- [IIC Intermedia - WRC-23 and the unresolved battle for 6 GHz](https://iicintermedia.org/vol-52-issue-1/wrc-23-and-the-unresolved-battle-for-6-ghz/)

Capacity / spectral efficiency / reuse / densification:
- [Techplayon - Spectral Efficiency: 5G-NR and 4G-LTE](https://www.techplayon.com/spectral-efficiency-5g-nr-and-4g-lte/)
- [5G-networks.net - Spectral Efficiency: 5G-NR and 4G-LTE compared](https://www.5g-networks.net/spectral-efficiency-5g-nr-and-4g-lte-compared/)
- [Telcoma Global - 5G Spectral Efficiency](https://www.telcomaglobal.com/p/5g-spectral-efficiency)
- [Wikipedia - Spectral efficiency](https://en.wikipedia.org/wiki/Spectral_efficiency)
- [Wireless Future blog - How Much does Massive MIMO Improve the Spectral Efficiency?](https://ma-mimo.ellintech.se/2016/10/18/how-much-does-massive-mimo-improve-spectral-efficiency/)
- [Light Reading - T-Mobile, Ericsson squeeze 5.6 Gbit/s out of 5G in 2.5 GHz](https://www.lightreading.com/5g/t-mobile-ericsson-squeeze-56-gbits-out-of-5g-in-25ghz/d/d-id/763817)
- [Fierce Network - T-Mobile pulls more out of 2.5 GHz in MU-MIMO 5G demo](https://www.fierce-network.com/tech/t-mobile-pulls-more-out-2-5-ghz-mu-mimo-5g-demo-ericsson)
- [T-Mobile newsroom - T-Mobile Achieves Mind-Blowing 5G Speeds with MU-MIMO](https://www.t-mobile.com/news/network/t-mobile-achieves-mind-blowing-5g-speeds-with-mu-mimo)
- [arXiv 1503.03912 - Towards 1 Gbps/UE: Understanding Ultra-Dense Small Cell Deployments](https://arxiv.org/pdf/1503.03912)
- [ScienceDirect - Frequency Reuse, an overview](https://www.sciencedirect.com/topics/computer-science/frequency-reuse)
- [ResearchGate - Small Cells in Cellular Networks: Challenges of Future HetNets](https://www.researchgate.net/publication/265911120_Small_Cells_in_Cellular_Networks_Challenges_of_Future_HetNets)

Satellite direct-to-cell capacity / beam size:
- [arXiv 2506.00283 - Direct-to-Cell: A First Look into Starlink's Direct Satellite-to-Device RAN](https://arxiv.org/html/2506.00283v7)
- [AST SpaceMobile - SpaceMobile Network](https://ast-science.com/spacemobile-network/)
- [AST SpaceMobile - Next-Generation BlueBird](https://ast-science.com/next-gen-bluebird/)
- [NewSpaceTracker - Direct-to-Smartphone Satellites](https://newspacetracker.com/articles/direct-to-smartphone-satellites/)
- [techneconomyblog - LEO Satellites (spot-beam sizes, beam frequency reuse)](https://techneconomyblog.com/category/leo-satellites/)
- [Dgtl Infra - Cell Tower Range: How Far Do They Reach?](https://dgtlinfra.com/cell-tower-range-how-far-reach/)

SCS framework and the buy-vs-partner deals:
- [Federal Register - Single Network Future: Supplemental Coverage From Space](https://www.federalregister.gov/documents/2024/04/30/2024-06669/single-network-future-supplemental-coverage-from-space-space-innovation)
- [Inside Global Tech - FCC's SCS Rules Take Effect May 30](https://www.insideglobaltech.com/2024/04/30/fcc-acts-to-expand-satellite-to-smartphone-coverage-supplemental-coverage-from-space-rules-will-enable-partnerships-between-satellite-operators-and-wireless-network-providers-in-the/)
- [Inside Global Tech - FCC Authorizes SpaceX and T-Mobile to Premiere SCS](https://www.insideglobaltech.com/2024/12/09/fcc-issues-filing-guidelines-for-supplemental-coverage-from-space-scs-applications-authorizes-spacex-and-t-mobile-to-premier-scs-deployment/)
- [Wikipedia - AST SpaceMobile](https://en.wikipedia.org/wiki/AST_SpaceMobile)
- [SDxCentral - FCC grants AST SpaceMobile access to AT&T, Verizon spectrum](https://www.sdxcentral.com/news/fcc-grants-ast-spacemobile-access-to-att-verizon-spectrum/)
- [DCD - AST SpaceMobile pairs with AT&T and Verizon](https://www.datacenterdynamics.com/en/news/ast-spacemobile-pairs-with-att-and-verizon-for-satellite-broadband/)
- [Broadband Breakfast - FCC Grants AST SpaceMobile's Direct-to-Cell Request](https://broadbandbreakfast.com/fcc-grants-ast-spacemobiles-direct-to-cell-request/)
- [Via Satellite - Verizon Deepens AST SpaceMobile Ties With Commercial Agreement](https://www.satellitetoday.com/connectivity/2025/10/08/verizon-deepens-ast-spacemobile-ties-with-commercial-agreement/)
- [Grokipedia - Starlink Direct to Cell](https://grokipedia.com/page/Starlink_Direct_to_Cell)
- [FCC DA-24-1193 - SpaceX/T-Mobile SCS grant](https://docs.fcc.gov/public/attachments/DA-24-1193A1.pdf)
- [US Mobile - Starlink Satellite Calls guide (SCS / 3GPP Release 17)](https://www.usmobile.com/blog/starlink-satellite-phone-calls/)
- [DCD - T-Mobile launches nationwide satellite service with Starlink](https://www.datacenterdynamics.com/en/news/t-mobile-launches-nationwide-satellite-service-with-starlink/)
- [EchoStar 8-K (Sept 2025) - SpaceX AWS-4/H-block sale, SEC](https://www.sec.gov/Archives/edgar/data/0001415404/000141540425000041/tmb-20250907xex99d1.htm)
- [EchoStar 8-K (Nov 2025) - SpaceX AWS-3 sale, SEC](https://www.sec.gov/Archives/edgar/data/0001415404/000141540425000049/tmb-20251106xex99.htm)
- [Broadband Breakfast - SpaceX Buying EchoStar Satellite Spectrum for $17 Billion](https://broadbandbreakfast.com/spacex-buying-echostar-satellite-spectrum-for-17-billion/)
- [DCD - SpaceX acquires EchoStar's AWS-4 and H-block for $17bn](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/)
- [PBS - SpaceX pays $17 billion to acquire spectrum licenses from EchoStar](https://www.pbs.org/newshour/nation/spacex-pays-17-billion-to-acquire-spectrum-licenses-from-echostar)

C-band incumbent relocation (closing an open question from the grounding doc):
- [SpaceNews - Senator criticizes FCC's $9.7 billion C-band incentive payment program](https://spacenews.com/senator-criticizes-fccs-9-7-billion-c-band-incentive-payment-program/)
- [Telecompetitor - Satellite Operators Agree to Accelerate C-Band Relocation](https://www.telecompetitor.com/satellite-operators-agree-to-accelerate-c-band-relocation-sets-stage-for-historic-5g-auction/)

---

## 8. Confidence

**Overall: medium-high.**

- **High confidence:** the generation-is-a-standard framing and the IMT-2000/Advanced/2020 anchors; the 5G-NR-spans-67-FR1-plus-11-FR2-bands debunk of "5G = 5 GHz"; the refarming and DSS mechanics including the US carrier sunset of DSS; the FR3 (7.125 to 24.25 GHz) / WRC-27 candidate bands; the frequency-reuse-and-densification scaling logic; the SCS partner/lease structure of AST (AT&T/Verizon 850 MHz) and Starlink (T-Mobile PCS G-block); and the $17B+ SpaceX/EchoStar purchase. Each carried by 2+ independent sources.
- **Medium confidence:** the precise per-beam satellite numbers (Starlink ~3.1 Mbps / 0.52 to 0.61 bps/Hz from a single arXiv measurement study, though widely consistent; AST 120 Mbps/40 MHz/5,600 cells from the company and Wikipedia); the exact ~78.7 km satellite cell width (one source, corroborated by the 50 to 80 km LEO spot-beam range from a second). The DSS 15%/25% overhead is single-source.
- **Lower confidence / my own inference:** the area-capacity ratios in Section 4.4 are [DERIVED] order-of-magnitude arithmetic from sourced inputs (beam/cell sizes and per-cell capacities), not measured end-to-end; treat the ~300x-to-30,000x range as directional. The undisclosed Starlink/T-Mobile revenue-share terms remain a gap.

---

## 9. Open Questions

1. **What are the actual commercial terms of an SCS partnership?** The Verizon-AST $100M and stc $175M figures are public, but the per-subscriber revenue split and the fraction of a carrier's band a satellite gets to ride are not. This is the number the cost-per-subscriber model most needs and it is the natural next research target.
2. **How many simultaneous voice/data users does one direct-to-cell beam actually support?** The per-beam Mbps is sourced; converting to concurrent users needs a per-user rate assumption (e.g. a 100 kbps voice/text user vs a 1 Mbps data user) and the beam's user-scheduling model. Worth a dedicated derivation.
3. **Does FR3 (7 to 15 GHz) help or hurt a space direct-to-cell play?** More bandwidth per operator (>400 MHz) is attractive, but higher frequency means narrower beams, more path loss, and harder phone-to-LEO links. Whether 6G-era FR3 is reachable from orbit for direct-to-cell is unresolved and central to the ten-year view.
4. **What does AST's own ~45 MHz of L-band MSS change?** AST holds some of its own spectrum (not just leased carrier band). Whether an entrant could likewise acquire a sliver of MSS spectrum (the satellite-side door in [`rf_limited_service.md`](../laser_comms/rf_limited_service.md)) to reduce carrier dependence deserves a look.
5. **Will carriers re-adopt DSS for the satellite layer?** DSS is being sunset terrestrially, but sharing a band millisecond-by-millisecond between a terrestrial cell and an overhead satellite beam is conceptually the same problem. Whether SCS deployments use DSS-like sharing or hard channel dedication affects how much capacity the satellite actually gets.

---

## Claims ledger

Each hard claim below carries 2+ independent sources (or is tagged single-source / derived) for the catalog step to ingest.

1. **A cellular "generation" (G) is a standard and capability set, not a frequency; G = generation index.** Sources: [Data Alliance](https://www.data-alliance.net/blog/cellular-wireless-technologies-5g-lte-4g-gsm-3g-2g-and-6g), [Commsbrief](https://commsbrief.com/what-do-the-terms-1g-2g-3g-4g-and-5g-really-mean/). [FACT]
2. **3G = IMT-2000 (144 kbps mobile / 384 kbps pedestrian / 2 Mbps indoor); 4G = IMT-Advanced (100 Mbps mobile / 1 Gbps fixed).** Sources: [Data Alliance](https://www.data-alliance.net/blog/cellular-wireless-technologies-5g-lte-4g-gsm-3g-2g-and-6g), [Commsbrief](https://commsbrief.com/what-do-the-terms-1g-2g-3g-4g-and-5g-really-mean/). [FACT]
3. **5G = IMT-2020 (ITU-R M.2083), three usage scenarios eMBB / URLLC / mMTC; technologies GSM/UMTS/LTE/NR enable 2G/3G/4G/5G.** Sources: [Data Alliance](https://www.data-alliance.net/blog/cellular-wireless-technologies-5g-lte-4g-gsm-3g-2g-and-6g); corroborated in [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md) (Verizon, Cambridge Wireless). [FACT]
4. **5G NR is standardized across ~67 FR1 bands (410 MHz to 7.125 GHz) and ~11 FR2 bands (24.25 to 71 GHz) as of 3GPP Release 18; it spans 600 MHz to 39 GHz, not a single "5 GHz" band.** Sources: [Wikipedia - 5G NR frequency bands](https://en.wikipedia.org/wiki/5G_NR_frequency_bands), [RF Page](https://www.rfpage.com/lte-and-5g-nr-frequency-bands-explained/). [FACT]
5. **Cellular 5G and 5 GHz Wi-Fi are unrelated and non-interoperable (different radios/chipsets).** Sources: [Peplink](https://www.peplink.com/resources/5g-routers/is-a-5ghz-router-the-same-as-5g/), [Two River Computer](https://www.tworivercomputer.com/can-someone-explain-5g/), [Arrow](https://www.arrow.com/en/research-and-events/articles/5g-vs-5ghz-differences). [FACT]
6. **Hard spectrum refarming (drain old-gen users, re-light band for new gen) is a slow, multi-year process.** Sources: [Tweet4Technology](https://tweet4technology.blogspot.com/2023/04/dynamic-spectrum-sharing-dss.html), [Celona](https://www.celona.io/5g-lan/dynamic-spectrum-sharing-how-it-works-why-it-matters). [FACT]
7. **Dynamic Spectrum Sharing (DSS) lets 4G LTE and 5G NR share the same channel dynamically (~1 ms granularity) via software, avoiding hard refarming.** Sources: [Devopedia](https://devopedia.org/5g-dynamic-spectrum-sharing), [Celona](https://www.celona.io/5g-lan/dynamic-spectrum-sharing-how-it-works-why-it-matters), [Samsung white paper](https://images.samsung.com/is/content/samsung/assets/global/business/networks/insights/white-papers/0122_dynamic-spectrum-sharing/Dynamic-Spectrum-Sharing-Technical-White-Paper-Public.pdf). [FACT]
8. **DSS imposes ~15% (5G NR) and ~25% (4G LTE) performance overhead.** Source: [Tweet4Technology](https://tweet4technology.blogspot.com/2023/04/dynamic-spectrum-sharing-dss.html). [FACT, single-source]
9. **US carriers have largely sunset DSS (AT&T shuttered most DSS in 2021; moved 850 MHz to dedicated 5G) in favor of dedicated 5G channels.** Sources: [Light Reading - quiet sunset of DSS](https://www.lightreading.com/5g/the-quiet-sunset-of-5g-dynamic-spectrum-sharing), [Fierce Network](https://www.fierce-network.com/operators/verizon-relies-dynamic-spectrum-sharing-more-widely-than-at-t-report). [FACT]
10. **WRC-23 harmonized the core 5G mid-band 3.3 to 3.8 GHz (3300 to 3400 MHz IMT in Regions 1/2; 3600 to 3800 MHz in Region 2).** Sources: [CTU - WRC-23 outcome](https://ctu.int/wp-content/uploads/2024/02/WRC-23-outcome-for-Mobile-service-and-IMT.pdf), [FedSoc](https://fedsoc.org/commentary/fedsoc-blog/what-happened-at-the-world-radiocommunication-conference). [FACT]
11. **WRC-23 identified upper 6 GHz (6425 to 7125 MHz) for IMT in Region 1 (and parts of Region 3 / Mexico / Brazil), contested with Wi-Fi/RLAN.** Sources: [CTU](https://ctu.int/wp-content/uploads/2024/02/WRC-23-outcome-for-Mobile-service-and-IMT.pdf), [IIC Intermedia](https://iicintermedia.org/vol-52-issue-1/wrc-23-and-the-unresolved-battle-for-6-ghz/). [FACT]
12. **FR3 (upper mid-band) is 7.125 to 24.25 GHz in 3GPP, between FR1 (410 MHz to 7.125 GHz) and FR2 (24.25 to 71 GHz).** Sources: [Samsung Research](https://research.samsung.com/blog/Upper-Mid-Band-Spectrum-for-6G-Opportunities-and-Key-Enablers), [Nokia 6G](https://www.nokia.com/6g/6g-mid-band-spectrum-technology-explained/). [FACT]
13. **WRC-23 set the WRC-27 IMT/6G candidate study bands: 4.4 to 4.8 GHz, 7.125 to 8.4 GHz, 14.8 to 15.35 GHz.** Sources: [Samsung Research](https://research.samsung.com/blog/Upper-Mid-Band-Spectrum-for-6G-Opportunities-and-Key-Enablers), [Enterprise IT World](https://www.enterpriseitworld.com/decoding-the-spectrum-landscape-of-6g/). [FACT]
14. **FR3 / 7 to 15 GHz can offer >400 MHz per operator versus ~100 MHz in FR1.** Sources: [Nokia 6G](https://www.nokia.com/6g/6g-mid-band-spectrum-technology-explained/), [BackITapp](https://consulting.backitapp.com/spectrum-for-6g/fr3/). [FACT]
15. **Practical spectral efficiency: ~1.5 bps/Hz (4G LTE), ~3 bps/Hz (5G single-stream).** Sources: [Techplayon](https://www.techplayon.com/spectral-efficiency-5g-nr-and-4g-lte/), [5G-networks.net](https://www.5g-networks.net/spectral-efficiency-5g-nr-and-4g-lte-compared/). [FACT]
16. **T-Mobile real 2.5 GHz massive-MIMO spectral efficiency ~7.5 to 9.0 bps/Hz (vs ~2.5 to 3.0 for 4G); 16-layer MU-MIMO demo hit 5.6 Gbps on one 100 MHz channel (~50+ bps/Hz).** Sources: [Light Reading](https://www.lightreading.com/5g/t-mobile-ericsson-squeeze-56-gbits-out-of-5g-in-25ghz/d/d-id/763817), [Fierce Network](https://www.fierce-network.com/tech/t-mobile-pulls-more-out-2-5-ghz-mu-mimo-5g-demo-ericsson), [T-Mobile newsroom](https://www.t-mobile.com/news/network/t-mobile-achieves-mind-blowing-5g-speeds-with-mu-mimo). [FACT]
17. **Massive MIMO's ~145.6 bps/Hz record only appears to beat Shannon because ~128 parallel antennas/streams are used; each stream still obeys Shannon.** Source: [Wireless Future blog](https://ma-mimo.ellintech.se/2016/10/18/how-much-does-massive-mimo-improve-spectral-efficiency/). [FACT, single-source]
18. **Terrestrial frequency reuse (reuse-1) plus small-cell densification increases area capacity roughly linearly with cell count (cell-splitting gain).** Sources: [arXiv 1503.03912](https://arxiv.org/pdf/1503.03912), [ScienceDirect - frequency reuse](https://www.sciencedirect.com/topics/computer-science/frequency-reuse), [ResearchGate - small cells in HetNets](https://www.researchgate.net/publication/265911120_Small_Cells_in_Cellular_Networks_Challenges_of_Future_HetNets). [FACT]
19. **A LEO direct-to-cell spot beam is ~50 to 80 km wide (AST tiling: ~78.7 km hex cells across a ~1,660 km footprint of ~725 cells).** Sources: [techneconomyblog](https://techneconomyblog.com/category/leo-satellites/), [NewSpaceTracker](https://newspacetracker.com/articles/direct-to-smartphone-satellites/). [FACT] (78.7 km figure single-source, corroborated by 50 to 80 km range)
20. **A terrestrial low/mid-band macro cell is ~1.6 to 5 km radius.** Sources: [Dgtl Infra](https://dgtlinfra.com/cell-tower-range-how-far-reach/); consistent with [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md). [FACT]
21. **Starlink Direct-to-Cell delivers ~3.1 Mbps per beam at ~0.52 to 0.61 bps/Hz on a 2x5 MHz PCS G-block channel (up to ~18.6 Mbps if all spectrum aggregated); operates at ~0 dB median SINR.** Source: [arXiv 2506.00283 measurement study](https://arxiv.org/html/2506.00283v7). [FACT, single-source study]
22. **AST SpaceMobile next-gen BlueBird targets up to 120 Mbps per cell on up to 40 MHz, ~5,600 US coverage cells, 10 GHz total processing per satellite.** Sources: [AST SpaceMobile network](https://ast-science.com/spacemobile-network/), [AST next-gen BlueBird](https://ast-science.com/next-gen-bluebird/), [Wikipedia - AST SpaceMobile](https://en.wikipedia.org/wiki/AST_SpaceMobile). [FACT]
23. **Direct-to-cell satellite area capacity is ~0.0008 Mbps/km² (Starlink DTC) to ~0.083 Mbps/km² (AST) versus ~27+ Mbps/km² terrestrial mid-band macro, i.e. ~300x to ~30,000x more bits/s/km² on the ground.** Sources: [DERIVED] from claims 16, 19, 20, 21, 22. [DERIVED]
24. **The FCC Supplemental Coverage from Space (SCS) framework (adopted 2024, "Single Network Future") lets a satellite operator use a terrestrial carrier's licensed spectrum as a gap-filler, authorized only where the terrestrial licensee(s) lease their spectrum rights.** Sources: [Federal Register](https://www.federalregister.gov/documents/2024/04/30/2024-06669/single-network-future-supplemental-coverage-from-space-space-innovation), [Inside Global Tech](https://www.insideglobaltech.com/2024/04/30/fcc-acts-to-expand-satellite-to-smartphone-coverage-supplemental-coverage-from-space-rules-will-enable-partnerships-between-satellite-operators-and-wireless-network-providers-in-the/). [FACT]
25. **AST SpaceMobile uses AT&T's and Verizon's 850 MHz (plus FirstNet Band 14 / 700 MHz) under SCS; structured as commercial agreements (Verizon $100M), not a spectrum purchase; AST also holds ~45 MHz of its own lower-mid-band (incl. ~40 MHz L-band MSS).** Sources: [Wikipedia - AST SpaceMobile](https://en.wikipedia.org/wiki/AST_SpaceMobile), [SDxCentral](https://www.sdxcentral.com/news/fcc-grants-ast-spacemobile-access-to-att-verizon-spectrum/), [DCD](https://www.datacenterdynamics.com/en/news/ast-spacemobile-pairs-with-att-and-verizon-for-satellite-broadband/), [Via Satellite](https://www.satellitetoday.com/connectivity/2025/10/08/verizon-deepens-ast-spacemobile-ties-with-commercial-agreement/). [FACT]
26. **Starlink Direct-to-Cell uses T-Mobile's PCS G-block (1910 to 1915 MHz up / 1990 to 1995 MHz down) under SCS, explicitly via a lease arrangement with T-Mobile (FCC grant Nov 26, 2024, up to 7,500 NGSO satellites).** Sources: [FCC DA-24-1193](https://docs.fcc.gov/public/attachments/DA-24-1193A1.pdf), [arXiv 2506.00283](https://arxiv.org/html/2506.00283v7), [Inside Global Tech](https://www.insideglobaltech.com/2024/12/09/fcc-issues-filing-guidelines-for-supplemental-coverage-from-space-scs-applications-authorizes-spacex-and-t-mobile-to-premier-scs-deployment/). [FACT]
27. **SpaceX is buying its own cellular spectrum for next-gen direct-to-cell: ~$17B for EchoStar's AWS-4 and H-block (up to $8.5B cash + up to $8.5B stock + ~$2B interest funding), plus ~$2.6B for EchoStar's AWS-3 portfolio.** Sources: [EchoStar 8-K Sept 2025 / SEC](https://www.sec.gov/Archives/edgar/data/0001415404/000141540425000041/tmb-20250907xex99d1.htm), [EchoStar 8-K Nov 2025 / SEC](https://www.sec.gov/Archives/edgar/data/0001415404/000141540425000049/tmb-20251106xex99.htm), [Broadband Breakfast](https://broadbandbreakfast.com/spacex-buying-echostar-satellite-spectrum-for-17-billion/), [DCD](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/), [PBS](https://www.pbs.org/newshour/nation/spacex-pays-17-billion-to-acquire-spectrum-licenses-from-echostar). [FACT]
28. **C-band incumbents received ~$9.7B in accelerated-relocation incentive payments to vacate (most to Intelsat ~$4.87B and SES ~$3.97B), closing the open question in `spectrum_fundamentals_economics.md`.** Sources: [SpaceNews](https://spacenews.com/senator-criticizes-fccs-9-7-billion-c-band-incentive-payment-program/), [Telecompetitor](https://www.telecompetitor.com/satellite-operators-agree-to-accelerate-c-band-relocation-sets-stage-for-historic-5g-auction/). [FACT]
