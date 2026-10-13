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
low cost. That is the product. It is first an IoT network. It also serves
people on small self-orienting terminals and on mounted antennas. It can carry
phones and voice later.

Two models answer the question. They stand side by side, and their numbers
never add:

- **The engineering case** (the Iridium model) asks what the fleet can carry.
  It sells every seat of each people class, each class alone. It publishes IoT
  as a capacity, never as sales.
- **The product case** asks what the network would sell. It sells four classes
  at the investor's prices, held flat: the small terminal, the mounted
  terminal, minimal-packet IoT and data IoT. Its headline is the typical market
  of 2,000 drawn markets.

## The Verdict At A Glance

The answer, in short:

- **The fleet.** Fly every Neutron launch on the shared ramp and the fleet
  passes the 340-satellite coverage floor in FY2031, with 528 satellites
  flying. By FY2036 it flies 4,288 satellites. It costs $1,554.4M a year then.
- **The product case.** At the investor's prices the network would earn
  **$13,156.2M a year in FY2036 at an 88.2 percent margin**. About four fifths
  of it is IoT. This is the typical market. It sits a little below the median
  of the markets where the case works ($14,159.9M).
- **The engineering case.** Each people class could fill the whole fleet
  alone. In FY2036 the small terminal alone would serve 24.6 million people
  for $2,952.8M a year, at a 47.4 percent own margin. The mounted terminal
  alone would serve 3.5 million for $2,116.3M, at 26.5 percent.
- **IoT's room is large.** In FY2036 the fleet's IoT uplink fits 11.5 billion
  minimal-packet devices (that class alone: a capacity, not a forecast). The
  product case sells 184.9 million of them.

The plan by date. Each satellite lives five years, so the fleet flying is the
last five years' launches, 16 satellites to a launch:

| Year | Neutron launches that year | Satellites flying | The fleet's cost a year |
|---|---|---|---|
| FY2031 | 14 | 528 | $191.4M |
| FY2033 | 35 | 1,360 | $493.0M |
| FY2035 | 70 | 3,072 | $1,113.6M |
| FY2036 | 90 | 4,288 | $1,554.4M |

The product case, in the typical market:

| Year | Revenue a year | Margin | IoT's share of revenue |
|---|---|---|---|
| FY2031 | $2,194.6M | 91.3 percent | 79.4 percent |
| FY2033 | $5,465.7M | 91.0 percent | 80.0 percent |
| FY2035 | $10,527.3M | 89.4 percent | 79.6 percent |
| FY2036 | $13,156.2M | 88.2 percent | 79.1 percent |

The engineering case, each terminal alone (people; revenue a year; own
margin). Each column is the whole fleet sold to that class, so the columns
never add:

| Year | Small terminal ($10 a month) | Mounted terminal ($50 a month) |
|---|---|---|
| FY2031 | 4,139,229; $496.7M; 61.5 percent | 526,557; $315.9M; 39.4 percent |
| FY2033 | 9,941,462; $1,193.0M; 58.7 percent | 1,289,233; $773.5M; 36.3 percent |
| FY2035 | 19,400,399; $2,328.0M; 52.2 percent | 2,676,447; $1,605.9M; 30.7 percent |
| FY2036 | 24,607,046; $2,952.8M; 47.4 percent | 3,527,090; $2,116.3M; 26.5 percent |

Four things never add:

- The engineering case and the product case. They answer different questions.
  Read them side by side.
- People and devices.
- IoT and government.
- The two applications. The data-center model's all-in case flies the same 301
  launches through FY2036. Each application runs as if it had the shared ramp
  to itself, so their headlines never add.

This is not a precision forecast or a DCF. It is a feasibility study built
from visible, source-linked assumptions. Every number here comes from the
promoted artifacts, a cited research claim, or a setting the investor made.

## Source Snapshot

