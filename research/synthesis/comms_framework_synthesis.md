# Communications Model Framework: the Cost-per-Subscriber Chain, the Forward Comparison, and the Direct-to-Cell Spine

*Research date: June 2026. Communications research-wiki effort, wave 4 (shared library).*

**Builds on / does not duplicate:** this is the wave-4 FRAMEWORK doc. Its job is to lay out the *shape of the communications model*, in the same form as the data-center track's conclusion ([`data_center/conclusion.md`](../../data_center/conclusion.md)), and to populate that shape with the wave-4 numbers. It does NOT re-derive the inputs; every number is carried from a source doc cited by path. The load-bearing inputs are:

- The unit and the per-GB physics: [`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md) (the two-flavor ratio, the ~$480-680/sub/yr space cost, the ~$0.05-0.30/GB space figure, the marginal-cost floor), [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) (the ~$5-9/GB D2C delivery cost, the beam-saturation ceiling, the cannibalization read, the ex-China sizing).
- The capacity-to-customers bridge: [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) (generations vs bands, refarming, FR3/WRC-27, the Shannon-times-footprint asymmetry, the SCS partner/lease model), [`starlink_v3_specs.md`](../competitors/starlink_v3_specs.md) (the V3 capacity benchmark and the direct-to-cell fleet).
- The catalyst: [`comms_6g_demand_value.md`](../economics/comms_6g_demand_value.md) (the forced-cost-no-premium 6G read), [`comms_4g_5g_transition_cost.md`](../economics/comms_4g_5g_transition_cost.md) (the ground next-upgrade cost "X", the radio-refresh shape).
- The launch coupling: [`neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md) (how many comms satellites Neutron carries, and the launch-cost-per-satellite that feeds cost-per-subscriber).
- The side track: [`laser_dc_interconnect_viability.md`](../laser_comms/laser_dc_interconnect_viability.md) (the laser DC-to-DC market, separate from the RF consumer spine).
- The market and demand base: [`comms_baseline_synthesis.md`](comms_baseline_synthesis.md), [`comms_addressable_sizing.md`](../economics/comms_addressable_sizing.md).

