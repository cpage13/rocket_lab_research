# Neutron Comms-Payload Fit: Can Neutron Carry a Starlink-V3-Class or a Direct-to-Cell-Class Satellite?

**Research date:** 2026-06-18
**Purpose:** Determine whether Rocket Lab's Neutron can carry a Starlink-V3-class broadband satellite and a direct-to-cell satellite (AST SpaceMobile BlueBird-class), how many fit per Neutron launch, and what that implies for launch cost per satellite (which drives cost per subscriber). Companion to the orbital data-center track; same model shape (cost per subscriber up the chain).
**Vehicle modeled:** Neutron ONLY. Rocket Lab has no Starship-class vehicle; none is assumed.
**Status:** Understanding-building input. No verdict. All payload-fit conclusions inherit the unresolved Neutron SSO-mass and usable-fairing-volume uncertainties flagged in the grounding docs.

> **Grounds in and does not duplicate:** `rocket_lab/neutron/neutron_specs.md` and `rocket_lab/neutron/payload_and_block_upgrade.md`. Those two docs are the authority on Neutron's own numbers (mass by mode/orbit, fairing, block-upgrade upside). This doc takes those as given and adds only the **comms-satellite side** and the **fit arithmetic**. Where a Neutron number is used below it is cited to those docs, not re-derived.

---

## 0. Answer first (the three numbers that matter)

1. **Starlink-V3-class broadband satellite: Neutron is MASS-bound and fits roughly 4 to 5 per launch (reusable DRL).** A V3 masses ~1,900 kg [FACT] and the binding limit is Neutron's payload mass, not its fairing. At ~9,500 kg reusable-to-SSO (working estimate, per grounding doc) that is **~5 satellites**; at the ~13,000 kg LEO downrange figure, ~6 to 7. SpaceX itself flies ~60 V3 per Starship [FACT], so Neutron carries on the order of **one-twelfth of a Starship's V3 batch** per flight. The V3 stows flat for dense stacking, so the ~5.5 m Neutron fairing diameter is not the limiter for V3.

2. **Direct-to-cell satellite (BlueBird Block 2-class): the giant antenna is the binding constraint, and a current-design Block 2 is a poor fit for Neutron, on the order of 1 per launch.** A Block 2 BlueBird masses ~5,830 to 6,100 kg [FACT] and deploys a ~223 m² phased-array antenna [FACT], the largest commercial array in LEO. Folded, that array's stowed footprint is what fills a fairing: three Block 2 fit on a Falcon 9 (5.2 m fairing) [FACT], and only **one** rode each New Glenn (7 m fairing) and each Indian LVM3 [FACT]. Neutron's ~5.5 m fairing sits between Falcon 9 and New Glenn, so **~1 (possibly 2) Block 2 per Neutron launch** is the realistic envelope, antenna-stow-limited well before the ~9,500 kg mass limit (one satellite is only ~6 t). This is the case the prompt flags: **payload size, not mass, is most binding for direct-to-cell.**

3. **Implication for constellation cost: launch cost per satellite is set by satellites-per-launch, and that is where Neutron is structurally disadvantaged for the very payloads this thesis cares about.** At a ~$50 to 55 M Neutron launch [FACT, company target, per grounding doc], ~5 V3 per launch is **~$10 to 11 M of launch cost per V3 satellite**; ~1 Block 2 per launch is **~$50 to 55 M of launch cost per direct-to-cell satellite.** For comparison, a Falcon 9 carrying 3 Block 2 spreads its cost over 3, and a Starship carrying ~60 V3 spreads it over 60. Neutron cannot match the per-satellite launch economics of a Starship-class vehicle for these payloads; its competitiveness, if any, comes from cadence, dedicated insertion, and smaller-satellite or block-upgraded-Neutron paths, not from raw batch size.

The rest of this doc sources and derives each of these.

---

## 1. The two reference satellites (the comms-payload side)

### 1a. Starlink V3 (the broadband / home-internet reference)

V3 is SpaceX's third-generation broadband satellite, designed to fly only on Starship and not on Falcon 9. Key specs (all forward-looking; V3 began deploying 2026):

