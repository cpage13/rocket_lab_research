# Direct-to-Cell Antenna-Aperture Tradeoff: Why AST Goes Giant, Starlink Goes Smaller-and-Many, and Whether Direct-to-Cell Can Flat-Stack

**Research date:** 2026-06-22
**Purpose:** Answer the physics question underneath the launch-fit asymmetry the corpus already documents: *why* must a direct-to-cell satellite carry a giant antenna while a broadband satellite can be a small flat panel, *how* does the required satellite aperture scale with the target service level (texting vs voice vs data vs broadband-to-phone), why does AST SpaceMobile build one giant aperture on few satellites while Starlink builds a smaller aperture on many, and whether direct-to-cell could be done flat-stacking many-per-Neutron. This grounds the Neutron-launched space-communications business.
**Status:** Understanding-building input. No verdict. Link-budget arithmetic is order-of-magnitude (the public numbers are partial), and every value is flagged sourced / derived / estimate / unknown.

> **Grounds in and does not duplicate (this doc is the LINK-BUDGET / GAIN-PHYSICS layer; the corpus already owns the mechanics and the fit):**
> - [`research/competitors/large_array_folding_and_stow.md`](../competitors/large_array_folding_and_stow.md) (COMM-197..208): owns the **fold/stow mechanics** (V3 barely folds its RF aperture; AST Block 2 is a ~220-265-tile "phone-booth-to-studio-apartment" accordion; RF arrays pack to ~34-48% vs a solar membrane's ~0.01%). This doc explains *why the aperture has to be that big in the first place* (the link budget), which is the upstream cause of the fold problem that doc characterizes.
> - [`research/rocket_lab/neutron/neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md) (COMM-155/157/160/202/204/205, claims 8/11/19/20): owns the **per-launch fit arithmetic** (V3 mass-bound ~5/Neutron; AST Block 2 size-bound ~1/Neutron; 3 on Falcon 9, 1 on New Glenn, 1 on LVM3) and the ~223 m^2 / ~64 m^2 array figures and ~5,830-6,100 kg Block 2 mass. This doc takes those as given and supplies the gain-physics reason the antenna is large.
> - [`research/direct_communication/leo_constellation_coverage_minimums.md`](leo_constellation_coverage_minimums.md) (COMM-209..228): owns the **coverage floor vs capacity scaling** (continuity is geometry-governed; throughput is Shannon-x-beams-governed; AST coverage floor ~45-90 sats). This doc owns the per-satellite *aperture* lever that sits underneath both.
> - [`research/competitors/starlink_v3_v4_spectrum_incorporation.md`](../competitors/starlink_v3_v4_spectrum_incorporation.md) (COMM-178..190) and [`research/competitors/starlink_v3_specs.md`](../competitors/starlink_v3_specs.md): own the **spectrum quantity** and the V2-mini D2C ~7 Gbps / V3 D2C ~700 Gbps capacity stack. This doc cites those and does not re-derive them.
> - [`research/laser_comms/rf_limited_service.md`](../laser_comms/rf_limited_service.md): owns the **large-professional-dish advantage** for a B2B broadband sliver and the GEO-vs-LEO EIRP table. This doc generalizes that "the dish supplies the gain" insight into the broadband-vs-direct-to-cell asymmetry (Section 6).

---

## 0. Answer first (the aperture-vs-service-level relationship in one screen)

**The bare phone cannot help close the link, so the satellite antenna must supply essentially all of the gain, and the antenna area needed grows with the data rate you want. That single fact splits the market into "giant aperture" (AST, broadband-to-phone) and "modest aperture, many satellites" (Starlink, messaging-to-low-rate first). A broadband satellite escapes this entirely because the customer's dish supplies the gain on the ground, so its own antenna can be small and flat-stack.**

1. **Why direct-to-cell is fundamentally hard (the phone side).** A standard smartphone transmits ~0.2 W (~23 dBm) into a near-omnidirectional ~0 dBi antenna, so its EIRP is ~23 dBm, and SAR limits and the handful of square centimeters of phone real estate forbid making it stronger or more directional [FACT]. The satellite is ~350 to 700 km away; free-space path loss at ~1.9 GHz over that path is ~150+ dB [FACT]. The phone's signal arrives at the satellite at roughly **-130 dBm**, while an LTE QPSK signal needs about **-105 dBm** to decode, a ~25 dB shortfall the *satellite alone* must make up, because nothing about the phone can be changed [FACT, single-source link budget]. **The satellite supplies the gain the phone cannot.** [DERIVED]

2. **How the required aperture scales with service level (the core relationship).** Antenna gain is set by aperture area: `G = 4 pi eta A / lambda^2` [FACT, formula]. More gain (bigger A) buys both more receive sensitivity (G/T, the uplink from the phone) and more downlink EIRP, and link capacity rises with that gain. The revealed-by-industry mapping of **antenna area to service class**, at the ~1-2 GHz / 700-900 MHz cellular bands the systems use:

   | Operator | Satellite antenna area | Per-beam / per-cell rate | Service class | Tag |
   |---|---|---|---|---|
   | Lynk Global | **~1 to 1.5 m^2** ("pizza box") | very low | intermittent two-way **SMS** | [FACT] |
   | Globalstar (and similar small arrays) | small (sub-few-m^2) | very low | **messaging** | [FACT] |
   | Starlink Gen2 direct-to-cell | **~25 m^2** | ~2 to 4 Mbps/beam (~3.1 Mbps measured, SMS-first) | **SMS -> voice/low-rate data** | [FACT] |
   | AST BlueBird Block 1 | **~64 m^2** | (broadband-grade) | **broadband to phone** | [FACT] |
   | AST BlueBird Block 2 | **~223 m^2** | up to ~120 Mbps/cell, ~2,000-2,500 cells | **broadband to phone** | [FACT] |

   Reading the ladder: **~1 m^2 buys texting, ~25 m^2 buys a few Mbps per beam, ~60+ m^2 buys broadband-grade service to a bare phone.** Aperture is the service-level dial. [FACT for the points; DERIVED for the "dial" reading]

3. **Why AST goes giant (~64 m^2 -> ~223 m^2).** AST's target is full broadband (voice, data, video) to an unmodified 4G/5G handset, which sits at the top of that ladder, so it needs the largest aperture. AST states the rationale itself: "Given the low power and small antenna size of standard mobile phones, the satellite must provide the necessary signal strength" [FACT, AST official]. The Block 2 array's modeled gain is **~42 dBi at 880 MHz** (`G = 4 pi eta A / lambda^2` with A=223 m^2, eta~0.7), versus a terrestrial cell tower's ~16 dBi, i.e. the satellite is a vastly higher-gain "cell tower in space" to overcome the ~150+ dB path [FACT/DERIVED]. The giant aperture is the *enabling* component, not a luxury.

4. **Why Starlink goes smaller-aperture + many satellites.** Starlink's direct-to-cell payload rides the V2-mini bus with a **~25 m^2** phased array, an order of magnitude smaller in area than AST Block 2, which caps per-satellite direct-to-cell capacity (SMS first, ~3.1 Mbps/beam measured, voice/data following) but lets the satellite stay flat-stackable and fly ~20+ per Falcon 9 alongside broadband units [FACT]. Starlink "compensates with a denser constellation": direct-to-cell capability is added to a portion of new builds, so coverage and capacity scale with the thousands-strong constellation rather than a separate giant-satellite program [FACT]. The smaller aperture is a deliberate *capacity-per-satellite penalty traded for many-per-launch and constellation scale.* [DERIVED]

5. **The tradeoff, and the floor.** AST: one giant aperture, very high per-satellite capacity (~100x a Starlink D2C satellite per independent estimate), but volume-bound to ~1-2 per medium launcher, so the constellation is dozens (~45-90 for coverage, 248 authorized). Starlink: modest aperture, ~100x less per-satellite direct-to-cell capacity, but many-per-launch and thousands deployed. There **is a hard floor**: below ~1 to 1.5 m^2 of satellite antenna you get only intermittent messaging (Lynk/Globalstar), and broadband-grade service to a bare phone is not achievable below the ~50-60 m^2 class on the public evidence. [DERIVED]

6. **Can direct-to-cell flat-stack at 6-9 per Neutron? Only at the low end of the service ladder.** A messaging/low-rate direct-to-cell satellite (Lynk-class ~1 m^2, or a Starlink-class ~25 m^2 panel) is small enough to flat-stack many-per-launch, and *that* is how Starlink already flies its direct-to-cell payloads. But **broadband-to-phone forces the ~64-223 m^2 giant aperture**, which folds into a bulky stack and goes ~1 per Neutron (per the fit doc). So "6-9 per Neutron" is feasible for a **messaging/thin-data** direct-to-cell satellite and **not** for a broadband-to-phone one. The service ambition sets the aperture, the aperture sets the stow bulk, the stow bulk sets satellites-per-launch. [DERIVED]

7. **The broadband-vs-direct-to-cell asymmetry (the core reason their satellites differ in size).** A broadband customer has a **high-gain phased-array dish** (Starlink's ~1,280-element flat panel, paid for by the customer) that supplies the ground-side gain, so the *satellite's* user antenna can be small and flat-pack. A direct-to-cell customer has only a bare phone with ~0 dBi, so **all** the gain the dish would have provided must instead live on the satellite. Same physics, opposite placement of the big antenna: on the ground for broadband, in orbit for direct-to-cell. That is why broadband satellites flat-stack many-per-launch and direct-to-cell broadband satellites do not. [DERIVED, multi-source-supported]

The rest of this doc sources and derives each point.

---

## 1. The link budget to an unmodified handset: why the satellite must supply the gain

A communications link closes when the received signal exceeds the receiver's decode threshold by the required margin. The terms (Friis / standard satcom link budget):

```
P_rx (dBm) = EIRP_tx (dBm) - FSPL (dB) + G_rx (dBi) - losses
FSPL (dB)  = 20 log10(d) + 20 log10(f) + 92.45   (d in km, f in GHz)
G          = 4 pi eta A / lambda^2                (antenna gain from aperture area A, efficiency eta)
```

[FACT, formulas: standard link-budget references; the `G = 4 pi eta A / lambda^2` form is stated in the SpaceX Gen2 direct-to-cellular FCC technical narrative and the direct-to-device academic literature.]

### 1.1 The phone side is fixed and weak (this is the whole problem)

| Phone parameter | Value | Why it cannot be improved | Tag |
|---|---|---|---|
| Transmit power | **~0.2 W (23 dBm)**, up to ~1-2 W peak | SAR (specific-absorption-rate) safety limits cap radiated power near the head | [FACT] |
| Antenna gain | **~0 dBi** (near-omnidirectional) | A phone is small and held at any angle; it cannot host a directional high-gain antenna | [FACT] |
| Effective EIRP | **~23 dBm** | = 23 dBm + 0 dBi | [FACT] |
| Antenna aperture | a few cm^2 | Multiple radios already crowd the handset; no room for a satellite high-gain element | [FACT] |

A standard smartphone transmits at "roughly 0.2 to 2 watts of radio power, enough to reach a cell tower a few kilometers away" [FACT, TechTimes]; in the direct-to-device link budget it is modeled as "0.2 W (23 dBm)" into "a low gain antenna (typically 0 dBi)," for an EIRP of 23 dBm [FACT, Panariello / Frank Rayal]. SAR limits and the lack of physical space for a high-gain antenna mean **none of these phone numbers can move**, which is the defining constraint: you cannot change the phone, so you must change the satellite. [FACT/DERIVED]

### 1.2 The path eats ~150+ dB and opens a gap only the satellite can close

Frank Rayal's worked direct-to-handset link budget (the cleanest public arithmetic, single-source so flagged): at **1900 MHz**, free-space path loss to LEO is **~153 dB**, so the phone's 23 dBm EIRP arrives at the satellite at **~-130 dBm**; to decode an LTE signal at its lowest modulation (QPSK) the received power "needs to exceed -105 dBm" [FACT, single-source]. That is a **~25 dB deficit** the satellite must recover purely through its own antenna gain and low-noise receive chain, because the phone has nothing left to give. [FACT/DERIVED]

The same logic runs in the downlink: the satellite must put enough EIRP onto a ~0 dBi phone to close the forward link, and EIRP also rises with antenna gain (aperture). **So both directions, uplink sensitivity (G/T) and downlink power (EIRP), improve with one lever: a bigger satellite antenna.** [DERIVED] As the direct-to-device analysis puts it, "at parity of bandwidth, frequency and satellite orbit, the only parameters that influence the link budget are satellite EIRP in downlink and satellite G/T in uplink," both of which "the satellite service link antenna should be designed with large antenna gain achieved by increasing the antenna aperture (size)" [FACT, Panariello].

### 1.3 The minimum aperture even for a thin channel is already ~1.4 m^2

For a narrow ~5 MHz channel carrying ~32 kbps per user (messaging-grade), Frank Rayal computes the satellite needs **~29 dBi of antenna gain, corresponding to an effective aperture of ~1.4 m^2** [FACT, single-source]; for comparison a terrestrial base-station antenna in the same band is ~17 dBi / ~0.1 m^2. So **even messaging-grade direct-to-cell requires a satellite antenna ~14x the aperture of a cell tower**, and that is the *floor*: a sub-1-m^2 satellite antenna (Lynk's ~1 m^2 "pizza box") delivers only intermittent SMS. [FACT/DERIVED] Everything above messaging needs more.

---

## 2. How aperture scales with the target service level (texting -> voice -> data -> broadband)

The link from aperture to service level runs through capacity. More aperture means more gain (`G = 4 pi eta A / lambda^2`), which means a higher SNR per beam (raising the achievable spectral efficiency toward the Shannon ceiling) and a narrower beam (smaller cell, more reuse), both of which raise the deliverable rate. The corpus already owns the Shannon-x-beams capacity ceiling (COMM-108, COMM-178..190); here is the *aperture* end of it, as revealed by what each operator actually fields.

### 2.1 The revealed aperture-to-service ladder

| Service target | Representative system | Satellite antenna area | Gain (approx.) | Delivered rate | Tag |
|---|---|---|---|---|---|
| Intermittent **SMS** | Lynk Global | ~1 to 1.5 m^2 | ~29 dBi-class (floor) | two-way text | [FACT] |
| **Messaging** | Globalstar / small arrays | sub-few m^2 | low | text / IoT | [FACT] |
| **SMS -> voice / low-rate data** | Starlink Gen2 D2C | ~25 m^2 | high | ~2-4 Mbps/beam (~3.1 measured) | [FACT] |
| **Broadband to phone** | AST BlueBird Block 1 | ~64 m^2 | ~broadband-grade | voice/data/video | [FACT] |
| **Broadband to phone (high)** | AST BlueBird Block 2 | ~223 m^2 | ~42 dBi @ 880 MHz | up to ~120 Mbps/cell | [FACT/DERIVED] |

Sources: Lynk ~1-1.5 m^2 "pizza box" SMS and Globalstar messaging ([Panariello / NTN-DtD](https://www.linkedin.com/pulse/non-terrestrial-networks-satellite-direct-to-device-panariello), [Aerospace America](https://aerospaceamerica.aiaa.org/departments/direct-to-device-satellite-internet-sparks-competing-concepts/)); Starlink Gen2 ~25 m^2 at 2-4 Mbps/beam (Panariello), ~3.1 Mbps/beam measured ([arXiv crowdsourced D2C study](https://arxiv.org/html/2506.00283v6)); AST 64 m^2 / 223 m^2 and 120 Mbps/cell ([AST How-It-Works](https://ast-science.com/how-it-works/), [AST Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/)); Block 2 ~42 dBi at 880 MHz ([SpaceX/AST direct-to-device technical narratives, via the FCC-filing analysis surfaced in the spectrum-opportunities literature](https://arxiv.org/html/2506.18672v1)).

### 2.2 The sensitivity is steep (small dB, large rate change)

Because capacity rises with SNR, small gains in antenna dB move the rate a lot: the direct-to-device literature notes "an increase of 1 dB improves the rate by the factor 1.58, or increases the range by factor 1.12" [FACT, single-source academic]. Antenna gain scales with area, so going from Lynk's ~1 m^2 to AST's ~223 m^2 is a ~23 dB aperture-gain increase (`10 log10(223/1.4)` from the messaging floor is ~22 dB), which is the difference between "intermittent SMS" and "120 Mbps broadband cell." **The aperture ladder and the service ladder are the same ladder.** [DERIVED]

### 2.3 Why this is a *direct-to-cell* problem specifically

This whole ladder exists only because the phone is fixed at ~0 dBi. If the ground side could add gain (a dish), the satellite would not need to climb the aperture ladder to reach broadband, which is exactly the broadband case in Section 6. So the aperture-vs-service relationship is a property of *bare-handset* service, not of satellite broadband in general. [DERIVED]

---

## 3. Why AST goes giant (~64 m^2 Block 1, ~223 m^2 Block 2)

AST's product is full broadband (voice, data, video) to an *unmodified* 4G/5G phone, the top of the service ladder, so it needs the top of the aperture ladder.

### 3.1 AST's own stated rationale

AST states the physics directly: **"Given the low power and small antenna size of standard mobile phones, the satellite must provide the necessary signal strength. To compensate, our BlueBird 1-5 satellites use 693 sq ft [~64 m^2] phased array antennas, the largest commercial arrays ever deployed in low Earth orbit"** [FACT, AST official How-It-Works]. The next-generation BlueBirds are "3x larger with 10x the data capacity" (the ~223 m^2 Block 2), and "each BlueBird can deliver up to 120 Mbps per coverage cell across more than 2,000 cells" [FACT, AST official]. AST describes "the largest phased antenna arrays in low Earth orbit in order to capture the weak signal from your phone," with "the larger aperture [translating] directly into signal gain, the ability to detect the faint uplink from a phone... and return a downlink strong enough for broadband data" [FACT, AST / TechTimes].

### 3.2 The independent gain numbers

- **Block 2 gain ~42 dBi at 880 MHz**, computed as `G = 4 pi eta A / lambda^2` with A = 223 m^2 and efficiency ~0.7, per the direct-to-device technical analysis of AST's FCC filings [FACT/DERIVED, the formula is FCC-narrative; the 42 dBi is a derived value in the literature]. AST publicly characterizes its aperture as delivering gain "north of 40 dBi," versus ~16 dBi for a standard terrestrial tower [FACT, single-source academic restatement].
- **A 40 MHz beam at AST's spectral efficiency supports ~120 Mbps downlink**, the per-cell figure AST quotes [FACT, AST + academic].
- AST's BlueWalker 3 prototype (the 64 m^2 test article) demonstrated **~21 Mbps** to a phone, an early validation that a 64 m^2-class aperture reaches real broadband-ish rates [FACT, multi-source].

### 3.3 The consequence AST accepts

The giant aperture is the binding launch-volume constraint (per [`neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md): 3 Block 2 on a Falcon 9, 1 on New Glenn, 1 on LVM3, ~1 on Neutron) and drives a ~6 t satellite costing ~$19-21 M to build. AST accepts few-but-giant satellites because *broadband to a bare phone cannot be done any other way on the aperture physics.* The constellation is correspondingly small: ~45-90 satellites for coverage, 248 authorized (COMM-155/157), not thousands. [DERIVED]

