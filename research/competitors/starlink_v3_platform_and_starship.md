# Starlink V3 (Gen3): The Platform, Antenna, Mass, and Why It Requires Starship

**Research date:** 2026-06-22
**Purpose:** Pin the Starlink V3 (Gen3) satellite as a physical *platform*, to ground a Neutron-launched space communications business. Specifically: mass, stowed and deployed dimensions, the phased-array antenna, per-satellite capacity, the direct-to-cell payload and its capability vs V2 Mini, and the load-bearing question, **why is V3 launched on Starship and not Falcon 9**, with the crucial implication: does a V3-class satellite physically fit a ~5 to 5.5 m Neutron fairing, or is it sized for Starship's ~8 to 9 m fairing?
**Status:** Understanding-building input. No go/no-go verdict. China excluded from all benchmarks.

> **Grounds in and does NOT duplicate (companion docs own these layers):**
> - [`research/competitors/starlink_v3_specs.md`](starlink_v3_specs.md): owns the V3 cost-and-capacity benchmark stack (per-satellite ~1 Tbps down / ~160-200 Gbps up, the broadband Gen2 + dedicated direct-to-cell fleets). This doc takes the capacity numbers as confirmation anchors and focuses on the **platform** (mass, antenna size, dimensions, why-Starship, D2C aperture).
> - [`research/competitors/starlink_v3_v4_spectrum_incorporation.md`](starlink_v3_v4_spectrum_incorporation.md): owns the **spectrum-quantity** stack (how many MHz/GHz per band, Ku/Ka/V/E/W, the ~65 MHz EchoStar D2C block). This doc does NOT re-cover spectrum; it references it where the D2C capability depends on it.
> - [`research/competitors/large_array_folding_and_stow.md`](large_array_folding_and_stow.md): owns the fold/stow *mechanics* (V3 broadband aperture barely folds; D2C arrays are many-fold accordions). This doc takes those mechanics as given and adds the platform context.
> - [`research/rocket_lab/neutron/neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md): owns the per-launch fit arithmetic (V3 mass-bound ~5/Neutron; the launch-cost-per-satellite chain). This doc supplies the **why-Starship-not-Falcon-9** reasoning and the fairing-fit conclusion that doc's V3 row relies on.

---

## 0. Answer first (the founder's six questions)

1. **Mass and antenna.** A V3 masses **~1,760 to 2,000 kg (working figure ~1,900 kg)**, roughly **3x a V2 Mini**, and is a flat ~7 m slab that unfolds to a **~60 m deployed wingspan** (solar-dominated) [FACT, multi-source]. Its broadband phased array is a **fully-digital phased array** (Ku/Ka, with E-band backhaul), but SpaceX has **not published the broadband aperture area in m^2**; the ~25 m^2 deployable-antenna figure that circulates is the **direct-to-cell** aperture (carried over from the V2 Mini D2C design), not a disclosed V3 *broadband* aperture [FACT for the D2C ~25 m^2; UNKNOWN for the broadband aperture area].

2. **Direct-to-cell on V3.** V3 (Gen3) is the platform for a **dedicated up-to-15,000-satellite direct-to-cell constellation** (FCC SAT-LOA-20250916-00282, filed Sep 16 2025), targeting **4G-LTE-equivalent service (text + voice + data, up to ~100 Mbps peak, ~2 to 10 Mbps sustained) to unmodified phones**, a large step up from the **V2 Mini D2C** capability (commercially texting + low-rate data at hundreds of kbps, with voice only entering beta in late 2025) [FACT, multi-source]. The D2C antenna is the giant deployable phased array (~25 m^2-class on V2 Mini), the part that is large, not the broadband aperture.

3. **Why Starship, not Falcon 9 (the load-bearing answer).** V3 is launched on Starship because **it is too large and too heavy for Falcon 9's 5.2 m fairing**: a ~7 m-long, ~1,900 kg V3 slab does not fit and stack inside Falcon 9 the way the deliberately *downsized* V2 Mini does. Starship offers a **9 m fairing (8 m payload envelope) and ~100 t to LEO**, into which **~54 to 100 V3 (commonly cited ~60) load per launch** versus ~21 to 24 V2 Mini on a Falcon 9 [FACT, multi-source]. The reason is **both** mass (3x V2 Mini) **and** physical size (the ~7 m slab exceeds the 5.2 m Falcon 9 fairing), with the size being the qualitative reason it cannot fly on Falcon 9 at all.

4. **Does a V3-class sat fit a ~5 to 5.5 m Neutron fairing?** **A bare V3 slab physically fits, but V3 is sized for Starship's ~8 to 9 m fairing, not for a 5 m one.** The ~7 m long x ~3.5 m wide flat body lies inside Neutron's ~5.5 m diameter x ~14 m fairing and, being flat, stacks, so unlike Falcon 9 the *shape* gate does not categorically exclude it. The binding limit on Neutron is **mass** (~1,900 kg each against ~9,500 kg reusable-to-SSO -> ~5/launch), exactly as [`neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md) finds. So: a V3-class broadband slab is **Neutron-carriable (mass-bound, ~5/launch), but Neutron carries ~1/12 of a Starship's V3 batch**, and the V3 is dimensioned for the Starship bay, not the Neutron one.

