# Data Center Conclusion

Under the current baseline model, a Neutron-launched orbital AI-inference data
center looks strong enough to justify serious follow-on work. By **2036** it
models to about **$5.94B** in annual revenue and **$1.74B** in annual gross
profit (about **29.3%** margin), at about **1.92x** the cost of an equivalent
ground build. This is not a precision forecast or a DCF. It is a bounded
feasibility exercise built from visible, source-linked assumptions.

The interesting part is not "a data center in space" as a slogan. It is the
machine Rocket Lab could build around it: integrate GPUs and networking on the
ground, package them into rack-like orbital nodes, attach them to a Rocket Lab
bus with solar, radiator, thermal, and communications, launch on Neutron, and
improve the whole stack through repeated cadence.

## Source Snapshot

| Item | Current source |
|---|---|
| Space model | `data_center/models/space/default.json` |
| Ground reference | `data_center/models/ground/default.json` |
| Default scenario | `code/scenarios/default.yaml` |

## The 2036 Model

2036 is the headline year: the first clean takeoff year, after cadence has left
prototype scale and the central case has turned gross-margin positive. Read it
as two separate stories.

**Cadence**, what Rocket Lab launches and deploys that year:

| Cadence signal | Value |
|---|---:|
| Neutron launches, one node each | **90** |
| New orbital compute power added | about **38 MW** (37,978 kW) |

**Active base**, the installed fleet producing the revenue run-rate (keep it
separate from cadence):

| Active-base signal | Value |
|---|---:|
| Active on-orbit nodes | **268** |
| Active node power | about **112 MW** (112,318 kW) |
| Annual revenue run-rate | **$5.94B** |
| Annual gross profit run-rate | **$1.74B** |
| Gross margin | **29.3%** |
| Revenue per GPU package | about **$0.59M** |
| Cost per GPU package | about **$0.42M** |

The 90-launch year is the production and deployment moment; the 268-node active
base is the revenue run-rate. Do not collapse them into one number.

## How The Numbers Are Built

The cost is bottom-up. Each node's build-and-launch cost is the sum of its
parts: compute, bus, solar, radiator, and launch. Multiply by the fleet
deployed or living in a given year and that is the annual cost. None of it is a
top-down market estimate.

Revenue is tied to that cost, not guessed on its own. The model prices at a
multiple of cost, about **1.5x** tapering toward **1.40x** by 2036, which is
what produces the roughly **29.3%** gross margin. The ground reference uses the
same multiple, so both sides target the same margin. That is what makes the
comparison fair: with margins held equal, the **1.92x** orbital-to-ground cost
gap is also the price gap, so an orbital token would cost about **90% more**
than a comparable ground token.

## Context: What The Model Is, And Is Not

The modeled product is orbital AI inference, not frontier-model training, and
none of this stack has been designed or iterated for space yet. The default
translates public terrestrial hardware assumptions into a Neutron-centered
orbital scenario. That conservative translation is the point: even without a
space-native design, the case already lands close enough to ground cost to study
seriously, and it has room to improve. Production and iteration historically
surface gains no one anticipated, so it would not be surprising if the costs
here came down over the next decade. That upside is noted, not modeled.

Read it with a vertical-integration lens that the baseline does not pay for.
Many cost lines behave like external buy prices, but in a Rocket Lab-operated
program Rocket Lab would supply most of them to itself: bus, solar, radiator and
thermal hardware, integration, launch, operations, and laser communications.
GPUs and some networking are the clearest outside purchases. That internal-customer effect is upside the model leaves on
the table, not a freebie baked in.

## Core Default Assumptions

| Assumption | Status | Source marker |
|---|---|---|
| 90 launches/year target by 2036 | Scenario input, not Rocket Lab guidance | `RLDC-CADENCE-90` |
| 12.5 t SSO block-upgrade mass envelope | Scenario input, not a published payload guarantee | `RLDC-PAYLOAD-SSO-UPGRADE` |
| Five-year service life | Scenario input | `RLDC-SERVICE-LIFE-5Y` |
| Roughly 400 kW node simplification | Derived model scale | `RLDC-NODE-POWER-400KW` |
| High-cadence launch cost around $13M | Scenario input | `RLDC-LAUNCH-COST-2036` |
| Central revenue multiple 1.5x cost, tapering to 1.40x by 2036 | Scenario input | `RLDC-REVENUE-MULTIPLE-1_5X` |
| No separate secure-compute premium | Narrative boundary | Central cost-multiple path, not a premium scenario |

