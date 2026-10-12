# Flatellite Panel and Stack: How Large a Body Neutron Holds, and How Many Fit a Launch

**Research date:** 2026-09-29 (a calculation and its independent validation, run locally); landed here 2026-10-05.
**Purpose:** Give the Iridium model's panel and satellites-per-launch values their repo rows: the largest Flatellite body that Neutron's fairing holds, and how many such bodies stack per launch today and with the Neutron block upgrade. This refines [`flatellite_platform.md`](flatellite_platform.md) (COMM-249..270), whose "~16 per Neutron" is a read of one render at the 13 t reference orbit; those rows stay as history.
**Vehicle modeled:** Neutron only.
**Status:** Validated locally: calculation C computed the panel and the counts, and validation D, a separate check that wrote none of the inputs or the calculation, re-derived them with its own code and re-read the sources. The panel is a good upper bound. The counts are low confidence. Its status in this wiki is in `research/RESEARCH_TRACKER.md`.

> **Grounds in and does not duplicate:**
> - [`flatellite_platform.md`](flatellite_platform.md) (COMM-249..270): what Flatellite is, that Rocket Lab publishes no mass, power or dimension (COMM-252), the single render-read mass (COMM-253, COMM-256) and the render's ~16 (COMM-255, COMM-258..260).
> - [`neutron/payload_and_block_upgrade.md`](neutron/payload_and_block_upgrade.md) (NTR-007): the block upgrade as a lift gain on historical launch-vehicle growth, which this note's +15 to +30 percent band carries as an assumption.
> - The local record (validated, the investor's checkout only): `.agent/other/flatellite_dimensions_09_29/` (local), with `calc_summary.md`, `calc_flatellite_stack.py` and its output (calculation C), and `validation_flatellite_09_29.md`, `validate_flatellite_09_29.py` and its output (validation D).

---

## 0. Answer first

1. **Panel: at most 15.4 m^2,** a chamfered near-square octagon about 4.1 m by 4.0 m (calculation C: 15.40 m^2, 4.13 by 4.03 m; validation D: 15.42 m^2, 4.14 by 4.04 m). It is an upper bound: the body's corners touch the usable envelope. With clearance, or a body also sized for Falcon 9, it is 14.0 to 15.4 m^2. (COMM-711)
2. **Today: 15 per launch, mass-bound** (range 11 to 20). (COMM-712)
3. **With the Neutron block upgrade: 16,** for the stack kept in the fairing's cylinder at calculation C's 0.3949 m pitch (6.3187 m / 16, R1's 16 layers filling the cylinder; a convention, not a bound) on a rod-held base; a Lightband adapter gives 15, an ESPA ring 14. An upgraded Neutron could carry 17 to 19 only with the stack rising into the nose. Low confidence. (COMM-713)

Both counts rescale the layer count of one illustrative Rocket Lab render. The readings that do not rest on that count of 16 point lower (9 to 15 today).

---

## 1. The inputs, each with its class

| Input | Value | Class and source |
|---|---|---|
| Usable envelope, lower band | 4.7915 m wide, from the interface plane to 4.5632 m | OFFICIAL: Neutron Payload User's Guide v1.0 (Jan 2025), Sec. 4.3, Fig. 13 |
| Usable envelope, upper band | 5.5799 m wide, 4.5632 to 6.3187 m | OFFICIAL: same figure |
| Nose callouts | 3.7067 m wide at 9.1698 m; a 0.3248 m tip at 11.6497 m | OFFICIAL: same figure; the profile between callouts (arc or chords) is an ESTIMATE |
| Lift, 500 km at 40 degrees, booster landing downrange | 13,000 kg | OFFICIAL: the guide's Table 2 |
| Lift, 450 km at 53 degrees (the model's orbit), downrange landing | 12,600 kg, plus or minus 100 | ESTIMATE: read off the guide's performance curves and interpolated between inclinations; validation D's own read gives 12,601 to 12,630 kg |
| Body shape | a chamfered octagon, 1.025 : 1, all eight vertices on one circle (within 0.32 percent) | ESTIMATE: Rocket Lab's Q1 2025 investor deck, slide 20 (a plan-view line drawing, no scale), measured by research A and validation D |
| Satellite mass | 812.5 kg (13,000 kg / 16), with the author's hedge "about 200 kg less" (612.5 kg) | ESTIMATE, single source and circular: illdefined.space derived it from the render's count (COMM-253, COMM-256) |
| Render layers | R1, Rocket Lab's Flatellite fairing render: 16 layers inside the cylinder (three readers). R5, the 2023 Neutron stack artwork: about 26 (two readers) | ESTIMATE: Rocket Lab captions R1 "for illustrative purposes only, not intended to be an accurate representation" (its Q2 2026 investor deck, slide 10) |
| Stack pitch (stowed thickness per satellite) | not published for Flatellite or any comparable | UNKNOWN: 0.3949 m if R1's 16 layers fill the 6.3187 m cylinder (6.3187 m / 16, calculation C's convention); 0.243 m if R5's 26 fill it (6.3187 m / 26, the same convention); 0.43 to 0.49 m if R1 is scaled to its own drawn fairing width (validation D) |
| Adapter height | 0 (a rod-held base), 0.0533 m (a Lightband), 0.61 m (an ESPA ring) | UNKNOWN for Neutron: the Lightband's 53.3 mm is official for that product (its MkII user manual); the ESPA ring's 0.61 m is a reference value (ESTIMATE) |
| Dispenser mass | none given | UNKNOWN: the guide never says whether Table 2 includes an adapter or dispenser, so the counts below allow none and report the headroom |
| Block upgrade | +15 to +30 percent lift, envelope unchanged | ESTIMATE: the repository's analogy (NTR-007); Rocket Lab has announced neither a lift gain nor a fairing change |

---

## 2. The panel (COMM-711)

The drawn body's eight vertices lie on one circle, so the largest body that fits a usable diameter D has a circumradius of D / 2, and the drawn shape covers 0.854 of that circle (calculation C: 0.8542, 0.8519 to 0.8556 over the drawing readings; validation D: 0.855, found by an exhaustive minimum-enclosing-circle search rather than an assumed circumradius).

| Largest body | Lower band (4.79 m) | Upper band (5.58 m) |
|---|---|---|
| Box, calculation C | 4.13 by 4.03 m | 4.81 by 4.69 m |
| Box, validation D | 4.14 by 4.04 m | 4.82 by 4.70 m |
| Area, calculation C | **15.40 m^2** (15.36 to 15.43) | 20.89 m^2 |
| Area, validation D | **15.42 m^2** | 20.91 m^2 |

**Why the lower band sets the panel.** A stack that starts at the interface plane spends its lowest 4.56 m in the 4.79 m band, so every plate of a full-height stack is the lower-band body. The 5.58 m body fits only a short stack between 4.56 and 6.32 m: 1.76 m, 3 to 7 bodies, 63 to 146 m^2 of panel per launch, against 231 m^2 for 15 lower-band bodies (validation D). The renders show the full-height stack.

**An upper bound.** The body's corners touch the envelope. Each 0.05 m of radial allowance costs about 4 percent of the area: 14.77 m^2 at 0.05 m and 14.14 m^2 at 0.10 m (calculation C; validation D: 14.78 and 14.16). A body also sized for Falcon 9's usable envelope would be 3.95 by 3.85 m, 14.04 m^2 (validation D). So the panel is 15.4 m^2 at most, and 14.0 to 15.4 m^2 with clearance. The envelope is OFFICIAL and the shape reading moves the area by only 0.4 percent, so confidence is good for the bound.

**No flat 25 m^2 body fits.** A flat body of 25 m^2, of any shape, is larger than the full circle of the widest usable band (5.58 m across: 24.45 m^2), so no flat 25 m^2 body fits anywhere in Neutron's usable envelope; the largest body of the drawn shape there is 20.89 m^2, and only in the short upper-band stack (calculation C; validation D: "the model's 25 m^2 cannot fit flat", 25 m^2 being the Iridium model's panel until the investor approved 15.4 m^2 on 2026-10-03). 25 m^2 is now only the saturation curve's reference panel, which the model scales linearly to the 15.4 m^2 panel (ADR 005). The older rows that put a flat ~20 to 25 m^2 Flatellite in Neutron's ~5.5 m fairing (COMM-321, COMM-362, COMM-371, COMM-375, COMM-376, COMM-559) set, where they give a reason, a 5.0 m square's side against the bore and miss its 7.07 m diagonal; they carry a dated pointer here (2026-10-12), as does COMM-322, the flat counts they assume.

**Body against aperture.** The model's panel stands for the antenna aperture. Another Rocket Lab render shows seven raised tiles on the body's face, so the aperture may be smaller than the body; the body only bounds it.

---

## 3. Satellites per launch today (COMM-712)

Two gates, and the smaller binds.

- **Mass:** floor(lift / mass). At 12,600 kg: 15 at 812.5 kg (412 kg of headroom), 20 at 612.5 kg (350 kg). The lift read-off's uncertainty changes no count: 15 holds anywhere from 12.19 to 13.0 t at 812.5 kg (validation D).
- **Geometry:** floor(usable stack height / pitch), for a full-height stack of lower-band bodies. In the cylinder on a rod-held base the stack is 6.319 m tall; at calculation C's 0.3949 m pitch (6.3187 m / 16, R1's 16 layers filling the cylinder) that is 16 bodies.

So mass binds at 15 (calculation C and validation D agree exactly). **The range is 11 to 20** (validation D): 20 at the hedged 612.5 kg with R5's thinner pitch (0.243 m), and 11 at R1's width-anchored pitch (0.43 to 0.49 m) with the stack kept in the cylinder, where geometry binds at 11 to 14. Calculation C's low end of 14 assumed its 0.3949 m pitch was an upper bound on the thickness; validation D showed the render is not drawn to the guide's proportions, so it bounds the pitch from neither side.

**Circularity.** The mass gate is floor(16 x 12,600 / 13,000) = floor(15.51) = 15: the render's 16 layers less 3 percent for the 53 degree orbit, because the mass itself is 13,000 kg / 16. Both gates rescale the same illustrative render, so neither carries independent information about the satellite. The readings that do not rest on the 16 point lower: R1's own proportions (11 to 15) and Starlink's mass per square metre on this body (Starlink v1.5, 303 kg on 3.64 m^2, and V2 Mini, 800 kg on 11.07 m^2, both masses FCC filing inputs: 1,113 to 1,282 kg per body, 9 to 11 per launch).

---

## 4. Satellites per launch with the Neutron block upgrade (COMM-713)

The upgrade is an assumption: +15 to +30 percent lift with the envelope unchanged.

- **Mass:** 17 at +15 percent (14,490 kg) and 20 at +30 percent (16,380 kg), at 812.5 kg; 23 to 26 at 612.5 kg.
- **Geometry** at calculation C's 0.3949 m pitch (6.3187 m / 16, R1's 16 layers filling the cylinder; both calculation C's output table and validation D's):

