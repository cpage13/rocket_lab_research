# The Iridium Model: Conclusion

Rocket Lab is acquiring Iridium, and with it a rare asset: a globally
coordinated L-band allocation it will own outright. This document is the
feasibility verdict on modernizing that spectrum with a Neutron-launched
fleet.

The business meaning in one paragraph: for about **$900 million** of total
hardware and launch spend, a 340-satellite fleet serves about 10 million
subscribers plus about 52 million IoT devices and earns about **$8.25 billion
a year** at set prices, an operating margin near **98 percent** against the
$145 million a year it costs to keep the fleet flying. Scaled to the most
satellites the spectrum can use, about 2,000, the same sheet reads about
**$48.5 billion a year**. The bet is demand and the not-yet-modeled
operations line, never the hardware.

| The verdict at a glance | At 340 satellites (the baseline) | At about 2,000 satellites (the ceiling) |
|---|---|---|
| Complete by | 2035 at an 18 percent launch share; 2031 with most of the manifest | about 2035 with 90 percent or more of the manifest |
| Subscribers (people) | about 10.6 million | about 62 million |
| IoT devices (counted separately) | about 51.7 million | about 304 million |
| Revenue per year (the published sheet) | about $8.25B | about $48.5B |
| Fleet cost per year | about $145M | about $835M |
| Operating margin (pre-operations) | about 98.2 percent | about 98.3 percent |

This is not a precision forecast or a DCF. It is a bounded feasibility
exercise built from visible, source-linked assumptions, and every number
here traces to the frozen model baseline, a cited research claim, or an
explicitly labeled scenario dial. The assumptions that carry the table are
stated where they bite and collected at the end.

## Source Snapshot

The Iridium model is one input scenario promoted to one model output. The
scenario YAML is the single set of input dials; promoting it produces the
model JSON; this conclusion is static editorial prose tied to that promoted
default.

| Item | File | What it is |
|---|---|---|
| Iridium model | [`communications/models/iridium/default.json`](models/iridium/default.json) | The promoted model: the frozen baseline, its derivation, units, and sources |
| Default scenario | [`code/scenarios/iridium.yaml`](../code/scenarios/iridium.yaml) | The input dials; copy, edit, and re-run to test alternatives |
| Assumptions ledger | [`communications/assumptions.md`](assumptions.md) | Every default assumption, its source status, and where it comes from |
| Design | [`communications/design.md`](design.md) | The workstream architecture and how the model is built |
| Evidence | [`research/SOURCE_INDEX.md`](../research/SOURCE_INDEX.md) | The `COMM-*` claim ledger and the research wiki |

## What We Have: The Spectrum

Two different quantities hide in "8 MHz of L-band at 1.6 GHz", and the model
rests on keeping them apart. The frequency (about 1.6 GHz) is where the
signal sits on the dial: it sets reach, and L-band's reach is the product
story (the rain, clouds, and foliage that degrade Ku- and Ka-band broadband
barely touch it; COMM-627). The bandwidth is the width held: it sets
capacity.

| Holding | Width | Status |
|---|---|---|
| Exclusive (1618.725 to 1626.5 MHz) | 7.775 MHz | Owned outright; the baseline models it as 8.0 (COMM-611) |
| Shared with Globalstar | 0.95 MHz | Usable today under coordination |
| Full coordinated span (1616 to 1626.5 MHz) | 10.5 MHz | The upside variant: a live FCC dispute (Rocket Lab versus Amazon after both deals close) |

Winning the full 10.5 MHz adds about **31 percent** to everything in this
document (about 40,950 subscribers per satellite instead of 31,200). It is
gated on that coordination, so it is a labeled variant, never the baseline.

## What We Build: The Satellite

Each modeled satellite is a flat-panel **phased array of about 25 square
meters** with digital beamforming, laser crosslinks between satellites (so
traffic routes in space and the L-band is spent entirely on users), and Ka
feeder links. About **12 fit on one Neutron launch**.

| Per satellite | Today's Iridium (66 satellites) | The modeled satellite |
|---|---|---|
| Throughput | about 2.64 Mbps (COMM-639) | about 780 Mbps at the weakest device class |
| The multiple | | roughly 300x (about 1,000x to gain terminals, the corpus modernization figure) |

