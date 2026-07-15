# Data Center Conclusion

Under the current baseline model, a Neutron-launched orbital AI-inference data
center looks strong enough to justify serious follow-on work. By **2036** Rocket
Lab is putting up **90 nodes a year** (about **68 MW**), every cohort earns a
**33% margin** across its five-year life, and the whole build-launch-operate
program runs at about **1.28x** the cost of an equivalent ground build. This is
not a precision forecast or a DCF. It is a bounded feasibility exercise built
from visible, source-linked assumptions.

In plain terms: the 33% margin means each year's nodes sell their computing at
1.5 times their own cost, and the 1.28x means that cost, building, launching,
and running the nodes for five years, is about a quarter more than what the
same computing power costs on the ground. With both sides priced at the same
margin, a customer would pay about 28% more per unit of orbital AI work than
for the ground equivalent. The rest of this document builds those numbers from
their parts.

The interesting part is not "a data center in space" as a slogan. It is the
machine Rocket Lab could build around it: integrate GPUs and networking on the
ground, package them into rack-like orbital nodes, attach them to a Rocket Lab
bus with solar, radiator, thermal, and communications, launch on Neutron, and
improve the whole stack through repeated cadence. Why that machine beats
ground construction, and everything these numbers deliberately refuse to
count in its favor (the learning curve, the captured supplier margin, the
premium revenue lanes, the runway past this table), is the subject of
[the structural case](structural_case.md). This document is the numbers; the
structural case is the pitch. Read them in either order.

The baseline's thermal architecture follows the industry's direction rather
than fighting it: SpaceX's June 2026 AI-1 reveal validated the deployed,
double-sided, run-hot radiator, and this model semi-copies that design (a
dedicated radiator wing, edge-on to the sun, not backed against the solar
array where it would lose a radiating face). The default radiator is set
within 10 percent of AI-1's implied mass. Run the model at full AI-1
equivalence on the same cost dials and it reads about **0.91x**, below ground
parity; that bracket is its own companion, [the AI-1 comparison](ai1_comparison.md).

## Source Snapshot

Three of these files are named "default", which deserves a word: the scenario
YAML is the single set of input dials, and promoting it produces the two model
outputs, the space model and the ground reference. They are different models
that share a filename, not copies.

| Item | File | What it is |
|---|---|---|
| Space model | [`data_center/models/space/default.json`](models/space/default.json) | The promoted orbital model: every number in this document, with formula, units, and source per cell. |
| Ground reference | [`data_center/models/ground/default.json`](models/ground/default.json) | A separate model: the same 2036 cohort costed as a terrestrial build, the denominator of the 1.28x. |
| Default scenario | [`code/scenarios/default.yaml`](../code/scenarios/default.yaml) | The input dials that produce both models; copy, edit, and re-run to test alternatives. |
| Assumptions ledger | [`data_center/assumptions.md`](assumptions.md) | Every default assumption, its source status, and where it comes from. |
| The structural case | [`data_center/structural_case.md`](structural_case.md) | The companion argument: why Rocket Lab specifically, and why these numbers read as a floor. |
| The AI-1 comparison | [`data_center/ai1_comparison.md`](ai1_comparison.md) | SpaceX's June 2026 satellite design run through this same model. |

## The Build-Out, Year By Year

The story is a ramp, not a single year. Each year puts up more nodes, and each
year's cohort earns a fixed multiple on its own cost for its full five-year life
at a constant **33% margin**. The growth comes from cadence and better GPUs,
not from a moving margin. This is what each launch year deploys and what that
year's nodes earn per year, on their own:

| Launch year | Launches (one node each) | MW put up | Living fleet | This cohort: revenue/yr | This cohort: profit/yr |
|---|---:|---:|---:|---:|---:|
| 2027 | 2 | 0.9 | 2 | $38M | $13M |
| 2028 | 3 | 1.7 | 5 | $71M | $24M |
| 2029 | 5 | 3.4 | 10 | $132M | $44M |
| 2030 | 9 | 6.2 | 19 | $231M | $77M |
| 2031 | 14 | 10.0 | 33 | $370M | $123M |
| 2032 | 22 | 16.0 | 53 | $596M | $199M |
| 2033 | 35 | 25.5 | 85 | $930M | $310M |
| 2034 | 51 | 37.8 | 131 | $1.39B | $465M |
| 2035 | 70 | 52.7 | 192 | $1.98B | $660M |
| 2036 | 90 | 67.7 | 268 | $2.52B | $840M |

Read down the cohort columns, not across into a fleet total. Each cohort holds
that revenue and profit every year for five years. The 2036 cohort alone (90
nodes) earns about **$2.52B a year** and about **$840M of profit a year**. The
shape is the point: launches run 2, 3, 5, 9, 14, 22, 35, 51, 70, 90, and the
next year pushes past 100.

