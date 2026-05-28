# Data Center Conclusion - Current Baseline Model

Under the current baseline model, an orbital AI-inference data-center wedge
looks strong enough to justify serious follow-on work. This is not a precision
revenue forecast or DCF. It is a bounded feasibility exercise: given the visible
assumptions, the modeled Neutron-scale deployment produces a coherent case on
scale, economics, and order-of-magnitude cost.

The interesting part is not "put a data center in space" as a slogan. The
interesting part is the machine Rocket Lab could build around it: integrate
GPUs and networking on the ground, package them into rack-like orbital nodes,
attach those nodes to Rocket Lab-built bus, solar, radiator, thermal, and
communications infrastructure, launch them on Neutron, and improve the whole
stack through repeated cadence.

The model should also be read with a vertical-integration lens. Many baseline
cost lines behave like external buy prices or customer-facing prices. In a real
Rocket Lab-operated program, Rocket Lab would be buying much of its own
infrastructure: bus, solar, radiator and thermal hardware, integration, launch,
operations, and potentially communications. GPUs and some networking hardware
are the clearest outside purchases. That internal-customer effect is a selling
point, not a modeled freebie.

This conclusion is the plain-English bottom line for the current baseline
data-center model. The machine-readable outputs behind it are
`data_center/models/space/default.json` and
`data_center/models/ground/default.json`.

The modeled product is orbital AI inference, not frontier-model training. The
default is based on public terrestrial hardware assumptions translated into a
Neutron-centered orbital scenario; it is not a claim that Rocket Lab has
announced the project or that the hardware has already been optimized for
space.

That conservative translation is why the result is worth reading. The default
does not assume a final space-native stack, yet it still produces a business
case that is close enough to ground cost to study seriously. The current
orbital reference is not at parity, but the biggest burdens are visible and
tunable.

## Source Snapshot

| Item | Current source |
|---|---|
| Space model | `data_center/models/space/default.json` |
| Ground reference | `data_center/models/ground/default.json` |
| Default scenario | `code/scenarios/default.yaml` |
| Space schema | `v8` |
| Space validation | Promoted default has no validation failures |
| Ground comparison label | `same_order_of_magnitude` |

## Final Modeled Year

The headline year is **2036**. The model is already ramping before then: by the
middle years, cadence has left prototype scale and the central case is already
gross-margin positive. But **2036** is where the curve starts to look like a
real infrastructure business. It is the first clean takeoff year in the public
story.

The **2036 cadence** story is what Rocket Lab launches and deploys that year:

| Cadence signal | Current value | Source marker |
|---|---:|---|
| Final modeled year | **2036** | Promoted model horizon |
| Launches in the year | **90** | `RLDC-CADENCE-90` |
| New orbital nodes deployed | **90** | Promoted 2036 output |
| New node power added | **37,978 kW**, about **38 MW** | `RLDC-DEPLOYED-CAPACITY-2036-40MW` |

The **2036 active-base** story is the installed-base revenue run-rate. Keep it
separate from the cadence story:

| Active-base signal | Current value | Source marker |
|---|---:|---|
| Active on-orbit base | **268 nodes** | `RLDC-SPACE-2036-LIVING-FLEET` |
| Active node power | **112,318 kW**, about **112 MW** | `RLDC-SPACE-2036-ON-ORBIT-POWER` |
| Annual revenue run-rate | **$5.94B** | `RLDC-SPACE-2036-REVENUE-CENTRAL` |
| Annual gross profit run-rate | **$1.74B** | Promoted 2036 output |
| Gross margin | **29.3 percent** | `RLDC-SPACE-2036-MARGIN-CENTRAL` |
| Implied annual revenue per GPU package | about **$0.59M** | Promoted 2036 per-package output |
| Implied annual cost per GPU package | about **$0.42M** | Promoted 2036 per-package output |

Do not collapse these into one metric. The 90-launch year is the production and
deployment moment. The active on-orbit base is the annual revenue run-rate.

## Core Default Assumptions

| Assumption | Status | Source marker |
|---|---|---|
| 90 launches/year target by 2036 | Scenario input, not Rocket Lab guidance | `RLDC-CADENCE-90` |
| 12.5 t SSO block-upgrade mass envelope | Scenario input, not a published payload guarantee | `RLDC-PAYLOAD-SSO-UPGRADE` |
| Five-year service life | Scenario input | `RLDC-SERVICE-LIFE-5Y` |
| Roughly 400 kW node simplification | Derived model scale | `RLDC-NODE-POWER-400KW` |
| High-cadence launch cost around $13M | Scenario input | `RLDC-LAUNCH-COST-2036` |
| Central revenue multiple anchored at 1.5x cost, tapering to 1.40x by 2036 | Scenario input | `RLDC-REVENUE-MULTIPLE-1_5X` |
| No separate secure-compute premium in the default conclusion | Narrative boundary | Default conclusion uses the central cost-multiple path, not a separate premium scenario |

