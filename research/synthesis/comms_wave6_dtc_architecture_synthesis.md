# Communications Wave 6: The Direct-to-Cell Architecture, from the Gain-Placement Asymmetry to the Settled Tier-1 Operating Point

*Research date: June 2026. Communications research-wiki effort, wave 6 (shared library).*

**Builds on / does not duplicate:** this is the wave-6 SYNTHESIS doc. Its job is to take the five wave-6 source docs and assemble them, around the single governing DTC system model, into one coherent picture of the direct-to-cell (DTC) architecture: why a DTC satellite needs a big antenna at all, how big, on what platform, at what orbit, on what spectrum, and over what coverage. It does NOT re-derive the inputs; every number is carried from a source doc cited by path. The load-bearing inputs are:

- The gain physics: [`dtc_antenna_aperture_tradeoff.md`](../direct_communication/dtc_antenna_aperture_tradeoff.md) (the link budget to a bare phone, the aperture-to-service ladder, and the broadband-vs-DTC gain-placement asymmetry; COMM-293..314).
- The Rocket-Lab-native platform: [`flatellite_platform.md`](../rocket_lab/flatellite_platform.md) (the Flatellite flat-body aperture, its per-Neutron count, and its status; COMM-249..270).
- The competitor platform and launch-fit benchmark: [`starlink_v3_platform_and_starship.md`](../competitors/starlink_v3_platform_and_starship.md) (V3 mass/size, why-Starship, the Neutron fairing-fit implication, and the Flatellite-as-Neutron-analog; COMM-271..292).
- The per-phone operating point: [`dtc_per_phone_rate_and_latency.md`](../direct_communication/dtc_per_phone_rate_and_latency.md) (the single-phone rate vs the per-cell rate, the aperture that delivers it, the flat-vs-fold verdict, and the low-orbit latency advantage; COMM-336..355 + COMM-371..378).
- The coverage geography: [`dtc_coverage_geography.md`](../direct_communication/dtc_coverage_geography.md) (population by latitude, the latitude-band insight, the 53-deg inclination, and the 95%-of-population target; COMM-386..405).

> **The governing model.** The DTC architecture is fixed once in [`dtc_system_model.md`](../direct_communication/dtc_system_model.md) (the single source-of-truth system model; COMM-315..335 + COMM-356..365), which states the four satellite-side levers (aperture, power, path loss/altitude, owned spectrum) with the phone held fixed and weak, the two service tiers, and the hard aperture floor. That doc is a WORK IN PROGRESS at this writing (a flat-antenna correction, the coverage result, and a final review are pending), so this synthesis references it as the governing model but does not restate it line by line, and the model doc itself is not yet filed as a reviewed catalog entry.

> **Reading guide.** Every hard number is tagged **[FACT]** (sourced to 2+ independent bodies), **[FACT, single-source]** (one source only), **[ESTIMATE]** (third-party model, target, or projection), or **[DERIVED]** (this doc's or a source doc's arithmetic on cited inputs). Sources are inline; the underlying citations live in the source docs and in [`SOURCE_INDEX.md`](../SOURCE_INDEX.md) (COMM-249..405). China is **excluded** from every market figure.

> **Scope and status.** This doc is ISOLATED TO COMMUNICATIONS and renders **NO verdict**. It assembles the wave-6 architecture into a single picture and names the biggest still-unresolved numbers. The model design itself lives in the working briefs under `.agent/other/comms_model_design/`; this doc is the sourced, citable backing for the architecture those briefs describe.

---

## 0. The wave in one page

Wave 6 answers a single question the prior waves left open: if a Rocket Lab communications business leads with direct-to-cell (the lead market by optionality), what does the satellite actually have to be, and where does it fly? The answer assembles from five docs into one chain.