| Item | File | What it is |
|---|---|---|
| The Iridium model (the engineering case) | [`communications/models/iridium/default.json`](models/iridium/default.json) | Each people class's people, revenue and own margin per year, IoT's room and capacity, and the readings (schema `iridium-v7`, stamp 2026-10-13) |
| The saturation curve | [`communications/models/iridium/saturation_curve.json`](models/iridium/saturation_curve.json) | The useful beams each fleet keeps lit over places people live, per class, at the 25 m^2 reference panel (schema `saturation-v1`, stamp 2026-10-12) |
| The product case | [`communications/models/product_case/default.json`](models/product_case/default.json) | The four classes per reported year in the typical market, the spreads over 2,000 drawn markets, and the checks (schema `product-case-v1`, stamp 2026-10-13) |
| The scenarios | [`code/scenarios/iridium.yaml`](../code/scenarios/iridium.yaml), [`code/scenarios/product_case.yaml`](../code/scenarios/product_case.yaml) | The settings each model reads |
| Assumptions ledger | [`communications/assumptions.md`](assumptions.md) | Every default assumption, its source status, and where it comes from |
| Design | [`communications/design.md`](design.md) | The application's architecture and how the models are built |
| Evidence | [`research/SOURCE_INDEX.md`](../research/SOURCE_INDEX.md) | The `COMM-*` claim ledger and the research wiki |

## What We Have: The Spectrum

Two different quantities hide in "8 MHz of L-band at 1.6 GHz", and the model
rests on keeping them apart. The frequency (about 1.6 GHz) is where the
signal sits on the dial: it sets reach, and reach is the product story. The
bandwidth is the width held: it sets capacity.

| Holding | Width | Status |
|---|---|---|
| Exclusive (1618.725 to 1626.5 MHz) | 7.775 MHz | Owned outright; the model holds 8.0 (COMM-611) |
| Shared with Globalstar | 0.95 MHz | Usable today under coordination |
| Full coordinated span (1616 to 1626.5 MHz) | 10.5 MHz | Contingent upside: a live FCC dispute (Rocket Lab versus Amazon after both deals close) |

Winning the full 10.5 MHz would raise people and each class's revenue by about
31 percent (10.5 / 8 = 1.3125). The fleet and its cost would not move. The
saturation curve is computed at 8 MHz, so this is a linear note, not a model
run.

## What We Build: The Satellite

Each modeled satellite is a flat-panel phased array with digital beamforming,
laser crosslinks between satellites (so traffic routes in space and the L-band
is spent entirely on users), and Ka feeder links. The panel is the Flatellite
body Rocket Lab drew: at most **15.4 square meters**, about 4.1 by 4.0 meters,
sized to Neutron's 4.79 meter usable fairing band (COMM-711). **Sixteen fit on
one Neutron launch** with the Neutron block upgrade assumed from the first
launch (COMM-713). Fifteen fit without it, a mass-bound count today
(COMM-712).

| Per satellite | Today's Iridium (66 satellites) | The modeled satellite |
|---|---|---|
| Peak throughput | about 2.64 Mbps of voice payload | 1,478.4 Mbps for the small terminal, 1,848 Mbps for the mounted terminal |

That is about 560 times today's per-satellite payload, at the small
terminal's peak. The incumbent figure is reproducible but rests on a
single-lineage input (COMM-639), so read the comparison as a tensioned
estimate, not a certified fleet total.

## How The Capacity Arises

The chain is short, and every link carries a labeled status:

| Link | Small terminal | Mounted terminal | Status |
|---|---|---|---|
| Spectrum held (a width) | 8 MHz | 8 MHz | Fact: 7.775 MHz exclusive, rounded (COMM-611) |
| Spectral efficiency | 2.0 bits per hertz | 2.5 bits per hertz | Estimate: the central value of 1.5 to 2.5 and of 2 to 3 |
| One beam | 16 Mbps | 20 Mbps | The width times the efficiency |
| Beams per satellite | 92.4 | 92.4 | 150 on the 25 m^2 reference panel (the reuse calibration, an estimate, COMM-410, COMM-411), times 15.4 / 25 = 0.616 |
| The satellite's peak | 1,478.4 Mbps | 1,848 Mbps | The beams times one beam |
| A beam's downlink pool | 10.72 Mbps | 13.4 Mbps | One beam times the downlink share, 0.67 |

The band is time-shared between the two directions. The downlink holds 67
percent of the frame (the downlink share, ADR 008). The uplink holds the rest,
and IoT rides the uplink. The published rates are downlink rates.