The curve is an S. The single-digit years (2027 to 2030) are the flat start:
small cohorts, a small fleet, the proving phase. The steep middle begins once
cadence climbs into the 20s and 30s (2032 and 2033), because each year's new
cohort dwarfs the cohort retiring five years behind it: 2033 launches 35 nodes
and retires 3, and 2036 launches 90 and retires 14. That gap between additions
and retirements compounds the living fleet five-fold from 2032 to 2036 (53
nodes to 268), and it keeps compounding past 2036 for as long as the launch
rate keeps climbing. Nothing in the system caps that rate: launch pads and
rockets can both be built. The model's own brake is a launch-rate parameter
scoped to this ten-year window's infrastructure (`RLDC-CADENCE-CEILING-150`),
a horizon assumption, not a ceiling. 2036 is the steep middle of the S, not
the end.

The window closes before the curve does. The promoted model ends at 2036 by
choice of horizon, not because anything flattens: extend the same default
dials to 2040 (one dial, the model window, nothing else changes) and the
fleet reads **591 living nodes**, about 448 MW, about **$17.7B a year of
revenue and $5.9B of profit** at the same margin, with cadence at 139
launches a year and still rising. Those four years lean on extrapolated
silicon generations, so they illustrate the curve's direction rather than
extend the promoted output (`RLDC-FORWARD-WINDOW-2040`). For scale, the 2036
fleet's $7.4B a year is about 12 times Rocket Lab's entire FY2025 revenue of
$602M, and the 2040 illustration is about 29 times.

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
what produces the **33.3%** margin. The ground reference uses the same multiple,
so both sides target the same margin. That is what makes the comparison fair:
with margins held equal, the **1.28x** orbital-to-ground cost gap is also the
price gap, so an orbital token would cost about **28% more** than a comparable
ground token. The 1.5x multiple is not arbitrary: it is set to match where
comparable cloud and GPU operators actually run their margins (see
[`research/economics/operating_margins_and_revenue_multiple_2026.md`](../research/economics/operating_margins_and_revenue_multiple_2026.md)). It is
still a dial, and changing it moves every margin together but not the 1.28x
cost gap, which is set by cost alone.

## Context: What The Model Is, And Is Not