5. **V2 Mini comparison.** ~**575 to 800 kg** (early units ~800 kg, optimized ~525 to 575 kg), ~**4.1 m x 2.7 m** body, a **more powerful phased array** plus a ~**25 m^2 deployable D2C antenna** on the D2C variant, **~96 Gbps down / ~6.7 Gbps up**, and **~21 to 24 per Falcon 9** (record 24) [FACT, multi-source]. V2 Mini was *deliberately downsized* to fit Falcon 9 while Starship was delayed; V3 is the full-size design that drops that constraint.

6. **Implication for Neutron (analysis, flagged).** **Rocket Lab's Flatellite is the natural Neutron-sized analog of a V3-style flat-pack broadband/D2C satellite**: a low-profile, **stackable** flat satellite, **up to 16 per Neutron**, **~800 kg-class** (estimate), with optical crosslinks, aimed at large constellations. A "V3-class but Neutron-sized" satellite is therefore not a shrunk-V3-with-a-25 m^2-antenna; it is a **smaller, lighter flat-pack stacked many-per-launch** (the Flatellite concept), trading per-satellite capacity for stackability inside Neutron's smaller fairing. [ANALYSIS, flagged; Flatellite mass is an estimate, not disclosed.]

The rest sources and qualifies each of these.

---

## 1. The V3 platform: mass and dimensions

### 1.1 Mass

| Source | V3 mass stated | Tag |
|---|---|---|
| NextBigFuture (Feb 2025) | "**about 1900 kg**" (vs V2 Mini 575 kg) | [FACT] |
| RV Mobile Internet Resource Center | "**approximately 1900 kg** vs. 575 kg" for V2 Mini | [FACT] |
| Internet In Space | "**1,760 kg** per satellite" | [FACT] |
| Grokipedia / Basenor / multiple secondaries | "**up to ~2,000 kg** each" (rounded upper cite) | [FACT] |
| Basenor ("what the specs mean") | "approximately **2,000 kg** each... **more than three times the mass of a V2 Mini**" | [FACT] |

