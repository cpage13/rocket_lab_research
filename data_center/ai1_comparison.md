# The AI-1 Comparison

*Companion to the [conclusion](conclusion.md) (the numbers) and the [structural case](structural_case.md) (the why), source-linked through the [assumptions](assumptions.md). On June 8, 2026, SpaceX revealed AI-1, its orbital AI data-center satellite. This document makes one assumption, once: AI-1's specs are real, and a Neutron node is built to them. AI-1 is an unflown design revealed three days before SpaceX's IPO; every AI-1 figure here comes from that reveal ([sources](../research/competitors/starship_addendum.md)). Said once, not repeated.*

**The short version: AI-1 makes the Neutron case stronger.** It matches our model where the model is well grounded (silicon, solar area) and beats it in exactly one place (the radiator). Built to its specs, a Neutron node carries about 3x the compute per launch at today's silicon, the cost premium over ground falls from about 90 percent to about 30 percent, and revenue rises about 60 percent at the same margin. Turn the cost dials we already track and the orbital build comes out cheaper than ground. One bet decides all of it: the radiator.

## The Numbers

Same model, same 12.5 t envelope, same costs, same launch prices; only AI-1's mass dials and its silicon swapped in (the scenario ships as [`code/scenarios/ai1_equivalent.yaml`](../code/scenarios/ai1_equivalent.yaml); the default stays the only promoted model). The node is not a single AI-1: it packs about six to seven AI-1s' worth of hardware into one launch. A node is one orbital data-center unit, one per Neutron launch, and each launch year's cohort earns a fixed margin over its five-year life. The primary breakdown, by launch year (first launches in 2027; verified runs):

| Launch year | Launches | Cohort revenue/yr, default | Cohort revenue/yr, AI-1-spec | Cohort gross profit/yr, default | Cohort gross profit/yr, AI-1-spec |
|---|---:|---:|---:|---:|---:|
| 2027 | 2 | $39M | $81M | $13M | $27M |
| 2029 | 5 | $118M | $203M | $39M | $68M |
| 2032 | 22 | $521M | $852M | $174M | $284M |
| 2036 | 90 | $2.11B | $3.34B | $705M | $1.11B |

The AI-1-spec cohorts earn about 2.1x the default in the early years and settle at about 1.6x (+58 percent) by 2036, as the default's advancing silicon closes the gap. Every row runs the same 33.3 percent gross margin. The FY2036 snapshot, with the fleet details:

| FY2036 | Default node | AI-1-spec node |
|---|---:|---:|
| Compute per launch | 422 kW (37 packages) | 902 kW (440 packages) |
| Cost premium per ground dollar | $0.92 | $0.29 |
| Cohort revenue, 90 launches | $2.11B/yr | $3.34B/yr (+58%) |
| Cohort gross profit, 90 launches | $0.70B/yr | $1.11B/yr (+58%) |
| Living-fleet revenue, 268 nodes | $6.31B/yr | $10.08B/yr (+60%) |
| Living-fleet gross profit | $2.10B/yr | $3.36B/yr (+60%) |
| Gross margin | 33.3% | 33.3% (pinned by design) |

Margin holds at 33.3 percent because the model prices revenue at a flat 1.5x of cost. The win lands as more revenue per launch and a far more competitive token: per-token cost falls by roughly a third against ground. (Held-price reading, derived, not the published frame: at unchanged token prices the same gap is margin, 33 percent toward 55.)

The cost ladder. Each step is a lever this project already tracks:

| Step | Orbit-to-ground cost ratio |
|---|---:|
| Default, today's published center | 1.92x |
| Default + solar and radiator cost halved to $20k/kW | 1.50x |
| AI-1 mass dials, the conservative center of this comparison | 1.29x |
| AI-1 dials + radiator cost halved | 1.10x |
| AI-1 dials + both cost dials halved | 0.91x, below ground |

