# The Iridium Model: Conclusion

Under the current baseline, a Neutron-launched next-generation Iridium fleet
looks strong enough to justify serious follow-on work. On the roughly **8 MHz**
of L-band that Iridium already owns outright, a modern **340-satellite** fleet
(the coverage floor) serves about **10 million subscribers** at about **31,200
subscribers per satellite**, deployed by **2035** at an 18 percent share of
Neutron's ramping cadence (about **29 launches**, 12 satellites each). This is
not a precision forecast or a DCF. It is a bounded feasibility exercise built
from visible, source-linked assumptions, and every number here traces to the
frozen model baseline or a cited research claim.

In plain terms: Iridium serves about 2.5 million subscribers today on 66
satellites flying a 1990s architecture, and the whole fleet moves about 174
megabits per second, less than one home internet connection. The spectrum is
not the limit. The old architecture is. A modern flat-panel satellite with
digital beamforming carries roughly **1,000 times** the data of one Iridium
satellite today on the very same spectrum. The rest of this document builds the
outcome of that modernization from its parts.

One assumption sits underneath the phone numbers and is stated here up front,
not buried: a literally unmodified 2026 phone receives nothing on Iridium's
1616 to 1626.5 MHz band. The phone-class rates below assume the band enters
standard phone chipsets (the in-chipset ecosystem assumption), the path
Qualcomm and Iridium built and demonstrated once and then terminated in
November 2023 with zero phone adoption. The barrier there is commercial, not physics.
The terminal and device tiers below need no such assumption: they run on
hardware Rocket Lab could build and ship itself.

## Source Snapshot

The Iridium model is one input scenario promoted to one model output. The
scenario YAML is the single set of input dials, and promoting it produces the
Iridium model JSON. The conclusion is static editorial prose tied to that
promoted default.

| Item | File | What it is |
|---|---|---|
| Iridium model | [`communications/models/iridium/default.json`](models/iridium/default.json) | The promoted model: the frozen baseline, its derivation, units, and sources. |
| Default scenario | [`code/scenarios/iridium.yaml`](../code/scenarios/iridium.yaml) | The input dials that produce the model; copy, edit, and re-run to test alternatives. |
| Assumptions ledger | [`communications/assumptions.md`](assumptions.md) | Every default assumption, its source status, and where it comes from. |
| Design | [`communications/design.md`](design.md) | The workstream architecture and how the model is built. |
| Evidence | [`research/SOURCE_INDEX.md`](../research/SOURCE_INDEX.md) | The `COMM-*` claim ledger and the research wiki. |

## The Fleet, And What It Serves

The story is a modern fleet on old spectrum. Each satellite is a flat-panel
digital-beamforming array of about 25 square meters, with laser crosslinks and
Ka feeder links, so the L-band is spent entirely on user traffic. About 12 fit
on a Neutron launch. The model sizes the fleet as the larger of the coverage
floor (340 satellites for continuous coverage of the populated world) and the
capacity need (321 satellites to hold 10 million subscribers), so coverage
binds and the fleet is **340 satellites**.

| Baseline output (8 MHz exclusive, phone class, 25 square meters) | Value |
|---|---:|
| Per-satellite capacity | about **0.78 Gbps** |
| Subscribers per satellite | about **31,200** |
| Fleet size (coverage floor binds) | **340 satellites** |
| Subscribers served | about **10 million** |
| Fleet aggregate capacity | about **265 Gbps** |
| Coverage complete | **2035** |
| Launches (12 satellites each) | about **29**, at an 18 percent cadence share |

That aggregate of about 265 Gbps across 340 modern satellites is more than a
thousand times the roughly 174 Mbps the entire 66-satellite Iridium fleet moves
today. The gain is almost all architecture: more beams, digital beamforming,
and dense cell reuse on the same held megahertz.

## Per Subscriber, By Device

The per-person ceiling is the beam pool, not the satellite total. A phone lives
in one beam and shares that beam's pool with the other people in it. On the
owned 8 MHz the phone-class beam pool is about 5.2 Mbps. The service is sized so
a phone sees about **1.0 Mbps at peak** and about **5.0 Mbps off peak**, with no
external antenna. Users who opt into a small antenna get more, because a larger
antenna holds a higher spectral efficiency:

| Device (same ~31,200 subscribers per satellite, 8 MHz) | Peak | Lightly loaded |
|---|---:|---:|
| Phone, no external antenna | about **1.0 Mbps** | about **5.0 Mbps** |
| Small boosted antenna | about **3.1 Mbps** | about **15.4 Mbps** |
| Larger mounted antenna | about **3.9 Mbps** | about **19.2 Mbps** |