**Working figure: ~1,900 kg per V3**, with a sourced band of **~1,760 to 2,000 kg**. The ~1,760 figure (Internet In Space) and the ~1,900 figure (NextBigFuture, RV Mobile) are the lower, more specific cites; ~2,000 kg is the rounded upper. All agree V3 is **~3x a V2 Mini**. [FACT, multi-source] (This matches the ~1,900 kg working figure already carried in [`neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md) and [`starlink_v3_specs.md`](starlink_v3_specs.md).)

### 1.2 Dimensions: a ~7 m flat slab that unfolds to ~60 m

| Dimension | Value | Tag | Sources |
|---|---|---|---|
| Stowed long axis (length) | **~7 m** (Gen2/V3 body listed ~7 m x 3.5 m) | [FACT, single-source-class] | Gunter's Space Page; Internet In Space ("~7 meters long") |
| Stowed form | **flat panel, dense-stacked** in the Starship bay, deployed one at a time (PEZ dispenser) | [FACT, multi-source] | Via Satellite (Starship payload test); NextBigFuture |
| Deployed wingspan | **~60 m**, unfolded from a **7 to 8 m base** | [FACT, multi-source] | NextBigFuture ("60 m wingspan... 7-8 m base"); Tom's Hardware |
| Deployed-span character | dominated by **dual solar arrays** ("larger antennas and solar panels"; "nearly as wide as the ISS") | [FACT, multi-source] | NextBigFuture (Gen3-vs-ISS); Grokipedia (dual solar arrays longer than prior gens) |

**The structural point (carried from [`large_array_folding_and_stow.md`](large_array_folding_and_stow.md)):** the ~60 m "wingspan" is **solar-wing-dominated**, not RF-aperture-dominated. The broadband phased-array aperture is essentially the **flat ~7 m x ~3.5 m body itself**, which flat-packs and stacks; what unfolds to ~60 m is mostly the solar array. This is why V3 stows dense for Starship and is mass-bound (not size-bound) on any reasonable fairing. [FACT/DERIVED]

### 1.3 The broadband phased-array antenna (size: partly UNKNOWN)

- V3 uses a **fully-digital phased array with dynamic beamforming** (a step beyond the partly-analog earlier design), optimized for **Ku/Ka** user/feeder bands with **E-band backhaul** [FACT, multi-source: Grokipedia; Basenor 10x].
- **The broadband aperture area in m^2 is NOT publicly disclosed by SpaceX.** The "**~25 m^2** deployable antenna" figure that circulates in V3 write-ups is the **direct-to-cell** aperture (the same ~25 m^2-class deployable array introduced on the V2 Mini D2C variant), not a stated V3 *broadband* aperture. Treat the broadband aperture as "approximately the flat satellite body" (per the fold doc), **not** as a published 25 m^2 number. [UNKNOWN for broadband aperture m^2; FACT that the ~25 m^2 figure is the D2C aperture]
- **Beam/cell count for V3 is not hard-disclosed** (the spectrum doc reaches the ~1 Tbps figure via a beams x reuse x efficiency derivation, not a published beam count). [UNKNOWN]

---

## 2. Capacity (confirmation anchors; owned by the specs doc)

These are restated only to anchor the platform; the capacity stack lives in [`starlink_v3_specs.md`](starlink_v3_specs.md).

| Quantity | V3 | V2 Mini | Tag | Sources |
|---|---|---|---|---|
| User downlink per satellite | **~1 Tbps (~1,024 Gbps)** | ~96 Gbps | [FACT, multi-source] | Tom's Hardware; Basenor; NextBigFuture; RV Mobile |
| User uplink per satellite | **~160 to 200 Gbps** | ~6.7 Gbps | [FACT, multi-source] | NextBigFuture (160); Basenor (160-200); RV Mobile (160) |
| Downlink leap vs V2 Mini | **~10x** (96 -> 1,024 Gbps) | baseline | [FACT, multi-source] | Basenor; RV Mobile ("10x downlink, 24x uplink") |
| Combined RF + laser backhaul | **~4 Tbps** per satellite | n/a | [FACT, multi-source] | Basenor; NextBigFuture |
| Per Starship launch | **~60 V3 -> ~60 Tbps added** (some cite 54 to 100) | ~21 to 24 V2 Mini / Falcon 9 | [FACT, multi-source] | Tom's Hardware; NextBigFuture; RV Mobile |

The number of **beams/cells** is not hard-disclosed; "gigabit to the user" requires a **terminal hardware upgrade** and is a peak, not a sustained per-user allocation [FACT: Basenor].

---

## 3. Direct-to-cell on V3 vs V2 Mini (the capability ladder)

### 3.1 V2 Mini direct-to-cell (the current, deployed capability)

- The D2C variant of the V2 Mini carries a **~25 m^2 (roughly "25 square meter") deployable antenna array** that "functions as a cell tower in space," reaching **unmodified phones** [FACT, multi-source: US Mobile; SatelliteInternet; the Gen2 D2C ~25 m^2 figure also appears in the V2 Mini specs reporting].
- **Capability today (2025-2026):** commercially **texting + images** (T-Satellite launched commercially **Jul 23 2025**), **low-rate data** rolling out from **Oct 2025** at "hundreds of kilobits per second at best" (basic browsing/email, not video/streaming), and **voice in beta from late 2025** (native voice still in development; WhatsApp voice/video usable) [FACT, multi-source: US Mobile; 5Gstore/T-Mobile].
- Spectrum: rides **T-Mobile's PCS G-block 2x5 MHz** under FCC SCS (the thin-channel reason throughput is low), per [`starlink_v3_v4_spectrum_incorporation.md`](starlink_v3_v4_spectrum_incorporation.md) COMM-185. [FACT]
- Fleet: **300+** D2C-capable satellites in orbit by early 2026, growing with most Falcon 9 Starlink missions [FACT: US Mobile].

### 3.2 V3 direct-to-cell (the dedicated next-gen constellation)

- **A dedicated, separate direct-to-cell constellation of up to 15,000 V3-class satellites**, FCC filing **SAT-LOA-20250916-00282 (Sep 16 2025)**, at **~326 to 335 km, ~53 deg** [FACT, multi-source: NextBigFuture; FCC filing reference; LinkedIn coverage of the filing].
- **Capability target: 4G-LTE-equivalent text + voice + data to unmodified phones, ~100 Mbps peak / ~2 to 10 Mbps sustained per the reporting**, i.e. a large step beyond the V2 Mini's texting-plus-low-data, approaching **broadband-to-phone** rather than messaging-to-phone [FACT, single-source-cluster: NextBigFuture; treat the exact Mbps as reported-not-SpaceX-confirmed].
- **The capacity jump is a spectrum + aperture story, not a new band on the phone:** it depends on the **~65 MHz of dedicated MSS/AWS spectrum SpaceX is acquiring from EchoStar (~$17B+)** (owned by [`starlink_v3_v4_spectrum_incorporation.md`](starlink_v3_v4_spectrum_incorporation.md) COMM-186/187 and [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md)) feeding the **large deployable D2C phased array**. NextBigFuture frames it as ">100x capacity over V2 DTC (from ~7 Gbps aggregate to projected 700+ Gbps per D2C satellite)" [FACT for the framing; the "700+ Gbps" and ">100x" are projections, flagged].
- **The large aperture is the D2C-specific part.** As [`large_array_folding_and_stow.md`](large_array_folding_and_stow.md) establishes, closing the link to a handset needs a big folded aperture; that, not the broadband panel, is the bulky element. So "V3 direct-to-cell" = V3 bus + large deployable D2C array + dedicated spectrum.

**The clean ladder:** V2 Mini D2C = **texting + thin data + voice-in-beta** on a leased 2x5 MHz channel and a ~25 m^2 array. V3 D2C = **broadband-class text/voice/data (4G-equivalent)** on **owned ~65 MHz** and a dedicated 15,000-sat fleet. The step is bought with **owned spectrum + a dedicated constellation**, not a new phone band.

---

## 4. Why Starship, not Falcon 9 (the load-bearing question)

### 4.1 The explicit reason, stated and sourced

**V3 is launched on Starship and not Falcon 9 because it is physically too large AND too heavy for Falcon 9's fairing.** Two independent strands:

- **Size (the qualitative blocker):** a V3 is a **~7 m-long slab**; Falcon 9's fairing is **~5.2 m in diameter**. The ~7 m flat body does not fit and stack inside the Falcon 9 fairing the way the deliberately *downsized* V2 Mini (~4.1 x 2.7 m) does. Internet In Space states it plainly: V3 "**simply does not fit inside Falcon 9's 5.2-meter fairing**... V3 requires Starship's massive payload volume." [FACT, multi-source: Internet In Space; corpus dishycentral note that full-size V2/V3 "cannot launch on Falcon 9... designed specifically for Starship"]
- **Mass (the economic blocker):** V3 is **~3x a V2 Mini** (~1,900 vs ~575 kg). Starship lifts **~100 t** of Starlink per launch vs **~17 t** on Falcon 9, so even setting shape aside, batching V3 economically needs Starship's lift. Basenor: V3 is "more than three times the mass of a V2 Mini, which is precisely why Starship, not Falcon 9, is the only vehicle capable of deploying them economically." [FACT, multi-source: Basenor; RV Mobile (100 t vs 17 t)]

### 4.2 How many V3 per Starship, and why Falcon 9 is infeasible

| Vehicle | Fairing diameter | Payload envelope | V3 per launch | Why | Tag |
|---|---|---|---|---|---|
| **Starship** | **~9 m** (8 m payload envelope), ~18 m tall fairing | ~100 t to LEO, ~1,100 m^3 | **~54 to 100 (commonly ~60)** | V3 sized for this bay; flat slabs stack | [FACT, multi-source] |
| **Falcon 9** | **~5.2 m** | ~17 t to LEO | **0 (infeasible)** for full-size V3 | ~7 m slab exceeds 5.2 m fairing; only the *downsized* V2 Mini (~21 to 24) fits | [FACT, multi-source] |

Sources: Starship 9 m fairing / 8 m envelope / 100 t / 1,100 m^3 ([eoPortal Starship](https://www.eoportal.org/other-space-activities/starship-of-spacex), [SpaceX Starship Users Guide](https://spacex.relayto.com/e/starship-users-guide-37uiuuepbks0x)); ~60 V3/Starship ([Tom's Hardware](https://www.tomshardware.com/service-providers/network-providers/spacex-shows-off-massive-new-v3-starlink-satellites-expanded-technology-will-deliver-gigabit-internet-to-customers-for-the-first-time-and-enable-60-tera-bits-per-second-downlink-capacity), [NextBigFuture](https://www.nextbigfuture.com/2025/02/spacex-version-3-starship-and-version-3-starlink-both-arrive-in-2025.html)); 54 V3 and 100 t vs 17 t ([RV Mobile Internet](https://www.rvmobileinternet.com/what-the-failure-of-starship-flight-7-means-for-starlink-v3-satellites-coming/)); ~100 V3 / 200 t upper cite ([NextBigFuture Gen3-vs-ISS](https://www.nextbigfuture.com/2024/03/spacex-starship-launched-starlink-gen-3-unfolded-nearly-as-wide-as-the-space-station.html)); V2 Mini 21 to 24/Falcon 9 ([Payload record-24](https://payloadspace.com/spacex-improves-falcon-9-performance-and-flies-a-record-24-starlink-v2-mini-satellites/)). **The per-Starship count spans ~54 to 100 across sources; ~60 is the most frequently cited operational figure** (the ~100/200 t cite is an upper-bound from an earlier projection). [FACT with a flagged spread.]

### 4.3 The crucial fairing-fit implication for Neutron

**Is a V3-class satellite sized for a ~5 m fairing (Neutron) or for Starship's ~8 to 9 m fairing?** **It is dimensioned for Starship's ~8 to 9 m bay, but a bare V3 slab still physically fits a ~5.5 m Neutron fairing** because the binding V3 dimension is the **~7 m length lying along the ~14 m fairing**, with a **~3.5 m width** well under the ~5.5 m diameter, and the body is **flat (stackable)**:

- **Falcon 9 (5.2 m): categorically excluded for full-size V3** (the qualitative reason V3 needs Starship). [FACT]
- **Neutron (~5.5 m diameter x ~14 m fairing): a V3 slab fits the shape gate** (7 m long x 3.5 m wide flat panel inside a 5.5 m x 14 m fairing, and it stacks), so unlike Falcon 9, Neutron is **not** categorically shape-excluded for a V3-class slab. **The binding gate on Neutron is mass** (~1,900 kg each vs ~9,500 kg reusable-to-SSO -> **~5 per launch**, ~1/12 of a Starship batch), exactly as [`neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md) concludes. [FACT/DERIVED]
- **The asymmetry that matters:** Falcon 9 *cannot* carry a full-size V3 (shape); Neutron *can* carry a few (mass-bound). But **V3 is optimized for Starship**, so flying V3-shaped satellites on Neutron is inherently ~1/12-batch economics. The Neutron-sensible path is a **smaller flat-pack sized to its fairing** (Section 6), not a literal V3.

**One important caveat (flagged):** Neutron's usable fairing *length* is eaten by Stage 2 sitting inside the "Hungry Hippo" fairing (per the grounding docs), so the practical stack height is less than the 14 m external height. This does not change "a V3 slab fits," but it does cap how many slabs stack before the mass limit even binds. [DERIVED, from grounding docs.]

---

## 5. V2 Mini reference (the downsized predecessor)

| Parameter | V2 Mini | Tag | Sources |
|---|---|---|---|
| Mass | **~575 to 800 kg** (early ~800 kg; optimized ~525 to 575 kg) | [FACT, multi-source] | dishycentral (~800 kg); NextBigFuture (575 kg); Wikipedia/Starlink |
| Body dimensions | **~4.1 m x 2.7 m** (stowed ~1.25 x 1.0 x 0.6 m per one teardown-style cite) | [FACT, multi-source] | Wikipedia/Space.com (4.1 x 2.7 m); dishycentral (stowed) |
| Antenna | **more powerful phased array** + **E-band backhaul**; D2C variant adds a **~25 m^2 deployable antenna** | [FACT, multi-source] | Starlink Gen2 PDF (E-band, 4x capacity); US Mobile / SatelliteInternet (~25 m^2 D2C array) |
| Downlink / uplink | **~96 Gbps / ~6.7 Gbps** | [FACT, multi-source] | NextBigFuture; Gunter's Space Page |
| Per Falcon 9 | **~21 to 24** (record 24, Jun 2026) | [FACT, multi-source] | Payload (record 24); Everyday Astronaut |
| Why it fits Falcon 9 | **deliberately downsized** to fit the 5.2 m fairing while Starship was delayed | [FACT, multi-source] | Internet In Space; dishycentral; corpus |

**The key narrative:** V2 Mini exists *because* full-size V2/V3 could not fly until Starship. SpaceX shrank the satellite to keep launching on Falcon 9. V3 is the **un-shrunk** design that the Starship fairing finally allows, which is precisely why its size is the thing that excludes Falcon 9. [FACT/DERIVED]

---

## 6. Implication for Neutron: is Flatellite the Neutron-sized analog of a V3? (ANALYSIS, flagged)

This section is analysis, not a SpaceX/Rocket Lab spec sheet. Flags are explicit.

**Claim: a "V3-class but Neutron-sized" broadband or direct-to-cell satellite is the Rocket Lab Flatellite concept, NOT a literal shrunk V3.** Reasoning:

- A literal V3 on Neutron is **mass-bound at ~5/launch** (Section 4.3), i.e. ~1/12 of a Starship batch, with launch-cost-per-satellite ~$10 to 11 M vs a small fraction of that on Starship ([`neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md)). That is structurally uncompetitive for a mega-constellation. So the Neutron-rational design is **not** "fly V3s," it is "fly many smaller flat-packs."
- **Rocket Lab's Flatellite** (announced Feb 27 2025) is exactly that shape: a **low-profile, stackable, flat satellite**, **up to 16 per Neutron launch**, with **Neutron-native integration**, **optical crosslinks** (Mynaric heritage), and electric propulsion, aimed at **large constellations** for connectivity + sensing (defense/commercial) [FACT for the qualitative design: Rocket Lab announcement; FACT for "up to 16/Neutron"; ESTIMATE for mass ~800 kg].
- **The Flatellite is the structural mirror of a Starlink flat-pack**: renderings "appear remarkably similar to a Starlink satellite, except a single satellite occupies one layer in the stack (instead of Starlink's two)" [analysis source: illdefined.space, flagged speculative]. So the Neutron analog of "V3 the flat-pack platform" is "Flatellite the flat-pack platform," each sized to its own rocket's fairing.
- **What a Neutron-sized V3-analog looks like (the founder's ask), flagged as analysis:**
  - **Mass:** ~**800 kg-class** (Flatellite estimate), roughly **V2-Mini-sized, not V3-sized** (so ~10 to 16 per Neutron, not ~5), because Neutron's fairing and lift favor the smaller flat-pack.
  - **Antenna:** a flat phased array roughly the body size for broadband (like V3's broadband panel), and, for a D2C variant, a **smaller deployable array than V3's** (a 5.5 m fairing cannot stow a V3/AST-class many-tile aperture and still stack, per [`large_array_folding_and_stow.md`](large_array_folding_and_stow.md)). The D2C lever for a Neutron entrant is **better fold/stow efficiency or a smaller aperture**, not V3-scale.
  - **Capacity:** correspondingly **below V3's ~1 Tbps** per satellite, with the constellation making up throughput by **count** (many per launch), not per-satellite size.
- **Honest gaps:** Rocket Lab has **not** published Flatellite mass, dimensions, antenna size, or per-satellite capacity. The "Neutron-sized V3-analog" is therefore a **design-space inference**, not a datasheet comparison. The one hard Flatellite number is **"stacks of up to 16 per Neutron"**; everything else (mass ~800 kg, capacity) is estimated. [ANALYSIS / ESTIMATE, flagged.]

**Net:** Flatellite is the Neutron-native answer to the same flat-pack stacking problem V3 solves for Starship, but at **V2-Mini-class mass and ~16/launch**, not V3-class mass and ~5/launch. The Neutron path to a comms constellation is the small stackable flat-pack, not the literal V3.

---

## 7. What this gives the model

1. **V3 is a ~1,900 kg, ~7 m flat slab that unfolds to ~60 m (mostly solar).** Its broadband aperture is the flat body (area not disclosed); the big deployable antenna is the **direct-to-cell** one (~25 m^2-class).
2. **Why Starship: size first (the ~7 m slab cannot fit Falcon 9's 5.2 m fairing), mass second (~3x V2 Mini, 100 t vs 17 t lift).** ~60 V3/Starship (range 54 to 100) vs ~21 to 24 V2 Mini/Falcon 9.
3. **A V3-class slab fits a ~5.5 m Neutron fairing (mass-bound ~5/launch), but V3 is dimensioned for Starship's ~8 to 9 m bay**, so Neutron carries ~1/12 of a Starship batch. Falcon 9 is categorically excluded for full-size V3; Neutron is not (it is mass-limited).
4. **V3 direct-to-cell = a dedicated up-to-15,000-sat constellation (FCC SAT-LOA-20250916-00282) targeting 4G-equivalent text/voice/data**, a step up from V2 Mini's texting-plus-thin-data-plus-beta-voice, bought with **owned ~65 MHz** + a **large deployable array**.
5. **The Neutron-sized analog of a V3 is the Flatellite** (stackable flat-pack, up to 16/Neutron, ~800 kg estimate), not a literal shrunk V3; per-satellite capacity drops and constellation throughput comes from count.

---

## Open questions / uncertainties

1. **V3 broadband aperture area (m^2).** Not disclosed by SpaceX. The ~25 m^2 figure is the **D2C** aperture, not the broadband one. [UNKNOWN]
2. **V3 beam/cell count.** Not hard-disclosed; the ~1 Tbps is reached by derivation, not a published beam count. [UNKNOWN]
3. **Exact V3 stowed thickness and the broadband-vs-solar split of the ~60 m span.** Inferred (flat-pack, solar-dominated), not published. [UNKNOWN; carried from the fold doc]
4. **Per-Starship V3 count.** Sources span **54 to 100**; ~60 is the operational figure, ~100/200 t is an upper-bound projection. [FACT with spread]
5. **V3 D2C sustained throughput per phone.** "~2 to 10 Mbps sustained / 100 Mbps peak / 700+ Gbps per sat" are **reported projections**, not SpaceX-confirmed datasheet values. [FLAGGED projection]
6. **Flatellite mass, dimensions, antenna, capacity.** Only "up to 16/Neutron" is firm; mass ~800 kg and the V3-analog framing are estimates/analysis. [ESTIMATE / ANALYSIS]
7. **Neutron usable fairing length (Stage-2-inside penalty).** Caps how many V3 slabs stack before the mass limit binds; unpublished. [UNKNOWN; carried from grounding docs]

---

## Sources

- [Starlink V3 Satellites: Everything About SpaceX's Next-Generation Constellation, Internet In Space (V3 ~7 m long, 1,760 kg, does not fit Falcon 9's 5.2 m fairing, needs Starship)](https://internetin.space/blog/starlink-v3-satellites-next-generation/)
- [SpaceX Version 3 Starship and Version 3 Starlink Both Arrive in 2025, NextBigFuture (V3 ~1900 kg vs V2 Mini 575 kg, 60 m wingspan, 1 Tbps down / 160 Gbps up, 96 vs 1024 Gbps)](https://www.nextbigfuture.com/2025/02/spacex-version-3-starship-and-version-3-starlink-both-arrive-in-2025.html)
- [SpaceX Starship Starlink Gen 3 Nearly as Wide as the Space Station, NextBigFuture (60 m wingspan from 7-8 m base, over 2 tons, ~100/Starship, 200 t)](https://www.nextbigfuture.com/2024/03/spacex-starship-launched-starlink-gen-3-unfolded-nearly-as-wide-as-the-space-station.html)
- [Starlink V3 Satellites: 10x Bandwidth Leap Explained, Basenor (1,024 Gbps/sat, fully-digital phased array, 60/Starship, ~4 Tbps RF+laser, gigabit needs terminal upgrade)](https://www.basenor.com/blogs/news/starlink-v3-satellites-10x-bandwidth-leap-explained)
- [Starlink V3 Satellites: What the Next-Gen Specs Mean, Basenor (~2,000 kg, >3x V2 Mini mass, only Starship can deploy economically, ~350 km)](https://www.basenor.com/blogs/news/starlink-v3-satellites-what-the-next-gen-specs-mean)
- [What the Failure of Starship Flight 7/8 Means for Starlink V3, RV Mobile Internet (V3 ~1900 kg vs 575 kg, 54/Starship vs 20-23 V2 Mini, 100 t vs 17 t, 10x down/24x up)](https://www.rvmobileinternet.com/what-the-failure-of-starship-flight-7-means-for-starlink-v3-satellites-coming/)
- [SpaceX shows off massive new V3 Starlink satellites, Tom's Hardware (gigabit to users, 60 Tbps downlink/launch, 60 V3/Starship)](https://www.tomshardware.com/service-providers/network-providers/spacex-shows-off-massive-new-v3-starlink-satellites-expanded-technology-will-deliver-gigabit-internet-to-customers-for-the-first-time-and-enable-60-tera-bits-per-second-downlink-capacity)
- [SpaceX 15000 V3 Starlink Direct-to-Cellphone Satellites, NextBigFuture (FCC SAT-LOA-20250916-00282, 15,000 sats, 4G-LTE-equivalent text/voice/data, >100x V2 DTC, 326-335 km, $17B EchoStar)](https://www.nextbigfuture.com/2025/09/spacex-15000-v3-starlink-direct-to-cellphone-satellites.html)
- [Starlink Satellite Calls On Your Phone: Direct-to-Cell Guide 2026, US Mobile (~25 m^2 deployable D2C antenna, texting Jul 2025, data Oct 2025 hundreds of kbps, voice beta late 2025, 300+ D2C sats)](https://www.usmobile.com/blog/starlink-satellite-phone-calls/)
- [Starlink Direct to Cell and T-Satellite Guide 2026, SatelliteInternet.com (D2C array, T-Mobile partnership, capability timeline)](https://www.satelliteinternet.com/providers/starlink/starlink-direct-to-cell/)
- [SpaceX Improves Falcon 9 and Flies a Record 24 Starlink V2 Mini, Payload (21-24 V2 Mini per Falcon 9, record 24)](https://payloadspace.com/spacex-improves-falcon-9-performance-and-flies-a-record-24-starlink-v2-mini-satellites/)
- [How Big Are Starlink Satellites? dishycentral (V2 Mini ~800 kg, ~4.0 x 2.7 m; full-size V2 cannot launch on Falcon 9, designed for Starship)](https://dishycentral.com/how-big-are-starlink-satellites)
- [Starlink Block v3.0 (Gen2), Gunter's Space Page (~7 m x 3.5 m body, band payload)](https://space.skyrocket.de/doc_sdat/starlink-v2-0-ss.htm)
- [Starlink Block v2-Mini, Gunter's Space Page (V2 Mini ~96 Gbps down / 6.7 Gbps up reference)](https://space.skyrocket.de/doc_sdat/starlink-v2-mini.htm)
- [Starship of SpaceX, eoPortal (9 m fairing diameter, 18 m high, 8 m payload envelope, 100 t to LEO, 1,100 m^3)](https://www.eoportal.org/other-space-activities/starship-of-spacex)
- [Starship Users Guide, SpaceX (9 m fairing, 8 m payload dynamic envelope, extended 22 m height)](https://spacex.relayto.com/e/starship-users-guide-37uiuuepbks0x)
- [Starships Payload Milestone Gives a Preview of V3 Starlink Launches, Via Satellite (flat stowed, dense stack, deploy one at a time)](https://www.satellitetoday.com/launch/2025/08/27/starships-payload-milestone-in-test-flight-gives-a-preview-of-v3-starlink-launches/)
- [Rocket Lab Announces Flatellite, Rocket Lab (stackable flat satellite, mass manufacture, Neutron integration, large constellations, connectivity + sensing)](https://rocketlabcorp.com/updates/rocket-lab-announces-flatellite-a-new-satellite-designed-for-mass-manufacture-and-tailored-for-large-constellations/)
- [Stacking the Deck: Rocket Lab's Flatellite, illdefined.space (up to 16/Neutron, ~800 kg estimate, optical crosslinks, one layer per stack vs Starlink's two; analysis/speculative)](https://www.illdefined.space/stacking-the-deck-rocket-labs-flatellite/)
- *(V3 mass ~1,900 kg, ~7 m slab, ~60 m span, fold mechanics, and the per-launch fit arithmetic are cross-referenced from [`starlink_v3_specs.md`](starlink_v3_specs.md), [`large_array_folding_and_stow.md`](large_array_folding_and_stow.md), and [`neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md); the D2C spectrum from [`starlink_v3_v4_spectrum_incorporation.md`](starlink_v3_v4_spectrum_incorporation.md). Not all re-listed.)*

---

## Claims ledger (COMM-271..292)

For the catalog reconciliation step to ingest. Each hard claim with tag and sources; single-source and projection claims flagged.

| Claim ID | Claim | Status | Sources |
|---|---|---|---|
| COMM-271 | Starlink V3 mass is **~1,760 to 2,000 kg per satellite (working ~1,900 kg)**, roughly **3x a V2 Mini**. | FACT (multi-source) | NextBigFuture (1900); RV Mobile (1900); Internet In Space (1760); Basenor (~2000, >3x V2 Mini) |
| COMM-272 | V3 stows as a **flat ~7 m-long (~7 x 3.5 m) slab** and deploys to a **~60 m wingspan** from a 7-8 m base; the span is **solar-array-dominated**, not RF-aperture-dominated. | FACT (multi-source) | Gunter's (7 x 3.5 m); Internet In Space (~7 m); NextBigFuture (60 m span, 7-8 m base); cross-ref large_array_folding_and_stow.md |
| COMM-273 | V3 uses a **fully-digital phased array with dynamic beamforming** (Ku/Ka user/feeder, E-band backhaul); the broadband **aperture area in m^2 is NOT publicly disclosed**. | FACT for architecture; UNKNOWN for aperture area | Grokipedia; Basenor (fully-digital phased array) |
| COMM-274 | The "**~25 m^2** deployable antenna" cited in V3 write-ups is the **direct-to-cell** aperture (the V2 Mini D2C-class array), not a disclosed V3 **broadband** aperture. | FACT (for the D2C ~25 m^2); flags a common conflation | US Mobile; SatelliteInternet; Gen2 D2C ~25 m^2 reporting |
| COMM-275 | V3 per-satellite capacity: **~1 Tbps (~1,024 Gbps) downlink, ~160 to 200 Gbps uplink, ~4 Tbps combined RF+laser**; ~10x the V2 Mini downlink (96 Gbps). | FACT (multi-source) | Tom's Hardware; Basenor; NextBigFuture; RV Mobile |
| COMM-276 | V3 **beam/cell count is not hard-disclosed**; "gigabit to the user" requires a **terminal hardware upgrade** and is a peak, not sustained per-user rate. | UNKNOWN (beams); FACT (terminal upgrade) | Basenor; cross-ref starlink_v3_v4_spectrum_incorporation.md |
| COMM-277 | V3 (Gen3) is the platform for a **dedicated up-to-15,000-satellite direct-to-cell constellation**, FCC **SAT-LOA-20250916-00282 (Sep 16 2025)**, ~326-335 km, ~53 deg. | FACT (multi-source) | NextBigFuture; FCC filing reference; LinkedIn coverage of filing |
| COMM-278 | V3 direct-to-cell **target capability: 4G-LTE-equivalent text + voice + data to unmodified phones (~100 Mbps peak, ~2 to 10 Mbps sustained per reporting)**, a step up from V2 Mini D2C. | FACT (single-source-cluster); the Mbps are reported projections, flagged | NextBigFuture; cross-ref comms_direct_to_cell.md |
| COMM-279 | V2 Mini direct-to-cell capability (deployed): **commercial texting + images (T-Satellite Jul 23 2025), low-rate data from Oct 2025 (hundreds of kbps), voice in beta from late 2025**; rides T-Mobile PCS G-block 2x5 MHz. | FACT (multi-source) | US Mobile; 5Gstore/T-Mobile; cross-ref starlink_v3_v4_spectrum_incorporation.md COMM-185 |
| COMM-280 | V3 D2C capacity step is framed as **">100x V2 DTC" (~7 Gbps aggregate -> projected 700+ Gbps per D2C satellite)**, enabled by ~65 MHz owned EchoStar spectrum + a large deployable array. | FACT for the framing; the 700+ Gbps and >100x are projections, flagged | NextBigFuture; cross-ref starlink_v3_v4_spectrum_incorporation.md COMM-186/187 |
| COMM-281 | **V3 is launched on Starship and not Falcon 9 primarily because it is too LARGE for Falcon 9's 5.2 m fairing** (the ~7 m slab does not fit/stack), with mass (~3x V2 Mini) the secondary, economic reason. | FACT (multi-source) | Internet In Space ("does not fit inside Falcon 9's 5.2-meter fairing"); Basenor (3x mass); dishycentral (full-size cannot launch on Falcon 9) |
| COMM-282 | **Starship carries ~54 to 100 V3 per launch (commonly cited ~60, adding ~60 Tbps)**; Falcon 9 carries **0 full-size V3** (only the downsized V2 Mini, ~21 to 24). | FACT (multi-source, with a flagged 54-100 spread) | Tom's Hardware (60); NextBigFuture (60; 100 upper); RV Mobile (54); Payload (21-24 V2 Mini) |
| COMM-283 | **Starship fairing is ~9 m diameter (8 m payload envelope), ~100 t to LEO, ~1,100 m^3**; V3 is dimensioned for this bay. | FACT (multi-source) | eoPortal Starship; SpaceX Starship Users Guide |
| COMM-284 | **Falcon 9's fairing is ~5.2 m diameter and ~17 t to LEO**, vs Starship's ~9 m / ~100 t; the size gap is the qualitative reason V3 needs Starship. | FACT (multi-source) | RV Mobile (100 t vs 17 t); Falcon 9 PUG (5.2 m, cross-ref neutron_comms_payload_fit.md) |
| COMM-285 | A **bare V3 slab physically fits a ~5.5 m Neutron fairing** (7 m long x 3.5 m wide flat panel inside ~5.5 m x ~14 m, and it stacks); unlike Falcon 9, Neutron is **not** shape-excluded for a V3-class slab. | FACT/DERIVED | Gunter's (7 x 3.5 m); cross-ref neutron_comms_payload_fit.md; Neutron PUG 5.5 m |
| COMM-286 | On Neutron the binding gate for a V3-class slab is **mass (~1,900 kg each vs ~9,500 kg reusable-to-SSO -> ~5/launch, ~1/12 of a Starship batch)**, not shape. | DERIVED | cross-ref neutron_comms_payload_fit.md (claims 19, 21) |
| COMM-287 | **V3 is dimensioned for Starship's ~8 to 9 m bay**, not a 5 m fairing; flying V3-shaped satellites on Neutron is inherently ~1/12-batch economics, so the Neutron-rational design is a smaller flat-pack, not a literal V3. | DERIVED / ANALYSIS | synthesis of COMM-282..286; neutron_comms_payload_fit.md |
| COMM-288 | V2 Mini reference: **~575 to 800 kg, ~4.1 x 2.7 m body, ~96 Gbps down / ~6.7 Gbps up, ~21 to 24 per Falcon 9**; deliberately **downsized to fit the 5.2 m fairing** while Starship was delayed. | FACT (multi-source) | dishycentral; NextBigFuture; Space.com/Wikipedia; Payload; Gunter's |
| COMM-289 | V2 Mini direct-to-cell variant carries a **~25 m^2 deployable phased-array antenna** ("cell tower in space") reaching unmodified phones. | FACT (multi-source) | US Mobile; SatelliteInternet; Gen2 D2C reporting |
| COMM-290 | **Rocket Lab's Flatellite** (announced Feb 27 2025) is a **low-profile stackable flat satellite, up to 16 per Neutron**, Neutron-integrated, with optical crosslinks, for large constellations (connectivity + sensing). | FACT for design + 16/launch; mass ~800 kg is an ESTIMATE | Rocket Lab announcement; illdefined.space (16/Neutron, ~800 kg estimate) |
| COMM-291 | **The Neutron-sized analog of a V3 flat-pack is the Flatellite, NOT a literal shrunk V3**: ~V2-Mini-class mass (~800 kg), ~10 to 16 per Neutron (vs ~5 for V3), correspondingly **below V3's ~1 Tbps** per satellite; a D2C variant needs a **smaller/better-folding aperture** than V3's (5.5 m fairing cannot stow a V3/AST-class many-tile array and still stack). | ANALYSIS / ESTIMATE (flagged) | synthesis; Rocket Lab; cross-ref large_array_folding_and_stow.md, neutron_comms_payload_fit.md |
| COMM-292 | **Unknown gaps:** V3 broadband aperture m^2; V3 beam count; exact stowed thickness and broadband-vs-solar split of the 60 m span; V3 D2C sustained per-phone throughput (reported projections only); Flatellite mass/dimensions/capacity (only 16/Neutron firm). | UNKNOWN / FLAGGED | (absence of disclosure across all sources above) |
