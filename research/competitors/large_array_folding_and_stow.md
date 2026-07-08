# Large-Array Folding and Stow: How Much Does a Starlink V3 Fold vs a Direct-to-Cell Array?

**Research date:** 2026-06-22
**Purpose:** Answer the founder's specific question: "How much can you fold a large space antenna, maybe twice?" Concretely, how much does the Starlink V3 broadband satellite fold (stowed vs deployed, the fold ratio, how many fold lines), how that compares to a folding direct-to-cell array (AST BlueBird Block 2's ~223 m^2 aperture), and the general engineering rule for how tightly a large RF phased array can pack. This is a *mechanics-of-stow* doc; it does not re-derive capacity or per-launch fit.
**Status:** Understanding-building input. No verdict.

> **Grounds in and does not duplicate:**
> - [`research/competitors/starlink_v3_specs.md`](starlink_v3_specs.md): owns the V3 capacity-and-spec stack (1 Tbps/sat, ~60 m wingspan, ~7-8 m x ~3.5 m stowed body, ~1,900-2,000 kg mass, deploys flat-pack "PEZ dispenser" from Starship). This doc takes those numbers as given and adds only the **fold/stow geometry** layer.
> - [`research/rocket_lab/neutron/neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md): owns the per-launch fit arithmetic (V3 mass-bound ~5/Neutron; BlueBird Block 2 antenna-size-bound ~1/Neutron) and the revealed per-fairing counts (3 Block 2 on Falcon 9, 1 on New Glenn, 1 on LVM3). This doc explains *why* the Block 2 is size-bound by characterizing the fold, and supplies the missing-published-dimensions flag that doc relies on.

---

## 0. Answer first (the founder's "maybe twice?" question)

**Direct answer: a Starlink V3 does NOT fold "maybe twice." Its broadband aperture barely folds at all, while the direct-to-cell array folds far more than twice (it is a many-section accordion). These are two opposite stow problems, and conflating them is the trap.**

1. **The Starlink V3 broadband antenna IS essentially the flat satellite body itself, and it barely folds.** The thing that unfolds to the ~60 m "wingspan" is dominated by the two **solar wings**, not the broadband phased-array aperture. The RF user-link antenna is a flat panel that is roughly the stowed slab itself (~7-8 m long, ~3.5 m wide) [FACT, multi-source]. So the broadband aperture's deployed-to-stowed *area* ratio is close to **~1x (it does not meaningfully fold)**; what folds is the solar array, which is a wing, not an RF aperture. The founder's "fold it twice" intuition is closer to right for the *solar* part than for the RF part. [FACT/DERIVED]

2. **The AST BlueBird Block 2 direct-to-cell array is the opposite: a ~223 m^2 aperture built from ~250-265 modular "Micron" tiles (~0.84 m^2 / ~9 sq ft each) that folds far more than twice.** AST itself describes the satellite as unfolding "from a stowed volume roughly the size of a **phone booth** into a flat panel the size of a **studio apartment**" [FACT, AST framing]. That is not a two-fold; it is a multi-section accordion/origami pack of dozens of fold lines. The deployed aperture is ~15 m on a side (square) or ~17-19 m circle-equivalent [DERIVED], so it must collapse by something like **15-20x in its widest linear dimension** to fit a ~5 m fairing, i.e. many folds, not two. [FACT/DERIVED]

3. **The general rule (why a big RF array is NOT a solar wing).** A solar array folds magnificently (helical/Z-fold antennas hit stowed-to-deployed *volume* ratios near 0.01%, and flexible solar wings reach areal packing densities ~0.5-1.0 m^2 per liter) because it is a thin flexible membrane that can roll or accordion almost arbitrarily. A **phased-array RF aperture cannot pack nearly that tightly**: it carries rigid antenna tiles, T/R electronics, beamforming, thermal, and structure on a panel that must be flat and rigid to micron-tolerance-ish flatness when deployed. Published deployable-reflectarray packaging efficiencies land at ~**34-48%**, and AST's tiled approach packs to a "phone booth," not a soda can. So the honest rule is: **the more RF electronics per square meter (direct-to-cell, low-band, big aperture), the worse it folds; the V3 broadband aperture sidesteps this by not folding its aperture at all and just flying a modest flat panel with foldable solar wings.** [FACT, multi-source]

**The one-line founder answer:** "Fold it maybe twice" is roughly true for the V3 *broadband aperture* (it basically doesn't fold, it's a flat panel) and badly underestimates a *direct-to-cell* array (which is a phone-booth-to-studio-apartment, many-fold accordion). The reason Neutron's fairing bites on direct-to-cell and not on V3 is exactly this fold asymmetry.

---

## 1. The Starlink V3: what actually folds, and by how much

### 1.1 The aperture vs the wings (the key distinction)

The ~60 m "wingspan" headline conflates two very different structures:

| Element | Stowed | Deployed | Fold character | Tag |
|---|---|---|---|---|
| Satellite body / broadband phased-array aperture | flat slab ~7-8 m x ~3.5 m | ~same flat panel (the body IS the aperture) | **minimal fold** | [FACT/DERIVED] |
| Dual solar arrays ("wings") | folded against / stacked with the body | extend the assembly toward ~60 m total wingspan | **high fold (a wing, not an RF aperture)** | [FACT] |

Sources: [Gunter's Space Page, Starlink Block v3.0 (~7 m x 3.5 m body)](https://space.skyrocket.de/doc_sdat/starlink-v2-0-ss.htm); [NextBigFuture (Gen3 ~60 m wingspan from a 7-8 m base, "larger antennas and solar panels")](https://www.nextbigfuture.com/2024/03/spacex-starship-launched-starlink-gen-3-unfolded-nearly-as-wide-as-the-space-station.html); [Grokipedia summary (dual solar arrays longer than prior gens; stowed for dense stacking)](https://grokipedia.com/page/Starlink_V3_satellites); deployment-test behavior from [Skylinker (Starship 11 deployed V3 simulators, cargo-bay/deploy-mechanism verification)](https://www.skylinker.io/p/starship-11-a-step-towards-a-new-era-of-starlink-v3-eng).

**The load-bearing point:** SpaceX has NOT published a separate "broadband antenna fold ratio," because the broadband aperture is essentially the flat satellite slab that PEZ-dispenses from Starship. It ships flat, deploys flat, and stacks dense precisely *because* the RF aperture is not a large unfurling structure. The ~60 m number is a solar-wing-dominated span, and the solar wing is the part that folds. [DERIVED, flagged]

### 1.2 V3 fold ratio (broadband aperture)

- **Deployed-aperture-area to stowed-slab-area ratio: ~1x (negligible fold of the RF aperture).** The aperture is the body. [DERIVED]
- **Number of fold lines on the broadband aperture: effectively 0-1** (it is flat-stacked, not accordion-folded). No public SpaceX figure; inferred from the flat-pack, dense-stack deployment SpaceX demonstrated with V3 simulators on Starship Flight 11. [DERIVED/UNKNOWN on exact count]
- **What DOES fold: the solar arrays**, which deploy from the stowed stack toward the ~60 m span. Their fold count is not published. [UNKNOWN]

This is why [`neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md) finds V3 **mass-bound, not size-bound** on Neutron: a flat ~7 m slab fits any reasonable fairing and stacks; the only question is how many ~1,900 kg slabs the rocket can lift.