A fleet does not use every beam. The saturation curve, computed once on a
world population grid, counts the useful beams: the beams a fleet keeps lit
over places people live. Beams over oceans and empty land carry no one. Each
class's people at a fleet are the curve's capacity there, times the downlink
share and the panel factor, over the class's busy-hour load per person (50
kbps for the small terminal, 500 kbps for the mounted terminal).

As the fleet grows, satellites overlap over the same places, and each added
satellite adds fewer people. Each class's **saturation number** marks where
the curve flattens, where a 1 percent bigger fleet adds less than 0.1 percent
more capacity: 19,995 satellites for the small terminal. The mounted
terminal's curve has not flattened by 55,407 satellites, as far as the curve
measures. These are spectrum bounds, reported beside the launch cadence. They
are never caps on the build. Inside the horizon the launch cadence binds every
class: the fleet reaches 4,288 in FY2036.

What spectral efficiency means, in plain terms: the width sets how many times
per second the wave may change state (about 8 million per second on 8 MHz;
change it faster and the signal spreads outside the owned lane), and the
link's signal quality sets how many distinguishable amplitude-and-phase
states each change can carry, the way a clean wire can carry four voltage
levels where a noisy one carries only two. Throughput is the product of the
two. A better antenna does not widen the spectrum: it cleans the signal, so
each change carries more bits. That one fact is the device ladder in the next
section.

These are conditional model outputs, not measured performance from a finished
spacecraft. The reuse calibration is the number real engineering would move
first.

## Who Uses It: The Devices

The service is device-diverse by design, and it leads with hardware Rocket Lab
can build and ship without anyone's permission:

| | Small terminal | Mounted terminal |
|---|---|---|
| Who | A person who wants connectivity anywhere: a laptop in the field, a cabin, a boat | A vehicle, ship, aircraft, or fixed site |
| Antenna | A small flat antenna, or a USB device on a laptop; about 10 dBi, self-orienting | A mounted antenna; 15 dBi |
| Price | $10 a month | $50 a month |
| Speed while active | 2 Mbps; about 10 Mbps off-peak | 5 Mbps; about 13.4 Mbps off-peak |
| Users active at once | 2.5 percent at the busy hour; 0.5 percent off-peak | 10 percent at the busy hour; 2 percent off-peak |
| Data a month (the engineering case) | 5.4 GB, "about five gigabytes a month" | 54 GB |

