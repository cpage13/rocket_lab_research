# The AI-1 Comparison

*Companion to the [conclusion](conclusion.md) (the numbers) and the [structural case](structural_case.md) (the why), source-linked through the [assumptions](assumptions.md). On June 8, 2026, SpaceX revealed AI-1, its orbital AI data-center satellite. This document makes one assumption, once: AI-1's specs are real, and a Neutron node is built to them. AI-1 is an unflown design revealed three days before SpaceX's IPO; every AI-1 figure here comes from that reveal ([sources](../research/competitors/starship_addendum.md)). Said once, not repeated.*

**The short version: AI-1 validated the architecture, and the model now runs it.** When AI-1 was revealed, it matched our model where the model was well grounded (silicon, solar area) and beat it in exactly one place: the radiator. As of 2026-07-14 the default semi-copies that radiator (a deployed, double-sided, run-hot wing within 10 percent of AI-1's implied mass), which moved the default from 1.92x ground to about **1.28x**. What remains of the bracket is silicon and structure: build the node to AI-1's full spec, pinned 2026 silicon and its lighter solar and bus, and the same model at the same cost dials reads about **0.91x, below ground parity**. Even that bracket counts none of the unpriced levers (the learning curve, the margin on the buy-priced lines, premium revenue): the upside inventory lives in [the structural case](structural_case.md).

## The Numbers

Same model, same 12.5 t envelope, same costs, same launch prices; only AI-1's remaining dials swapped in (pinned B300/GB300 silicon, 0.003 t/kW solar, a 0.10 t bus; the scenario ships as [`code/scenarios/ai1_equivalent.yaml`](../code/scenarios/ai1_equivalent.yaml); the default stays the only promoted model). The node is not a single AI-1: it packs about six to seven AI-1s' worth of hardware into one launch. A node is one orbital data-center unit, one per Neutron launch, and each launch year's cohort earns a fixed margin over its five-year life. By launch year (first launches in 2027; verified runs):

| Launch year | Launches | Cohort revenue/yr: default | Cohort revenue/yr: AI-1-spec |
|---|---:|---:|---:|
| 2027 | 2 | $38M | $60M |
| 2029 | 5 | $132M | $149M |
| 2032 | 22 | $596M | $614M |
| 2036 | 90 | $2.52B | $2.37B |

The AI-1-spec cohorts out-earn the default early (about 1.6x in 2027) and fall slightly behind it by 2036, because the default's frontier silicon path grows more expensive and more capable while AI-1's pinned rack stands still, and revenue is coupled to cost. The competitive story is not revenue, it is the ratio. The FY2036 snapshot:

| FY2036 | Default node | AI-1-spec node |
|---|---:|---:|
| Compute per launch | 753 kW (66 packages) | 902 kW (440 packages) |
| Cost per ground dollar | $1.28 | $0.91, below ground |
| Cohort revenue, 90 launches | $2.52B/yr | $2.37B/yr |
| Cohort profit, 90 launches | $0.84B/yr | $0.79B/yr |
| Living-fleet revenue, 268 nodes | $7.42B/yr | $7.17B/yr |
| Margin | 33.3% | 33.3% (pinned by design) |

Margin holds at 33.3 percent because the model prices revenue at a flat 1.5x of cost. The AI-1 bracket's win lands as a cheaper token, not more revenue: below ground parity at matched margins.

The cost ladder, each step a lever this project tracks:

| Step | Orbit-to-ground cost ratio |
|---|---:|
| The old public default, until 2026-07-14 (heavy co-mounted radiator, $40k/kW dials) | 1.92x |
| Light AI-1-class radiator, old $40k/kW cost dials | 1.69x |
| The current default (light radiator, $20k/kW dials, frontier silicon) | 1.28x |
| AI-1-equivalent at the same dials (pinned 2026 silicon, lighter solar and bus) | 0.91x, below ground |

The bottom row is the point: parity is not exotic. It is the same architecture the default already flies, plus AI-1's lighter solar and bus and its willingness to pin today's silicon.

## Ten Years Out

AI-1 carries today's silicon (about one GB300 NVL72 rack), so the AI-1-spec node pins it; the default's frontier silicon advances. The two designs age in opposite directions (design years below; the cohort table above starts at 2027, the first launch year):

| Launch year | Default node | AI-1-spec node | Compute ratio |
|---|---:|---:|---:|
| 2026 | 457 kW / 3,345 PF | 902 kW / 6,600 PF | 2.0x |
| 2029 | 688 kW / 12,500 PF | 902 kW / 6,600 PF | 0.5x |
| 2032 | 729 kW / 24,294 PF | 902 kW / 6,600 PF | 0.3x |
| 2036 | 753 kW / 46,021 PF | 902 kW / 6,600 PF | 0.1x |

The pinned rack buys a 2x head start; advancing silicon takes over within three years. Keep AI-1's remaining mass dials AND the advancing roadmap and a node mass-fills toward the megawatt class, where Neutron's fairing volume, not mass, becomes the binding question (crossover near 1 to 2 MW). Flagged as a modeling frontier, not resolved.

## What AI-1 Is

| Spec | Value | Status |
|---|---|---|
| Compute power | 120 kW average / 150 kW peak | confirmed |
| Specific power | 70 kW of compute per tonne | confirmed |
| Solar | 250 W/m2, about 600 m2, about 70 m span | confirmed (area derived) |
| Whole-satellite mass | about 1.7 to 2.1 t | derived |
| Silicon | about one GB300 NVL72 rack; NVIDIA first, interchangeable bay | NVIDIA + bay confirmed; one-rack yardstick press |
| Throughput | about 1.1 to 1.44 exaFLOPS dense FP4 | derived (no official FLOPS) |
| Radiator | up to 110 m2, deployable liquid, double-sided knife-edge, redundant pumps | press; orientation pending confirmation |
| Launch | Starship to about 600 km; first deployments as early as 2028, factory targeted end-2027 | press |

Two readings matter. The headline power is compute power, the same basis as our node: solar output sits about equal to peak compute, so cell efficiency sets array area, not delivered watts. And the silicon is our FY2026 model year: 72 packages at 15 PF reproduce the rack's throughput, and our compute mass matches a real NVL72. Their satellite is the first column of our model, not the last.

## The Radiator: The Bet We Now Share

Our original node-mass write-up assumed the radiator co-mounts on the back of the solar array ([node_mass_model.md](../research/node_design/node_mass_model.md) Section 4; the model's `single_face_co_mounted` architecture, now the labeled conservative exception). AI-1 flies a separate, double-sided, knife-edge radiator run hot instead, and since 2026-07-14 so does the default: a radiator backed by the solar array loses a radiating face and absorbs array heat, so the separated wing is simply the better architecture. The physics is one line: radiated flux scales as temperature to the fourth power, so a hotter loop sheds more heat from less area.

| Radiator | Flux | What buys it |
|---|---:|---|
| ISS heat-rejection system, flown | 147 W/m2 | ammonia near 0 C, crew loop |
| ISS photovoltaic radiator, flown | 330 W/m2 | warmer electronics loop |
| The old co-mounted dial (the conservative exception) | 350 to 417 W/m2 | just above flown practice |
| AI-1 and the current default, 110 m2-class at 120 to 150 kW | 1,091 to 1,400 W/m2 | 74 to 97 C double-sided hot loop |

Same panel mass class on both sides (theirs implies 3.6 to 5.5 kg per square meter, ours sat at 4.2 to 5.0): the advantage is temperature, not material, and not a heat pump (studied for decades, never flown as a primary spacecraft thermal system, and mass-negative on our dials). Redwire's May 2026 study independently shows 757 W/m2 at a 48 C interface, so the regime is engineering, not magic. The open engineering is the chip-to-coolant-to-panel path at that temperature; the refreshed cost analysis and the thermal-path model track it (`research/node_design/solar_radiator_cost_refresh_2026_07.md`, `RLDC-SOLAR-RADIATOR-MASS`).

The model still polices the bracket: the AI-1-spec run trips the pinned-silicon validation flag by design, labeling itself. A literal AI-1 does not fit Neutron (a 70 m span built for a 9 m fairing): the mass ratios carry over, the form factor does not, and volume stays comfortable below about 1 MW (`RLDC-FAIRING-VOLUME-80M3`).