The modeled product is orbital AI inference, not frontier-model training, and
none of this stack has been designed or iterated for space yet. The default
translates public terrestrial hardware assumptions into a Neutron-centered
orbital scenario, with two investor-set 2026-07-14 anchors stated plainly: the
AI-1-class radiator (deployed, double-sided, run hot, within 10 percent of
AI-1's implied mass) and solar and radiator cost dials of $20k/kW each,
reasoned from assembly-line manufacturing scale and in-house vertical
integration rather than from legacy one-off spacecraft procurement. Production
and iteration historically surface gains no one anticipated, so it would not
be surprising if the costs here came down further. That upside is noted, not
modeled.

Read it with the vertical-integration bookkeeping stated exactly. The bus
and the networking and integration inside the compute line are priced at
outsider buy-rates even though Rocket Lab builds them, so the margin there is
uncounted headroom. The solar and radiator dials already assume Rocket Lab's
own scale pricing, so the model claims no second margin on them. Launch
already prices its own cadence learning, operations are unmodeled at zero (a
stated risk, not an upside), and the GPUs are the clearest outside purchase.
The full counted-versus-uncounted inventory is in
[the structural case](structural_case.md).

## Core Default Assumptions

| Assumption | Status | Source marker |
|---|---|---|
| 90 launches/year target by 2036 | Scenario input, not Rocket Lab guidance | `RLDC-CADENCE-90` |
| 12.5 t SSO block-upgrade mass envelope | Scenario input, not a published payload guarantee | `RLDC-PAYLOAD-SSO-UPGRADE` |
| Five-year service life | Scenario input | `RLDC-SERVICE-LIFE-5Y` |
| Roughly 750 kW node simplification | Derived model scale | `RLDC-NODE-POWER-400KW` |
| High-cadence launch cost around $13M | Scenario input | `RLDC-LAUNCH-COST-2036` |
| AI-1-class radiator: deployed double-sided, 1.65 kg/kW | Investor-set scenario (2026-07-14) | `RLDC-SOLAR-RADIATOR-MASS` |
| Solar and radiator cost $20k/kW each | Investor-set scenario (2026-07-14) | `RLDC-SOLAR-RADIATOR-COST` |
| Revenue multiple flat at 1.5x cost, no taper | Scenario input | `RLDC-REVENUE-MULTIPLE-1_5X` |
| No separate secure-compute premium | Narrative boundary | Central cost-multiple path, not a premium scenario |

The central output is a flat **33.3% margin**. The low and high revenue bands
are sensitivity outputs, not the public default.

## Ground Reference

As a sanity check, the model builds the same 2036 cohort on the ground: the same
90 nodes, 5,940 GPU packages, and 68 MW of compute, but in a terrestrial data
center instead of orbit. Over five years:

| Same 2036 cohort, five-year cost | Value |
|---|---:|
| Built on the ground | about **$6.56B** |
| Built and launched to orbit | about **$8.40B** |
| Orbital vs ground | about **1.28x** |

In plain terms: orbital costs about a quarter more than ground for the same
compute. A brand-new orbital build landing within about 1.3x of mature ground
infrastructure, before any space-native design iteration, is the finding. The
ground figure is a rough cost screen, not a site-specific quote.

## Where The Cost Sits, And The Levers

The 2036 node costs about $93M for five years, and the shares tell you where
the leverage is: compute about **45%**, solar about **16%**, radiator about
**16%**, launch about **15%**, bus about **7%**. Compute now dominates, which
is what you want: the dead-weight support systems no longer carry the cost
story. Launch is not where the leverage is: even halving the launch price
moves the ratio only from about 1.28x to about 1.18x.

The bracket above the default is full AI-1 equivalence: pin today's silicon
(one GB300-class rack per 120 kW box), take AI-1's lighter solar and bus, and
the same model at the same cost dials reads about **0.91x**, below ground
parity. The default deliberately does not claim that: it keeps our
frontier-silicon path and our heavier solar and bus. See
[the AI-1 comparison](ai1_comparison.md).

A further lever is service life. The base case amortizes each node over five
years; building the node to last seven (not assumed in the default) spreads the
same build cost over seven years instead of five, about a 30% lower annual cost.
The operator can pass that through as roughly a 30% lower annual price at the
same margin and still recover the node, which narrows the token premium, but
through pricing rather than cheaper hardware: the orbital build-cost ratio
itself does not move. Reaching seven years is not a significant ask of Neutron
or the flight; it mainly takes a bit more on-orbit hardware (station-keeping and
shielding), single-digit-percent on payload. See
[`research/synthesis/orbital_lifetime_5v7yr_synthesis.md`](../research/synthesis/orbital_lifetime_5v7yr_synthesis.md).

## Why The Scale Is Not Outlandish

The 2036 deployed-year capacity is about **68 MW** (rounded elsewhere to about
70 MW/year) against a rough **100 GW** market reference. The modeled deployment
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
market might tolerate the remaining cost gap, not hidden model inputs.

## The Conservative Exception

The 1.28x rests on two investor-set assumptions, stated here rather than
hedged throughout. First, the radiator: the default asserts the AI-1-class
deployed double-sided run-hot design at 1.65 kg/kW from day one; the physics
lever is real (heat rejection scales with temperature to the fourth power)
but the chip-to-coolant-to-panel path at that temperature is engineering, not
heritage. Second, the cost dials: $20k/kW for solar and radiator is reasoned
from assembly-line scale, Rocket Lab's own silicon-array program, and
internalized supplier margin; solar's evidence is strong, the radiator's is
directional (no public $/kW data exists, and a refreshed cost analysis is
running as a parallel research task).

If those assumptions fail, the model already carries the fallback: returning
both cost dials to the old $40k/kW reads about **1.69x**, and the full prior
posture (the heavy co-mounted radiator at 12 kg/kW plus $40k dials) reads
about **1.92x**. That heavy posture was the public default until 2026-07-14
and remains available as the labeled conservative exception; the ledger keeps
the stress cases visible ($30-40k central-cautious, $60-100k radiator stress).
The claim is not that 1.28x is proven. The claim is that 1.28x is what the
industry-validated architecture and assembly-line economics imply, and that
even the deliberately pessimistic posture stays under 2x.

## Refinement Roadmap

The baseline is the reference case; the next work sharpens it: the refreshed
solar and radiator cost analysis (in flight, `RLDC-SOLAR-RADIATOR-COST`),
launch-cost sensitivity (`RLDC-LAUNCH-COST-2036`), payload-case comparisons
(`RLDC-PAYLOAD-SSO-UPGRADE`), ground-scope refinement (`RLDC-GROUND-COST-BASIS`),
GPU/package definition tracking, and market-scale updates
(`RLDC-MARKET-100GW-2036`). Thermal and resilience work continues too: the
chip-to-coolant-to-panel model behind the run-hot radiator, long-life
reliability, and radiation-shielding mass against the solar and radiator stack.

## Fleet Snapshot

The living fleet is only the cohorts still inside their five-year window: nodes
older than five years stop earning and drop out of the count, the power, and the
revenue. Tracked every three years, the installed base grows like this:

| Year | Launched to date | Living fleet | Living power | Annual revenue | Annual profit |
|---|---:|---:|---:|---:|---:|
| 2030 | 19 | 19 | ~12 MW | $0.47B | $0.16B |
| 2033 | 90 | 85 | ~61 MW | $2.26B | $0.75B |
| 2036 | 301 | 268 | ~200 MW | $7.42B | $2.47B |

By 2036, 301 nodes have launched but only 268 are live: the 2027 to 2031 cohorts
have aged past five years and no longer count toward power or revenue. Each
living node carries about 750 kW, and the whole fleet runs at the same flat 33%
margin. The point of this view is the slope, not the single-year total: the
installed base roughly doubles every two to three years as cadence compounds.
