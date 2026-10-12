# The Iridium Saturation Module: Research Note

**Research date:** 2026-07 (the Iridium physics loop) and 2026-09-28 to 2026-10-04 (the saturation design, its prototypes, two blind derivations and its review rounds), all run locally; Section 1 landed here 2026-10-05, Section 2 on 2026-10-12.
**Purpose:** The research behind the Iridium model's saturation module (ADRs 005 to 010): how many satellites the owned 8 MHz of L-band can serve, per device class. Section 1 holds the inputs of the saturation curve, and of the engine that reads it, whose only source was local research, each with its repo row, so the code cites the wiki and never a local path. The curve is computed at a 25 m^2 reference panel and scaled linearly to the model's 15.4 m^2 panel, a factor of 0.616 (COMM-711; ADR 005); "the 25 m^2 reference panel" in this note is that computation basis, not a satellite that flies (no flat 25 m^2 body fits Neutron, COMM-711). Section 2 holds the three records ADRs 008 to 010 cite: how the downlink share relaxes each cell's cap inside the curve, the subscriber-share run, and the gap to the exact linear program. The module's other cross-checks and measured magnitudes are not recorded here yet (the tracker's open items).
**Status:** Section 1 (2026-10-05): the inputs, every one a model input and none a model output. Section 2 (2026-10-12): the three records ADRs 008 to 010 cite, local measurements on the design's prototypes; none is a model input or a published number.

> **Grounds in and does not duplicate:**
> - [`rocket_lab/iridium_lband_capacity_and_modernization.md`](../rocket_lab/iridium_lband_capacity_and_modernization.md) (COMM-635..660: Iridium's band, beams and narrowband headroom), [`lband_device_gate_and_ntn_roadmap.md`](lband_device_gate_and_ntn_roadmap.md) (COMM-661..676: the devices, NB-IoT NTN and its rate), [`spectrum_and_phased_array_fundamentals.md`](spectrum_and_phased_array_fundamentals.md) (COMM-569: gain, aperture and beamwidth), and [`rocket_lab/iridium_acquisition.md`](../rocket_lab/iridium_acquisition.md) (COMM-620: the 340-byte SBD message).
> - The local record (the investor's checkout only): the July physics loop, `.agent/other/iridium_physics_loop/iridium_physics_validation.md` (local), claims C-101, C-102, C-204, C-401 and C-409; the saturation design, `.agent/lifecycle/design_09_28.md` (local), with its review rounds, `.agent/lifecycle/peer_review_design_09_28.md` (local); its prototypes and blind derivations, `.agent/other/saturation_reach_09_28/` (local); its strategy, `.agent/lifecycle/strategy_09_29.md` (local), and the strategy's independent number audit, `.agent/lifecycle/number_audit_strategy_09_29.md` (local); and the build's reproductions of the prototypes, `.agent/lifecycle/execution_saturation_10_04_p1.md` (local) and `.agent/lifecycle/execution_saturation_10_04_p2.md` (local).

---

## 1. The inputs whose only source was local research

Eight values, each a constant the module or the engine reads. Three are computed (`derived_estimate`). Four are engineering estimates with no external source: their rows take `scenario`, a chosen modeling assumption, and they are not investor-set. One is a standard's exact value, `certified` on two credible secondary sources that cite the standard's clauses.

### 1.1 NB-IoT's narrowest uplink subcarrier: 3.75 kHz (COMM-714)

**What it is.** NB-IoT's narrowest uplink allocation: one subcarrier, or tone, 3.75 kHz wide, used only by single-tone transmissions (single-tone also runs at 15 kHz, and multi-tone at 15 kHz only). NB-IoT's 180 kHz carrier holds 48 such tones, or 12 at 15 kHz; the 8 MHz band holds about 2,133 (8,000 kHz / 3.75 kHz).

**How the model uses it.** The IoT reading counts each message's channel time on one tone against the tones the uplink share of the band carries.

**Basis.** A 3GPP NB-IoT value: TS 36.211, Section 10.1.2.1 and Table 10.1.2.3-1 (the NB-IoT uplink numerology and its resource units), as two independent technical references state and cite it. MathWorks' "NB-IoT Uplink Waveform Generation" states that single-tone transmissions use either 15 kHz or 3.75 kHz spacing and multi-tone transmissions 15 kHz, with a 2 ms slot at 3.75 kHz, citing Table 10.1.2.3-1. ShareTechnote's "LTE-NB: Physical Layer: Uplink: Frame Structure" gives the two spacings, 48 subcarriers of 3.75 kHz in the 180 kHz carrier and single-subcarrier resource units at 3.75 kHz, citing Section 10.1.2.1 and showing Table 10.1.2.3-1. The row is `certified` on those two sources, as this ledger certifies other standard and textbook facts (COMM-569, COMM-662); the standard's own text was not read. The design's IoT check (its § 1.8) and its prototype (`iot_headroom.py`, local) carry the value, and the independent number audit of the strategy judged it a correct standard NB-IoT value.

### 1.2 The interference trim's conservative array floor: -0.4 dBi (COMM-715)

**What it is.** The average far-sidelobe gain of the satellite's array: how much of every co-channel beam leaks toward cells it does not serve. The interference trim lowers capacity for the aggregate interference from every satellite in view; this is its conservative floor.

**Derivation.** -0.4 dBi = 39.6 dBi - 40 dB.
- 39.6 dBi is the broadside directivity of the 25 m^2 reference panel at 1.621 GHz with uniform illumination, 4 pi A / lambda^2 with lambda = 18.49 cm (the physics loop's C-101 gives 39.5 dBi at 1.6 GHz).
- The 40 dB is C-401's conservative edge. The far floor of a calibrated digital array is its mean error-sidelobe floor, sigma^2 / N, an estimate from the phased-array literature (Mailloux; Skolnik) as C-401 applies it: for the reference panel's about 2,848 elements at 5 to 20 percent per-element error power it lies 47.6 to 41.5 dB below the peak, and C-401 takes -40 dB as the conservative edge. C-409 places its interference-budget wall at that floor.

### 1.3 The trim's calibrated-array band: -2 and -8 dBi (COMM-716)

**Derivation.** C-401's band itself: 39.6 - 41.5 = -1.9 dBi, rounded to -2, and 39.6 - 47.6 = -8.0 dBi. The trim reports at these two floors beside the conservative edge of 1.2.

### 1.4 The scan roll-off exponent: 1.3, in g = cos^1.3(eta) (COMM-717)

**What it is.** An array element's gain falls as the beam scans away from broadside: g = cos^1.3(eta) at scan angle eta. In the trim it weights the power each beam needs (power control holds the flux at the target, so a beam's power goes as the slant range squared over g) and each satellite's sidelobes toward a victim cell.

**Basis.** ESTIMATE. Blind derivation A chose it ("cos^1.3 element roll-off, ESTIMATE", its § 3) and blind derivation B used the same exponent in its elevation-dependent link sensitivity (its § 7); neither brief supplied it. The design's uplink link budget uses it too: the round-1 review's budget of a 0 dBi phone-class device, a 7 dB noise figure, 6.5 dB of extra losses, a 10 dB SNR target and 39.6 dBi at nadir with cos^1.3 scan loss (the design's 1.7, "Power and the uplink"). It moves only the trim and that power estimate. An array element-pattern reference would source it.

### 1.5 The terminal pattern's floor: -20 dB (COMM-718)

**What it is.** The directional terminals' antenna pattern: a Gaussian main lobe of the class's 3 dB beamwidth (60.3 degrees for the 10 dBi small terminal, 33.9 degrees for the 15 dBi mounted terminal), floored at -20 dB relative to its peak. It prices how much each stacked co-channel layer over a cell interferes with that cell's other layers, so it sets the directional classes' spectral efficiency from the geometry each cell gets.

**Basis.** ESTIMATE: the design's round-2 reviewer's value (the design's § 2, its rule 3, and the round-2 check of the stacked layers). It is optimistic for the small terminal, whose side levels toward other layers the design's revision 1 had put at -10 to -15 dB. A terminal antenna reference would source it.

### 1.6 The IoT airtime: 4 to 7 s per 340-byte message on one tone (COMM-719)

**What it is.** How long one minimal-packet IoT message (340 bytes, the SBD message size of COMM-620) holds one 3.75 kHz uplink tone.

**Basis.** ESTIMATE: the design reviewer's figure (round 1, RV-16), with no working written down. It is 1.5 to 5 times the 1.4 to 2.7 s that the corpus's 1 to 2 kbps NB-IoT NTN envelope (COMM-665) gives for 2,720 bits before repetition and overhead. It is conservative against the physics loop's uplink budget: C-204's 0.2 W, 0 dBi device nets +4.2 dB at the 450 km mask edge over a 1.54 MHz channel, and one 3.75 kHz tone is about 26 dB narrower, so an outdoor device at the mask needs little or no repetition, and its airtime sits near the no-repetition figure. It feeds only the IoT reading, which sizes nothing. A worked NB-IoT NTN airtime budget on this array would source it.

### 1.7 The taper's beamwidth factor: 1.0934 lambda / D (COMM-720)

**What it is.** The realistic-array band, the design's F9, carries the effective ground area per beam as three points: the uniform beam, central (footprints touching, the upper bound on the beams in use); the 2.32 degree taper, x 1.52; and the taper with wider spacing, x 2.3. A real array tapers its illumination to control sidelobes, which widens the beam. The taper point uses a 3 dB beamwidth of 1.0934 lambda / D on the 25 m^2 reference panel's 5 m side at 1.621 GHz, 2.32 degrees, against the uniform beam's 0.886 lambda / D, 1.88 degrees. Its footprint is (1.0934 / 0.886)^2 = 1.52 times the uniform beam's area.

**Derivation.** 1.0934 = 0.886 x 2.32 / 1.88. The 2.32 degrees is the physics loop's C-102: the tapered 70 lambda / D convention (COMM-569's beamwidth rule) on the 25 m^2 reference panel's equal-area diameter, 5.64 m, at 1.6 GHz, where uniform illumination gives 1.94 degrees. Cross-check: blind derivation B's own taper, 1.10 lambda / D, gives an area 1.54 times the uniform beam's. The ratio takes its two beams from two frames: the tapered beam is C-102's equal-area circle at 1.6 GHz, the uniform beam the 5 m square's at 1.621 GHz. In one frame, C-102's own pair (2.32 and 1.94 degrees) gives an area 1.43 times the uniform beam's, so the factor's x 1.52 lies inside the bracket from x 1.43 (C-102) to x 1.54 (blind derivation B), and no input moves (noted 2026-10-12, after the review since the push).

### 1.8 The co-channel spacing area factor: 1.5 (COMM-721)

**What it is.** A real network spaces co-channel beams wider than touching footprints to limit interference. The band's third point gives each beam 1.5 times its ground area; with the taper, 1.52 x 1.5 = 2.3 times the uniform beam's.

**Basis.** Blind derivation B's rule (its § 7 sensitivities: co-channel spacing 1.5x, ground area per beam x 1.5; the taper and the spacing together, area x 2.3). The design carries it as the band's third point (its § 2 and F9). An engineering choice with no external source.

---

## 2. The records ADRs 008 to 010 cite

Three cross-checks the module's ADRs cite: how the downlink share relaxes each cell's people cap inside the curve (ADR 008), the subscriber-share run (ADR 009) and the gap to the exact linear program (ADR 010). Each is a local measurement on the saturation design's prototypes (`reach_sim.py` for the phone class, `directional_sim.py` for the terminals), 2026-09-28 to 2026-10-03, at the design's settings then: one usage for every class (1 Mbps at 2.5 percent busy-hour concurrency, so 208 people a beam for the phone class and 640 and 800 for the small and mounted terminals), 150 beams, the uniform beam on the 25 m^2 reference panel, the band in full-time use (d = 1) and 40 footprint bands. None was re-run on the module. The module reproduces the phone prototype's rows within 1.2e-5 at those settings, its saturation number (20,456) exactly, and the terminal prototypes' maximum use within 2e-7 (the build's reproductions: `.agent/lifecycle/execution_saturation_10_04_p1.md` (local), task 5, and `.agent/lifecycle/execution_saturation_10_04_p2.md` (local), task 10); the promoted curve runs the investor's per-class usage (2026-10-04: at d = 1, 277.33 people a beam for the phone class, 320 for the small terminal and 40 for the mounted terminal, from the curve's parameters) at 160 footprint bands (the investor's ruling, 2026-10-06). So each record gives the measured size of its effect at those settings, not a figure at the promoted curve's. None is a model input or a published number, so none mints a claim ID; a row joins if a public document ever quotes one.

### 2.1 How the downlink share relaxes each cell's people cap (ADR 008)

**What it measures.** The curve is computed with the band in full-time use (d = 1), and the engine scales people and capacity by d (ADR 008). That rule ignores one effect: a smaller d lowers the people each beam carries (the class's people a beam times d), so a cell takes more beams before its people cap binds, and the allocation can light a little more. The check ran the prototypes at d = 0.67 (for the phone class also 0.5 and 0.75) against d = 1, on the same snapshots.

| Class | Maximum use | At 342, 992 and 1,482 satellites | Larger fleets |
|---|---|---|---|
| Small terminal (capacity) | +5.785 percent | +0.356, +0.703 and +1.173 percent | +2.443 percent at 5,402; +3.828 at 20,022 (one snapshot) |
| Mounted terminal (capacity) | +9.758 percent | +0.537, +1.032 and +1.442 percent | +3.229 percent at 5,402; +6.012 at 34,040 (one snapshot) |
| Phone class (useful beams) | +0.226 percent | +0.0017, +0.0048 and +0.0121 percent | not run |

**What it shows.** The phone class's figures are the same at d = 0.5, 0.67 and 0.75. The error is one-sided: the curve under-counts the directional classes, more as the fleet grows, and moves the phone class's useful beams by about 0.01 percent or less at these fleets. On the elasticity shift those ratios imply, the directional saturation numbers come out conservative by about 2 percent (the small terminal) and 3 to 4 percent (the mounted terminal), an ESTIMATE. The 2026-10-03 independent check of the revenue table estimated from the same ratios that, at its table's fleets (FY2031 to the steady state then, 529 to 7,225 satellites as the prototype builds them), a run at d = 0.67 carries 0.50 to 2.75 percent more (the small terminal) and 0.74 to 3.66 percent more (the mounted terminal) than the d = 1 curve times d, and the phone class 0.012 percent or less, also an ESTIMATE. The relaxation acts only where a cell's people cap binds, and the cap scales with the class's people a beam: 640 and 800 for the terminals at the one usage measured here, 320 and 40 on the promoted curve. So on the promoted curve the terminals' caps bind less often, and the mounted terminal's almost never, which is why the review since the push (2026-10-12) found the panel rule exact for it: `.agent/other/review_since_push_10_12/verify_code.md` (local). The relaxation at the promoted settings was not measured.

**Source record and status.** The strategy's finding SR-03, in its Revision 1: `.agent/lifecycle/strategy_09_29.md` (local). Its two outputs of 2026-09-29, `strategy_checks_09_29_output.txt` (part 1) and `strategy_checks_directional_09_29_output.txt`, sit with their scripts in `.agent/other/saturation_reach_09_28/` (local), and the 2026-10-03 estimate in the same folder's `revenue_new_defaults_validation_10_03.md` (its verdict item 4 and method item 4). A local measurement, validated: the strategy's round-1 reviewer re-ran the phone class at d = 0.67 with its own script (that folder's `strategy_review_r1/d_dependence_check_output.txt`: maximum use 384,932 to 385,803 beams, as in part 1), and the strategy's independent number audit matched every figure in the table to its output (its rows 16, 18, 19 and 20): `.agent/lifecycle/number_audit_strategy_09_29.md` (local). In the ledger's terms a `derived_estimate`; the shift of the saturation numbers is an ESTIMATE.

### 2.2 The subscriber-share run (ADR 009)

**What it measures.** The curve's demand is every resident of an inhabited cell (take-up 1.0, the maximal-demand bound; ADR 009). The run gives each cell 5 percent of its residents instead (take-up 0.05), for the phone class at the design's settings, to see how much the result rests on that choice.

| Marker (the round-2 reviewer's dense rerun, 2 snapshots a fleet) | Every resident | 5 percent of residents |
|---|---|---|
| Maximum use (beams) | 384,932 | 255,384 |
| The saturation number (elasticity under 0.10) | 20,456 | 18,892 (-7.6 percent) |
| Elasticity under 0.25 | 16,021 | 12,078 (-24.6 percent) |
| 90 percent of maximum use | 15,970 | 13,674 (-14.4 percent) |

**What it shows.** The maximum use moves with the share (it is an upper bound, reported as a band); the saturation number moves 7.6 percent. Across the other demand definitions and grids of the same rerun (10 and 100 people per km^2; the 0.125 and 0.5 degree grids) it moved -15 to +4 percent, and the 0.25 marker was the fragile one (-20 to -36 percent); the promoted curve carries 10 and 100 people per km^2 and the 0.5 degree grid as band points. The run also served the blind comparison. Blind derivation A, an analytic continuum relaxation, gave its markers at a 5 percent subscriber share; on that share the design's sweep (the round-1 reviewer's run) gives 85,971 useful beams at 1,980 satellites (101,834 at take-up 1.0) and markers of about 13,900 (90 percent of maximum use) and about 12,200 (elasticity under 0.25), against blind A's about 7,000 and 8,000 to 8,700, so the gap was blind A's method (a time-averaged continuum, biased early), not the demand. Blind derivation B, a numerical model on its own map at take-up 1.0, put the knee at 19,451 and 14,655 satellites (elasticity under 0.10 and 0.25), within 5 to 9 percent of the design's 20,456 and 16,021.

**Source record and status.** The design's Section 3 (revision 1, RV-07; revision 2, R2-10), its Section 7 decision 3, and its F3 to F5: `.agent/lifecycle/design_09_28.md` (local). The runs, of 2026-09-28, are in `.agent/other/saturation_reach_09_28/` (local): `review_r2/knee_take05.txt` (the dense rerun, with `review_r2/knee_robustness.py`), `review_r1/sweep_take05.txt` (the comparison) and the central markers in `knees_final_output.txt`. A local measurement by the design's round-1 and round-2 reviewers, independent of the design's lead; the strategy's number audit recomputed the share's -7.6 percent from the rows (its row 173: Matches). In the ledger's terms a `derived_estimate`.

### 2.3 The gap to the exact linear program (ADR 010)

**What it measures.** The module fills each snapshot's satellite-cell pairs smallest footprint first, a heuristic, and ships no solver (ADR 010). The check solved the exact fluid linear program on identical snapshots, pairs and constraints (scipy's HiGHS) and set the heuristic's useful beams against its optimum, for the phone class at the design's settings.

| Demand, grid | Satellites | Heuristic over the exact optimum | Run by |
|---|---|---|---|
| 10 people per km^2, 0.25 degree | 992; 3,969; 8,010 | 97.2; 95.7; 96.4 percent | the design's lead |
| 1 person per km^2, 0.25 degree | 992 | 97.8 percent | the design's lead |
| 1 person per km^2, 0.25 degree | 1,980 | 96.05 percent | the round-1 reviewer |
| 1 person per km^2, 0.5 degree | 1,980; 6,006; 10,000 | 96.51; 95.63; 95.97 percent | the round-1 reviewer |

**What it shows.** The heuristic reaches 95.6 to 97.8 percent of the exact optimum from 992 to 10,000 satellites (a gap of 2.2 to 4.4 percent), on both demand definitions and both grids. Blind derivation B's own greedy reached 96 to 98 percent of its own exact optimum mid-curve and 100 percent at saturation. The gap closes toward saturation: in the prototype's dense phone run the useful beams stay at 0.989 to 0.993 of min(ceiling, supply) from 20,022 to 40,000 satellites, so the exact optimum can add at most about 1 percent there, and the module's promotion stops if the phone class falls below 0.98 of that bound at any snapshot from 20,000 satellites up (its stall floor). The design estimated that the exact optimum would move the 90 percent marker about 10 percent earlier and the elasticity markers a few percent earlier, never the order of magnitude, an ESTIMATE.

**Source record and status.** The design's Section 4, "The gap to the exact optimum" (revision 1, RV-06), and its F5: `.agent/lifecycle/design_09_28.md` (local). The outputs, of 2026-09-28, are in `.agent/other/saturation_reach_09_28/` (local): `lp_check_output.txt` and `lp_check_ipm_output.txt` (the lead's, with `lp_check.py` and `lp_check_ipm.py`; the interior-point run at 3,969 satellites and 1 person per km^2 was stopped after about 1 hour 45 minutes without converging), `review_r1/lp_gap_ipm_0p25.txt` and `review_r1/lp_gap_ipm_0p5.txt` (the round-1 reviewer's, with `review_r1/lp_gap.py`), and `run_phone_150_banded_dense.txt` (the bound ratio). A local measurement made twice, by the design's lead and independently by its round-1 reviewer; the strategy's number audit matched every ratio to its output (its row 138: Matches when rounded). In the ledger's terms a `derived_estimate`; the effect on the markers is an ESTIMATE.

---

## Sources

- Corpus rows: COMM-569 (gain and beamwidth), COMM-620 (the 340-byte SBD message), COMM-665 (NB-IoT NTN's 1 to 2 kbps), and COMM-662 (Iridium's band is time-division duplex, so the uplink and the downlink share its tones in time).
- The Iridium physics loop (local, validated in July 2026): C-101 (the reference panel's gain), C-102 (its beamwidth, uniform and tapered), C-204 (the uplink budget of a 0.2 W, 0 dBi device), C-401 (the calibrated array's error-sidelobe floor), C-409 (the interference-budget wall at that floor).
- The phased-array error-floor estimate (Mailloux; Skolnik), as C-401 applies it; not re-read for this note.
- The saturation design (local): § 1.7 "Power and the uplink", § 1.8 (the IoT row and its channel-time check), § 2 (the beam, the effective-area band and the directional rules), F9 (the realistic-array band); its round-1 and round-2 reviews; its prototypes `interference_trim.py`, `iot_headroom.py`, `directional_sim.py` and `reach_sim.py`, the round-2 check `review_r2/layers_check.py`, and blind derivations A and B (`blind_a/derivation.md`, `blind_b/derivation.md`), all under `.agent/other/saturation_reach_09_28/` (local).
- The independent number audit of the strategy (local), which asked that the tone get its own citation and that the airtime, the pattern floor and the scan roll-off be labeled estimates, and which matched Section 2's figures to their outputs (its rows 16, 18 to 20, 138 and 173).
- For Section 2, all in `.agent/other/saturation_reach_09_28/` (local) unless named: the strategy's SR-03, `.agent/lifecycle/strategy_09_29.md` (local); `strategy_checks_09_29_output.txt`, `strategy_checks_directional_09_29_output.txt`, `strategy_review_r1/d_dependence_check_output.txt` and `revenue_new_defaults_validation_10_03.md` (2.1); the design's Section 3, Section 7 decision 3 and F3 to F5, `review_r2/knee_take05.txt`, `review_r1/sweep_take05.txt` and `knees_final_output.txt` (2.2); the design's Section 4, `lp_check_output.txt`, `lp_check_ipm_output.txt`, `review_r1/lp_gap_ipm_0p25.txt`, `review_r1/lp_gap_ipm_0p5.txt` and `run_phone_150_banded_dense.txt` (2.3); each output beside the script that wrote it.
- For COMM-714: [MathWorks, "NB-IoT Uplink Waveform Generation"](https://www.mathworks.com/help/lte/ug/nb-iot-uplink-waveform-generation.html) and [ShareTechnote, "LTE-NB: Physical Layer: Uplink: Frame Structure"](https://www.sharetechnote.com/html/Handbook_LTE_NB_FrameStructure_UL.html), both read 2026-10-05, both citing 3GPP TS 36.211 Table 10.1.2.3-1, and ShareTechnote also Section 10.1.2.1; the standard's own text was not read.

---

## Claims ledger (COMM-714..COMM-721)

The same rows as `research/SOURCE_INDEX.md`, "The saturation module's locally sourced inputs (COMM-714..721)".

- **COMM-714**: NB-IoT's narrowest uplink allocation is **one 3.75 kHz subcarrier** (single-tone only; single-tone also runs at 15 kHz, and multi-tone at 15 kHz only), so Iridium's 8 MHz holds about **2,133 tones**; the IoT reading counts message channel time in these tones. [FACT, two secondary sources that cite the standard] Sources: MathWorks, "NB-IoT Uplink Waveform Generation"; ShareTechnote, "LTE-NB: Physical Layer: Uplink: Frame Structure"; 3GPP TS 36.211 Table 10.1.2.3-1 (both cite it) and Section 10.1.2.1 (ShareTechnote).
- **COMM-715**: The interference trim's **conservative array floor is -0.4 dBi**: the 25 m^2 reference panel's 39.6 dBi broadside directivity at 1.621 GHz less C-401's conservative -40 dB edge of a calibrated array's sigma^2 / N error-sidelobe floor, the floor at which C-409 places its interference-budget wall. [DERIVED on an ESTIMATE floor] Sources: the physics loop's C-101, C-401, C-409 (local); Mailloux and Skolnik as C-401 applies them.
- **COMM-716**: The trim's **calibrated-array band is -2 to -8 dBi**: 39.6 dBi less C-401's 41.5 to 47.6 dB, the sigma^2 / N floor of about 2,848 elements at 20 to 5 percent per-element error power. [DERIVED on an ESTIMATE floor] Sources: the physics loop's C-401 (local).
- **COMM-717**: The array's **scan roll-off is g = cos^1.3(eta)**, weighting each beam's power and sidelobes by scan angle in the trim. [ESTIMATE: chosen independently by blind derivations A and B; also in the design's uplink link budget] Sources: blind A § 3, blind B § 7, the design's 1.7 "Power and the uplink" (local).
- **COMM-718**: The directional terminals' **pattern floor is -20 dB** below the main-lobe peak (a Gaussian main lobe of 60.3 degrees for the small terminal, 33.9 degrees for the mounted terminal); optimistic for the small terminal, whose side levels the design earlier put at -10 to -15 dB. [ESTIMATE: the design's round-2 reviewer's value] Sources: the design's § 2, rule 3; `directional_sim.py` and `review_r2/layers_check.py` (local).
- **COMM-719**: A **340-byte minimal-packet IoT message holds one 3.75 kHz uplink tone for about 4 to 7 s**: 1.5 to 5 times the 1.4 to 2.7 s that COMM-665's 1 to 2 kbps NB-IoT NTN envelope gives before repetition and overhead, and conservative against the physics loop's uplink budget (C-204), under which an outdoor device at the mask needs little or no repetition. [ESTIMATE: the design reviewer's figure, RV-16] Sources: the design's round-1 review (RV-16) and § 1.8, `iot_headroom.py`, C-204 (local); COMM-620, COMM-665.
- **COMM-720**: The taper point's **beamwidth factor is 1.0934 lambda / D**, 2.32 degrees on the 25 m^2 reference panel's 5 m side at 1.621 GHz against the uniform 0.886 lambda / D (1.88 degrees), so its **footprint is 1.52 times** the uniform beam's area; 2.32 degrees is C-102's tapered 70 lambda / D convention. Blind derivation B's independent taper, 1.10 lambda / D, gives x 1.54. The ratio mixes two frames (C-102's equal-area circle at 1.6 GHz, the 5 m square at 1.621 GHz); C-102's own pair in one frame gives x 1.43, so x 1.52 lies inside the bracket x 1.43 to x 1.54. [DERIVED] Sources: the physics loop's C-102 (local); COMM-569; `reach_sim.py` and the design's F9 (local); blind B § 7 (local).
- **COMM-721**: The band's **co-channel spacing gives each beam 1.5 times its ground area**; with the taper, **2.3 times** the uniform beam's (1.52 x 1.5). [ESTIMATE: blind derivation B's rule; the 2.3 DERIVED] Sources: blind B § 7; the design's § 2 and F9 (local).