| Stack top, adapter | Usable height | Bodies |
|---|---|---|
| In the cylinder, rod-held base | 6.319 m | **16** |
| In the cylinder, Lightband | 6.265 m | 15 |
| In the cylinder, ESPA ring | 5.709 m | 14 |
| Into the nose (chord profile), rod-held base | 7.519 m | 19 |
| Into the nose (arc profile), rod-held base | 7.856 m | 19 |

Kept in the cylinder on a rod-held base, the stack takes 6.3187 m / 0.3949 m = 16 bodies, so the cylinder holds R1's 16 by construction, and the fairing binds there before the extra lift is used (validation D's binding gate: "upgraded 16 to 16 (geometry / geometry)"). Calculation C's headline 17 to 19 needs the stack to rise 1.2 to 1.5 m into the nose, above anything Rocket Lab has drawn. At R1's width-anchored pitch the cylinder holds only 11 to 14. If the upgrade also brought a taller fairing (not announced), the count would be the mass gate, 17 to 20 at the headline mass. **The range is 11 to 26** (validation D): 26 at the hedged 612.5 kg and +30 percent lift with R5's thinner pitch (0.243 m), and 11 at R1's width-anchored pitch in the cylinder. Confidence is low: the count is Rocket Lab's illustrative render count, rescaled.