These are what a user can expect most of the time; congestion can lower the
rates. The data a month counts 4 busy hours a day and a 30-day month: 180 MB a
day for the small terminal and 1,800 MB for the mounted terminal. The product
case raises it as the network grows, at the same prices: to 9 GB and 90 GB a
month by FY2036 (the investor's usage, 2026-10-12).

One design note travels with the small terminal: antenna gain is directional,
so it is specified with a self-orienting mount (a fixed tilt or a few switched
elements, no user pointing, no moving parts). A bare flat antenna lying face-up
earns these rates only with a satellite high overhead. The mount is what makes
the rates typical rather than best-case.

**Phones and voice.** The network can also carry phones and voice. A phone
needs a chip that speaks Iridium's band, and no standard phone chip does
today: Qualcomm and Iridium built one, and the partnership ended in 2023 with
no phone adoption (COMM-666, COMM-670). So the phone is its own, later model.
The investor: "This phone is its own model. We'll keep it out for now"
(2026-10-07). The engineering model still sizes a phone class at its $15
floor. Sold alone, the FY2036 fleet would serve 20,823,193 phones for $3,748.2M
a year, at a 58.5 percent own margin.

## IoT: The Network's Focus

The investor: "To be clear, the reason to keep IoT in there is that it is
primarily an IoT network. That is its thing, right?" (2026-10-06).

**IoT's room.** IoT devices send small messages up to the satellite. They ride
the uplink, the third of the frame the downlink leaves, on the beams the fleet
lights over places people live (the phone class's beams, since IoT antennas
are low gain). The room grows with the fleet:

| Year | Message payload a second | Access attempts a second | Message channels open at once |
|---|---|---|---|
| FY2031 | 6.6 Gbps | 1.1 million | 13.5 million |
| FY2033 | 15.6 Gbps | 2.6 million | 32.1 million |
| FY2035 | 30.2 Gbps | 5.0 million | 62.0 million |
| FY2036 | 38.5 Gbps | 6.4 million | 78.9 million |

The payload counts a 20 percent MAC efficiency (COMM-659). The access attempts
count 57 devices a random-access window, the cautious end of 57 to 1,650
(COMM-654), at an assumed one window a second. The channels are 3.75 kHz
narrowband tones (COMM-714). A minimal-packet message holds one for 4 to 7
seconds (COMM-719); the capacity below counts the cautious 7.

**What the room holds, each class alone: a capacity, not a forecast.** At its
engineering usage, each IoT class alone fits this many devices. Each class is
given the whole room, so the two never add:

| Year | Minimal-packet IoT alone (48 messages of 340 bytes a day) | Data IoT alone (4 bursts of 100 KB a day, beside the 48 messages) |
|---|---|---|
| FY2031 | 1,965,864,139 | 170,588,558 |
| FY2033 | 4,676,970,581 | 405,845,782 |
| FY2035 | 9,037,946,324 | 784,271,000 |
| FY2036 | 11,497,881,052 | 997,732,709 |

Access attempts bind minimal-packet IoT. Payload binds data IoT. Below the
340-satellite coverage floor the model publishes no capacity, since IoT needs
continuous coverage.

**What the market would buy: the product case.** The product case sells IoT at
its own, heavier usage (768 messages a day for minimal-packet IoT and 13 bursts
for data IoT by FY2036), so its devices are never divided by the capacity
above. It uses a part of the room:

| Year | IoT devices sold | IoT revenue a year | The uplink room used (busy hours; off-peak) |
|---|---|---|---|
| FY2031 | 24,191,736 minimal-packet; 12,095,868 data IoT | $1,741.8M | 14.5 percent; 14.5 percent |
| FY2033 | 72,183,871; 24,664,672 | $4,374.5M | 4.2 percent; 21.7 percent |
| FY2035 | 147,273,061; 42,675,455 | $8,374.5M | 9.9 percent; 28.8 percent |
| FY2036 | 184,890,668; 52,087,110 | $10,406.3M | 11.8 percent; 31.4 percent |

Data IoT sends its bursts outside the busy hours from FY2033, so the busy-hour
use drops that year.

**Upside the model leaves out.** IoT's room counts only the beams over places
people live. Beams over oceans and empty land, where ships, buoys, and remote
sensors sit, are not counted.

## The Fleet: Orbit And The Coverage Floor

The orbit is the model's own: about **450 kilometers at 53 degrees**
inclination, chosen because people live at mid-latitudes. The covered band
holds roughly 99.6 percent of the world's population, and the project's
coverage simulation needs about 10 percent fewer satellites there than a polar
fleet (341 versus 375 at the 95 percent threshold and a 25 degree mask). The
honest bounds on that simulation: a fuller phasing search finds 320 satellites
passing the same stored geographic metric, the saved 341 case is the robust
one under equal-area weighting, and the metric is geographic rather than
population-weighted. So 340 is a supported conservative scenario and the exact
floor is an engineering decision. The promoted artifact carries this orbit
posture as a labeled scenario block with those bounds attached.

340 satellites is the **coverage floor**. Nothing is sold in a year whose
fleet is below it. The ramp passes it in FY2031, with 528 satellites flying.

## How It Deploys

The deployment question is the same all-in question the data-center model
answers: what happens if you go pedal to the metal? Every Neutron launch on the
shared cadence ramp flies communications satellites, 16 to a launch. The ramp
flies 2, 3, 5, 9 and 14 launches from FY2027 to FY2031, then 22, 35, 51, 70 and
90 from FY2032 to FY2036. Each satellite lives five years, so the fleet flying
is the last five years' launches: 528 satellites in FY2031, 4,288 in FY2036.

- The fleet passes the 340-satellite coverage floor in FY2031, the first year
  anything is sold.
- Through FY2036 the ramp flies 301 launches. The first satellites retire in
  FY2032. In FY2036 the fleet replaces 224 satellites ($406.0M) and still
  grows.
- The data-center model flies the same 301 launches. Each application runs as
  if it had the ramp to itself, so their headlines never add.

The all-in share is a modeling scenario and is stated as one. In practice the
manifest is shared.

## What It Means For The Business

### What The Fleet Costs

The cost model is deliberately flat (an investor simplification, 2026-07-09):

| Cost line | Value | Basis |
|---|---|---|
| Satellite build | $1.0M each | Just below the prior 1.05 dial and the about-$1.2M Starlink V3 hardware anchor (COMM-080) |
| Launch, flat at any cadence | $13.0M | Just below the shared curve's grounded $13.5M high-cadence floor |
| A satellite in orbit | $1.8125M | $1.0M plus $13.0M over 16 |
| A satellite-year | $0.3625M | Over its five-year life |
| Spent through FY2031 | $957.0M | 33 launches, 528 satellites |
| Spent through FY2036 | $8,729.0M | 301 launches |
| The fleet's cost a year | $191.4M in FY2031 to $1,554.4M in FY2036 | The fleet flying times $0.3625M |

The margin is a full-cost margin: revenue less the fleet's annualized build,
launch, and replacement cost, over revenue. Operations cost is held at zero by
explicit assumption, a line to research and add later, stated in every model
output. For scale, Iridium spends about $376.3M a year of real operating cost
today (revenue $871.7M minus operational EBITDA $495.3M, COMM-615, COMM-616).
Charged that much in FY2036, the product case's margin would read 85.3 percent,
and the engineering view of the terminals (below) 29.8 percent.

### The Engineering Case: Every Seat Sold

The engineering case sells every seat each people class's fleet carries, at
the class's flat price. The table at the top shows each terminal alone.
Stated plainly (the investor's yes, 2026-10-12):

- Revenue rises every year in each class.
- The fleet's cost a seat rises, because each added satellite reaches fewer
  new people. A month, it rises from $3.85 to $5.26 for the small terminal and
  from $30.29 to $36.73 for the mounted terminal (FY2031 to FY2036).
- Each seat gets its class's set usage in every year. The service that
  improves with scale is the product case's.

So each own margin falls as the fleet grows: 61.5 to 47.4 percent for the
small terminal, 39.4 to 26.5 percent for the mounted terminal. The investor's
test is carried by the product case: "With more scale, more time, and more
satellites, your service should improve and your cost should come down. ... It
should also do so in a way where revenue increases" (2026-10-06).

**Where the next satellite stops paying.** Sold to one class alone at full
price, an added satellite earns more than it costs until the fleet reaches
6,006 satellites for the small terminal and 5,402 for the mounted terminal. Past those points it earns
less. The FY2036 fleet (4,288) is inside both. Each step compares two
separately computed fleets, so the people added need not fall at every step.

**The terminals as one business.** To read the two terminals together, split
the beams in today's mix: 75.7 percent to the small terminal and 24.3 percent
to the mounted terminal. That is Iridium's 402,000 voice-and-data and 16,100
broadband customers today, as busy-hour beams (COMM-617). Each class's seats
are its share of its people, rounded down:

| Year | Small terminal seats | Mounted terminal seats | Revenue a year | Margin |
|---|---|---|---|---|
| FY2031 | 3,134,834 | 127,770 | $452.8M | 57.7 percent |
| FY2033 | 7,529,140 | 312,835 | $1,091.2M | 54.8 percent |
| FY2035 | 14,692,841 | 649,446 | $2,152.8M | 48.3 percent |
| FY2036 | 18,636,082 | 855,857 | $2,749.8M | 43.5 percent |

This view falls under 50 percent from FY2035. It leaves out IoT, which only
the product case sells, and the phone. So it is not the whole business the
investor's 50 percent floor names. It is published, never tested against the
floor.

### The Product Case: What The Network Would Sell

The product case is its own model, built on the engineering artifact
(ADR 012). It never feeds the engineering model. It works in four steps:

1. **Demand.** Each class's customers start from Iridium today: 402,000
   voice-and-data customers at $47 a month, 16,100 broadband at $259, and
   1,998,000 IoT devices at $7.78 (COMM-617, COMM-618). A demand curve grows
   them with the network's scale (7.8 times today's terminal network in
   FY2031, 46.6 times in FY2036), with the price, and with the service.
2. **Markets.** No market research sets how strongly customers respond. So
   the case draws 2,000 markets, each response drawn over a stated range
   (COMM-723).
3. **The usable test.** A choice is usable in a market when, in every reported
   year, the whole business earns at least a 50 percent margin, at least three
   quarters of the terminals' busy-hour beams are filled, IoT fits its room,
   and revenue rises (COMM-725).
4. **The pick.** The prices are the investor's, held flat. The pick chooses
   only each IoT class's usage: the most median revenue among the usages
   usable in at least three quarters of the markets. It takes minimal-packet
   IoT at eight times its usage path and data IoT at its path. It is usable in
   1,744 of 2,000 markets (87.2 percent).

The headline is the central market: each response at the middle of its range,
the typical market. The four classes side by side (customers or devices;
revenue a year):

| Year | Small terminal ($10) | Mounted terminal ($50) | Minimal-packet IoT ($3) | Data IoT ($6) |
|---|---|---|---|---|
| FY2031 | 3,134,834; $376.2M | 127,770; $76.7M | 24,191,736; $870.9M | 12,095,868; $870.9M |
| FY2033 | 7,529,140; $903.5M | 312,835; $187.7M | 72,183,871; $2,598.6M | 24,664,672; $1,775.9M |
| FY2035 | 14,692,841; $1,763.1M | 649,446; $389.7M | 147,273,061; $5,301.8M | 42,675,455; $3,072.6M |
| FY2036 | 18,636,082; $2,236.3M | 855,857; $513.5M | 184,890,668; $6,656.1M | 52,087,110; $3,750.3M |

What each customer gets, and the price per unit, at the same monthly prices:

| Year | Small terminal | Mounted terminal | Minimal-packet IoT | Data IoT |
|---|---|---|---|---|
| FY2031 | 5.4 GB a month; $1.85 a GB | 54 GB; $0.93 a GB | 48 messages a day; 0.21 cents a message | 8 bursts a day; $0.25 a MB |
| FY2033 | 6.7 GB; $1.49 a GB | 67 GB; $0.75 a GB | 274 messages; 0.036 cents | 10 bursts; $0.20 a MB |
| FY2035 | 8.1 GB; $1.23 a GB | 81 GB; $0.62 a GB | 634 messages; 0.016 cents | 12 bursts; $0.16 a MB |
| FY2036 | 9 GB; $1.11 a GB | 90 GB; $0.56 a GB | 768 messages; 0.013 cents | 13 bursts; $0.15 a MB |

Data IoT also sends 48 messages a day in every year.

The year, with the believability test (more satellites: better service, lower
unit cost, rising revenue; the margin may fall):

| Year | Revenue a year (margin) | Profit a year | The fleet's cost per GB carried |
|---|---|---|---|
| FY2031 | $2,194.6M (91.3 percent) | $2,003.2M | $0.66 |
| FY2033 | $5,465.7M (91.0 percent) | $4,972.7M | $0.57 |
| FY2035 | $10,527.3M (89.4 percent) | $9,413.7M | $0.53 |
| FY2036 | $13,156.2M (88.2 percent) | $11,601.8M | $0.52 |

**How firm the headline is.** The headline is the typical market, and it sits
a little below the median of the markets where the case is usable. In FY2036
the usable markets' revenue runs from $8,055.3M at the 10th percentile through
$14,159.9M at the median to $26,338.7M at the 90th. The headline's $13,156.2M
sits at the 44.5th percentile. Over all 2,000 markets the median is $13,517.2M
($6,588.2M to $28,205.1M at the 10th and 90th), with the headline at the 48th.
In 73 of the 2,000, the pick sells IoT past its room in some year. Both
terminals sell every seat in the typical market in every reported year.
Across the usable markets in FY2036, the small terminal sells every seat in
91.3 percent of them and the mounted terminal in 89.4 percent.

**Where IoT starts.** Iridium reports one commercial IoT segment: 1,998,000
devices at $7.78 a month (COMM-617, COMM-618). Minimal-packet IoT takes it
whole as its start. Data IoT starts beside it at the investor's proportion,
half the count at double the price: 999,000 devices at $15.56 (COMM-726). So
the two IoT classes start from twice Iridium's IoT revenue today: $373.1M a
year against $186.5M. Iridium sells data services today too (Certus); data IoT
is a device class of its own beside them.

**What lower prices would do.** This is context, never the case. The model
also tries terminal prices falling by FY2036, the small terminal to as low as
$6 and the mounted terminal to $40. Lower prices make more markets usable and
earn less. At $6 and $40 (with minimal-packet IoT at twice its usage path),
1,934 of 2,000 markets are usable, but the median revenue summed over the four
reported years falls to $26,807.2M, from the pick's $33,656.8M. The pick sits
on that trade-off: no choice is both usable in more markets and earns more.

### The Two Cases Side By Side

The two cases agree on the terminals. In every reported year the product case
sells every terminal seat in the typical market: the same seats the
engineering view of the terminals sells. They differ on IoT. The engineering
model publishes IoT only as a capacity. Only the product case sells IoT.

| FY2036 | The engineering view of the terminals | The product case (the typical market) |
|---|---|---|
| Small terminal | 18,636,082 seats; $2,236.3M | The same |
| Mounted terminal | 855,857 seats; $513.5M | The same |
| IoT | A capacity: 11,497,881,052 minimal-packet or 997,732,709 data IoT devices, each class alone | 184,890,668 minimal-packet and 52,087,110 data IoT devices; $10,406.3M |
| Revenue a year | $2,749.8M | $13,156.2M |
| Margin | 43.5 percent | 88.2 percent |

The engineering case is a maximum for each people class. The product case is
the market's view. They are never added.

### The Prices: Held Flat

The prices are the investor's: the small terminal $10 a month and the mounted
terminal $50 (2026-10-07: "Yes, let's use the $10 and $50. Let's do that"),
minimal-packet IoT $3 and data IoT $6 (2026-10-06: "Let's go with the three
and six for now"). They are held flat in every year while the service
improves: "The prices will not go down, but they will not go up" (the
investor, 2026-10-06 19:38). Over time inflation makes a flat price cheaper in
real terms. Inflation is not modeled.

Each price sits below today's Iridium price for its kind of customer: $47 for
voice and data, $259 for broadband, and $7.78 for IoT (COMM-618). Why can
prices fall? Because today's prices ration scarce supply. Iridium's Certus
broadband peaks at 704 kbps down (COMM-620), and its broadband customers pay
$259 a month on average (COMM-618). The mounted terminal gets 5 Mbps while
active, for $50.

### The Margin Floor

The investor: "I think about a 50% floor for margin ... You wouldn't want to
go below that for sure" (2026-10-07). The floor is 50 percent on the whole
business. The product case carries it: its usable test requires it in every
year, and its headline reads 88.2 percent in FY2036. Each class alone stays at
or above break-even. In the engineering case each terminal's own margin stays
positive (26.5 to 61.5 percent). In the product case each IoT class's revenue
alone covers the fleet's whole cost (in FY2036, $6,656.1M and $3,750.3M against
$1,554.4M). The engineering model's own margins are published, never tested
against 50 percent.

### Government

Government is left out of revenue. For scale, Iridium's U.S. Space Force EMSS
contract is $738.5M over seven years (signed September 2019): about $107M a
year, stepping to $110.5M in its final year (COMM-619). It is named so a
reader can extrapolate. IoT and government are never added.

### The Structural Read

The spectrum position came with the about $8.0B acquisition (COMM-602). The
fleet that modernizes it costs $1,554.4M a year in FY2036, against the product
case's $13,156.2M. The modernized fleet's book replaces today's
$871.7M-a-year Iridium book (COMM-615) as the old fleet retires: the two are
never summed, and neither are people and devices.

## The Panel: Why 15.4 Square Meters

The model's satellite carries the Flatellite panel because that is the body
Rocket Lab drew for Neutron: at most 15.4 square meters, about 4.1 by 4.0
meters, in the fairing's 4.79 meter usable band (COMM-711). The area is enough
because frequency does the work of area at 1.6 GHz: a panel this size has the
gain and cell size of a much larger array at cellular frequencies, which is
why the design point is many small satellites rather than a few large ones.

The saturation curve is computed at a 25 m^2 reference panel. The model scales
it by the panel's area: 15.4 / 25 = 0.616 on people, useful beams, and
capacity (ADR 005). Below the reference panel every class carries at least
what this rule gives. Computed at 15.4 m^2 directly, the small terminal
carries up to about 1.8 percent more people and the mounted terminal exactly
what the rule gives. Each beam's rate is held at its reference-panel value:
the link effect of another panel is not modeled.

## The Upside Not Priced

- **IoT over oceans and empty land.** IoT's room counts only the beams over
  places people live.
- **The coordinated 10.5 MHz.** About 31 percent more people and class
  revenue, the fleet and its cost unmoved.
- **Phones and voice.** A later, separate model, once a phone chip speaks the
  band.
- **Government.** Left out of revenue; the EMSS contract is named above.

## The Runway

Inside the horizon the launch cadence, not the spectrum, binds every class.
The fleet reaches 4,288 satellites in FY2036. At 90 launches a year held, it
would settle at 7,200 beyond the horizon, still far below the small terminal's
saturation number (19,995). Sold to one terminal class alone at full price,
an added satellite stops paying from 5,402 (the mounted terminal) and 6,006
(the small terminal), so each terminal's runway at full price ends there. IoT's room keeps growing with
the fleet, and the product case uses less than a third of it in FY2036 (31.4
percent of the uplink off-peak).

## What Would Change The Verdict

- **The reuse calibration.** The 150 beams a reference panel carries is the
  widest physical error bar and needs real antenna, interference, and traffic
  engineering.
- **The saturation curve's simplifications.** Fluid beams with idealized
  footprints on one shell; everyone at the busy hour at once; no terrain
  blockage and no interference from other systems; every seat taken up. The
  terminals' -20 dB pattern floor is an estimate, optimistic for the small
  terminal.
- **The usage.** People scale inversely with each class's busy-hour load: its
  rate while active times its share of users active.
- **The downlink share.** People scale with it (0.67). IoT's room scales with
  the uplink's share.
- **The panel.** The linear rule, with the link effect of the smaller panel
  not modeled.
- **The orbit metric.** A population-weighted coverage target and an
  operational availability requirement could move the floor from 340.
- **IoT's access.** The random-access window rate (one a second, assumed; no
  source gives one) and a message's tone time (4 to 7 seconds, COMM-719) set
  how many devices the room holds.
