# The Iridium Model: Conclusion

## What This Is

Rocket Lab has agreed to acquire Iridium, with closing expected in mid-2027
subject to the transaction's conditions (COMM-601, COMM-606). With it comes a
rare asset: a globally coordinated slice of L-band spectrum near 1.6 GHz that
Iridium holds exclusively. This document is the feasibility verdict on
modernizing that spectrum with a Neutron-launched fleet.

Start with what the spectrum is good at. L-band near 1.6 GHz propagates well:
it holds through rain and clouds, tolerates foliage, and reaches where higher
frequencies struggle (COMM-426, COMM-563, COMM-627). The width held is modest,
so this is not competing with high-bandwidth video streaming. What it delivers
is a decent, reliable link: not high-end broadband, but nowhere near dial-up.
That carries voice, text, maps, photos, and music. Difficult-environment
performance is a relative advantage over higher-frequency satellite links,
not a guarantee through every wall.

That profile fits where usage is going. Interaction is shifting toward AI
agents. A prompt to the cloud is small. The answer coming back is small.
Agent traffic needs reliability and reach, not continuous bulk download. The
same is true for IoT: sensors, vehicles, and machines that need a dependable
connection everywhere and send little data. Reliable, everywhere, low power,
low cost. That is the product: tens of millions of IoT devices and millions
of people, on purpose-built terminals, on small self-orienting antennas, and,
if the band ever enters standard chipsets, on phones.

## The Verdict At A Glance

The business meaning in one paragraph: about **$725 million** of hardware and
launch spend puts the full 340-satellite fleet up by **2031**, serving about
10.6 million people of capacity plus about 51.7 million IoT devices and
earning about **$8.25 billion a year** at investor-set prices with every
serveable slot sold, an operating margin near **98 percent** against the $145
million a year of satellite replacement that keeps the fleet flying. Keep
launching and the same spectrum saturates near **2,000 satellites by 2035**,
where the same sheet reads about **$48.5 billion a year**. In this model the
bet is demand and the not-yet-modeled operations line: the hardware is small
next to the roughly $8.0 billion acquisition that carried the spectrum
(COMM-602).

| The verdict | 340 satellites, complete 2031 | About 2,000 satellites, complete 2035 |
|---|---|---|
| Launches to build | 29 | 167 (186 flown through 2035, replacements included) |
| People capacity (subscribers) | about 10.6 million | about 62 million |
| IoT devices (counted separately) | about 51.7 million | about 304 million |
| Revenue per year (the published sheet) | about $8.25B | about $48.5B |
| Fleet cost per year | about $145M | about $835M |
| Operating margin (pre-operations) | about 98.2 percent | about 98.3 percent |
| Build-and-hold spend through FY2036 | $1.45B | $5.0B |

Both columns run the same all-in deployment scenario: the whole modeled
Neutron manifest flies communications satellites (the deployment section
states that assumption plainly). The years are explicit on purpose. 340
satellites is the 2031 story. By 2035 the build is at the spectrum's
saturation ceiling near 2,000.

This is not a precision forecast or a DCF. It is a bounded feasibility
exercise built from visible, source-linked assumptions, and every number here
traces to the frozen model baseline, a cited research claim, or an explicitly
labeled scenario dial.

## Source Snapshot

| Item | File | What it is |
|---|---|---|
| Iridium model | [`communications/models/iridium/default.json`](models/iridium/default.json) | The promoted model: the frozen baseline, its derivation, units, and sources, including the fleet, launch, and capacity denominators and the labeled orbit scenario block (schema iridium-v4) |
| Default scenario | [`code/scenarios/iridium.yaml`](../code/scenarios/iridium.yaml) | The input dials; copy, edit, and re-run to test alternatives |
| Saturation companion | [`code/scenarios/iridium_saturation.yaml`](../code/scenarios/iridium_saturation.yaml) | The 2,000-satellite build-out: one dial moved (the target rises to the cap-binding 62,400,000) |
| Assumptions ledger | [`communications/assumptions.md`](assumptions.md) | Every default assumption, its source status, and where it comes from |
| Design | [`communications/design.md`](design.md) | The workstream architecture and how the model is built |
| Evidence | [`research/SOURCE_INDEX.md`](../research/SOURCE_INDEX.md) | The `COMM-*` claim ledger and the research wiki |

## What We Have: The Spectrum

Two different quantities hide in "8 MHz of L-band at 1.6 GHz", and the model
rests on keeping them apart. The frequency (about 1.6 GHz) is where the
signal sits on the dial: it sets reach, and reach is the product story. The
bandwidth is the width held: it sets capacity.