The central 2036 output is about **29.3% gross margin**. The low and high
revenue bands are sensitivity outputs, not the public default.

## Ground Reference

The ground comparison is deliberately cautious. It anchors to the same 2036
deployed-year cohort as the space model (**90 nodes**, **3,330 GPU packages**,
**37,978 kW**), not to the 112 MW active base.

| Reference (five-year) | Value |
|---|---:|
| Ground build | about **$3.68B** |
| Orbital build plus launch | about **$7.05B** |
| Orbital / ground ratio | about **1.92x** |

The costs are in the same order of magnitude, but this is not parity (see
[How The Numbers Are Built](#how-the-numbers-are-built) for why this cost ratio
is also the price ratio). Each ground input traces to the research ledger under
`RLDC-GROUND-COST-BASIS`. Still to refine on the ground side: energy price, PUE,
utilization, facility shell and fit-out, cooling, operations, maintenance, and
the exact package basis.

## Cost-Down And Thermal Sensitivities

The base case is deliberately conservative, and there is real room to close the
gap to ground. Two levers do most of the work, and both show up in the 2036
cohort. The first is cost: the default pays `$40k/kW` for solar and `$40k/kW`
for radiator, where research supports `$20k/kW` for solar and treats it as a
weaker but plausible target for radiator. The second is mass: a lighter solar
and radiator design frees envelope mass for more GPU packages per node, so the
same 90 launches carry more compute.

Stacked against the 2036 base case (illustrative sensitivities, not the promoted
default):

| 2036 case | Packages/node | Living power | Orbital / ground | Token premium |
|---|---:|---:|---:|---:|
| Base (default) | 37 | ~112 MW | 1.92x | ~90% |
| Solar and radiator at $20k/kW | 37 | ~112 MW | 1.50x | ~50% |
| Plus ~25% lighter solar and radiator | 49 | ~149 MW | 1.38x | ~38% |

In the ambitious case the same 90 launches and 268-node fleet carry about a
third more compute (49 packages per node instead of 37, about 149 MW of living
power instead of 112) at the same roughly 29% margin, and the premium a customer
would pay over a comparable ground token falls from about 90% to about 38%.
Revenue is slightly lower because it is coupled to cost, but the token is far
more competitive.

Launch is not where the leverage is. It is only about 18% of total system cost,
against roughly 30% for compute and about 22% each for solar and radiator. Even
halving the launch price moves the orbital-to-ground ratio only from 1.92x to
about 1.75x, roughly a 9% cut in cost per token. The levers that matter are
solar, radiator, and how much compute each launch carries, not the rocket.

## Why The Scale Is Not Outlandish

The 2036 deployed-year capacity is about **38 MW** (rounded elsewhere to about
40 MW/year) against a rough **100 GW** market reference. The modeled deployment
is a small slice of expected AI capacity, not a market-share claim. The concept
also does not require becoming a hyperscaler overnight: start as a focused
wedge, learn the node and operations stack at small scale, then scale into orbit
as cadence and demand grow.

## Why A Customer Might Care

The premium case is not "compute, but farther away." Space can matter when a
customer values what ground capacity cannot easily offer: relief from land,
water, grid, permitting, and local-politics siting fights; solar power once
deployed; physical separation for sovereign, defense, or high-security
workloads; and purpose-built connectivity through laser, narrowband, or RF
links. The default prices none of these as a premium; they are reasons the
market might tolerate a higher orbital cost, not hidden model inputs.

## Refinement Roadmap

The baseline is the reference case; the next work sharpens it: launch-cost
sensitivity (`RLDC-LAUNCH-COST-2036`), payload-case comparisons
(`RLDC-PAYLOAD-SSO-UPGRADE`), solar and radiator cost-down
(`RLDC-SOLAR-RADIATOR-COST`), ground-scope refinement (`RLDC-GROUND-COST-BASIS`),
GPU/package definition tracking, and market-scale updates
(`RLDC-MARKET-100GW-2036`). Thermal and resilience work continues too:
hotter-operation physics, long-life reliability, and radiation-shielding mass
against the solar and radiator stack.