- **The market.** The product case's three response ranges are modeling
  choices that no market research grounds (COMM-723).
- **Operations cost.** The explicit zero. A real operating line lowers every
  margin; Iridium's own $376.3M a year is the scale hint.
- **The manifest share.** All-in is a modeling scenario.

## Alternatives, One Line Each

- **A cut a reader applies.** A lower price divides the revenue and leaves the
  people; a smaller market divides both. Every margin is re-derived against
  the same fleet cost, never divided. The phone class keeps its $15.
- **Without the block upgrade.** 15 satellites a launch: the fleet is 15 / 16
  of the default, 4,020 satellites in FY2036.
- **Another panel.** People scale with the panel's area: 14.0 m^2, the panel
  with clearance (COMM-711), gives about 0.909 times. Below the reference panel
  every class carries at least what this gives.
- **The coordinated 10.5 MHz.** About 31 percent more people and class revenue
  (10.5 / 8 = 1.3125); the fleet and its cost unmoved.
- **IoT at $4 and $8, the investor's earlier prices.** The pick holds, and the
  typical market's revenue is the same ($13,156.2M at 88.2 percent in FY2036):
  the devices fall to three quarters (138,668,001 minimal-packet and 39,065,332
  data IoT in FY2036), and 1,807 of 2,000 markets are usable.

## Structural Context

This model exists because Rocket Lab agreed to acquire Iridium. If the deal
closes, Rocket Lab stops being a greenfield entrant and becomes an incumbent
MSS operator: owned, globally coordinated spectrum, an operating fleet,
ground infrastructure, and 2.5 million existing customers (see
[`research/rocket_lab/iridium_acquisition.md`](../research/rocket_lab/iridium_acquisition.md)).
The decision this model sizes is what a modern rebuild of that network could
deliver. The broader argument for why Rocket Lab, almost alone, owns the
parts, the rocket, and the production lines is the data center's
[structural case](../data_center/structural_case.md), written for the data
center. This document is the Iridium numbers.

This is a feasibility model, not Rocket Lab guidance, a demand forecast, a
completed spacecraft design, or investment advice. The strongest conclusion
is physical: narrow, reliable L-band can support a useful IoT and MSS product
at the modeled rates if the reuse, the curve's simplifications, the panel,
the downlink share, and IoT's access assumptions close in engineering. The
deployment schedule and the economics are scenario layers built on top of that
physical case, and their settings are stated where they bite.
