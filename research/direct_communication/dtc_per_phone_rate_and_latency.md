# Direct-to-Cell Per-Phone Operating Point: the Single-Phone Rate (Not the Per-Cell Rate), the Aperture That Delivers It, and the Low-Orbit Latency Advantage

**Research date:** 2026-06-23
**Status:** Understanding-building input for the Neutron Tier-1 direct-to-cell (DTC) business. No go/no-go verdict. This doc pins the PER-SINGLE-PHONE operating point the founder refined the product around (a ~25 to 50 Mbps rate to ONE phone), separating it cleanly from the per-cell/per-beam capacity figures the corpus already carries, mapping the aperture that delivers it, and grounding the low-orbit latency advantage. Every value is flagged sourced (FACT) / derived (DERIVED) / estimate (ESTIMATE) / unknown (UNKNOWN).

> **Why this document exists.** The founder refined the DTC product to a precise target: a SINGLE-PHONE downlink of ~25 to 50 Mbps, delivered by a MIDDLE aperture (~50 m^2, between Starlink's ~25 m^2 and AST's ~223 m^2) plus LOW orbit (~350 to 550 km). This is NOT the per-beam 2 to 10 Mbps the corpus quotes for the V3 fleet, and NOT AST's "~120 Mbps," which is a PER-CELL number shared across many phones. The corpus's governing model ([`dtc_system_model.md`](dtc_system_model.md), COMM-315..335) names the two service tiers and the levers, but it does NOT cleanly state how a cell's total throughput divides into a single-phone rate, nor does it anchor the single-phone rate to a measured single-device demonstration. This doc closes that gap: it establishes that the published DTC figures are per-cell/per-beam, that a lightly-loaded cell hands the full beam to one phone (so per-cell-when-alone equals the single-phone peak), and that a ~50 m^2 array at low orbit on owned spectrum lands the ~25 to 50 Mbps single-phone target, because ~50 m^2 is only ~1.07 dB below the ~64 m^2 array that already demonstrated ~21 Mbps to a phone (AST BlueWalker 3).

> **Grounds in and does NOT re-derive (this doc adds the PER-PHONE layer on top of the per-cell ladder the corpus owns):**
> - [`research/direct_communication/dtc_antenna_aperture_tradeoff.md`](dtc_antenna_aperture_tradeoff.md) (COMM-293..314): owns the LINK BUDGET and the aperture-to-service ladder (the phone is fixed and weak; gain = 4 pi eta A / lambda^2; the ~1 m^2 / ~25 m^2 / ~64 m^2 / ~223 m^2 rungs). This doc takes that ladder as given and re-labels its rate column as PER-CELL/PER-BEAM where the source figures are cell aggregates, then maps the SINGLE-PHONE rate underneath it.
> - [`research/direct_communication/dtc_system_model.md`](dtc_system_model.md) (COMM-315..335): owns the GOVERNING RULE (aperture + owned spectrum set the tier; altitude a weak ~3.5 to 4 dB trim; satellite count never a per-phone-rate lever; the two-tier split). This doc supplies the per-phone numbers that sit inside Tier 1, and confirms COMM-317's "a thousand texting satellites still only text each phone" with the scheduler mechanism (count does not raise the single-phone rate).
> - [`research/direct_communication/leo_constellation_coverage_minimums.md`](leo_constellation_coverage_minimums.md) (COMM-209..228): owns the altitude/slant-range geometry (footprint, slant range, pass duration). This doc uses the slant ranges for both the path-loss trim (Section 2) and the propagation-latency floor (Section 3).
> - [`research/competitors/starlink_v3_platform_and_starship.md`](../competitors/starlink_v3_platform_and_starship.md) (COMM-271..292): owns the V3 D2C platform (~25 m^2 aperture, dedicated up-to-15,000-sat fleet at ~326 to 335 km, ~2 to 10 Mbps sustained / ~100 Mbps peak per phone REPORTED projection). This doc takes those as given and adds the AST single-device anchors.
> - Cross-references (not re-listed): [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md), [`spectrum_purchase_and_6g.md`](spectrum_purchase_and_6g.md), [`large_array_folding_and_stow.md`](../competitors/large_array_folding_and_stow.md).

> **Tagging.** **[FACT]** sourced (multi-source unless flagged single-source), **[DERIVED]** computed in this doc from sourced inputs, **[ESTIMATE]** a third-party model/target/projection, **[UNKNOWN]** a named gap (not invented). New claims use **COMM-336..355** (the original reserved block) and **COMM-371..385** (the Section 2.6 aperture-curve block; COMM-356..370 belong to the [`dtc_system_model.md`](dtc_system_model.md) integration block, so the next free contiguous start is COMM-371). Neither block is exceeded. No em-dashes anywhere.

---

## 0. Answer first (the per-phone operating point in one screen)

**The published direct-to-cell throughput figures are PER-CELL / PER-BEAM (a shared pool), not per-single-phone. But a lightly-loaded cell hands its whole beam to one phone, so the per-cell-when-alone capacity IS the single-phone peak. On that reading, a ~50 m^2 array at low orbit on ~20 to 40 MHz of owned spectrum lands the founder's ~25 to 50 Mbps single-phone target, because ~50 m^2 is only ~1.07 dB below the ~64 m^2 array that already demonstrated ~21 Mbps to a real phone (AST BlueWalker 3), and low orbit hands back ~3.5 to 3.9 dB that more than erases the aperture shrink. The single-phone RATE is set by aperture (gain) plus owned bandwidth; the extra aperture above ~50 to 64 m^2 buys per-cell CAPACITY (more concurrent users, smaller cells), not a higher peak to one handset. Low orbit also delivers a structural product advantage independent of rate: ~5 to 10 ms of propagation versus GEO's ~240 to 280 ms, which keeps an interactive voice call inside the ITU-T G.114 "good" band.**

1. **Per-cell vs per-phone, resolved (Section 1).** AST's "up to 120 Mbps" is explicitly **per coverage cell** (AST's own words), shared across the hundreds-to-thousands of phones in a ~30 to 48 km beam. AST's BlueWalker 3 demonstrations (~10.3, ~14, ~21 Mbps) were **single-device** measurements with one phone alone in an otherwise idle test cell. Starlink's measured ~3.1 Mbps is **per beam**, which the source paper states verbatim is "an upper-bound estimate of the throughput per connection, corresponding to the scenario of a single user occupying the full bandwidth of the beam." So the per-cell figure and the best-case single-phone figure CONVERGE when one phone is alone, and DIVERGE (per-user falls to ~1 Mbps or less) when the cell is busy. [FACT]

2. **How a cell divides to a phone (Section 1.3).** A satellite beam serves users by a time-division scheduler, one phone at a time per resource block, exactly like a terrestrial cell. A lightly-loaded cell gives the near-full beam to one phone (this is precisely why the demonstrated single-device speeds equal the per-channel beam capacity); a busy cell splits the same pool across all active users in the beam. The single-phone PEAK is the per-cell capacity; the single-phone AVERAGE falls with concurrent users. [FACT]

3. **The aperture for a single phone (Section 2).** The empirical anchor is almost exactly the founder's case: **AST BlueWalker 3, a ~64 m^2 array, demonstrated up to ~21 Mbps to a phone.** A ~50 m^2 array is only **+1.07 dB** smaller in gain (10 log10(64/50)), so in aperture terms the founder's middle array is essentially the BW3 array. Dropping to low orbit (~350 to 400 km) buys back **~3.5 to 3.9 dB** of path loss versus AST's ~513 km, more than offsetting the shrink. Rate then scales linearly with owned bandwidth (Shannon B term): **~17 MHz at 3 bps/Hz, or ~20 to 25 MHz at 2 to 2.5 bps/Hz, reaches 50 Mbps to one phone**, well inside the 40 MHz / 120 Mbps-per-cell envelope AST specs on a comparable aperture. **So ~50 m^2 is enough for 25 to 50 Mbps to one phone, given low orbit and ~20 to 40 MHz of owned downlink. You do NOT need ~64 to 100 m^2 for the single-phone rate.** [DERIVED, anchored on the BW3 FACT; two named soft spots in Section 2.4]

4. **Latency (Section 3).** Low LEO (~350 to 550 km) has **~5 to 10 ms of pure round-trip propagation** (phone to satellite to gateway and back) and **~20 to 50 ms measured end-to-end**, versus GEO's **~240 to 280 ms propagation (a single GEO uplink leg alone is ~120 ms)** and **~600 to 700 ms measured**. ITU-T G.114 puts interactive voice in a "good" band up to 150 ms one-way and "unacceptable" above 400 ms. **Low orbit keeps the entire G.114 budget free for codec, jitter buffer, and backhaul, so a satellite call feels like a normal mobile call; GEO structurally cannot, regardless of hardware.** This is the historical Iridium-vs-Inmarsat satphone contrast. [FACT for the measured figures and thresholds; DERIVED for the propagation floors]

The rest sources and derives each point.

---

## 1. Per-cell / per-beam vs per-single-phone (the distinction the founder's product turns on)

The corpus's aperture ladder ([`dtc_antenna_aperture_tradeoff.md`](dtc_antenna_aperture_tradeoff.md), COMM-298) lists a single "per-beam / per-cell rate" column. This section pins which of those figures are cell aggregates (shared) and what a SINGLE phone actually gets, because the founder's target (~25 to 50 Mbps to one phone) is a different quantity from the headline numbers.

### 1.1 The four numbers, each pinned as per-cell or per-phone

