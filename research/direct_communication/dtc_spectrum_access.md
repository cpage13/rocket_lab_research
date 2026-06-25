# DTC Spectrum Access: Can You Use Any Spectrum, What Is Available, and How You Would Obtain It

*Research date: June 2026. Communications research-wiki effort (shared library). Direct-to-cell (DTC) spectrum-access doc. No go/no-go verdict.*

**The question this doc answers (founder's framing, verbatim intent):** "A 25 m^2 antenna does not mean you must use a 25 MHz signal. What spectrum is available for that kind of antenna? Can you use ANY spectrum? What is available, and how would you obtain it?" The premise is correct and important: antenna size and held bandwidth are independent dials. Aperture sets link quality (gain, G/T, EIRP); it does not set how many MHz you are licensed to transmit on. This doc takes that decoupling as the starting point and then shows what re-couples a DTC entrant to a narrow band set anyway: not the antenna, but the unmodified phone's radio.

**Builds on / does not duplicate (cite, do not repeat):**
- [`spectrum_purchase_and_6g.md`](spectrum_purchase_and_6g.md) (COMM-229..248): the quantity benchmark (GSMA 80-100 MHz to launch, ~100-200 MHz to match an incumbent), the secondary-market $/MHz-POP prices, the total-dollar US+Europe translation (~$32-46B for 100 MHz, ~$65-90B for 200 MHz), and the 6G/FR3/WRC-27 "decided vs open" analysis. This doc **uses** those numbers in the acquisition-routes section; it does not re-derive them.
- [`spectrum_generations_and_availability.md`](spectrum_generations_and_availability.md) (COMM-104..114): what a "generation" is, refarming/DSS, the FCC SCS partner/lease model, the EchoStar exception. This doc **applies** the SCS mechanics to the entrant's options; it does not re-explain them.
- [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) (COMM-141..154): the rent-to-own spectrum shift, the EchoStar ~$17B / ~65 MHz and AST/Ligado ~45 MHz deals, the ~20x per-GB capacity gap.
- [`starlink_v3_v4_spectrum_incorporation.md`](../competitors/starlink_v3_v4_spectrum_incorporation.md) (COMM-178..190): the band-by-band MHz inventory, the PCS G-block 2x5 MHz lease, the ~65-vs-115 MHz EchoStar distinction.
- [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md) (COMM-001..022): the auction $/MHz-POP baseline (C-band ~$0.94), who holds which US tier, the "terrestrial auction door is closed to an entrant" verdict.
- [`dtc_antenna_aperture_tradeoff.md`](dtc_antenna_aperture_tradeoff.md) (COMM-313): the aperture-and-spectrum asymmetry (broadband rides wide Ku/Ka because the dish closes the link at high-order modulation; DTC is stuck in thin low-band cellular slices), which is the physical root of this doc's "you cannot use any spectrum" answer.
- [`channels_aggregate_answer.md`](channels_aggregate_answer.md): carrier aggregation sums separate held channels, so total capacity is bounded by how much spectrum you hold, a licensing/business limit, not a per-channel physics cap.

**The NEW contribution here is one integrated answer the corpus has only in scattered pieces:** the explicit "no, you cannot use any spectrum, and here is precisely why (the phone's radio set, not the antenna)," a clean realistic-DTC band inventory with the carrier-owned gate stated as the binding availability constraint, and the three acquisition routes (SCS lease, outright purchase, auction/6G) laid side by side with costs and the entrant's honest options. Where this doc states a band edge for DTC eligibility, it is now sourced to the **FCC SCS Report and Order itself** (the prior docs cited the deals, not the rule's band list).

> **Reading guide.** Every hard number is tagged **[FACT]** (2+ independent sources), **[FACT, single-source]**, **[DERIVED]** (arithmetic on cited inputs), **[ESTIMATE]** (third-party model/sizing), or **[UNKNOWN]** (named gap). China is excluded. No verdict on the Rocket Lab business is rendered.

---

## Answer First

**1. Can you use any spectrum? No.** The antenna decouples bandwidth from aperture in physics, but the **unmodified phone re-couples you to existing cellular bands**, because the phone can only tune the radios it already has. A bare handset has front-end filters and power amplifiers for roughly **600 MHz to ~2.1 GHz cellular bands** and nothing else in the satellite-relevant range; it has no Ku, Ka, mmWave, L-band MSS, or any non-cellular radio. So a DTC satellite must transmit in a band the phone's chipset already supports, and the FCC's Supplemental Coverage from Space (SCS) rules authorize exactly that set: **600 MHz, 700 MHz, 800 MHz, Broadband PCS (~1.9 GHz), and the AWS H-block (~2 GHz)** [FACT]. The 25 m^2 aperture buys you link quality on those bands; it does not unlock arbitrary spectrum, because there is no phone on the other end that can receive it.

**2. What is available, and how much?** The realistic DTC inventory is **low-band and lower-mid-band cellular only**: 600/700/800/850/900 MHz low-band plus PCS ~1.9 GHz and AWS ~2 GHz, with the SCS rule list as the authoritative menu (~600 MHz to ~2 GHz). The total *physically usable* pool across those bands is on the order of a few hundred MHz, but the *available-to-an-entrant* pool is far smaller, because **essentially all of the good low-band is already carrier-owned**: the prime US low-band and mid-band is fully spoken for (COMM-021, COMM-022), and a new entrant hits that wall. Against the corpus's competitive benchmark of **~100 MHz mid-band to launch and ~200 MHz to match an incumbent** (COMM-229, COMM-236), the realistic clean DTC holding sits one to two orders of magnitude below: a leased **2x5 MHz** SCS slice today, or an owned **~65 MHz** block at the deep-pocketed extreme (the EchoStar buy). The gate is ownership, not physics.