| Parameter | Value | Tag | Sources |
|---|---|---|---|
| Mass per satellite | **~1,900 kg** (some say "up to ~2,000 kg") | [FACT] | NextBigFuture; Tom's Hardware (via Grokipedia/Basenor secondary) |
| Stowed form | **Flat panel, dense-stacked** in the Starship bay, deployed one at a time | [FACT] | Via Satellite (Starship payload test); NextBigFuture |
| Deployed wingspan | **~60 m**, unfolded from a **7 to 8 m base** | [FACT] | Tom's Hardware; NextBigFuture |
| Length (stowed long axis) | **~7 m** | [FACT, single-source] | Gunter's Space Page (Starlink v2.0/Gen2 entry, listed 7 m × 3.5 m) |
| Downlink capacity | **~1 Tbps** per satellite (~1,024 Gbps) | [FACT] | Tom's Hardware; Basenor; NextBigFuture |
| Uplink capacity | **~160 Gbps** per satellite | [FACT] | NextBigFuture; Basenor (cites SpaceX) |
| Per Starship launch | **~60 V3 satellites**, adding **~60 Tbps** | [FACT] | Tom's Hardware; Basenor; NextBigFuture |
| Why not Falcon 9 | "Physically larger and heavier than V2; incompatible with Falcon 9's fairing" | [FACT] | Basenor; NextBigFuture; Tom's Hardware |