| Holding | Width | Status |
|---|---|---|
| Exclusive (1618.725 to 1626.5 MHz) | 7.775 MHz | Owned outright; the baseline models it as 8.0 (COMM-611) |
| Shared with Globalstar | 0.95 MHz | Usable today under coordination |
| Full coordinated span (1616 to 1626.5 MHz) | 10.5 MHz | Contingent upside: a live FCC dispute (Rocket Lab versus Amazon after both deals close) |

Winning the full 10.5 MHz raises the spectrum-linear outputs by 31.25
percent: the beam pool, per-satellite capacity, density at a fixed rate and
concurrency, and the revenue quantities that inherit that density (about
40,950 people per satellite instead of 31,200). It does not move dates,
costs, or orbit results. It is a labeled variant, never the baseline.

## What We Build: The Satellite

Each modeled satellite is a flat-panel **phased array of about 25 square
meters** with digital beamforming, laser crosslinks between satellites (so
traffic routes in space and the L-band is spent entirely on users), and Ka
feeder links. **Twelve fit on one Neutron launch**: 12 times the roughly 800
kg single-source mass estimate is about 9,600 kg, 73.8 percent of the
certified about 13,000 kg LEO envelope (COMM-253/256, COMM-258/260). No block
upgrade is assumed: today's vehicle carries today's 12, the pure mass
quotient would allow about 16, and any future block upgrade is unmodeled
upside.

| Per satellite | Today's Iridium (66 satellites) | The modeled satellite |
|---|---|---|
| Throughput | about 2.64 Mbps | about 780 Mbps at the weakest device class |

That is roughly 300x per satellite, and fleet against fleet the gap is wider:
340 modern satellites move about **265 Gbps** against the roughly **174
Mbps** the whole 66-satellite fleet moves today, more than a thousandfold.
The incumbent figures are reproducible but rest on a single-lineage input
(COMM-639), so read that comparison as a tensioned estimate, not a certified
fleet total.

## How The Capacity Arises

The per-satellite chain is short enough to hold in your head, and every link
carries a labeled status:

| Link | Value | Status |
|---|---|---|
| Spectrum held (a width) | 8.0 MHz | Fact: 7.775 MHz exclusive, rounded (COMM-611) |
| Weakest-class spectral efficiency | 0.65 bits per hertz | Chosen central inside the measured 0.5 to 0.8 band (COMM-428/429: mean 0.79, median 0.64, measured over the air on a working phone service, interference included) |
| Effective spectrum reuse | about 150x | Calibrated estimate, corpus band 130 to 200x (COMM-410/411): the widest error bar in the model |
| Busy-hour concurrency | 2.5 percent | Corpus-central inside 1 to 5 percent (COMM-543) |
| Active rate (the service tier) | 1.0 Mbps | Investor-set dial |

Walk it forward. One beam running the whole 8 MHz at the weakest device
class's efficiency carries 8 x 0.65 = **5.2 Mbps**: the beam pool, and the
hard per-person ceiling. The satellite does not light one beam: it aims about
150 of them at different patches of ground and reuses the same 8 MHz in every
one, the way a terrestrial network reuses its band across cells. So one
satellite moves 5.2 x 150 = **780 Mbps**. At the busy hour 2.5 percent of
subscribers transmit at once, so 780 Mbps serves 780 active users at **1.0
Mbps each**, and the density is the same equation run backwards: **31,200
people per satellite**. Reuse multiplies how many people a satellite serves,
never one person's rate.

These are conditional model outputs, not measured performance from a finished
spacecraft. The reuse calibration is the number real engineering would move
first: across the corpus band edges, per-satellite capacity spans roughly 0.3
to 1.5 Gbps against the 0.78 central.

One warning travels with every density figure in this document. The corpus
carries a second density chain, about 3,000 subscribers per satellite per
megahertz on a gain-terminal basis, which lands numerically adjacent (31,500
on 10.5 MHz) to the model's 31,200 (8 MHz, phone class) while meaning
something different. Both chains are one formula evaluated at different
device classes over different load bases, and the corpus source is itself
ambiguous by about a factor of two in the load it assumes. Never blend them.
This conclusion stands on the calibrated phone-class chain, the conservative
side: the gain-terminal chain is terminal-tier headroom above it.

## Who Uses It: The Devices

The service is device-diverse by design, and the ladder leads with the
hardware Rocket Lab can build and ship without anyone's permission:

| Device tier | Efficiency (bits/Hz) | Busy-hour rate | Light-load ceiling |
|---|---|---|---|
| Small antenna (a puck, or a USB device on a laptop; about 10 dBi, self-orienting) | 2.0 | about 3.1 Mbps | about 15.4 Mbps |
| Mounted antenna (vehicles, ships, fixed sites; 15+ dBi) | 2.5 | about 3.8 Mbps | about 19.2 Mbps |
| Phone-class radio (0 dBi, no external antenna) | 0.65 | about 1.0 Mbps | about 5.0 Mbps |

Three facts organize the table. First, the per-person ceiling is the beam
pool, never the satellite total: a user lives in one beam and shares that
beam's pool with its other users. Second, the baseline is computed at the
weakest tier on purpose: every headline number uses the phone-class 0.65, so
the published figures are the conservative floor, and held at the same 1.0
Mbps rate the antenna tiers raise density instead of speed, to about 96,000
and 120,000 people per satellite. Third, only the phone row carries an
ecosystem assumption: Iridium's band is in no standard phone chipset today
(Qualcomm and Iridium built and demonstrated that chip once; the partnership
ended in 2023 with zero phone adoption, a commercial barrier, not physics).
The antenna tiers need no such assumption. A standard 2026 phone cannot use
this band, so the phone row is a possible later path, never the dependency.

One design note travels with the small-antenna row: antenna gain is
directional, so the tier is specified with a self-orienting mount (a fixed
tilt or a few switched elements, no user pointing, no moving parts). A bare
flat puck lying face-up earns these rates only with a satellite high
overhead; the mount in the spec is what makes the row's rates typical rather
than best-case.

Separately, and counted separately, the same fleet carries **tens of millions
of IoT devices**. IoT are devices, not people, and they ride nearly free: at
kilobit-class rates their traffic is negligible against a satellite's 780
Mbps, so the sizing assigns IoT zero traffic load. One honest qualifier: the
random-access channel that carries them does reserve about 7 percent of the
8 MHz, so a fully joint sizing reads about 29,000 people per satellite rather
than 31,200. The published device count derives from the revenue mix (about
51.7 million at the baseline); the 10-million passthrough dial reports only
when the revenue case is off.

## The Fleet: Orbit, Size, And The Ceiling

At the 10-million-person target the pure capacity need is 321 satellites, and
the baseline flies a conservative **340**. The orbit is the model's own:
about **450 kilometers at 53 degrees** inclination, chosen because people
live at mid-latitudes. The covered band holds roughly 99.6 percent of the
world's population, and the project's coverage simulation needs about 10
percent fewer satellites there than a polar fleet (341 versus 375 at the 95
percent threshold and a 25 degree mask). The honest bounds on that
simulation: a fuller phasing search finds 320 satellites passing the same
stored geographic metric, the saved 341 case is the robust one under
equal-area weighting, and the metric is geographic rather than
population-weighted. So 340 is a supported conservative scenario and the
exact floor is an engineering decision. The promoted artifact carries this
orbit posture as a labeled scenario block with those bounds attached.

Why a ceiling exists at all: on a fixed band, capacity comes from beams
reusing the spectrum over separated patches of ground, and once every patch
is covered on the 8 MHz, additional satellites add overlapping co-channel
beams that interfere rather than add (COMM-413 to COMM-416). The model
encodes this as an investor-set saturation cap near **2,000 satellites**,
informed by that real mechanism rather than uniquely solved: 31,200 x 2,000
is the **62.4-million-person ceiling**, the second column of the verdict
table. Starlink's far larger fleet does not contradict the ceiling: that
system holds hundreds of megahertz of user spectrum against this band's 8,
so fleet counts are not comparable across systems.

A richer service tier trades headcount for speed: at a 2.5 Mbps active rate
the density falls to 12,480 per satellite and the 10-million target needs a
capacity-bound 802-satellite fleet, which the all-in build completes in 2033.

## How It Deploys

The deployment question is the same all-in question the data-center model
answers: what happens if you go pedal to the metal? The whole modeled Neutron
manifest flies communications satellites on the shared cadence ramp.

- The **340-satellite fleet completes in 2031**: 29 launches, flown 2, 3, 5,
  9, and 10 across 2027 through 2031. The early ramp binds, not the share.
- Kept going, the build reaches the **2,000-satellite ceiling in 2035**: 186
  launches flown through completion (the no-retirement quotient is 167;
  replacements begin while the fleet deploys), 200 cumulative through FY2036.
- Once a fleet stops growing, the replacement treadmill is modest: about 68
  satellites a year for the 340 fleet, roughly 6 launches.