**3. How would you obtain it? Three routes, very different costs.**
- **(a) SCS lease (ride a carrier's band): near-zero spectrum capex, but you need the carrier partner and share their band.** This is the realistic-entrant path. Starlink leases T-Mobile's PCS G-block (2x5 MHz at ~1.9 GHz); AST uses AT&T's and Verizon's 700/800 MHz under commercial agreements (Verizon ~$100M, not a spectrum purchase). The FCC SCS framework (rules effective May 30, 2024) makes this legal but requires the terrestrial partner to hold all licenses on the channel and lease them to you before grant, and the operation is secondary (no interference to the carrier) [FACT].
- **(b) Buy spectrum outright: tens of billions.** The precedent is SpaceX buying EchoStar's AWS-4 + H-block + AWS-3, **~65 MHz nationwide for ~$17B** (FCC-approved 2026, ~$1.03/MHz-POP) [FACT]. To OWN a competitive US-plus-Europe cellular mid-band position the corpus prices the entry ticket at **~$32-46B for 100 MHz and ~$65-90B for 200 MHz, spectrum-only** (COMM-245, COMM-246). The only blocks a satellite entrant can actually buy are distressed MSS/satellite holdings (EchoStar, Ligado), and the last buyer set the price as a hyperscaler.
- **(c) Auctions / new allocations / 6G: not a near-term door for a DTC entrant.** There is no greenfield US cellular low-band or mid-band left to auction. The one greenfield is **6G upper mid-band (FR3, the 7.125-8.4 GHz "golden band" plus 4.4-4.8 and 14.8-15.35 GHz)**, but it is terrestrial-led, not yet allocated/auctioned/held, auctions ~2028-2032+, and the physics is hostile to a LEO-to-handset link at 7-15 GHz, so a satellite NTN entrant should not count on it (COMM-247, COMM-248). 3GPP NTN bands keep the satellite tier on MSS/FSS spectrum, not on the FR3 mobile pie.

**4. The entrant's realistic position (honest options, no verdict).** A Rocket Lab style new entrant has effectively two doors. **Door A, the carrier partnership (SCS):** near-zero spectrum capex, fast, but you ride 5-40 MHz of a carrier's band, you share their network, and your capacity is gated by what they lease you (today's reality is a 2x5 MHz slice). **Door B, the multi-billion purchase:** own a dedicated block, but the only buyable blocks are distressed MSS holdings, ~65 MHz cost ~$17B over the US alone, and a competitive US+Europe position is ~$32-90B spectrum-only, before a single satellite. There is no third "just use a wide clean band because the antenna is big" door, because the phone cannot receive a wide clean band that is not already a cellular allocation. The aperture is the lever the operator controls; the spectrum is the lever it must lease or buy.

**Confidence: high on the gate and the band set; high on the route costs (corpus-sourced and re-validated); medium-high on the 6G trajectory call.** The "phone has no non-cellular radio" point and the SCS band list are multi-source FACT. The route costs inherit the corpus's confidence (the $32-90B figures are DERIVED order-of-magnitude anchors; the EchoStar ~$17B/~65 MHz is multi-source FACT). The "a satellite entrant cannot get FR3" read is a well-attested trajectory, not a formally settled fact.

---

## 1. Can You Use Any Spectrum? No, and Precisely Why

### 1.1 The decoupling is real: aperture is not bandwidth

The founder's premise is correct. Antenna gain is set by aperture area (`G = 4 pi eta A / lambda^2`), and that is a separate quantity from the channel bandwidth B you are licensed to occupy [FACT, formula; COMM in `dtc_antenna_aperture_tradeoff.md`]. A 25 m^2 array delivers a high-gain, sensitive link; on that link you could in principle carry a narrow 5 MHz channel or a wide 100 MHz channel, and you can sum multiple held channels by carrier aggregation so total capacity tracks total MHz held, not one channel's width ([`channels_aggregate_answer.md`](channels_aggregate_answer.md)). So nothing about the aperture forces a "25 MHz signal." The constraint on how much spectrum you hold is a licensing and business constraint, not an antenna constraint. So far the premise holds completely.

### 1.2 What re-couples you: the unmodified phone's radio set

The DTC product is defined by one thing: it talks to an **ordinary unmodified smartphone** (COMM-141; [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md)). "The phone thinks it is on its normal network." That single design choice is what forecloses arbitrary spectrum, for a reason that has nothing to do with the satellite and everything to do with the handset:

- A phone can only tune the **radios it physically has**: band-specific front-end filters, duplexers, and power amplifiers, plus a modem that implements the 3GPP air interface. Modern flagship phones cover a few dozen 3GPP bands, essentially all of them **cellular allocations between ~600 MHz and ~6 GHz** (with the satellite-relevant, coverage-grade subset at ~600 MHz to ~2.1 GHz) ([powerfulsignal cellular bands chart](https://powerfulsignal.com/cellular-frequency-bands/), [sqimway USA FCC LTE bands](https://www.sqimway.com/lte_fcc.php)) [FACT].
- A bare phone has **no Ku/Ka/mmWave-satellite radio, no L-band MSS radio, and no antenna or filter for any non-cellular allocation**. The traditional satellite bands a broadband terminal uses (Ku 10.7-12.7 GHz, Ka 17-30 GHz, V/E-band) are simply not present in a handset's RF front end (the Starlink user-link inventory that a *dish* receives is in COMM-180..184; a phone has none of it). This is why SCS was designed around terrestrial cellular bands in the first place: it lets the satellite "speak the carrier's existing standard on the carrier's existing band, to unmodified phones," which "solves handset compatibility for free" (COMM-110). The corollary is the constraint: if a band is not already a cellular band the phone supports, the phone cannot hear the satellite on it, no matter how large the satellite antenna is.

This is the physical root the corpus already documents as the aperture-and-spectrum asymmetry (COMM-313): a broadband customer's **dish** can be pointed and can run high-order modulation on wide Ku/Ka, so broadband rides wide non-cellular spectrum; a DTC **bare phone** supplies no gain and has no non-cellular radio, so DTC is "stuck in thin ~5-10 MHz low-band cellular slices." The asymmetry is not a market accident; it is set by what the receiving device can physically do. The giant aperture compensates for the phone's weakness on the link budget; it cannot compensate for the phone's missing radios on the spectrum question.

The regulator states the same logic from the spectrum side. The FCC authorized SCS specifically on bands "previously allocated exclusively to terrestrial service," precisely so that "subscribers need no new devices" and existing unmodified smartphones work, rather than requiring "special receivers for satellite-specific frequency bands" ([Inside Global Tech, SCS rules](https://www.insideglobaltech.com/2024/04/30/fcc-acts-to-expand-satellite-to-smartphone-coverage-supplemental-coverage-from-space-rules-will-enable-partnerships-between-satellite-operators-and-wireless-network-providers-in-the/), [FCC SCS Report and Order DOC-400678A1](https://docs.fcc.gov/public/attachments/DOC-400678A1.pdf)) [FACT]. SCS exists because the only spectrum a phone can use from a satellite is the cellular spectrum it already supports.

### 1.3 The exact usable band set for DTC

The authoritative menu is the FCC SCS Report and Order's authorized-band list (the corpus previously cited the deals; this is the rule itself). SCS satellite-to-unmodified-phone operations are authorized in [FACT, FCC primary + secondary]:

| Band | Frequency edges (MHz) | 3GPP / common name | Used by |
|---|---|---|---|
| **600 MHz** | 614-652 / 663-698 | n71 low-band | (T-Mobile holds US 600 MHz) |
| **700 MHz** | 698-769, 775-799, 805-806 | n12/n13/n14/n29 low-band; FirstNet Band 14 = 758-768/788-798 | AST (FirstNet/700) |
| **800 MHz** | 824-849 / 869-894 | n5/n26 low-band (cellular 850) | AST (AT&T/Verizon 850) |
| **Broadband PCS** | 1850-1915 / 1930-1995 | n2/n25 (incl. G-block 1910-1915/1990-1995) | Starlink (T-Mobile PCS G-block 2x5 MHz) |
| **AWS H-block** | 1915-1920 / 1995-2000 | n70-adjacent | SpaceX (owned, EchoStar buy) |

Sources for the band list: [FCC SCS Report and Order (DOC-400678A1)](https://docs.fcc.gov/public/attachments/DOC-400678A1.pdf); [Inside Global Tech SCS summary](https://www.insideglobaltech.com/2024/04/30/fcc-acts-to-expand-satellite-to-smartphone-coverage-supplemental-coverage-from-space-rules-will-enable-partnerships-between-satellite-operators-and-wireless-network-providers-in-the/) [FACT, two independent statements of the same band list]. The EchoStar-owned extension adds **AWS-4 (2000-2020 up / 2180-2200 down)** and **AWS-3 unpaired uplink (~1695-1710)**, the owned ~65 MHz block near ~2 GHz that SpaceX bought outside the SCS-lease menu (COMM-186) [FACT].

Two things stand out. First, every eligible band is **at or below ~2.2 GHz**, i.e. low-band and lower-mid-band, where path loss to LEO is tolerable and the phone has radios. There is no Ku/Ka/mmWave row, because no phone could use one. Second, these are not blank bands: each one is a band incumbent carriers already hold and use terrestrially, which is the availability gate Section 2 develops. The SCS rule does not create new spectrum; it lets a satellite reuse, by lease, spectrum a carrier already owns.

**So the answer to "can you use any spectrum" is no:** you can use the ~600 MHz to ~2 GHz cellular bands the phone already supports, by lease or purchase, and nothing else. The antenna size changes the link, not the menu.

---

## 2. What Is Available, and How Much (the Carrier-Owned Gate)

### 2.1 The physical pool vs the available pool

Two different "how much" numbers must be kept separate.

- **The physically usable pool** (all the cellular spectrum below ~2.2 GHz that a phone could in principle use from a satellite) is on the order of a few hundred MHz when you sum the SCS-eligible bands above (600/700/800 MHz low-band plus PCS and the H/AWS-4 region). This is the universe of DTC-capable spectrum.
- **The available-to-an-entrant pool** is far smaller, because **essentially all of that low-band and lower-mid-band is already licensed to and used by terrestrial carriers**. The corpus is explicit: the prime US mid-band is fully spoken for (Verizon and AT&T hold C-band, T-Mobile holds 2.5 GHz; COMM-021), and "T-Mobile holds the best low-band (600 MHz)" (COMM-022); Section 6 of [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md) calls this "the wall a fresh entrant hits." There is no pool of unassigned DTC-grade low-band sitting idle for an entrant to license.

This is the gate. The constraint on DTC spectrum is not that the bands do not exist or that the antenna cannot use them; it is that the bands that work are owned.

### 2.2 How far real availability is from the competitive benchmark

The corpus carries a clear benchmark for "how much spectrum a competitive operator needs" (COMM-229, COMM-236) [FACT]:
- **~80-100 MHz of mid-band per operator just to launch competitive 5G** (GSMA), and
- **~200 MHz total to match an incumbent** (US carriers actually hold ~280-375 MHz of sub-7-GHz spectrum each; COMM-233..235).

Now compare what a DTC entrant can actually assemble:

| What | Spectrum held | Multiple of the ~100 MHz floor | Source |
|---|---|---|---|
| Competitive operator (benchmark) | ~100-200+ MHz | 1x to 2x+ | COMM-229, COMM-236 [FACT] |
| AST owned (Ligado L-band MSS) | ~45 MHz lower-mid-band | ~0.45x | COMM-150 [FACT] |
| SpaceX owned (EchoStar buy) | ~65 MHz near 2 GHz | ~0.65x | COMM-149, COMM-186 [FACT] |
| Starlink SCS lease (T-Mobile PCS G-block) | **2x5 MHz = 10 MHz** | **~0.1x** | COMM-185 [FACT] |
| AST SCS partner bands (700/800 via AT&T/Verizon) | partner low-band, shared | n/a (not owned) | COMM-148 [FACT] |

The realistic clean DTC holding is one to two orders of magnitude below the competitive total. The *leased* slice (today's working reality for Starlink DTC) is **2x5 MHz**, about a tenth of the ~100 MHz floor; the *owned* extreme (SpaceX's ~$17B purchase) reaches **~65 MHz**, still below the ~100 MHz launch floor and over the US alone. No DTC operator today holds a "competitive total" of clean dedicated spectrum; they ride thin leased slices or a single sub-floor owned block. The availability gate is why.

A note on why the slices are thin even before ownership: the DTC link runs at low spectral efficiency on a bare-phone link (~0.5-0.8 bps/Hz measured for Starlink; COMM-428), so DTC is "aperture-and-spectrum-starved on both ends" (COMM-313). But the binding limit on *how much* spectrum the operator holds is the ownership gate, not the efficiency: carrier aggregation would let the operator sum as many MHz as it could acquire ([`channels_aggregate_answer.md`](channels_aggregate_answer.md)); it just cannot acquire much, because the bands are owned.

---

## 3. How Would You Obtain It? The Three Routes, Side by Side

### 3.1 Route (a): Supplemental Coverage from Space (SCS) lease, ride a carrier's band

**Mechanism.** The FCC's SCS framework (adopted 2024, "Single Network Future"; rules effective **May 30, 2024**, built on 3GPP Release 17 NTN) lets a satellite operator use a terrestrial carrier's licensed band as a gap-filler, on a **secondary** basis (no harmful interference to, and no protection from, the primary terrestrial service), and **only where the terrestrial partner holds all the licenses on that channel across a geographically independent area and leases the rights to the satellite operator before the FCC grants SCS authority** (COMM-110; [FCC SCS Report and Order](https://docs.fcc.gov/public/attachments/DOC-400678A1.pdf), [Inside Global Tech](https://www.insideglobaltech.com/2024/04/30/fcc-acts-to-expand-satellite-to-smartphone-coverage-supplemental-coverage-from-space-rules-will-enable-partnerships-between-satellite-operators-and-wireless-network-providers-in-the/)) [FACT]. So the carrier partner is structurally required; you cannot do SCS on a band you have no partner for.

**Precedents** [FACT]:
- **Starlink + T-Mobile:** Starlink leases T-Mobile's **PCS G-block, 2x5 MHz (1910-1915 up / 1990-1995 down, ~1.9 GHz)**, "pursuant to a lease arrangement with T-Mobile"; FCC grant Nov 26, 2024, up to 7,500 NGSO satellites (COMM-111, COMM-185).
- **AST + AT&T/Verizon:** AST uses AT&T's and Verizon's **850 MHz plus FirstNet Band 14 / 700 MHz** under SCS, structured as commercial agreements (Verizon ~$100M), **not** a spectrum purchase; AST also holds ~45 MHz of its own lower-mid-band (COMM-111, COMM-148, COMM-150). The FCC granted AST commercial direct-to-device authority (April 2026) for up to 248 satellites using "premium low-band 700/800 MHz in coordination with Verizon, AT&T, and FirstNet" ([Via Satellite, AST FCC grant](https://www.satellitetoday.com/connectivity/2026/04/22/fcc-grants-ast-spacemobile-commercial-authorization-for-direct-to-device-service/), [BusinessWire, AST FCC authority](https://www.businesswire.com/news/home/20260422147378/en/)) [FACT].

**Cost and constraints.** Spectrum capex is **near zero** (you pay a commercial fee to the carrier, e.g. AST/Verizon ~$100M, not a license purchase) [FACT]. The cost is structural, not financial: you need a carrier partner, you ride their band on a secondary non-interfering basis, the lease can be thin (Starlink's is 2x5 MHz), and your capacity is gated by what the carrier is willing to lease in their own busy band. This is the realistic-entrant door, and it is the one both real DTC players walked through first.

### 3.2 Route (b): Buy spectrum outright

**Precedent (the only one at scale).** SpaceX is buying EchoStar's **AWS-4 + H-block + AWS-3, ~65 MHz nationwide, for ~$17B** (up to $8.5B cash + up to $8.5B stock + ~$2B interim financing for the AWS-4/H-block, plus ~$2.6B stock for AWS-3); FCC-approved 2026 with a $2.4B escrow tied to EchoStar's abandoned terrestrial buildout; licenses fully transfer ~Nov 30, 2027 (COMM-112, COMM-149, COMM-187). The ~65 MHz figure (15 MHz AWS-3 + 40 MHz AWS-4 + 10 MHz H-block) is multi-source confirmed, including the FCC grant itself and Bloomberg Law ("FCC Grants SpaceX ~65MHz of Midband Spectrum for D2D Network") ([SpaceNews, FCC approves with escrow](https://spacenews.com/fcc-approves-spacex-spectrum-deal-with-2-4-billion-escrow-condition/), [Bloomberg Law](https://news.bloomberglaw.com/bankruptcy-law/fcc-grants-spacex-65mhz-of-midband-spectrum-for-d2d-network), [DCD](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/)) [FACT]. Note the corpus's correction (COMM-188): the "~115 MHz" sometimes quoted is the total of both 2026 FCC transactions; **SpaceX received ~65 MHz, AT&T received the other ~50 MHz**.

**The "115 MHz off the shelf" is two different doors.** Worth holding clearly: the headline that SpaceX "got 115 MHz" conflates the EchoStar purchase (~65 MHz to SpaceX) with a separate AT&T transaction (~50 MHz, 30 MHz of 3.45 GHz + 20 MHz of 600 MHz). The DTC-relevant owned block is ~65 MHz (COMM-188) [FACT].

**Implied price and the entrant's bill.** The EchoStar deal implies **~$1.03/MHz-POP** (~$17B / ~65 MHz / ~342M US POPs), in the same range as US mid-band auctions and secondary deals (~$0.65-1.03/MHz-POP; COMM-238..241) [FACT on deal value, ESTIMATE on the decimal]. There is no entrant discount: you pay roughly auction prices, you just avoid waiting for an auction. Translating to a competitive **US-plus-Europe** OWNED position (COMM-245, COMM-246) [DERIVED, order-of-magnitude]:
- **100 MHz US+Europe: ~$32-46B, spectrum-only** (US ~$22-35B at $0.65-1.03/MHz-POP x ~342M POPs; Europe ~$11-20B at ~EUR 0.19-0.36/MHz-POP x ~518M POPs).
- **200 MHz US+Europe (incumbent-matching depth): ~$65-90B, spectrum-only.**

These are license-only figures, before satellites, ground, or operations, and they assume a flat $/MHz-POP (real auctions vary 2-3x by market), so treat them as entry-cost anchors, not a bid (COMM-245 caveat).

**The catch specific to a satellite entrant.** The only blocks a satellite operator can actually buy are **distressed MSS / satellite holdings** (EchoStar's AWS-4/H-block/AWS-3, Ligado's L-band), because those started as satellite/MSS spectrum and their owners were financially pressured (COMM, Door 3 in `spectrum_purchase_and_6g.md`). Prime cellular bands (C-band, AWS, 600/700 MHz) are held by carriers who are not selling their core spectrum, and the FCC applies an "enhanced factor" review to any buyer aggregating roughly one-third or more of suitable sub-1-GHz spectrum (COMM-242). So the outright-purchase door is narrow (a handful of MSS holders), the supply is finite, and the recent buyer (SpaceX) set the price as a hyperscaler.

### 3.3 Route (c): Auctions and new allocations, including 6G

**No greenfield cellular low/mid-band is left to auction.** The last greenfield US mid-band slice (C-band, Auction 107) cost ~$80.9B; there is no comparable unassigned cellular block queued for auction (COMM-001, COMM-002; Section 8 of [`spectrum_fundamentals_economics.md`](spectrum_fundamentals_economics.md)) [FACT]. So the auction door for DTC-grade bands is effectively closed in the near term.

**The one greenfield is 6G upper mid-band (FR3), and it is not for a satellite DTC entrant** (COMM-247, COMM-248) [FACT on bands/framing, trajectory call on access]:
- **What:** 6G's new spectrum is FR3 (7.125-24.25 GHz), with the WRC-27 study bands **7.125-8.4 GHz (the "golden band"), 4.4-4.8 GHz, and 14.8-15.35 GHz** (quote the union of the corpus's two subsets to avoid a false contradiction: 4.4-4.8, 7.125-8.4, 12.7-13.25, 14.8-15.35 GHz). FR3 can offer >400 MHz per operator vs ~100 MHz in FR1.
- **Status:** not allocated to mobile, not auctioned, owned by no carrier for mobile today; currently FSS/Fixed Service/federal incumbents. National auctions would follow WRC-27 identification (Nov-Dec 2027), so **~2028-2032+** before any FR3 mobile licenses sell. This is the one place the "all the good spectrum is already filed" wall is not yet built.
- **Can a satellite entrant get it? Largely no.** WRC-27 Agenda Item 1.7 is framed for the **terrestrial** component of IMT, and the physics is hostile to a phone-to-LEO link at 7-15 GHz (high path loss, NLOS uplink to a handset). The satellite role at FR3 is incumbent FSS/NTN coexistence (adjacent 10.7-12.7 GHz, 13.85-14 GHz), not a new mobile allocation. 3GPP NTN (Release 19/20) keeps the satellite tier on MSS/FSS bands as a complementary coverage layer, not a claim on the FR3 mobile pie. So FR3 changes the *terrestrial competitor's* capacity, not the entrant's DTC spectrum options.

**Net on route (c):** for a DTC entrant, auctions and new allocations are not a near-term door. The bands the phone can use are not being auctioned (they are owned), and the bands being opened (FR3/6G) are terrestrial and physically wrong for LEO-to-handset. The DTC spectrum path stays on routes (a) and (b).

### 3.4 The three routes at a glance

| Route | What you get | Spectrum capex | Key requirement / catch |
|---|---|---|---|
| **(a) SCS lease** | Ride a carrier's existing 5-40 MHz cellular band (Starlink: 2x5 MHz PCS; AST: 700/800 partner) | **Near zero** (commercial fee, e.g. ~$100M) | Need a carrier partner who holds all licenses on the channel and leases them; secondary/non-interfering; thin slice |
| **(b) Buy outright** | Own a dedicated block (~65 MHz precedent) | **~$17B for ~65 MHz US (EchoStar); ~$32-90B for 100-200 MHz US+Europe** | Only distressed MSS/satellite holdings are buyable; finite supply; hyperscaler-set price; FCC aggregation review |
| **(c) Auction / 6G** | Nothing DTC-grade near-term | n/a (no DTC-band auctions) | No greenfield cellular low/mid-band left; FR3/6G is terrestrial and physics-hostile to LEO-handset; ~2028-2032+ |

---

## 4. The Entrant's Realistic Position (Honest Options, No Verdict)

Given the gate, a Rocket Lab style new entrant has effectively **two real doors**, and the choice between them is the whole spectrum question for a DTC business.

**Door A: the carrier partnership (SCS lease).** Near-zero spectrum capex; fast to stand up; legally enabled by the 2024 SCS rules. You ride a carrier's existing low/lower-mid band (the realistic working slice today is ~2x5 MHz, as Starlink does; AST's 700/800 partner arrangement is wider but still partner-held and shared). The costs are structural: you must secure a carrier partner (they hold the spectrum and the customer relationship), you operate secondary and non-interfering in their band, and your DTC capacity is bounded by what they are willing to lease in spectrum they are also using terrestrially. This is the door both incumbents (Starlink, AST) walked through first, and it is the only door that does not require a multi-billion spectrum outlay.

**Door B: the multi-billion purchase.** You own a dedicated block, free of a carrier's day-to-day control, which is the architecture SpaceX is moving toward with the EchoStar buy. But the only buyable blocks are distressed MSS/satellite holdings (EchoStar, Ligado), that supply is finite (and SpaceX just took the largest piece), ~65 MHz cost ~$17B over the US alone, and a competitive US-plus-Europe owned position is ~$32-90B spectrum-only, before any satellites. This is a hyperscaler's move, not a typical new entrant's.

**There is no Door C of the form the founder's question probes ("use a wide clean band because the antenna is big").** The antenna decouples bandwidth from aperture in physics, but the unmodified phone re-couples the entrant to the ~600 MHz-to-2 GHz cellular bands it can actually receive, and those bands are owned. A 25 m^2 (or larger) aperture buys link quality and per-beam rate on whatever cellular band you hold; it does not let you transmit DTC on Ku/Ka/mmWave or on any clean unallocated band, because no handset could hear it. So the realistic entrant's spectrum is exactly: lease a carrier's cellular slice (Door A), or buy a distressed MSS block for billions (Door B). The aperture is the lever the operator owns; the spectrum is the lever it must lease or buy from someone who already holds it.

The honest framing for the model: spectrum is not a free input unlocked by the antenna, and it is not a single number. It is a **route choice** with two very different cost structures (near-zero-capex lease vs multi-billion purchase) and a hard ceiling set by the carrier-owned gate, and it sits upstream of every per-satellite capacity and revenue number the rest of the corpus computes.

---

## 5. What This Adds to the Model

1. **The antenna does not unlock spectrum; the phone gates it.** Aperture and bandwidth are independent (the premise is right), but the unmodified handset can only receive existing cellular bands (~600 MHz to ~2 GHz), so DTC spectrum is confined to the SCS-eligible cellular set regardless of antenna size. [FACT]
2. **The exact usable DTC band set is now sourced to the FCC SCS Report and Order:** 600/700/800 MHz, Broadband PCS (~1.9 GHz), AWS H-block (~2 GHz), plus the owned AWS-4/AWS-3 extension. No Ku/Ka/mmWave row exists, because no phone could use one. [FACT]
3. **The binding constraint is the carrier-owned gate, not physics or efficiency.** All DTC-grade low-band is owned; the realistic clean holding (2x5 MHz leased, ~65 MHz owned at the extreme) sits one to two orders of magnitude below the ~100-200 MHz competitive benchmark. [FACT/DERIVED]
4. **Three acquisition routes, two real doors.** SCS lease (near-zero capex, carrier-partner-gated, thin slice) vs outright purchase (~$17B/~65 MHz US; ~$32-90B for 100-200 MHz US+Europe; distressed-MSS-only). Auction/6G is not a near-term DTC door (no greenfield cellular bands; FR3 is terrestrial and physics-hostile to LEO-handset). [FACT/DERIVED]
5. **Spectrum is a route choice upstream of the capacity model.** It is not a free antenna-unlocked input; the lease-vs-buy decision sets a different cost structure and a different capacity ceiling before any per-satellite number is computed. [DERIVED]

---

## 6. Open Questions / Named Gaps

- **How wide a partner lease could an entrant actually secure?** Starlink's lease is 2x5 MHz; AST's partner footprint is wider (700/800 across AT&T/Verizon/FirstNet). The realistic MHz a *new* entrant (no existing carrier relationship) could lease is **[UNKNOWN]**: it depends on a willing partner with contiguous holdings, which is a commercial unknown, not a published number.
- **How much buyable MSS spectrum remains after SpaceX's EchoStar buy?** The distressed-MSS pool (EchoStar, Ligado) is finite and SpaceX took the largest piece. What is left for a new entrant via the purchase door, and at what price, is **[UNKNOWN]** (flagged as an open question in `spectrum_purchase_and_6g.md` too).
- **Could any clean new low-band come available?** No greenfield cellular low-band is currently queued; whether a future reallocation (e.g. a band cleared from another use) could open a clean DTC-grade low slice is **[UNKNOWN]** and not on any current auction calendar.
- **Will any FR3/6G band ever carry an NTN identification?** The most decision-relevant 10-year open item: whether WRC-27 (late 2027) or a later cycle opens any upper-mid-band slice to satellite mobile, or whether NTN stays confined to MSS/FSS + SCS leases. Current trajectory is terrestrial-only, but not formally shut [FACT on trajectory; outcome UNKNOWN].
- **The aperture-to-held-MHz interaction at the system level.** This doc establishes that held MHz is gated by ownership and that aperture is independent; a combined model (how much per-beam capacity a given aperture delivers across the realistic 5-65 MHz holding) lives in the DTC capacity/system docs, not here.

---

## 7. Claims Created (COMM-481 .. COMM-492)

| Claim ID | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-481 | Aperture and held bandwidth are independent dials: antenna gain `G = 4 pi eta A / lambda^2` sets link quality (G/T, EIRP, per-beam rate), NOT how many MHz the operator is licensed to hold; carrier aggregation sums separately-held channels so total capacity tracks total MHz held. The founder's premise (a 25 m^2 antenna does not force a 25 MHz signal) is correct. | Aperture != bandwidth | DERIVED | This doc Section 1.1; cross-ref `dtc_antenna_aperture_tradeoff.md` (COMM-313 formula), `channels_aggregate_answer.md` (carrier aggregation) |
| COMM-482 | But the unmodified phone re-couples a DTC entrant to existing cellular bands: a bare handset can only tune the radios it physically has (band-specific front-end filters, PAs, a 3GPP modem), which cover cellular allocations ~600 MHz to ~6 GHz (coverage-grade DTC subset ~600 MHz-2.1 GHz); it has NO Ku/Ka/mmWave-satellite, L-band MSS, or any non-cellular radio. So the antenna size does not unlock arbitrary spectrum: there is no handset that can receive a non-cellular band. | Phone radio set gates DTC spectrum | FACT | This doc Section 1.2; [powerfulsignal cellular bands](https://powerfulsignal.com/cellular-frequency-bands/), [sqimway USA FCC LTE bands](https://www.sqimway.com/lte_fcc.php), [FCC SCS R&O](https://docs.fcc.gov/public/attachments/DOC-400678A1.pdf); cross-ref COMM-110, COMM-313 |
| COMM-483 | Answer to "can you use any spectrum": NO. A DTC satellite must transmit in a cellular band the phone's chipset already supports. The FCC SCS Report and Order authorizes exactly that set; nothing outside it works to a bare phone, regardless of aperture. | Cannot use arbitrary spectrum | FACT | This doc Section 1.2-1.3; [FCC SCS R&O](https://docs.fcc.gov/public/attachments/DOC-400678A1.pdf), [Inside Global Tech SCS](https://www.insideglobaltech.com/2024/04/30/fcc-acts-to-expand-satellite-to-smartphone-coverage-supplemental-coverage-from-space-rules-will-enable-partnerships-between-satellite-operators-and-wireless-network-providers-in-the/); cross-ref COMM-313 |
| COMM-484 | The FCC SCS Report and Order authorizes satellite-to-unmodified-phone operation in: 600 MHz (614-652 / 663-698), 700 MHz (698-769, 775-799, 805-806; incl. FirstNet Band 14 758-768/788-798), 800 MHz (824-849 / 869-894), Broadband PCS (1850-1915 / 1930-1995; incl. G-block 1910-1915/1990-1995), and AWS H-block (1915-1920 / 1995-2000). Every eligible band is at/below ~2 GHz; there is no Ku/Ka/mmWave band, because no phone could use one. | SCS authorized band list (exact edges) | FACT | This doc Section 1.3; [FCC SCS R&O DOC-400678A1](https://docs.fcc.gov/public/attachments/DOC-400678A1.pdf), [Inside Global Tech](https://www.insideglobaltech.com/2024/04/30/fcc-acts-to-expand-satellite-to-smartphone-coverage-supplemental-coverage-from-space-rules-will-enable-partnerships-between-satellite-operators-and-wireless-network-providers-in-the/) |
| COMM-485 | SCS exists specifically because the only spectrum a phone can use from a satellite is the cellular spectrum it already supports: the FCC authorized SCS on bands "previously allocated exclusively to terrestrial service" so subscribers "need no new devices" and unmodified phones work, rather than needing "special receivers for satellite-specific frequency bands." | SCS rationale = handset compatibility | FACT | This doc Section 1.2; [Inside Global Tech SCS](https://www.insideglobaltech.com/2024/04/30/fcc-acts-to-expand-satellite-to-smartphone-coverage-supplemental-coverage-from-space-rules-will-enable-partnerships-between-satellite-operators-and-wireless-network-providers-in-the/), [FCC SCS R&O](https://docs.fcc.gov/public/attachments/DOC-400678A1.pdf); cross-ref COMM-110 |
| COMM-486 | Two distinct "how much" pools: the physically usable DTC pool (all SCS-eligible cellular spectrum below ~2.2 GHz) is on the order of a few hundred MHz; the available-to-an-entrant pool is far smaller because essentially all DTC-grade low/lower-mid band is already carrier-owned (the availability GATE). | Physical pool vs available pool | DERIVED | This doc Section 2.1; cross-ref COMM-021, COMM-022 (carriers hold the prime low/mid-band) |
| COMM-487 | How far real availability is from the competitive benchmark: vs ~100 MHz mid-band to launch and ~200 MHz to match an incumbent (COMM-229/236), real DTC holdings sit one-to-two orders of magnitude below: Starlink leases 2x5 MHz (~0.1x the floor), AST owns ~45 MHz and SpaceX ~65 MHz (~0.45-0.65x), none at a "competitive total" of clean dedicated spectrum. | DTC holdings vs benchmark | DERIVED | This doc Section 2.2; COMM-150, COMM-149/186, COMM-185, COMM-229, COMM-236 |
| COMM-488 | Route (a) SCS lease: near-zero spectrum capex (commercial fee, e.g. AST/Verizon ~$100M, not a license purchase), legally enabled by the 2024 SCS rules (effective May 30, 2024), but structurally requires a carrier partner who holds all licenses on the channel and leases them before grant, operates secondary/non-interfering, and yields a thin slice (Starlink 2x5 MHz). The realistic-entrant door. | SCS lease route economics | FACT | This doc Section 3.1; [FCC SCS R&O](https://docs.fcc.gov/public/attachments/DOC-400678A1.pdf), [Inside Global Tech](https://www.insideglobaltech.com/2024/04/30/fcc-acts-to-expand-satellite-to-smartphone-coverage-supplemental-coverage-from-space-rules-will-enable-partnerships-between-satellite-operators-and-wireless-network-providers-in-the/), [Via Satellite AST grant](https://www.satellitetoday.com/connectivity/2026/04/22/fcc-grants-ast-spacemobile-commercial-authorization-for-direct-to-device-service/); cross-ref COMM-110, COMM-111, COMM-148, COMM-185 |
| COMM-489 | Route (b) buy outright: SpaceX is buying EchoStar AWS-4+H-block+AWS-3 (~65 MHz nationwide) for ~$17B, FCC-approved 2026 with a $2.4B escrow, transfer ~Nov 30 2027 (~$1.03/MHz-POP); the "~115 MHz" headline is two deals (SpaceX ~65 MHz + AT&T ~50 MHz). A competitive US+Europe OWNED position is ~$32-46B (100 MHz) to ~$65-90B (200 MHz), spectrum-only; only distressed MSS/satellite holdings are buyable, finite supply, hyperscaler-set price. | Outright purchase route cost | FACT (deal) / DERIVED (US+EU totals) | This doc Section 3.2; [Bloomberg Law ~65MHz](https://news.bloomberglaw.com/bankruptcy-law/fcc-grants-spacex-65mhz-of-midband-spectrum-for-d2d-network), [SpaceNews escrow](https://spacenews.com/fcc-approves-spacex-spectrum-deal-with-2-4-billion-escrow-condition/), [DCD](https://www.datacenterdynamics.com/en/news/spacex-acquires-echostars-aws-4-and-h-block-spectrum-for-17bn/); cross-ref COMM-149, COMM-186, COMM-188, COMM-240, COMM-245, COMM-246 |
| COMM-490 | Route (c) auction/6G is not a near-term DTC door: no greenfield US cellular low/mid-band is left to auction (last greenfield C-band cost ~$80.9B); the one greenfield is 6G upper mid-band FR3 (golden band 7.125-8.4 GHz, plus 4.4-4.8 and 14.8-15.35 GHz), but it is terrestrial-led, not yet allocated/auctioned/held, auctions ~2028-2032+, and physics is hostile to a LEO-to-handset link at 7-15 GHz, so a satellite NTN entrant should not count on it. | Auction/6G not a DTC door | FACT (status/bands) / trajectory | This doc Section 3.3; cross-ref COMM-001, COMM-002, COMM-247, COMM-248 |
| COMM-491 | The entrant's realistic position: two real doors only. Door A carrier partnership/SCS (near-zero spectrum capex, fast, but partner-gated, secondary, thin slice). Door B multi-billion purchase (own a block, but only distressed-MSS blocks are buyable, ~$17B/~65 MHz US, ~$32-90B for 100-200 MHz US+Europe). No third "use a wide clean band because the antenna is big" door, because no handset can receive a non-cellular band. | Entrant's two real doors | DERIVED | This doc Section 4; cross-ref COMM-482, COMM-488, COMM-489 |
| COMM-492 | Spectrum for DTC is a route choice (lease vs buy) with two very different cost structures, not a free antenna-unlocked input and not a single number; it sits upstream of every per-satellite capacity and revenue number, with a hard ceiling set by the carrier-owned gate. | Spectrum = upstream route choice | DERIVED | This doc Sections 4-5; cross-ref COMM-486, COMM-487, COMM-491 |

---

## 8. Confidence

**Overall: high on the gate and band set, high on route costs (corpus-sourced and re-validated), medium-high on the 6G trajectory.**

- **High:** the "phone has no non-cellular radio" point (multi-source: handset band charts + FCC SCS rationale); the SCS authorized band list with exact edges (FCC Report and Order + independent legal summary); the SCS lease mechanics and precedents (Starlink 2x5 MHz, AST 700/800); the EchoStar ~$17B / ~65 MHz purchase (FCC grant + Bloomberg Law + trade press); the carrier-owned gate (corpus COMM-021/022 + holdings).
- **High (inherited):** the route-(b) US+Europe total-dollar figures (~$32-90B) are the corpus's DERIVED order-of-magnitude anchors (COMM-245/246), carried here unchanged with their flat-$/MHz-POP caveat.
- **Medium-high:** the EchoStar ~$1.03/MHz-POP decimal (single-source on the decimal; deal value multi-source).
- **Medium-high in direction, not formally settled:** "a satellite entrant cannot get FR3/6G." The terrestrial WRC-27 framing and the LEO-to-handset physics are well-attested, but WRC-27 has not concluded; it is a trajectory call (COMM-248).

No verdict on the Rocket Lab business is rendered; this is a neutral spectrum-access base doc.