---

## 4. Why Starlink goes smaller-aperture + many satellites

Starlink made the opposite aperture choice for direct-to-cell, and pays a per-satellite capacity penalty for it on purpose.

### 4.1 The ~25 m^2 antenna and what it buys

Starlink's direct-to-cell payload is a variant of the V2-mini bus (~4.1 m x 2.7 m body before solar deployment) carrying a **~25 m^2 phased array** dedicated to cellular [FACT]. That antenna "forms narrow beams that concentrate the satellite's receiving sensitivity on small geographic areas, improving the signal-to-noise ratio enough to pick up a phone's weak transmission" [FACT]. It is an order of magnitude smaller in area than AST Block 2 (~223 m^2), so it sits lower on the service ladder: SMS first, then voice/low-rate data, at **~2-4 Mbps/beam** (Panariello), **~3.1 Mbps/beam measured** during the SMS-only phase at 0.52-0.61 bps/Hz on the PCS G-block 2x5 MHz channel ([arXiv crowdsourced study](https://arxiv.org/html/2506.00283v6)).

### 4.2 The many-satellites compensation

Starlink "compensates with a denser constellation": direct-to-cell capability is added to a portion of new V2-mini/V3 builds, deployed ~20+ per Falcon 9, so direct-to-cell coverage and aggregate capacity scale with the thousands-strong constellation rather than a separate giant-satellite program [FACT]. The corpus already documents the V3 direct-to-cell roadmap: a *separate* up-to-15,000-satellite dedicated direct-to-cell fleet at ~326-335 km targeting ~700 Gbps/sat (COMM in [`starlink_v3_specs.md`](../competitors/starlink_v3_specs.md)). Even there, the per-satellite aperture stays far below AST's: SpaceX buys capacity with *more satellites and more spectrum* (the ~65 MHz EchoStar block, COMM-186/187), not a single giant aperture. [FACT/DERIVED]