These rates support messaging, voice, browsing, maps, photos, and audio.
Probably not streaming video. The rates are estimate-tier, derived from the
model's own spectral-efficiency tiers (phone about 0.65 bits per hertz, small
terminal about 2.0, larger terminal about 2.5). Held instead at the phone's 1.0
Mbps active rate, the same antennas raise density rather than speed, to about
96,000 and 120,000 subscribers per satellite.

Separately, and counted separately, the same fleet carries **tens of millions
of IoT devices**. IoT are devices, not people. They ride nearly free: at
kilobit-class narrowband rates the binding limit is random-access contention,
not spectrum, so the model passes through 10 million IoT devices with zero
sizing effect on the subscriber service.

## Revenue And Cost

The default revenue case is cost-plus, the same discipline as the data-center
model: price at a flat 1.5 times annualized cost, which produces a **33.3
percent margin**. On the 340-satellite baseline the cost-plus revenue is about
**251.5 million dollars per year** at that margin. The subscriber-price (ARPU)
revenue case is deliberately deferred: it awaits the founder setting per-tier
MSS prices, so the model does not yet publish an ARPU revenue number. As a
grounded shape datapoint, Iridium today turns 2.54 million subscribers into
about 872 million dollars a year of total revenue.

The build-and-hold cost of the 340-satellite fleet is about **1,085 million
dollars**. The cash cost per subscriber is about **7.95 dollars per year**,
with a caveat: that figure is a build-year cash artifact (fleet cost spread over
the served base in the coverage year), not a life-amortized number. On an
annualized basis the per-subscriber cost is higher (roughly 17 dollars per
subscriber per year at 10 million), and aligning the model to the annualized
basis is a tracked open item. Operations cost is held at **zero** by explicit
assumption, a fixed line to research and add later, and it is stated in every
model output rather than hidden.

## The Spectrum Upside, And The Aperture Story

Two levers move the baseline, and both are labeled so they are never mistaken
for the default.

The first is spectrum. The 8 MHz baseline is the exclusive holding. Iridium's
full coordinated span is **10.5 MHz**, including a Globalstar-shared sliver that
is the subject of a live FCC dispute (which becomes Rocket Lab versus Amazon
after both acquisitions close). Winning the full 10.5 MHz adds about **31
percent** to everything, to about 40,950 subscribers per satellite. It is gated
on that coordination, so it is an upside variant, not the baseline.

The second is aperture. At 1.6 GHz, frequency does the work of area: a 25
square meter array has the gain and cell size of a much larger array at cellular
frequencies, so the design point is many small satellites, not few large ones.
25 square meters is also the no-fold maximum of Neutron's 5.5 meter fairing. A
larger satellite of about **60 square meters** roughly doubles per-phone rates
(a phone would see about 2 Mbps at peak and closer to 10 off peak) and lifts
per-satellite density to about 74,880 subscribers, about 25 million at the same
340 satellites. But a 60 square meter panel is about 7.7 meters across its
smallest dimension. It does not stow flat in Neutron's fairing without folding,
which the flat-panel design philosophy rejects, and a no-fold 60 square meter
satellite needs a roughly 7-to-8-meter-class fairing, a larger and heavier
rocket. That vehicle does not exist, so the larger-aperture case stays out of
the model and lives here in prose as a labeled hypothetical: a real later step,
not a slight stretch.

Deployment speed is the third dial. At the conservative 18 percent cadence share
the coverage fleet completes in 2035. At a higher launch share the same 29
launches compress into a **3 to 7 year** build. 340 is a floor, not a ceiling,
and the next section is what happens as the fleet grows past it.

## The Saturation Ceiling

The founder's load-bearing point: past some number of satellites, more
satellites stop helping. On a fixed band, capacity comes from beams reusing the
spectrum over non-overlapping patches of ground. Once every patch under the
fleet is already covered by a beam on the 8 MHz, adding more satellites adds
overlapping co-channel beams that interfere rather than add, and the system goes
interference-limited. The model encodes this as a saturation cap of about
**2,000 satellites**. The mechanism is multi-source in the corpus
([`research/direct_communication/dtc_capacity_supply.md`](../research/direct_communication/dtc_capacity_supply.md),
COMM-413 through COMM-416).

At the cap, the model's own numbers by service tier:

| Tier | Subscribers per satellite | At the 2,000-satellite cap |
|---|---:|---:|
| Standard (1.0 Mbps active) | 31,200 | about **62 million** |
| Rich (2.5 Mbps active) | 12,480 | about **25 million** |