---

## Open questions (what would firm it up)

1. **A Rocket Lab count.** The U.S. Space Force's SB-AMTI order flies "multiple" Flatellites on one dedicated Neutron; a disclosed quantity would be the first real satellites-per-launch figure.
2. **A Flatellite mass** (a datasheet, or an FCC or ITU filing). It replaces the circular 812.5 kg, and the count moves most with it.
3. **A stowed thickness, or a photo of real hardware against a known scale.** It replaces the render pitch, which decides whether geometry binds.
4. **A Rocket Lab dimension.** It moves the panel from DERIVED to OFFICIAL.
5. **The aperture against the body,** and how the solar wings stow: folded over the body they add to the pitch (calculation C estimates about 10 panel layers per satellite); folded along the edges they shrink the body.
6. **The adapter or dispenser** height and mass on Neutron, and any clearance inside the envelope.

---

## Sources

- [Neutron Payload User's Guide v1.0 (Jan 2025)](https://rocketlabcorp.com/assets/Uploads/Rocket-Lab-Neutron-PUG-reduced-final.pdf): Sec. 4.3 and Fig. 13 (the usable envelope; vector art, drawn to scale), Table 2 (13,000 kg to 500 km at 40 degrees, downrange landing), the performance curves (the 450 km, 53 degree read), Sec. 4.3 and 4.6 (the adapter is mission-unique and sits inside the envelope). Read by research B and re-read by validation D from the guide's own PDF.
- [Rocket Lab Q1 2025 investor deck](https://investors.rocketlabcorp.com/static-files/bbf2962a-dc50-4fe1-90e9-75caa0b8e68d), slide 20, "Flatellite vertical integration": the plan-view body and wings, measured by research A and validation D.
- [Rocket Lab Q2 2026 investor deck](https://investors.rocketlabcorp.com/static-files/3dde8e68-7ce6-4685-8c0b-17afc94dbb86): the fairing render (R1) captioned for illustrative purposes only; the SB-AMTI dedicated Neutron launch.
- [illdefined.space: Stacking the Deck: Rocket Lab's Flatellite](https://www.illdefined.space/stacking-the-deck-rocket-labs-flatellite/) (2025-03-28): the mass, derived from the render's count, with the "about 200 kg less" hedge.
- Rocket Lab's own Flatellite fairing render (R1) on rocketlabcorp.com and the Neutron stack artwork (R5), counted by research A and validation D.
- [Rocket Lab MkII Motorized Lightband user manual](https://rocketlabcorp.com/assets/Uploads/PSC/2000785N-MkII-MLB-User-Manual.pdf): the Lightband's 53.3 mm height.
- [EELV Secondary Payload Adapter (Wikipedia)](https://en.wikipedia.org/wiki/EELV_Secondary_Payload_Adapter): the ESPA ring's 0.61 m reference height (ESTIMATE).
- The comparables' masses and areas (Starlink v1.5 and V2 Mini, FCC filing inputs) as research A classed them; plausibility only.
- Local, validated (the investor's checkout only): `.agent/other/flatellite_dimensions_09_29/calc_summary.md` (local), `validation_flatellite_09_29.md` (local), their scripts and outputs.

---

## Claims ledger (COMM-711..COMM-713)

The same rows as `research/SOURCE_INDEX.md`, "Flatellite panel and stack (COMM-711..713)".

- **COMM-711**: The Flatellite panel is **at most 15.4 m^2**, a chamfered near-square octagon about 4.1 by 4.0 m: Rocket Lab's drawn body shape sized to Neutron's 4.79 m usable lower band, where every full-height flat stack sits (calculation C: 15.40 m^2, 15.36 to 15.43, 4.13 by 4.03 m; validation D: 15.42 m^2, 4.14 by 4.04 m). An upper bound, because the body's corners touch the envelope; **14.0 to 15.4 m^2** with clearance (14.77 m^2 at 0.05 m, 14.14 at 0.10 m) or a body also sized for Falcon 9 (14.04 m^2). [DERIVED from an OFFICIAL envelope and an ESTIMATE shape] Sources: Neutron Payload User's Guide v1.0, Fig. 13; Rocket Lab Q1 2025 deck, slide 20; calculation C and validation D (local).
- **COMM-712**: **15 Flatellites per launch today, mass-bound** (range 11 to 20): 12,600 kg to 450 km at 53 degrees (a curve read of the guide) over 812.5 kg (13,000 / 16, circular with the render) leaves 412 kg of headroom; geometry at calculation C's 0.3949 m pitch (6.3187 m / 16, R1's 16 layers filling the cylinder) allows 16 in the cylinder. The 20 is the hedged 612.5 kg with R5's thinner pitch (0.243 m); the 11 is R1's width-anchored pitch with the stack in the cylinder. Low confidence: both gates rescale one illustrative render's 16 layers, and the readings that do not rest on that count point lower (9 to 15). [DERIVED from ESTIMATE inputs] Sources: Neutron Payload User's Guide v1.0, Table 2 and the performance curves; illdefined.space (COMM-253); calculation C and validation D (local).
- **COMM-713**: **With the Neutron block upgrade** (an assumed +15 to +30 percent lift, envelope unchanged), **16 per launch** for the stack kept in the fairing's cylinder at calculation C's 0.3949 m pitch (6.3187 m / 16, R1's 16 layers filling the cylinder; a convention, not a bound) on a rod-held base, so the cylinder holds R1's 16 by construction: the fairing binds before the extra lift is used (mass allows 17 to 20 at 812.5 kg). A Lightband adapter gives 15, an ESPA ring 14; 17 to 19 only with the stack rising 1.2 to 1.5 m into the nose; range 11 to 26 (the 26 at the hedged 612.5 kg and +30 percent lift with R5's thinner pitch). Low confidence. [DERIVED from ESTIMATE inputs under an assumed upgrade] Sources: calculation C's geometry table and validation D's binding gate (local); Lightband manual; NTR-007 for the upgrade analogy.
