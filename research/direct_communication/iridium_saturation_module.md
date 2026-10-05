# The Iridium Saturation Module: Research Note

**Research date:** 2026-07 (the Iridium physics loop) and 2026-09-28 to 2026-10-04 (the saturation design, its prototypes, two blind derivations and its review rounds), all run locally; Section 1 landed here 2026-10-05.
**Purpose:** The research behind the Iridium model's saturation module (ADRs 005 to 010): how many satellites the owned 8 MHz of L-band can serve, per device class. Section 1 holds the inputs of the saturation curve, and of the engine that reads it, whose only source was local research, each with its repo row, so the code cites the wiki and never a local path. The module's cross-checks and measured magnitudes join this note as the module is built (ADRs 008 to 010 name three: how the downlink share relaxes each cell's cap inside the curve, the subscriber-share run, and the gap to the exact linear program).
**Status:** Section 1. Every value is a model input; none is a model output.

> **Grounds in and does not duplicate:**
> - [`rocket_lab/iridium_lband_capacity_and_modernization.md`](../rocket_lab/iridium_lband_capacity_and_modernization.md) (COMM-635..660: Iridium's band, beams and narrowband headroom), [`lband_device_gate_and_ntn_roadmap.md`](lband_device_gate_and_ntn_roadmap.md) (COMM-661..676: the devices, NB-IoT NTN and its rate), [`spectrum_and_phased_array_fundamentals.md`](spectrum_and_phased_array_fundamentals.md) (COMM-569: gain, aperture and beamwidth), and [`rocket_lab/iridium_acquisition.md`](../rocket_lab/iridium_acquisition.md) (COMM-620: the 340-byte SBD message).
> - The local record (the investor's checkout only): the July physics loop, `.agent/other/iridium_physics_loop/iridium_physics_validation.md` (local), claims C-101, C-102, C-401 and C-409; the saturation design, `.agent/lifecycle/design_09_28.md` (local), with its review rounds, `.agent/lifecycle/peer_review_design_09_28.md` (local); its prototypes and blind derivations, `.agent/other/saturation_reach_09_28/` (local); and the independent number audit of its strategy, `.agent/lifecycle/number_audit_strategy_09_29.md` (local).

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
- The 40 dB is C-401's conservative edge. The far floor of a calibrated digital array is its mean error-sidelobe floor, sigma^2 / N, an estimate from the phased-array literature (Mailloux; Skolnik) as C-401 applies it: for the panel's about 2,848 elements at 5 to 20 percent per-element error power it lies 47.6 to 41.5 dB below the peak, and C-401 takes -40 dB as the conservative edge. C-409 places its interference-budget wall at that floor.

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

**What it is.** The realistic-array band, the design's F9, carries the effective ground area per beam as three points: the uniform beam, central (footprints touching, the upper bound on the beams in use); the 2.32 degree taper, x 1.52; and the taper with wider spacing, x 2.3. A real array tapers its illumination to control sidelobes, which widens the beam. The taper point uses a 3 dB beamwidth of 1.0934 lambda / D on the 5 m square aperture at 1.621 GHz, 2.32 degrees, against the uniform beam's 0.886 lambda / D, 1.88 degrees. Its footprint is (1.0934 / 0.886)^2 = 1.52 times the uniform beam's area.

**Derivation.** 1.0934 = 0.886 x 2.32 / 1.88. The 2.32 degrees is the physics loop's C-102: the tapered 70 lambda / D convention (COMM-569's beamwidth rule) on the 25 m^2 panel's equal-area diameter, 5.64 m, at 1.6 GHz, where uniform illumination gives 1.94 degrees. Cross-check: blind derivation B's own taper, 1.10 lambda / D, gives an area 1.54 times the uniform beam's.

### 1.8 The co-channel spacing area factor: 1.5 (COMM-721)

**What it is.** A real network spaces co-channel beams wider than touching footprints to limit interference. The band's third point gives each beam 1.5 times its ground area; with the taper, 1.52 x 1.5 = 2.3 times the uniform beam's.

**Basis.** Blind derivation B's rule (its § 7 sensitivities: co-channel spacing 1.5x, ground area per beam x 1.5; the taper and the spacing together, area x 2.3). The design carries it as the band's third point (its § 2 and F9). An engineering choice with no external source.

---

## Sources

- Corpus rows: COMM-569 (gain and beamwidth), COMM-620 (the 340-byte SBD message), COMM-665 (NB-IoT NTN's 1 to 2 kbps), and COMM-662 (Iridium's band is time-division duplex, so the uplink and the downlink share its tones in time).
- The Iridium physics loop (local, validated in July 2026): C-101 (the panel's gain), C-102 (its beamwidth, uniform and tapered), C-204 (the uplink budget of a 0.2 W, 0 dBi device), C-401 (the calibrated array's error-sidelobe floor), C-409 (the interference-budget wall at that floor).
- The phased-array error-floor estimate (Mailloux; Skolnik), as C-401 applies it; not re-read for this note.
- The saturation design (local): § 1.7 "Power and the uplink", § 1.8 (the IoT row and its channel-time check), § 2 (the beam, the effective-area band and the directional rules), F9 (the realistic-array band); its round-1 and round-2 reviews; its prototypes `interference_trim.py`, `iot_headroom.py`, `directional_sim.py` and `reach_sim.py`, the round-2 check `review_r2/layers_check.py`, and blind derivations A and B (`blind_a/derivation.md`, `blind_b/derivation.md`), all under `.agent/other/saturation_reach_09_28/` (local).
- The independent number audit of the strategy (local), which asked that the tone get its own citation and that the airtime, the pattern floor and the scan roll-off be labeled estimates.
- For COMM-714: [MathWorks, "NB-IoT Uplink Waveform Generation"](https://www.mathworks.com/help/lte/ug/nb-iot-uplink-waveform-generation.html) and [ShareTechnote, "LTE-NB: Physical Layer: Uplink: Frame Structure"](https://www.sharetechnote.com/html/Handbook_LTE_NB_FrameStructure_UL.html), both read 2026-10-05, both citing 3GPP TS 36.211, Section 10.1.2.1 and Table 10.1.2.3-1; the standard's own text was not read.

---

## Claims ledger (COMM-714..COMM-721)

The same rows as `research/SOURCE_INDEX.md`, "The saturation module's locally sourced inputs (COMM-714..721)".

- **COMM-714**: NB-IoT's narrowest uplink allocation is **one 3.75 kHz subcarrier** (single-tone only; single-tone also runs at 15 kHz, and multi-tone at 15 kHz only), so Iridium's 8 MHz holds about **2,133 tones**; the IoT reading counts message channel time in these tones. [FACT, two secondary sources that cite the standard] Sources: MathWorks, "NB-IoT Uplink Waveform Generation"; ShareTechnote, "LTE-NB: Physical Layer: Uplink: Frame Structure"; 3GPP TS 36.211, Section 10.1.2.1 and Table 10.1.2.3-1, as both cite them.
- **COMM-715**: The interference trim's **conservative array floor is -0.4 dBi**: the 25 m^2 panel's 39.6 dBi broadside directivity at 1.621 GHz less C-401's conservative -40 dB edge of a calibrated array's sigma^2 / N error-sidelobe floor, the floor at which C-409 places its interference-budget wall. [DERIVED on an ESTIMATE floor] Sources: the physics loop's C-101, C-401, C-409 (local); Mailloux and Skolnik as C-401 applies them.
- **COMM-716**: The trim's **calibrated-array band is -2 to -8 dBi**: 39.6 dBi less C-401's 41.5 to 47.6 dB, the sigma^2 / N floor of about 2,848 elements at 20 to 5 percent per-element error power. [DERIVED on an ESTIMATE floor] Sources: the physics loop's C-401 (local).
- **COMM-717**: The array's **scan roll-off is g = cos^1.3(eta)**, weighting each beam's power and sidelobes by scan angle in the trim. [ESTIMATE: chosen independently by blind derivations A and B; also in the design's uplink link budget] Sources: blind A § 3, blind B § 7, the design's 1.7 "Power and the uplink" (local).
- **COMM-718**: The directional terminals' **pattern floor is -20 dB** below the main-lobe peak (a Gaussian main lobe of 60.3 degrees for the small terminal, 33.9 degrees for the mounted terminal); optimistic for the small terminal, whose side levels the design earlier put at -10 to -15 dB. [ESTIMATE: the design's round-2 reviewer's value] Sources: the design's § 2, rule 3; `directional_sim.py` and `review_r2/layers_check.py` (local).
- **COMM-719**: A **340-byte minimal-packet IoT message holds one 3.75 kHz uplink tone for about 4 to 7 s**: 1.5 to 5 times the 1.4 to 2.7 s that COMM-665's 1 to 2 kbps NB-IoT NTN envelope gives before repetition and overhead, and conservative against the physics loop's uplink budget (C-204), under which an outdoor device at the mask needs little or no repetition. [ESTIMATE: the design reviewer's figure, RV-16] Sources: the design's round-1 review (RV-16) and § 1.8, `iot_headroom.py`, C-204 (local); COMM-620, COMM-665.
- **COMM-720**: The taper point's **beamwidth factor is 1.0934 lambda / D**, 2.32 degrees on the 5 m aperture at 1.621 GHz against the uniform 0.886 lambda / D (1.88 degrees), so its **footprint is 1.52 times** the uniform beam's area; 2.32 degrees is C-102's tapered 70 lambda / D convention. Blind derivation B's independent taper, 1.10 lambda / D, gives x 1.54. [DERIVED] Sources: the physics loop's C-102 (local); COMM-569; `reach_sim.py` and the design's F9 (local); blind B § 7 (local).
- **COMM-721**: The band's **co-channel spacing gives each beam 1.5 times its ground area**; with the taper, **2.3 times** the uniform beam's (1.52 x 1.5). [ESTIMATE: blind derivation B's rule; the 2.3 DERIVED] Sources: blind B § 7; the design's § 2 and F9 (local).