The all-in share is a modeling scenario and is stated as one. In practice the
manifest is shared and 100 percent is not realistic near-term, even if the
long-term direction trends that way. The framework survives lower shares with
later dates: at half the manifest the 340-satellite fleet completes in 2033
instead of 2031. Deployment speed is a dial. The feasibility question is
whether spectrum, rates, reuse, users, orbit, and coverage close, and a
particular completion year is secondary.

## What It Means For The Business

The cost model is deliberately flat (an investor simplification, 2026-07-09),
and both dials sit in-band of the research anchors:

| Cost line | Value | Grounding |
|---|---|---|
| Satellite build | $1.0M each | Just below the prior 1.05 dial and the about-$1.2M Starlink V3 hardware anchor (COMM-080) |
| Launch, flat at any cadence | $13.0M | Just below the shared curve's grounded $13.5M high-cadence floor |
| Build through 2031 (the 340 fleet) | about $725M | 29 launches, 348 satellites |
| Build-and-hold through FY2036 | $1.45B exactly | The 2031 build plus one full five-year fleet replacement: 696 units, 58 launches |
| Steady-state fleet cost | $145M per year | Satellites replaced on a five-year life, annualized |

Operations cost is held at **zero** by explicit assumption, a fixed line to
research and add later, stated in every model output rather than hidden. One
accounting artifact worth naming: the final model year (FY2036) replaces the
large 2031 cohort, so the final-year cash line reads $250 million, or $25 per
configured person, while the annualized basis is $14.50. The promoted JSON
names both bases directly: the final-year cash pair and the annualized line
(schema iridium-v4).

The published revenue case is the four-bucket ARPU sheet (Sheet A,
investor-set 2026-07-09): each bucket is a set price and a percentage of the
fleet's billable-connection pool, so every bucket scales with the satellite
count. The prices are anchored on what Iridium's customers pay today; the mix
is a set split, loosely guided by the shape of Iridium's base, with
government pinned to reproduce today's fixed contract. One table carries the
whole business at both fleet sizes:

| Bucket | Mix and price | At 340 satellites (2031) | At about 2,000 satellites (2035) |
|---|---|---|---|
| Standard personal | 15.0 percent at $15/mo | 9,360,000 people, $1.68B/yr | 55,058,824 people, $9.91B/yr |
| Premium terminal | 2.0 percent at $100/mo | 1,248,000 people, $1.50B/yr | 7,341,176 people, $8.81B/yr |
| IoT devices | 82.8 percent at $8/mo | 51,670,320 devices, $4.96B/yr | 303,943,059 devices, $29.18B/yr |
| Government | 0.2 percent at $74/mo | 121,680 contract units, $0.11B/yr | 715,765, $0.64B/yr |
| Total revenue | 100 percent | $8.25B/yr on a 62,400,000-connection pool | $48.5B/yr on a 367,058,824-connection pool |
| Fleet cost | | $145M/yr | $835M/yr |
| **Operating margin (pre-operations)** | | **about 98.2 percent** | **about 98.3 percent** |

The pool is a billable-connections accounting frame over which the mix
percentages are defined: subscribers are people, IoT are devices, government
is a contract line, and the three are never summed as one population. The
premium bucket is a price tier (ships, aircraft, premium IoT, and government
uses are illustrative examples of who buys it, never a claim about where 1.25
million units sit). A documented alternative sheet (Sheet B: today's device
ratio, about 39.3 million devices, about $7.07B a year) sits in the scenario
file and the ledger.

The margin definition travels with the number: it measures revenue against
the fleet's full build, launch, and replacement cost. Operations cost is the
explicit zero pending research and corporate overhead is never included, so
this is an operating-style margin, not a gross margin and not a net margin.
Three postures are stated, not hidden: full sell-through (every serveable
slot sells), the constant mix as the fleet grows, and prices held flat. For
scale, Iridium spends about **$376M a year** of real operating cost today
(revenue $871.7M minus operational EBITDA $495.3M, COMM-615/616), and an
Iridium-scaled operating line still leaves the margin north of **93
percent**. The real commercial uncertainties are demand, sell-through, mix,
prices, and actual operating cost.

Two anchors ground the prices:

| Anchor | The numbers |
|---|---|
| What Iridium's customers pay today (FY2025, COMM-618/619) | IoT $7.78; voice and data $47; Certus broadband $259 for a 0.7 Mbps-class service; the fixed about-$108M/yr government contract |
| The investor's standard-tier range | $10 to $20 per month, sized against the about 300 million people without coverage (COMM-021) |