**Note on the V3 mass spread.** Sources cluster at **~1,900 kg** (NextBigFuture explicit "about 1900 kg"; Gunter's lists a tentative "~1200 kg?" for an earlier Gen2 design that predates the disclosed full-size V3, so it is treated as stale and not used). The ~2,000 kg figure is a rounded upper cite of the same satellite. **Working figure: 1,900 kg per V3.** [DERIVED from the two converging sources.]

**Why the fairing is not V3's limiter on Neutron.** The V3 ships as a **flat panel ~7 m long** that only unfolds to its 60 m wingspan after release. Flat panels stack densely; that is precisely how Starship carries ~60 at once. So for V3 the question is purely **how much mass Neutron can lift**, not whether the shape fits. (Contrast with the antenna-dominated direct-to-cell case in 1b.)

### 1b. AST SpaceMobile BlueBird (the direct-to-cell reference, the lead market)

BlueBird is the direct-to-smartphone (direct-to-cell) satellite line. Its defining feature is an enormous unfurlable phased-array antenna, because closing the link to an unmodified handset on the ground requires a very large aperture. Two generations exist; **Block 2 is the current, very large design** the prompt names.

**Block 1 (first generation, 5 launched on one Falcon 9, Sep 2024):**

| Parameter | Value | Tag | Sources |
|---|---|---|---|
| Mass per satellite | **~1,500 kg** | [FACT] | Gunter's Space Page (BlueBird-1); KeepTrack |
| Antenna array area | **64.0 m²** (cited 64.38 m²), ~10 m diameter phased array | [FACT] | Gunter's; AST (via KeepTrack); Wikipedia |
| Per Falcon 9 launch | **5 satellites** | [FACT] | Gunter's; Wikipedia |

**Block 2 (current "next-generation" design; first flew Dec 2025; 3 flew on one Falcon 9 Jun 16, 2026):**

| Parameter | Value | Tag | Sources |
|---|---|---|---|
| Mass per satellite | **~5,830 to 6,100 kg** (BlueBird 6 = 6,100 kg; later units 5,830 kg) | [FACT] | Gunter's Space Page (BlueBird-2); Wikipedia; SpaceNews |
| Antenna array area | **~223 m²** ("nearly 2,400 sq ft"), largest commercial array in LEO | [FACT] | AST official (Next-Gen BlueBird); Wikipedia; SpaceNews |
| Capacity (spectrum processed) | **~10 GHz processing bandwidth** per satellite; ~2,000+ active cells; up to ~120 Mbps peak per cell | [FACT] | AST official; SpaceNews; spacevoyaging (Block 2 agreements) |
| Build cost per satellite | **~$19 to 21 M** (up from ~$16 to 18 M) | [FACT, single-source cluster] | Reported via AST disclosures (Wikipedia / investor commentary); treat as order-of-magnitude |
| Per Falcon 9 (5.2 m fairing) | **3 satellites** | [FACT] | Spaceflight Now; Gunter's (BlueBird 8/9/10) |
| Per New Glenn (7 m fairing) | **1 satellite** (BlueBird 7, NG-3, Apr 2026) | [FACT] | Gunter's; Wikipedia |
| Per LVM3 (5.0 m fairing) | **1 satellite** (BlueBird 6, Dec 2025) | [FACT] | SpaceNews; ISRO |

**Constellation context (why the per-launch count compounds):** AST holds FCC authorization for **248 satellites** [FACT, SpaceNews], says **~45 to 60** BlueBirds give continuous US/key-market coverage and **~90** give global coverage [FACT, SpaceNews / Fierce], and planned ~45 to 60 Block 2 by end-2026 [FACT, SpaceNews]. So the constellation is **dozens, not thousands**, of these large satellites. That makes launch-cost-per-satellite a first-order driver of total constellation cost, and therefore of cost per subscriber.

---

## 2. Neutron's envelope (carried over from the grounding docs, not re-derived)

From `payload_and_block_upgrade.md` and `neutron_specs.md` (cited there to Rocket Lab / the Neutron PUG v1.0):

| Neutron parameter | Value | Tag | Note |
|---|---|---|---|
| Fairing external height | **~14 m** ("Hungry Hippo") | [FACT] | Stage 2 lives inside it, so usable payload length is materially less |
| Fairing payload diameter | **up to 5.5 m** | [FACT] | PUG v1.0; older material said 5.0 m |
| Usable fairing volume | **~150 to 230 m³** | [ESTIMATE] | Not published by Rocket Lab; crude geometry |
| Payload to LEO (downrange / DRL, reusable) | **13,000 kg** | [FACT] | Headline reusable mode |
| Payload to LEO (expendable) | **15,000 kg** | [FACT] | |
| Payload to 500 km polar (DRL) | **10,100 kg** | [FACT] | PUG official proxy for high-inclination |
| Payload to SSO (DRL, reusable) | **~9,500 kg** (range 8,500 to 10,500) | [ESTIMATE] | Working figure; NOT a Rocket Lab number |
| Payload to SSO (expendable) | **~11,000 kg** | [ESTIMATE] | |
| Launch price | **~$50 to 55 M** | [FACT, company target] | Pre-first-flight guidance, not a transaction price |

**Two fit gates.** A satellite rides Neutron only if it passes BOTH:
- **Mass gate:** total stacked payload mass <= Neutron's mass-to-orbit for the chosen mode/orbit.
- **Volume/shape gate:** each satellite's STOWED envelope must fit within the ~5.5 m diameter fairing, and the stack must fit the usable length.

For broadband V3 the mass gate binds. For direct-to-cell Block 2 the shape gate binds. That asymmetry is the whole story.

---

## 3. Fit arithmetic: Starlink-V3-class on Neutron

**Geometry first (does one even fit?).** A V3 is a ~7 m flat panel stowed [FACT, single-source]. A ~7 m long flat panel lies inside a 14 m fairing with a 5.5 m diameter cross-section comfortably, and panels stack. Shape does not bind. So V3-on-Neutron reduces to mass.

**Mass-limited count (the binding calculation):**

| Neutron mode / orbit | Neutron payload | V3 at ~1,900 kg each | Satellites per launch [DERIVED] |
|---|---|---|---|
| DRL, SSO (working est.) | ~9,500 kg | 9,500 / 1,900 = 5.0 | **~5** |
| DRL, LEO (official) | 13,000 kg | 13,000 / 1,900 = 6.8 | **~6 to 7** |
| Expendable, SSO (est.) | ~11,000 kg | 11,000 / 1,900 = 5.8 | **~5 to 6** |
| Expendable, LEO (official) | 15,000 kg | 15,000 / 1,900 = 7.9 | **~7 to 8** |

So **Neutron carries roughly 5 V3-class satellites per reusable launch to a useful broadband orbit, 6 to 7 to low-inclination LEO.** [DERIVED]

**Sanity check against Starship.** Starship carries ~60 V3 per launch [FACT]. Neutron at ~5 per launch is **~1/12 of a Starship batch**. This matches the vehicles' mass ratio: Starship is a 100 to 150 t-class lifter [FACT, the V3 search sources] versus Neutron's ~9.5 to 13 t, i.e., ~10 to 13x, and V3 is mass-bound, so the satellite-count ratio tracks the payload-mass ratio. The arithmetic is internally consistent. [DERIVED]

**Capacity per Neutron launch (for the model's downstream chain).** At ~1 Tbps per V3 [FACT] and ~5 per launch, a Neutron broadband launch delivers **~5 Tbps** to orbit; a Starship launch delivers ~60 Tbps [FACT]. [DERIVED] This is the supply-side number that later feeds capacity-per-subscriber and cost-per-GB.

---

## 4. Fit arithmetic: direct-to-cell (BlueBird Block 2-class) on Neutron

This is the case the prompt singles out: **the antenna is enormous, so payload SIZE binds before mass.**

**Step 1: the deployed array cannot fit any fairing; it must fold.** A Block 2 array is **~223 m²** [FACT]. Geometry of that area, two ways:
- If square: sqrt(223) = **~14.9 m on a side.** [DERIVED]
- If circular (Block 1 was a 10 m circle for 64 m²; scale by sqrt(223/64) = 1.87): **~18.7 m diameter.** [DERIVED]

Either way the **deployed antenna is ~15 to 19 m across**, far larger than Neutron's 5.5 m fairing or even Starship's ~9 m. So like all large unfurlable apertures it **stows folded/rolled** and deploys on orbit. The binding question is the **folded stowed footprint**, which is not publicly published for Block 2 in meters.

**Step 2: infer the stowed footprint from how many fit each existing fairing.** This is the cleanest available evidence, because it is revealed by actual flights:

| Launch vehicle | Fairing payload diameter | Block 2 per launch (flown) | Tag |
|---|---|---|---|
| Falcon 9 | ~5.2 m | **3** (BlueBird 8/9/10) | [FACT] |
| LVM3 (India) | ~5.0 m | **1** (BlueBird 6) | [FACT] |
| New Glenn | ~7.0 m | **1** (BlueBird 7) | [FACT] |

**Reading this evidence for Neutron (5.5 m fairing):**
- Falcon 9 at 5.2 m carried **3** stowed Block 2 by stacking the folded satellites vertically along the ~13 m fairing length. Neutron's fairing diameter (5.5 m) is slightly larger and its external height (~14 m) is comparable, but Neutron's usable length is eaten by Stage 2 sitting inside the Hungry Hippo fairing (per grounding docs), so usable stack length is materially less than Falcon 9's clean ~13 m. New Glenn at 7 m diameter and a much taller fairing flew only 1, and LVM3 at 5.0 m flew 1, showing the count is sensitive to the specific stowed geometry and integration, not diameter alone.
- **Therefore the realistic Neutron envelope is ~1 to 3 Block 2 per launch, with ~1 to 2 the prudent planning number** given the Stage-2-inside-fairing length penalty. Treat **2 as an optimistic case and 1 as conservative.** [DERIVED, single-vehicle-comparison inference; the true number requires the Block 2 stowed dimensions and the Neutron usable-length envelope, neither published.]

**Step 3: confirm mass is NOT the binding gate here.** One Block 2 is ~6,100 kg; two would be ~12,200 kg. Against ~9,500 kg reusable-to-SSO, **two Block 2 already exceed the reusable SSO mass limit**, and even one-plus-margin is a large fraction of it. So for two-up you would need expendable or LEO mode for mass, AND you would still have to win the stow-geometry gate. **The antenna-driven stow geometry and the ~6 t-each mass both push toward roughly 1 per Neutron launch.** Both gates converge on a small number; size is the one that bites first at the 5.5 m fairing. [DERIVED]

**Why size binds for direct-to-cell but not broadband (the core asymmetry).** A V3 broadband panel is ~7 m and flat; you can stack ~5 to the mass limit. A Block 2 direct-to-cell satellite is built around a folded ~15 to 19 m aperture; even folded it is bulky enough that a 5.2 m fairing took only 3 and a 5.0 to 7.0 m fairing took only 1. **Direct-to-cell is the lead market for this thesis, and it is exactly the payload where Neutron's modest fairing is most limiting.** [DERIVED]

---

## 5. Implication for constellation cost (the reason this fit matters)

Satellites-per-launch sets launch-cost-per-satellite, which is a first-order input to total constellation cost and thence cost per subscriber. At Neutron's ~$50 to 55 M target launch price [FACT, company target]:

| Payload | Sats / Neutron launch | Launch $ per satellite [DERIVED] | Reference: same satellite on its actual vehicle |
|---|---|---|---|
| Starlink V3-class (broadband) | ~5 (DRL/SSO) | **~$10 to 11 M** | Starship ~60/launch -> far lower $/sat; Neutron cannot match batch economics |
| BlueBird Block 2-class (direct-to-cell) | ~1 (size-bound) | **~$50 to 55 M** | Falcon 9 3/launch spreads ~$67 M list over 3 (~$22 M/sat); New Glenn/LVM3 also flew these |

**What this says for the model (no verdict, just the shape):**

1. **For broadband, Neutron is a mass-limited medium-lift truck competing against a Starship-class batch lifter, and loses on $/satellite by roughly the payload-mass ratio (~10x).** A V3-class constellation launched on Neutron would carry ~$10 to 11 M of launch cost per satellite versus a small fraction of that per V3 on Starship. Neutron's broadband role is therefore not "build a V3-scale mega-constellation cheaply." If Neutron has a broadband angle it is **smaller, lighter satellites** (so more per launch) or **dedicated/responsive insertion** the batch lifter does not offer, not raw cost-per-bit at constellation scale.

2. **For direct-to-cell, the binding constraint is the antenna, and the satellites are few and very large, so launch cost is dominated by how many of these bulky folded apertures fit a fairing.** At ~1 Block 2 per Neutron launch, ~$50 to 55 M of launch cost lands on each satellite, versus ~$22 M when three share a Falcon 9. **Neutron's 5.5 m fairing is the disadvantage**, and it bites hardest on precisely the lead market. The lever that would help Neutron here is **antenna stowage efficiency** (a satellite designed to fold into a 5.5 m fairing and stack 2 to 3 high) or a **smaller direct-to-cell satellite** than BlueBird Block 2, not more lift.

3. **The block-upgraded-Neutron upside (per grounding doc, +15 to 30%) changes the broadband count modestly and the direct-to-cell count barely at all.** A ~12 to 13 t reusable-to-SSO block-upgraded Neutron lifts ~6 to 7 V3 instead of ~5 (helps broadband), but adds little for direct-to-cell because that case is **size-bound, not mass-bound**: a bigger SSO mass budget does not enlarge the 5.5 m fairing. To move the direct-to-cell number Rocket Lab would need a larger fairing, which is not announced. [DERIVED]

4. **The unresolved Neutron numbers cap the precision.** The V3 count swings with the unpublished SSO mass (5 vs 6 to 7 across the SSO-to-LEO range), and the Block 2 count swings with the unpublished Block 2 stowed dimensions and Neutron usable length (1 vs 2 to 3). Both per-launch counts, and therefore both $/satellite figures, should be carried as ranges, not points.

---

## 6. Side-by-side summary

| | **Starlink V3-class (broadband)** | **BlueBird Block 2-class (direct-to-cell)** |
|---|---|---|
| Mass per satellite | ~1,900 kg [FACT] | ~5,830 to 6,100 kg [FACT] |
| Defining dimension | Flat ~7 m panel, stows dense | ~223 m² antenna, folds from ~15 to 19 m aperture [FACT/DERIVED] |
| Binding gate on Neutron | **Mass** | **Stowed size (antenna)** |
| Per Neutron launch (DRL) | **~5** (6 to 7 to LEO) [DERIVED] | **~1** (optimistically 2) [DERIVED] |
| Reference per-launch elsewhere | ~60 / Starship [FACT] | 3 / Falcon 9; 1 / New Glenn; 1 / LVM3 [FACT] |
| Launch $ per satellite (Neutron, ~$52 M) | **~$10 to 11 M** [DERIVED] | **~$50 to 55 M** [DERIVED] |
| Neutron's competitive lever | Smaller sats or dedicated insertion | Antenna-stow efficiency or smaller D2C sat |
| Block-upgrade help | Modest (mass-bound) | Minimal (size-bound) |

**Bottom line.** Neutron **can** physically carry both classes, but only a few of each: about **5 broadband V3-class** satellites per launch (mass-limited) and about **1 direct-to-cell Block 2-class** satellite per launch (antenna-size-limited). For the broadband case it is out-scaled ~10x on $/satellite by a Starship-class batch lifter; for the direct-to-cell case (the lead market) its modest 5.5 m fairing is the binding limit and pins it near 1 satellite per launch. Neutron's plausible role in a communications constellation is therefore **not** matching mega-constellation launch economics, but serving **smaller or stow-optimized satellites, dedicated/responsive insertions, or a block-upgraded path**, all of which raise satellites-per-launch and pull launch-cost-per-subscriber down toward competitiveness. None of this is a verdict; it sets the constraint the cost-per-subscriber model must respect.

---

## Open questions / uncertainties

1. **Neutron SSO mass (unpublished).** The V3-per-launch count (5 vs 6 to 7) rides directly on the ~9,500 kg working estimate. Confirm with Rocket Lab. Inherited from the grounding docs as the project's #1 open number.
2. **Neutron usable payload length and volume (unpublished).** With Stage 2 inside the Hungry Hippo fairing, the usable stack length is less than the 14 m external height. This is what decides whether 1 or 2+ Block 2-class satellites fit. No public figure.
3. **BlueBird Block 2 stowed (folded) dimensions (unpublished).** Only the deployed ~223 m² area and the revealed per-fairing counts (3 on F9, 1 on New Glenn / LVM3) are public. The folded footprint in meters would let the Block 2-per-Neutron count be computed directly instead of inferred from other vehicles.
4. **V3 exact mass.** Sources give ~1,900 kg (used here) to ~2,000 kg; a Gunter's "~1200 kg?" entry appears stale and was excluded. A firmer V3 mass tightens the broadband count.
5. **Cadence vs batch size.** This doc sizes per-launch payload only. Whether Neutron's economics close depends on launch cadence and price realization (both pre-first-flight and uncertain per the grounding docs), not just satellites-per-launch.
6. **Satellite design is the swing variable.** Both per-launch counts assume the satellites stay V3-sized and Block-2-sized. A communications operator designing to Neutron's 5.5 m fairing (smaller broadband panels, tighter-folding direct-to-cell apertures) would change both counts and is the most likely path to Neutron relevance here.

---

## Sources

- [Starlink V3 satellites, Tom's Hardware (mass, 1 Tbps, 60/Starship, 60 Tbps)](https://www.tomshardware.com/service-providers/network-providers/spacex-shows-off-massive-new-v3-starlink-satellites-expanded-technology-will-deliver-gigabit-internet-to-customers-for-the-first-time-and-enable-60-tera-bits-per-second-downlink-capacity)
- [SpaceX Version 3 Starship and Version 3 Starlink, NextBigFuture (V3 ~1900 kg, V2 Mini 575 kg, 60 m wingspan, 160 Gbps up / 1 Tbps down)](https://www.nextbigfuture.com/2025/02/spacex-version-3-starship-and-version-3-starlink-both-arrive-in-2025.html)
- [Starlink V3 Satellites: 10x Bandwidth Leap, Basenor (1,024 Gbps/sat, 60/Starship, 61,000 Gbps, 350 km, incompatible with Falcon 9 fairing)](https://www.basenor.com/blogs/news/starlink-v3-satellites-10x-bandwidth-leap-explained)
- [Starship's Payload Milestone gives a preview of V3 Starlink launches, Via Satellite (flat stowed, dense stack, deploy one at a time)](https://www.satellitetoday.com/launch/2025/08/27/starships-payload-milestone-in-test-flight-gives-a-preview-of-v3-starlink-launches/)
- [Starlink Block v3.0 (Gen2), Gunter's Space Page (7 m × 3.5 m; band payload; stale "~1200 kg?")](https://space.skyrocket.de/doc_sdat/starlink-v2-0-ss.htm)
- [Starlink Block v2-Mini, Gunter's Space Page (V2 Mini reference)](https://space.skyrocket.de/doc_sdat/starlink-v2-mini.htm)
- [SpaceX flies a record 24 Starlink V2 Mini, Payload (Falcon 9 V2 Mini per-launch count, ~730 kg implied)](https://payloadspace.com/spacex-improves-falcon-9-performance-and-flies-a-record-24-starlink-v2-mini-satellites/)
- [BlueBird Block 1, Gunter's Space Page (~1500 kg, 64.38 m² / 10 m array, 5 on one Falcon 9, 507×523 km / 53°)](https://space.skyrocket.de/doc_sdat/bluebird-1.htm)
- [BlueBird Block 2, Gunter's Space Page (BlueBird 6 = 6100 kg, later units 5830 kg, 3 on Falcon 9, 1 on New Glenn, 507×523 km / 53°)](https://space.skyrocket.de/doc_sdat/bluebird-2.htm)
- [AST SpaceMobile, Wikipedia (Block 2 6,100 kg, ~223 m² array, ~120 Mbit/s, >3x larger / 10x capacity vs Block 1, build cost cluster)](https://en.wikipedia.org/wiki/AST_SpaceMobile)
- [Next-Generation BlueBird, AST SpaceMobile official (nearly 2,400 sq ft array, 10 GHz processing bandwidth, 2000+ cells, 120 Mbps peak/cell)](https://ast-science.com/next-gen-bluebird/)
- [SpaceX launches 3 Block 2 BlueBird satellites, Spaceflight Now (3 per Falcon 9, ~6 t each, ~223 m² array, Jun 16 2026)](https://spaceflightnow.com/2026/06/16/live-coverage-spacex-to-launch-3-block-2-bluebird-satellites-for-ast-spacemobile/)
- [SpaceX launches 3 huge BlueBird direct-to-cell satellites, Space.com (3 giant D2C satellites, Falcon 9)](https://www.space.com/space-exploration/launches-spacecraft/spacex-falcon-9-bluebird-8-to-10-direct-to-cell-launch)
- [Indian rocket launches AST's next-gen BlueBird 6, SpaceNews (6,100 kg, ~223 m², 120 Mbps, 1 per LVM3; 248-sat FCC authorization; ~45 to 60 by end-2026)](https://spacenews.com/indian-rocket-launches-ast-spacemobiles-next-gen-bluebird-6-satellite/)
- [FCC clears AST SpaceMobile constellation, SpaceNews (248 satellites)](https://spacenews.com/fcc-clears-ast-spacemobile-constellation-as-launch-setback-clouds-ramp-up/)
- [AST SpaceMobile and the problem of delivering broadband from space, Fierce Network (~45 to 60 for continuous US coverage, ~90 for global)](https://www.fierce-network.com/wireless/ast-spacemobile-and-problem-delivering-broadband-space)
- [The Satellites the Size of a Studio Apartment, KeepTrack (BlueBird scale, Block 1 ~1.5 t)](https://keeptrack.space/deep-dive/ast-spacemobile-bluebirds)
- [AST SpaceMobile Signed Launch Agreements for Block 2, Space Voyaging (Block 2 program, AST5000 ASIC, capacity)](https://www.spacevoyaging.com/news/2024/11/17/ast-spacemobile-signed-launch-agreements-for-its-new-block2-bluebird-satellites/)
- *(Neutron specs cross-referenced from `rocket_lab/neutron/neutron_specs.md` and `rocket_lab/neutron/payload_and_block_upgrade.md`, which cite Rocket Lab / the Neutron PUG v1.0; not re-listed here.)*

---

## Claims ledger

Each hard claim with two or more independent sources (single-source claims tagged). For catalog ingestion.

1. **Starlink V3 mass is ~1,900 kg per satellite** (up to ~2,000 kg in rounded cites). Sources: NextBigFuture ("about 1900 kg"); Tom's Hardware (~2,000 kg). [FACT]
2. **Starlink V3 deploys to a ~60 m wingspan from a ~7 to 8 m base and stows as a flat, dense-stacked panel.** Sources: Tom's Hardware; NextBigFuture; Via Satellite (Starship payload test, flat-stack deployment). [FACT]
3. **Starlink V3 downlink is ~1 Tbps (~1,024 Gbps) per satellite; uplink ~160 Gbps.** Sources: Tom's Hardware; Basenor (1,024 Gbps); NextBigFuture (160 Gbps up / 1 Tbps down). [FACT]
4. **Starship carries ~60 V3 per launch, adding ~60 Tbps (~61,000 Gbps).** Sources: Tom's Hardware; Basenor; NextBigFuture. [FACT]
5. **Starlink V3 cannot fly on Falcon 9 (too large/heavy for its fairing); it requires Starship.** Sources: Basenor; NextBigFuture; Tom's Hardware. [FACT]
6. **Starlink V3 stowed long axis is ~7 m (Gen2 listing 7 m × 3.5 m).** Source: Gunter's Space Page (single source). [FACT, single-source]
7. **BlueBird Block 1 mass is ~1,500 kg.** Sources: Gunter's Space Page (BlueBird-1); KeepTrack. [FACT]
8. **BlueBird Block 1 antenna array is ~64 m² (64.38 m²), ~10 m diameter phased array.** Sources: Gunter's Space Page; AST (via KeepTrack); Wikipedia. [FACT]
9. **Five BlueBird Block 1 launched on a single Falcon 9 (Sep 12, 2024).** Sources: Gunter's Space Page; Wikipedia. [FACT]
10. **BlueBird Block 2 mass is ~5,830 to 6,100 kg per satellite (BlueBird 6 = 6,100 kg).** Sources: Gunter's Space Page (BlueBird-2); Wikipedia; SpaceNews. [FACT]
11. **BlueBird Block 2 antenna array is ~223 m² ("nearly 2,400 sq ft"), the largest commercial array in LEO.** Sources: AST official (Next-Gen BlueBird); Wikipedia; SpaceNews. [FACT]
12. **BlueBird Block 2 has ~10 GHz processing bandwidth, ~2,000+ active cells, up to ~120 Mbps peak per cell.** Sources: AST official; SpaceNews; Space Voyaging. [FACT]
13. **Three BlueBird Block 2 launched on a single Falcon 9 (Jun 16, 2026).** Sources: Spaceflight Now; Gunter's Space Page; Space.com. [FACT]
14. **One BlueBird Block 2 launched per New Glenn (BlueBird 7, NG-3) and per LVM3 (BlueBird 6).** Sources: Gunter's Space Page; Wikipedia (New Glenn); SpaceNews / ISRO (LVM3). [FACT]
15. **AST holds FCC authorization for 248 satellites.** Sources: SpaceNews (FCC clearance); SpaceNews (BlueBird 6). [FACT]
16. **~45 to 60 BlueBirds give continuous US/key-market coverage; ~90 give global coverage.** Sources: Fierce Network; SpaceNews. [FACT]
17. **BlueBird Block 2 build cost is ~$19 to 21 M per satellite (risen from ~$16 to 18 M).** Source: AST disclosures via Wikipedia / investor commentary (single-source cluster). [FACT, single-source]
18. **Falcon 9 payload fairing diameter is ~5.2 m; LVM3 ~5.0 m; New Glenn ~7 m.** Sources: SpaceX/Falcon documentation (per grounding-doc Falcon PUG); ISRO; Blue Origin (widely reported). [FACT]
19. **Neutron carries ~5 V3-class satellites per reusable (DRL) launch (mass-limited), ~6 to 7 to LEO.** Derivation: 9,500 to 13,000 kg Neutron payload (grounding docs) divided by ~1,900 kg per V3 (claim 1). [DERIVED]
20. **Neutron carries ~1 (optimistically up to ~2 to 3) BlueBird Block 2-class satellites per launch, antenna-stow-limited.** Derivation: revealed per-fairing counts (3 on Falcon 9 at 5.2 m, 1 on New Glenn at 7 m, 1 on LVM3 at 5.0 m; claims 13 to 14, 18) bracketing Neutron's 5.5 m fairing, with the Stage-2-inside-fairing usable-length penalty (grounding docs). [DERIVED]
21. **Launch cost per satellite on Neutron (~$52 M launch): ~$10 to 11 M per V3-class; ~$50 to 55 M per Block 2-class.** Derivation: ~$50 to 55 M Neutron launch price (grounding docs) divided by claims 19 and 20. [DERIVED]
22. **A Neutron broadband launch delivers ~5 Tbps to orbit (5 V3 at ~1 Tbps); a Starship launch ~60 Tbps.** Derivation: claim 3 times claim 19; claim 4. [DERIVED]