Fleet against fleet, 340 modern satellites move about **265 Gbps** against
the roughly 174 Mbps the whole 66-satellite fleet moves today: more than a
thousandfold, of which roughly 300x is per-satellite architecture and about
5x is flying 340 satellites instead of 66.

## How The Capacity Numbers Arise

The per-satellite chain is short enough to hold in your head, and every link
carries a labeled status:

| Link | Value | Status |
|---|---|---|
| Spectrum held (a width) | 8.0 MHz | Fact (7.775 MHz exclusive, rounded; COMM-611) |
| Weakest-class spectral efficiency | 0.65 bits per hertz | Measured in the wild (COMM-428/429) |
| Effective spectrum reuse | about 150x | Calibrated estimate (corpus band 130 to 200x; COMM-410/411) |
| Busy-hour concurrency | 2.5 percent | Corpus-central (1 to 5 percent; COMM-543) |
| Active rate (the service tier) | 1.0 Mbps | Chosen dial |

Walk it forward. One beam running the whole 8 MHz at the weakest device
class's efficiency carries 8 x 0.65 = **5.2 Mbps**: the beam pool, and the
hard per-person ceiling. The satellite does not light one beam: it aims
about 150 of them at different patches of ground and reuses the same 8 MHz
in every one, the way a terrestrial network reuses its band across cells.
So one satellite moves 5.2 x 150 = **780 Mbps**. The code packages the reuse
as the 0.15 constant (150 reuses divided by 1,000, quoted per unit of
spectral efficiency so one constant serves every device tier). The last step
is people: at the busy hour 2.5 percent of subscribers transmit at once, so
780 Mbps across 31,200 x 0.025 = 780 active users is **1.0 Mbps each**, and
the density is the same equation run backwards: 780 / (1.0 x 0.025) =
**31,200 subscribers per satellite**.

Two links carry the real uncertainty. The 0.65 is the strongest external
anchor in the model (measured over the air on Starlink's operating phone
service, median 0.64, interference included). The 150x reuse calibration is
the widest error bar and the number real engineering would move first:
across the corpus band edges (the efficiency band and the supply-anchor band
together) per-satellite capacity spans roughly 0.3 to 1.5 Gbps against the
0.78 central. The model quotes calibrated centrals and treats everything
else as sweepable dials.

## Who Uses It: The Devices

The service is device-diverse by design, and the ladder leads with the
hardware Rocket Lab can build and ship without anyone's permission:

| Device tier | Efficiency (bits/Hz) | Peak | Lightly loaded | Requires |
|---|---|---|---|---|
| Small antenna (a puck, or a USB device on a laptop; about 10 dBi, unpointed) | 2.0 | about 3.1 Mbps | about 15.4 Mbps | Nothing: our hardware |
| Mounted antenna (vehicles, ships, fixed sites; 15+ dBi) | 2.5 | about 3.9 Mbps | about 19.2 Mbps | Nothing: our hardware |
| Phone, a possible later path (0 dBi, no external antenna) | 0.65 | about 1.0 Mbps | about 5.0 Mbps | The band in standard phone chipsets |

Three facts organize the table:

1. **The per-person ceiling is the beam pool, never the satellite total.** A
   user lives in one beam and shares that beam's pool (bandwidth times the
   tier's efficiency) with the other users in it. The 150x reuse multiplies
   how many people the satellite serves, never one person's rate.
2. **The baseline is computed at the weakest tier on purpose.** The 31,200
   density and every headline number use the phone-class 0.65, so the
   published numbers are the conservative floor: every real device on the
   ladder does better on the same fleet. Held at the same 1.0 Mbps rate, the
   antenna tiers raise density instead of speed, to about 96,000 and 120,000
   subscribers per satellite.
3. **Only the phone row carries an ecosystem assumption.** Iridium's band is
   in no standard phone chipset today (Qualcomm and Iridium built and
   demonstrated that chip once; it was terminated in November 2023 with zero
   phone adoption: the barrier is commercial, not physics). The antenna
   tiers need no such assumption, which is why the phone is one possible
   later path and never the dependency.