Today's prices are premium-niche prices on a starved network: at $259 for 0.7
Mbps, the incumbent price per megabit runs about $370, roughly 800 times a
terrestrial line (about $80 a month for 170 to 180 Mbps, roughly $0.46 per
megabit; COMM-422). A modernized fleet with about 1,500 times today's supply
on the same spectrum is what breaks that regime: it sells abundance at mass
prices while keeping the premium book (today's Certus buyer gets roughly 4
Mbps instead of 0.7). The standard-tier price sensitivity around the
published point (a sensitivity view pricing the standard tier alone, not a
competing total):

| Standard-tier price | Revenue at 10M subscribers | At the 62-million ceiling |
|---|---|---|
| $10 per month | $1.2B/yr | $7.4B/yr |
| $15 per month | $1.8B/yr | $11.2B/yr |
| $20 per month | $2.4B/yr | $14.9B/yr |

The structural read, scoped to this model: the expensive part of this case
was never the satellites ($725M builds the whole baseline fleet), it was the
spectrum position, and that came with the about-$8.0B acquisition (COMM-602).
The modernized fleet's book replaces today's $871.7M-a-year Iridium book as
the old fleet retires: the two are never summed, and neither are people and
devices.

## The Aperture Explainer

The 60-square-meter case is an explainer, not a model case: if the antenna
were bigger, what would that buy? At 1.6 GHz, frequency does the work of
area: a 25 square meter array already has the gain and cell size of a much
larger array at cellular frequencies, which is why the design point is many
small satellites. A **60 square meter** panel would carry 2.4x the capacity,
spendable either way: roughly double per-user rates at today's density, or
about **74,880 people per satellite** (about 25 million on the same 340
satellites). But a 60 square meter square is about 7.7 meters on a side: it
does not stow in Neutron without folding, which the flat-panel philosophy
rejects, so it needs a larger fairing that does not exist. It stays out of
the model as a labeled hypothetical. Its launch coupling is five satellites
per launch by the inverse-area convention; the separate estimate-bound mass
arithmetic reads six.

## What Would Change The Verdict

- **The reuse calibration.** The 150x effective reuse is the widest physical
  error bar and needs real antenna, interference, and traffic engineering.
- **Concurrency and rate.** Density moves inversely with the 2.5 percent
  busy-hour concurrency and the 1.0 Mbps active rate. Both are dials; the
  off-peak 0.5 percent is an investor-set pair value with no corpus anchor.
- **The orbit metric.** A population-weighted coverage target and an
  operational availability requirement could move the fleet floor from 340.
- **The ecosystem assumption, scoped to the phone row only.** If the band
  never enters standard chipsets, the service is the antenna tiers plus IoT,
  which carry the published economics on their own.
- **IoT contention.** The zero-sizing-load convention needs a joint
  random-access and reservation model; the honest joint reading today is
  about 29,000 people per satellite.
- **The density chains.** The ceiling figures inherit the calibrated
  phone-class chain and its roughly factor-of-two tension with the corpus
  gain-terminal rule (terminal-tier headroom, never blended).
- **Operations cost.** The explicit zero. A real operating line lowers every
  margin; Iridium's own $376M a year is the scale hint.
- **Pricing and sell-through.** The published revenue rests on investor-set
  prices, full sell-through on capacity, and a constant mix: stated scenario
  dials, unproven demand.
- **The manifest share.** All-in is a modeling scenario; lower shares move
  completion years out (half the manifest puts the 340 fleet at 2033).

## Structural Context

This model exists because Rocket Lab agreed to acquire Iridium, which would
reframe it from a greenfield entrant into an incumbent MSS operator with
owned, globally coordinated spectrum, an operating fleet, ground
infrastructure, and 2.5 million existing customers, plus the modernization
decision this model sizes (see
[`research/rocket_lab/iridium_acquisition.md`](../research/rocket_lab/iridium_acquisition.md)).
The broader argument for why Rocket Lab, almost alone, owns the parts, the
rocket, and the production lines to build a fleet like this is the shared
[structural case](../data_center/structural_case.md). This document is the
Iridium numbers. The structural case is the why.

This is a feasibility model, not Rocket Lab guidance, a demand forecast, a
completed spacecraft design, or investment advice. The strongest conclusion
is physical: narrow, reliable L-band can support a useful MSS and IoT product
at the modeled rates if the reuse, orbit, device, and contention assumptions
close in engineering. The deployment schedule and the economics are scenario
layers built on top of that physical case, and their dials are stated where
they bite.