### 4.3 The capacity penalty, quantified

Independent estimates put **each AST Block 2 array at ~35-40x the area of a Starlink direct-to-cell antenna and ~100x the bandwidth/capacity per satellite** ([newspacetracker](https://newspacetracker.com/articles/direct-to-smartphone-satellites/), [Aerospace America](https://aerospaceamerica.aiaa.org/departments/direct-to-device-satellite-internet-sparks-competing-concepts/)). So Starlink's smaller aperture is roughly a two-orders-of-magnitude per-satellite capacity penalty for direct-to-cell, which it recovers by flying ~two-to-three orders of magnitude more satellites. **The two companies land at comparable system capacity from opposite ends of the aperture-vs-count tradeoff.** [DERIVED, the ~100x and the constellation-scale offset are from separate sources, so the "comparable system capacity" netting is reasoned, not directly sourced.]

---

## 5. The tradeoff, quantified, and the floor

### 5.1 One-giant-aperture-few-satellites vs moderate-aperture-many-satellites

| Axis | **AST (giant aperture, few satellites)** | **Starlink (moderate aperture, many satellites)** | Tag |
|---|---|---|---|
| Satellite antenna area | ~64 m^2 (Block 1) -> ~223 m^2 (Block 2) | ~25 m^2 (D2C payload) | [FACT] |
| Satellite gain (cellular band) | ~42 dBi @ 880 MHz (Block 2) | high but ~an order of magnitude less area | [FACT/DERIVED] |
| Service reached | full broadband (up to ~120 Mbps/cell) | SMS -> voice/low-rate data (~3.1 Mbps/beam now) | [FACT] |
| Per-satellite D2C capacity | ~100x a Starlink D2C satellite | baseline | [FACT, independent estimate] |
| Satellites per medium launch | ~1-3 (size-bound; ~1/Neutron) | ~20+ (flat-stack, shared with broadband) | [FACT, fit doc] |
| Constellation size | dozens (~45-90 coverage; 248 authorized) | thousands (D2C scales with the broadband fleet; up to 15,000 dedicated filed) | [FACT] |
| Launch-cost lever | spread one giant-satellite launch over 1-3 satellites | spread one launch over ~20+ | [DERIVED] |

**Net on total system capacity:** AST concentrates capacity into few high-aperture nodes; Starlink spreads it across many low-aperture nodes. Per the independent ~100x-per-satellite and the ~100-1,000x-more-satellites figures, both can reach comparable aggregate direct-to-cell capacity, by opposite routes. [DERIVED]

**Net on per-bit launch cost:** the corpus's fit doc already carries this (claim 21 there): on Neutron, ~1 giant Block 2 per launch loads ~$50-55 M of launch cost on one satellite, while a flat-stack of small satellites spreads the same launch over ~20+. So for a *given launcher*, the moderate-aperture-many-satellites architecture has the far lower launch cost per satellite and (because each small satellite still carries real capacity) plausibly the lower launch cost per delivered bit, *at the messaging/low-rate service level*. The giant-aperture architecture only wins per-bit if broadband-to-phone (which the small aperture cannot deliver) is what the market pays for. [DERIVED]

### 5.2 The floor on satellite antenna size

There is a hard lower bound below which direct-to-cell is not meaningfully viable:

- **Below ~1 to 1.5 m^2:** only intermittent two-way SMS (Lynk-class). The ~29 dBi / ~1.4 m^2 figure is the computed floor for even a thin ~32 kbps channel [FACT, single-source].
- **~25 m^2:** SMS, then voice and a few Mbps per beam (Starlink-class). [FACT]
- **~50-60+ m^2:** broadband-grade service to a bare phone becomes achievable (AST Block 1 at 64 m^2 demonstrated ~21 Mbps on BlueWalker 3). [FACT]

So **meaningful direct-to-cell starts around ~1 m^2 (messaging) and broadband-to-phone starts around ~60 m^2.** A satellite antenna materially below ~1 m^2 cannot close the bare-handset link at a useful service level. [DERIVED]

---

## 6. Can direct-to-cell be flat-stacked at 6-9 per Neutron?

**Only for a messaging / thin-data service, not for broadband-to-phone.** The answer is set entirely by which rung of the aperture ladder the service requires.

### 6.1 The flat-stack regime (low end of the ladder): yes

A messaging or low-rate direct-to-cell satellite carries a small antenna (Lynk ~1 m^2; Starlink-class ~25 m^2 panel) that either is a flat panel already or folds only modestly. Starlink **already flies its direct-to-cell payloads flat-stacked**, ~20+ per Falcon 9 on the V2-mini bus [FACT]. A ~25 m^2-class panel is far less bulky stowed than a ~223 m^2 accordion (the fold mechanics are in [`large_array_folding_and_stow.md`](../competitors/large_array_folding_and_stow.md)), so on Neutron's 5.5 m fairing a **messaging/thin-data direct-to-cell satellite could plausibly stack at the multi-per-launch level** the prompt asks about. The exact count (whether 6-9 specifically) depends on the panel's stowed dimensions, which are not published, so the count itself is UNKNOWN, but the *regime* (many-per-launch) is the same one Starlink demonstrates. [DERIVED; specific 6-9 count UNKNOWN]

### 6.2 The broadband-to-phone regime (top of the ladder): no

Broadband-to-phone forces the ~64-223 m^2 giant aperture (Sections 2-3). That aperture folds into a bulky multi-tile accordion that the fit doc shows goes ~1 per Neutron (3 on Falcon 9, 1 on New Glenn, 1 on LVM3). **No fold efficiency rescues a broadband-to-phone aperture into a 6-9-per-Neutron flat stack**; the corpus's fold-mechanics doc caps RF-aperture packing at the ~34-48% / phone-booth class, far short of a thin-wafer flat stack (COMM-207). So a broadband direct-to-cell satellite is ~1 per Neutron, full stop. [DERIVED]

### 6.3 The implication for a Neutron-launched direct-to-cell business

The launcher does not change the physics; the *service ambition* sets the aperture, and the aperture sets satellites-per-launch:

- **Aim at messaging / thin-data direct-to-cell** and Neutron can fly a many-per-launch flat stack (the favorable launch economics regime), competing on cadence and dedicated insertion.
- **Aim at broadband-to-phone** and Neutron is pinned near ~1 giant satellite per launch (the unfavorable regime the fit doc documents), out-scaled by a Starship-class batch lifter.

This is the strategic fork for the comms thesis: the aperture ladder is also a launch-economics ladder, and Neutron's 5.5 m fairing is comfortable on the low rungs and binding on the high ones. [DERIVED]

---

## 7. The broadband-vs-direct-to-cell asymmetry (why their satellites differ in size at all)

This is the single cleanest way to state the whole result, and it is the founder's underlying question made explicit.

**The gain a link needs is fixed by the physics; what differs is *where* you put the big antenna.**

| | **Broadband (dish-served)** | **Direct-to-cell (bare phone)** |
|---|---|---|
| Ground-side antenna | High-gain phased-array **dish** (~1,280 elements, the customer pays for it) | Bare phone, ~0 dBi, near-omnidirectional | 
| Who supplies the ground-side gain | **The customer's dish** | Nothing; the phone cannot | 
| Therefore the satellite's user antenna | can be **small and flat-pack** (the dish already closed the link) | must be **giant** (it supplies the gain the dish would have) | 
| Stow behavior | flat panel, dense-stack, many-per-launch (V3) | folded accordion, ~1-3 per medium launcher (broadband-grade) | 
| Binding launch gate | **mass** | **stowed size (antenna)** | 

[FACT/DERIVED; the dish-supplies-the-gain mechanism is multi-source, and the satellite-size consequence is the corpus's documented mass-vs-size asymmetry.]

The mechanism, stated plainly: a Starlink broadband user terminal is "a large user terminal dish with multiple antenna elements for gain," whereas "the newer direct-to-cell approach puts the large antenna arrays on the satellites themselves, allowing ordinary phones to connect without any dish" [FACT, multi-source]. **The big antenna is on the ground for broadband and in orbit for direct-to-cell.** That single relocation is why a broadband satellite is a flat ~7 m panel that stacks ~5 per Neutron (mass-bound) while a broadband-to-phone satellite is a ~223 m^2 folded aperture that goes ~1 per Neutron (size-bound). The corpus already documents the *consequence* (the mass-vs-size launch asymmetry, COMM-208); this doc supplies the *cause* (the gain has to live somewhere, and a bare phone forces it onto the satellite). [DERIVED]

A second-order corollary worth noting: this also explains the **spectrum** asymmetry the corpus documents. Broadband rides wide Ku/Ka spectrum because the dish-closed link can run high-order modulation; direct-to-cell is stuck in thin ~5-10 MHz low-band cellular slices (COMM-185/186) partly because the bare-handset link runs at low spectral efficiency (~0.5-0.6 bps/Hz measured for Starlink SMS), so direct-to-cell capacity is *aperture-and-spectrum-starved on both ends*. The giant aperture is the operator's only lever it fully controls; the spectrum it must buy or lease (COMM-187, the ~$17B EchoStar deal). [DERIVED, ties to existing claims]

---

## 8. So what (for the Neutron comms thesis)

1. **The aperture is the direct-to-cell service-level dial, and it is a hard physical relationship.** ~1 m^2 = texting, ~25 m^2 = a few Mbps/beam, ~60+ m^2 = broadband-to-phone. A Neutron-launched direct-to-cell business must pick its rung knowingly, because the rung sets everything downstream.
2. **The rung sets satellites-per-launch, and therefore the launch economics.** Low rungs flat-stack many-per-Neutron (good economics, the regime Starlink already exploits); the broadband rung is ~1-per-Neutron (the regime the fit doc shows Neutron loses on versus a batch lifter).
3. **AST's giant aperture is forced by its broadband-to-phone ambition, not a design preference**, and AST says so itself ("the satellite must provide the necessary signal strength"). Starlink's smaller aperture is forced by its flat-stack-many-satellites strategy and a lower (for now) service target.
4. **The broadband-vs-direct-to-cell asymmetry is the load-bearing insight:** the customer's dish supplies the gain for broadband, so its satellite antenna is small; the bare phone supplies nothing, so its satellite antenna is giant. This is *why* the two satellite classes differ in size, and it is the cause underneath the corpus's already-documented mass-vs-size launch asymmetry.
5. **No verdict.** This doc establishes the physics and the tradeoff; whether a Neutron-launched direct-to-cell business closes depends on the service target chosen (Section 6), the spectrum it can access (existing COMM-185..188), the coverage floor (COMM-209..228), and the launch economics (fit doc), none assessed here.

---

## Open questions / uncertainties

1. **The handset link budget is single-sourced.** The ~153 dB FSPL / ~-130 dBm received / ~-105 dBm QPSK floor / ~29 dBi / ~1.4 m^2 chain is from one worked analysis (Frank Rayal). The *shape* (a ~25 dB satellite-must-supply gap, aperture as the lever) is corroborated by AST's own framing and the Panariello service ladder, but the exact dB values would benefit from a second independent link budget. [single-source on the exact numbers]
2. **The aperture-to-service ladder is revealed, not derived from first principles here.** The ~1 m^2 = SMS / ~25 m^2 = few-Mbps / ~64 m^2 = broadband mapping comes from what operators field, not a closed-form capacity-vs-area curve in this doc. A first-principles curve (capacity vs aperture at fixed spectrum/orbit) would sharpen the floor. [DERIVED, empirical]
3. **Starlink direct-to-cell antenna area is "~25 m^2," loosely sourced.** The ~25 m^2 figure recurs across trade press; the satellite body is ~4.1 m x 2.7 m, and whether 25 m^2 is the physical panel or an effective/deployed figure is not crisply pinned. [FACT, but the precise area is soft]
4. **The "~100x per-satellite capacity" AST-vs-Starlink ratio is an independent estimate**, not an apples-to-apples disclosed measurement (different bands, spectrum, beam counts, service definitions). Treat as order-of-magnitude. [estimate]
5. **The 6-9-per-Neutron count for a messaging direct-to-cell satellite is a regime claim, not a computed count.** The stowed dimensions of a ~25 m^2-class direct-to-cell panel on a Neutron fairing are not published, so the specific number is UNKNOWN; only the many-per-launch *regime* is established (by Starlink's flat-stack precedent). [UNKNOWN on the exact count]
6. **The 42 dBi Block 2 gain is derived from the aperture formula in the FCC narrative**, with an assumed ~0.7 efficiency; AST's public "north of 40 dBi" corroborates the magnitude but the exact realized gain (and at which band, since AST spans 700-900 MHz) is not a single disclosed datasheet number. [DERIVED]
7. **Voice/data service levels are moving targets.** Starlink direct-to-cell was SMS-only through mid-2025 with voice/data "planned"; AST broadband-to-phone is largely prototype-and-early-deployment. The service-class column will shift as both mature; the *aperture* relationship that sets the ceiling does not. [time-sensitive]

---

## Sources

Link budget and aperture physics:
- [Non-Terrestrial Networks, Satellite Direct-to-Device, when antenna dimensions matter (Panariello, LinkedIn): the aperture-to-service ladder (AST 64 m^2 broadband; Starlink Gen2 25 m^2 at 2-4 Mbps/beam; Globalstar messaging; Lynk 1-1.5 m^2 SMS); EIRP/G-T as the only link-budget levers; large aperture as the gain lever](https://www.linkedin.com/pulse/non-terrestrial-networks-satellite-direct-to-device-panariello)
- [T-Mobile + SpaceX Direct Satellite-to-Handset Service: Lots of Hype and Little Reality (Frank Rayal): the worked handset link budget, 1900 MHz / 153 dB FSPL / -130 dBm received / -105 dBm QPSK floor / 29 dBi / 1.4 m^2 minimum aperture; 5 MHz / 32 kbps; messaging-not-broadband](https://frankrayal.com/2022/08/29/t-mobile-spacex-direct-satellite-to-handset-service-lots-of-hype-and-little-reality/)
- [Spectrum Opportunities for the Wireless Future: From Direct-to-Device Satellite Applications to 6G Cellular (arXiv 2506.18672, HTML): G = 4 pi eta A / lambda^2; Block 2 ~42 dBi at 880 MHz from 223 m^2 / 0.7 efficiency; 40 MHz beam -> 120 Mbps; AST gain "north of 40 dBi" vs ~16 dBi tower; 1 dB -> 1.58x rate / 1.12x range](https://arxiv.org/html/2506.18672v1)
- [Designing Efficient Satellite Links: A Review of the Link Budget Analysis (Qorvo): standard satcom link-budget framework, EIRP/G-T, large-antenna advantage](https://www.qorvo.com/design-hub/blog/designing-efficient-satellite-links-a-review-of-the-link-budget-analysis)
- [Satellite uplink G/T explanation for link budget calculations (satsig.net)](https://www.satsig.net/lbgt.htm)

AST SpaceMobile (giant aperture):
- [How it Works, AST SpaceMobile (official): "Given the low power and small antenna size of standard mobile phones, the satellite must provide the necessary signal strength"; 693 sq ft / ~64 m^2 Block 1; capture the faint phone uplink](https://ast-science.com/how-it-works/)
- [Next-Generation BlueBird, AST SpaceMobile (official): ~223 m^2 / nearly 2,400 sq ft, 3x larger / 10x capacity, up to 120 Mbps/cell across 2,000+ cells](https://ast-science.com/next-gen-bluebird/)
- [AST SpaceMobile Block 2 BlueBirds Reach Orbit (TechTimes): smartphone 0.2-2 W; the link-budget problem; ~35-40x more signal gain per satellite; 35-40x larger than Starlink D2C antenna; broadband vs messaging](https://www.techtimes.com/articles/318740/20260620/ast-spacemobile-block-2-bluebirds-reach-orbit-satellite-broadband-direct-your-phone-nears.htm)
- [AST SpaceMobile, Wikipedia (Block 2 223 m^2, 120 Mbps, gain rationale)](https://en.wikipedia.org/wiki/AST_SpaceMobile)

Starlink direct-to-cell (moderate aperture, many satellites):
- [Direct-to-Cell: A First Look into Starlink's Direct Satellite-to-Device RAN through Crowdsourced Measurements (arXiv 2506.00283): ~3.1 Mbps/beam, 0.52-0.61 bps/Hz, SMS-only Oct 2024-Jul 2025, PCS G-block 2x5 MHz, ~400 sats; AST contrast (less dense, higher altitude, very large arrays)](https://arxiv.org/html/2506.00283v6)
- [SpaceX unveils first batch of larger upgraded Starlink satellites (Spaceflight Now): V2-mini bus ~4.1 x 2.7 m, more powerful phased arrays](https://spaceflightnow.com/2023/02/26/spacex-unveils-first-batch-of-larger-upgraded-starlink-satellites/)
- [Your Phone Already Talks to Space (KeepTrack): Starlink D2C ~25 m^2 deployable array, narrow beams to lift SNR enough to hear a phone; dish-vs-no-dish framing](https://keeptrack.space/deep-dive/starlink-direct-to-cell)

The tradeoff and the asymmetry:
- [Direct-to-device satellite internet sparks competing concepts (Aerospace America / AIAA): AST ~200 sats, large antennas / more powerful beams / fewer satellites (63 -> 223 m^2, thousands of 48-km beams, 5,600 km^2/sat); Starlink dense low-altitude, smaller D2C antenna / lower gain / denser constellation; Lynk/Globalstar small antennas / messaging](https://aerospaceamerica.aiaa.org/departments/direct-to-device-satellite-internet-sparks-competing-concepts/)
- [Direct-to-Smartphone Satellites: AST SpaceMobile, Starlink (New Space Tracker): AST 223 m^2 vs ~65 sq ft Starlink, 35-40x size, ~100x bandwidth per satellite; large-antenna-few-sats vs small-antenna-many-sats](https://newspacetracker.com/articles/direct-to-smartphone-satellites/)
- *(Per-launch fit, fold mechanics, coverage floors, spectrum quantities cross-referenced from `neutron_comms_payload_fit.md`, `large_array_folding_and_stow.md`, `leo_constellation_coverage_minimums.md`, `starlink_v3_specs.md`, `starlink_v3_v4_spectrum_incorporation.md`; not re-listed.)*

---

## Claims ledger (COMM-293..314)

For the catalog step to ingest. Each hard claim with sources and tag. IDs COMM-293 through COMM-314 reserved for this doc.

- **COMM-293**, A standard smartphone for direct-to-cell is fixed at ~0.2 W (23 dBm) transmit into a ~0 dBi near-omnidirectional antenna (EIRP ~23 dBm), and SAR limits plus the lack of physical space for a high-gain element mean none of this can be improved; the phone cannot help close the link. [FACT] Sources: Panariello (0.2 W / 23 dBm / 0 dBi / 23 dBm EIRP); Frank Rayal; TechTimes (0.2-2 W).
- **COMM-294**, In the direct-to-cell uplink at ~1900 MHz to LEO, free-space path loss is ~153 dB, the phone's signal arrives at the satellite at ~-130 dBm, and an LTE QPSK signal needs ~-105 dBm to decode, a ~25 dB deficit the satellite alone must recover. [FACT, single-source on the exact numbers] Source: Frank Rayal worked link budget.
- **COMM-295**, Both link directions improve with one lever: satellite antenna gain (aperture). Uplink sensitivity (G/T) and downlink EIRP both rise with antenna area; at parity of bandwidth/frequency/orbit, satellite EIRP (down) and G/T (up) are the only link-budget parameters, both maximized by increasing antenna aperture. [FACT] Sources: Panariello; Qorvo link-budget review.
- **COMM-296**, Antenna gain follows G = 4 pi eta A / lambda^2 (effective aperture area A, efficiency eta); this is the formula tying satellite antenna size to gain and is stated in SpaceX/AST direct-to-device FCC technical narratives. [FACT, formula] Sources: SpaceX Gen2 D2C FCC technical narrative (formula); arXiv 2506.18672.
- **COMM-297**, Even a thin ~5 MHz / ~32 kbps (messaging-grade) direct-to-cell channel requires ~29 dBi of satellite antenna gain, an effective aperture of ~1.4 m^2, about 14x the ~0.1 m^2 / ~17 dBi of a terrestrial base-station antenna; this is the aperture floor. [FACT, single-source] Source: Frank Rayal.
- **COMM-298**, The revealed aperture-to-service-level ladder for bare-handset service: ~1-1.5 m^2 (Lynk) = intermittent SMS; small arrays (Globalstar) = messaging; ~25 m^2 (Starlink Gen2) = SMS then a few Mbps/beam; ~64 m^2 (AST Block 1) = broadband; ~223 m^2 (AST Block 2) = up to 120 Mbps/cell. Aperture is the direct-to-cell service dial. [FACT for the points; DERIVED for the "dial" reading] Sources: Panariello; Aerospace America; AST official; arXiv 2506.00283.
- **COMM-299**, The aperture-to-rate sensitivity is steep: an increase of 1 dB of link gain improves the rate by a factor ~1.58 (or range by ~1.12); since gain scales with area, the Lynk-to-AST aperture span (~1.4 to ~223 m^2, ~22 dB) is the difference between intermittent SMS and 120 Mbps broadband. [FACT for the 1 dB factor (single-source academic); DERIVED for the span] Source: arXiv 2506.18672.
- **COMM-300**, AST goes giant because broadband-to-phone is the top of the aperture ladder; AST states it directly: "Given the low power and small antenna size of standard mobile phones, the satellite must provide the necessary signal strength," using 693 sq ft (~64 m^2) Block 1 arrays, "the largest commercial arrays ever deployed in low Earth orbit." [FACT, AST official] Source: AST How-It-Works.
- **COMM-301**, AST BlueBird Block 2's ~223 m^2 array yields a modeled gain of ~42 dBi at 880 MHz (G = 4 pi eta A / lambda^2, eta ~0.7); AST characterizes its aperture as "north of 40 dBi" versus ~16 dBi for a terrestrial tower; a 40 MHz beam at its efficiency carries ~120 Mbps. [FACT/DERIVED; 42 dBi derived in the literature, "north of 40 dBi" single-source] Sources: arXiv 2506.18672; AST Next-Gen BlueBird (120 Mbps/cell).
- **COMM-302**, AST's BlueWalker 3 prototype (the 64 m^2 test article) demonstrated ~21 Mbps to a phone, early validation that a ~64 m^2-class aperture reaches real broadband-ish rates. [FACT] Sources: Aerospace America; AST/trade press.
- **COMM-303**, Starlink's direct-to-cell payload rides a V2-mini bus (~4.1 x 2.7 m body) carrying a ~25 m^2 phased array, an order of magnitude smaller in area than AST Block 2, capping per-satellite direct-to-cell capacity but staying flat-stackable. [FACT; the precise 25 m^2 is soft] Sources: Spaceflight Now (bus dimensions); KeepTrack / trade press (~25 m^2).
- **COMM-304**, Starlink's measured direct-to-cell performance during the SMS-only phase (Oct 2024-Jul 2025) was ~3.1 Mbps/beam at 0.52-0.61 bps/Hz on the PCS G-block 2x5 MHz channel, with voice/data following; ~2-4 Mbps/beam is the cited range. [FACT] Sources: arXiv 2506.00283 (crowdsourced measurements); Panariello (2-4 Mbps/beam).
- **COMM-305**, Starlink compensates for its smaller aperture with constellation density: direct-to-cell capability is added to a portion of new builds (~20+ per Falcon 9), so coverage and capacity scale with the thousands-strong fleet; a separate up-to-15,000-satellite dedicated D2C fleet is filed (existing COMM in starlink_v3_specs.md). [FACT/DERIVED] Sources: Aerospace America; New Space Tracker; cross-ref starlink_v3_specs.md.
- **COMM-306**, Independent estimates put each AST Block 2 array at ~35-40x the area of a Starlink direct-to-cell antenna and ~100x the per-satellite direct-to-cell bandwidth/capacity; the two operators reach comparable aggregate capacity from opposite ends of the aperture-vs-satellite-count tradeoff. [FACT for the ~35-40x / ~100x (independent estimate); DERIVED for the comparable-aggregate netting] Sources: New Space Tracker; TechTimes; Aerospace America.
- **COMM-307**, For a given launcher, the moderate-aperture-many-satellites architecture has far lower launch cost per satellite (one launch spread over ~20+ vs ~1-3 giant satellites) and plausibly lower launch cost per delivered bit at the messaging/low-rate level; the giant-aperture architecture wins per-bit only if broadband-to-phone (unreachable by the small aperture) is what the market pays for. [DERIVED] Sources: this doc Section 5; cross-ref neutron_comms_payload_fit.md claim 21.
- **COMM-308**, There is a hard floor on satellite antenna size for direct-to-cell: below ~1-1.5 m^2 only intermittent SMS; ~25 m^2 for voice/few-Mbps; ~50-60+ m^2 for broadband-to-phone; a satellite antenna materially below ~1 m^2 cannot close the bare-handset link at a useful service level. [DERIVED] Sources: Frank Rayal (1.4 m^2 floor); Panariello / Aerospace America (the ladder).
- **COMM-309**, Direct-to-cell CAN be flat-stacked many-per-launch only at the messaging/thin-data service level; Starlink already flies its ~25 m^2-class D2C payloads flat-stacked ~20+ per Falcon 9. A messaging-grade D2C satellite is plausibly multi-per-Neutron; the specific 6-9 count is UNKNOWN (the ~25 m^2-class panel's stowed dimensions on a Neutron fairing are unpublished). [DERIVED; specific count UNKNOWN] Sources: this doc Section 6; Starlink flat-stack precedent (trade press); cross-ref neutron_comms_payload_fit.md.
- **COMM-310**, Broadband-to-phone CANNOT be flat-stacked at 6-9 per Neutron: it forces the ~64-223 m^2 giant aperture, which folds into a bulky accordion that goes ~1 per Neutron (3 on Falcon 9, 1 on New Glenn, 1 on LVM3); RF-aperture packing caps at ~34-48% (phone-booth class), far short of a thin flat stack. [DERIVED] Sources: this doc Section 6; cross-ref neutron_comms_payload_fit.md (per-fairing counts) and large_array_folding_and_stow.md (COMM-207).
- **COMM-311**, The broadband-vs-direct-to-cell asymmetry (the core reason their satellites differ in size): a broadband customer's high-gain dish (Starlink ~1,280-element flat panel, customer-paid) supplies the ground-side gain so the satellite's user antenna can be small/flat-pack; a direct-to-cell customer's bare phone (~0 dBi) supplies nothing, so all that gain must live on the satellite, forcing a giant aperture. The big antenna is on the ground for broadband and in orbit for direct-to-cell. [DERIVED, multi-source-supported] Sources: KeepTrack / trade press (dish-vs-no-dish); this doc Section 7; cross-ref rf_limited_service.md (large-dish advantage).
- **COMM-312**, This gain-placement asymmetry is the upstream CAUSE of the corpus's already-documented launch asymmetry: a broadband satellite is a flat ~7 m panel that stacks ~5/Neutron (mass-bound) while a broadband-to-phone satellite is a ~223 m^2 folded aperture at ~1/Neutron (size-bound), purely because the gain has to live somewhere and a bare phone forces it onto the satellite. [DERIVED] Sources: this doc Section 7; cross-ref neutron_comms_payload_fit.md (COMM/claim 20) and large_array_folding_and_stow.md (COMM-208).
- **COMM-313**, Corollary spectrum asymmetry: broadband rides wide Ku/Ka because the dish-closed link runs high-order modulation, while direct-to-cell is stuck in thin ~5-10 MHz low-band cellular slices partly because the bare-handset link runs at low spectral efficiency (~0.5-0.6 bps/Hz measured for Starlink SMS); direct-to-cell capacity is aperture-and-spectrum-starved on both ends, so the giant aperture is the operator's main self-controlled lever (spectrum must be bought/leased, e.g. the ~$17B EchoStar block). [DERIVED, ties to existing COMM-185..187] Sources: this doc Section 7; cross-ref starlink_v3_v4_spectrum_incorporation.md (COMM-185/186/187), arXiv 2506.00283 (0.52-0.61 bps/Hz).
- **COMM-314**, Strategic fork for a Neutron-launched direct-to-cell business: the aperture ladder is also a launch-economics ladder; Neutron's 5.5 m fairing is comfortable on the low rungs (messaging/thin-data, many-per-launch) and binding on the high rung (broadband-to-phone, ~1 per launch where a Starship-class batch lifter out-scales it). The service ambition, not the launcher, sets the aperture, and the aperture sets satellites-per-launch. [DERIVED] Source: this doc Sections 5-8.

---

*COMM-293..314 created by this doc. Catalog rows for LIBRARY.md / RESEARCH_TRACKER.md / SOURCE_INDEX.md are returned to the catalog/reconciliation agent, not edited here.*