The central **2036** output is roughly **29 percent gross margin**. Low and
high revenue bands remain sensitivity outputs, not the public default story.

## Ground Reference

The ground comparison is useful but intentionally cautious. It anchors to the
same 2036 deployed-year cohort as the space model:
**90 nodes**, **3,330 GPU packages**, and **37,978 kW**. It does not anchor to
the 112 MW active on-orbit base.

The current output puts the five-year ground reference at about $3.68B and the
orbital build-and-launch reference at about **$7.05B**. The orbital/ground
ratio is about **1.92x**, so if both providers target similar margins, the
current default implies an orbital token would need to cost roughly **90
percent** more than a comparable ground token. That says the costs are at least
in the same order of magnitude, but it does not prove parity. The ground
artifact now links each input to the research wiki source ledger under
`RLDC-GROUND-COST-BASIS` and the per-input `RLDC-GROUND-*` claims.

What remains to refine on the ground side: site-specific energy price, PUE,
utilization, facility shell and fit-out allocation, cooling, operations,
maintenance, and the exact GPU/package comparison basis. Those are refinement
questions for a better ground model, not empty slots in the current research
wiki.

## Cost-Down And Thermal Sensitivities

The default uses `$40k/kW` for solar and `$40k/kW` for radiator
(`RLDC-SOLAR-RADIATOR-COST`). If both lines move toward `$20k/kW`, the modeled
orbital/ground ratio falls to about 1.50x, or roughly a 50 percent token
premium (`RLDC-SOLAR-RADIATOR-COSTDOWN-SENSITIVITY`). This is a sensitivity,
not the current default.

Thermal-path improvements are separate from cost-down. If better
chip-to-coolant and coolant-to-radiator design lets the system run a hotter
radiator path while preserving GPU/HBM junction reliability, freed mass could
support more packages, redundancy, or margin. A rough 2036 sensitivity of three
to four extra packages per node would move the 90-node annual cohort from 3,330
packages to roughly 3,600-3,690 packages
(`RLDC-THERMAL-PACKAGE-DENSITY-SENSITIVITY`). That is useful upside, but the
current baseline model does not treat it as proved parity.

## Why The Scale Is Not Outlandish

The default **2036** deployed-year capacity is about **38 MW**, rounded
elsewhere to about **40 MW/year**. The external market reference is only a rough
**100 GW** sanity check. The point is that the modeled deployment is a small
slice of expected AI data-center capacity, not that Rocket Lab captures a
defined market share.

Nor does the concept require Rocket Lab to become a hyperscaler overnight. It
can start as a focused infrastructure wedge: build and test GPU systems on the
ground, learn the node and operations stack at small scale, then move the
repeatable unit into orbit as launch cadence and customer demand grow.

The strategic loop is simple: build the cadence, keep launches reliably booked,
use Rocket Lab hardware inside Rocket Lab's own product, and let compute
revenue plus manufacturing learning reinforce each other. The current baseline
does not add a special margin-capture credit for that loop.

## Why A Customer Might Care

The premium case is not just "compute, but farther away." Space can matter if a
customer values attributes that ordinary ground capacity does not provide:
siting relief from land, water, grid, permitting, and local political fights;
solar power once deployed; physical separation for sovereign, defense,
high-security, or dedicated-capacity workloads; and purpose-built connectivity
through laser links, narrowband links, RF, or other controlled channels.

The current default does not price a separate security or green premium. Those
are reasons the market might tolerate a higher orbital cost, not hidden inputs
inside the model.

## Refinement Roadmap

The current baseline is the reference case. The next work is to sharpen and
extend it through launch-cost sensitivity runs (`RLDC-LAUNCH-COST-2036`),
payload-case comparisons (`RLDC-PAYLOAD-SSO-UPGRADE`), solar and radiator
cost-down scenarios (`RLDC-SOLAR-RADIATOR-COST`), ground-scope refinements
(`RLDC-GROUND-COST-BASIS`), GPU/package definition tracking, and market-scale
updates (`RLDC-MARKET-100GW-2036`).

Thermal and resilience work should also continue: GPU/HBM hotter-operation
physics, long-life reliability, and radiation-shielding sizing against the much
larger solar and radiator mass stack. Those are optimization and fidelity
passes for the next model versions, not reasons to discount the current
research-backed baseline.
