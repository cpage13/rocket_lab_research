# Starlink V3 and V4: How Much Spectrum Each Generation Actually Incorporates

*Research date: June 2026. Communications research-wiki effort. Part of the Rocket Lab orbital communications feasibility study (companion to the orbital data-center track).*

**Builds on / does not duplicate:**
- [`research/competitors/starlink_v3_specs.md`](starlink_v3_specs.md): the V3 cost-and-capacity benchmark (per-satellite ~1 Tbps down, ~160-200 Gbps up, the V2-to-V3 jump, the broadband Gen2 and dedicated direct-to-cell fleets, the Starship/Neutron-fit handoff). That doc owns the capacity-and-physical-spec stack and lists the band *names*; this doc owns the **spectrum-quantity** stack: how many MHz/GHz of bandwidth each link uses, band by band, and the bandwidth-to-capacity link that turns it into Tbps.
- [`research/direct_communication/spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md): what a cellular "generation" is, the SCS partner-vs-buy access question, the per-beam direct-to-cell capacity ceiling (Starlink ~3.1 Mbps on a 2x5 MHz channel), and the ~65 MHz EchoStar buy in the SCS context. That doc owns the access mechanism; this doc owns the spectrum *inventory*.
- [`research/direct_communication/spectrum_fundamentals_economics.md`](../direct_communication/spectrum_fundamentals_economics.md): Shannon, the speed-vs-connections tradeoff, the band tiers, the AWS-3/C-band auction dollar figures. This doc cites those; it does not re-derive them.

**The one-line answer the founder asked for:** *A V3 broadband satellite turns roughly **2 GHz of Ku-band user-downlink spectrum** (8 channels x 250 MHz) into ~1 Tbps by reusing that same 2 GHz across **dozens of narrow spot beams** at ~4-4.5 bits/Hz per beam, fed by a much wider **Ka-band (multi-GHz) and E-band (2x5 GHz, 71-76 / 81-86 GHz) gateway/backhaul** pipe; the capacity jump is bought with more beams and more spectrum-reuse, not a new user band.* The clean statement and the arithmetic are in Section 5.

This doc carries no go/no-go verdict. China is excluded from all totals (no Chinese system used as a benchmark).

---

## Summary / Verdict

**Confidence: medium-high** on the broadband band ranges (Ku/Ka/V/E are in the FCC Gen2 grants and repeated across independent technical sources) and on the ~2 GHz Ku user-downlink / ~500 MHz Ku user-uplink channel structure (multiple independent reverse-engineering and modeling sources converge); **high** on the direct-to-cell ~65 MHz EchoStar holding and the T-Mobile PCS G-block 2x5 MHz lease (FCC grants, SEC filings, multiple outlets); **medium** on the exact per-satellite *usable* aggregate (the 2 GHz-to-1 Tbps link is a beams-times-reuse-times-efficiency derivation, with the beam count not hard-disclosed for V3); **low / UNKNOWN** on a distinct "V4" generation: as of June 2026 SpaceX has not announced a satellite branded V4 with disclosed spectrum, so the "next generation" spectrum story is the V3 + Gen2 V-band/W-band upgrade authority, not a separate V4 datasheet.

1. **Broadband user link (the bandwidth users actually touch): ~2 GHz of Ku-band downlink and ~500 MHz of Ku-band uplink per satellite.** Ku-band: ~10.7-12.7 GHz space-to-Earth (user downlink), ~14.0-14.5 GHz Earth-to-space (user uplink), structured as **8 x 250 MHz downlink channels (2,000 MHz total)** and **8 x 62.5 MHz uplink channels (500 MHz total)**, a ~75/25 down/up split. This is the spectrum a Ku user terminal sees. [FACT, multi-source]

2. **Gateway / feeder link (the much wider backhaul pipe): Ka-band (multiple GHz) plus, on Gen2/V-class, E-band 2x5 GHz.** Ka-band feeder: ~17.8-19.3 GHz space-to-Earth and ~27.5-30 GHz Earth-to-space (each ~1.5-2.5 GHz wide). E-band, FCC-approved for Gen2 in 2023: **71-76 GHz space-to-Earth and 81-86 GHz Earth-to-space (5 GHz in each direction, 10 GHz total)**, which SpaceX said enables roughly **4x more capacity per satellite**. [FACT, multi-source]

3. **Gen2 also carries V-band and W-band authority.** The FCC Gen2 grants let SpaceX operate the satellites with additional **V-band** (37.5-42.0 GHz space-to-Earth; 47.2-50.2 and 50.4-51.4 GHz Earth-to-space) and W-band frequencies, on top of Ku/Ka/E. V-band is a high-capacity, short-reach, rain-faded band used for additional user and feeder capacity rather than a new mass-market user band. [FACT, multi-source for the V-band grant; W-band authority single-source-class]

4. **Inter-satellite links are optical (laser), not RF, and carry no licensed spectrum.** ~3-4 terminals/sat, ~100 Gbps each. The ~4 Tbps "total per satellite" figure in the V3-specs doc is user-facing RF (~1 Tbps) plus this laser mesh plus the wide gateway pipe. [FACT, carried from the V3-specs doc]

5. **Direct-to-cell is a separate, narrow, low-frequency spectrum story.** Two distinct slices: (a) a **~5-10 MHz carrier gap-filler** leased under FCC Supplemental Coverage from Space (SCS): Starlink rides **T-Mobile's PCS G-block, a 2x5 MHz channel** (1910-1915 MHz up / 1990-1995 MHz down, ~1.9 GHz); and (b) **~65 MHz of dedicated cellular spectrum SpaceX is acquiring from EchoStar for ~$17B+** (15 MHz unpaired AWS-3 + 40 MHz AWS-4 + 10 MHz H-block, all ~1.7-2.2 GHz). The next-gen V3 direct-to-cell fleet is the home for this ~65 MHz; it is the single largest spectrum *purchase* in the story and the reason direct-to-cell capacity is a spectrum-acquisition problem first. [FACT, multi-source]

6. **"V4" is UNKNOWN as a disclosed spectrum generation.** As of June 2026, SpaceX has not published a satellite called "V4" with its own spectrum plan. The disclosed forward spectrum story is the V3 + Gen2 multi-band (Ku/Ka/V/E/W) upgrade authority plus the dedicated ~65 MHz direct-to-cell block, not a separate V4 datasheet. Any "V4 incorporates X MHz" claim would be unsourced and must be flagged. [UNKNOWN]

**Numbers to treat with care:** the per-satellite *usable* aggregate (the 2 GHz-to-1 Tbps link is a beams x reuse x efficiency derivation; V3 beam count not hard-disclosed); the exact Ka feeder edges (sources vary by ~0.1-0.5 GHz); the V-band/W-band utilization (granted, but how much V3 actually lights up is not disclosed); and anything labeled "V4."

---

## 1. The spectrum inventory, band by band

The cleanest way to answer "how much spectrum does Starlink incorporate" is to separate the **user link** (the bandwidth a customer's terminal or phone touches) from the **gateway/feeder + backhaul link** (the much wider pipe between satellite and ground core), because the wide backhaul is most of the licensed bandwidth and is invisible to the user.

| Link | Band | Frequency range | Bandwidth (per direction) | Role | Status |
|---|---|---|---|---|---|
| **User downlink** | Ku | ~10.7-12.7 GHz (space-to-Earth) | **~2,000 MHz** (8 x 250 MHz channels) | Broadband user receive | [FACT, multi-source] |
| **User uplink** | Ku | ~14.0-14.5 GHz (Earth-to-space) | **~500 MHz** (8 x 62.5 MHz channels) | Broadband user transmit | [FACT, multi-source] |
| **Gateway downlink** | Ka | ~17.8-19.3 GHz (space-to-Earth) | **~1.5 GHz-class** | Feeder to ground gateway | [FACT, multi-source] |
| **Gateway uplink** | Ka | ~27.5-30.0 GHz (Earth-to-space) | **~2.5 GHz-class** | Gateway to satellite | [FACT, multi-source] |
| **Backhaul (Gen2)** | E | 71-76 / 81-86 GHz | **5 GHz each way (10 GHz total)** | High-capacity gateway/backhaul; ~4x capacity/sat | [FACT, multi-source] |
| **Additional (Gen2)** | V | 37.5-42.0 (down) / 47.2-50.2, 50.4-51.4 GHz (up) | **several GHz** | Extra user/feeder capacity | [FACT, multi-source] |
| **Additional (Gen2)** | W | >75 GHz authority | (granted, utilization undisclosed) | Future high-capacity | [FACT, single-source-class] |
| **Inter-satellite** | Optical (laser) | n/a (not RF spectrum) | ~100 Gbps/terminal, 3-4 terminals | Mesh backbone | [FACT, carried] |
| **Direct-to-cell (SCS lease)** | PCS G-block | 1910-1915 / 1990-1995 MHz | **2x5 MHz (10 MHz total)** | Gap-filler to phones, T-Mobile lease | [FACT, multi-source] |
| **Direct-to-cell (owned)** | AWS-3 / AWS-4 / H-block | ~1.7-2.2 GHz | **~65 MHz** (15 + 40 + 10) | Dedicated next-gen D2C, EchoStar buy | [FACT, multi-source] |

Sources: Ku user 10.7-12.7 GHz down / 14.0-14.5 GHz up and the 8x250 MHz / 8x62.5 MHz channelization ([ShareTechnote Starlink](https://www.sharetechnote.com/html/Communication_Satellite_Starlink.html), [UT Austin Radionav Lab signal-structure paper](https://radionavlab.ae.utexas.edu/wp-content/uploads/starlink_structure.pdf), [Mike Puchol capacity model](https://mikepuchol.com/modeling-starlink-capacity-843b2387f501)); Ka feeder 17.8-19.3 / 27.5-30 GHz ([americantv frequency breakdown](https://www.americantv.com/what-frequency-does-starlink-use.php), [ShareTechnote](https://www.sharetechnote.com/html/Communication_Satellite_Starlink.html)); E-band 71-76/81-86 GHz, ~4x capacity ([SpaceNews E-band grant](https://spacenews.com/spacex-gets-e-band-radio-waves-to-boost-starlink-broadband/)); V-band Gen2 grant ([FCC DA-23-997 V-band order](https://docs.fcc.gov/public/attachments/DA-23-997A1.pdf), [Via Satellite Gen2 7,500 approval](https://www.satellitetoday.com/connectivity/2026/01/12/fcc-gives-spacex-approval-for-7500-more-starlink-gen2-satellites/)); D2C T-Mobile G-block lease ([FCC DA-24-1193](https://docs.fcc.gov/public/attachments/DA-24-1193A1.pdf)); EchoStar ~65 MHz ([Light Reading "115 MHz off the shelf"](https://www.lightreading.com/regulatory-politics/spacex-is-now-a-spectrum-holder-not-just-a-satellite-operator), [DCD AWS-4/H-block](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/)).

**Note on the source spread for the user-uplink range.** One technical compendium ([ShareTechnote](https://www.sharetechnote.com/html/Communication_Satellite_Starlink.html)) lists Ku user uplink in the 17.8-19.3 / 37.5-42.5 GHz region, which mixes the *gateway/feeder* (Ka/V) bands into the user-uplink row. The cleaner, FCC-grounded and reverse-engineering consensus is that the **user** uplink is Ku at ~14.0-14.5 GHz (~500 MHz), and the higher ranges are **gateway/feeder** (Ka) and **V-band** feeder, not user uplink. The table above uses the consensus assignment. This is flagged because a careless read of a single source conflates user and gateway spectrum.

---

## 2. The broadband user spectrum: ~2 GHz Ku down, ~500 MHz Ku up

This is the bandwidth that actually reaches a broadband customer's dish, and it is the same envelope across V1, V2, and V3.

- **Downlink: ~2 GHz of Ku-band** (10.7-12.7 GHz), divided into **8 channels of 250 MHz each** (some sources state 240 MHz; the round figure is 2,000 MHz total) ([Mike Puchol model](https://mikepuchol.com/modeling-starlink-capacity-843b2387f501), [UT Austin signal-structure paper](https://radionavlab.ae.utexas.edu/wp-content/uploads/starlink_structure.pdf)).
- **Uplink: ~500 MHz of Ku-band** (~14.0-14.5 GHz), as **8 channels of 62.5 MHz**, giving the ~75/25 downlink/uplink asymmetry ([ShareTechnote](https://www.sharetechnote.com/html/Communication_Satellite_Starlink.html)).
- **The user-facing spectrum does not grow generation to generation.** V3 stays in this same Ku user envelope. This matters and is restated in Section 5: V3's ~10x capacity leap does *not* come from giving each user more Ku bandwidth; it comes from forming more, narrower beams that reuse the same 2 GHz more times, plus a much wider gateway/backhaul pipe (Ka + E) so the satellite is not backhaul-starved.

This is the [`spectrum_fundamentals_economics.md`](../direct_communication/spectrum_fundamentals_economics.md) speed-vs-connections tradeoff in a real platform: Ku is the workhorse user band because it balances rain tolerance, antenna size, and bandwidth; the raw width per user is fixed at the 2 GHz pool, and capacity is won spatially (beams), not by widening the user channel.

---

## 3. The gateway / backhaul spectrum: Ka multi-GHz, then E-band 10 GHz, then V/W

The wide spectrum lives in the feeder and backhaul links, not the user link.

- **Ka-band feeder:** ~17.8-19.3 GHz down and ~27.5-30 GHz up, each link **one-to-a-few GHz wide**, far wider than the 2 GHz user pool. This is the pipe that carries aggregated user traffic between the satellite and a ground gateway ([americantv](https://www.americantv.com/what-frequency-does-starlink-use.php), [ShareTechnote](https://www.sharetechnote.com/html/Communication_Satellite_Starlink.html)).
- **E-band backhaul (the Gen2 capacity unlock):** FCC approved SpaceX in 2023 to use **71-76 GHz space-to-Earth and 81-86 GHz Earth-to-space, 5 GHz in each direction, 10 GHz total**. SpaceX stated this E-band backhaul enables **~4x more capacity per satellite** than earlier iterations, because the satellite-to-ground feeder stops being the bottleneck ([SpaceNews E-band grant](https://spacenews.com/spacex-gets-e-band-radio-waves-to-boost-starlink-broadband/)). E-band is the single most important *added* spectrum in the V2-mini/V3-class generation.
- **V-band (Gen2 grant):** SpaceX is authorized to operate Gen2 satellites in **37.5-40.0 and 40.0-42.0 GHz (space-to-Earth)** and **47.2-50.2 and 50.4-51.4 GHz (Earth-to-space)** (the 42.0-42.5 GHz request was dismissed). V-band is several more GHz of high-capacity, short-reach spectrum for additional user/feeder capacity ([FCC DA-23-997](https://docs.fcc.gov/public/attachments/DA-23-997A1.pdf), [Via Satellite](https://www.satellitetoday.com/connectivity/2026/01/12/fcc-gives-spacex-approval-for-7500-more-starlink-gen2-satellites/)).
- **W-band (>75 GHz):** the Gen2 upgrade authority also names W-band frequencies, but how much V3 actually lights up is not disclosed (utilization UNKNOWN; the *authority* is FACT).

**The structural read:** the user link is a fixed ~2.5 GHz (Ku down+up); the *system* incorporates well over **20 GHz of licensed RF** when Ka feeder + E-band + V-band are counted, plus optical ISLs that carry no licensed spectrum at all. The capacity story is a wide-backhaul story feeding a spectrally-reused user link.

---

## 4. Direct-to-cell spectrum: the ~5-10 MHz lease and the ~65 MHz purchase

Direct-to-cell is a completely different spectrum regime: low-frequency (~1.7-2.2 GHz) cellular spectrum, in tiny slices, reaching unmodified phones. There are two distinct slices and the founder asked for both.

### 4.1 The carrier gap-filler slice (SCS lease): a 2x5 MHz channel

Starlink Direct-to-Cell rides **T-Mobile's PCS G-block: 1910-1915 MHz Earth-to-space and 1990-1995 MHz space-to-Earth, a 2x5 MHz (10 MHz total) channel**, under the FCC's Supplemental Coverage from Space (SCS) framework, "pursuant to a lease arrangement with T-Mobile" (FCC grant Nov 26, 2024) ([FCC DA-24-1193](https://docs.fcc.gov/public/attachments/DA-24-1193A1.pdf); per-beam capacity of this channel in [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md), ~3.1 Mbps/beam at ~0.52-0.61 bps/Hz). This is the "~5 to 10 MHz SCS gap-filler" the founder named: a single carrier's small dedicated D2C channel, leased not owned. AST's analogue is AT&T/Verizon 850 MHz (also a thin SCS slice).

### 4.2 The dedicated D2C slice (owned): ~65 MHz from EchoStar for ~$17B+

For its *next-generation* dedicated direct-to-cell fleet (the up-to-15,000-satellite V3 D2C constellation, FCC SAT-LOA-20250916-00282), SpaceX is **buying its own cellular spectrum**: **~65 MHz of nationwide spectrum from EchoStar, = 15 MHz unpaired AWS-3 + 40 MHz AWS-4 + 10 MHz H-block**, all in the ~1.7-2.2 GHz region (AWS-4 = 2000-2020 MHz up / 2180-2200 MHz down, the "golden band" for D2C; H-block fills ~1995-2000 MHz; AWS-3 unpaired uplink ~1695-1710 MHz, 3GPP Band n70). Price: **~$17B for AWS-4 + H-block** (up to $8.5B cash + up to $8.5B SpaceX stock, Sept 2025) plus **~$2.6B for the AWS-3 portfolio** (SpaceX stock, Nov 2025); FCC-approved May 12, 2026 ([Light Reading "115 MHz off the shelf"](https://www.lightreading.com/regulatory-politics/spacex-is-now-a-spectrum-holder-not-just-a-satellite-operator), [DCD AWS-4/H-block $17bn](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/), [SpaceNews AWS-3 $2.6B](https://spacenews.com/echostar-sells-more-direct-to-device-spectrum-for-bigger-spacex-stake/), [Aetha AWS-3 analysis](https://www.aethaconsulting.com/what-starlinks-latest-purchase-of-aws-3-spectrum-tells-us-about-its-d2d-plans/)).

**The 115-vs-65 MHz nuance (a correction worth pinning).** Reporting often cites "~115 MHz" around this deal. That ~115 MHz is the **total spectrum the FCC moved in the two May-2026 transactions**, of which **SpaceX received ~65 MHz** (the 15+40+10 above) and **AT&T received the other ~50 MHz** (30 MHz of 3.45 GHz mid-band + 20 MHz of 600 MHz low-band) ([Light Reading](https://www.lightreading.com/regulatory-politics/spacex-is-now-a-spectrum-holder-not-just-a-satellite-operator)). So **SpaceX's owned D2C holding is ~65 MHz**, not 115 MHz; the corpus's existing ~65 MHz figure (COMM in the V3-specs ledger, [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md)) is correct and this doc confirms it and explains the 115 MHz source of confusion.

**Why this matters for the thesis (carried, not re-argued):** more MHz is the direct-to-cell capacity lever (a beam scales roughly linearly with channel width, per [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md)), which is exactly why SpaceX spent ~$17B+ to go from a 2x5 MHz lease to a ~65 MHz owned block. A Rocket-Lab-scale entrant's realistic path is the SCS lease (the 2x5 MHz door), not the ~$17B buy.

---

## 5. The bandwidth-to-capacity link in a real platform (the founder's ask)

The founder asked to see, concretely, "a V3 broadband satellite turns roughly X MHz of bandwidth into ~1 Tbps via Y." Here is the chain, grounded in the V2-mini numbers that are reverse-engineered and disclosed, then scaled to V3.

**The V2-mini anchor (where the arithmetic is checkable):**
- User-downlink spectrum pool: **~2,000 MHz** (8 x 250 MHz Ku channels).
- Beams: **48 downlink beams** (4 antennas x 8 beams x 2 polarizations), reusing the 2 GHz pool spatially.
- Spectral efficiency: **~4-4.5 bits/Hz** per beam (modeled ceiling) ([Mike Puchol model](https://mikepuchol.com/modeling-starlink-capacity-843b2387f501), [UT Austin signal-structure paper](https://radionavlab.ae.utexas.edu/wp-content/uploads/starlink_structure.pdf)).
- Disclosed V2-mini per-satellite downlink: **~96 Gbps** (4x a V1.5) ([V2-mini ~96 Gbps down / ~6.7 Gbps up](https://space.skyrocket.de/doc_sdat/starlink-v2-mini.htm)).

The check: 2,000 MHz x ~4.5 bits/Hz ≈ 9 Gbps from a *single* spectral reuse; ~96 Gbps implies the 2 GHz pool is effectively reused on the order of ~10x across the beam pattern (not every beam is full-rate at once). The exact decomposition is not publicly pinned, but the shape is clear: **capacity = (user spectrum pool) x (spectral efficiency) x (number of times the pool is spatially reused across beams).**

**Scaling to V3 (the ~1 Tbps figure):**
- **Same ~2 GHz Ku user-downlink pool** (no new user band).
- **More, narrower, fully-digital beams** ("dozens of targets simultaneously," fully-digital phased array vs the partly-analog earlier design), so the 2 GHz pool is reused many more times.
- **A much wider Ka + E-band (10 GHz) gateway/backhaul pipe** so the satellite is not feeder-limited (the ~4x E-band capacity unlock).
- Result: **~1 Tbps downlink** (~10x the V2-mini ~96 Gbps), ~160-200 Gbps uplink ([carried from](starlink_v3_specs.md)).

**The clean statement for the founder:**

> **A V3 broadband satellite turns roughly 2 GHz of Ku-band user-downlink spectrum (8 x 250 MHz channels) into ~1 Tbps by reusing that same 2 GHz across dozens of narrow, fully-digital spot beams at ~4-4.5 bits/Hz per beam, while a wide Ka-band (multi-GHz) plus E-band (10 GHz, 71-76 / 81-86 GHz) gateway-and-backhaul pipe keeps the feeder from bottlenecking. The ~10x jump from a V2-mini comes from more beams and more spectral reuse plus the wider backhaul, NOT from giving each user more Ku bandwidth.**

This is the load-bearing insight for the Rocket Lab thesis: **the user spectrum is fixed and modest (~2 GHz); the capacity comes from beams and backhaul.** A new entrant who cannot form as many beams (smaller antenna, less power, fewer satellites over a footprint) or who lacks the wide E-band backhaul cannot match the per-satellite capacity even with the *same* Ku user allocation. Spectrum quantity at the user link is not the differentiator; beams x backhaul x satellite count is. (This dovetails with [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md): a beam is Shannon-times-footprint gated and cannot densify, so per-beam bandwidth and beam count, not a bigger user band, set the ceiling.)

---

## 6. Is there a "V4"? (UNKNOWN, flagged)

The founder asked about V4 spectrum "if disclosed." **It is not disclosed.** As of June 2026:
- SpaceX has not announced a satellite branded **V4** with its own spectrum/band plan or capacity datasheet. The current frontier satellite is **V3** (first Starship-class flight May 22, 2026, dummy payloads; operational H2 2026 target).
- The disclosed *forward* spectrum story is not a new generation's band plan, it is: (a) the **Gen2 multi-band upgrade authority** (Ku/Ka/V/E/W) already granted for the existing satellites, and (b) the **dedicated ~65 MHz direct-to-cell block** (EchoStar) for the up-to-15,000-satellite V3 D2C fleet.
- The genuine forward greenfield in the wider spectrum landscape is **FR3 / 7-15 GHz at WRC-27** (the one band not yet filed, per [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md)), but no SpaceX "V4 uses FR3" plan is on record.

**Therefore: treat any "V4 incorporates X MHz" statement as unsourced.** The honest answer is that the next-generation spectrum incorporation is the V3 + Gen2 multi-band envelope plus the dedicated D2C block, and a distinct V4 spectrum generation is not publicly pinned. [UNKNOWN]

---

## 7. What this gives the model

1. **The user spectrum is fixed and modest (~2 GHz Ku down, ~500 MHz Ku up), identical across V1/V2/V3.** The per-generation capacity leap is a beams-and-backhaul story, not a user-bandwidth story.
2. **The system incorporates >20 GHz of licensed RF** when the Ka feeder + E-band (10 GHz) + V-band are counted, plus license-free optical ISLs. The wide backhaul (especially E-band's ~4x unlock) is most of the spectrum and is invisible to the user.
3. **Direct-to-cell is two thin low-band slices:** a 2x5 MHz SCS lease (the entrant-realistic door) and a ~65 MHz owned block costing ~$17B+ (the hyperscale exception). The ~115 MHz often quoted is the full FCC transaction; SpaceX got ~65 MHz, AT&T got ~50 MHz.
4. **The bandwidth-to-capacity link is concrete and checkable on V2-mini** (2 GHz x ~4.5 bits/Hz x ~10x spatial reuse ≈ ~96 Gbps) and scales to V3's ~1 Tbps by more beams + wider backhaul. A new entrant matches per-satellite capacity only by matching beams x backhaul x satellite count, not by holding the same Ku band.
5. **"V4" is not a disclosed spectrum generation as of June 2026.** Do not let a V4 spectrum number into the model without a source.

---

## Open questions / uncertainties

- **V3 beam count.** Not hard-disclosed; the 2 GHz-to-1 Tbps decomposition (beams x reuse x efficiency) is therefore a derivation, not a pinned breakdown.
- **How much V-band / W-band V3 actually lights up.** The Gen2 authority is granted; realized utilization is undisclosed.
- **Exact Ka feeder edges.** Sources vary by ~0.1-0.5 GHz on the 17.8-19.3 / 27.5-30 GHz edges; the ~GHz-class width is robust, the decimals are not all double-pinned.
- **A genuine V4.** No disclosed V4 spectrum plan; if one appears, the "next generation spectrum" row in the model should be revisited.
- **Per-user realized Ku rate.** The 2 GHz pool is shared; the gigabit-per-user V3 headline needs a terminal upgrade and is a peak, not a sustained per-user allocation.

---

## Claims ledger

For the catalog step to ingest. Assigned from this doc's range **COMM-178..190**. Each hard claim with its independent sources.

| Claim ID | Claim | Status | Sources |
|---|---|---|---|
| COMM-178 | Starlink broadband **user-downlink** spectrum is ~2 GHz of Ku-band (10.7-12.7 GHz), structured as **8 x 250 MHz channels (2,000 MHz total)**; identical envelope across V1/V2/V3. | FACT (multi-source) | [Mike Puchol model](https://mikepuchol.com/modeling-starlink-capacity-843b2387f501), [UT Austin signal-structure paper](https://radionavlab.ae.utexas.edu/wp-content/uploads/starlink_structure.pdf), [ShareTechnote](https://www.sharetechnote.com/html/Communication_Satellite_Starlink.html) |
| COMM-179 | Starlink broadband **user-uplink** spectrum is ~500 MHz of Ku-band (~14.0-14.5 GHz), as **8 x 62.5 MHz channels** (~75/25 down/up split). | FACT (multi-source) | [ShareTechnote](https://www.sharetechnote.com/html/Communication_Satellite_Starlink.html), [UT Austin signal-structure paper](https://radionavlab.ae.utexas.edu/wp-content/uploads/starlink_structure.pdf) |
| COMM-180 | **Ka-band gateway/feeder** links: ~17.8-19.3 GHz space-to-Earth and ~27.5-30 GHz Earth-to-space, each ~1-2.5 GHz wide (far wider than the user pool). | FACT (multi-source) | [americantv](https://www.americantv.com/what-frequency-does-starlink-use.php), [ShareTechnote](https://www.sharetechnote.com/html/Communication_Satellite_Starlink.html) |
| COMM-181 | **E-band backhaul** (FCC-approved 2023, Gen2): **71-76 GHz space-to-Earth and 81-86 GHz Earth-to-space, 5 GHz each way (10 GHz total)**; SpaceX states it enables ~4x more capacity per satellite. | FACT (multi-source) | [SpaceNews E-band grant](https://spacenews.com/spacex-gets-e-band-radio-waves-to-boost-starlink-broadband/), [Via Satellite Gen2](https://www.satellitetoday.com/connectivity/2026/01/12/fcc-gives-spacex-approval-for-7500-more-starlink-gen2-satellites/) |
| COMM-182 | **V-band** Gen2 authority: 37.5-40.0 and 40.0-42.0 GHz (space-to-Earth); 47.2-50.2 and 50.4-51.4 GHz (Earth-to-space); the 42.0-42.5 GHz request was dismissed. | FACT (multi-source) | [FCC DA-23-997 V-band order](https://docs.fcc.gov/public/attachments/DA-23-997A1.pdf), [Via Satellite Gen2](https://www.satellitetoday.com/connectivity/2026/01/12/fcc-gives-spacex-approval-for-7500-more-starlink-gen2-satellites/) |
| COMM-183 | Gen2 satellites also carry **W-band (>75 GHz) operating authority** alongside Ku/Ka/V/E; realized V3 utilization undisclosed. | FACT (single-source-class) | [Via Satellite Gen2 (Ku/Ka/V/W upgrade authority)](https://www.satellitetoday.com/connectivity/2026/01/12/fcc-gives-spacex-approval-for-7500-more-starlink-gen2-satellites/) |
| COMM-184 | Inter-satellite links are **optical (laser), not RF**, carrying no licensed spectrum (~3-4 terminals/sat, ~100 Gbps each); the ~4 Tbps "total/sat" is user RF + this mesh + gateway pipe. | FACT (carried) | [`starlink_v3_specs.md`](starlink_v3_specs.md), [Gunter's Space Page](https://space.skyrocket.de/doc_sdat/starlink-v2-0-ss.htm) |
| COMM-185 | Direct-to-cell **SCS gap-filler slice**: Starlink leases T-Mobile's **PCS G-block, 2x5 MHz (10 MHz total)**, 1910-1915 MHz up / 1990-1995 MHz down (~1.9 GHz), "pursuant to a lease arrangement with T-Mobile." | FACT (multi-source) | [FCC DA-24-1193](https://docs.fcc.gov/public/attachments/DA-24-1193A1.pdf), [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) (COMM-112) |
| COMM-186 | Direct-to-cell **dedicated owned slice**: SpaceX is acquiring **~65 MHz from EchoStar = 15 MHz unpaired AWS-3 + 40 MHz AWS-4 + 10 MHz H-block** (~1.7-2.2 GHz), for the next-gen V3 D2C fleet. | FACT (multi-source) | [Light Reading "115 MHz off the shelf"](https://www.lightreading.com/regulatory-politics/spacex-is-now-a-spectrum-holder-not-just-a-satellite-operator), [DCD AWS-4/H-block](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/), [Aetha](https://www.aethaconsulting.com/what-starlinks-latest-purchase-of-aws-3-spectrum-tells-us-about-its-d2d-plans/) |
| COMM-187 | The EchoStar D2C spectrum cost **~$17B (AWS-4 + H-block, up to $8.5B cash + up to $8.5B stock, Sept 2025) plus ~$2.6B (AWS-3, stock, Nov 2025)**; FCC-approved May 12, 2026. | FACT (multi-source) | [DCD $17bn](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/), [SpaceNews AWS-3 $2.6B](https://spacenews.com/echostar-sells-more-direct-to-device-spectrum-for-bigger-spacex-stake/), [PBS $17B](https://www.pbs.org/newshour/nation/spacex-pays-17-billion-to-acquire-spectrum-licenses-from-echostar) |
| COMM-188 | The "~115 MHz" often quoted is the **total of both May-2026 FCC transactions**; **SpaceX received ~65 MHz**, **AT&T received the other ~50 MHz** (30 MHz of 3.45 GHz + 20 MHz of 600 MHz). SpaceX's owned D2C holding is ~65 MHz, not 115 MHz. | FACT (multi-source) | [Light Reading "115 MHz off the shelf"](https://www.lightreading.com/regulatory-politics/spacex-is-now-a-spectrum-holder-not-just-a-satellite-operator), [SpaceNews FCC approval](https://spacenews.com/fcc-approves-spacex-spectrum-deal-with-2-4-billion-escrow-condition/) |
| COMM-189 | **The bandwidth-to-capacity link:** a V2-mini turns ~2 GHz of Ku user-downlink (8 x 250 MHz) into ~96 Gbps via **48 beams at ~4-4.5 bits/Hz with ~10x spatial reuse**; V3 scales the SAME 2 GHz to ~1 Tbps by more/narrower fully-digital beams plus wider Ka+E-band (10 GHz) backhaul, NOT a new user band. | DERIVED (sourced inputs) | [Mike Puchol model](https://mikepuchol.com/modeling-starlink-capacity-843b2387f501), [UT Austin signal-structure paper](https://radionavlab.ae.utexas.edu/wp-content/uploads/starlink_structure.pdf), [V2-mini ~96 Gbps](https://space.skyrocket.de/doc_sdat/starlink-v2-mini.htm), [`starlink_v3_specs.md`](starlink_v3_specs.md) |
| COMM-190 | **"V4" is not a disclosed spectrum generation as of June 2026:** no SpaceX satellite branded V4 with its own band/spectrum plan; the forward story is the V3 + Gen2 multi-band (Ku/Ka/V/E/W) upgrade authority plus the dedicated ~65 MHz D2C block. | UNKNOWN | (absence of disclosure; [`starlink_v3_specs.md`](starlink_v3_specs.md) deployment status, [Via Satellite Gen2](https://www.satellitetoday.com/connectivity/2026/01/12/fcc-gives-spacex-approval-for-7500-more-starlink-gen2-satellites/)) |