The rates support messaging, voice, browsing, maps, photos, and audio.
Probably not streaming video, and the service does not pretend otherwise.
The band's reliability carries the product: a link that holds in rain, under
foliage, and in motion (COMM-426/563, and the L-band row COMM-627; the
first-principles explainer is
[`research/direct_communication/spectrum_and_phased_array_fundamentals.md`](../research/direct_communication/spectrum_and_phased_array_fundamentals.md))
is a different product from a dish that needs clear sky, even at a fraction
of the speed.

Separately, and counted separately, the same fleet carries **tens of
millions of IoT devices**. IoT are devices, not people, and they ride nearly
free: at kilobit-class rates the binding limit is random-access contention,
not spectrum, so IoT is zero load in the sizing. The published device count
derives from the revenue mix (about 51.7 million at the baseline); the
10-million passthrough dial reports only when the ARPU case is off.

## How It Deploys: Launches And The Ceiling

The model sizes the fleet as the larger of the coverage floor and the
capacity need, capped at saturation: at the 10-million target, coverage
binds (the capacity need is 321 satellites), so the baseline fleet is
**340 satellites, about 29 Neutron launches**. The ceiling is about
**2,000 satellites, about 167 launches** (the two columns of the verdict
table). Deployment speed is purely a manifest-share dial, and these are
model runs, not estimates:

| Share of Neutron's launches | The 340-satellite fleet completes |
|---|---|
| 18 percent (the conservative baseline) | 2035 |
| 50 percent | 2033 |
| 80 percent | 2032 |
| 90 to 100 percent | 2031, the floor: the early whole-fleet ramp (2, 3, 5, 9, 14 launches a year through 2031) binds, not the share |

These timelines assume Neutron does the launching. Reaching the 2,000
ceiling takes about 167 launches: about 2035 with 90 percent or more of the
manifest, past the modeled decade at smaller shares.

Why a ceiling exists at all: on a fixed band, capacity comes from beams
reusing the spectrum over separated patches of ground, and once every patch
is covered by a beam on the 8 MHz, additional satellites add overlapping
co-channel beams that interfere rather than add. The model encodes this as
the saturation cap of about 2,000 satellites (the mechanism is
multi-source:
[`research/direct_communication/dtc_capacity_supply.md`](../research/direct_communication/dtc_capacity_supply.md),
COMM-413 to COMM-416), which is where the verdict table's 62-million
subscriber column comes from: 31,200 per satellite times 2,000 satellites.
A richer service tier trades headcount for speed: at a 2.5 Mbps active rate
the density falls to 12,480 per satellite (a capacity-bound 802-satellite
fleet serves the 10-million target, and at the 0.18 share it truthfully
reaches only 576 of 802 by FY2036).

One warning travels with the cap figures, loud on purpose. The corpus
carries a second density chain, about 3,000 subscribers per satellite per
megahertz, built on **gain-terminal** efficiency, and it implies roughly
twice these densities. The two chains are different calculations at
different device classes and must never be blended: the model's **31,200**
(8 MHz, phone-class) and the corpus rule's **31,500** (10.5 MHz,
gain-terminal chain) are numerically adjacent and conceptually different.
This conclusion stands behind the model's calibrated chain, the conservative
side; the gain-terminal chain is best read as the terminal-tier headroom
above it.

### Why Starlink Flies Thousands More Satellites Than Our Ceiling

The ceiling scales with spectrum and with what the user's hardware can do,
so the honest comparison is a table:

| Factor | Starlink broadband | This fleet |
|---|---|---|
| User spectrum | 2,000+ MHz of Ku (eight 250 MHz channels; 20+ GHz system-wide with backhaul) | 8 to 10.5 MHz of L-band |
| User hardware | A pointed dish: real aperture, angular discrimination | The same physics on our antenna tiers (puck about 10 dBi, mounted 15+ dBi); none on the phone tier |
| Constellation | Multiple shells and inclinations (the Gen2 plan is about 30,000 satellites near 340 to 360, 525 to 535, and 604 to 614 km) | One constellation (orbit selection is open design work) |
| The wall, normalized | about 15,000 D2C satellites filed on about 65 MHz: about 230 satellites per MHz | about 2,000 on 8 MHz: about 250 satellites per MHz |

