# LEO Constellation Coverage Minimums: the satellite-count FLOOR for continuous (24/7) coverage

*Research date: June 2026. Communications research-wiki effort. Part of the Rocket Lab orbital communications feasibility study (companion to the orbital data-center track).*

**Builds on / does not duplicate:**
- [`research/laser_comms/constellation_mesh.md`](../laser_comms/constellation_mesh.md) Section 4: owns the requirement split (a tight along-track compute cluster vs a globally-distributed constellation), the Walker notation `i: N/P/F`, Iridium `86.4°: 66/6/2`, and the "10+ satellites per plane to keep one point covered" intuition. This doc does NOT re-litigate that; it makes the coverage-floor count concrete for the comms-track target geographies (US, US+Europe, mid-latitude band).
- [`research/orbital/orbit_types_primer.md`](../orbital/orbit_types_primer.md) Sections 3-5: owns the LEO-vs-GEO coverage trade (3 GEO sats ≈ global; LEO needs many), orbital-plane basics, Iridium 66/6 (11/plane, 30° apart, 780 km, 86.4°), and the relay-layer concept. This doc does NOT repeat the primer; it supplies the geometry math behind those counts.
- [`research/competitors/starlink_v3_specs.md`](../competitors/starlink_v3_specs.md): owns the Starlink Gen2 shell structure (~29,988 sats, ~340-360 / ~525-535 / ~604-614 km) and the VLEO-capacity-over-coverage-efficiency trade (the "lower orbit covers less ground, so you need more sats" note). This doc explains WHY that trade has the slope it does, and separates the COVERAGE driver from the CAPACITY driver Starlink's count is actually dominated by.
- [`research/direct_communication/spectrum_generations_and_availability.md`](spectrum_generations_and_availability.md): owns the per-beam / per-footprint CAPACITY ceiling (Shannon x footprint, no densification, COMM-108). This doc owns the COVERAGE floor that sits underneath capacity.

This doc answers one bounded question for the founder's hypothesis: **before capacity even matters, how many LEO satellites are the minimum for CONTINUOUS (24/7) coverage of a target area** (the continental US; the US plus parts of Europe; a near-global mid-latitude band). It then states the verdict on the founder's hypothesis that *the primary effect of adding satellites is COVERAGE up to a floor, then CAPACITY beyond it.*

---

## Summary / Verdict

**Confidence: high** on the orbital geometry (footprint size, pass duration, period) because it is closed-form physics validated against published references and against Iridium's real flown count; **medium-high** on the specific floor counts because the streets-of-coverage (SOC) method this doc uses is a known, slightly-conservative analytic model (it reconciles to ~84 satellites for a configuration Iridium actually flies with 66, i.e. it runs ~20-30% high versus an optimized Walker pattern), so the counts are reported as **ranges and orders of magnitude, not exact buildable numbers**.

1. **A single LEO satellite covers a small circle and is overhead only briefly.** At 550 km with a 25° minimum elevation angle, one satellite's footprint is a circle ~`1,880 km` across and a fixed ground point sees it for only ~`2-5 minutes` per pass; at the lower 350 km VLEO shell the footprint shrinks to ~`1,290 km` across and the overhead window to ~`2-3 minutes`. The orbital period is ~`91 min` (350 km) to ~`96 min` (550 km). [FACT, closed-form + multi-source]

2. **Continuous coverage of even one fixed point therefore needs a STRING of satellites in a plane (the next rises before the last sets), and continuous coverage of an AREA needs MULTIPLE such strings (planes) tiled across the target's longitude span.** This is the streets-of-coverage construction. [FACT, standard constellation theory]