A warning must travel with these numbers, and it is loud on purpose: the
corpus carries two density chains, and they are different-meaning numbers. The
model's chain is capacity-first: per-satellite Gbps calibrated to the corpus
supply anchor, then divided by the per-user load at phone-class efficiency,
giving the 31,200 and the cap figures above. The corpus separately carries a
density rule of about 3,000 subscribers per satellite per megahertz, built on
gain-terminal spectral efficiency, and at these tiers it implies roughly twice
these densities (about 24,000 per satellite at the 2.5 Mbps rate on 8 MHz,
about 48 million at the cap). Both chains are estimate-tier, and they are not
the same calculation, so they must never be blended. The sharpest trap is a
near-collision: the model's **31,200** (8 MHz, 1.0 Mbps, phone-class
efficiency) and the corpus rule's **31,500** (10.5 MHz, the
3,000-per-megahertz chain) are numerically adjacent and conceptually
different. Never conflate them. The numbers this conclusion stands behind are
the model's calibrated numbers, the conservative side at these tiers.

### Why Can Starlink Fly 11,000-Plus Satellites When We Saturate At 2,000?

The saturation ceiling scales with the spectrum held, so the honest answer is
that Starlink's ceiling sits far higher because Starlink holds far more
spectrum, discriminates with a dish that a phone cannot, and spreads its fleet
across orbital shells. Three grounded reasons, in order of weight:

1. **Spectrum breadth.** Starlink's broadband service rides on the order of
   **2,000-plus megahertz** of Ku-band user spectrum (eight 250 MHz channels),
   and the whole system incorporates more than 20 GHz once the Ka and E-band
   backhaul are counted. That is against our **8 to 10.5 MHz** of L-band. The
   saturation ceiling is linear in spectrum, so a fleet on hundreds of times the
   bandwidth saturates at hundreds of times the satellite count.

2. **Terminal gain.** A Starlink dish has real aperture and discriminates
   angularly: it can distinguish satellites in different sky positions, so many
   satellites can reuse the same frequencies to neighboring dishes at the same
   time. That angular reuse is a whole extra dimension a zero-gain phone
   physically cannot offer. Our phone tier has no such discrimination, which is
   exactly why the phone lane is the tightest one.

3. **Shells and inclinations.** Starlink flies multiple orbital shells at
   different altitudes and inclinations (the Gen2 plan is roughly 30,000
   satellites across shells near 340 to 360, 525 to 535, and 604 to 614
   kilometers). Inclination concentrates satellites over the latitudes where
   demand is, and multiple shells ease coordination. This is the smallest of the
   three factors, and interference between Starlink's own satellites is real but
   managed, with narrow beams on both ends plus frequency coordination.

The clean check, and it is estimate-tier: Starlink's own dedicated
direct-to-cell fleet is filed at **15,000 satellites on about 65 MHz** of
cellular spectrum, roughly **230 satellites per megahertz**. Our saturation cap
is **2,000 satellites on 8 MHz**, roughly **250 satellites per megahertz**.
Almost the same satellites-per-megahertz ratio. It is the same physics and the
same wall, scaled by the spectrum each system holds. Starlink does not escape
the ceiling. It buys a higher one.

## What Would Change The Verdict

The baseline is the reference case, and a handful of assumptions carry it:

- **The ecosystem assumption.** If Iridium's band never enters standard phone
  chipsets, the phone-class rates do not reach unmodified phones at all, and the
  reachable service is the terminal and device tiers plus IoT. The barrier is
  commercial, not physical, but it is real and unresolved.
- **Concurrency.** The per-user rates rest on 2.5 percent busy-hour and 0.5
  percent off-peak concurrency. The peak figure is corpus-central; the off-peak
  figure is a founder-set pair with no corpus anchor.
- **The density chains.** The 62-million and 25-million cap figures inherit the
  calibrated chain and its roughly factor-of-two tension with the corpus rule.
- **Operations cost.** Held at zero by explicit assumption. A real operating
  line will lower every margin.

## Structural Context

This model exists because Rocket Lab bought Iridium, which reframes Rocket Lab
from a greenfield entrant into an incumbent MSS operator with owned,
globally-coordinated spectrum, an operating fleet, ground infrastructure, and
2.5 million customers, plus the modernization decision this model sizes (see
[`research/rocket_lab/iridium_acquisition.md`](../research/rocket_lab/iridium_acquisition.md)).
The broader argument for why Rocket Lab, almost alone, owns the parts, the
rocket, and the production lines to build a fleet like this is the shared
[structural case](../data_center/structural_case.md). This document is the
Iridium numbers. The structural case is the why.
