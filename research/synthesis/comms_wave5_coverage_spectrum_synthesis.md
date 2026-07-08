# Communications Wave 5: Coverage Floor, Spectrum Incorporation, and the Cost of Spectrum, for the Coverage-First Model

*Research date: June 2026. Communications research-wiki effort, wave 5 (shared library).*

**Builds on / does not duplicate:** this is the wave-5 SYNTHESIS doc. Its job is to take the four wave-5 source docs and assemble them into the inputs the COVERAGE-FIRST broadband model needs: the minimum satellite count for coverage, the spectrum each generation actually carries, how the hardware folds to fit a launcher, and what spectrum costs to buy. It does NOT re-derive the inputs; every number is carried from a source doc cited by path. The four load-bearing inputs are:

- The coverage floor: [`leo_constellation_coverage_minimums.md`](../direct_communication/leo_constellation_coverage_minimums.md) (the streets-of-coverage floor for continuous 24/7 coverage, validated against Iridium 66, and the coverage-vs-capacity regime distinction).
- The spectrum incorporation: [`starlink_v3_v4_spectrum_incorporation.md`](../competitors/starlink_v3_v4_spectrum_incorporation.md) (the band-by-band MHz/GHz inventory and the bandwidth-to-capacity link in a real platform).
- The fold geometry: [`large_array_folding_and_stow.md`](../competitors/large_array_folding_and_stow.md) (the V3-vs-direct-to-cell fold ratio and the launch-fit asymmetry).
- The spectrum economics: [`spectrum_purchase_and_6g.md`](../direct_communication/spectrum_purchase_and_6g.md) (how much MHz, the secondary-market price per MHz-POP, the US+Europe total dollars, and the 6G/FR3 access question).

> **Reading guide.** Every hard number is tagged **[FACT]** (sourced to 2+ independent bodies), **[FACT, single-source]** (one source only), **[ESTIMATE]** (third-party model or sizing), or **[DERIVED]** (this doc's own arithmetic on cited inputs, or a source doc's closed-form derivation). Sources are inline; the underlying citations live in the source docs and in [`SOURCE_INDEX.md`](../SOURCE_INDEX.md) (COMM-178..248). China is **excluded** from every market total.

> **Scope and status.** This doc is ISOLATED TO COMMUNICATIONS and renders **NO verdict**. It assembles the wave-5 numbers in the slots the coverage-first model needs and flags the biggest still-unresolved numbers. The model design itself lives in the working briefs under `.agent/other/comms_model_design/` ([`DESIGN.md`](../../.agent/other/comms_model_design/DESIGN.md), [`SPECTRUM_spec.md`](../../.agent/other/comms_model_design/SPECTRUM_spec.md)); this doc is the sourced, citable backing for the numbers those briefs previously asserted chat-only.

---

## 0. The wave in one page

The wave-5 question was set by the coverage-first model: a Neutron-launched constellation covers a target region (US plus Europe), then serves whatever fraction of the covered population its purchased bandwidth allows. That model needs four numbers it did not have cold:

1. **How many satellites does coverage take?** The continuous-coverage FLOOR for US plus Europe is **~130-450 satellites** [DERIVED], a few hundred, not tens and not tens-of-thousands. Coverage is cheap.
2. **What spectrum does a real constellation incorporate, and is bandwidth the differentiator?** A V3 incorporates a **fixed ~2 GHz Ku user-downlink** (8 x 250 MHz, identical V1/V2/V3) [FACT]; the per-generation capacity leap is beams x spatial-reuse x wide backhaul, **not** a new user band. User bandwidth is NOT the differentiator.
3. **Does the hardware fold to fit Neutron?** A V3 broadband aperture **barely folds (fold ratio ~1x)** and is mass-bound [DERIVED]; a direct-to-cell array folds many times and is size-bound. Broadband is the geometry-favored Neutron comms play.
4. **What does spectrum cost?** The secondary market trades mid-band at **~$0.65-1.03 per MHz-POP** [DERIVED], so a US+Europe footprint costs **~$32-46B for 100 MHz** and **~$65-90B for 200 MHz**, spectrum-only [DERIVED].