The bottom row is the point: nearly the same satellites-per-megahertz
ratio. It is the same physics and the same wall, scaled by the spectrum each
system holds. Starlink does not escape the ceiling; it buys a higher one
with spectrum breadth, which is the dominant factor by far.

The hardware row deserves one honest clarification, because it is not a gap
between companies: it is a gap between device tiers. A terminal with real
aperture discriminates angularly (it can tell satellites apart by sky
position), which lets many satellites reuse the same frequencies to
neighboring users: an extra reuse dimension. **Our puck and mounted tiers
have exactly that physics**: it is why their efficiency is 2.0 to 2.5
against the phone's 0.65, and it is where the corpus's roughly-2x
gain-terminal density chain comes from. The tier that cannot discriminate is
the phone, and the model deliberately computes its headline numbers at that
weakest tier. So the published ceiling is the phone-lane ceiling, the
tightest one; a terminal-weighted service has documented headroom above it.

## What It Means For The Business: Revenue, Cost, And Margin

The cost model is deliberately flat (a founder simplification, 2026-07-09),
and both dials sit in-band of the research anchors:

| Cost line | Value | Grounding |
|---|---|---|
| Satellite build | $1.0M each | Just below the prior 1.05 dial and the about-$1.2M Starlink V3 hardware anchor (COMM-080) |
| Launch, flat at any cadence | $13.0M | Just below the shared curve's grounded $13.5M high-cadence floor |
| Build-and-hold through FY2036 | $900M exactly | The 29-launch build plus the replacement treadmill: 432 satellites across 36 launches |
| Steady-state fleet cost | $145M per year | Satellites are replaced on a five-year life |
| Per subscriber | $7.50 per year (one lumpy final year of satellite replacement spread over the base, not life-amortized); about $14.50 annualized | Aligning to the annualized basis is a tracked open item |

Operations cost is held at **zero** by explicit assumption, a fixed line to
research and add later, stated in every model output rather than hidden.

The published revenue case is the four-bucket ARPU sheet (Sheet A,
founder-set 2026-07-09): each bucket is a set price and a percentage of the
fleet's billable-connection pool, so every bucket scales with the satellite
count. The prices are anchored on what Iridium's customers pay today; the
mix is a set split, loosely guided by the shape of Iridium's base, with
government pinned to reproduce today's fixed contract. One table carries the
whole business at both fleet sizes:

| Bucket | Mix and price | At 340 satellites | At about 2,000 satellites |
|---|---|---|---|
| Standard personal | 15.0 percent at $15/mo | 9,360,000 people, $1.68B/yr | 55,058,824 people, $9.91B/yr |
| Premium terminal | 2.0 percent at $100/mo | 1,248,000 people, $1.50B/yr | 7,341,176 people, $8.81B/yr |
| IoT devices | 82.8 percent at $8/mo | 51,670,320 devices, $4.96B/yr | 303,943,059 devices, $29.18B/yr |
| Government | 0.2 percent at $74/mo | 121,680, $0.11B/yr | 715,765, $0.64B/yr |
| Total revenue | 100 percent | $8.25B/yr on a 62,400,000-connection pool | $48.5B/yr on a 367,058,824-connection pool |
| Fleet cost | | $145M/yr | $835M/yr |
| **Operating margin (pre-operations)** | | **about 98.2 percent** | **about 98.3 percent** |

The pool is a billable-connections accounting frame over which the mix
percentages are defined: subscribers are people, IoT are devices, government
is a contract line, and the three are never summed as one population. The
premium bucket is a price tier (ships, aircraft, premium IoT, and government
uses are illustrative examples of who buys it, never a claim about where
1.25 million units sit). A documented alternative sheet (Sheet B: today's
device ratio, about 39.3 million devices, about $7.07B a year) sits in the
scenario file and the ledger.

The margin definition travels with the number: it measures revenue against
the fleet's full build, launch, and replacement cost; operations cost is the
explicit zero pending research and corporate overhead is never included, so
it is an operating-style margin in the data-center model's convention, not a
gross margin and not a net margin. For scale, Iridium spends about **$376M a
year** of real operating cost today (revenue $871.7M minus operational
EBITDA $495.3M, COMM-615/616), so an Iridium-scaled operating line still
leaves the margin north of **90 percent**. Three postures are stated, not
hidden: full sell-through (every serveable slot sells), the constant mix as
the fleet grows, and prices held flat.