| Figure | Value | Per-cell / per-beam (shared) or per-single-phone? | Tag |
|---|---|---|---|
| AST "up to 120 Mbps" | ~120 Mbps | **PER COVERAGE CELL** (AST's own words: "up to 120 Mbps per coverage cell across more than 2,000 cells"); shared across all phones in the cell | [FACT] |
| AST BlueWalker 3 demos | ~10.3, ~14, ~21 Mbps | **SINGLE DEVICE** (one unmodified phone alone in an idle test cell, one ~5 MHz channel); the ~21 Mbps is the per-channel beam capacity going to one phone | [FACT for the rates; the single-device read is FACT-from-press-language + analyst, device count UNKNOWN] |
| Starlink DTC measured | ~3.1 Mbps | **PER BEAM = single-user-when-alone** (source verbatim: "upper-bound estimate of the throughput per connection... a single user occupying the full bandwidth of the beam"); 0.52 to 0.61 bps/Hz on PCS G-block 2x5 MHz, SMS phase | [FACT] |
| AST device peak (Block 1 / Block 2) | ~98.9 Mbps / ~200 Mbps (design) | **SINGLE DEVICE PEAK** (best-case instantaneous to one phone under favorable geometry/spectrum); distinct from the 120 Mbps/cell sustained aggregate | [FACT for 98.9 (AST-originated); ESTIMATE for ~200 Block 2 design target] |

Sources: AST 120 Mbps/cell ([AST How-It-Works](https://ast-science.com/how-it-works/), [AST Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/), [AST FAQ](https://ast-science.com/faqs/)); BW3 ~10.3 Mbps ([RCR Wireless](https://www.rcrwireless.com/20230622/featured/ast-spacemobile-hits-space-based-lte-speeds-of-10-mbps-using-att-spectrum), [Fierce](https://www.fierce-network.com/tech/ast-spacemobile-touts-10-mbps-download-speeds-during-tests-hawaii)), ~14 Mbps + 5G ([AST press](https://ast-science.com/ast-spacemobile-achieves-space-based-5g-cellular-broadband-connectivity-from-everyday-smartphones-another-historic-world-first/), [SpaceNews](https://spacenews.com/ast-spacemobile-achieves-space-based-5g-cellular-broadband-connectivity-from-everyday-smartphones/)), ~21 Mbps peak ([Wikipedia/AST](https://en.wikipedia.org/wiki/AST_SpaceMobile), [Farrar/WIA white paper](https://wia.org/wp-content/uploads/2025/05/TMF-White-Paper-on-Satellite-D2D_May-2025.pdf)); Starlink ~3.1 Mbps/beam ([arXiv 2506.00283](https://arxiv.org/abs/2506.00283), [arXiv HTML](https://arxiv.org/html/2506.00283v8)); AST device peaks 98.9 / ~200 Mbps ([TechTimes Block 2](https://www.techtimes.com/articles/318740/20260620/ast-spacemobile-block-2-bluebirds-reach-orbit-satellite-broadband-direct-your-phone-nears.htm)).

### 1.2 The unifying read: per-cell-when-alone equals the single-phone peak

The apparent contradiction (AST quotes 120 Mbps/cell but 98.9 Mbps to a device; Starlink measures 3.1 Mbps/beam) dissolves once the scheduler is in view. A cell's spectrum is a single shared pool. When one phone is alone in the cell, it can be scheduled across the whole pool, so it momentarily gets the full per-cell capacity (capped by its own device/channel limits). When the cell is busy, that pool time-shares across all active phones. Therefore:

- **The single-phone PEAK is the per-cell/per-beam capacity** (one phone owning the beam). AST's 120 Mbps/cell on 40 MHz at ~3 bps/Hz is exactly the rate a sole-occupant phone could see; AST's separate 98.9 Mbps device peak is the same order. Starlink's 3.1 Mbps/beam IS the single-user-when-alone rate (the paper says so).
- **The single-phone AVERAGE under load is far lower.** The independent analyst figure (Tim Farrar / WIA white paper) is that once hundreds-to-thousands of phones share a 12 to 20 mile (AST ~30 mile / ~48 km) beam, the per-user rate falls to **~1 Mbps or less in most cases**, with 4G-LTE-class outdoor speeds the realistic operational ceiling. [FACT, analyst; AST does not publish a loaded per-user rate, a named gap, see 1.4]

**The founder's target is a single-phone PEAK / lightly-loaded rate (~25 to 50 Mbps), which is the correct quantity to size the aperture and bandwidth against, and it is distinct from both the per-cell aggregate and the busy-cell per-user average.** [DERIVED]

### 1.3 The mechanism, stated plainly

A satellite DTC beam is a cell. The satellite serves users in the beam by a time-division scheduler (which users, when, at what modulation), one phone per resource block at an instant, identical in principle to a terrestrial base station. Three consequences:

- A lightly-loaded cell can hand the near-full beam capacity to one phone, which is exactly why the demonstrated single-device speeds (BW3 ~21 Mbps, Starlink ~3.1 Mbps) equal the per-channel beam capacity. [FACT]
- Beams are huge (a single beam covers ~100 to 600 sq mi, ~12 to 30 miles across, ~30x a suburban tower footprint; AST's is ~48 km / ~30 mile diameter), so the user count sharing one beam is large, and the per-user average under load is correspondingly small. [FACT, analyst]
- Spectrum is the binding pool: per-beam capacity is roughly bandwidth x spectral efficiency, then divided by active users. The single-phone peak rises linearly with owned MHz (the lever in Section 2). [FACT]

Source: scheduler/time-division and beam-size framing ([Farrar/WIA white paper](https://wia.org/wp-content/uploads/2025/05/TMF-White-Paper-on-Satellite-D2D_May-2025.pdf), [arXiv 2507.14188 cellular-to-satellite blueprint](https://arxiv.org/abs/2507.14188)); per-beam-as-single-user-bound ([arXiv 2506.00283](https://arxiv.org/html/2506.00283v8)).

### 1.4 What the operators do NOT disclose (named gaps)

- **AST never publishes the sustained per-USER rate under load.** It publishes per-cell (120 Mbps) and device peaks (98.9 / ~200 Mbps), but not what one phone gets in a loaded cell. The ~1 Mbps-or-less figure is the analyst (Farrar), not AST. [UNKNOWN from AST; analyst ESTIMATE fills it]
- **AST never stated the simultaneous device count or the test channel bandwidth behind its BW3 ~21 Mbps.** "Single device" is inferred from the press-release one-phone language plus Farrar's corroboration ("21 Mbps in a 5 MHz block... shared by hundreds or thousands of users"), and the bandwidth is inferred as one ~5 MHz channel, but neither is asserted by AST. These two gaps are the soft spots in the single-phone anchor (Section 2.4). [UNKNOWN]
- **Starlink's ~2 to 10 Mbps sustained / ~100 Mbps peak per phone** is a single secondary source (NextBigFuture) and a company aspiration, not a measured value. [ESTIMATE/projection, flagged, = COMM-278]

---

## 2. The aperture-to-single-phone-rate mapping (is ~50 m^2 enough for 25 to 50 Mbps to one phone?)

The founder's product: ~25 to 50 Mbps to ONE phone, on a MIDDLE aperture (~50 m^2) plus LOW orbit (~350 to 550 km) plus realistic OWNED spectrum. This section builds the aperture-to-single-phone-rate mapping and answers the sizing question.

### 2.1 The mapping table

Single-phone rate = the lightly-loaded per-cell capacity (Section 1.2), i.e. one phone momentarily owning the beam. Gains computed from G = 4 pi eta A / lambda^2 at ~880 MHz with eta = 0.7, anchored on the literature's worked point (223 m^2 -> ~42 dBi) and scaled by 10 log10(area ratio), which is exact and altitude-independent.

| Aperture (m^2) | Gain @ ~880 MHz (dBi) | Real-world anchor | Demonstrated / target SINGLE-PHONE rate | Tag |
|---|---|---|---|---|
| ~1.4 | ~20 | Frank Rayal messaging floor | ~32 kbps on 5 MHz | [FACT, link-budget] |
| ~25 | ~32.5 | Starlink Gen2 DTC | 3.1 Mbps/beam (= single-user-when-alone) on 2x5 MHz; ~2 to 10 Mbps sustained / ~100 peak target | [FACT measured; ESTIMATE target] |
| **~50** | **~35.5** | **founder's middle aperture** | **~25 to 50 Mbps inferred (low orbit + ~20 to 40 MHz owned)** | **[DERIVED, see 2.3]** |
| ~64 | ~36.5 | AST BlueWalker 3 / BlueBird Block 1 | **up to ~21 Mbps demonstrated to a phone (BW3)**; 120 Mbps per cell on 40 MHz (Block 1) | [FACT demonstrated; FACT per-cell] |
| ~100 | ~38.5 | (none flying) | >21 Mbps, scales with bandwidth | [DERIVED] |
| ~223 | ~42 | AST BlueBird Block 2 | 120 Mbps per cell on 40 MHz; ~500 kbps/user at ~5% beam load | [FACT] |

The load-bearing rows: **120 Mbps is per cell (= single-phone peak when alone) = 40 MHz x 3 bps/Hz**; **Starlink 3.1 Mbps is the explicit single-user-when-alone bound**; and **the ~50 m^2 row sits between two flying anchors, ~1.07 dB below the ~64 m^2 BW3 array that already did ~21 Mbps to a phone.** Sources: gain formula and 223 m^2 -> 42 dBi, 40 MHz -> 120 Mbps, ~500 kbps/user at 5% load ([arXiv 2506.18672](https://arxiv.org/html/2506.18672v1)); Starlink single-user bound ([arXiv 2506.00283](https://arxiv.org/html/2506.00283v8)); messaging floor ([Frank Rayal](https://frankrayal.com/2022/08/29/t-mobile-spacex-direct-satellite-to-handset-service-lots-of-hype-and-little-reality/)); BW3 ~21 Mbps + 64 m^2 (Section 1.1 sources); AST Block 1 40 MHz/beam ([AST BlueBird 1-5](https://ast-science.com/bluebird-1-5/), [AST FAQ](https://ast-science.com/faqs/)).

### 2.2 The gain-step and altitude-step arithmetic (verified in this doc)

**Gain steps (aperture ratios, exact, frequency- and altitude-independent), 10 log10(area ratio):**

| Step | dB |
|---|---|
| 25 -> 50 m^2 | +3.01 |
| 25 -> 64 m^2 | +4.08 |
| **50 -> 64 m^2** | **+1.07** |
| 50 -> 100 m^2 | +3.01 |
| 64 -> 223 m^2 | +5.42 |
| 50 -> 223 m^2 | +6.49 |

**Altitude steps (free-space path loss, 20 log10(slant-range ratio), Earth radius 6371 km), 550 -> 350 km:** the frequency and constant terms cancel in the difference, so these dB-deltas hold at any DTC band.

| Elevation | Slant 550 -> 350 km | dFSPL saved |
|---|---|---|
| 90 deg (overhead) | 550 -> 350 km | 3.93 dB |
| 45 deg | 749 -> 483 km | 3.82 dB |
| 30 deg | 993 -> 652 km | 3.65 dB |
| 25 deg | 1123 -> 747 km | 3.54 dB |
| 10 deg (horizon) | 1815 -> 1303 km | 2.88 dB |

**Headline: dropping 550 -> 350 km buys ~3.5 to 3.9 dB at useful elevations (30 to 90 deg), tapering to ~2.9 dB at the horizon.** This matches the corpus's ~3.5 to 4 dB (COMM-316). [DERIVED, computed; verified against the corpus slant ranges COMM-209]

### 2.3 The synthesis chain: ~50 m^2 + low orbit + owned bandwidth -> 25 to 50 Mbps to one phone

Anchored on the strongest empirical point (BW3), built step by step, each step tagged.

- **Start [FACT]:** AST BlueWalker 3, ~64 m^2 at ~513 km on AT&T Band 5 (~850 MHz), demonstrated **up to ~21 Mbps to a phone**. (Two undisclosed quantities, both UNKNOWN: device count, test channel bandwidth.)
- **Step A, aperture 64 -> 50 m^2 [DERIVED]:** lose 10 log10(64/50) = **1.07 dB**. Aperture-wise ~50 m^2 is nearly identical to BW3; the rate effect is small and (in the power-limited regime) sub-linear.
- **Step B, altitude ~513 km -> ~350 to 400 km [DERIVED]:** gain **~3.5 to 3.9 dB** of path loss at useful elevations. This more than offsets Step A, leaving **~+2.4 to +2.8 dB net link improvement** versus BW3 even after shrinking the array.
- **Step C, owned bandwidth [FACT mechanism, ESTIMATE inputs]:** rate scales linearly in the Shannon B term, R = B log2(1+SNR). At ~2 to 3 bps/Hz (consistent with AST's commercial ~3 bps/Hz baseline; the BW3 test bps/Hz is UNKNOWN but back-solving 21 Mbps gives ~2.1 bps/Hz on 10 MHz, ~3.0 on 7 MHz, ~4.2 on 5 MHz):
  - To clear **25 Mbps** to one phone: ~8 to 12 MHz at 2 to 3 bps/Hz, roughly the bandwidth BW3 likely already had, plus the orbit help. Well-covered.
  - To clear **50 Mbps** to one phone: **~17 MHz at 3 bps/Hz, ~20 MHz at 2.5 bps/Hz, or ~25 MHz at 2 bps/Hz.** Squarely inside AST's own 40 MHz / 120 Mbps-per-cell envelope on a comparable aperture.

**Conclusion [DERIVED]: ~50 m^2 is enough for 25 to 50 Mbps to ONE phone, given low orbit (~350 to 400 km) and ~20 to 40 MHz of owned downlink at ~2 to 3 bps/Hz. You do NOT need ~64 to 100 m^2 for the single-phone RATE; the larger apertures buy per-cell CAPACITY (more concurrent users, smaller cells, more beams), not a higher peak to one handset.** This is consistent with the governing rule (COMM-320): aperture plus owned spectrum set the rate, altitude trims a few dB, and ~50 m^2 sits at the Tier-1 rung, above the ~25 m^2 floor.

### 2.4 The honest weak points (where this is inference, not proof)

1. **The BW3 anchor has two undisclosed quantities** (simultaneous device count, test channel bandwidth). If the ~21 Mbps was already a multi-device aggregate, the per-phone start point is lower and the chain needs more owned bandwidth to reach 50 Mbps. This is the single biggest soft spot. [UNKNOWN]
2. **Linear-bandwidth scaling assumes constant spectral efficiency.** Doubling bandwidth doubles rate only if SNR-per-Hz holds, i.e. the array and power can illuminate the wider channel at ~2 to 3 bps/Hz. At fixed aperture and power, spreading power over more bandwidth lowers SNR-per-Hz; the +2.4 to +2.8 dB net from low orbit is real margin that helps, but a full jump to 40 MHz is partly a hand-wave without the test-bandwidth number. [Mechanism FACT, magnitude ESTIMATE]
3. **Single-phone = sole beam occupancy.** "25 to 50 Mbps to one phone" is a peak / lightly-loaded number; the average falls with concurrent users (AST's own 5%-load example gives ~500 kbps/user). The founder's framing (one unmodified phone, lightly loaded) is the right one for a peak-to-one-phone claim, but it is best-case, not loaded-network. [DERIVED]

### 2.5 Arithmetic correction to carry into the corpus (the "1 dB = 1.58x" figure)

The corpus carries "1 dB of link gain improves the rate by a factor ~1.58" (COMM-299, restated in COMM-316). **That factor is mislabeled: it is the +2 dB factor, not +1 dB.** Verified: 10^(0.1) = **1.259** (so +1 dB = x1.26, +25.9%), and 10^(0.2) = **1.585** (so +2 dB = x1.585). The multiplicative-rate rule also holds only in the low-SNR / power-limited regime (rate proportional to linear SNR); in the bandwidth-limited / high-SNR regime, +1 dB adds a roughly fixed bits/s/Hz, not a fixed multiplier. DTC handset links are typically power-limited, so the multiplicative view is reasonable as an approximation. Corrected, the ~3.5 to 3.9 dB from 550 -> 350 km maps to a rate factor of ~1.95x (nadir) to ~2.45x in the power-limited regime, before other budget terms. [DERIVED; this is a flag for the catalog/reconciliation pass to fix COMM-299/316, NOT an edit made here.]

---

## 2.6 Aperture-to-single-phone-rate curve (25 / 50 / 64 m^2): does a FLAT ~25 m^2 Flatellite already clear ~25 Mbps to one phone?

> **Why this subsection exists (the architecture fork it resolves).** Section 2.3 grounded the founder's ~25 to 50 Mbps single-phone target at the ~50 m^2 MIDDLE aperture. But ~50 m^2 is ~7.07 m on a side, which EXCEEDS Neutron's ~5.5 m fairing as a flat panel, so it must FOLD, and a folded DTC array stows to ~3 satellites/Neutron (the flat-to-fold cliff, [`dtc_system_model.md`](dtc_system_model.md) Section 5.2, COMM-362). The Rocket Lab **Flatellite is a FLAT body that is its own aperture** ([`flatellite_platform.md`](../rocket_lab/flatellite_platform.md), COMM-263): it does NOT fold, which is exactly how it stacks ~16 per launch, and a flat panel is capped by the ~5.5 m fairing footprint at roughly **20 to 25 m^2** (a 5.0 m square is ~25 m^2). So the decision-critical question is a single number with a ~5x swing on satellites-per-launch attached: **does a flat ~25 m^2 Flatellite ALREADY clear a ~25 Mbps single-phone bar on its own (then you never fold and keep the many-per-launch flat stack), or does it fall short (then the bigger folding ~50 m^2 array is required, at ~3/Neutron)?** This subsection extends the SAME grounded method used for the ~50 m^2 case down to ~25 m^2 to answer it. [Framing; the fold/stow and per-launch counts are SOURCED, COMM-362/263]

### 2.6.1 The method (identical to Section 2.3, applied at three apertures)

Same chain, same anchor, three aperture points (~25 / ~50 / ~64 m^2):
- **Anchor [FACT]:** AST BlueWalker 3, ~64 m^2 at ~513 km, demonstrated up to **~21 Mbps to ONE phone** (two undisclosed quantities, the simultaneous device count and the test channel bandwidth, both UNKNOWN, Section 1.1 / 2.4).
- **Aperture step [DERIVED]:** 10 log10(A/64) dB relative to the 64 m^2 anchor (exact, frequency- and altitude-independent).
- **Low-orbit path-loss gain [DERIVED]:** **+3.5 to 3.9 dB** flying at ~350 km versus BW3's ~513 km, at useful elevations (30 to 90 deg), the grounded band from Section 2.2 / COMM-346. (The bare-overhead 20 log10(513/350) = 3.32 dB; the corpus band of 3.5 to 3.9 dB is the useful-elevation figure carried throughout this doc, used here for consistency.)
- **Bandwidth scaling [FACT mechanism, ESTIMATE inputs]:** single-phone rate R = B x (spectral efficiency), linear in owned bandwidth B, at **~2 to 3 bps/Hz** (the same constant the ~50 m^2 case assumed; AST's commercial baseline is ~3 bps/Hz, and back-solving BW3's 21 Mbps gives ~2.1 bps/Hz on 10 MHz, ~3.0 on 7 MHz, ~4.2 on 5 MHz).
- **dB-to-rate (power-limited regime) [DERIVED]:** +1 dB = 10^0.1 = 1.26x (the corrected factor, Section 2.5 / COMM-356).

### 2.6.2 The curve: net link delta versus BW3, by aperture

The aperture step and the low-orbit gain combine into a **net link delta versus the BW3 demonstration**, which is the headroom that says whether each array can sustain ~2 to 3 bps/Hz across an owned channel. Computed in this doc:

| Aperture | Aperture step 10 log10(A/64) | + low-orbit gain (350 vs 513 km) | = NET vs BW3 | Rate-multiplier (power-limited, 10^(dB/10)) | Link-only rate vs BW3's own bandwidth | Tag |
|---|---|---|---|---|---|---|
| **~25 m^2** (flat Flatellite) | **-4.08 dB** | +3.5 to +3.9 dB | **-0.58 to -0.18 dB** | **0.87 to 0.96x** | **~18 to 20 Mbps** | [DERIVED] |
| **~50 m^2** (folding, Section 2.3 point) | **-1.07 dB** | +3.5 to +3.9 dB | **+2.43 to +2.83 dB** | **1.75 to 1.92x** | **~37 to 40 Mbps** | [DERIVED] |
| **~64 m^2** (BW3 / AST Block 1) | **0.00 dB** (anchor) | +3.5 to +3.9 dB | **+3.50 to +3.90 dB** | **2.24 to 2.45x** | **~47 to 52 Mbps** | [DERIVED] |

**Reading the "link-only rate vs BW3's own bandwidth" column:** it holds bandwidth FIXED at BW3's own (undisclosed) test channel and scales the 21 Mbps anchor by the net link delta only. It is NOT the final owned-spectrum rate (that needs the bandwidth column below); it is the clean, bandwidth-free measure of where each aperture sits relative to the one flying single-phone datapoint. The load-bearing fact: **a flat ~25 m^2 array at ~350 km sits at NEAR-PARITY with the ~64 m^2 BW3 link (-0.58 to -0.18 dB), because the ~4.08 dB aperture shrink is almost entirely erased by the ~3.5 to 3.9 dB low-orbit gain.** Flying low is what makes the small flat aperture viable: at BW3's own ~513 km altitude, ~25 m^2 would be a full ~4.08 dB down, but at ~350 km it is essentially the BW3 link.

### 2.6.3 The curve as the owned-spectrum rate (R = B x efficiency)

The corpus's direct method expresses the single-phone rate as bandwidth x spectral efficiency, with the net link margin above as the headroom that makes the owned channel deliverable at ~2 to 3 bps/Hz. Across the owned 20 to 40 MHz range, R = B x eff is (this is the per-phone rate any aperture that sustains the efficiency reaches):

| Owned bandwidth | at 2 bps/Hz | at 2.5 bps/Hz | at 3 bps/Hz |
|---|---|---|---|
| **20 MHz** (bottom of owned range) | 40 Mbps | 50 Mbps | 60 Mbps |
| **30 MHz** (middle) | 60 Mbps | 75 Mbps | 90 Mbps |
| **40 MHz** (top) | 80 Mbps | 100 Mbps | 120 Mbps |

Aperture enters NOT as a separate multiplier on this table but as the question of **whether the array plus power can hold ~2 to 3 bps/Hz across that owned bandwidth.** The net-link column in 2.6.2 is the evidence: ~64 m^2 has the most headroom (+3.5 to 3.9 dB vs BW3), ~50 m^2 has +2.4 to 2.8 dB, and **~25 m^2 has ~0 dB (near-parity), i.e. it sustains essentially the same efficiency BW3 demonstrated, just with the low-orbit gain spent on erasing the aperture shrink rather than on extra margin.** [DERIVED]

### 2.6.4 THE VERDICT: yes, a flat ~25 m^2 Flatellite clears ~25 Mbps to a single phone on its own

**A flat ~25 m^2 Flatellite at low orbit (~350 km) on owned spectrum DOES clear ~25 Mbps to a single lightly-loaded phone, so the fold is NOT required for the ~25 Mbps bar.** Two independent reads agree:

1. **Bandwidth read (the direct one).** To clear 25 Mbps needs only B = 25 / eff = **~8.3 MHz at 3 bps/Hz, ~10 MHz at 2.5, or ~12.5 MHz at 2 bps/Hz.** That is the BOTTOM of the owned 20 to 40 MHz range, with room to spare: even at the **bottom (20 MHz) and the most conservative 2 bps/Hz, ~25 m^2 reaches ~40 Mbps**, well past the 25 Mbps bar. So 25 Mbps is cleared at the BOTTOM of 20 to 40 MHz; the full ~25 to 50 Mbps band is reached from the bottom-to-middle (25 Mbps at ~12.5 MHz / 2 bps/Hz; 50 Mbps at ~17 MHz / 3 bps/Hz, ~20 MHz / 2.5, or ~25 MHz / 2). [DERIVED]
2. **Link read (the cross-check).** The flat ~25 m^2 array at ~350 km is at ~link-parity with the ~64 m^2 BW3 array that ALREADY demonstrated ~21 Mbps to one phone (net -0.58 to -0.18 dB). So at BW3's own (narrow, undisclosed) test bandwidth it does ~18 to 20 Mbps; widening to the owned 20 to 40 MHz channel at the same efficiency lifts it through and past 25 Mbps. The 25 Mbps bar is barely above what a parity-with-BW3 link does on BW3's OWN bandwidth, so a wider owned channel clears it comfortably. [DERIVED]

**The consequence for the fork.** Because the flat ~25 m^2 Flatellite clears the ~25 Mbps single-phone bar on its own, **you do NOT need to fold to a ~50 m^2 array to hit ~25 Mbps**, and you keep the flat, no-deploy, many-per-launch stack (the ~16/Neutron Flatellite render-read, or the ~6 to 8 V3-class default; either way the FLAT count, not the ~3/Neutron folded count, COMM-362/322). The ~50 m^2 fold is what you would reach for to push toward the TOP of the founder's band (~50 Mbps with comfortable link margin and more per-cell capacity headroom), not to clear ~25 Mbps. Restating the cliff with the rate attached:

| Aperture | Flat or fold on Neutron | Sats/Neutron (from COMM-362) | Single-phone rate it supports | Clears ~25 Mbps bar? | Tag |
|---|---|---|---|---|---|
| **~25 m^2** (flat Flatellite) | **FLAT** (fits ~5.5 m fairing) | **~6 (default) up to ~16 (render-read ceiling)** | **~25 to 50 Mbps across 20 to 40 MHz owned (link at BW3-parity)** | **YES, at the bottom of 20 to 40 MHz** | [DERIVED; counts SOURCED COMM-362/322] |
| ~50 m^2 (Section 2.3 point) | FOLD (~7.07 m side) | ~3 | ~25 to 50 Mbps with ~+2.4 to +2.8 dB net margin | yes, with more link margin | [DERIVED] |
| ~64 m^2 (AST Block 1 / BW3) | FOLD (~8.0 m side) | ~2 | ~21 Mbps demonstrated; >25 Mbps on wider owned BW | yes | [FACT demo + DERIVED] |

**So the architecture answer is: stay flat at ~25 m^2 and keep the many-per-launch stack; the ~25 Mbps single-phone bar is cleared without folding, and folding to ~50 m^2 is a margin/capacity choice for the top of the band, not a requirement for ~25 Mbps. The ~5x swing in satellites-per-launch (flat ~16 vs folded ~3) does NOT have to be paid to reach ~25 Mbps to one phone.** [DERIVED, the decision-critical conclusion; capped by the two unknowns in 2.6.5]

### 2.6.5 The two load-bearing unknowns, and exactly how each moves the verdict

The verdict rides on the BW3 anchor, which has two undisclosed quantities (Section 2.4). They are the honest cap on confidence, and they move the ~25 m^2 answer in opposite, boundable ways:

1. **BW3's simultaneous device count (the single biggest soft spot).** The chain assumes BW3's ~21 Mbps was to ONE phone. If it was instead a MULTI-DEVICE aggregate of N phones, the true single-phone start point is ~21/N Mbps, and the ~25 m^2 link-parity rate falls proportionally: at N=1 (the assumed case) ~25 m^2 does ~18 to 20 Mbps at BW3's bandwidth and clears 25 Mbps on a wider owned channel; **at N=2 the single-phone anchor is ~10.5 Mbps and the ~25 m^2 link-only rate is ~9.6 Mbps at BW3 bandwidth, so the array would need roughly DOUBLE the owned bandwidth (or the higher ~3 bps/Hz) to still clear 25 Mbps, eroding the comfortable margin; at N=3+ the flat ~25 m^2 case needs the full top of the 20 to 40 MHz range, and the fold to ~50 m^2 (which keeps ~+2.4 to +2.8 dB more link margin) becomes the safer route.** AST's press language and the Farrar corroboration point to a single device, which is why N=1 is the working assumption, but AST never asserted it. **Direction: if BW3 was multi-device, the flat-25 verdict weakens and the fold-to-50 case strengthens; this is the unknown most able to flip the fork.** [UNKNOWN]
2. **BW3's test channel bandwidth, via the constant ~2 to 3 bps/Hz assumption.** The R = B x eff scaling assumes the array and power can hold ~2 to 3 bps/Hz across the WIDER owned 20 to 40 MHz channel. If BW3's ~21 Mbps came on a NARROW channel (e.g. ~5 MHz, implying a high ~4.2 bps/Hz under favorable test geometry), then spreading the flat ~25 m^2 array's fixed power over a 20 to 40 MHz owned channel lowers SNR-per-Hz, and the realized efficiency on the wide channel could fall below ~2 to 3 bps/Hz, pulling the rate down. The ~0 dB net link margin of the flat ~25 m^2 case (versus the ~50 m^2 case's +2.4 to +2.8 dB) means **the flat array has LESS headroom to defend the efficiency across a wide channel, so this unknown bites the ~25 m^2 case harder than the ~50 m^2 case.** The conservatism floor that holds it up: even at a pessimistic 2 bps/Hz, clearing 25 Mbps needs only ~12.5 MHz, so unless the wide-channel efficiency falls BELOW ~1.25 bps/Hz (well under the ~0.5 to 0.6 bps/Hz Starlink SMS floor but far under any data-grade figure) the ~25 Mbps bar still clears. **Direction: a narrow BW3 test bandwidth plus power-spreading lowers the achievable wide-channel efficiency, shrinking the flat-25 margin; the bar still clears unless efficiency collapses below ~1.25 bps/Hz, but the comfortable cushion is the part at risk.** [Mechanism FACT, magnitude ESTIMATE / UNKNOWN]

**Net on confidence.** The CENTRAL verdict (a flat ~25 m^2 Flatellite clears ~25 Mbps to one phone on its own, so the fork does not force the fold) is well-supported on the grounded method and survives the conservative 2 bps/Hz floor. But it is an INFERENCE off a single flying datapoint with two undisclosed quantities, and the device-count unknown in particular could move it: if BW3's ~21 Mbps was a 2+-device aggregate, the flat ~25 m^2 case loses its comfortable margin and the ~50 m^2 fold (with its ~2.4 to 2.8 dB extra headroom) becomes the prudent choice for a firm ~25 Mbps. The verdict is "yes, stay flat" with a named, boundable caveat, not a proven number. [DERIVED, honest cap]

---

## 3. The low-orbit latency advantage (a structural product edge independent of rate)

Low orbit is not only the path-loss trim (Section 2); it is a qualitatively decisive advantage for a PHONE service because of latency. This section grounds the numbers and the threshold.

### 3.1 The latency table

Speed of light = 299,792 km/s ~ 300 km/ms. "One-way propagation" is a single phone-to-satellite leg. A phone-to-sat-to-GROUND service traverses 4 propagation segments per round trip (phone -> sat, sat -> gateway, gateway -> sat, sat -> phone). Pure propagation is physics (DERIVED); measured end-to-end is always larger (adds modulation/demod, scheduling/queuing, ground routing).

| Orbit / altitude | One-way propagation (phone -> sat) | Round-trip propagation (4-segment) | Typical MEASURED end-to-end | Tag |
|---|---|---|---|---|
| Low LEO / Starlink DTC ~340 to 360 km | ~1.2 ms overhead, ~1.7 to 1.8 ms slant | **~5 to 10 ms** | No published DTC user-latency yet | altitude [FACT]; one-way [FACT]; RT [DERIVED]; gap [FACT] |
| Starlink broadband ~550 km | ~1.8 ms | ~7 to 8 ms | **~25 to 60 ms** (commonly cited); ~45 ms median (Ookla Q1 2025) | one-way [FACT]; measured [FACT] |
| AST BlueBird ~508 to 527 km (BW3) | ~1.7 to 1.8 ms | ~7 to 8 ms | claimed ~20 to 40 ms (AST, single-vendor) | altitude [FACT]; latency [ESTIMATE] |
| GEO ~35,786 km | **~119 to 125 ms** | **~240 to 280 ms** (up+down); ~480 to 560 ms full user-to-server-to-user | **~600 to 700 ms** (measured) | one-way [FACT]; ~480 ms floor [FACT]; measured [FACT] |
| Iridium LEO ~780 km (satphone, contrast) | ~2.6 ms | ~10 to 15 ms pure | ~395 ms quoted (incl. inter-satellite routing) | [FACT, single-source-ish; framing flagged] |

Sources: c and one-way ~1.8 ms LEO ([SpeedTestHQ Starlink latency](https://speedtesthq.com/guides/satellite/starlink-latency-explained), [Frank Rayal LEO-vs-fiber latency](https://frankrayal.com/2021/07/07/latency-in-leo-satellites-vs-terrestrial-fiber/)); Starlink DTC shell ~340 to 360 km ([FCC DA-24-1193](https://docs.fcc.gov/public/attachments/DA-24-1193A1.pdf)); Starlink ~45 ms median ([RCR Wireless](https://www.rcrwireless.com/20250616/test-and-measurement/starlink-speeds), [Light Reading](https://www.lightreading.com/satellite/starlink-smokes-geo-satellite-operators-in-speed-latency-report)); GEO ~120 ms one-way / ~600 to 700 ms measured ([Orbital Radar speeds and latency](https://orbitalradar.com/satellite-internet/speeds-and-latency), [IEEE ComSoc GEO-vs-LEO](https://techblog.comsoc.org/2025/07/18/geo-satellite-internet-from-hughesnet-and-viasat-cant-compete-with-leo-starlink-in-speed-or-latency/)); AST altitude ([Wikipedia/AST](https://en.wikipedia.org/wiki/AST_SpaceMobile)); Iridium ([OSAT Iridium-vs-Inmarsat](https://osat.com/blogs/blog/comparison-between-iridium-and-inmarsat-satellite-phones)). The 4-segment round-trip propagation figures are computed in this doc (low LEO ~4.7 ms overhead to ~10 ms slant; GEO ~477 ms overhead) and are consistent with the cited measured-latency-minus-overhead structure. [DERIVED]

### 3.2 The GEO-vs-LEO contrast, quantified

- **Pure propagation:** LEO round trip ~5 to 10 ms vs GEO ~240 to 280 ms (up+down only). A ~30 to 50x physics gap. A single GEO uplink leg (~120 ms) alone exceeds an entire LEO end-to-end session. [DERIVED + FACT]
- **Measured user latency:** LEO ~25 to 60 ms vs GEO ~600 to 700 ms, which sources frame as a ~15x real-world difference. [FACT]
- The gap is geometric and unavoidable: GEO is ~65 to 100x higher than these LEO shells, and that distance is physics, not a hardware deficiency that improves with better silicon. [DERIVED]

### 3.3 Why low orbit is a product advantage for a phone service (the ITU-T G.114 threshold)

**ITU-T G.114 (One-way transmission time)** sets the planning bands for interactive voice:
- **0 to 150 ms one-way: acceptable / preferred** (most users notice no impairment).
- **150 to 400 ms one-way: acceptable with increasing degradation.**
- **above 400 ms one-way: unacceptable** for general network planning (even with zero echo, ~10%+ of speakers report difficulty at 400 ms).

Source: [ITU-T G.114](https://www.itu.int/rec/T-REC-G.114) (the 150 ms / 400 ms one-way thresholds), corroborated by secondary tables.

The product consequence:
- A **low-LEO** DTC link spends only ~5 to 10 ms of its one-way budget on the satellite hop, leaving essentially the entire G.114 "good" band (up to 150 ms) for codec, jitter buffer, and terrestrial backhaul. The space segment is effectively invisible to the conversation, so a satellite voice call can feel like a normal mobile call (vendors quote 20 to 50 ms total, comfortably inside "preferred"). [FACT/DERIVED]
- **GEO** burns ~120 ms one-way on a single satellite hop before any codec/buffer delay; a real two-hop voice path pushes one-way delay to ~250 to 300 ms+, into the degraded 150 to 400 ms band, often near or past the 400 ms unacceptability limit. This is why GEO is fine for streaming/downloads but makes live voice awkward (talk-over, noticeable lag). [FACT/DERIVED]
- The field proof point: **Iridium (LEO) is famous for natural-feeling satphone calls, while GEO satphones (Inmarsat/Thuraya) have a perceptible delay**, the same physics observed for decades. [FACT]

**For an interactive phone product (voice, video calls, conversational/real-time apps), low orbit is the enabling decision: it keeps one-way delay inside G.114's "good" band by construction. This is a structural advantage of the Tier-1 low-orbit architecture independent of the per-phone rate, and it is a reason the product flies low beyond the ~3.5 to 4 dB of path-loss it buys.** [DERIVED]

---

## 4. So what (for the Neutron Tier-1 DTC business)

1. **The product target is a single-phone PEAK / lightly-loaded rate (~25 to 50 Mbps), which is the right quantity to size against, and it is distinct from the per-cell aggregate (AST's 120 Mbps/cell) and the busy-cell per-user average (~1 Mbps or less under load).** The corpus's per-cell ladder is correct; this doc adds the per-phone layer underneath it.
2. **~50 m^2 is enough for the single-phone rate.** It is only ~1.07 dB below the ~64 m^2 BW3 array that already demonstrated ~21 Mbps to a phone; low orbit hands back ~3.5 to 3.9 dB; and ~20 to 40 MHz of owned downlink takes a lightly-loaded phone to 25 to 50+ Mbps. The extra aperture above ~50 to 64 m^2 buys per-cell capacity (concurrent users), not single-phone peak. This sits at the Tier-1 rung of the governing model (COMM-320), between the ~25 m^2 floor and the ~60+ m^2 Tier-2 broadband rung.
3. **Owned spectrum is the co-equal lever.** The single-phone rate is aperture (gain) AND bandwidth; ~50 m^2 only reaches 50 Mbps WITH ~20 to 40 MHz of owned downlink. This inherits the corpus spectrum gate (COMM-325): the rate target cannot be met on a thin ~5 to 10 MHz SCS-leased slice alone.
4. **Low orbit is a structural product advantage for a phone service beyond the path-loss trim.** ~5 to 10 ms propagation keeps interactive voice inside the ITU-T G.114 "good" band; GEO (~240 to 280 ms) cannot. This is a reason to fly low independent of the rate, and it differentiates the Tier-1 low-orbit architecture from any GEO alternative.
5. **No verdict.** This doc establishes the per-phone operating point, the aperture-to-single-phone-rate mapping, and the latency advantage. Whether the business closes depends on the owned-spectrum position (COMM-325), the coverage/capacity floor at low altitude (COMM-323), the per-satellite capacity and Flatellite mass (COMM-322/324, UNKNOWN), and the launch economics (fit doc), none assessed here.

---

## 5. Refinements and notes for the corpus (not edits; for the reconciliation pass)

- **AST's PLANNED operational constellation is ~725 to 740 km**, higher than the ~507 to 523 km BlueBird/BW3 operating altitude the corpus uses (COMM-319, COMM-321 carry ~507 to 523 km). The 42 dBi gain is altitude-independent (aperture x frequency only), so the aperture analysis is unaffected, but the planned-altitude refinement modestly raises AST's propagation floor and weakens any "AST flies low" reading. The founder's Tier-1 product flies LOW (~350 to 550 km) regardless, so the low-orbit advantage is the entrant's, not AST's. [FACT, refinement; flag for the catalog pass]
- **The "1 dB = 1.58x rate" figure (COMM-299, COMM-316) is mislabeled** (it is the +2 dB factor; +1 dB = x1.26). Section 2.5 has the corrected values. This does not change any tier conclusion (the corpus uses it qualitatively), but the catalog should correct the factor. [DERIVED, flag for the catalog pass]
- **AST's BW3 ~21 Mbps is the single-device anchor the system model (COMM-302) needed.** COMM-302 currently reads "~21 Mbps to a phone" without the per-cell/per-phone label; this doc confirms it was a single-device demo (with the device-count and bandwidth gaps noted). [FACT, sharpening of COMM-302]

---

## Open questions / uncertainties

1. **The BW3 single-device anchor has two undisclosed quantities** (simultaneous device count, test channel bandwidth). The single-phone-rate chain (Section 2.3) is a well-supported inference, not a proven number, until these are known. [UNKNOWN, the load-bearing gap]
2. **No operator publishes a sustained per-USER rate under load**; the ~1 Mbps-or-less busy-cell figure is analyst (Farrar), not vendor. The single-phone PEAK (~25 to 50 Mbps lightly-loaded) is the founder's target; the loaded average is a separate, lower, undisclosed number. [UNKNOWN from vendors]
3. **No measured end-to-end latency for satellite DTC** (Starlink DTC or AST) is published; the ~20 to 50 ms is the broadband-LEO measured figure plus the propagation floor, not a measured DTC number. The propagation floor (~5 to 10 ms) is solid physics; the end-to-end DTC latency is a real evidence gap. [UNKNOWN, measured DTC latency]
4. **Linear-bandwidth scaling assumes constant spectral efficiency**, which requires the aperture and power to illuminate the wider channel at ~2 to 3 bps/Hz; at fixed array/power, spreading power over more bandwidth lowers SNR-per-Hz. The +2.4 to +2.8 dB net from low orbit is the margin that makes this plausible, but the exact achievable efficiency on a wider owned channel is not pinned. [ESTIMATE on the magnitude]
5. **Satellite power for a Neutron/Flatellite DTC satellite is UNKNOWN** (COMM-330); power is the second EIRP term alongside aperture gain, and it is decisive for whether a ~50 m^2 array closes the wider-bandwidth link at ~2 to 3 bps/Hz. [UNKNOWN, carried]
6. **The aperture-to-single-phone-rate mapping is anchored on revealed demonstrations, not a closed-form capacity-vs-aperture-vs-altitude-vs-bandwidth curve.** A first-principles joint curve would convert the ~50 m^2 -> 25 to 50 Mbps inference into an exact threshold; it is not in the corpus. [DERIVED, empirical]

---

## Sources

Per-cell vs per-phone and the scheduler mechanism:
- [AST How it Works (official): "up to 120 Mbps per coverage cell across more than 2,000 cells"](https://ast-science.com/how-it-works/)
- [AST Next-Generation BlueBird (official): 120 Mbps per cell, 2,000+ cells, 223 m^2](https://ast-science.com/next-gen-bluebird/)
- [AST FAQ (official): peak data transmission speeds of up to 120 Mbps per cell](https://ast-science.com/faqs/)
- [Direct-to-Cell: A First Look into Starlink's Direct Satellite-to-Device RAN through Crowdsourced Measurements (arXiv 2506.00283): ~3.1 Mbps per beam = upper-bound throughput per connection for a single user occupying the full beam bandwidth; 0.52 to 0.61 bps/Hz; PCS G-block 2x5 MHz; 2x25 MHz -> ~15.5 Mbps/beam](https://arxiv.org/html/2506.00283v8)
- [Tim Farrar / WIA white paper on Satellite D2D (May 2025): 120 Mbps is per-beam pool shared by hundreds-to-thousands of users in a 12 to 30 mile beam, per-user ~1 Mbps or less under load; AST 21 Mbps in a 5 MHz block shared by hundreds-to-thousands; Musk "current peak speed per beam and the beams are large"](https://wia.org/wp-content/uploads/2025/05/TMF-White-Paper-on-Satellite-D2D_May-2025.pdf)
- [From Cell Towers to Satellites: A 2040 Blueprint for Globally Connected 6G (arXiv 2507.14188): beam scheduling, one-phone-per-resource-block time-division](https://arxiv.org/abs/2507.14188)

AST BlueWalker 3 single-device demonstrations and array:
- [AST achieves space-based 5G connectivity / ~14 Mbps (AST official): single unmodified Samsung Galaxy S22, Hawaii](https://ast-science.com/ast-spacemobile-achieves-space-based-5g-cellular-broadband-connectivity-from-everyday-smartphones-another-historic-world-first/)
- [AST achieves 5G from space (SpaceNews): ~14 Mbps download record](https://spacenews.com/ast-spacemobile-achieves-space-based-5g-cellular-broadband-connectivity-from-everyday-smartphones/)
- [AST hits space-based LTE ~10 Mbps using AT&T spectrum, 850 MHz band (RCR Wireless)](https://www.rcrwireless.com/20230622/featured/ast-spacemobile-hits-space-based-lte-speeds-of-10-mbps-using-att-spectrum)
- [AST ~10 Mbps download in Hawaii tests (Fierce)](https://www.fierce-network.com/tech/ast-spacemobile-touts-10-mbps-download-speeds-during-tests-hawaii)
- [AST SpaceMobile (Wikipedia): up to 21 Mbit/s demonstrated; 693 sq ft / 64 m^2 BW3 array; ~508 to 527 km operating altitude; first call Midland TX to Japan](https://en.wikipedia.org/wiki/AST_SpaceMobile)
- [AST BlueWalker 3 voice calls (Via Satellite): first two-way voice from an unmodified phone](https://www.satellitetoday.com/connectivity/2023/04/25/ast-spacemobile-reports-making-voice-calls-with-bluewalker-3-satellite/)
- [AST Block 2 BlueBirds reach orbit (TechTimes): Block 1 device peak 98.9 Mbps, Block 2 design ~200 Mbps to standard smartphones](https://www.techtimes.com/articles/318740/20260620/ast-spacemobile-block-2-bluebirds-reach-orbit-satellite-broadband-direct-your-phone-nears.htm)

Aperture-to-rate physics and link budget:
- [Spectrum Opportunities for the Wireless Future (arXiv 2506.18672): G = 4 pi eta A / lambda^2 = 42 dBi at 223 m^2 / 880 MHz; 40 MHz beam -> 120 Mbps; ~500 kbps/user at 5% beam load](https://arxiv.org/html/2506.18672v1)
- [T-Mobile + SpaceX Direct Satellite-to-Handset (Frank Rayal): handset 23 dBm / 0 dBi; ~29 dBi / ~1.4 m^2 satellite aperture for ~32 kbps on 5 MHz](https://frankrayal.com/2022/08/29/t-mobile-spacex-direct-satellite-to-handset-service-lots-of-hype-and-little-reality/)
- [AST BlueBird 1-5 (official): Block 1 up to 40 MHz per beam, 850 MHz, 120 Mbps per cell](https://ast-science.com/bluebird-1-5/)

Latency:
- [ITU-T G.114 One-way transmission time: 150 ms preferred / 400 ms unacceptable thresholds](https://www.itu.int/rec/T-REC-G.114)
- [Starlink latency explained, ~1.8 ms one-way propagation (SpeedTestHQ)](https://speedtesthq.com/guides/satellite/starlink-latency-explained)
- [Latency in LEO satellites vs terrestrial fiber (Frank Rayal)](https://frankrayal.com/2021/07/07/latency-in-leo-satellites-vs-terrestrial-fiber/)
- [Starlink ~45 ms median latency, Ookla Q1 2025 (RCR Wireless)](https://www.rcrwireless.com/20250616/test-and-measurement/starlink-speeds)
- [Starlink smokes GEO operators in speed/latency (Light Reading)](https://www.lightreading.com/satellite/starlink-smokes-geo-satellite-operators-in-speed-latency-report)
- [Satellite internet speeds and latency, GEO ~600 to 700 ms vs LEO (Orbital Radar)](https://orbitalradar.com/satellite-internet/speeds-and-latency)
- [GEO satellite internet cannot compete with LEO on latency (IEEE ComSoc)](https://techblog.comsoc.org/2025/07/18/geo-satellite-internet-from-hughesnet-and-viasat-cant-compete-with-leo-starlink-in-speed-or-latency/)
- [Starlink DTC shell ~340 to 360 km (FCC DA-24-1193)](https://docs.fcc.gov/public/attachments/DA-24-1193A1.pdf)
- [Iridium vs Inmarsat satphone latency (OSAT): LEO natural-feeling calls vs GEO perceptible delay](https://osat.com/blogs/blog/comparison-between-iridium-and-inmarsat-satellite-phones)
- *(Slant ranges, footprint, and the ~3.5 to 4 dB altitude trim cross-referenced from `leo_constellation_coverage_minimums.md` COMM-209/217 and `dtc_system_model.md` COMM-316; not re-listed.)*

---

## Claims ledger (COMM-336..355)

For the catalog/reconciliation step to ingest. Each hard claim with sources and tag; single-source and projection claims flagged. IDs COMM-336 through COMM-355 reserved for this doc. Cross-references existing IDs heavily.

- **COMM-336**, Published DTC throughput figures are PER-CELL / PER-BEAM (a shared pool), not per-single-phone: AST's "up to 120 Mbps" is explicitly "per coverage cell across more than 2,000 cells," shared across the hundreds-to-thousands of phones in a ~30 to 48 km beam. [FACT] Sources: AST How-It-Works, AST Next-Gen BlueBird, AST FAQ; Farrar/WIA white paper (beam-sharing).
- **COMM-337**, Starlink's measured ~3.1 Mbps is PER BEAM and equals the single-user-when-alone bound: the source states it is "an upper-bound estimate of the throughput per connection, corresponding to the scenario of a single user occupying the full bandwidth of the beam," at 0.52 to 0.61 bps/Hz on PCS G-block 2x5 MHz during the SMS phase. [FACT] Source: arXiv 2506.00283.
- **COMM-338**, AST BlueWalker 3 demonstrated SINGLE-DEVICE downlinks of ~10.3 Mbps (Jun 2023, LTE), ~14 Mbps (Sep 2023, with first space-based 5G), and up to ~21 Mbps (peak), each to one unmodified phone alone in an idle test cell on one ~5 MHz channel; the ~21 Mbps is the per-channel beam capacity going to one phone. [FACT for the rates; single-device read is FACT-from-press-language + analyst (Farrar); the simultaneous device count and exact test bandwidth are UNKNOWN] Sources: RCR Wireless, Fierce (10.3); AST press, SpaceNews (14 + 5G); Wikipedia/AST, Farrar/WIA (21 in a 5 MHz block).
- **COMM-339**, The per-cell figure and the best-case single-phone figure CONVERGE when one phone is alone in the cell (it is scheduled across the whole pool, so per-cell-when-alone = single-phone peak) and DIVERGE when the cell is busy (the pool time-shares across all active phones, dropping per-user to ~1 Mbps or less per the analyst). [DERIVED + FACT] Sources: this doc Section 1.2; Farrar/WIA (per-user ~1 Mbps or less under load); arXiv 2506.18672 (~500 kbps/user at 5% load); cross-ref COMM-317 (count not a per-phone-rate lever).
- **COMM-340**, A satellite DTC beam serves users by a time-division scheduler, one phone per resource block at an instant, identical in principle to a terrestrial cell; a lightly-loaded cell hands the near-full beam to one phone (why the demonstrated single-device speeds equal the per-channel beam capacity), a busy cell splits it; beams are huge (~12 to 30 mile, AST ~48 km) so the user count per beam is large. [FACT] Sources: Farrar/WIA white paper; arXiv 2507.14188 (beam scheduling); arXiv 2506.00283.
- **COMM-341**, The founder's product target is a single-phone PEAK / lightly-loaded rate (~25 to 50 Mbps to ONE phone), the correct quantity to size aperture and bandwidth against, distinct from the per-cell aggregate (AST 120 Mbps/cell) and the busy-cell per-user average (~1 Mbps or less). [DERIVED] Source: this doc Sections 0, 1.2, 4.
- **COMM-342**, AST publishes per-cell capacity and single-device PEAKS (Block 1 ~98.9 Mbps, Block 2 design ~200 Mbps to standard smartphones) but NOT a sustained per-USER rate under load; the loaded per-user rate (~1 Mbps or less) is analyst (Farrar), a named gap in AST's disclosure. [FACT for 98.9 (AST-originated); ESTIMATE for ~200 design; UNKNOWN for AST loaded per-user] Sources: TechTimes (98.9 / ~200); Farrar/WIA (loaded ~1 Mbps).
- **COMM-343**, Aperture-to-gain at ~880 MHz (G = 4 pi eta A / lambda^2, eta ~0.7, anchored on 223 m^2 -> ~42 dBi): ~25 m^2 ~32.5 dBi, ~50 m^2 ~35.5 dBi, ~64 m^2 ~36.5 dBi, ~100 m^2 ~38.5 dBi; the gain steps (10 log10 area ratio) are 25->50 +3.01 dB, 50->64 +1.07 dB, 64->223 +5.42 dB. [DERIVED, gain steps exact; the 223->42 dBi anchor is FACT/derived in the literature] Source: arXiv 2506.18672; this doc Section 2.2.
- **COMM-344**, AST's "up to 120 Mbps per cell" is exactly 40 MHz x ~3 bps/Hz, which is the single-phone peak when one phone owns the beam; a single phone reaching ~50 Mbps therefore needs ~17 MHz at 3 bps/Hz, ~20 MHz at 2.5, or ~25 MHz at 2, all inside AST's 40 MHz / 120 Mbps-per-cell envelope on a comparable aperture. [DERIVED] Sources: arXiv 2506.18672 (40 MHz -> 120 Mbps); AST BlueBird 1-5 (40 MHz/beam); this doc Section 2.
- **COMM-345**, ~50 m^2 is only ~1.07 dB below the ~64 m^2 BlueWalker 3 array that demonstrated ~21 Mbps to a phone, so in aperture (gain) terms the founder's middle array is essentially the BW3 array. [DERIVED, anchored on COMM-338] Source: this doc Section 2.2/2.3.
- **COMM-346**, Dropping 550 -> 350 km buys ~3.5 to 3.9 dB of path loss at useful elevations (30 to 90 deg), tapering to ~2.9 dB at the 10 deg horizon (20 log10 slant ratio); this more than offsets the ~1.07 dB aperture shrink from 64 to 50 m^2, leaving ~+2.4 to +2.8 dB net link improvement versus BW3. [DERIVED] Sources: slant ranges COMM-209; this doc Section 2.2; consistent with COMM-316 (~3.5 to 4 dB).
- **COMM-347**, Synthesis: ~50 m^2 is enough for ~25 to 50 Mbps to ONE phone, given low orbit (~350 to 400 km) and ~20 to 40 MHz of owned downlink at ~2 to 3 bps/Hz; ~64 to 100 m^2 is NOT needed for the single-phone RATE (the extra aperture buys per-cell CAPACITY: concurrent users, smaller cells, more beams). This sits at the Tier-1 rung (COMM-320), above the ~25 m^2 floor, below the ~60+ m^2 Tier-2 broadband rung. [DERIVED, well-supported inference] Sources: this doc Section 2.3; chain anchored on COMM-338 (BW3 ~21 Mbps), COMM-343/346 (gain/altitude), COMM-344 (bandwidth); governing rule COMM-320.
- **COMM-348**, The single-phone-rate chain has two named soft spots: the BW3 anchor's undisclosed simultaneous-device-count and test-channel-bandwidth (if 21 Mbps was a multi-device aggregate, the start point is lower), and linear-bandwidth scaling assuming constant ~2 to 3 bps/Hz (spreading fixed power over more bandwidth lowers SNR-per-Hz; the ~+2.4 to +2.8 dB net from low orbit is the margin that makes it plausible). [UNKNOWN on the device count/bandwidth; ESTIMATE on the efficiency magnitude] Source: this doc Section 2.4.
- **COMM-349**, ARITHMETIC CORRECTION: the corpus's "1 dB of link gain improves the rate by a factor ~1.58" (COMM-299, COMM-316) is mislabeled; +1 dB = x1.26 (10^0.1 = 1.259) and the ~1.585 factor is +2 dB (10^0.2). The multiplicative-rate rule holds only in the low-SNR / power-limited regime (DTC handset links qualify, as an approximation). Corrected, ~3.5 to 3.9 dB maps to ~1.95x to ~2.45x rate. [DERIVED; flag for the catalog pass to fix COMM-299/316, NOT edited here] Source: this doc Section 2.5.
- **COMM-350**, Low LEO (~350 to 550 km) round-trip PROPAGATION (4-segment phone-sat-gateway-sat-phone) is ~5 to 10 ms, versus GEO's ~240 to 280 ms (up+down only; a single GEO uplink leg ~119 to 125 ms exceeds an entire LEO end-to-end session); a ~30 to 50x physics gap. [DERIVED for the floors; FACT for the GEO one-way] Sources: SpeedTestHQ, Frank Rayal (LEO one-way ~1.8 ms); Orbital Radar, IEEE ComSoc (GEO ~120 ms one-way); this doc Section 3.1.
- **COMM-351**, Measured END-TO-END latency: low/broadband LEO ~25 to 60 ms (Starlink ~45 ms median, Ookla Q1 2025) versus GEO ~600 to 700 ms, a ~15x real-world difference; end-to-end is always larger than propagation (adds modulation/demod, scheduling/queuing, ground routing). [FACT] Sources: RCR Wireless, Light Reading (Starlink ~45 ms); Orbital Radar, IEEE ComSoc (GEO ~600 to 700 ms).
- **COMM-352**, ITU-T G.114 (One-way transmission time) puts interactive voice at 0 to 150 ms one-way "preferred," 150 to 400 ms degrading, above 400 ms "unacceptable"; a low-LEO DTC link spends only ~5 to 10 ms round-trip on the satellite hop, leaving the entire "good" band free for codec/jitter/backhaul (so a satellite call feels like a normal mobile call), while a GEO two-hop voice path reaches ~250 to 300 ms+ one-way, into the degraded-to-unacceptable band. Low orbit is a structural product advantage for a phone service independent of rate. [FACT for the thresholds; DERIVED for the budget consequence] Sources: ITU-T G.114; this doc Section 3.3; field proof Iridium (LEO) vs Inmarsat/Thuraya (GEO) (OSAT).
- **COMM-353**, No MEASURED end-to-end latency for satellite DTC (Starlink DTC or AST) is published; the ~20 to 50 ms is the broadband-LEO measured figure plus the propagation floor, not a measured DTC number; the propagation floor (~5 to 10 ms) is solid physics, the end-to-end DTC latency is a real evidence gap. [UNKNOWN, measured DTC latency] Source: arXiv 2506.00283 (SMS-only beta measured RAN params, not latency); this doc Section 3.1.
- **COMM-354**, REFINEMENT to the corpus AST altitude: AST's PLANNED operational constellation is ~725 to 740 km (per its FCC petition), higher than the ~507 to 523 km BlueBird/BW3 operating altitude carried in COMM-319/321; the 42 dBi gain is altitude-independent (aperture x frequency), so the aperture analysis is unaffected, but this weakens any "AST flies low" reading. The founder's Tier-1 product flies LOW (~350 to 550 km) regardless, so the low-orbit advantage is the entrant's, not AST's. [FACT, refinement; flag for the catalog pass] Source: AST FCC petition reporting; cross-ref COMM-319/321.
- **COMM-355**, Net per-phone operating point for the Neutron Tier-1 DTC business: a ~50 m^2 array at low orbit (~350 to 550 km) on ~20 to 40 MHz of OWNED spectrum delivers ~25 to 50 Mbps to a single lightly-loaded phone (single-phone PEAK, not the per-cell 120 Mbps aggregate nor the busy-cell ~1 Mbps average), plus a structural latency advantage (~5 to 10 ms propagation, inside ITU-T G.114's good band) that GEO cannot match; the rate is aperture (gain) AND owned bandwidth, so the spectrum gate (COMM-325) co-determines it, and the per-satellite/Flatellite power and capacity remain UNKNOWN (COMM-322/324/330). No verdict. [DERIVED/SYNTHESIS] Sources: this doc Sections 0, 4; grounds in COMM-336..354, COMM-320 (governing rule), COMM-325 (spectrum), COMM-338 (BW3 anchor).

### Aperture-to-single-phone-rate curve block (Section 2.6): COMM-371..385

Section 2.6 extends the grounded single-phone-rate method down to the FLAT ~25 m^2 Flatellite aperture to resolve the flat-versus-fold fork. IDs COMM-371 through COMM-385 are reserved for this block; COMM-371..378 are used, COMM-379..385 held in reserve (ceiling not exceeded). (COMM-356..370 are the integration block carried in [`dtc_system_model.md`](dtc_system_model.md); this doc's own reserved block was COMM-336..355, and COMM-371 is the next free contiguous start above the model's reserved 356..370.)

- **COMM-371**, The flat-versus-fold architecture fork: the Rocket Lab Flatellite is a FLAT body that is its own aperture (it does NOT fold, which is how it stacks ~16/Neutron, COMM-263), capped by Neutron's ~5.5 m fairing footprint at roughly ~20 to 25 m^2 (a 5.0 m square ~= 25 m^2); the ~50 m^2 Section-2.3 operating point is ~7.07 m on a side, exceeds the fairing, and must FOLD to ~3/Neutron (COMM-362). The decision-critical question is whether a flat ~25 m^2 aperture already clears the ~25 Mbps single-phone bar (keep the flat many-per-launch stack) or falls short (require the ~50 m^2 fold), a ~5x swing in satellites-per-launch (flat ~6 to 16 vs folded ~3). [SYNTHESIS, framing] Sources: this doc Section 2.6; grounds in COMM-263 (Flatellite flat/no-fold), COMM-362 (flat-to-fold cliff), COMM-322 (flat counts).
- **COMM-372**, Aperture gain step relative to the ~64 m^2 BW3 anchor (10 log10(A/64), exact, frequency/altitude-independent): ~25 m^2 = -4.08 dB, ~50 m^2 = -1.07 dB, ~64 m^2 = 0.00 dB. [DERIVED] Sources: this doc Section 2.6.2; anchor COMM-338.
- **COMM-373**, Net single-phone link delta versus the BW3 demonstration (aperture step + low-orbit gain of +3.5 to 3.9 dB at ~350 vs ~513 km): ~25 m^2 = -0.58 to -0.18 dB (NEAR-PARITY with BW3), ~50 m^2 = +2.43 to +2.83 dB, ~64 m^2 = +3.50 to +3.90 dB; in the power-limited regime (10^(dB/10)) these are rate-multipliers of 0.87 to 0.96x, 1.75 to 1.92x, and 2.24 to 2.45x respectively, i.e. link-only single-phone rates (at BW3's own bandwidth) of ~18 to 20 Mbps, ~37 to 40 Mbps, ~47 to 52 Mbps. The flat ~25 m^2 aperture's ~4.08 dB shrink is almost entirely erased by the low-orbit gain, so flying low is what makes the small flat aperture viable. [DERIVED] Sources: this doc Section 2.6.2; grounds in COMM-338 (anchor), COMM-346 (low-orbit gain), COMM-356 (dB-to-rate factor), COMM-372 (aperture steps).
- **COMM-374**, The owned-spectrum single-phone rate, R = bandwidth x spectral efficiency at ~2 to 3 bps/Hz: 20 MHz -> 40 to 60 Mbps, 30 MHz -> 60 to 90 Mbps, 40 MHz -> 80 to 120 Mbps. Aperture enters not as a separate multiplier on this table but as whether the array+power sustains ~2 to 3 bps/Hz across the owned channel; the net-link margins (COMM-373) are that evidence (~64 m^2 most headroom, ~25 m^2 ~0 dB / near-parity, sustaining essentially BW3's efficiency with the low-orbit gain spent on erasing the aperture shrink). [DERIVED] Sources: this doc Section 2.6.3; grounds in COMM-344 (40 MHz -> 120 Mbps envelope), COMM-373.
- **COMM-375**, VERDICT: a FLAT ~25 m^2 Flatellite at low orbit (~350 km) on owned spectrum CLEARS ~25 Mbps to a single lightly-loaded phone on its own, so the fold is NOT required for the ~25 Mbps bar. Two reads agree: (bandwidth) 25 Mbps needs only ~8.3 MHz at 3 bps/Hz, ~10 at 2.5, or ~12.5 at 2 bps/Hz, the BOTTOM of the owned 20 to 40 MHz range, and even at the bottom (20 MHz) and a conservative 2 bps/Hz the array reaches ~40 Mbps; (link) the flat ~25 m^2 array is at ~parity with the ~64 m^2 BW3 link that already did ~21 Mbps to one phone, so a wider owned channel lifts it through 25 Mbps. The full ~25 to 50 Mbps band is reached from the bottom-to-middle of 20 to 40 MHz. [DERIVED, decision-critical] Sources: this doc Section 2.6.4; grounds in COMM-373, COMM-374, COMM-338 (BW3 anchor).
- **COMM-376**, Consequence for the fork: because the flat ~25 m^2 Flatellite clears ~25 Mbps on its own, the architecture keeps the FLAT no-deploy many-per-launch stack (~6 default to ~16 render-read ceiling, the flat counts of COMM-362/322), NOT the ~3/Neutron folded count; folding to ~50 m^2 is a margin/per-cell-capacity choice for the TOP of the band (~50 Mbps with ~+2.4 to +2.8 dB net headroom), not a requirement for ~25 Mbps. The ~5x satellites-per-launch swing (flat ~16 vs folded ~3) does not have to be paid to reach ~25 Mbps to one phone. [DERIVED] Sources: this doc Section 2.6.4; grounds in COMM-375, COMM-362 (per-launch counts), COMM-322 (flat default/ceiling).
- **COMM-377**, UNKNOWN that can flip the fork (the single biggest soft spot): BW3's simultaneous device count. The chain assumes ~21 Mbps was to ONE phone; if it was a multi-device aggregate of N phones, the single-phone start is ~21/N and the flat ~25 m^2 link-only rate falls proportionally (N=1 ~18 to 20 Mbps, N=2 ~9.6 Mbps at BW3 bandwidth, N=3+ needs the full top of 20 to 40 MHz). At N>=2 the flat-25 comfortable margin erodes and the ~50 m^2 fold (with ~+2.4 to +2.8 dB more link margin) becomes the safer route to a firm ~25 Mbps. AST never asserted the device count; press language + Farrar point to one device, hence N=1 is the working assumption. [UNKNOWN, direction-stated] Sources: this doc Section 2.6.5; grounds in COMM-338 (the two undisclosed BW3 quantities), COMM-348.
- **COMM-378**, UNKNOWN that caps confidence (bites the flat case harder): BW3's test channel bandwidth, via the constant ~2 to 3 bps/Hz assumption. R = B x eff assumes the array+power holds ~2 to 3 bps/Hz across the WIDER owned 20 to 40 MHz channel; if BW3's 21 Mbps came on a narrow channel (~5 MHz, ~4.2 bps/Hz), spreading the flat ~25 m^2 array's fixed power over a wide owned channel lowers SNR-per-Hz, and the flat array's ~0 dB net margin (vs the ~50 m^2 case's +2.4 to +2.8 dB) gives it less headroom to defend the efficiency. Conservatism floor: even at 2 bps/Hz, 25 Mbps needs only ~12.5 MHz, so the bar clears unless wide-channel efficiency collapses below ~1.25 bps/Hz; the comfortable cushion, not the bar itself, is the part at risk. [Mechanism FACT, magnitude ESTIMATE/UNKNOWN] Sources: this doc Section 2.6.5; grounds in COMM-348, COMM-313 (DTC spectral efficiency floor).

---

*COMM-336..355 created by this doc (the original reserved block, not exceeded), plus COMM-371..385 (the Section-2.6 aperture-curve block, of which COMM-371..378 are used; COMM-356..370 belong to the [`dtc_system_model.md`](dtc_system_model.md) integration block, so COMM-371 is the next free contiguous start). Catalog rows for LIBRARY.md / RESEARCH_TRACKER.md / SOURCE_INDEX.md are returned to the catalog/reconciliation agent, not edited here. This doc is not committed by this pass.*
