# Data Center Conclusion

Under the current baseline model, a Neutron-launched orbital AI-inference data
center looks strong enough to justify serious follow-on work. By **2036** Rocket
Lab is putting up **90 nodes a year** (about **38 MW**), and every cohort earns
a **33% gross margin** across its five-year life, at about **1.92x** the cost of
an equivalent ground build. This is not a precision forecast or a DCF. It is a
bounded feasibility exercise built from visible, source-linked assumptions.

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

## The Build-Out, Year By Year

The story is a ramp, not a single year. Each year puts up more nodes, and each
year's cohort earns a fixed multiple on its own cost for its full five-year life
at a constant **33% gross margin**. The growth comes from cadence and better
GPUs, not from a moving margin. This is what each launch year deploys and what
that year's nodes earn per year, on their own:

| Launch year | Launches (one node each) | MW put up | Living fleet | This cohort: revenue/yr | This cohort: gross profit/yr |
|---|---:|---:|---:|---:|---:|
| 2027 | 2 | 0.6 | 2 | $39M | $13M |
| 2028 | 3 | 1.0 | 5 | $67M | $22M |
| 2029 | 5 | 1.9 | 10 | $118M | $39M |
| 2030 | 9 | 3.5 | 19 | $206M | $69M |
| 2031 | 14 | 5.7 | 33 | $331M | $110M |
| 2032 | 22 | 9.1 | 53 | $521M | $174M |
| 2033 | 35 | 14.4 | 85 | $810M | $270M |
| 2034 | 51 | 21.3 | 131 | $1.20B | $399M |
| 2035 | 70 | 29.5 | 192 | $1.66B | $555M |
| 2036 | 90 | 38.0 | 268 | $2.11B | $705M |

Read down the cohort columns, not across into a fleet total. Each cohort holds
that revenue and gross profit every year for five years. The 2036 cohort alone
(90 nodes) earns about **$2.11B a year** and about **$705M of gross profit a
year**. The shape is the point: launches run 2, 3, 5, 9, 14, 22, 35, 51, 70, 90,
and the next year pushes past 100 toward the cadence ceiling. 2036 is the
inflection, not the end.

If you add up every cohort still alive, you get the installed fleet, which the
Fleet Snapshot at the end tracks. That aggregate is a side effect of the cohort
build-out, not the headline.

## How The Numbers Are Built

The cost is bottom-up. Each node's build-and-launch cost is the sum of its
parts: compute, bus, solar, radiator, and launch. Multiply by the fleet
deployed or living in a given year and that is the annual cost. None of it is a
top-down market estimate.

Revenue is tied to that cost, not guessed on its own. The model prices at a flat
**1.5x** of cost, the same every year since each cohort launches fresh, which is
what produces the **33.3%** gross margin. The ground reference uses the same
multiple, so both sides target the same margin. That is what makes the
comparison fair: with margins held equal, the **1.92x** orbital-to-ground cost
gap is also the price gap, so an orbital token would cost about **90% more**
than a comparable ground token. The multiple itself is just a dial anyone can
change in the model: it moves every margin together but not the 1.92x cost gap,
which is set by cost alone.

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
| Revenue multiple flat at 1.5x cost, no taper | Scenario input | `RLDC-REVENUE-MULTIPLE-1_5X` |
| No separate secure-compute premium | Narrative boundary | Central cost-multiple path, not a premium scenario |

The central output is a flat **33.3% gross margin**. The low and high
revenue bands are sensitivity outputs, not the public default.

## Ground Reference

As a sanity check, the model builds the same 2036 cohort on the ground: the same
90 nodes, 3,330 GPU packages, and 38 MW of compute, but in a terrestrial data
center instead of orbit. Over five years:

| Same 2036 cohort, five-year cost | Value |
|---|---:|
| Built on the ground | about **$3.68B** |
| Built and launched to orbit | about **$7.05B** |
| Orbital vs ground | about **1.92x** |

In plain terms: orbital costs about **1.92x** what ground costs for the same
compute, so a buyer pays roughly **90% more** for an orbital token than a ground
token. That is not parity, but it is the same order of magnitude, which is the
surprising part: a brand-new orbital build lands within about 2x of mature
ground infrastructure. The ground figure is a rough cost screen, not a
site-specific quote.

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
power instead of 112) at the same roughly 33% margin, and the premium a customer
would pay over a comparable ground token falls from about 90% to about 38%.
Revenue is slightly lower because it is coupled to cost, but the token is far
more competitive.

Launch is not where the leverage is. It is only about 18% of total system cost,
against roughly 30% for compute and about 22% each for solar and radiator. Even
halving the launch price moves the orbital-to-ground ratio only from 1.92x to
about 1.75x, roughly a 9% cut in cost per token. The levers that matter are
solar, radiator, and how much compute each launch carries, not the rocket.

A further lever is service life. The base case amortizes each node over five
years; building the node to last seven (not assumed in the default) spreads the
same build cost over seven years instead of five, about a 30% lower annual cost.
The operator can pass that through as roughly a 30% lower annual price at the
same margin and still recover the node, which narrows the token premium, but
through pricing rather than cheaper hardware: the orbital build-cost ratio
itself does not move. Reaching seven years is not a significant ask of Neutron
or the flight; it mainly takes a bit more on-orbit hardware (station-keeping and
shielding), single-digit-percent on payload. See
`research/synthesis/orbital_lifetime_5v7yr_synthesis.md`.

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

## Fleet Snapshot

The living fleet is only the cohorts still inside their five-year window: nodes
older than five years stop earning and drop out of the count, the power, and the
revenue. Tracked every three years, the installed base grows like this:

| Year | Launched to date | Living fleet | Living power | Annual revenue | Annual gross profit |
|---|---:|---:|---:|---:|---:|
| 2030 | 19 | 19 | ~7 MW | $0.43B | $0.14B |
| 2033 | 90 | 85 | ~35 MW | $1.99B | $0.66B |
| 2036 | 301 | 268 | ~112 MW | $6.31B | $2.10B |

By 2036, 301 nodes have launched but only 268 are live: the 2027 to 2031 cohorts
have aged past five years and no longer count toward power or revenue. Each
living node carries about 420 kW, and the whole fleet runs at the same flat 33%
margin. The point of this view is the slope, not the single-year total: the
installed base roughly doubles every two to three years as cadence compounds.
