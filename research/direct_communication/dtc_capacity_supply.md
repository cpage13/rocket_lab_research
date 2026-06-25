# Direct-to-Cell Capacity Supply: Per-Satellite Throughput for a Flat ~20-24 m^2 Array, the Spectrum-Saturation Ceiling, and the Speed-vs-Users Tradeoff

**Research date:** 2026-06-23
**Status:** Understanding-building input for the SUPPLY side of a Neutron direct-to-cell (DTC) model. No go/no-go verdict. This doc pins the PER-SATELLITE total capacity of a FLAT ~20-24 m^2 phased array on ~25 MHz of owned spectrum (the full chain, with the beam count flagged as the softest input), the SPECTRUM-SATURATION CEILING (the founder's "past some point more satellites stop helping speed" point, where beams overlap and the system goes interference-limited), and the SPEED-vs-USERS tradeoff (per-cell capacity divided by active users = sustained per-user speed, as a formula plus a worked example). Every value is flagged sourced (FACT) / derived (DERIVED) / estimate (ESTIMATE) / unknown (UNKNOWN).

> **Why this document exists.** The corpus owns the per-PHONE link budget (a ~50 m^2 array at low orbit on ~20-40 MHz owned spectrum delivers ~25-50 Mbps to ONE lightly-loaded phone, [`dtc_per_phone_rate_and_latency.md`](dtc_per_phone_rate_and_latency.md) COMM-361) and the governing rule (aperture + owned spectrum set the tier, altitude is a weak trim, count is never a per-phone-rate lever, [`dtc_system_model.md`](dtc_system_model.md) COMM-320). What it has NOT pinned is the SUPPLY-side total: how much aggregate throughput one flat satellite produces, and the two relationships the founder asked for explicitly: (1) where adding satellites STOPS raising per-user speed (the spectrum-saturation ceiling), and (2) the speed-vs-active-users curve. The founder benchmarks against terrestrial 5G (~170-180 Mbps down, ~$80/mo) and will accept a satellite service at ~20-30 Mbps ONLY if it is much cheaper, wants the FEWEST satellites for the best speed and broadest coverage, and notes that past some point more satellites do not help. That "point" is set by per-satellite capacity and the fixed spectrum, and this doc grounds it.

> **Grounds in and does NOT re-derive (this doc adds the AGGREGATE-CAPACITY and SATURATION layer on top of the per-phone link the corpus owns):**
> - [`dtc_system_model.md`](dtc_system_model.md) (COMM-315..335, COMM-356..370): owns the GOVERNING RULE (four levers, count not a per-phone-rate lever, the two tiers). This doc takes the rule as given and quantifies the per-satellite CAPACITY (the aggregate the rule's "count buys total capacity" clause refers to) and the saturation point.
> - [`dtc_per_phone_rate_and_latency.md`](dtc_per_phone_rate_and_latency.md) (COMM-336..355, COMM-371..378): owns the per-cell-vs-per-phone split and the single-phone rate (~25-50 Mbps). This doc uses the same scheduler mechanism and the same ~2-3 bps/Hz efficiency, applied to the WHOLE satellite (beams x per-cell x reuse), and to the per-user-under-load curve.
> - [`dtc_antenna_aperture_tradeoff.md`](dtc_antenna_aperture_tradeoff.md) (COMM-293..314): owns the aperture-to-gain physics (G = 4 pi eta A / lambda^2) and the aperture ladder. This doc uses the gain relation to scale the BEAM COUNT from AST's 223 m^2 / ~2,500 beams down to a flat ~20-24 m^2 array.
> - [`economics/comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) (COMM-141, COMM-142): owns the AST capacity-physics anchor (~10 GHz processing, ~2,000-2,500 cells, ~20.3 km / ~324 km^2 narrowest beam, ~56 Gbps theoretical per satellite). This doc uses ~56 Gbps as the processor/backhaul cap anchor and the ~324 km^2 beam as the footprint anchor.
> - [`spectrum_generations_and_availability.md`](spectrum_generations_and_availability.md) (COMM-108, COMM-114) and [`leo_constellation_coverage_minimums.md`](leo_constellation_coverage_minimums.md) (COMM-224, COMM-226): own the spatial-reuse / Shannon-x-beams capacity framework and the coverage-vs-capacity regime split. This doc takes the framework and adds the SATURATION ceiling (where reuse stops scaling).
> - [`competitors/starlink_v3_specs.md`](../competitors/starlink_v3_specs.md) (COMM-271..292 platform; specs-doc claims): owns the V3 / V2-mini D2C capacity numbers (V2-mini D2C ~7 Gbps aggregate / 48 beams x ~7 Mbps; V3 D2C ~700 Gbps projection). This doc uses both as the upper and lower per-satellite anchors.
> - Cross-references (not re-listed): [`spectrum_purchase_and_6g.md`](spectrum_purchase_and_6g.md) (the ~25 MHz owned-spectrum cost), [`flatellite_platform.md`](../rocket_lab/flatellite_platform.md) (the flat body-is-aperture platform).

> **Tagging.** **[FACT]** sourced (multi-source unless flagged single-source), **[DERIVED]** computed in this doc from sourced inputs, **[ESTIMATE]** a third-party model/target/projection, **[UNKNOWN]** a named gap (not invented). New claims use **COMM-406..425** (the reserved block; not exceeded). No em-dashes anywhere.

---

## 0. Answer first (the supply side in one screen)

**A flat ~20-24 m^2 phased array on ~25 MHz of owned spectrum at low orbit produces roughly ~5-15 Gbps of total per-satellite DTC throughput, set by BEAMS (~200-450 for a flat ~20-24 m^2 array, scaled from AST's ~2,500 at 223 m^2) times PER-CELL capacity (~25 MHz x ~2-3 bps/Hz = ~50-75 Mbps/cell) times the fraction of beams reusing the same ~25 MHz at once, and bounded WELL BELOW the per-beam-times-cell raw product by the fixed ~25 MHz of owned spectrum, not by the onboard processor. The spectrum-saturation ceiling is the founder's load-bearing point: over a FIXED ground area on a FIXED ~25 MHz, total deliverable bits are capped at ~(25 MHz x spectral efficiency x the number of non-overlapping beams the geometry allows), and adding satellites past the point where their beams overlap and share that same ~25 MHz STOPS raising per-user speed, because the extra beams interfere rather than add (the system goes interference-limited). The speed-vs-users tradeoff is then a simple division: sustained per-user speed = per-cell capacity / active users in the cell, so a ~50-75 Mbps cell serving 50 active users gives ~1-1.5 Mbps each, and hitting a ~20-30 Mbps sustained target requires holding active users per cell to roughly 2-4, which over a populated band forces either many more beams (more/bigger satellites or more spectrum) or accepting that only a thin, lightly-loaded slice of users gets the headline speed.**

1. **Per-satellite total capacity (Section 2), the full chain.** Total per-sat throughput = beams x per-cell capacity x spatial-reuse fraction, capped by min(owned spectrum, onboard processor). For a flat ~20-24 m^2 array: **~200-450 beams** (scaled from AST's ~2,500 at 223 m^2 by the ~9-11x aperture ratio; this is the SOFTEST input), **~50-75 Mbps per cell** (25 MHz x 2-3 bps/Hz), and a spatial-reuse fraction set by how many of those beams can use the same 25 MHz simultaneously without interfering. The raw beam-times-cell product (~10-34 Gbps) is the OPTIMISTIC bound; the realistic per-satellite total lands **~5-15 Gbps**, because the fixed ~25 MHz and inter-beam interference bind before the processor does. This brackets the two flying anchors: Starlink V2-mini D2C ~7 Gbps aggregate (48 beams x ~7 Mbps) and AST Block 2 ~56 Gbps (2,800 cells x 20 Mbps, on 8x the spectrum and 10x the aperture). [DERIVED, beam count UNKNOWN-grade]

2. **The spectrum-saturation ceiling (Section 3), the founder's "more satellites stop helping" point.** Over a FIXED ground area on a FIXED ~25 MHz, the maximum deliverable bits/s = 25 MHz x spectral efficiency x N_reuse, where N_reuse is the number of beams that can simultaneously reuse the 25 MHz over that area WITHOUT their footprints overlapping (set by beam width / angular separation, not by satellite count). Once enough satellites are overhead that every patch of ground is already covered by a beam on the 25 MHz, **adding more satellites adds OVERLAPPING co-channel beams that interfere rather than add capacity**, and per-user speed stops rising (the system is interference-limited, not coverage-limited). This is multi-source: full frequency reuse "leads to severe inter-beam co-channel interference and degrades SINR," and "overlaps of multiple co-channel beams can reduce the communication capacity," so beyond the reuse limit more satellites do not raise per-user speed. [FACT for the mechanism, multi-source; DERIVED for the 25 MHz-specific ceiling]

3. **The speed-vs-users tradeoff (Section 4), a formula plus a worked example.** Sustained per-user speed = per-cell capacity / active users in the cell (the cell's ~25 MHz pool time-shared by the scheduler). So **per_user = (25 MHz x eff) / users_active**. Worked: a ~50-75 Mbps cell serving 50 active users gives ~1-1.5 Mbps each; serving 5 gives ~10-15 Mbps; serving 2-3 gives ~20-30 Mbps. To DELIVER ~20-30 Mbps sustained you must hold active users per cell to ~2-4, and the number of users a fleet can serve at that target = (total beams across the fleet over the area) x (2-4 users/beam). Over a populated band the active-user density is the binding input: a ~324 km^2 beam over even lightly-populated ground with ~0.5% concurrency can hold thousands of attached phones but only a few dozen ACTIVE at once, so the 20-30 Mbps headline is a lightly-loaded / scheduled-priority number, not a whole-population number. [DERIVED, formula + example]

The rest sources and derives each point.

---

## 1. The supply-side model (beams x per-cell x reuse, capped by spectrum or processor)

The per-PHONE link (the corpus) answers "how fast to ONE phone." The SUPPLY side answers "how much TOTAL the satellite produces, and how that total divides." The governing identity, assembled from the corpus's own pieces:

```
Per-satellite total DTC capacity  =  N_beams  x  C_cell  x  f_reuse        [bits/s]
                                      bounded above by  min( C_spectrum , C_processor )

  N_beams      = number of simultaneous beams/cells the phased array forms   (scales with aperture)
  C_cell       = per-cell capacity = B_owned x SE                            (Shannon, owned bandwidth x spectral efficiency)
  f_reuse      = fraction of beams that can reuse B_owned at once            (spatial-reuse efficiency, <1, interference-set)
  C_spectrum   = B_owned x SE x N_reuse_max                                  (the spectrum-and-reuse hard cap over a footprint)
  C_processor  = onboard digital-processing / backhaul bandwidth limit       (AST: ~10 GHz processing -> ~56 Gbps realized)
```

[Framework DERIVED from the corpus: Shannon C = B log2(1+SNR) and the beams-x-reuse area-capacity model are COMM-108 / COMM-224 / COMM-114; the per-cell B x SE form and the ~2-3 bps/Hz are COMM-344 / COMM-114; the processor cap is the AST ~10 GHz / ~56 Gbps anchor COMM-141/142.]

The load-bearing reading: **per-satellite capacity is the product of how many beams you form and how much each beam carries, but the fixed owned bandwidth caps the whole thing**, because every beam that reuses the same 25 MHz competes for the same Shannon pool. The processor (~10 GHz on AST) is a SECOND cap, but on a thin ~25 MHz owned slice the SPECTRUM binds long before the processor does (Section 2.4). This is the supply-side statement of the corpus's "DTC is spectrum-starved" finding (COMM-313, COMM-333).

### 1.1 The anchors this model must bracket

| System | Aperture | Owned/used spectrum | Beams/cells | Per-cell rate | Per-satellite aggregate | Tag |
|---|---|---|---|---|---|---|
| Starlink V2-mini D2C | ~25 m^2 | 2x5 MHz (PCS G), SMS phase | 48 down | ~7 Mbps/beam (fronthaul-limited) | **~7 Gbps aggregate class** | [FACT] |
| Starlink V3 D2C (projected) | ~25 m^2-class deployable | ~65 MHz owned (EchoStar) | undisclosed | ~2-10 Mbps sustained/user | **~700 Gbps projected** | [ESTIMATE/projection] |
| AST BlueBird Block 2 | ~223 m^2 | up to 40 MHz/beam | ~2,000-2,500 (one analyst 2,800) | up to ~120 Mbps/cell | **~56 Gbps theoretical** (2,800 x 20 Mbps) | [FACT cells; DERIVED 56 Gbps] |
| **Flat ~20-24 m^2 (this model)** | **~20-24 m^2** | **~25 MHz owned** | **~200-450 (scaled, SOFT)** | **~50-75 Mbps/cell** | **~5-15 Gbps (Section 2)** | **[DERIVED]** |

Sources: V2-mini D2C 48 beams x ~7 Mbps / ~7 Gbps aggregate ([thexlab.org working paper](https://thexlab.org/wp-content/uploads/2025/07/Starlink_Analysis_Working_Paper_v0.2.pdf), [NextBigFuture](https://www.nextbigfuture.com/2025/09/spacex-15000-v3-starlink-direct-to-cellphone-satellites.html)); V3 D2C ~700 Gbps / >100x V2 ([NextBigFuture](https://www.nextbigfuture.com/2025/09/spacex-15000-v3-starlink-direct-to-cellphone-satellites.html), confirms 700 Gbps, >100x, 15,000 sats, 326-335 km, ~2-100 Mbps/user beam-sharing-dependent); AST ~2,500 beams / 40 MHz / 120 Mbps-cell / 42 dBi / 3 bps/Hz / 20.3 km / 324 km^2 ([arXiv 2506.18672](https://arxiv.org/html/2506.18672v1), confirmed verbatim: "2500 adjustable antenna beams," "every downlink beam supporting a bandwidth over 40 MHz," "20.3 km," "324 km^2," "42 dBi," "3 bps/Hz"); AST ~56 Gbps theoretical / 2,800 cells x 20 Mbps ([Fierce/Madden via comms_direct_to_cell.md](../economics/comms_direct_to_cell.md) COMM-142); AST5000 ASIC handling ">2,000 coverage cells" / "up to 2,500 uplink beams" ([TechTimes](https://www.techtimes.com/articles/318740/20260620/ast-spacemobile-block-2-bluebirds-reach-orbit-satellite-broadband-direct-your-phone-nears.htm), [Mobile World Live](https://www.mobileworldlive.com/ast-spacemobile/us-fcc-licences-next-gen-ast-satellite-test/)).

Any flat-array estimate must sit between the ~7 Gbps Starlink V2-mini D2C floor (similar ~25 m^2-class aperture but thinner spectrum) and well below the ~56 Gbps AST ceiling (10x the aperture, 8x the spectrum). A ~20-24 m^2 array on ~25 MHz, roughly the Starlink aperture on ~2.5x the spectrum, lands a few-to-low-tens of Gbps. [DERIVED]

---

## 2. Per-satellite total capacity for a flat ~20-24 m^2 array on ~25 MHz (the full chain)

### 2.1 N_beams: how many beams a flat ~20-24 m^2 array forms (the softest input, flagged)

The number of simultaneous beams a phased array forms scales with its aperture (more area / more elements = more, narrower beams). The clean physics: beam angular width is inverse to aperture diameter, so a larger aperture both makes each beam narrower (smaller cell) AND lets the array place more independent beams across its field of view; the beam count tracks aperture AREA for a fixed cell-size goal. [FACT, phased-array physics: aperture is inversely related to beam angular size, and an array's independent-beam count scales with element count / aperture area, [USPTO 12200508 / beamforming refs](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12200508), [Kilic, Radio Science 2009, multi-spot-beam aperture scaling](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2008rs004052)]

The anchor: **AST's ~223 m^2 array forms ~2,500 beams** ([arXiv 2506.18672](https://arxiv.org/html/2506.18672v1), confirmed). Scaling to a flat ~20-24 m^2 array by aperture ratio:

| Scaling assumption | Flat-array beams (from 2,500 at 223 m^2) | Tag |
|---|---|---|
| Linear in area (beams proportional to A): 20-24 / 223 x 2,500 | **~224-269** | [DERIVED, linear-in-area] |
| At fixed cell SIZE (more conservative; smaller array -> wider beams -> fewer cells AND bigger cells): area ratio applied to count | **~200-270** | [DERIVED] |
| If the flat array holds a SMALLER cell goal (denser beams): up to | **~400-450** | [DERIVED, optimistic] |

**Working band: ~200-450 beams for a flat ~20-24 m^2 array, with ~250 as the central linear-in-area figure. This is the SOFTEST input in the chain and is UNKNOWN-grade**, because (a) AST's 2,500 is for a 10x-larger aperture at a specific altitude/band, (b) Rocket Lab has published no Flatellite beam count (COMM-270), and (c) the beam count also depends on the digital-beamforming processor, which is unpublished for a flat entrant. Starlink's V2-mini D2C ~25 m^2-class array forming **48 beams** is the relevant LOW anchor (a flying ~25 m^2 D2C array), which suggests the linear-in-area ~250 may be optimistic and the true count could be nearer the low-hundreds or even below; the spread from ~48 (Starlink flying) to ~250 (AST-scaled) is the honest uncertainty. [DERIVED + UNKNOWN; the single load-bearing soft input]

> **Flag.** The 48-beam Starlink V2-mini D2C anchor and the ~250 AST-scaled figure differ by ~5x for similar apertures, because AST's 2,500 beams ride a much larger digital processor and a giant aperture, while Starlink's 48 is a deliberately modest D2C payload. A flat ~20-24 m^2 entrant array is bounded by these: plausibly ~50-250 beams in practice, ~200-450 if it carries an AST-class beamforming processor. The Section-2.3 capacity range carries this spread.

### 2.2 C_cell: per-cell capacity on ~25 MHz

Per-cell capacity = owned bandwidth x spectral efficiency. The corpus's spectral-efficiency anchors for a phone-to-LEO link:
- AST commercial baseline: **~3 bps/Hz** (120 Mbps / 40 MHz) [FACT, [arXiv 2506.18672](https://arxiv.org/html/2506.18672v1)].
- Starlink measured (SMS phase, ~0 dB median SINR): **~0.52-0.61 bps/Hz** [FACT, [arXiv 2506.00283](https://arxiv.org/html/2506.00283v8)], which rises toward 1-3 bps/Hz for a data-grade link with better SINR and owned (cleaner) spectrum.
- 4G LTE reference: **~1.5 bps/Hz** average [FACT, COMM-114].

**Working: ~2-3 bps/Hz for a data-grade DTC link on owned, cleaner mid-band spectrum.** On ~25 MHz:

| Spectral efficiency | C_cell = 25 MHz x SE | Tag |
|---|---|---|
| 2 bps/Hz (conservative) | **50 Mbps/cell** | [DERIVED] |
| 2.5 bps/Hz (mid) | **62.5 Mbps/cell** | [DERIVED] |
| 3 bps/Hz (AST-class) | **75 Mbps/cell** | [DERIVED] |

So **~50-75 Mbps per cell on ~25 MHz**, consistent with the per-phone doc (one phone alone in a cell sees this as its peak, COMM-344). [DERIVED]

### 2.3 The total: beams x per-cell x reuse, the optimistic and realistic bands

**Optimistic (raw beam-times-cell product, ignoring the spectrum cap):**

| | Low (200 beams, 50 Mbps) | Central (250 beams, 62.5 Mbps) | High (450 beams, 75 Mbps) |
|---|---|---|---|
| Raw product | **~10 Gbps** | **~15.6 Gbps** | **~33.8 Gbps** |

But the raw product DOUBLE-COUNTS the spectrum: it pretends every beam has its own independent 25 MHz, when in fact all beams share the SAME owned 25 MHz and only NON-OVERLAPPING beams reuse it simultaneously. The realistic total applies the spatial-reuse fraction (Section 3) and the spectrum cap.

**Realistic (spectrum-and-reuse-bound):**

The hard cap over the satellite's footprint is C_spectrum = 25 MHz x SE x N_reuse_max, where N_reuse_max is how many non-overlapping beams tile the footprint. For a flat ~20-24 m^2 array at low orbit, the footprint tiles into the ~200-450 beams, but only a fraction can be lit on the SAME 25 MHz at once without co-channel interference (typical satellite reuse factors are ~3-4 to ~20x depending on isolation, COMM-rf_limited_service). Taking a spatial-reuse fraction of ~30-60% of beams simultaneously co-channel (the rest on guard-separation or time-shared):

| | Low | Central | High | Tag |
|---|---|---|---|---|
| Realistic per-satellite total | **~5 Gbps** | **~8-10 Gbps** | **~15 Gbps** | [DERIVED] |

**Headline: a flat ~20-24 m^2 array on ~25 MHz produces ~5-15 Gbps of total per-satellite DTC throughput, central ~8-10 Gbps.** This sits sensibly between Starlink V2-mini D2C ~7 Gbps (thinner spectrum, same aperture class) and far below AST Block 2 ~56 Gbps (10x aperture, 8x spectrum, 10x beams). The ~700 Gbps V3 D2C projection is on a dedicated 15,000-sat fleet with much more spectrum and a far larger processor and is NOT a flat-entrant anchor. [DERIVED, bracketed by both flying anchors]

### 2.4 Why the SPECTRUM binds, not the processor (the cap that matters)

AST's processor is **~10 GHz of processing bandwidth, realizing ~56 Gbps** across 2,800 cells (COMM-141/142). That processor cap is ~56 Gbps. A flat entrant's processor is unpublished (COMM-270) but a smaller flat array would carry a smaller processor. The decisive point: **on ~25 MHz of owned spectrum, the SPECTRUM caps the total far below any plausible processor.** 25 MHz x 3 bps/Hz x even ~50x reuse = ~3.75 Gbps from a single 25 MHz slice reused 50 times; to reach ~10-15 Gbps total you already need ~130-200x effective reuse, which is at the high end of what beam isolation allows. The onboard processor (the ~10 GHz / ~56 Gbps AST anchor the prompt flagged) is therefore NOT the binding cap for a thin-spectrum flat satellite; the **~25 MHz of owned spectrum is**, exactly as the corpus's spectrum-gate finding predicts (COMM-325). AST's own analysis says the same on the supply side: AST "already operate near the practical limits of antenna size and radiated power," so "expanded bandwidth is the most viable path to increased D2D throughput" [FACT, [arXiv 2506.18672](https://arxiv.org/html/2506.18672v1)]. More spectrum, not a bigger processor or more satellites, is the lever that raises per-satellite total. [DERIVED + FACT]

---

## 3. The spectrum-saturation ceiling (where more satellites stop raising per-user speed)

This is the founder's load-bearing point: "past some point more satellites stop helping speed." That point is the SPECTRUM-SATURATION CEILING, and it is set by per-satellite capacity and the fixed ~25 MHz, not by satellite count.

### 3.1 The ceiling, stated as a formula

Over a FIXED ground area A_ground on a FIXED owned bandwidth B_owned:

```
Max deliverable area capacity  =  B_owned  x  SE  x  N_reuse(A_ground)        [bits/s over A_ground]

  N_reuse(A_ground) = number of NON-OVERLAPPING co-channel beams that tile A_ground
                    = A_ground / A_beam        (footprint area / per-beam footprint area)
```

N_reuse is set by the BEAM FOOTPRINT (aperture and altitude), NOT by satellite count. Once every patch of A_ground is covered by one beam on B_owned, the area capacity has hit B_owned x SE x (A_ground / A_beam). **Adding more satellites over the SAME area does not raise this**, because their beams cover ground that is already covered, on the same 25 MHz, so they ADD CO-CHANNEL INTERFERENCE rather than capacity. [DERIVED, from the corpus reuse framework COMM-224 + the multi-source interference finding below]

### 3.2 The mechanism, multi-source (why overlapping beams stop adding capacity)

The interference-limited ceiling is well-attested across independent sources:
- **Full frequency reuse "leads to severe inter-beam co-channel interference and consequently degrades the SINR at the receiver, thereby limiting system performance"** [FACT, [IEEE Xplore 10816533, multibeam LEO beam-size optimization](https://ieeexplore.ieee.org/document/10816533/), [MDPI Electronics multibeam LEO](https://www.mdpi.com/2079-9292/13/6/1096)].
- **"Overlaps of multiple co-channel beams can reduce the communication capacity of satellites,"** and "co-frequency interference may increase upon increasing the number of satellites" [FACT, [arXiv 2501.02750 spectrum sharing satellite-terrestrial](https://arxiv.org/html/2501.02750v3), [arXiv 2310.15011 interference management](https://arxiv.org/html/2310.15011)].
- The corpus already owns the upstream cause: **a beam is a fixed pool of capacity over a fixed footprint that cannot densify** (COMM-108, COMM-224); the only way to add capacity over busy ground is more NON-OVERLAPPING beams, which a fixed aperture/altitude cannot manufacture beyond the tiling limit. [FACT, COMM-224]

So the chain is: fixed 25 MHz -> fixed per-cell capacity -> fixed beam footprint -> a fixed number of non-overlapping beams tile the area -> **once that tiling is achieved, more satellites overlap and interfere, and per-user speed stops rising.** [DERIVED, mechanism multi-source]

### 3.3 Where the ceiling sits, quantified for ~25 MHz

The ceiling is reached at the satellite count where the constellation first achieves continuous single-beam coverage of the target on the 25 MHz (the coverage floor, COMM-215/224: ~130-450 satellites for US+Europe continuity, raised at VLEO). Beyond that:

- **Below the coverage floor (~few hundred satellites for US+Europe):** adding satellites buys COVERAGE / continuity (closing time-of-day gaps), and per-user speed in a covered cell is already at the per-cell-divided-by-users level. [FACT, COMM-224]
- **At the floor through a modest multiple of it:** adding satellites buys CAPACITY via MORE non-overlapping beams over busy ground (each satellite's beams tile a different patch), so area capacity and the number of users served at a target speed rise. [FACT, COMM-224]
- **Past the reuse limit (when beams over the SAME patch overlap on the same 25 MHz):** adding satellites STOPS raising per-user speed; the extra co-channel beams interfere, and the system is interference-limited. **This is the founder's "more satellites do not help" point.** [DERIVED + FACT, multi-source interference]

The exact satellite count at the ceiling depends on beam footprint (aperture/altitude) and the spatial-reuse factor, which for a flat-array entrant are UNKNOWN-grade (the beam count of Section 2.1). But the STRUCTURE is firm: **per-user speed is capped at (25 MHz x SE) / users_active regardless of satellite count, and satellite count only helps until every patch of the target is tiled by one non-overlapping beam on the 25 MHz; past that, the fixed spectrum is the wall.** The founder's instinct is correct: there is a saturation point, and it is set by the per-satellite capacity (beams x per-cell) and the fixed 25 MHz, not by adding airframes. [DERIVED]

### 3.4 The one thing that DOES raise the ceiling

The ceiling B_owned x SE x N_reuse moves only with: (a) MORE OWNED SPECTRUM (B_owned, linear and the strongest lever, the corpus's repeated finding and AST's own "expanded bandwidth is the most viable path"), (b) higher SPECTRAL EFFICIENCY (SE, bounded by the ~0 dB-SINR phone link, only ~2-4x headroom), or (c) MORE NON-OVERLAPPING BEAMS over the area via SMALLER beam footprints (tighter beams from a BIGGER aperture, or lower altitude shrinking the footprint, both of which add tiling slots, COMM-226). Critically, (c) via bigger aperture is the AST route (more beams per satellite), and via lower altitude is a weak help that also raises the coverage floor. **Adding satellites of the SAME aperture on the SAME spectrum over the SAME area is none of these and hits the ceiling.** [DERIVED, ties to COMM-320/325]

---

## 4. The speed-vs-users tradeoff (per-cell capacity / active users = sustained speed)

The third relationship the founder asked for: how sustained per-user speed depends on how many users share a cell, as a formula plus a worked example.

### 4.1 The formula

A cell is the ~25 MHz pool, time-shared by the scheduler across all ACTIVE users in the beam (the corpus's scheduler mechanism, COMM-340). So:

```
Sustained per-user speed  =  C_cell / users_active  =  (B_owned x SE) / users_active

  users_active = simultaneously-transmitting users in the beam (NOT all attached phones;
                 active = a fraction of attached, set by the concurrency/activity factor)
```

And the number of users a FLEET can serve at a TARGET speed over an area:

```
Users_at_target  =  N_beams_over_area  x  (C_cell / target_speed)
                  =  N_beams_over_area  x  users_per_beam_at_target
```

[DERIVED, from the corpus per-cell-pool / scheduler model COMM-336..340]

### 4.2 The worked example (on a ~50-75 Mbps cell)

Take C_cell = ~50-75 Mbps (25 MHz x 2-3 bps/Hz, Section 2.2):

| Active users in the cell | Sustained per-user speed (at 62.5 Mbps mid) | Tag |
|---|---|---|
| 1 (sole occupant, the per-phone PEAK) | **~62.5 Mbps** (the corpus's ~25-50 Mbps single-phone band sits here) | [DERIVED] |
| 2-3 | **~21-31 Mbps** (the founder's ~20-30 Mbps target band) | [DERIVED] |
| 5 | **~12.5 Mbps** | [DERIVED] |
| 10 | **~6.25 Mbps** | [DERIVED] |
| 50 | **~1.25 Mbps** | [DERIVED] |
| 125 | **~0.5 Mbps** (matches AST's published ~500 kbps/user at ~5% beam load) | [DERIVED, cross-checks AST] |

The ~500 kbps-at-125-users row matches AST's own published ~500 kbps/user rural figure ([arXiv 2506.18672](https://arxiv.org/html/2506.18672v1)), and the ~1 Mbps-at-50-users row matches the analyst busy-cell figure (Farrar, ~1 Mbps or less under load, COMM-339), so the formula is calibrated to both flying-system datapoints. [DERIVED, cross-checked]

### 4.3 What it takes to DELIVER ~20-30 Mbps sustained (the founder's target)

To hit **~20-30 Mbps sustained per user, the cell must hold active users to ~2-4** (62.5 Mbps / 25 Mbps = 2.5). The number of users served at that target across the fleet = (total beams over the area) x (~2-4 users/beam). Three consequences:

1. **The 20-30 Mbps headline is a lightly-loaded / scheduled-priority number, not a whole-population number.** A single ~324 km^2 beam over populated ground holds far more than 2-4 attached phones; it holds 2-4 ACTIVE at the target speed only because of low concurrency (most attached phones are idle at any instant). With a typical activity factor of ~0.5-2% (busy-hour cellular), a beam can hold ~100-800 attached users while keeping ~2-4 active, so ~20-30 Mbps is sustainable for a populated band ONLY at low concurrency, and degrades toward ~1 Mbps the moment concurrency spikes (an event, a crowd, an outage). [DERIVED, concurrency-dependent]
2. **To serve MORE users at the target, you need MORE BEAMS over the area**, which (Section 3) means more non-overlapping beams via bigger aperture or more spectrum, NOT more satellites of the same aperture on the same 25 MHz past the tiling limit. [DERIVED]
3. **The active-user density over a populated band is the binding UNKNOWN input.** The corpus has no grounded active-user-per-km^2 figure for a populated band; this is the gap that turns the formula into a fleet sizing (Section 6). The founder must set the assumed concurrency and populated-band active-user density (per the "ask the founder for assumptions" rule). [UNKNOWN, named gap]

### 4.4 The terrestrial benchmark check (why "cheaper" is the only door)

The founder benchmarks against terrestrial 5G (~170-180 Mbps, ~$80/mo) and accepts ~20-30 Mbps only if much cheaper. The supply side confirms WHY this is the only viable framing: the same ~25 MHz that one satellite beam spends ONCE over a ~324 km^2 footprint, terrestrial spends ~100+ times over via cell-splitting in that area (COMM-108), so satellite DTC area capacity is ~30x-to-thousands-x below terrestrial (COMM-114), and DTC delivery is ~$5-9/GB versus ~$0.30/GB terrestrial (COMM-direct_to_cell). **The satellite cannot win on speed or capacity over served ground; it can only win on COVERAGE (reaching phones nothing else reaches) and must price the ~20-30 Mbps far below terrestrial.** The supply ceiling is exactly why: a fixed 25 MHz over a huge beam cannot densify, so the product is a coverage layer at a low per-user speed, sold cheap, not a capacity competitor. [DERIVED, ties the supply side to the founder's benchmark]

---

## 5. So what (for the Neutron DTC supply model)

1. **Per-satellite total capacity for a flat ~20-24 m^2 array on ~25 MHz is ~5-15 Gbps (central ~8-10 Gbps)**, set by ~200-450 beams x ~50-75 Mbps/cell x spatial-reuse, bracketed by Starlink V2-mini D2C (~7 Gbps) and far below AST Block 2 (~56 Gbps, 10x aperture / 8x spectrum). The beam count is the softest input (~48 Starlink-flying to ~250 AST-scaled, ~200-450 with an AST-class processor). [DERIVED]
2. **The binding cap is the ~25 MHz of owned spectrum, NOT the onboard processor.** The ~10 GHz / ~56 Gbps AST processor anchor the prompt flagged is far above what 25 MHz can feed; the spectrum is the wall, exactly as AST's own "expanded bandwidth is the most viable path" states. More spectrum is the per-satellite-capacity lever. [DERIVED + FACT]
3. **The spectrum-saturation ceiling is real and the founder is right about it.** Over a fixed area on a fixed 25 MHz, per-user speed is capped at (25 MHz x SE) / users_active regardless of satellite count; satellites help only until every patch is tiled by one non-overlapping beam, then more satellites overlap and interfere (interference-limited), and per-user speed stops rising. The ceiling moves only with more spectrum, higher SE (limited), or smaller beams (bigger aperture / lower altitude), never with more same-aperture satellites past the tiling limit. [DERIVED + FACT, multi-source]
4. **The speed-vs-users tradeoff is per_user = (25 MHz x SE) / users_active**, calibrated to AST's ~500 kbps-at-125-users and the analyst ~1 Mbps-at-50-users. Hitting ~20-30 Mbps requires ~2-4 active users per cell, so the headline is a low-concurrency / lightly-loaded number; serving more users at the target needs more beams (bigger aperture or more spectrum), not more satellites. [DERIVED]
5. **The fewest-satellites-for-best-speed answer:** speed-to-one-(lightly-loaded)-phone is set by aperture + spectrum + altitude (the per-phone doc, ~25-50 Mbps), and adding satellites does NOT raise it; satellites buy COVERAGE up to the floor and CAPACITY (more users at the target) up to the reuse ceiling. So the fewest satellites that clear the coverage floor already deliver the best PER-USER speed the spectrum allows; beyond the reuse ceiling, more satellites add cost without speed. The founder's "fewest satellites, best speed, broadest coverage" optimum is the coverage-floor count (a few hundred for US+Europe), and the lever for MORE served users or higher speed is spectrum and aperture, not airframe count. [DERIVED, the synthesis answer]
6. **No verdict.** This doc establishes the supply-side capacity, the saturation ceiling, and the speed-vs-users tradeoff. Whether the business closes depends on the owned-spectrum position (~25 MHz here vs the ~100-200 MHz competitive benchmark, COMM-325), the populated-band active-user density (UNKNOWN, Section 6), the per-phone rate (the corpus), and the launch economics (the fit doc), none assessed here.

---

## 6. Open questions / named gaps

1. **The flat-array BEAM COUNT is the load-bearing soft input (UNKNOWN-grade).** Scaling AST's 2,500 beams at 223 m^2 to a flat ~20-24 m^2 array gives ~200-270 linear-in-area, but Starlink's flying ~25 m^2 D2C array forms only 48 beams, a ~5x spread driven by the size of the onboard digital-beamforming processor, which is unpublished for a flat entrant (COMM-270). The whole ~5-15 Gbps per-satellite total rides on this; it is the single number most worth pinning. [UNKNOWN]
2. **The populated-band ACTIVE-USER DENSITY (and concurrency factor) is unset.** The speed-vs-users formula needs active users per cell over a target band to become a fleet sizing; the corpus has no grounded figure. The founder must set the assumed concurrency (~0.5-2% busy-hour) and populated-band active-user density. [UNKNOWN, founder assumption]
3. **The spatial-reuse fraction (f_reuse) for a flat-array constellation is an estimate.** Satellite reuse factors span ~3-4 to ~20x by isolation; the ~30-60%-of-beams-co-channel assumption (Section 2.3) is a planning band, not a measured value for this aperture/altitude. [ESTIMATE]
4. **The exact satellite count at the saturation ceiling is geometry-dependent and UNKNOWN.** The STRUCTURE (per-user speed capped by spectrum past the tiling limit) is firm and multi-source; the precise count where overlap begins depends on the flat-array beam footprint, which depends on (1). [DERIVED structure; UNKNOWN count]
5. **Spectral efficiency on a wider/cleaner owned channel is an estimate.** The ~2-3 bps/Hz assumes the array and power hold that efficiency across 25 MHz at the phone link's ~0 dB SINR; the corpus flags this (COMM-348). Starlink's measured ~0.52 bps/Hz on SMS-grade spectrum is the low anchor; data-grade owned mid-band should do better, but the realized figure is not pinned. [ESTIMATE]
6. **Per-satellite capacity is anchored on revealed systems, not a closed-form beams-x-aperture-x-spectrum curve.** A first-principles joint curve would convert the ~5-15 Gbps band into a tighter number; it is not in the corpus. [DERIVED, empirical]

---

## Sources

Per-satellite capacity anchors (AST, Starlink V2/V3):
- [Spectrum Opportunities for the Wireless Future (arXiv 2506.18672): AST 2,500 adjustable beams, 40 MHz/beam, 20.3 km / 324 km^2 beam, 42 dBi, 3 bps/Hz, 120 Mbps/cell, 500 kbps/user rural, G = 4 pi eta A / lambda^2; AST near practical limits of antenna size and power so expanded bandwidth is the most viable path](https://arxiv.org/html/2506.18672v1)
- [AST SpaceMobile Block 2 BlueBirds Reach Orbit (TechTimes): AST5000 ASIC handling >2,000 coverage cells, up to 2,500 uplink beams](https://www.techtimes.com/articles/318740/20260620/ast-spacemobile-block-2-bluebirds-reach-orbit-satellite-broadband-direct-your-phone-nears.htm)
- [US FCC licences next-gen AST satellite test (Mobile World Live): Block 2 array, >2,000 coverage cells, beam-steering ASIC](https://www.mobileworldlive.com/ast-spacemobile/us-fcc-licences-next-gen-ast-satellite-test/)
- [SpaceX 15,000 V3 Starlink Direct-to-Cellphone Satellites (NextBigFuture): V3 D2C ~700 Gbps/sat, >100x V2 D2C (~7 Gbps), 15,000 sats, 326-335 km, ~2-100 Mbps/user beam-sharing-dependent, ~65 MHz / 2 GHz AWS-4 EchoStar](https://www.nextbigfuture.com/2025/09/spacex-15000-v3-starlink-direct-to-cellphone-satellites.html)
- [Direct-to-Cell: A First Look into Starlink's RAN through Crowdsourced Measurements (arXiv 2506.00283): ~3.1 Mbps/beam, ~0.52-0.61 bps/Hz, ~0 dB SINR, 2x5 MHz PCS G-block, ~18.6 Mbps aggregate at full holdings](https://arxiv.org/html/2506.00283v8)
- [Starlink capacity working paper (thexlab.org): V2-mini D2C ~48 beams x ~7 Mbps, ~7 Gbps aggregate, fronthaul-limited](https://thexlab.org/wp-content/uploads/2025/07/Starlink_Analysis_Working_Paper_v0.2.pdf)

Beam-count-vs-aperture scaling (phased-array physics):
- [Adaptive taper selection for beamforming (USPTO 12200508): aperture inversely related to beam angular size, ~2.4 m / >4,000 elements for 0.5 deg beams at 20 GHz](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12200508)
- [Antenna aperture size reduction in multiple spot beam cellular satellite systems (Kilic, Radio Science 2009): aperture-vs-spot-beam-count scaling](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2008rs004052)
- [From Cell Towers to Satellites: 2040 Blueprint for Urban-Grade D2D (arXiv 2507.14188): beam scheduling, time-division one-phone-per-resource-block, up to 2,500 uplink beams tracked](https://arxiv.org/pdf/2507.14188)

Spectrum-saturation / interference-limited ceiling (multi-source):
- [Optimizing Beam Size in Multibeam LEO Satellite Networks: Interbeam Interference, Doppler, Frequency Reuse (IEEE Xplore 10816533): full frequency reuse leads to severe inter-beam co-channel interference, degrades SINR, limits system performance](https://ieeexplore.ieee.org/document/10816533/)
- [Spectrum Sharing in Satellite-Terrestrial Integrated Networks (arXiv 2501.02750): overlaps of multiple co-channel beams reduce satellite capacity; co-frequency interference increases with more satellites](https://arxiv.org/html/2501.02750v3)
- [Interference Management by Harnessing Multi-Domain Resources in Spectrum-Sharing Satellite-Ground Networks (arXiv 2310.15011): overlapping co-channel beams in dense constellations as a fundamental capacity limit](https://arxiv.org/html/2310.15011)
- [Interference Situational Aware Beam Pointing Optimization for Dense LEO (MDPI Electronics 13/6/1096): interference-limited vs noise-limited regimes by elevation/shadowing; aggressive reuse causes inter-beam interference](https://www.mdpi.com/2079-9292/13/6/1096)
- *(The beam-is-a-fixed-pool-that-cannot-densify framework, the coverage-vs-capacity regime split, the ~3 bps/Hz / 0.52 bps/Hz / 1.5 bps/Hz efficiency anchors, the ~56 Gbps AST processor cap, the ~$5-9/GB cost floor, and the ~25 MHz owned-spectrum cost are cross-referenced from [`spectrum_generations_and_availability.md`](spectrum_generations_and_availability.md), [`leo_constellation_coverage_minimums.md`](leo_constellation_coverage_minimums.md), [`economics/comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md), [`dtc_system_model.md`](dtc_system_model.md), and [`spectrum_purchase_and_6g.md`](spectrum_purchase_and_6g.md); not re-listed.)*

---

## Claims ledger (COMM-406..425)

For the catalog/reconciliation step to ingest. Each hard claim with sources and tag; single-source and projection claims flagged. IDs COMM-406 through COMM-425 reserved for this doc (not exceeded). Cross-references existing IDs heavily.

- **COMM-406**, Per-satellite total DTC capacity = N_beams x C_cell x f_reuse, bounded above by min(C_spectrum, C_processor), where C_cell = owned bandwidth x spectral efficiency (Shannon) and C_spectrum = owned bandwidth x SE x the number of non-overlapping reuse beams over the footprint; this is the supply-side identity assembled from the corpus's Shannon-x-beams framework. [DERIVED, framework] Grounds in COMM-108, COMM-224, COMM-114, COMM-344, COMM-141/142.
- **COMM-407**, The number of simultaneous beams a phased array forms scales with aperture area / element count (aperture is inversely related to beam angular size, and independent-beam count tracks element count); AST's ~223 m^2 array forms ~2,500 beams. [FACT, phased-array physics] Sources: USPTO 12200508 (aperture-vs-beam-angle, >4,000 elements for 0.5 deg at 20 GHz); Kilic Radio Science 2009; arXiv 2506.18672 (AST 2,500 beams).
- **COMM-408**, A flat ~20-24 m^2 array forms an estimated ~200-450 beams (central ~250 by linear-in-area scaling from AST's 2,500 at 223 m^2), but Starlink's flying ~25 m^2-class D2C array forms only 48 beams, a ~5x spread driven by the unpublished onboard digital-beamforming processor size; this is the SOFTEST, UNKNOWN-grade input in the chain. [DERIVED + UNKNOWN] Sources: arXiv 2506.18672 (AST 2,500); thexlab.org (Starlink 48); Flatellite beam count unpublished (cross-ref COMM-270).
- **COMM-409**, Per-cell capacity on ~25 MHz of owned spectrum is ~50-75 Mbps (25 MHz x ~2-3 bps/Hz), using the corpus's data-grade DTC spectral-efficiency band (AST ~3 bps/Hz; Starlink measured ~0.52-0.61 bps/Hz at ~0 dB SINR; 4G ~1.5 bps/Hz). [DERIVED] Sources: arXiv 2506.18672 (AST 3 bps/Hz / 120 Mbps on 40 MHz); arXiv 2506.00283 (Starlink 0.52-0.61); cross-ref COMM-114, COMM-344.
- **COMM-410**, A flat ~20-24 m^2 array on ~25 MHz produces ~5-15 Gbps total per-satellite DTC throughput (central ~8-10 Gbps), the realistic spectrum-and-reuse-bound figure; the raw beam-times-cell product (~10-34 Gbps) is the optimistic bound that double-counts the shared spectrum. This brackets Starlink V2-mini D2C (~7 Gbps) and sits far below AST Block 2 (~56 Gbps, 10x aperture, 8x spectrum). [DERIVED] Sources: this doc Section 2.3; anchors COMM-142 (AST 56 Gbps), thexlab.org / NextBigFuture (Starlink 7 Gbps).
- **COMM-411**, On ~25 MHz of owned spectrum the binding cap is the SPECTRUM, not the onboard processor: 25 MHz x 3 bps/Hz x even ~50x reuse is ~3.75 Gbps from one slice, so reaching ~10-15 Gbps needs ~130-200x effective reuse, while the AST processor cap is ~10 GHz processing / ~56 Gbps, far above what 25 MHz can feed; AST's own analysis says it operates near the practical limits of antenna size and power so expanded bandwidth is the most viable path to more throughput. [DERIVED + FACT] Sources: arXiv 2506.18672 (AST near practical limits, expanded bandwidth the path); COMM-141/142 (processor cap); cross-ref COMM-325 (spectrum gate).
- **COMM-412**, V2-mini D2C ~7 Gbps aggregate (48 beams x ~7 Mbps, fronthaul-limited) and AST Block 2 ~56 Gbps theoretical (2,800 cells x 20 Mbps, 10 GHz processing) are the lower and upper per-satellite anchors; the V3 D2C ~700 Gbps projection is a dedicated-15,000-sat-fleet projection with much more spectrum and processor, NOT a flat-entrant anchor. [FACT lower/upper anchors; ESTIMATE/projection for 700 Gbps] Sources: thexlab.org, NextBigFuture (V2 7 Gbps, V3 700 Gbps projection); COMM-142 (AST 56 Gbps).
- **COMM-413**, THE SPECTRUM-SATURATION CEILING (formula): over a fixed ground area on a fixed owned bandwidth, max area capacity = B_owned x SE x N_reuse, where N_reuse = A_ground / A_beam is the number of NON-OVERLAPPING co-channel beams that tile the area, set by beam footprint (aperture/altitude), NOT by satellite count. [DERIVED] Grounds in COMM-224 (beam cannot densify), COMM-108.
- **COMM-414**, THE SATURATION MECHANISM (multi-source): once every patch of the target is covered by one beam on the owned spectrum, adding more satellites over the SAME area adds OVERLAPPING co-channel beams that interfere rather than add capacity, so per-user speed stops rising (interference-limited): full frequency reuse "leads to severe inter-beam co-channel interference and degrades the SINR, limiting system performance," and "overlaps of multiple co-channel beams can reduce the communication capacity," with co-frequency interference increasing as more satellites are added. [FACT, multi-source] Sources: IEEE Xplore 10816533; arXiv 2501.02750; arXiv 2310.15011; MDPI Electronics 13/6/1096; cross-ref COMM-224.
- **COMM-415**, This is the founder's "past some point more satellites stop helping speed" point, and it is correct: per-user speed is capped at (B_owned x SE) / users_active regardless of satellite count; satellite count helps only until the target is tiled by one non-overlapping beam on the owned spectrum (the coverage floor, ~130-450 sats for US+Europe), and past the reuse limit more same-aperture satellites add cost without raising per-user speed. [DERIVED + FACT] Sources: this doc Section 3.3; COMM-215/224 (coverage floor), COMM-414 (interference).
- **COMM-416**, The saturation ceiling moves ONLY with (a) more owned spectrum (linear, the strongest lever and AST's stated path), (b) higher spectral efficiency (bounded by the ~0 dB-SINR phone link, ~2-4x headroom), or (c) more non-overlapping beams via smaller footprints (bigger aperture or lower altitude, which adds tiling slots); adding satellites of the SAME aperture on the SAME spectrum over the SAME area is none of these and hits the ceiling. [DERIVED] Grounds in COMM-320, COMM-325, COMM-226, COMM-411.
- **COMM-417**, THE SPEED-vs-USERS FORMULA: sustained per-user speed = C_cell / users_active = (B_owned x SE) / users_active, where users_active is the simultaneously-transmitting users in the beam (a concurrency fraction of attached phones), because the cell's spectrum pool is time-shared by the scheduler across active users. [DERIVED] Grounds in COMM-336..340 (per-cell pool / scheduler).
- **COMM-418**, Worked speed-vs-users on a ~50-75 Mbps cell (25 MHz x 2-3 bps/Hz): 1 active user ~62.5 Mbps (the single-phone peak band), 2-3 ~21-31 Mbps (the founder's ~20-30 Mbps target), 5 ~12.5 Mbps, 10 ~6.25 Mbps, 50 ~1.25 Mbps, 125 ~0.5 Mbps; the 125-user / ~500 kbps row matches AST's published ~500 kbps/user rural figure and the 50-user / ~1 Mbps row matches the analyst busy-cell figure, calibrating the formula to both flying datapoints. [DERIVED, cross-checked] Sources: arXiv 2506.18672 (AST 500 kbps/user); cross-ref COMM-339 (Farrar ~1 Mbps under load).
- **COMM-419**, To DELIVER ~20-30 Mbps sustained per user the cell must hold active users to ~2-4 (62.5 / 25 = 2.5); the number of users served at the target across a fleet = (total non-overlapping beams over the area) x (~2-4 users/beam). So the ~20-30 Mbps headline is a low-concurrency / lightly-loaded number, and serving more users at the target requires MORE BEAMS (bigger aperture or more spectrum), not more satellites past the tiling limit. [DERIVED] Sources: this doc Section 4.3; COMM-417, COMM-416.
- **COMM-420**, A ~324 km^2 beam over populated ground holds far more than 2-4 ATTACHED phones; it holds ~2-4 ACTIVE (the ~20-30 Mbps condition) only at low concurrency (~0.5-2% busy-hour activity factor), so it can carry ~100-800 attached users while keeping ~2-4 active, and the ~20-30 Mbps degrades toward ~1 Mbps when concurrency spikes (event/crowd/outage). [DERIVED, concurrency-dependent] Grounds in COMM-417, COMM-418, arXiv 2506.18672 (324 km^2 beam).
- **COMM-421**, The populated-band ACTIVE-USER DENSITY and concurrency factor are an UNKNOWN, named gap: the corpus has no grounded active-users-per-km^2 for a target band, which is the input that turns the speed-vs-users formula into a fleet sizing; the founder must set the assumed concurrency and active-user density. [UNKNOWN, founder assumption] Source: this doc Section 4.3 / Section 6.
- **COMM-422**, The supply ceiling confirms WHY the founder's "much cheaper" framing is the only door: the same 25 MHz a satellite beam spends once over ~324 km^2 is spent ~100+ times by terrestrial cell-splitting in that area, so DTC area capacity is ~30x-to-thousands-x below terrestrial and DTC delivery is ~$5-9/GB vs ~$0.30/GB terrestrial; the satellite wins only on COVERAGE (reaching phones nothing else reaches) and must price ~20-30 Mbps far below terrestrial's ~170-180 Mbps / ~$80/mo. [DERIVED] Grounds in COMM-108, COMM-114, COMM-direct_to_cell ($5-9/GB).
- **COMM-423**, The fewest-satellites-for-best-speed answer: speed to one lightly-loaded phone is set by aperture + owned spectrum + altitude (the per-phone doc ~25-50 Mbps) and is NOT raised by adding satellites; satellites buy coverage up to the floor and capacity (more users at the target) up to the reuse ceiling, so the fewest satellites that clear the coverage floor (a few hundred for US+Europe) already deliver the best per-user speed the spectrum allows, and the lever for more served users or higher speed is spectrum and aperture, not airframe count. [DERIVED, synthesis answer] Grounds in COMM-361 (per-phone rate), COMM-415, COMM-419, COMM-215/224.
- **COMM-424**, The spatial-reuse fraction (f_reuse) for a flat-array constellation is an ESTIMATE: satellite reuse factors span ~3-4 to ~20x by isolation, and the ~30-60%-of-beams-co-channel assumption is a planning band, not a measured value for this aperture/altitude; it is one of the swing inputs on the ~5-15 Gbps per-satellite total. [ESTIMATE] Sources: this doc Section 2.3; cross-ref rf_limited_service (HTS reuse up to ~20x).
- **COMM-425**, Net supply-side picture for a Neutron DTC business: a flat ~20-24 m^2 array on ~25 MHz produces ~5-15 Gbps/sat (spectrum-bound, not processor-bound); the spectrum-saturation ceiling caps per-user speed at (25 MHz x SE) / users_active regardless of satellite count, so more same-aperture satellites stop raising speed past the tiling limit; ~20-30 Mbps sustained needs ~2-4 active users/cell (a low-concurrency headline); and the levers that raise the ceiling are owned spectrum and aperture, not airframe count. The ~25 MHz here is well below the ~100-200 MHz competitive spectrum benchmark, the binding constraint on the whole supply side. No verdict. [DERIVED/SYNTHESIS] Grounds in COMM-410, COMM-413, COMM-415, COMM-419, COMM-325.

---

*COMM-406..425 created by this doc (the reserved block, not exceeded). Catalog rows for LIBRARY.md / RESEARCH_TRACKER.md / SOURCE_INDEX.md are returned to the catalog/reconciliation agent, not edited here. This doc is not committed by this pass.*