> **Reading guide.** Every hard number is tagged **[FACT]** (sourced to 2+ independent bodies), **[FACT, single-source]** (one source only), **[ESTIMATE]** (third-party model or sizing), or **[DERIVED]** (this doc's own arithmetic on cited inputs). Sources are inline; the underlying 2+ citations live in the source docs and are not all re-pasted. China is **excluded** from every market total and appears only as a labelled aside.

> **Scope and status.** This doc is ISOLATED TO COMMUNICATIONS and renders **NO verdict** on the Rocket Lab comms business. It is a *framework*: the unit, the chain, the per-market structure, the spectrum bridge, the wave-4 numbers in their slots, the catalyst, and the open questions. It is the comms analogue of the data-center conclusion's method, not a populated model with an output ratio. The working hypotheses live in [`comms_thesis.md`](../vision/comms_thesis.md) (Revision 4 records the same framework). Read every framing as "the model shape, to be populated and tested," not as a finding.

---

## 0. The framework in one page

The data-center model has a clean spine: start from the **space cost per node**, apply a **1.5x revenue multiple** for a ~33% regular margin, then compare **forward** against a fresh ground build, yielding the 1.92x orbit-to-ground ratio ([`data_center/conclusion.md`](../../data_center/conclusion.md)). The communications model is built in the same shape, with one structural twist the data-center track never faces: in served markets the ground competitor is not a fresh build but an **incumbent defending sunk plant at marginal cost**, so the "forward comparison" forks.

The comms chain, stated once:

1. **The unit:** cost per subscriber per year, and cost per GB. (Section 1.)
2. **The chain:** space cost per subscriber, times a **1.5x revenue multiple** for an approximately 30% regular margin (revenue minus the full per-subscriber cost, not gross profit), then a **forward comparison** against what *ground must spend on its next upgrade cycle*, not against already-paid-for plant. (Section 2.)
3. **Per market:** **direct-to-cell** is the lead (Section 3.1), with home-broadband **cannibalization** as a live dynamic; **fixed broadband** is the possibly-shrinking secondary (Section 3.2); **laser DC-interconnect** is a separate side track, not part of the RF consumer spine (Section 3.3).
4. **The spectrum bridge:** Shannon caps a beam's capacity; capacity divided by customers is the cost-per-subscriber driver; spectrum is obtained by **partnering with a carrier (SCS lease)**, not by buying a cellular band. (Section 4.)
5. **The numbers, in their slots:** V3 capacity, D2C economics, the 4G-to-5G cost X, 6G demand, Neutron fit. (Section 5.)
6. **The catalyst:** the **forced 6G upgrade users will not pay a premium for**, which compresses the incumbent on the exact axis the forward comparison measures. (Section 6.)
7. **The biggest open questions.** (Section 7.)

The single most important structural difference from the data-center model, stated up front so the rest reads correctly: **a satellite beam is capacity-gated by Shannon-times-footprint and cannot densify, so cost-per-subscriber RISES with user density, the opposite of terrestrial.** ([`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) S3.1; [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) S4.) This one fact bends every part of the chain below and is why the model's unit must be density-aware.

---

## 1. The Unit: Cost per Subscriber per Year, and per GB

The model's unit is deliberately the same as the supply-cost and cost-ratio docs, so the framework plugs straight into them.

### 1.1 Cost per subscriber per year (the primary unit)

| Anchor (per subscriber per year) | Value | Status | Source |
|---|---|---|---|
| **Space all-in delivery, mature incumbent (Starlink-scale)** | **~$480-680/sub/yr** | [FACT/DERIVED] (anchored to the audited SpaceX S-1 segment margin) | [`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md) COMM-114/115 |
| of which space-specific (satellite + launch replacement) | ~$200-260/sub/yr | [ESTIMATE, single-lineage] | same |
| **Space, small new entrant (non-Starlink)** | **multiples higher** (denominator-driven; not a single number) | [ESTIMATE] | [`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md) S5.2 |
| Ground, fresh rural fiber build (annualized) | ~$875-1,540/sub/yr | [DERIVED] | [`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md) COMM-109 |
| Ground, incumbent marginal defense (served fixed broadband) | ~$84-180/sub/yr (10-20% of ARPU) | [FACT] | [`comms_incumbent_margins_competitive_floor.md`](../economics/comms_incumbent_margins_competitive_floor.md) |
| Reference ARPU: Starlink blended | ~$66-92/mo (~$790-1,104/yr); recent ~$66/mo | [FACT] | SpaceX S-1; [SpaceXChart](https://spacexchart.com/starlink); [The Information](https://www.theinformation.com/articles/spacexs-starlink-revenue-per-user-fell-18-customers-quadrupled) |
| Reference ARPU: direct-to-cell retail | ~$10/mo (~$120/yr), often free-bundled | [FACT] | [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) (Via Satellite; rvmobileinternet) |

The decisive feature of the per-subscriber unit is that **the space number is fixed-cost-dominated and denominator-driven.** The ~$480-680/sub/yr that "closes" is Starlink's disclosed 2025 actual at ~10.3M subscribers ($11.4B revenue, 38.6% operating margin) [FACT, SpaceX S-1]; the same per-subscriber cost is unreachable for a small constellation because the fixed fleet-plus-launch-plus-ground cost spreads over too few subscribers ([`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md) S5.2). **Scale is the denominator of the unit, and the entity with the scale is the incumbent.** A Rocket-Lab-scale entrant's per-subscriber cost is therefore the central unknown the model must eventually populate (Section 7, OQ1).

### 1.2 Cost per GB (the capacity unit, and the one that exposes density)

The per-GB unit is where the satellite-vs-terrestrial asymmetry shows its teeth, and the framework needs both the broadband and the direct-to-cell versions because they are different numbers.

| Service | Space cost per GB | Ground cost per GB | Ratio | Status | Source |
|---|---|---|---|---|---|
| **Direct-to-cell delivery (beam-saturated)** | **~$5-9/GB** (refined ~$5-6/GB) | terrestrial 5G ~$0.20-0.30/GB | **~17-30x** | [FACT] (single named analyst, two articles) | [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) COMM-018; [Fierce/Madden, "price per gigabyte"](https://www.fierce-network.com/wireless/space-economics-price-gigabyte-space); [Fierce/Madden, "broadband from space"](https://www.fierce-network.com/wireless/ast-spacemobile-and-problem-delivering-broadband-space) |
| **Broadband (network-average)** | ~$0.05-0.30/GB, **rising sharply at user density** | fixed broadband <$0.01/GB once plant exists; mobile ~$0.50-1.50/GB | vs fixed ~5-30x+ above; vs mobile in-range | [DERIVED/ESTIMATE] | [`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md) COMM-111 |

Two things to read off this table, because they govern the whole model:

1. **The D2C per-GB cost (~$5-9/GB) is much higher than the broadband network-average (~$0.05-0.30/GB)** because a direct-to-cell link is photon-starved (Starlink D2C runs at ~0 dB median SINR vs ~5 dB terrestrial) and beam-saturated, where a broadband dish has a high-gain antenna ([`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) S3.2; [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) S4.3). The model must not use one $/GB for both markets.
2. **The space $/GB rises with density; the terrestrial $/GB falls with density.** The same megahertz a satellite spends once over a ~4,000 km² beam is spent ~100+ times over by terrestrial cells in the same area [DERIVED, [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) S4]. This is why the per-GB axis "gets worse for space exactly in the dense markets where served competition happens" ([`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md) S3.2). The unit is not a constant; it is a function of where the subscriber is.

### 1.3 The bridge between the two units

Cost per subscriber and cost per GB are linked by **consumption**: a subscriber who pulls G GB/month at $C/GB costs roughly `12 x G x C` per year in delivery, plus the fixed per-subscriber share. For direct-to-cell the consumption is tiny (a safety-net/coverage add-on, "hundreds of kbps at best" today, demand "concentrated to specific trips" per Juniper), so the per-subscriber cost is dominated by the fixed share, not the per-GB term. For broadband the consumption is large (~360-850 GB/month per household, [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) COMM-024), so the per-GB term dominates and the density penalty bites hard. **The model should carry the unit in whichever form is binding for the market in question: per-subscriber for low-consumption D2C, per-GB for high-consumption broadband.**

---

## 2. The Chain: Space Cost x 1.5 Revenue Multiple, then a Forward Comparison

This is the comms version of the data-center spine, with the fork that defines the comms model.

### 2.1 Step one: the space cost per subscriber (the numerator)

Start from the per-subscriber cost in Section 1.1: ~$480-680/sub/yr at incumbent scale, multiples higher for a small entrant. For the direct-to-cell lead market the relevant cost is dominated by the fixed per-subscriber share plus the beam-capacity allocation, not the (tiny) per-GB consumption. This numerator is the analogue of the data-center node's full build-plus-launch-plus-operate cost.

### 2.2 Step two: the 1.5x revenue multiple for an approximately 30% regular margin

The model prices delivery at **1.5x the full per-subscriber cost**, the same dial the data-center model uses, producing an approximately **30% regular margin** (revenue minus the full per-subscriber cost, not gross profit). At Starlink's actual that dial is roughly where the incumbent already runs: a 38.6% segment operating margin implies revenue at ~1.6x the all-in delivery cost ([`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md) S5), so the 1.5x assumption is conservative against the disclosed reality, not aggressive. The multiple is the same on both sides of the comparison so the margins are held equal and the ratio that falls out is a cost ratio, exactly as in the data-center method.

> **A definitional note carried from the project's standing rule.** The ~30% is the item's REGULAR profit: revenue minus the node's full per-subscriber build-plus-launch-plus-operate cost, NOT gross profit. (Project memory, "Model profit definition.") Stated concretely: at ~$580/sub/yr cost (the midpoint), a 1.5x multiple is ~$870/sub/yr revenue and ~$290/sub/yr regular profit.

### 2.3 Step three: the FORWARD comparison (and why it forks)

The data-center model compares the orbital build forward against a **fresh ground build** (a new terrestrial data center), because in compute there is no incumbent defending an identical rack at marginal cost. Communications is different: the ground "cost to deliver" is **two numbers**, depending on whether the plant already exists ([`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md)). The forward comparison therefore forks, and which branch applies is set entirely by geography:

| Branch | Ground competitor | Forward comparison | Direction (mature space cost) |
|---|---|---|---|
| **(a) Unserved / fringe** | A **fresh** fiber/cell build | Space all-in vs annualized fresh-build cost | **Space cheaper** by ~1.3-3.2x rural, ~65-90x extreme tail [DERIVED] |
| **(b) Served / dense** | An **incumbent** on sunk plant | Space all-in vs incumbent's marginal defend cost | **Space costlier** by ~3-8x [DERIVED] |

[Both from [`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md) COMM-110/111.]

**The crucial framing move, and the reason the founder's "forward, not paid-off plant" instruction matters most here:** the *right* forward comparison is not against the incumbent's already-paid-for plant, nor against its list price, but against **what ground must spend on its next upgrade cycle.** That is the 6G radio refresh (Section 6), the cost the incumbent has not yet sunk. Framing the comparison against the *next* cycle does two things the static comparison cannot: (1) it puts both sides on a forward, not-yet-built footing, which is the only fair mirror of the data-center 1.92x; and (2) it catches the incumbent at the moment of its forced spend, when its own unit economics are deteriorating (forced 6G capex against falling ARPU). The model's headline comparison should therefore be **space all-in per subscriber vs the incumbent's per-subscriber next-upgrade (6G) cost**, with the fresh-build (branch a) and marginal-defense (branch b) numbers as the bounding cases.

### 2.4 The chain, assembled

> **space cost per subscriber (density-aware)  ->  x1.5 for ~30% regular margin  ->  compare forward against ground's NEXT-upgrade cost per subscriber (6G refresh), bounded below by a fresh-build (space wins, fringe) and above by incumbent marginal defense (space loses, dense).**

The output is not a single ratio (the founder's requested mirror of 1.92x genuinely does not exist for comms, [`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md) S4). It is a **map**: space wins on the forward cost comparison exactly where there is no sunk-plant floor (the unserved/remote fringe and the premium/sovereign layer), and loses exactly where there is one (dense served). The map and the addressable-dollars map ([`comms_addressable_sizing.md`](../economics/comms_addressable_sizing.md)) coincide, which is the load-bearing convergence the cost track already established.

---

## 3. Per Market

### 3.1 Direct-to-cell: the lead market (and the cannibalization dynamic)

**Why direct-to-cell leads.** It is the lead market for three structural reasons the corpus supports: (1) it is the segment where space has a genuine, non-substitutable product (reach an unmodified phone in a dead zone), versus broadband where it is one option among FWA/fiber/cable; (2) it is where the capital is actually flowing (SpaceX's ~$17B EchoStar spectrum buy and 15,000-satellite dedicated D2C fleet; AST's ~45 MHz Ligado deal); and (3) it carries the optionality to grow into the home-broadband wallet ([`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) S5.3).

**The unit economics, in the model's terms.** Direct-to-cell is the served sub-market where space is *least disadvantaged on coverage value* but still ~17-30x above terrestrial on raw $/GB (~$5-9/GB vs ~$0.20-0.30/GB) [FACT, Madden]. Because D2C consumption is tiny (a coverage/safety-net add-on), the per-subscriber cost is dominated by the fixed share, and the retail ARPU is thin (~$10/month, often free-bundled, with AST citing a 50/50 MNO revenue split [FACT, [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) S2.1]). So the D2C model is a **high-volume, low-ARPU, capacity-gated** line: revenue is `subscribers x ~$120/yr x satellite-operator share`, and cost is `subscribers x (fixed per-sub share + small per-GB term)`, with the binding constraint being how many subscribers fit under a fixed-capacity beam.

**The cannibalization dynamic (home broadband).** This is the live strategic question and the reason D2C may be larger than home broadband. The honest, physics-bounded read ([`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) S4):

- **D2C cannibalizes the home connection at the EDGE, not the CORE, and the boundary is set by beam-saturation physics, not consumer preference.** Where a home is rural/remote, single-occupant, light-usage, or already satellite-served, a good-enough D2C phone can collapse the dedicated home line (and even the dish) into the device. Where a home is urban/suburban, indoor, multi-occupant, heavy-usage, the ~17-30x per-GB gap and the indoor/density limits keep the fixed line in place. D2C "will likely never work" indoors or in dense urban areas [FACT, WIA].
- **A second-order cannibalization comes first:** D2C may eat satellite fixed broadband (Starlink dishes) and standalone messaging before it touches terrestrial home broadband ([`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) S4.3). That is intra-space wallet-splitting, not enlargement against terrestrial.
- **The model implication:** do not model D2C as eating the ~$129B fixed-broadband-class wallet; model it as eating the *thin-edge* slice plus the standalone coverage/messaging market, with optionality on more **if and only if** 6G-era capacity narrows the per-GB gap. The "D2C is the larger market" hypothesis is a bet on capacity physics improving, not a current fact ([`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) S5.2).

**Sizing the lead market (ex-China).** Near-term D2C served revenue converges at **~$12-14B by 2030-31** across four independent houses (Omdia ~$12B / 411M MAU; Juniper 133M MAU by 2031, usage "lower than anticipated"; ABI $11.6B; Mordor $13.8B) [FACT]. That is ~10x smaller than the ~$129B fixed-broadband-class served slice on near-term revenue, but the D2C *addressable base* (~5.5B out-of-coverage-capable phones, ~$1.1T cited ceiling) is far larger, and the 10-year optionality is the forward thesis ([`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) S5).

### 3.2 Fixed broadband: the possibly-shrinking secondary

Fixed broadband is the secondary market, and the model should treat it as **possibly shrinking** for two reasons. First, it is the market D2C may cannibalize at the edge (Section 3.1). Second, on its own merits it is a diminishing-returns business: willingness-to-pay for speed is sharply concave (~$2.34/Mbps at 4-10 Mbps collapsing to ~$0.02/Mbps at 100-1,000 Mbps), gigabit is available to >91% of US homes but bought by only ~30%, and ARPU is flat-to-declining ([`comms_baseline_synthesis.md`](comms_baseline_synthesis.md) S4.1) [FACT]. In the model's terms, fixed broadband is where space loses the forward cost comparison in served territory (branch b, ~3-8x above the marginal floor; ~5-30x+ on $/GB) and wins only in the unserved fringe (branch a). It is a real but *defended and shrinking-at-the-edge* secondary line, not the lead.

The Starlink V3 benchmark (Section 5.1) is the frontier of this secondary market: ~1 Tbps/sat, gigabit-to-a-user, ~12M+ subscribers. It is the cost-and-capacity yardstick a fixed-broadband space line is measured against, and it is Starship-bound (Section 5.5), which is the launch-coupling constraint for any Neutron-scale entrant.

### 3.3 Laser DC-interconnect: a separate side track

Laser (free-space optical) data-center-to-data-center interconnect is **not part of the RF consumer spine** and is modeled as a separate side track ([`laser_dc_interconnect_viability.md`](../laser_comms/laser_dc_interconnect_viability.md)). The framework records it here so the model does not conflate it with direct-to-cell or broadband:

- **Terrestrial laser DCI is a narrow supplement, not the backbone.** The headline AI-DCI job needs petabit-scale capacity (~5 Pbit/s within a region) met by trenched coherent fiber; a commercial free-space-optical link carries ~25 Gbps, two-to-five orders of magnitude short [FACT]. Laser's terrestrial role is gap-fill, route-diversity, obstacle-hop, and secure/fast-deploy, each measured in tens of Gbps.
- **The orbital case flips:** in space there is no fiber to compete with, so laser ISL is the only credible medium and is proven at scale (Starlink ~27,000 space lasers). This is the one arena where direct laser links between data centers are the primary architecture, and it is the natural home for Rocket Lab's Mynaric optical-terminal asset ([`laser_dc_interconnect_viability.md`](../laser_comms/laser_dc_interconnect_viability.md) S6).
- **Model treatment:** a separate, bandwidth-gated, point-to-point line with a different unit (per-link Gbps and per-route pricing, not per-subscriber), addressed to a different buyer (orbital-DC operators, hyperscalers needing redundancy), and explicitly out of the consumer cost-per-subscriber chain. It connects the comms track back to the orbital data-center thesis but does not belong in the RF spine's math.

---

## 4. The Spectrum Capacity-to-Customers Bridge

This is the engine room of the model: the link from Shannon to cost-per-subscriber, and the spectrum-access decision that sets the capacity ceiling.

### 4.1 Shannon caps the beam; capacity / customers is the cost driver

A satellite beam carries `capacity = bandwidth x log2(1 + SNR)`, shared across every customer in its footprint ([`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) S4; [`comms_baseline_synthesis.md`](comms_baseline_synthesis.md) S3.1). The cost-per-subscriber driver is then **fixed beam capacity divided by the number of customers under the beam**: more customers under a fixed-capacity beam means less capacity each, so to hold a per-user experience you must cap subscribers per beam, which caps revenue per beam against a fixed beam cost. This is the inversion that defines the model:

> **Terrestrial adds capacity by adding cells (densification), so cost-per-subscriber FALLS with density. A satellite cannot densify below its aperture-and-altitude beam-size limit, so cost-per-subscriber RISES with density.** ([`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) S4.3-4.4; [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) S3.1.)

The measured anchors that bound the bridge (Section 5.1 has the full table): a Starlink D2C beam delivers ~3.1 Mbps on a 2x5 MHz channel (~0.52-0.61 bps/Hz); AST targets up to 120 Mbps/cell on 40 MHz; a terrestrial mid-band macro delivers ~750 Mbps to 5.6 Gbps/cell. Normalized to area, terrestrial delivers ~300x (vs AST) to ~30,000x (vs Starlink D2C) more bits/s per km² [DERIVED, [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) COMM-23]. **Space direct-to-cell is therefore a coverage layer, not a capacity layer, and the model must price it per-subscriber under a fixed-capacity beam.**

### 4.2 More bandwidth is the lever, and it is bought, not free

The measurement data makes the spectrum-to-capacity link almost linear: Starlink's per-beam throughput scales with bandwidth (~3.1 Mbps on 2x5 MHz PCS, ~6.2 Mbps with H-Block added, ~18.6 Mbps aggregate at full holdings) [FACT, single technical source]; AST's ~120 Mbps comes from ~40 MHz, roughly 8x the bandwidth ([`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) S2.3). **More MHz is the capacity lever,** which is why ~$17B (SpaceX/EchoStar) and ~45 MHz (AST/Ligado) changed hands. The generation label (4G/5G/6G) and the band are orthogonal: a satellite speaks whichever *standard* the partner's handsets expect over whatever *band* it leases ([`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) S1).

### 4.3 The carrier-partnership spectrum model (the SCS lease, the realistic door)

The single most decision-relevant finding for the model's spectrum input: a new space entrant accesses cellular spectrum by **partnering with a carrier under the FCC's Supplemental Coverage from Space (SCS) framework**, leasing the carrier's already-licensed band as a gap-filler, NOT by buying its own cellular band ([`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) S5).

| Path | Mechanism | Who does it | Cost shape | Handset compatibility |
|---|---|---|---|---|
| **Partner / lease (SCS)** | Ride a carrier's licensed band under an SCS lease; satellite is a gap-filler | AST (AT&T/Verizon 850 MHz), Starlink D2C (T-Mobile PCS G-block) | Commercial deal / revenue share; near-zero spectrum capex | **Instant**: phones already support the band/standard |
| **Buy outright** | Acquire your own cellular licenses on the secondary market | SpaceX next-gen (~$17B EchoStar AWS-4/H/AWS-3) | Tens of billions; hyperscale-only | Must align bands/handsets yourself |

[FACT, [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) S5.5.]

**For the model:** the spectrum input is not "what does a cellular band cost to buy" but "what are the commercial terms of an SCS partnership, and what fraction of a carrier's band do you get to ride." A realistic entrant rides a partner's band (instant handset compatibility, near-zero spectrum capex), and the capacity that band delivers from orbit is then gated as in Section 4.1: a few Mbps to ~120 Mbps per large beam, a coverage layer. The SpaceX ~$17B buy is the hyperscale exception, not the entry path. **This is the spectrum-as-moat hypothesis stated as a model input:** the players who matter are spending billions to own dedicated D2D spectrum precisely because the borrowed slice is too thin to lift throughput past messaging, so an entrant's capacity ceiling is a spectrum-access question first and a satellite question second.

### 4.4 The forward spectrum opening: FR3 / 7-15 GHz at WRC-27

The one greenfield not yet filed is the **upper mid-band FR3 (7.125-24.25 GHz)**, with WRC-23 having teed up 4.4-4.8, 7.125-8.4, and 14.8-15.35 GHz as IMT study bands for identification at **WRC-27**; the 7-15 GHz range can offer >400 MHz per operator versus ~100 MHz in today's mid-band [FACT, [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) COMM-13/14]. For the ten-year model this is the genuine forward opening, but it cuts two ways: more bandwidth per operator is attractive, while higher frequency means narrower beams and more path loss, which is *harder* for a wide-footprint phone-to-LEO link (Section 7, OQ4). Whether FR3 is reachable from orbit for direct-to-cell is unresolved and central to the forward view.

---

## 5. The Wave-4 Numbers, in Their Slots

This section places each wave-4 number where the model uses it. The numbers are carried, not re-derived.

### 5.1 V3 capacity (the frontier RF benchmark)

| Metric | V3 value | Multiple vs V2 mini | Status | Source |
|---|---|---|---|---|
| Downlink/sat | ~1 Tbps (1,000+ Gbps) | ~10-13x | [FACT] | [`starlink_v3_specs.md`](../competitors/starlink_v3_specs.md) COMM-1 |
| Uplink/sat | ~160-200 Gbps | ~3-4x | [FACT] | same COMM-2 |
| Per Starship launch | ~60 Tbps (~60 sats) | >20x per launch | [FACT] | same COMM-4 |
| Mass | ~1,900-2,000 kg (catalog ~1,200) | ~3.3x | [FACT/ESTIMATE] | same COMM-6 |
| System capacity today | ~450 Tbps (end-2025), ~12M+ subs | (rising to multi-Pbps) | [FACT] | same COMM-15/17 |
| **Direct-to-cell V3 fleet** | up to 15,000 sats, ~700+ Gbps/sat target, ~65 MHz EchoStar spectrum | >100x V2 D2C | [FACT (filing); ESTIMATE (700 Gbps)] | same COMM-18/19 |

**Model use:** V3 is the capacity yardstick the broadband secondary line is measured against, and the dedicated 15,000-satellite D2C fleet is the structural proof that the frontier player is betting on direct-to-cell as the lead market. The capacity jump is ~10x per satellite bought with ~3.3x mass and an ~8x-cheaper-per-bit launch, but **the >20x-per-launch economics are Starship-bound** ([`starlink_v3_specs.md`](../competitors/starlink_v3_specs.md) S2), which is the launch-coupling the model must respect for any Neutron-scale entrant (Section 5.5).

### 5.2 Direct-to-cell economics (the lead-market unit)

| Metric | Value | Status | Source |
|---|---|---|---|
| Delivery cost per GB | ~$5-9/GB (refined ~$5-6/GB) | [FACT, single analyst, two articles] | [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) COMM-018 |
| Terrestrial 5G per GB (the benchmark it is measured against) | ~$0.20-0.30/GB | [FACT] | same |
| Retail ARPU | ~$10/mo, often free-bundled | [FACT] | same COMM-14 |
| Per-beam throughput (Starlink, current) | ~3.1 Mbps on 2x5 MHz | [FACT, single technical] | same COMM-9 |
| Per-cell throughput (AST, target) | up to ~120 Mbps on 40 MHz | [FACT] | same COMM-2 |
| Near-term served revenue (ex-China) | ~$12-14B by 2030-31 | [FACT, 4 houses] | same COMM-023 |
| Addressable base | ~5.5B out-of-coverage-capable phones; ~$1.1T cited ceiling | [FACT] | same COMM-025 |

**Model use:** these are the inputs to the per-subscriber chain for the lead market (Section 3.1): thin ARPU, high $/GB, capacity-gated subscribers-per-beam, large addressable base, small near-term served revenue.

### 5.3 The 4G-to-5G cost X (the ground next-upgrade hurdle)

| Metric | Value | Status | Source |
|---|---|---|---|
| Per-operator incremental 5G mid-band deployment capex | Verizon ~$10B / ~7,000-8,000 sites; AT&T ~$6-8B; T-Mobile ~$10-15B (5G slice) | [FACT] | [`comms_4g_5g_transition_cost.md`](../economics/comms_4g_5g_transition_cost.md) claims 1/6/10 |
| Per-site radio upgrade cost | ~$20-50k/site (Massive MIMO radio on existing tower) | [FACT] | same (cross-checked [PatentPC](https://patentpc.com/blog/5g-infrastructure-costs-what-telcos-are-paying)) |
| RAN/radio share of deployment capex | ~55-65% of network-deployment capex | [FACT, direction] | same claim 18 |
| Ex-China global 5G deployment envelope | ~$700-800B (2020-2025) | [DERIVED] | same claim 25 |
| Shape of the cost | a new RADIO refresh on (mostly) existing sites, not new sites | [FACT] | same S2 |

**Model use:** X is the cost a space alternative must beat **on the ground's next upgrade cycle**, not against paid-off plant (Section 2.3). The load-bearing finding is its *shape*: the 5G cycle's deployment cost was carried overwhelmingly by new radio hardware on existing sites (~$20-50k/site, ~55-65% of deployment capex), not by new sites, the core, or (in cash-capex terms) spectrum. The 6G cycle will be the same shape (Section 6). So **X-on-the-next-cycle ≈ the per-POP/per-subscriber cost of the next radio refresh**, plus whatever new 6G spectrum is auctioned, possibly plus densification if 6G pushes higher in frequency ([`comms_4g_5g_transition_cost.md`](../economics/comms_4g_5g_transition_cost.md) S7).

### 5.4 6G demand (the no-premium finding that makes X a forced cost)

| Metric | Value | Status | Source |
|---|---|---|---|
| Consumers unwilling to pay >5 euros/mo for 10x speed | ~two-thirds | [FACT] | [`comms_6g_demand_value.md`](../economics/comms_6g_demand_value.md) claim 7 |
| Consumers who would pay extra for 5G at all | ~one-third, averaging ~$4.40-5.06/mo | [FACT] | same claim 8 |
| Consumers who could not tell 4G from 5G | 54% | [FACT, single dataset/2 outlets] | same claim 10 |
| 5G ARPU premium delivered | none; ARPU declining ~1.3-2%/yr through 2028 | [FACT] | same claim 12 |
| First commercial 6G | late-2029 to 2030; specs (Release 21) end-2028 | [FACT] | same claim 5 |

**Model use:** this is what makes X a *forced* cost rather than a demand-funded one. Users will not pay a premium for the next G (the $10/month test answers "almost certainly not"; the proxy ceiling was ~$5 and the realized premium was ~0), so the incumbent must spend X with no matching revenue line. This is the catalyst (Section 6).

### 5.5 Neutron fit (the launch coupling that feeds cost-per-subscriber)

| Payload | Sats per Neutron launch | Launch $ per satellite (~$52M launch) | Binding gate | Status | Source |
|---|---|---|---|---|---|
| Starlink V3-class (broadband) | ~5 (DRL/SSO), ~6-7 to LEO | ~$10-11M/sat | **Mass** | [DERIVED] | [`neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md) claims 19/21 |
| BlueBird Block 2-class (direct-to-cell) | ~1 (optimistically 2) | ~$50-55M/sat | **Stowed size (antenna)** | [DERIVED] | same claims 20/21 |

**Model use:** satellites-per-launch sets launch-cost-per-satellite, a first-order input to constellation cost and thence cost-per-subscriber. The asymmetry is the point: for broadband Neutron is mass-bound and carries ~1/12 of a Starship's V3 batch (~10x worse on $/satellite); for the lead market (direct-to-cell) the giant antenna is the binding constraint and Neutron's 5.5 m fairing pins it near ~1 satellite per launch. **Neutron's plausible comms role is therefore not matching mega-constellation launch economics but serving smaller or stow-optimized satellites, dedicated/responsive insertions, or a block-upgraded path** ([`neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md) S5). This sets the constraint the cost-per-subscriber model must respect; it is not a verdict.

---

## 6. The Catalyst: the Forced 6G Upgrade Users Will Not Pay a Premium For

The catalyst is the single dynamic that makes the forward comparison favorable on the axis the model measures, and it is stated as a working hypothesis, not a verdict.

**The mechanism, in three steps** ([`comms_6g_demand_value.md`](../economics/comms_6g_demand_value.md) S3; [`comms_4g_5g_transition_cost.md`](../economics/comms_4g_5g_transition_cost.md) S7):

1. **Demand plateaus.** Users will not pay a premium for "more G" (Section 5.4): ~two-thirds balk above 5 euros/month even for a 10x speed jump; 5G delivered no ARPU premium and ARPU is falling ~1.3-2%/yr. The marginal-value-per-generation curve has flattened to near zero for the typical consumer.
2. **Capacity cost is forced anyway.** 6G is a supply-push driven by traffic growth, competitive parity, and vendors/governments, not a demand-pull. An independent analyst: "Even if you erased the label '6G,' operators would still need to add spectrum where available, extend fiber backhaul, and multiply sites in hot zones... More cars, more lanes. You cannot avoid building it." Operators say so openly ("do our customers really need another G?", Orange; those "footing the bill just want to get off", Light Reading). Corroborated by 2026 trade press ([The Register, "don't repeat 5G mistakes with 6G"](https://www.theregister.com/networks/2026/06/03/dont-repeat-5g-mistakes-with-6g-plead-mobile-operators/5250572); [TelecomTV, 6G "last chance"](https://www.telecomtv.com/content/6g/6g-is-the-last-chance-for-operators-to-take-back-control-55618/amp/); [IEEE Spectrum, capacity limits drive a 6G infrastructure focus](https://spectrum.ieee.org/6g-network-infrastructure-bell-labs)).
3. **Therefore the incumbent's per-subscriber economics deteriorate on the next cycle.** Forced 6G capex (the radio-refresh X, ~$20-50k/site, ~55-65% of deployment capex, landing ~2030-2035) against declining ARPU compresses the incumbent on exactly the cost the forward comparison measures.

**Why this matters for the model.** The forward comparison (Section 2.3) is against ground's *next* upgrade, and the catalyst says that next upgrade is one the incumbent must do without a revenue offset. So the benchmark the space alternative races is a target whose own unit economics are *worsening*, not improving. Three consequences ([`comms_6g_demand_value.md`](../economics/comms_6g_demand_value.md) S3.3):

- The cost-down hurdle is measured against a rising-cost, falling-revenue incumbent.
- 6G does not unlock a consumer premium a space entrant would have to match (if it had created a $10/month premium for peak speed, space would face a higher bar; it has not, and the evidence says it will not).
- The one axis 6G monetization is chasing (guaranteed reliability/experience, differentiated connectivity worth ~5-12% ARPU uplift) is the axis the corpus already says coverage-oriented supply wins on (reach, reliability), not raw bandwidth.

**Stated as a hypothesis:** the demand environment a space comms business would enter ~2030 is favorable in exactly the way the founder framed: 6G is a cost ground must bear that users will not fund, which compresses the incumbent and shifts competition onto the axes a cheaper alternative can contest. Whether a *space* business captures this depends on its own cost stack (the scale/denominator question, Section 7), which the catalyst does not resolve.

---

## 7. The Biggest Open Questions

These are the framework-level open questions, the ones that decide whether the model, once populated, produces a favorable or unfavorable map. The input-level questions live in the source docs.

1. **The entrant-specific (non-Starlink) cost per subscriber.** The ~$480-680/sub/yr that "closes" is Starlink's incumbent-scale actual; a Rocket-Lab-scale constellation's per-subscriber cost is "multiples higher" but unquantified. This is the single number that converts the framework into a populated model, and it is denominator-driven (how many subscribers spread the fixed cost). ([`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md) OQ3.)
2. **The SCS partnership commercial terms.** The capacity input depends on what fraction of a carrier's band an entrant rides and the per-subscriber revenue split (AST cites 50/50; the realized satellite-operator ARPU after the carrier's half and free-bundling is not cleanly public). ([`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) OQ1; [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) OQ3.)
3. **The sustained (not peak) per-user throughput under realistic beam loading.** The 150 Mbps (Starlink) and 200 Mbps (AST) figures are single-user, full-beam, line-of-sight peaks. The number that decides home-broadband cannibalization is the *sustained shared* rate when a beam carries hundreds of users; no operator has disclosed it. ([`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) OQ2.)
4. **Whether FR3 / 7-15 GHz is reachable from orbit for direct-to-cell.** The forward spectrum opening (more bandwidth per operator) is upper mid-band, which means narrower beams and more path loss, harder for a wide phone-to-LEO link. Whether the 6G-era greenfield helps or hurts a space D2C play is central to the ten-year view. ([`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) OQ3.)
5. **Whether 6G forces densification (the swing in X).** If 6G capacity comes from more-advanced antennas on existing macro sites (the 5G pattern), X stays bounded; if it requires upper-mid-band/cmWave small-cell densification, X rises sharply, *widening* the window for a space alternative. The forward comparison should run both bounds. ([`comms_4g_5g_transition_cost.md`](../economics/comms_4g_5g_transition_cost.md) OQ2.)
6. **The D2C-vs-fixed-broadband cannibalization timeline.** The "D2C is the larger market" hypothesis hinges on when 6G-era NTN capacity rises enough for the phone to credibly substitute for the home line beyond the thin edge. This is the single most important unknown for the lead-market sizing, and it is a capacity-physics date, not a demand date. ([`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) OQ5.)
7. **A hard space cost-per-GB at next-gen spectrum.** The ~$5-9/GB D2C figure predates the EchoStar ~65 MHz and Gen2 ~100 Gbps satellites; a re-derived $/GB at full spectrum and tighter beams would tell the model how far the ~17-30x gap actually narrows, and whether D2C ever crosses below the terrestrial mobile marginal floor in any served setting. ([`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) OQ1.)
8. **Single-operator capture share.** The whole framework sizes a contestable pie (~$45-150B addressable, ~$12-14B near-term D2C); what share a specific entrant wins against the scaled incumbent is the competitive-share question no cost or demand doc answers. ([`comms_addressable_sizing.md`](../economics/comms_addressable_sizing.md) OQ3.)

---

## 8. What This Framework Is, and Is Not

**It is:** the shape of the communications model, in the same form as the data-center conclusion's method (cost per unit, times a 1.5x multiple, compared forward against ground's next-upgrade cost), with the wave-4 numbers placed in their slots, the direct-to-cell lead and the cannibalization dynamic made explicit, the spectrum-to-customers bridge laid out, the carrier-partnership (SCS) spectrum model stated as the realistic input, and the forced-6G catalyst recorded as the dynamic that makes the forward comparison favorable on the model's axis.

**It is not:** a populated model with an output ratio. The founder's requested single mirror of the data-center 1.92x genuinely does not exist for comms (the forward comparison forks on whether ground plant exists), so the output is a *map*, not a number. The entrant-specific cost per subscriber, the SCS terms, the sustained per-beam rate, and the competitive share are all open (Section 7), and until they are populated the framework produces structure, not a verdict. **No judgment on the Rocket Lab comms business is made here.**

---

## Sources

*Wave-4 source docs (each carries its own underlying 2+ citations inline)*
- [`research/economics/comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md)
- [`research/economics/comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md)
- [`research/direct_communication/spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md)
- [`research/competitors/starlink_v3_specs.md`](../competitors/starlink_v3_specs.md)
- [`research/economics/comms_6g_demand_value.md`](../economics/comms_6g_demand_value.md)
- [`research/economics/comms_4g_5g_transition_cost.md`](../economics/comms_4g_5g_transition_cost.md)
- [`research/rocket_lab/neutron/neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md)
- [`research/laser_comms/laser_dc_interconnect_viability.md`](../laser_comms/laser_dc_interconnect_viability.md)

*Base docs grounded in*
- [`research/synthesis/comms_baseline_synthesis.md`](comms_baseline_synthesis.md)
- [`research/economics/comms_addressable_sizing.md`](../economics/comms_addressable_sizing.md)
- [`data_center/conclusion.md`](../../data_center/conclusion.md) (the method mirror)

*Direct verification for this framework (wave-4 anchor confirmations)*
- [Fierce/Madden, the price per gigabyte in space (D2C ~$5-6/GB vs 5G ~$0.20-0.30/GB)](https://www.fierce-network.com/wireless/space-economics-price-gigabyte-space)
- [Fierce/Madden, AST and the problem of delivering broadband from space ($5-9/GB, ~20x)](https://www.fierce-network.com/wireless/ast-spacemobile-and-problem-delivering-broadband-space)
- [SpaceXChart, Starlink unit economics (~$92/mo blended FY2025, 38.6% operating margin, ~10.3M subs)](https://spacexchart.com/starlink)
- [The Information, Starlink revenue per user fell 18% as customers quadrupled](https://www.theinformation.com/articles/spacexs-starlink-revenue-per-user-fell-18-customers-quadrupled)
- [PatentPC, 5G infrastructure costs (~$20-50k per existing-site radio upgrade)](https://patentpc.com/blog/5g-infrastructure-costs-what-telcos-are-paying)
- [The Register, don't repeat 5G mistakes with 6G (operators plead)](https://www.theregister.com/networks/2026/06/03/dont-repeat-5g-mistakes-with-6g-plead-mobile-operators/5250572)
- [TelecomTV, 6G is the last chance for operators to take back control](https://www.telecomtv.com/content/6g/6g-is-the-last-chance-for-operators-to-take-back-control-55618/amp/)
- [IEEE Spectrum, capacity limits in 5G prompt a 6G focus on infrastructure](https://spectrum.ieee.org/6g-network-infrastructure-bell-labs)

---

## Confidence

- **The framework structure (the unit, the chain, the fork, the per-market split, the spectrum bridge): high.** It is a faithful assembly of the data-center method and the wave-1-to-4 source docs; each structural claim traces to a sourced doc.
- **The wave-4 numbers in their slots: inherited.** Each carries the confidence of its source doc; the D2C $/GB and the V3 capacity figures are medium-high (multi-source or single-named-analyst corroborated in direction), the entrant-specific cost is explicitly open.
- **The catalyst (forced-6G-no-premium): medium-high as a hypothesis.** The demand-side no-premium finding is the corpus's most robust result (now corroborated by 2026 trade press); the forced-cost framing is well-supported but stated as a working hypothesis, not a verdict.
- **The output: deliberately withheld.** This is a framework, not a populated model; the map (space wins on the forward comparison in the unserved/fringe and premium/sovereign, loses in dense served) is high-confidence as a *direction*, and the per-subscriber numbers that would turn it into a ratio are open.

---

## Claims ledger

For the catalog step to ingest (no COMM- IDs assigned here, per the lead's instruction). Each hard claim with its 2+ independent sources; single-source and derived claims are flagged. Claims already held in wave-1-to-3 docs (the ~$480-680/sub/yr space cost, the two-flavor ratio, the addressable pool, the ARPU-premium-absence, etc.) are referenced here and should be reconciled to their existing COMM- ids rather than duplicated; the genuinely new framework-level claims are below.

1. **The comms model unit is cost per subscriber per year and per GB, density-aware: space cost-per-subscriber RISES with user density (Shannon-times-footprint, no densification), the inverse of terrestrial.** Sources: [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) S4 (techneconomyblog; arXiv 2506.00283); [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) S3.1 (WIA; Madden/Fierce). [DERIVED from sourced inputs]
2. **Direct-to-cell delivery costs ~$5-9/GB (refined ~$5-6/GB) versus terrestrial 5G ~$0.20-0.30/GB, ~17-30x higher.** Sources: [Fierce/Madden "price per gigabyte"](https://www.fierce-network.com/wireless/space-economics-price-gigabyte-space); [Fierce/Madden "broadband from space"](https://www.fierce-network.com/wireless/ast-spacemobile-and-problem-delivering-broadband-space). [FACT, single named analyst across two articles]
3. **The model chain is: space cost per subscriber x 1.5 revenue multiple (for ~30% regular margin) compared FORWARD against ground's next-upgrade cost, not paid-off plant; the forward comparison forks on whether ground plant already exists.** Sources: [`data_center/conclusion.md`](../../data_center/conclusion.md) (the 1.5x/forward method); [`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md) (the two-flavor fork). [DERIVED, framework synthesis]
4. **The 1.5x revenue multiple is conservative against Starlink's disclosed actual (38.6% operating margin implies revenue at ~1.6x all-in delivery cost).** Sources: [SpaceXChart](https://spacexchart.com/starlink); [`comms_ground_vs_space_cost_ratio.md`](../economics/comms_ground_vs_space_cost_ratio.md) S5 (SpaceX S-1). [DERIVED]
5. **Direct-to-cell is the model's lead market (non-substitutable product, where the capital is flowing, carries the cannibalization optionality); D2C cannibalizes home broadband at the EDGE not the CORE, bounded by beam-saturation physics.** Sources: [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) S4-S5 (WIA; Opensignal; Omdia; Juniper). [FACT (consensus) / ESTIMATE (the boundary read)]
6. **Near-term direct-to-cell served revenue ex-China is ~$12-14B by 2030-31 (Omdia ~$12B/411M MAU; Juniper 133M MAU by 2031; ABI $11.6B; Mordor $13.8B), against a ~5.5B-device / ~$1.1T addressable ceiling.** Sources: [Omdia](https://omdia.tech.informa.com/pr/2026/mar/smartphone-satellite-direct-to-device-service-revenue-to-approach12-billion-dollars-by-2030); [ComputerWeekly/Juniper](https://www.computerweekly.com/news/366643796/Direct-to-cell-growth-hits-headwinds-while-6G-set-for-rapid-uptake); plus [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) COMM-021/022/023/025. [FACT (multi-house) / DERIVED (the convergence)]
7. **The spectrum input is a carrier-partnership (FCC SCS lease), not a band purchase: a satellite rides a carrier's licensed band as a gap-filler with instant handset compatibility and near-zero spectrum capex; buying spectrum outright (SpaceX ~$17B EchoStar) is the hyperscale exception.** Sources: [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) S5 (Federal Register SCS; FCC DA-24-1193; EchoStar 8-K). [FACT]
8. **More MHz is the capacity lever (Starlink per-beam throughput scales near-linearly with bandwidth: ~3.1 Mbps on 2x5 MHz to ~18.6 Mbps aggregate at full holdings; AST ~120 Mbps on ~40 MHz), which is why ~$17B and ~45 MHz changed hands.** Sources: [`comms_direct_to_cell.md`](../economics/comms_direct_to_cell.md) S2.3 (arXiv 2506.00283); [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) S4 (AST; arXiv). [FACT]
9. **The forward spectrum opening is FR3 / 7-15 GHz at WRC-27 (>400 MHz/operator vs ~100 MHz today), the one greenfield not yet filed, but it is upper mid-band (narrower beams, more path loss) and its reachability from orbit for direct-to-cell is unresolved.** Sources: [`spectrum_generations_and_availability.md`](../direct_communication/spectrum_generations_and_availability.md) COMM-13/14 (Samsung Research; Nokia; CTU; Enterprise IT World). [FACT (the bands) / open (orbital reachability)]
10. **The ground next-upgrade cost X is a new RADIO refresh on existing sites (~$20-50k/site, ~55-65% of deployment capex), not new sites; the 6G cycle (~2030-2035) repeats this shape.** Sources: [`comms_4g_5g_transition_cost.md`](../economics/comms_4g_5g_transition_cost.md) claims 14/16/18 (Ericsson; STL Partners); [PatentPC](https://patentpc.com/blog/5g-infrastructure-costs-what-telcos-are-paying) (~$20-50k/site). [FACT]
11. **The catalyst is the forced 6G upgrade users will not pay a premium for: ~two-thirds of users balk above 5 euros/mo even for 10x speed, 5G delivered no ARPU premium (ARPU falling ~1.3-2%/yr), yet 6G capex is forced by traffic/parity physics ("you cannot avoid building it"), so the incumbent's per-subscriber economics deteriorate on the next cycle.** Sources: [`comms_6g_demand_value.md`](../economics/comms_6g_demand_value.md) claims 7/8/12/14/15 (McKinsey; PwC; Telecoms.com; Light Reading; Orange); corroborated [The Register](https://www.theregister.com/networks/2026/06/03/dont-repeat-5g-mistakes-with-6g-plead-mobile-operators/5250572), [TelecomTV](https://www.telecomtv.com/content/6g/6g-is-the-last-chance-for-operators-to-take-back-control-55618/amp/), [IEEE Spectrum](https://spectrum.ieee.org/6g-network-infrastructure-bell-labs). [FACT (the demand finding) / hypothesis (the forced-cost framing)]
12. **Neutron carries ~5 V3-class broadband satellites per launch (mass-bound, ~$10-11M/sat) and ~1 direct-to-cell BlueBird-Block-2-class satellite per launch (antenna-stow-bound, ~$50-55M/sat); the >20x-per-launch V3 economics are Starship-bound, so Neutron's comms role is smaller/stow-optimized satellites or dedicated insertion, not mega-constellation launch economics.** Sources: [`neutron_comms_payload_fit.md`](../rocket_lab/neutron/neutron_comms_payload_fit.md) claims 19/20/21; [`starlink_v3_specs.md`](../competitors/starlink_v3_specs.md) COMM-4/24. [DERIVED]
13. **Laser DC-interconnect is a separate side track from the RF consumer spine: terrestrial laser is a tens-of-Gbps supplement (the petabit AI-DCI backbone is trenched fiber), while orbital DC-to-DC laser is the primary architecture (no fiber in space); it uses a per-link, not per-subscriber, unit and a different buyer.** Sources: [`laser_dc_interconnect_viability.md`](../laser_comms/laser_dc_interconnect_viability.md) S2/S6 (SemiAnalysis; Taara/Tom's Hardware; optical_comms). [FACT]