Two anchors ground the prices:

| Anchor | The numbers |
|---|---|
| What Iridium's customers pay today (FY2025, COMM-618/619) | IoT $7.78; voice and data $47; Certus broadband $259 for a 0.7 Mbps-class service; the fixed about-$108M/yr government contract |
| The founder's standard-tier range | $10 to $20 per month, sized for the about 300 million people without coverage (COMM-021) |

Today's prices are premium-niche prices on a starved network: at $259 for
0.7 Mbps, the incumbent price per megabit runs roughly 650 times terrestrial
broadband (a home line at about $100 a month for about 180 Mbps is roughly
$0.55 per megabit; Certus is about $370). A modernized fleet with about
1,500 times today's supply on the same spectrum is what breaks that regime:
it sells abundance at mass prices while keeping the premium book (today's
Certus buyer gets roughly 4 Mbps instead of 0.7). The standard-tier price
sensitivity around the published point (a sensitivity view pricing the
standard tier alone, not a competing total):

| Standard-tier price | Revenue at 10M subscribers | At the 62-million ceiling |
|---|---|---|
| $10 per month | $1.2B/yr | $7.4B/yr |
| $15 per month | $1.8B/yr | $11.2B/yr |
| $20 per month | $2.4B/yr | $14.9B/yr |

The structural read: the expensive part of this business was never the
satellites ($900M builds the whole baseline fleet), it was the spectrum
position, and that came with the about-$8.0B acquisition (COMM-602). The
modernized fleet's book replaces today's $871.7M-a-year Iridium book as the
old fleet retires; the two are never summed, and neither are people and
devices.

## The Aperture What-If

At 1.6 GHz, frequency does the work of area: a 25 square meter array has the
gain and cell size of a much larger array at cellular frequencies, so the
design point is many small satellites, not few large ones, and 25 square
meters is the no-fold class for Neutron's 5.5 meter fairing. A **60 square
meter** satellite carries 2.4x the capacity, spendable one way or the other:
per-user peak rates roughly double at today's density (the lightly-loaded
reading stays capped by the class-fixed beam pool), or density rises to
about **74,880 per satellite** (about 25 million at the same 340 satellites;
the model's what-if takes the density side). But a 60 square meter panel is
about 7.7 meters on a side as a square: it does not stow in Neutron without
folding, which the flat-panel philosophy rejects, so the case needs a
7-to-8-meter-class fairing, a larger rocket that does not exist. It stays
out of the model as a labeled hypothetical: a real later step, not a slight
stretch.

## What Would Change The Verdict

- **The ecosystem assumption, scoped to the phone row only.** If Iridium's
  band never enters standard phone chipsets, the phone tier stays closed and
  the service is the antenna tiers plus IoT, which carry the published
  economics on their own. Commercial barrier, not physical.
- **Concurrency.** The per-user rates rest on 2.5 percent busy-hour and 0.5
  percent off-peak. The peak figure is corpus-central; the off-peak figure
  is a founder-set pair with no corpus anchor.
- **The density chains.** The ceiling figures inherit the calibrated
  phone-class chain and its roughly factor-of-two tension with the corpus
  gain-terminal rule (read: terminal-tier headroom, never blended).
- **Operations cost.** The explicit zero. A real operating line lowers every
  margin; Iridium's own $376M a year is the scale hint.
- **Pricing and sell-through.** The published revenue rests on founder-set
  prices (Sheet A: 15 / 100 / 8 / 74), full sell-through on capacity, and a
  constant mix as the fleet grows: stated scenario dials, unproven demand.

## Structural Context

This model exists because Rocket Lab bought Iridium, which reframes Rocket
Lab from a greenfield entrant into an incumbent MSS operator with owned,
globally coordinated spectrum, an operating fleet, ground infrastructure,
and 2.5 million customers, plus the modernization decision this model sizes
(see
[`research/rocket_lab/iridium_acquisition.md`](../research/rocket_lab/iridium_acquisition.md)).
The broader argument for why Rocket Lab, almost alone, owns the parts, the
rocket, and the production lines to build a fleet like this is the shared
[structural case](../data_center/structural_case.md). This document is the
Iridium numbers. The structural case is the why.
