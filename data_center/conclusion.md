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
| Space schema | `v8` |
| Space validation | No validation failures |
| Ground comparison label | `same_order_of_magnitude` |

## The 2036 Model

2036 is the headline year: the first clean takeoff year, after cadence has left
prototype scale and the central case has turned gross-margin positive. Read it
as two separate stories.

**Cadence**, what Rocket Lab launches and deploys that year:

| Cadence signal | Value | Source marker |
|---|---:|---|
| Launches in the year | **90** | `RLDC-CADENCE-90` |
| New orbital nodes deployed | **90** | Promoted 2036 output |
| New node power added | **37,978 kW** (about **38 MW**) | `RLDC-DEPLOYED-CAPACITY-2036-40MW` |

**Active base**, the installed fleet producing the revenue run-rate (keep it
separate from cadence):

| Active-base signal | Value | Source marker |
|---|---:|---|
| Active on-orbit base | **268 nodes** | `RLDC-SPACE-2036-LIVING-FLEET` |
| Active node power | **112,318 kW** (about **112 MW**) | `RLDC-SPACE-2036-ON-ORBIT-POWER` |
| Annual revenue run-rate | **$5.94B** | `RLDC-SPACE-2036-REVENUE-CENTRAL` |
| Annual gross profit run-rate | **$1.74B** | Promoted 2036 output |
| Gross margin | **29.3%** | `RLDC-SPACE-2036-MARGIN-CENTRAL` |
| Revenue per GPU package | about **$0.59M** | Promoted 2036 per-package output |
| Cost per GPU package | about **$0.42M** | Promoted 2036 per-package output |

The 90-launch year is the production and deployment moment; the 268-node active
base is the revenue run-rate. Do not collapse them into one number.

## Context: What The Model Is, And Is Not

The modeled product is orbital AI inference, not frontier-model training. The
default translates public terrestrial hardware assumptions into a
Neutron-centered orbital scenario; it is not a claim that Rocket Lab has
announced the project or already optimized the hardware for space. That
conservative translation is the point: even without a space-native stack, the
case lands close enough to ground cost to study seriously.

Read it with a vertical-integration lens that the baseline does not pay for.
Many cost lines behave like external buy prices, but in a Rocket Lab-operated
program Rocket Lab would supply most of them to itself: bus, solar, radiator and
thermal hardware, integration, launch, and operations. GPUs and some networking
are the clear outside purchases. That internal-customer effect is upside the
model leaves on the table, not a freebie baked in.

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

If both providers target similar margins, that ratio implies an orbital token
costing roughly **90% more** than a comparable ground token. The costs are in
the same order of magnitude, but this is not parity. Each ground input traces to
the research ledger under `RLDC-GROUND-COST-BASIS`. Still to refine on the
ground side: energy price, PUE, utilization, facility shell and fit-out,
cooling, operations, maintenance, and the exact package basis.

## Cost-Down And Thermal Sensitivities

Solar and radiator cost dials are the sensitive lines. The default uses
`$40k/kW` for each (`RLDC-SOLAR-RADIATOR-COST`). If both move toward `$20k/kW`,
the orbital/ground ratio falls to about **1.50x**, roughly a 50% token premium
(`RLDC-SOLAR-RADIATOR-COSTDOWN-SENSITIVITY`). That is a sensitivity, not the
default.

Thermal-path improvements are a separate lever. If a hotter radiator path can
preserve GPU/HBM reliability, the freed mass supports more packages: a rough
2036 sensitivity adds three to four packages per node, lifting the 90-node
cohort from 3,330 packages to about 3,600 to 3,690
(`RLDC-THERMAL-PACKAGE-DENSITY-SENSITIVITY`). Useful upside, not booked.

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