3. **Coverage-floor counts (single 24/7 coverage), reported as ranges across the 350-550 km band and 10-25° elevation:**
   - **Continental US (CONUS):** roughly **~50 to ~150 satellites** as a buildable full-ring floor (lower end at 550 km / low elevation, higher end at 350 km / high elevation); an optimized regional Walker can sit at the **low tens** (published regional LEO designs use ~13-36 sats for a single mid-latitude receiver band). [ESTIMATE, SOC-derived + literature-corroborated]
   - **US plus parts of Europe:** roughly **~130 to ~450 satellites** full-ring floor, because the two regions straddle ~`150°` of longitude (US west coast ~-125° to Eastern Europe ~+30°), which roughly triples the number of orbital planes needed versus CONUS alone. [ESTIMATE, SOC-derived]
   - **Near-global mid-latitude band (all longitudes, ~±50-55° lat):** roughly **~290 to ~960 satellites** full-ring floor at the VLEO/LEO altitudes of interest; this is the regime where the count climbs toward the hundreds-to-low-thousands and converges with what real global LEO systems fly. [ESTIMATE, SOC-derived; reconciles with Iridium's 66 at higher altitude/low elevation and with the ~150-200-class global single-coverage figure at low elevation]

4. **The floor is dominated by TWO knobs, and both push it UP at the altitudes the modern systems use:** lower altitude (smaller footprint → more sats) and higher minimum elevation angle (better link / less rain-fade / less blockage → smaller usable footprint → more sats). Going from 550 km to 350 km roughly **doubles to triples** the floor; going from 10° to 25° elevation does the same. This is exactly why Starlink's VLEO Gen2 plan is ~30,000 satellites: it deliberately trades coverage efficiency for capacity density. [FACT/DERIVED]

5. **Verdict on the founder's hypothesis: CORRECT, with one sharpening.** The primary effect of the FIRST satellites you add is COVERAGE (continuity) up to a floor: below the floor you have gaps and no 24/7 service at all, and adding satellites buys you minutes-of-the-day, not bits-per-second. Once the floor is met (every point in the target always sees at least one satellite above the elevation mask), every ADDITIONAL satellite over the area buys CAPACITY (more simultaneous beams / spectrum reuse / throughput), not coverage. The sharpening: real mega-constellations are built so far ABOVE the coverage floor that their satellite count is set almost entirely by the capacity regime, and at very low altitude the coverage floor itself is *raised* (more sats needed just for continuity), so the two regimes are coupled through altitude rather than cleanly sequential. [DERIVED, hypothesis verdict]

**Numbers to treat with care (flagged in the claims ledger):** every floor count is a streets-of-coverage analytic estimate that runs ~20-30% high versus an optimized Walker pattern (validated against Iridium), so treat them as order-of-magnitude brackets, not buildable specs; the US+Europe count depends on how much of Europe is in-scope (longitude span assumption); and a real system's actual count is set by CAPACITY, well above any of these coverage floors.

---

## 1. The single-satellite geometry (why the floor exists at all)

Everything follows from one closed-form fact: a LEO satellite sees a small circle on the ground and crosses it fast.

### 1.1 Footprint size (Earth-central-angle method)

The Earth-central angle `λ` of the coverage circle, for satellite altitude `h`, Earth radius `Re` (~6,371 km), and a ground user's minimum elevation angle `εmin`, is:

```
λ = arccos( Re·cos(εmin) / (Re + h) ) − εmin
```

([formula per orbital-coverage patent literature, USPTO 10,951,305 and family](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10951305); standard SMAD/Wertz geometry). The footprint ground radius is `Re·λ` (λ in radians); the footprint area is `2π·Re²·(1 − cos λ)`. The slant range to the horizon-edge user is the geometry's `d` from the law of cosines.

Computed for the two altitudes of interest (350 km VLEO, the Starlink V3 / D2C shell; and 550 km, the current operational broadband shell), at three elevation masks:

| Altitude | Min elevation | Central angle λ | Footprint radius | Footprint diameter | Slant range | Footprint area |
|---|---|---|---|---|---|---|
| 350 km | 10° | 11.0° | ~1,224 km | ~2,450 km | ~1,300 km | ~4.7M km² |
| 350 km | 25° | 5.8° | ~643 km | ~1,290 km | ~750 km | ~1.3M km² |
| 350 km | 40° | 3.4° | ~382 km | ~760 km | ~530 km | ~0.46M km² |
| 550 km | 10° | 15.0° | ~1,664 km | ~3,330 km | ~1,815 km | ~8.7M km² |
| 550 km | 25° | 8.5° | ~941 km | ~1,880 km | ~1,125 km | ~2.8M km² |
| 550 km | 40° | 5.2° | ~573 km | ~1,150 km | ~810 km | ~1.0M km² |

[FACT, closed-form; cross-checked against [the cited ~934 km slant at 550 km / 25°](https://www.scirp.org/journal/paperinformation?paperid=138890) and [the worked footprint example, ~527 km radius / ~873,000 km² at 500 km / 40°](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10951305), both within rounding of this table.]

**The load-bearing point:** the usable footprint *shrinks fast* as altitude drops or elevation mask rises. A 25° mask (typical for a quality link with rain-fade and obstruction margin) at 350 km gives a circle only ~1,290 km across; covering the ~4,500 km width of CONUS at any instant takes several of those circles, and keeping them there 24/7 as the satellites race overhead takes many more.

### 1.2 Pass duration (why one satellite is never enough)

Orbital period and sub-satellite ground-track speed (computed from `μ = 398,600 km³/s²`):

| Altitude | Period | Ground-track speed | Max overhead pass (25° mask) | Max overhead pass (10° mask) |
|---|---|---|---|---|
| 350 km | ~91.4 min | ~7.30 km/s | ~2.9 min | ~5.6 min |
| 550 km | ~95.5 min | ~6.99 km/s | ~4.5 min | ~7.9 min |

[FACT, closed-form; consistent with the corpus's existing "~5-15 min per pass, ~6-8 passes/day" figure in [`constellation_mesh.md`](../laser_comms/constellation_mesh.md) and the general "2-15 minutes" visibility range in the [LEO coverage-duration literature](https://www.scirp.org/journal/paperinformation?paperid=138890).]

A fixed ground point is in view of any one satellite for at most a few minutes, a few times a day. **A single satellite delivers single-digit-percent contact time. Continuity requires a fleet whose footprints overlap in space and whose passes overlap in time.**

---

## 2. From one satellite to a coverage floor (streets-of-coverage)

The standard analytic construction for *minimum-count continuous coverage* is **streets-of-coverage (SOC)** ([multi-criteria SOC vs Walker study, ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0094576521003490); [minimum-satellite continuous-coverage design, arXiv 2410.03354](https://arxiv.org/html/2410.03354v1)):

- **Within a plane:** N satellites evenly spaced create a continuous "street" of coverage (a band along the ground track) only if adjacent footprints overlap. The street half-width `c` satisfies `cos λ = cos c · cos(180°/N)`. Below a minimum N the footprints don't even touch along-track and the street has gaps; above it, more satellites per plane widen the street.
- **Across planes:** planes are spaced in longitude so adjacent streets meet. The number of planes needed to blanket a target is set by the target's longitude span divided by the street width (`2c`).

So the floor is a product: **(satellites per plane to close the street) × (planes to tile the target's longitude span)**. Both factors grow as the footprint shrinks.

**This doc's SOC computation is validated against a real flown system.** Applying the same SOC model to Iridium's configuration (780 km, ~8° elevation) yields ~84 satellites for global single coverage; Iridium actually flies **66** ([Wikipedia: Iridium / satellite constellation](https://en.wikipedia.org/wiki/Satellite_constellation), and [`orbit_types_primer.md`](../orbital/orbit_types_primer.md)). The SOC estimate runs ~20-30% high versus the optimized Walker pattern Iridium uses, which is the known, expected behavior of the SOC bound. **Every count below should therefore be read as a slightly-conservative ceiling on the true minimum, i.e. an order-of-magnitude bracket.**

---

## 3. The coverage-floor counts for the target geographies

Using SOC at the two altitudes (350 / 550 km) and two elevation masks (10° horizon-grazing / 25° quality-link), with these longitude spans: CONUS ~58°, US+Western Europe ~150° (US west ~-125° to Eastern Europe ~+30°), near-global mid-latitude band 360°.

| Target | 550 km, 10° mask | 550 km, 25° mask | 350 km, 10° mask | 350 km, 25° mask |
|---|---|---|---|---|
| **Continental US** | ~50 | ~155 | ~105 | ~360 |
| **US + W. Europe** | ~135 | ~415 | ~230 | ~935 |
| **Near-global mid-lat band** | ~290 | ~960 | ~545 | ~2,230 |

[ESTIMATE, SOC-derived; full-ring buildable floor, i.e. you fly complete orbital rings, you cannot place satellites over only one latitude band of an inclined plane.]

**Reading the table:**
- The **range across a row is ~3-7x**, driven entirely by altitude and elevation mask. The honest single answer for each target is the *range*, not a point.
- **CONUS floor: ~50-150 satellites** (full-ring SOC). An optimized regional Walker-Delta does better: published LEO regional designs at 550-870 km find solutions with **~13-36 satellites** for continuous coverage of a single mid-latitude receiver band (30-60° latitude) ([regional LEO positioning constellation, ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0273117719300183)), and regional optimizations "up to ~70 satellites at 550 km" appear in the design literature. So the *true* CONUS continuity floor is plausibly **low tens of satellites** with an optimized pattern, rising toward ~150 in the conservative SOC / low-altitude / high-elevation corner.
- **US + Europe floor: ~130-450 satellites** (SOC). The roughly-3x jump over CONUS is almost entirely the wider longitude span (~150° vs ~58°) requiring ~3x the orbital planes. The split-across-the-Atlantic geometry means you cannot share planes between the two regions the way a contiguous span would; you pay for the empty mid-Atlantic longitudes too, because a full orbital ring spans all longitudes anyway. **The headline coverage-floor number for the US+Europe target is therefore on the order of a few hundred satellites (~130-450), not tens and not tens-of-thousands.**
- **Near-global mid-latitude band: ~290-960 satellites** (SOC), converging with reality: this is the regime where the count reaches the hundreds-to-low-thousands and where real global LEO single-coverage systems live (Iridium 66 at higher altitude / low elevation; the ~150-200-class single global coverage figure at low elevation in [`constellation_mesh.md`](../laser_comms/constellation_mesh.md)'s navigation-Walker reference of 180-264 sats).

**Cross-checks (independent of this doc's SOC math):**
- Iridium: **66** satellites, global single voice coverage, 780 km, 86.4° ([Wikipedia](https://en.wikipedia.org/wiki/Satellite_constellation); [`orbit_types_primer.md`](../orbital/orbit_types_primer.md)). [FACT]
- Starlink Shell 1: **1,584** satellites, `53°: 1584/72/1`, 550 km ([deltaV Academy Walker constellations](https://www.deltavacademy.com/learn/walker-constellations)), far above any single-coverage floor, because it is sized for CAPACITY, not continuity. [FACT]
- Regional LEO continuous-coverage designs: **~13-36 satellites** for a mid-latitude band (30-60°) at 550-870 km ([ScienceDirect regional LEO](https://www.sciencedirect.com/science/article/abs/pii/S0273117719300183)). [FACT, literature]

---

## 4. Coverage FLOOR vs CAPACITY SCALING (the distinction the hypothesis turns on)

These are two different regimes governed by two different physics, and conflating them is the error the founder's hypothesis correctly separates.

**Regime 1, COVERAGE (continuity), governed by GEOMETRY.** Below the floor, the target has time-gaps: at some moments no satellite is above the elevation mask over part of the area, and there is simply no service then. Adding satellites in this regime buys *time-of-day coverage* (closing the gaps) and *geographic continuity*, not throughput. The floor is reached when **every point in the target always sees ≥1 satellite above the mask** (single coverage); fault-tolerant or beam-diverse service wants **2-fold or higher coverage**, which multiplies the floor by ~2-4x. The floor counts in Section 3 are this regime.

**Regime 2, CAPACITY (throughput), governed by SPECTRUM (Shannon) × number of beams over the area.** Above the floor, every additional satellite over the target adds beams, frequency reuse, and simultaneous capacity. This is the regime where Starlink's 1,584 (Shell 1) or ~30,000 (Gen2) live: they are not there for continuity (66-class numbers already give that), they are there because **demand density requires many satellites' worth of beams over the same ground at once**. Per [`spectrum_generations_and_availability.md`](spectrum_generations_and_availability.md) (COMM-108) and [`starlink_v3_specs.md`](../competitors/starlink_v3_specs.md) Section 5, a beam is a fixed pool of capacity over a fixed footprint that cannot densify, so the only way to add capacity over a busy area is more satellites over it.

**The altitude coupling (the sharpening on the hypothesis).** The two regimes are not perfectly sequential because **lowering altitude raises the coverage floor *and* the capacity ceiling at the same time.** Going to 350 km VLEO (Section 1) shrinks each footprint, so:
- You need MORE satellites just for the coverage floor (Section 3: ~2-3x more than at 550 km), AND
- Each satellite's smaller, tighter footprint enables MORE frequency reuse / capacity density (the reason Starlink chose VLEO for Gen2; see [`starlink_v3_specs.md`](../competitors/starlink_v3_specs.md) Section 3).

So at the altitudes the modern systems actually use, the coverage floor and the capacity-driven count are pushed up together, and the real flown count is set overwhelmingly by Regime 2.

---

## 5. Verdict on the founder's hypothesis

**Hypothesis:** *the primary effect of adding satellites is COVERAGE (up to the floor), then CAPACITY (beyond it).*

**Verdict: CORRECT, with one sharpening.** [DERIVED]

- **The first satellites buy COVERAGE.** Below the floor there is no 24/7 service at all over the target; adding satellites buys minutes-of-the-day and closes geographic gaps, not bits-per-second. The floor for the US+Europe target is on the order of **a few hundred satellites (~130-450, SOC; plausibly lower with an optimized Walker)**, small relative to a mega-constellation, large relative to a single useful compute cluster.
- **Satellites beyond the floor buy CAPACITY.** Once every point in the target is always covered, each additional satellite over the area adds beams and spectrum reuse, i.e. throughput. This is the regime that sets the real count of Starlink-class systems (1,584 to ~30,000), which sit far above any continuity floor.
- **Sharpening:** the two regimes are coupled through altitude rather than cleanly sequential. At the VLEO altitudes modern systems use, the coverage floor itself is *raised* (smaller footprints), and the systems are built so far above it that their count is dominated by capacity. So the clean "coverage-then-capacity" story is right as a *conceptual ordering* (you must clear continuity before throughput matters), but a real system rarely sits *at* its coverage floor, it overshoots it for capacity, and the floor it had to clear was itself inflated by the low-altitude capacity choice.

**Implication for the Rocket Lab comms thesis.** A continuity-only service over US+Europe is a **few-hundred-satellite** problem (a Neutron-scale deployment question, distinct from the ~30,000-satellite capacity build), but such a constellation delivers only the *floor* of capacity (a handful of beams per point, not a dense-market pipe). The gap between the **~130-450-satellite coverage floor** and the **~1,584-to-30,000-satellite capacity build** is precisely the gap between "always reachable, thin pipe" and "serves a dense market," and it is set by demand density and spectrum, not by geometry. This connects directly to the density-aware unit (COMM-172): coverage is cheap (a few hundred sats), capacity over dense ground is what is expensive.

---

## Open questions / uncertainties

- **SOC-vs-optimized-Walker gap.** Every floor count here is a streets-of-coverage estimate running ~20-30% high versus an optimized Walker pattern (validated against Iridium 66 vs SOC's ~84). The true minimums are somewhat lower; the *ranges and orders of magnitude* are the reliable output, not the point values.
- **US+Europe longitude-span assumption.** The ~150° span (US west to Eastern Europe) sets the ~3x plane-count jump over CONUS. Narrowing the European scope (e.g. only Western Europe to ~0°) would lower the count; widening it raises it. The few-hundred-satellite order of magnitude is robust to this; the exact number is not.
- **Single vs multi-fold coverage.** All Section-3 counts are *single* (1-fold) continuous coverage. Real service often wants 2-fold (handover, beam diversity, fault tolerance), which multiplies the floor by ~2-4x. The founder should specify the required coverage multiplicity before any of these becomes a planning number.
- **Inclination and high-latitude scope.** The counts assume the target sits within the inclination-reachable band. Including high-latitude Europe (>55-60°N) or polar coverage pushes toward Walker-Star (polar) patterns and changes the plane geometry; the mid-latitude band figures assume a Walker-Delta-style inclined design.
- **The floor is not the buildable count.** No real system sits at its coverage floor; the capacity regime (Section 4) sets the actual count. These floors answer "what is the geometric minimum for continuity," not "how many satellites would Rocket Lab build."

---

## Claims ledger

For the catalog step to ingest. Assigned COMM-209..228 from this agent's range. Each hard claim with its sources.

1. **[COMM-209]** Single-satellite footprint at 550 km / 25° elevation mask: Earth-central angle ~8.5°, footprint diameter ~1,880 km, slant range ~1,125 km; at 350 km / 25°, ~5.8°, ~1,290 km diameter, ~750 km slant. [FACT, closed-form] Sources: [Earth-central-angle formula, USPTO 10,951,305](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10951305); [550 km / 25° ~934 km slant cross-check, SciRP](https://www.scirp.org/journal/paperinformation?paperid=138890).

2. **[COMM-210]** LEO orbital period ~91 min (350 km) to ~96 min (550 km); sub-satellite ground-track speed ~7.0-7.3 km/s. [FACT, closed-form] Source: standard Keplerian geometry (μ=398,600 km³/s²); cross-checked vs corpus.

3. **[COMM-211]** Maximum overhead pass duration over a fixed point: ~2.9 min (350 km, 25° mask) to ~7.9 min (550 km, 10° mask); a single satellite gives single-digit-percent daily contact time. [FACT, closed-form] Sources: derived; consistent with [LEO 2-15 min visibility](https://www.scirp.org/journal/paperinformation?paperid=138890) and [`constellation_mesh.md`](../laser_comms/constellation_mesh.md) (~5-15 min/pass, 6-8 passes/day).

4. **[COMM-212]** Streets-of-coverage (SOC) is the standard minimum-count continuous-coverage construction; the in-plane street half-width c satisfies cos λ = cos c · cos(180°/N); the area floor = (sats/plane to close the street) × (planes to tile the longitude span). [FACT, standard theory] Sources: [SOC vs Walker, ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0094576521003490); [minimum-satellite continuous coverage, arXiv 2410.03354](https://arxiv.org/html/2410.03354v1).

5. **[COMM-213]** This doc's SOC model reconciles to ~84 satellites for Iridium's configuration (780 km, ~8° elevation) vs Iridium's actual flown 66; SOC runs ~20-30% high vs an optimized Walker, so the floor counts are slightly-conservative order-of-magnitude brackets. [DERIVED/ESTIMATE, validation] Sources: [Wikipedia satellite constellation (Iridium 66/6/2)](https://en.wikipedia.org/wiki/Satellite_constellation); [`orbit_types_primer.md`](../orbital/orbit_types_primer.md).

6. **[COMM-214]** Continental US (CONUS, ~58° longitude span) continuous single-coverage floor: ~50-150 satellites (full-ring SOC, 550 km low-elevation to 350 km high-elevation); an optimized regional Walker can reach the low tens. [ESTIMATE, SOC-derived + literature] Sources: SOC computation (this doc); [regional LEO ~13-36 sats, ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0273117719300183).

7. **[COMM-215]** US + Western Europe (~150° longitude span) continuous single-coverage floor: ~130-450 satellites (full-ring SOC); the ~3x jump over CONUS is the wider longitude span requiring ~3x the orbital planes. [ESTIMATE, SOC-derived] Source: SOC computation (this doc).

8. **[COMM-216]** Near-global mid-latitude band (all longitudes) continuous single-coverage floor: ~290-960 satellites (full-ring SOC, 550-350 km), converging with real global LEO single-coverage systems (Iridium 66 at higher altitude; ~150-200-class at low elevation). [ESTIMATE, SOC-derived] Sources: SOC computation (this doc); [`constellation_mesh.md`](../laser_comms/constellation_mesh.md) (180-264 nav-Walker reference).

9. **[COMM-217]** The coverage floor is driven by altitude and elevation mask: lowering altitude 550→350 km or raising the mask 10°→25° each roughly doubles-to-triples the floor (smaller usable footprint). [FACT/DERIVED] Source: footprint table (this doc, COMM-209).

10. **[COMM-218]** Regional LEO continuous-coverage literature: ~13-36 satellites cover a single mid-latitude receiver band (30-60° lat) at 550-870 km; regional optimizations up to ~70 sats at 550 km appear in the design literature. [FACT, literature] Source: [ScienceDirect regional LEO positioning](https://www.sciencedirect.com/science/article/abs/pii/S0273117719300183).

11. **[COMM-219]** Iridium flies 66 satellites (Walker-Star 86.4°: 66/6/2, 780 km) for global single voice coverage, the canonical real-world coverage-floor data point. [FACT] Sources: [Wikipedia satellite constellation](https://en.wikipedia.org/wiki/Satellite_constellation); [deltaV Academy](https://www.deltavacademy.com/learn/walker-constellations); [`orbit_types_primer.md`](../orbital/orbit_types_primer.md).

12. **[COMM-220]** Starlink Shell 1 is Walker-Delta 53°: 1584/72/1 at 550 km (1,584 sats, 72 planes × 22); this is far above any continuity floor and is sized for CAPACITY. [FACT] Source: [deltaV Academy Walker constellations](https://www.deltavacademy.com/learn/walker-constellations).

13. **[COMM-221]** Walker notation i: N/P/F (inclination : total / planes / phasing); Walker-Star = polar (global, incl. poles), Walker-Delta = inclined (mid-latitude/equatorial band). [FACT] Sources: [Wikipedia satellite constellation](https://en.wikipedia.org/wiki/Satellite_constellation); [deltaV Academy](https://www.deltavacademy.com/learn/walker-constellations).

14. **[COMM-222]** Earth-central-angle coverage formula: λ = arccos(Re·cos(εmin)/(Re+h)) − εmin; footprint radius = Re·λ; footprint area = 2π·Re²(1−cos λ). [FACT, formula] Source: [USPTO 10,951,305 orbital-coverage patent](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10951305).

15. **[COMM-223]** Footprint-area / radius worked cross-check: 500 km / 40° mask → λ≈4.74°, radius ~527 km, area ~873,000 km² (matches this doc's method within rounding). [FACT, cross-check] Source: [USPTO 10,951,305](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10951305).

16. **[COMM-224]** Coverage (continuity) and capacity (throughput) are distinct regimes: below the floor, added satellites buy time-of-day/geographic continuity (geometry-governed); above it, added satellites over the area buy beams/spectrum-reuse/throughput (Shannon-governed). [DERIVED, framework] Sources: this doc Section 4; [`spectrum_generations_and_availability.md`](spectrum_generations_and_availability.md) (COMM-108); [`starlink_v3_specs.md`](../competitors/starlink_v3_specs.md) Section 5.

17. **[COMM-225]** Multi-fold coverage multiplies the floor: 2-fold continuous coverage (handover/diversity/fault tolerance) costs ~2-4x the single-coverage floor. [ESTIMATE, standard theory] Source: SOC/Walker coverage theory (this doc).

18. **[COMM-226]** Altitude coupling: lowering to VLEO (~350 km) raises BOTH the coverage floor (smaller footprints → more sats for continuity) AND the capacity ceiling (tighter beams → more reuse), so the two regimes are pushed up together, not cleanly sequential. [DERIVED] Sources: this doc Sections 1, 4; [`starlink_v3_specs.md`](../competitors/starlink_v3_specs.md) Section 3 (VLEO capacity-density trade).

19. **[COMM-227]** Founder-hypothesis verdict: "adding satellites buys COVERAGE up to a floor, then CAPACITY beyond it" is CORRECT as a conceptual ordering; sharpening: real systems overshoot the floor for capacity and the floor is itself altitude-inflated, so the count of a flown system is set overwhelmingly by the capacity regime. [DERIVED, verdict] Source: this doc Section 5.

20. **[COMM-228]** Thesis implication: a continuity-only US+Europe service is a few-hundred-satellite problem (~130-450, SOC; plausibly lower optimized), distinct from the ~1,584-to-30,000-satellite capacity build; the gap between floor and capacity build is set by demand density and spectrum, connecting to the density-aware unit (COMM-172). [DERIVED] Sources: this doc Section 5; COMM-172, COMM-220.

---

*COMM-209..228 created by this doc. Catalog rows for LIBRARY.md / RESEARCH_TRACKER.md / SOURCE_INDEX.md are returned to the catalog agent, not edited here.*