1. **The big antenna moves from the ground to orbit, and that one relocation explains everything downstream.** A broadband customer owns a high-gain dish (Starlink's ~1,280-element flat panel, customer-paid) that supplies the ground-side gain, so the satellite's user antenna can be small and flat-pack. A direct-to-cell customer holds a bare phone (~0 dBi, ~23 dBm, fixed by SAR limits), which supplies nothing, so all the gain the dish would have provided must live on the satellite. **The big antenna is on the ground for broadband and in orbit for direct-to-cell.** This is the cause underneath the corpus's already-documented mass-vs-size launch asymmetry: a broadband satellite is a flat ~7 m panel that stacks ~5/Neutron (mass-bound), while a broadband-to-phone satellite is a ~223 m^2 folded aperture at ~1/Neutron (size-bound). [DERIVED, multi-source-supported; COMM-311, COMM-312]

2. **Aperture is the direct-to-cell service dial, and it splits the market into two tiers.** The revealed ladder: ~1 m^2 buys texting (Lynk), ~25 m^2 buys a few Mbps per beam (Starlink Gen2), ~60+ m^2 buys broadband-grade service to a bare phone (AST). The governing model names two tiers on this ladder: **Tier 1, "4G-grade DTC data" (~2 to 50 Mbps to a phone) at a moderate aperture, and Tier 2, "true broadband-to-phone" (~100+ Mbps, AST-class) at ~60+ m^2.** No buildable altitude turns a Tier-1 aperture into a Tier-2 one; aperture plus owned spectrum set the tier, altitude only trims a few dB. [FACT/DERIVED; COMM-298, COMM-308, governing model COMM-320]

3. **Rocket Lab's Flatellite is the Neutron-native answer, and its flat body is its own aperture.** Flatellite is a flat, stackable, no-deployable satellite explicitly pitched by Rocket Lab at "large-aperture systems, without the need for deployable antennas" for 5G-NTN/direct-to-cell. The flat body is the RF aperture, capped by Neutron's ~5.5 m fairing footprint at roughly **~20 to 24 m^2** (a ~5 m square), and because it does not fold it stacks **~8 to 16 per Neutron** (the ~16 a single render-read, estimate-bound). This is the V3 side of the fold asymmetry chosen for a DTC mission. [FACT for the design + framing; ESTIMATE for the mass/count; COMM-262, COMM-263, COMM-371]

4. **The settled Tier-1 operating point: low orbit, ~30 Mbps to one phone, ~25 MHz of owned spectrum, and the flat aperture is enough.** Published DTC throughputs (AST's ~120 Mbps) are per-cell, shared; a lightly-loaded cell hands its whole beam to one phone, so the per-cell-when-alone capacity IS the single-phone peak. Anchored on the one flying datapoint (AST BlueWalker 3, ~64 m^2, demonstrated ~21 Mbps to a phone), a **flat ~25 m^2 Flatellite at low orbit (~350 to 450 km) on ~20 to 40 MHz of owned spectrum clears ~25 Mbps to a single lightly-loaded phone on its own**, because the ~4 dB aperture shrink versus BW3 is almost entirely erased by the ~3.5 to 3.9 dB the low orbit hands back, and the rate then scales linearly with owned bandwidth. Low orbit also delivers a structural product edge: ~5 to 10 ms of propagation, inside the ITU-T G.114 "good" voice band, which GEO (~240 to 280 ms) cannot match. **So you keep the flat many-per-launch stack and only fold to ~50 m^2 to push the top of the band.** [DERIVED off the BW3 FACT; COMM-336, COMM-347, COMM-375, COMM-352]

5. **The coverage is one inclined band, and it is cheap relative to capacity.** About 95% of the world's people live within +/-55 deg latitude, the same ~95% the ITU says already sit inside a mobile-broadband footprint, so the band IS the demand base. An inclined constellation covers a global latitude BAND, not a region, so "cover US + Europe latitudes" is geometrically identical to covering the ~53-deg mid-latitude band, getting Sao Paulo, Johannesburg, Mumbai, Shanghai, and Sydney for free. **One ~53-deg shell at ~450 km, on the order of ~100 to 340 satellites for the populated band at a 95% target, covers ~95% of global mobile demand** (validated against the Iridium 66->78 real-world floor). The last few percent of people and the empty high-latitude edges are what add polar shells and the multi-fold multiplier, so they are a separately-priced scope decision. [FACT/DERIVED; COMM-386, COMM-394, COMM-404]

The biggest open numbers are three: per-satellite capacity, spectrum lease-vs-own, and per-satellite cost. The rest of this doc sources each link and names those gaps precisely.

---

## 1. The Confirmed Architecture

### 1.1 The gain-placement asymmetry (the load-bearing insight)

The gain a link needs is fixed by physics; what differs between broadband and direct-to-cell is *where you put the big antenna*.

| | Broadband (dish-served) | Direct-to-cell (bare phone) |
|---|---|---|
| Ground-side antenna | high-gain phased-array dish (~1,280 elements, customer-paid) | bare phone, ~0 dBi, ~23 dBm, fixed by SAR |
| Who supplies the ground-side gain | the customer's dish | nothing; the phone cannot |
| Therefore the satellite's user antenna | small, flat-pack (the dish already closed the link) | giant (it supplies the gain the dish would have) |
| Stow behavior | flat panel, dense-stack, many-per-launch | folded accordion (broadband-grade), ~1-3 per medium launcher |
| Binding launch gate | mass | stowed size (the antenna) |

The bare phone arrives at the satellite ~25 dB short of the LTE-QPSK decode floor (~153 dB free-space path loss at 1.9 GHz to LEO, the phone at ~-130 dBm against a ~-105 dBm threshold), a deficit only the satellite's own antenna gain and receive chain can close [FACT, single-source on the exact dB; COMM-294]. Antenna gain follows `G = 4 pi eta A / lambda^2`, so both uplink sensitivity (G/T) and downlink EIRP rise with one lever, aperture area [FACT; COMM-295, COMM-296]. **The big antenna is on the ground for broadband and in orbit for direct-to-cell, and that single relocation is the cause underneath the corpus's mass-vs-size launch asymmetry** (a flat ~7 m broadband panel at ~5/Neutron mass-bound vs a ~223 m^2 broadband-to-phone aperture at ~1/Neutron size-bound) [DERIVED; COMM-311, COMM-312].

### 1.2 The aperture-to-service ladder, and the two tiers

Aperture maps to service class on a revealed ladder, because more gain raises SNR per beam (toward the Shannon ceiling) and narrows the beam (more reuse):

| Service target | Representative system | Satellite antenna area | Tag |
|---|---|---|---|
| Intermittent SMS | Lynk Global | ~1 to 1.5 m^2 | [FACT] |
| SMS -> voice / low-rate data | Starlink Gen2 D2C | ~25 m^2 | [FACT] |
| Broadband to phone | AST BlueBird Block 1 | ~64 m^2 | [FACT] |
| Broadband to phone (high) | AST BlueBird Block 2 | ~223 m^2 (up to 120 Mbps/cell) | [FACT/DERIVED] |

The governing model draws two tiers on this ladder [governing model COMM-320]:

- **Tier 1, "4G-grade DTC data" (~2 to 50 Mbps to a bare phone):** reachable at a MODERATE aperture (~25 to 50 m^2), the rung above texting. This is the founder's product class.
- **Tier 2, "true broadband-to-phone" (~100+ Mbps, AST-class):** requires ~60+ m^2; a ~25 m^2 aperture does not reach it at any buildable altitude.

The lever ranking is the model's central rule: **aperture and owned spectrum are the STRONG levers; altitude is a WEAK lever** (550 -> 350 km buys only ~3.5 to 4 dB, far less than the ~9.5 dB aperture span from ~25 to ~223 m^2); and **satellite count is NOT a per-phone-rate lever at all** (it sets coverage continuity and total system capacity, not the rate to one handset) [DERIVED; COMM-308, governing model COMM-318/320].

### 1.3 The Flatellite flat-body aperture (~20 to 24 m^2, no fold, ~8 to 16 per Neutron)

Rocket Lab's Flatellite (unveiled 27 Feb 2025) is the Rocket-Lab-native instantiation of the V3-side flat-pack: a flat, stackable, high-power, no-deployable satellite, comms-first, with Rocket Lab's VP framing it as "an elegant solution for large-aperture systems, without the need for deployable [antennas]" and naming "5G NTN" with "minimum viable constellations in the 150 to 200-satellite range" [FACT, multi-source; COMM-249, COMM-262]. The flat body IS the RF aperture, so it is capped by Neutron's ~5.5 m fairing footprint at roughly **~20 to 24 m^2** (a ~5 m square is ~25 m^2), and because it does not fold it stacks dense: the candidate broadband sats-per-Neutron is **~12 to 16 (SSO-to-LEO)**, where ~16 to LEO is the convergence of the mass gate (13,000 kg / ~800 kg = 16.3) and Rocket Lab's own fairing render [DERIVED on a single-source mass; COMM-260, COMM-263].

This is the most favorable per-launch count in the corpus (~16 vs ~5 for a V3-class broadband slab, ~1 for an AST Block-2 D2C aperture), precisely because Flatellite is light and flat with no folding antenna, and also the softest, because Rocket Lab has published no mass, power, dimensions, or aperture area [ESTIMATE, single-source; COMM-253, COMM-264]. The competitor benchmark confirms the design logic: a V3 is launched on Starship because it is too LARGE for Falcon 9's 5.2 m fairing (the ~7 m slab) and ~3x a V2 Mini in mass; a bare V3 slab fits Neutron's ~5.5 m fairing but is mass-bound at ~5/launch (~1/12 of a Starship batch), so the Neutron-rational design is a smaller flat-pack, the Flatellite, not a literal V3 [FACT/DERIVED; COMM-281, COMM-285, COMM-287].

### 1.4 The settled Tier-1 operating point: low orbit, ~30 Mbps to one phone, ~25 MHz owned

The founder refined the product to a single-phone target (~25 to 50 Mbps to ONE phone), which is a different quantity from the per-cell figures the corpus carries. The resolution: published DTC throughputs are PER-CELL / PER-BEAM, shared (AST's "up to 120 Mbps per coverage cell across more than 2,000 cells"), but a lightly-loaded cell hands the whole beam to one phone, so **per-cell-when-alone equals the single-phone peak** [FACT; COMM-336, COMM-339]. Starlink's measured ~3.1 Mbps/beam is explicitly the single-user-when-alone bound; AST's BlueWalker 3 (~64 m^2) demonstrated up to ~21 Mbps to one phone [FACT; COMM-337, COMM-338].

Anchored on that BW3 datapoint, the chain to the founder's target:

- A ~50 m^2 array is only ~1.07 dB below the ~64 m^2 BW3 array in gain, so in aperture terms it is essentially the BW3 array [DERIVED; COMM-345].
- Dropping from BW3's ~513 km to ~350 to 400 km buys ~3.5 to 3.9 dB of path loss at useful elevations, which more than offsets the aperture shrink (~+2.4 to +2.8 dB net) [DERIVED; COMM-346].
- Rate then scales linearly with owned bandwidth (the Shannon B term): ~17 MHz at 3 bps/Hz, ~20 MHz at 2.5, or ~25 MHz at 2 reaches 50 Mbps to one phone, inside AST's own 40 MHz / 120 Mbps-per-cell envelope [DERIVED; COMM-344, COMM-347].

The decision-critical extension is downward to the FLAT Flatellite aperture: **a flat ~25 m^2 array at ~350 km on owned spectrum clears ~25 Mbps to a single lightly-loaded phone on its own** (25 Mbps needs only ~8 to 12 MHz; even 20 MHz at a conservative 2 bps/Hz reaches ~40 Mbps), because the ~4.08 dB aperture shrink versus BW3 is almost entirely erased by the low-orbit gain, leaving the flat array at near-parity with the BW3 link [DERIVED; COMM-375]. **So the fold is NOT required for the ~25 Mbps bar:** you keep the flat, no-deploy, many-per-launch stack, and folding to ~50 m^2 (which would cut to ~3/Neutron) is a margin-and-per-cell-capacity choice for the TOP of the band, not a requirement for ~25 Mbps [DERIVED; COMM-371, COMM-376]. Taking ~30 Mbps as a representative single-phone operating point sits comfortably inside this band at ~25 MHz of owned spectrum.

Low orbit also carries a structural product advantage independent of rate: a low-LEO DTC link spends only ~5 to 10 ms round-trip on the satellite hop, leaving the entire ITU-T G.114 "good" voice band (up to 150 ms one-way) free for codec/jitter/backhaul, so a satellite call feels like a normal mobile call; GEO burns ~240 to 280 ms (one uplink leg alone ~120 ms) and structurally cannot, the same Iridium-vs-Inmarsat contrast observed for decades [FACT for the thresholds; COMM-350, COMM-352].

### 1.5 The coverage result: one ~53-deg band covers ~95% of mobile demand

The coverage geography makes the constellation cheaper than it first appears. About 95% of the world's people live within +/-55 deg latitude (reconstructed ~96-97%; ~92-95% within +/-45 deg), and that is the SAME ~95% the ITU reports already lives inside a mobile-broadband footprint, so the populated band is the entire mobile-demand base [ESTIMATE for the band fractions, reconstructed; FACT for the ITU cross-check; COMM-386, COMM-390]. An inclined constellation covers a global latitude BAND (all longitudes within +/-i, as the Earth rotates under the fixed planes), not a region, so **"cover US + Europe latitudes" is geometrically identical to covering the ~53-deg mid-latitude band, getting Sao Paulo, Johannesburg, Mumbai, Shanghai, Jakarta, Sydney, and Buenos Aires at no additional satellite cost** [FACT/DERIVED; COMM-392, COMM-394]. Fly the primary shell at ~53 deg, the validated industry standard for the populated mid-latitudes (Starlink D2C and AST both 53.0, Globalstar 52, Kuiper top 51.9); to reach the Nordics/Alaska, add a 70 or ~97.6-deg shell rather than raising the base [FACT/DERIVED; COMM-395, COMM-400, COMM-401].

A 95%-of-population target is therefore a SINGLE inclined ~53-deg band sized to the streets-of-coverage floor, **on the order of ~100 to 340 satellites for the populated band** (the few-hundred-satellite US+Europe-equivalent floor of COMM-215/216, in the same band as Rocket Lab's own VP "150 to 200-satellite" 5G-NTN figure and validated against the Iridium 66->78 real-world count), with no polar shells, because covering the 53-deg band IS covering ~95% of people [DERIVED; COMM-404, COMM-405]. Chasing the last few percent and the empty high-latitude edges is what adds polar shells and the 2-4x multi-fold multiplier, so it should be an explicit, separately-priced scope decision, not a default.

---

## 2. The Biggest Still-Unresolved Numbers

Three numbers gate the architecture and are not yet pinned. The synthesis is honest that the operating point above rides on them.

1. **Per-satellite capacity (the largest gap).** Everything above sizes the single-phone RATE, which aperture plus owned spectrum set. It does NOT size per-satellite total CAPACITY (concurrent users, cells, aggregate Mbps), which is what determines how many satellites the demand actually needs and whether the constellation closes economically. The Flatellite's aperture area, power, beam count, and per-satellite throughput are all UNKNOWN (Rocket Lab publishes only "high-power"), so "more satellites per launch" (16 vs 1) does not yet translate to "more capacity per launch" [UNKNOWN; COMM-270, COMM-322 (model)]. Per-satellite power is the second EIRP term alongside aperture gain and is decisive for whether a ~25 to 50 m^2 array holds ~2 to 3 bps/Hz across a wide owned channel [UNKNOWN; COMM-348].

2. **Spectrum: lease vs own.** The single-phone rate is aperture AND owned bandwidth, so the ~25 to 50 Mbps target is unreachable on a thin ~5 to 10 MHz SCS-leased slice alone; it needs ~20 to 40 MHz of owned (or owned-equivalent) downlink [DERIVED; COMM-355, model spectrum gate COMM-325]. The corpus has the two ends priced: the FCC SCS partner/lease model nets spectrum to a near-wash, while OWNED mid-band runs ~$0.65 to 1.03/MHz-POP, i.e. ~$32 to 46B for 100 MHz US+Europe (COMM-241, COMM-245, wave 5). Which path the business takes is a tens-of-billions swing and is unresolved.

3. **Per-satellite cost.** The corpus has launch-cost-per-satellite (Flatellite at ~16/Neutron spreads a ~$50-55M Neutron launch over many satellites, far better than the ~$50-55M/sat a ~1/Neutron AST-class aperture loads) but NOT the Flatellite build cost, production rate, or unit economics; Rocket Lab has published no mass, no satellites-per-month, and no per-unit build time [UNKNOWN; COMM-268, COMM-256]. Without it the delivered cost per subscriber (the wave-3 gate) cannot be closed for a Flatellite-based DTC constellation.

A fourth, smaller caveat caps the Tier-1 confidence: the flat-25 verdict is an INFERENCE off a single flying datapoint (BW3) with two undisclosed quantities, the simultaneous device count and the test channel bandwidth. If BW3's ~21 Mbps was a multi-device aggregate, the flat ~25 m^2 case loses its comfortable margin and the ~50 m^2 fold becomes the prudent route to a firm ~25 Mbps [UNKNOWN, direction-stated; COMM-377, COMM-378].

---

## 3. Implications for the Direct-to-Cell Model

1. **The architecture is now specifiable end to end, at Tier 1.** A Neutron-launched DTC business that targets Tier-1 4G-grade service is: a flat ~20 to 25 m^2 Flatellite-class aperture (no fold), flown low (~350 to 450 km) at ~53 deg inclination, on ~20 to 40 MHz of owned (or owned-equivalent) spectrum, in a one-shell constellation of a few hundred satellites for ~95% of global mobile demand, delivering ~25 to 50 Mbps to a single lightly-loaded phone with a normal-feeling voice latency. Every element of that sentence is sourced above. The model can be populated at this shape.

2. **The service ambition, not the launcher, is the first decision.** The aperture ladder is also a launch-economics ladder: Neutron's 5.5 m fairing is comfortable on the Tier-1 rung (a flat aperture, many-per-launch) and binding on the Tier-2 broadband-to-phone rung (a ~223 m^2 folded aperture, ~1/launch where a Starship-class batch lifter out-scales it on $/satellite) [DERIVED; COMM-314]. The Rocket Lab path is Tier-1 DTC on a flat stack, not Tier-2 broadband-to-phone on a giant aperture.

3. **Coverage is cheap; capacity and spectrum are where the money is.** This is the wave-6 echo of the wave-5 finding (coverage is a few-hundred-satellite problem, the cost is in the spectrum). Wave 6 sharpens it: the few-hundred-satellite band also covers ~95% of demand, so the binding economic questions are per-satellite capacity (does the flat aperture carry enough users) and the spectrum lease-vs-own choice (a near-wash or a tens-of-billions capital line), not the satellite count.

4. **Low orbit is doing two jobs.** It buys the ~3.5 to 3.9 dB that lets the small flat aperture clear the Tier-1 rate, AND it delivers the latency that makes a phone product feel normal. Both are reasons to fly low that are independent of each other, and both belong to the LOW-flying entrant specifically (AST's own planned operational shell is ~725 to 740 km, higher, so the low-orbit advantage is the entrant's, not AST's) [FACT, refinement; COMM-354].

5. **No verdict.** This synthesis establishes the architecture and the settled Tier-1 operating point and names the three open numbers (per-satellite capacity, spectrum lease-vs-own, per-satellite cost). Whether a Neutron-launched DTC business closes depends on those three, the entrant-specific cost stack (still unmodeled, wave 3), and the demand sizing (wave 2), none decided here.

---

## 4. What the Governing Model Owns vs What This Synthesis Adds

The single source-of-truth for the DTC physics and the two-tier split is [`dtc_system_model.md`](../direct_communication/dtc_system_model.md) (the WIP governing model; COMM-315..335 + COMM-356..365), which fixes the four-lever relationship once so positions cannot drift between conversations. This synthesis does not replace it; it threads the five wave-6 source docs through that model into one narrative and adds three things the per-doc ledgers do not state together: the end-to-end Tier-1 operating point as a single specifiable shape (Section 1.4 + 3.1), the explicit naming of the three biggest open numbers as the binding economic gates (Section 2), and the coverage band tied to the demand base and the satellite-count floor (Section 1.5). When the governing model doc lands (after its pending flat-antenna correction, coverage result, and final review), this synthesis should be re-checked against it; the architecture here is expected to strengthen, not change, on that update.

---

## Sources

All numbers are carried from the five wave-6 source docs (cited inline by path and COMM-ID) and the WIP governing model; the underlying external citations live in those docs and in [`SOURCE_INDEX.md`](../SOURCE_INDEX.md) (COMM-249..405). This synthesis mints no new claim IDs. China is excluded from every market figure. No verdict.

- [`dtc_antenna_aperture_tradeoff.md`](../direct_communication/dtc_antenna_aperture_tradeoff.md) (COMM-293..314): the link budget and gain-placement asymmetry.
- [`flatellite_platform.md`](../rocket_lab/flatellite_platform.md) (COMM-249..270): the Flatellite flat-body aperture and per-Neutron count.
- [`starlink_v3_platform_and_starship.md`](../competitors/starlink_v3_platform_and_starship.md) (COMM-271..292): the V3 platform, why-Starship, and the Neutron-analog.
- [`dtc_per_phone_rate_and_latency.md`](../direct_communication/dtc_per_phone_rate_and_latency.md) (COMM-336..355 + COMM-371..378): the single-phone operating point and the latency advantage.
- [`dtc_coverage_geography.md`](../direct_communication/dtc_coverage_geography.md) (COMM-386..405): the population band, the latitude-band insight, and the 53-deg target.
- [`dtc_system_model.md`](../direct_communication/dtc_system_model.md) (COMM-315..335 + COMM-356..365): the WIP governing system model (not committed with this wave).