The 1.29x center credits AI-1 no cost advantage: our $40k/kW solar and radiator cost dials stay in place (themselves an open research line, `RLDC-SOLAR-RADIATOR-COST`). The bottom row is the point: parity is not exotic. It is the same node plus a cost-down already in the conclusion's sensitivity table.

## Ten Years Out

AI-1 carries today's silicon (about one GB300 NVL72 rack), so the AI-1-spec node pins it; the default's frontier silicon advances. The two designs age in opposite directions (design years below; the cohort table above starts at 2027, the first launch year):

| Launch year | Default node | AI-1-spec node | Compute ratio |
|---|---:|---:|---:|
| 2026 | 299 kW / 2,190 PF | 902 kW / 6,600 PF | 3.0x |
| 2029 | 385 kW / 7,000 PF | 902 kW / 6,600 PF | 0.9x |
| 2032 | 412 kW / 13,731 PF | 902 kW / 6,600 PF | 0.5x |
| 2036 | 422 kW / 25,800 PF | 902 kW / 6,600 PF | 0.3x |

The mass win buys a 3x head start; advancing silicon takes over by the end of the decade. Keep AI-1's mass dials AND the advancing roadmap and a node mass-fills to about 2.4 MW by FY2036, the first case where Neutron's fairing volume, not mass, becomes the binding question (crossover near 1 to 2 MW). Flagged as a modeling frontier, not resolved.

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

Two readings matter. The headline power is compute power, the same basis as our node: solar output sits about equal to peak compute, so cell efficiency sets array area, not delivered watts. That match is the area spec; AI-1's array mass is far lighter than our conservative dial, and that is part of its bet. And the silicon is our FY2026 model year: 72 packages at 15 PF reproduce the rack's throughput, and our compute mass matches a real NVL72. Their satellite is the first column of our model, not the last.

## Where We Were Wrong, and the One Bet

Our node-mass write-up assumed the radiator co-mounts on the back of the solar array ([node_mass_model.md](../research/node_design/node_mass_model.md) Section 4; the model's `single_face_co_mounted` architecture). AI-1 flies a separate, double-sided, knife-edge radiator run hot instead. The physics is one line: radiated flux scales as temperature to the fourth power, so a hotter loop sheds more heat from less area.

| Radiator | Flux | What buys it |
|---|---:|---|
| ISS heat-rejection system, flown | 147 W/m2 | ammonia near 0 C, crew loop |
| ISS photovoltaic radiator, flown | 330 W/m2 | warmer electronics loop |
| Our dial | 350 to 417 W/m2 | just above flown practice |
| AI-1, 110 m2 at 120 to 150 kW | 1,091 to 1,400 W/m2 | 74 to 97 C double-sided hot loop |

Same panel mass class on both sides (theirs implies 3.6 to 5.5 kg per square meter, ours 4.2 to 5.0): the advantage is temperature, not material, and not a heat pump (studied for decades, never flown as a primary spacecraft thermal system, and mass-negative on our dials). Redwire's May 2026 study independently shows 757 W/m2 at a 48 C interface, so the regime is engineering, not magic. Our model defers the same bet to its FY2031 thermal step; AI-1 takes it on day one.

That is the whole dispute, and the model polices it: the AI-1-spec run trips three validation flags. Two fire on purpose (pinned silicon; a radiator dial below the co-mounted floor), the upper bracket labeling itself. The third is a default-calibration check (the deployed-capacity rule) that fires only because this scenario is not the default. **If AI-1 flies at spec, the existing THR-014 sensitivity (0.006 to 0.008 t/kW) is the dial that moves toward central; until then the conservative dial stays.** Mass remains the binding lever and the 2x-miss cliff stands (`RLDC-SOLAR-RADIATOR-MASS`). A literal AI-1 does not fit Neutron (a 70 m span built for a 9 m fairing): the mass ratios carry over, the form factor does not, and volume stays comfortable below about 1 MW (`RLDC-FAIRING-VOLUME-80M3`).