---

## 2. The direct-to-cell array (AST BlueBird Block 2): the real folding problem

### 2.1 Why direct-to-cell forces a giant folded aperture

Closing the link to an **unmodified handset** on the ground (a tiny, low-gain antenna held against a head) requires an enormous satellite aperture, the opposite of a Starlink dish-served broadband user. So the direct-to-cell satellite is essentially "a giant antenna with a bus attached," and that antenna must fold to fly. [FACT, see grounding doc Section 1b]

### 2.2 The Micron-tile architecture (how it folds)

AST builds the aperture from modular tiles it calls **Microns**:

| Quantity | Value | Tag | Source |
|---|---|---|---|
| Micron tile area | **~9 sq ft (~0.84 m^2)** each; solar cells one side, antennas the other | [FACT] | [AST via Tom's-Hardware-class trade summary / AST X post: "Micron is the building block... solar on one side, antennas on the other"](https://x.com/AST_SpaceMobile/status/1463260467137327109?lang=en); [SatNews / techtimes (Microns ~9 sq ft modular blocks)](https://satnews.com/2025/12/24/ast-spacemobile-deploys-bluebird-6-largest-commercial-array-in-leo/) |
| Block 1 / BlueWalker 3 array | **64 m^2**, deployed **8 m x 8 m** | [FACT, multi-source] | [Gunter's BlueWalker 3](https://space.skyrocket.de/doc_sdat/bluewalker-3.htm); [Sky & Telescope (8x8 m, 64 m^2)](https://skyandtelescope.org/astronomy-news/bluewalker-3-satellite-unfolds-brightening-40-fold/) |
| Block 2 array | **~223 m^2 ("nearly 2,400 sq ft"), >3x Block 1** | [FACT, multi-source] | [AST Next-Gen BlueBird](https://ast-science.com/next-gen-bluebird/); [SpaceNews](https://spacenews.com/indian-rocket-launches-ast-spacemobiles-next-gen-bluebird-6-satellite/) |
| Implied Microns per Block 1 | **~76** (64 / 0.84) | [DERIVED] | derived from the two facts above |
| Implied Microns per Block 2 | **~265** (223 / 0.84) | [DERIVED] | derived; AST also frames the constellation as "growing to 10,000 Microns with ~45 satellites" -> ~220 Microns/sat [DERIVED, consistent] |

Cross-check: AST's "10,000 Microns across ~45 satellites" framing implies **~220 Microns per satellite** [DERIVED], in the same ballpark as the ~265 from area/tile-size. Treat **~220-265 Microns per Block 2 satellite** as the planning band. The tile count is the natural fold-count scale: an aperture built from a couple hundred ~0.84 m^2 tiles folds along **many** tile boundaries, not two.

### 2.3 The fold ratio (the founder's number)

- **AST's own stowed-vs-deployed framing: "phone booth -> studio apartment."** A phone booth footprint is on the order of ~1 m x ~1 m; a studio apartment is tens of m^2. That is a deployed-area-to-stowed-footprint expansion of **~roughly 30-60x in area** for Block 1's 64 m^2, and larger for Block 2's 223 m^2. [FACT for the AST framing; DERIVED for the multiple]
- **Linear collapse:** Block 2 deploys to **~15 m on a side** (sqrt(223)) or **~17-19 m circular-equivalent** [DERIVED]; folded it must fit inside a ~5 m fairing, so its widest dimension collapses by **~3-4x just to clear the fairing diameter**, and its *area* collapses far more (the panel folds in two axes / accordion). This is **many fold lines (dozens), not two.** [DERIVED]
- **Revealed-by-flight fold evidence (the cleanest hard data):** 3 Block 2 fit a Falcon 9 (5.2 m fairing), but only 1 fit each New Glenn (7 m) and LVM3 (5.0 m) [FACT, see grounding doc]. The fact that even a 7 m fairing took only one folded Block 2 shows the *folded* stack is still bulky, i.e. the array does NOT pack to a thin wafer. [FACT]

**So, "maybe twice?" for direct-to-cell: no, far more.** A ~223 m^2 tiled aperture folding down to a phone-booth-class stowed volume is a many-section accordion/origami pack. The exact number of fold lines is **not published** by AST (see Section 4), but the tile count (~220-265) and the phone-booth framing both put it well into the dozens, not two.

### 2.4 Why it needs a wide fairing

The binding stow dimension is the **folded panel stack**: a couple hundred rigid ~0.84 m^2 tiles, each carrying antennas + electronics, fold into a thick slab whose footprint must clear the fairing diameter and whose height eats fairing length. Because the tiles are rigid and electronics-laden (not a thin membrane), the folded stack is comparatively thick, which is why a 7 m New Glenn fairing still only took one. This is the mechanism behind the grounding doc's finding that Block 2 is **size-bound, not mass-bound** (one ~6 t satellite is well under any of these rockets' mass limits). [FACT/DERIVED]

---

## 3. The general rule: how tightly can a large RF phased array fold?

The founder's underlying question is whether a big space antenna folds like a solar panel. It does not. The honest engineering rule, multi-sourced:

| Structure type | Stowed-to-deployed packing | Why | Tag / source |
|---|---|---|---|
| Thin-membrane / helical deployable antenna | up to **~0.01% stowed-to-deployed volume** (1:9,800) | flexible, no electronics on the membrane, rolls/coils | [FACT] [ScienceDirect deployable-array review](https://www.sciencedirect.com/science/article/pii/S2950104025000161) |
| Flexible Z-fold solar array | areal packing **~0.5-1.0 m^2 per liter**; ~50-70 W/kg | thin substrate, accordion/Z-fold, no rigid RF tiles | [FACT] same review |
| Deployable **reflectarray** RF antenna | packaging efficiency **~34-48%** | rigid-ish RF panels, finite-thickness, hinge steps | [FACT] [Stepped-deployment phased-array study, ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S009457652100641X) |
| AST tiled phased array (direct-to-cell) | "phone booth -> studio apartment" (~tens of x area) | hundreds of rigid electronics-laden Micron tiles | [FACT, AST framing] |
| Starlink V3 broadband aperture | **~1x (does not fold; it is the flat body)** | aperture sized to dish-served users, not handsets; flat-pack | [DERIVED] |

**The rule in one sentence:** packing efficiency falls as you add rigid RF electronics per square meter. A solar wing or membrane reflector folds to near-nothing; a fully-populated phased-array aperture (especially a low-band, handset-closing, direct-to-cell one) packs only to the ~tens-of-percent / phone-booth class, which is why direct-to-cell apertures are the launch-volume-binding payload and why a modest fairing (Neutron's 5.5 m) bites on them.

**This is the structural reason the two cases diverge:** Starlink V3 keeps its RF aperture small (flat panel, broadband, dish-served) and folds only its *solar wings*, so it stows dense and is mass-bound. Direct-to-cell must fly a giant RF aperture to reach handsets, so it folds a many-tile accordion and is size-bound. Same launcher, opposite binding constraint, entirely because of how much the aperture has to fold.

---

## 4. What is genuinely unpublished (flag for the founder)

The founder is furious about made-up numbers, so these are explicitly UNKNOWN, not estimated as if known:

1. **V3 broadband-aperture fold lines / exact stowed thickness.** SpaceX publishes no datasheet. We know it flat-packs and dense-stacks; the exact aperture-vs-solar split of the ~60 m span and the solar fold count are **not public**. [UNKNOWN]
2. **AST BlueBird Block 2 stowed (folded) dimensions in meters.** AST publishes deployed area (~223 m^2) and the phone-booth/studio-apartment framing, but **not** the folded slab's L x W x H or the exact number of fold lines. The fold count is *inferred* from tile count (~220-265) and the phone-booth framing, not stated. [UNKNOWN on exact fold-line count; grounding doc lists this as an open number]
3. **Exact Microns per Block 2.** Two derivations bracket ~220 (constellation framing) to ~265 (area/tile-size); AST has not stated a per-satellite Micron count for Block 2. [DERIVED, ranged]
4. **V3 broadband aperture area.** Not separately published from the satellite body; the "~1x fold" conclusion rests on the aperture-equals-body observation, not an AST/SpaceX-stated aperture m^2. [DERIVED]

---

## 5. So what (for the thesis)

1. **The founder's "fold it twice" instinct is right for broadband and wrong for direct-to-cell.** A V3-class broadband aperture barely folds (flat panel + folding solar wings), so it is mass-bound and fits any fairing. A direct-to-cell array folds many times (phone-booth-to-studio-apartment, ~220-265 tiles) and is size-bound.
2. **This is the mechanical root of the Neutron asymmetry** already in [`neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md): Neutron's 5.5 m fairing is irrelevant to V3 (flat slab) but binding on Block 2 (~1/launch). The lever for a Neutron-relevant direct-to-cell satellite is **better fold/stow efficiency or a smaller aperture**, not more lift, because the constraint is fold geometry, not mass.
3. **No general "fold ratio" rescues a direct-to-cell aperture into a small fairing.** The physics caps RF-aperture packing at the tens-of-percent / phone-booth class (vs ~0.01% for a solar membrane). You cannot fold a handset-closing aperture like a solar wing; the electronics density forbids it.

---

## Open questions / uncertainties

1. **Block 2 folded dimensions in meters** (the single number that would convert the per-fairing counts into a direct fold ratio). Unpublished. [UNKNOWN]
2. **V3 broadband-aperture m^2 and its fold count**, separate from the solar wings. Unpublished. [UNKNOWN]
3. **Exact Micron count per Block 2** (~220-265 band). [DERIVED, ranged]
4. **Fold-line counts for either system.** Neither SpaceX nor AST publishes a fold-line count; all fold-count statements here are inferred from tile count, area, and the AST phone-booth framing. [UNKNOWN on exact counts]

---

## Sources

- [Gunter's Space Page, Starlink Block v3.0 (~7 m x 3.5 m body, band payload)](https://space.skyrocket.de/doc_sdat/starlink-v2-0-ss.htm)
- [NextBigFuture, Starlink Gen3 ~60 m wingspan from 7-8 m base (search-surfaced; larger antennas + solar panels, 60 m x 700 m laid-together footprint)](https://www.nextbigfuture.com/2024/03/spacex-starship-launched-starlink-gen-3-unfolded-nearly-as-wide-as-the-space-station.html)
- [Grokipedia, Starlink V3 (stowed for dense stacking; dual solar arrays longer than prior gens; integrated dispensers)](https://grokipedia.com/page/Starlink_V3_satellites)
- [Skylinker, Starship 11 / Starlink V3 simulators deployment test (cargo bay + deploy-mechanism verification)](https://www.skylinker.io/p/starship-11-a-step-towards-a-new-era-of-starlink-v3-eng)
- [Gunter's Space Page, BlueWalker 3 (8x8 m, 64 m^2, ~1.5 t, modular sub-antenna tiles)](https://space.skyrocket.de/doc_sdat/bluewalker-3.htm)
- [Sky & Telescope, BlueWalker 3 unfolds (8 by 8 meters, 64 m^2, brightened 40-fold)](https://skyandtelescope.org/astronomy-news/bluewalker-3-satellite-unfolds-brightening-40-fold/)
- [AST SpaceMobile, Next-Generation BlueBird (~223 m^2 / nearly 2,400 sq ft, >3x Block 1)](https://ast-science.com/next-gen-bluebird/)
- [SatNews, BlueBird 6 deploys largest commercial array (Microns ~9 sq ft modular blocks; 10,000 Microns across ~45 sats; >3x Block 1, 10x capacity)](https://satnews.com/2025/12/24/ast-spacemobile-deploys-bluebird-6-largest-commercial-array-in-leo/)
- [AST SpaceMobile X post (Micron = building block: solar one side, antennas other)](https://x.com/AST_SpaceMobile/status/1463260467137327109?lang=en)
- [KeepTrack, AST BlueBirds "size of a studio apartment" (phone-booth-to-studio-apartment fold framing)](https://keeptrack.space/deep-dive/ast-spacemobile-bluebirds) (search-surfaced summary; page 403s to direct fetch)
- [SpaceNews, Indian rocket launches BlueBird 6 (~223 m^2, 6,100 kg, 1 per LVM3, 248-sat FCC auth)](https://spacenews.com/indian-rocket-launches-ast-spacemobiles-next-gen-bluebird-6-satellite/)
- [ScienceDirect, large space flexible solar arrays review (helical 1:9,800 stowed-to-deployed volume; Z-fold ~0.5-1.0 m^2/liter; 50-70 W/kg)](https://www.sciencedirect.com/science/article/pii/S2950104025000161)
- [ScienceDirect, stepped-deployment phased-array antenna (reflectarray packaging efficiency ~34-48%; hinge-step folding of finite-thickness panels)](https://www.sciencedirect.com/science/article/abs/pii/S009457652100641X)
- *(Per-launch fit counts, Block 2 mass, and Falcon 9 / New Glenn / LVM3 per-fairing counts cross-referenced from [`neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md); not re-listed.)*

---

## Claims ledger (COMM-197..208)

For the catalog step to ingest. Each hard claim with sources and tag.

- **COMM-197**, The Starlink V3 broadband phased-array aperture is essentially the flat satellite body itself (~7-8 m x ~3.5 m stowed) and does NOT meaningfully fold; the ~60 m "wingspan" is dominated by the deployable solar arrays, not the RF aperture. [DERIVED] Sources: Gunter's Space Page (body dims); NextBigFuture (60 m span = "antennas and solar panels"); Grokipedia (dual solar arrays, dense-stack stow).
- **COMM-198**, V3 broadband aperture deployed-to-stowed area fold ratio is ~1x (negligible aperture fold); it flat-packs and dense-stacks (PEZ dispenser), which is why it is mass-bound not size-bound on a fairing. [DERIVED] Sources: Gunter's; Skylinker (Starship 11 V3-simulator deploy test); cross-ref neutron_comms_payload_fit.md.
- **COMM-199**, Starlink V3 fold-line count and the aperture-vs-solar split of the ~60 m span are not published by SpaceX. [UNKNOWN] Source: absence across Gunter's, NextBigFuture, Grokipedia, AST/SpaceX (no datasheet).
- **COMM-200**, AST's "Micron" is the ~9 sq ft (~0.84 m^2) modular tile building block of the BlueBird array (solar cells one side, antennas the other). [FACT] Sources: AST X post; SatNews (Microns ~9 sq ft).
- **COMM-201**, BlueWalker 3 / Block 1 array is 64 m^2 deployed as an 8 m x 8 m square; implies ~76 Microns. [FACT for 8x8 m / 64 m^2; DERIVED for ~76 Microns] Sources: Gunter's BlueWalker 3; Sky & Telescope (8x8 m).
- **COMM-202**, BlueBird Block 2 array is ~223 m^2 (nearly 2,400 sq ft), >3x Block 1; implies ~220-265 Microns per satellite (area/tile-size gives ~265; AST's 10,000-Microns/~45-sats framing gives ~220). [FACT for 223 m^2; DERIVED for Micron count] Sources: AST Next-Gen BlueBird; SatNews (10,000 Microns / ~45 sats); SpaceNews.
- **COMM-203**, AST describes the satellite as folding from a stowed volume "roughly the size of a phone booth" into a flat panel "the size of a studio apartment," i.e. a deployed-area-to-stowed-footprint expansion on the order of tens of x (many fold lines), not a 2-fold. [FACT for AST framing; DERIVED for the multiple] Source: KeepTrack (AST framing, search-surfaced).
- **COMM-204**, Block 2 deploys to ~15 m on a side (square-equiv of 223 m^2) or ~17-19 m circular-equivalent, so its widest dimension must collapse ~3-4x just to clear a ~5 m fairing, with far larger area collapse (dozens of fold lines). [DERIVED] Source: geometry of 223 m^2 (COMM-202).
- **COMM-205**, Revealed fold/stow bulk: 3 Block 2 fit a Falcon 9 (5.2 m fairing) but only 1 fit a New Glenn (7 m) and 1 an LVM3 (5.0 m), showing the folded aperture stack is bulky (does not pack to a thin wafer) and is size-bound, not mass-bound (~6 t each). [FACT] Sources: cross-ref neutron_comms_payload_fit.md (Spaceflight Now, Gunter's, SpaceNews).
- **COMM-206**, Exact BlueBird Block 2 folded/stowed dimensions in meters and the exact fold-line count are not published by AST. [UNKNOWN] Source: absence across AST Next-Gen BlueBird, SpaceNews, SatNews, Gunter's.
- **COMM-207**, General rule: a thin-membrane/helical deployable antenna can stow to ~0.01% deployed volume (1:9,800) and a flexible Z-fold solar array packs to ~0.5-1.0 m^2/liter, but a deployable RF reflectarray packs only to ~34-48% efficiency; RF-aperture packing falls as rigid electronics-per-m^2 rises. [FACT] Sources: ScienceDirect flexible-solar-array review (helical 1:9,800; Z-fold 0.5-1.0 m^2/L); ScienceDirect stepped-deployment phased-array (34-48% reflectarray packaging).
- **COMM-208**, Mechanical root of the launch-fit asymmetry: V3 broadband barely folds its aperture (mass-bound, fairing-agnostic), while a direct-to-cell array must fold a many-tile accordion to reach handsets (size-bound), so the same launcher hits opposite binding constraints purely from how much the aperture folds. [DERIVED] Sources: synthesis of COMM-197..207 plus neutron_comms_payload_fit.md.