The headline for the model: **coverage is cheap (a few-hundred-satellite problem) and the real economic line is spectrum, not the satellite count.** Whether that spectrum line enters the model at all depends on the access mechanism (the SCS lease nets it to a wash; owned spectrum makes it a real tens-of-billions capital line). That choice is now a sourced, quantified fork rather than a hand-wave.

---

## 1. The Confirmed Numbers

### 1.1 The coverage floor: a few hundred satellites for US plus Europe

A single LEO satellite covers a **~1,300-1,900 km** circle (~1,880 km diameter at 550 km / 25 deg mask; ~1,290 km at 350 km / 25 deg) [FACT, closed-form, COMM-209] and is overhead a fixed point only **~2-8 minutes per pass** (~2.9 min at 350 km/25 deg to ~7.9 min at 550 km/10 deg) [FACT, closed-form, COMM-211]. So one satellite gives single-digit-percent daily contact, and continuity is bought with a string of satellites per orbital plane and enough planes to tile the target's longitude span (the streets-of-coverage construction) [FACT, COMM-212].

The continuous single-coverage floors (streets-of-coverage, slightly conservative vs an optimized Walker, validated against Iridium's real 66) [DERIVED, COMM-213..216]:

| Target | Continuous-coverage floor (single, 24/7) |
|---|---|
| Continental US (~58 deg lon span) | ~50-150 satellites (low tens optimized) |
| **US + Western Europe (~150 deg lon span)** | **~130-450 satellites** |
| Near-global mid-latitude band (all longitudes) | ~290-960 satellites |

*Vintage: June 2026, streets-of-coverage, ex-China. All counts are order-of-magnitude brackets, not buildable specs.*

The floor is altitude- and elevation-driven: lowering 550 to 350 km OR raising the mask 10 to 25 degrees each roughly **doubles-to-triples** the floor [FACT, COMM-217]. The model's validation anchor is Iridium: the SOC model gives ~84 for Iridium's config against the actual **66** flown [FACT, COMM-219], so the SOC method runs ~20-30% high versus an optimized Walker, which is why the floors above are read as ranges [DERIVED, COMM-213].

### 1.2 The coverage-vs-capacity regime distinction (the founder hypothesis, confirmed)

The load-bearing framework finding: coverage and capacity are distinct regimes [DERIVED, COMM-224]. Below the floor, added satellites buy **continuity** (a geometry problem). Above it, added satellites over the same area buy **capacity** (beams, spectrum reuse, a Shannon problem). The founder's hypothesis ("adding satellites buys coverage up to a floor, then capacity beyond it") is **CORRECT as a conceptual ordering** [DERIVED, COMM-227], with one sharpening: real systems overshoot the floor for capacity, and VLEO raises the floor itself (smaller footprints need more satellites for continuity), so the regimes are altitude-coupled, not cleanly sequential, and a flown system's count is set overwhelmingly by capacity. This is why Starlink Shell 1 is **1,584** satellites at 550 km [FACT, COMM-220] and Gen2 VLEO is ~30,000, both far above any continuity floor [DERIVED, COMM-226].

So a continuity-only US+Europe service is a **few-hundred-satellite problem** (~130-450), distinct from the **~1,584-to-30,000-satellite capacity build** [DERIVED, COMM-228].

### 1.3 V3/V4 spectrum incorporation: the user link is fixed and modest

The broadband user link is fixed and modest, identical across generations [FACT, COMM-178, COMM-179]:

| Link | Spectrum incorporated | Structure |
|---|---|---|
| User downlink | ~2 GHz Ku (10.7-12.7 GHz) | 8 x 250 MHz, same V1/V2/V3 |
| User uplink | ~500 MHz Ku (~14.0-14.5 GHz) | 8 x 62.5 MHz, ~75/25 split |

The capacity-relevant spectrum is in the backhaul, not the user link: Ka gateway/feeder ~1-2.5 GHz each way [ESTIMATE, COMM-180], an **E-band backhaul of 10 GHz total** (71-76 / 81-86 GHz, FCC-approved 2023, SpaceX-stated ~4x capacity per satellite) [FACT, COMM-181], plus V-band and W-band Gen2 authority [FACT, COMM-182; ESTIMATE, COMM-183]. The whole system incorporates **>20 GHz of licensed RF** (Ka+E+V) plus license-free optical inter-satellite links [FACT, COMM-184].

There is **no disclosed "V4" spectrum generation** as of June 2026 [UNKNOWN, COMM-190]: the forward story is V3 plus Gen2 multi-band upgrade authority, not a new branded band plan.

### 1.4 The fold ratio: V3 ~1x, direct-to-cell many folds

A Starlink V3 broadband aperture IS the flat satellite body (~7-8 m x ~3.5 m); the ~60 m "wingspan" is solar-wing-dominated, not RF aperture [DERIVED, COMM-197]. Its deployed-to-stowed **fold ratio is ~1x** (flat-pack / dense-stack, ~60/Starship), so V3 is **MASS-bound, fairing-agnostic** [DERIVED, COMM-198]. "Fold it twice" is roughly right for V3.

A direct-to-cell array is the opposite. AST's BlueBird Block 2 ~223 m2 aperture [FACT, COMM-202] is ~220-265 modular ~0.84 m2 "Micron" tiles [FACT, COMM-200] folding "phone booth" stowed to "studio apartment" deployed, dozens of fold lines, not two [ESTIMATE, COMM-203], so it is **SIZE-bound** and the fold geometry is what fills the fairing. The revealed evidence: 3 Block 2 fit on Falcon 9 (5.2 m fairing) but only 1 on New Glenn (7 m) / 1 on LVM3 (5.0 m), so the count is set by fairing size [FACT, COMM-205]. The general rule: a solar membrane stows to ~0.01% of deployed volume but a populated RF phased array packs only to ~34-48% [FACT, COMM-207], so a handset-closing aperture cannot fold like a solar wing. This is the mechanical root of the V3-vs-direct-to-cell launch-fit asymmetry [DERIVED, COMM-208], and it is why broadband (mass-bound, flat-stacking) is the geometry-favored Neutron comms play.

### 1.5 The spectrum to buy: ~$32-46B (100 MHz) to ~$65-90B (200 MHz), US+Europe

How much spectrum an operator must hold: GSMA benchmark **80-100 MHz mid-band per operator** to launch competitive 5G [FACT, COMM-229]; US carriers actually hold ~280-375 MHz each [FACT, COMM-233..235]. Working dials: **~100 MHz floor, ~200 MHz to match an incumbent** [DERIVED, COMM-236].

What it costs (the number that answers the prior spectrum doc's open question): the secondary market trades mid-band at **~$0.65-1.03 per MHz-POP** [DERIVED, COMM-241], from the AT&T-UScellular deal (~$0.65) [DERIVED, COMM-238] and the SpaceX-EchoStar deal (~$1.03) [ESTIMATE, COMM-240], the same range as primary auctions with no entrant discount. Across the US (~342M POP) [FACT, COMM-243] plus Europe (~518M POP) [FACT, COMM-244]:

| Holding | US+Europe spectrum cost, spectrum-only |
|---|---|
| 100 MHz (competitive floor) | **~$32-46B** [DERIVED, COMM-245] |
| 200 MHz (incumbent match) | **~$65-90B** [DERIVED, COMM-246] |

*Vintage: June 2026, secondary-market $/MHz-POP, flat-rate order-of-magnitude anchors, ex-China.*

This is consistent with the SpaceX-EchoStar **~$17B for ~65 MHz** owned D2C block [FACT, COMM-187] (the per-MHz-POP price of which is exactly the ~$1.03 high end). For disambiguation: the "~115 MHz" often quoted is the full FCC transaction; SpaceX got ~65 MHz, AT&T got ~50 MHz [FACT, COMM-188].

---

## 2. The Biggest Still-Unresolved Numbers

The wave-5 set is geometry- and deal-grounded, but four numbers remain open and should travel as ranges, not specs:

1. **A buildable US+Europe Walker, not just the floor bracket.** The ~130-450 floor is a streets-of-coverage RANGE that runs ~20-30% high versus an optimized Walker [DERIVED, COMM-213], depends on the European longitude scope, and is single-fold; 2-fold continuous (handover/diversity) costs ~2-4x the single floor [ESTIMATE, COMM-225]. An optimized Walker with a stated altitude, elevation mask, and coverage multiplicity would convert the bracket into a buildable count.

2. **The owned-spectrum line versus the SCS-lease wash.** The model's spectrum REQUIREMENT is one ~40 MHz block reused across all beams at near-zero capex under the FCC SCS lease, a wash in the cost comparison by construction (see `SPECTRUM_spec.md`). But if the model instead assumes OWNED spectrum, the ~$32-90B above becomes a real capital line. Which mechanism the coverage-first model assumes is a founder call that swings whether spectrum enters the cost stack at all.

3. **The V3 beam count, fold-line counts, and Block 2 folded dimensions.** The ~2 GHz-to-~1 Tbps decomposition is DERIVED because SpaceX has not disclosed the V3 beam count [DERIVED, COMM-189], and the V3 and AST Block 2 fold-line counts plus the Block 2 folded dimensions in meters are genuinely UNPUBLISHED [UNKNOWN, COMM-199, COMM-206]. Every fold-count and spatial-reuse statement is inferred.

4. **Whether a satellite NTN entrant can ever touch 6G/FR3.** FR3 (7.125-8.4 GHz golden band, plus 4.4-4.8 and 14.8-15.35 GHz) is terrestrial greenfield, not yet allocated/auctioned/held, auctions ~2028-2032+ [ESTIMATE, COMM-247]; the wave-5 read is that a satellite entrant should not count on accessing it (LEO-to-handset physics hostile, satellite role limited to incumbent FSS coexistence) [COMM-248], but this is a trajectory direction, not a settled fact (WRC-27 has not concluded). Re-read after WRC-27.

---

## 3. Implications for the Coverage-First Broadband Model

The coverage-first model has a specific chain: a minimum number of satellites buys coverage, the model then ASSUMES full coverage of the target region, and the percent of the covered population actually served is set by purchased bandwidth (capacity), with spectrum cost as a real economic line. Wave-5 populates and tightens every link.

**Link 1: minimum-sats-for-coverage.** The US+Europe coverage floor is **~130-450 satellites** [COMM-215]. This is the entry ticket, a few-hundred-satellite build, well inside a Neutron cadence ramp (90 launches by 2036 at ~5 V3-class per launch is ~450 broadband satellites). The floor is cheap, and it is a coverage problem, not a capacity problem.

**Link 2: full-coverage assumption.** Coverage is flat across geography: a beam covers an area regardless of how many people are under it [COMM-224]. So once the floor is met, the model's "assume full coverage of the region" step is justified by geometry, and what varies geographically is not coverage but how many of the covered people the capacity can serve. The coverage floor sets the satellite count; demand density and spectrum set everything above it.

**Link 3: percent-of-covered-population served, set by purchased bandwidth.** This is where wave-5 corrects a tempting error. The user spectrum is NOT the differentiator [COMM-189]: a generation's capacity comes from beams x spatial-reuse x wide backhaul, not from a wider user band. So "percent served" is driven by the per-beam capacity the purchased bandwidth supports (the AST anchor: ~120 Mbps on ~40 MHz, NOT a naive bandwidth-times-efficiency division), divided by the per-user service level, times oversubscription, times beams, times the satellite count. The satellite count from Link 1 is a coverage number; the served-customer total is a capacity number layered on top of it. The biggest remaining input is the per-user service level and oversubscription (carried as a band in `SPECTRUM_spec.md`), not the spectrum quantity, which is one reused block.

**Link 4: spectrum cost as a real economic line.** Wave-5 makes this line concrete and forks it:
- Under the **SCS lease** (the entrant-realistic door, the ~2x5 MHz to ~40 MHz block reused across beams), spectrum is near-zero capex and a **wash** in the cost comparison by construction. This is the model's default.
- Under **owned spectrum** (the SpaceX-EchoStar ~$17B/~65 MHz path), spectrum is a real capital line: **~$32-46B for a 100 MHz US+Europe floor, ~$65-90B for a 200 MHz incumbent-match** [COMM-245, COMM-246]. At a sourced ~$0.65-1.03/MHz-POP with no entrant discount [COMM-241], this is not a hand-wave; it is a tens-of-billions line that dwarfs the satellite build.

The structural takeaway: **the satellites are cheap (a few hundred for coverage) and the spectrum is expensive if owned.** The model's headline sensitivity is therefore the spectrum access mechanism, not the satellite count. If the lease holds, spectrum nets out and the comparison is a satellite-cost-vs-ground-cost story. If the entrant must own spectrum, the cost stack gains a ~$32-90B line that no satellite cadence can absorb, which is exactly why the SCS lease, not the buy, is the realistic entrant path.

---

## 4. What Was Chat-Only and Is Now Sourced

The `.agent/other/comms_model_design/` briefs ([`DESIGN.md`](../../.agent/other/comms_model_design/DESIGN.md), [`SPECTRUM_spec.md`](../../.agent/other/comms_model_design/SPECTRUM_spec.md)) and the [`v3_spectrum_research_06_22.md`](../../.agent/other/v3_spectrum_research_06_22.md) brief asserted several numbers conversationally that are now properly sourced and citable in the corpus:

- **The coverage floor count.** The briefs treated "coverage is cheap and flat" as a stated principle. It is now a sourced, geometry-derived count: ~130-450 for US+Europe, validated against Iridium 66 ([`leo_constellation_coverage_minimums.md`](../direct_communication/leo_constellation_coverage_minimums.md), COMM-209..228).
- **The fold ratio and the launch-fit asymmetry.** The v3_spectrum brief's "V3 antenna IS the flat body, you can fold antennas but the D2C aperture is diameter-bound" is now sourced with the ~1x V3 fold ratio, the AST Micron tile count, and the membrane-vs-reflectarray packing rule ([`large_array_folding_and_stow.md`](../competitors/large_array_folding_and_stow.md), COMM-197..208).
- **The V3 spectrum incorporation.** The brief's band table is now the full band-by-band inventory with the load-bearing bandwidth-to-capacity derivation (user spectrum is not the differentiator) ([`starlink_v3_v4_spectrum_incorporation.md`](../competitors/starlink_v3_v4_spectrum_incorporation.md), COMM-178..190).
- **The spectrum dollars.** The briefs' "~$17B owned-spectrum buy is the hyperscale exception" is now backed by a sourced secondary-market price (~$0.65-1.03/MHz-POP) and the US+Europe total-dollar translation (~$32-90B), so the owned-spectrum scenario the briefs carried as a side note is now a quantified, citable line ([`spectrum_purchase_and_6g.md`](../direct_communication/spectrum_purchase_and_6g.md), COMM-229..248).

The model briefs can now cite these COMM IDs in place of the chat-only assertions, and the one number the briefs deliberately leave open (the per-user service level and oversubscription) is confirmed by wave-5 as the genuine remaining founder input, not a sourcing gap.
