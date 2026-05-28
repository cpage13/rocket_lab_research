# Orbit Types Primer — Foundational Reference

*Foundational research. Status: draft. Date: 2026-05-17.*

## Summary

Earth orbits are usually grouped into four regimes by altitude: **LEO** (Low Earth
Orbit, ~160–2,000 km), **MEO** (Medium Earth Orbit, ~2,000–35,786 km), **GEO/GSO**
(Geostationary/Geosynchronous, the single special shell at ~35,786 km), and **HEO**
(High Earth Orbit, anything above GEO — or, in other usage, Highly Elliptical Orbit).
Lower orbits go around the Earth fast (LEO: ~90–120 min); higher orbits go slow
(GEO: exactly one day).

**The key point of confusion, cleared up first:** a **sun-synchronous orbit (SSO)
is not a "high" orbit. SSO is a type of LEO** — a near-polar, inclined low orbit,
typically **~500–800 km altitude** with a ~96–101-minute period. It is "special"
only in *inclination* and how its orbital plane drifts (precesses) to track the
Sun — not in altitude. Our project's dawn-dusk SSO compute nodes sit firmly inside
the LEO regime, far *below* MEO and GEO.

The altitude you choose drives almost everything else: how much payload a rocket
can deliver (higher = far less payload), communications latency (higher = slower),
how much of the Earth one satellite can see (higher = more), and how many
satellites you need for continuous coverage (lower = many more). **Neutron is
optimized for LEO/SSO**, which is exactly where our compute nodes belong. A
separate **relay layer** — GEO data-relay satellites, or a LEO relay mesh — can
solve the one real weakness of a LEO compute constellation: each node only sees a
given ground station for a few minutes per pass.

---

## 1. The Orbit Regimes

Orbits are classified by **altitude** (height above Earth's surface) and the
resulting **orbital period** (time for one lap). The physics is fixed by gravity:
the higher you orbit, the slower you must travel and the longer one lap takes.

### Low Earth Orbit (LEO) — ~160–2,000 km

The crowded, busy regime closest to Earth. Satellites here travel at roughly
**7.8 km/s** and complete an orbit in about **90–120 minutes**
([Wikipedia: Low Earth orbit](https://en.wikipedia.org/wiki/Low_Earth_orbit),
[ESA: Types of orbits](https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits)).
This is home to the International Space Station, Hubble, most Earth-observation
satellites, and broadband megaconstellations like Starlink. It is the cheapest
regime to reach and gives the lowest communications latency, but a single LEO
satellite sees only a small patch of Earth at a time and whips out of view of any
ground station within minutes.

> **Sun-synchronous orbit (SSO) lives here.** SSO is a *subtype of LEO* — a
> near-polar, inclined low orbit, typically **~500–800 km**, period **~96–101 min**.
> It is not higher than other orbits; see Section 1a below. The project's compute
> nodes use a **dawn-dusk SSO**, a LEO orbit.

### Medium Earth Orbit (MEO) — ~2,000–35,786 km

The middle ground, defined as everything above LEO and below GEO
([Wikipedia: Medium Earth orbit](https://en.wikipedia.org/wiki/Medium_Earth_orbit)).
Orbital periods run from about **2 hours at the bottom of the range up to nearly
24 hours near the top**; the navigation constellations (GPS, Galileo, GLONASS)
famously sit at roughly **~20,000 km with a ~12-hour period**
([Wikipedia: Medium Earth orbit](https://en.wikipedia.org/wiki/Medium_Earth_orbit),
[ESA: Types of orbits](https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits)).
MEO is used mainly for navigation and some communications — a compromise between
LEO's low latency and GEO's broad coverage.

### Geostationary / Geosynchronous Orbit (GEO / GSO) — ~35,786 km

A single, special shell. At an altitude of **35,786 km** above the equator
(42,164 km from Earth's center), a satellite's orbital period exactly matches
Earth's rotation — **one sidereal day, ~23 h 56 min**
([Wikipedia: Geostationary orbit](https://en.wikipedia.org/wiki/Geostationary_orbit),
[Wikipedia: Geosynchronous orbit](https://en.wikipedia.org/wiki/Geosynchronous_orbit)).
A **geosynchronous** orbit has that 24-hour period; a **geostationary** orbit is
the special geosynchronous case that is also circular and over the equator, so the
satellite appears to hang **motionless in the sky**. Orbital speed is about
**3.07 km/s** ([Wikipedia: Geostationary orbit](https://en.wikipedia.org/wiki/Geostationary_orbit)).
This is the classic home of weather satellites and traditional TV/communications
satellites — one satellite covers roughly a third of the planet (Section 3).

### High Earth Orbit (HEO) — above GEO

Two meanings of "HEO" appear in the literature; do not confuse them:

- **High Earth Orbit:** any geocentric orbit *above* the geosynchronous altitude,
  hence a period **longer than 24 hours**. The Moon is the best-known object in
  this regime ([ESA: Types of orbits](https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits)).
- **Highly Elliptical Orbit:** an orbit with a very stretched, egg-shaped path — a
  low perigee and a very high apogee. The satellite spends most of its time loitering
  near apogee, which makes these orbits useful for covering high latitudes that GEO
  serves poorly (the classic example is the Russian Molniya orbit). A
  **Geostationary Transfer Orbit (GTO)** is a highly elliptical orbit used as a
  *stepping stone* — low perigee in LEO, apogee at GEO altitude
  ([Wikipedia: Geostationary transfer orbit](https://en.wikipedia.org/wiki/Geostationary_transfer_orbit)).

For this project, HEO is mostly background; it is included for completeness.

### 1a. Why sun-synchronous orbit is *not* a higher orbit

This deserves its own callout because it is a common misconception.

A sun-synchronous orbit is a **LEO**. What makes it "sun-synchronous" has nothing
to do with being high — it is about **inclination** (the tilt of the orbit relative
to the equator) and a clever exploitation of orbital mechanics:

- An SSO is **near-polar**, inclined around **97–99°** (slightly more than straight
  over the poles).
- At that specific inclination, the bulge of the Earth's equator gently tugs the
  orbital plane so it slowly rotates — **precesses** — by about **0.986° per day**.
- That happens to be exactly the rate at which the Earth moves around the Sun
  (360° in ~365 days). So the orbit plane stays at a **fixed angle to the Sun** all
  year, and the satellite crosses any given latitude at the **same local solar
  time** every pass.

That sun-tracking property is *why it is useful* (consistent lighting for imaging;
or, in the **dawn-dusk** variant, near-continuous sunlight on the solar panels).
But the satellite is still a **low-orbit satellite at ~500–800 km** — well inside
LEO, roughly **45–70× lower than GEO**. SSO is a *flavor of LEO*, not a rung above
it. (See `orbits_environment.md` for the dawn-dusk SSO analysis specific to this
project.)

### Comparison table of the regimes

| Regime | Altitude range | Orbital period | Speed | One-way light delay (ground↔sat)* | Plain-English description |
|---|---|---|---|---|---|
| **LEO** | ~160–2,000 km | ~90–120 min | ~7.8 km/s | ~0.5–7 ms | Fast, low, close. Cheapest to reach, lowest latency, smallest footprint. Home of ISS, Starlink, Earth-observation sats — **and SSO**. |
| → *SSO (subtype of LEO)* | ~500–800 km | ~96–101 min | ~7.5 km/s | ~2–7 ms | A near-polar, inclined LEO (~97–99°) whose plane tracks the Sun. **Not higher — just a special LEO.** |
| **MEO** | ~2,000–35,786 km | ~2–~24 h (GPS ~12 h) | ~3–7 km/s | ~7–120 ms | The middle. Navigation constellations (GPS/Galileo) sit here at ~20,000 km. |
| **GEO / GSO** | ~35,786 km (single shell) | ~24 h (1 sidereal day) | ~3.07 km/s | ~120 ms | Appears fixed in the sky. One satellite covers ~⅓ of Earth. Weather & traditional comsats. |
| **HEO** | above ~35,786 km | > 24 h | < 3 km/s | > 120 ms | High Earth Orbit (above GEO; the Moon). Note "HEO" also means *Highly Elliptical Orbit* — a stretched orbit, e.g. Molniya, GTO. |

\* One-way *light-travel* delay only — the physics floor. Real round-trip latency
adds the return leg plus processing and ground network; see Section 3.

---

## 2. Deploying to Each Orbit — Launch Cost and Delta-v

"How hard is it to get there" is measured in **delta-v** (Δv) — the total change in
velocity a rocket must supply. More delta-v means exponentially more propellant
(the rocket equation), which means **less payload** for a given vehicle.

### Reaching LEO / SSO

Getting anything to orbit at all is the expensive first step. A launch vehicle
needs roughly **9.0–9.4 km/s of delta-v** to reach LEO, once losses to gravity and
air drag are included ([Wikipedia: Delta-v budget](https://en.wikipedia.org/wiki/Delta-v_budget)).
That single number dominates the whole launch: most of the rocket's energy is spent
just getting *into* LEO.

**SSO costs a bit more than equatorial LEO** — not because it is higher, but
because it is highly inclined (~98°). Launching into a near-polar plane forfeits
most of the "free" eastward boost from Earth's rotation (~0.4 km/s at the equator)
and can require a small steering maneuver. The practical result, consistent across
Falcon-9- and Electron-class vehicles, is that **SSO payload is ~20–35% below the
same rocket's low-inclination LEO payload** (see `orbits_environment.md` for the
detailed Neutron estimate).

### Reaching MEO and GEO

Climbing above LEO costs **a lot more delta-v on top of the ~9.4 km/s already spent**:

- **LEO → GTO** (the elliptical transfer orbit toward GEO): roughly **+2.3–2.5 km/s**
  ([Wikipedia: Geostationary transfer orbit](https://en.wikipedia.org/wiki/Geostationary_transfer_orbit)).
- **GTO → GEO** (circularizing at the top): roughly **+1.5–1.85 km/s**
  ([Wikipedia: Geostationary transfer orbit](https://en.wikipedia.org/wiki/Geostationary_transfer_orbit),
  [Wikipedia: Delta-v budget](https://en.wikipedia.org/wiki/Delta-v_budget)).
- MEO falls in between, depending on the target altitude.

### Why higher orbits cost so much payload

Because of the rocket equation, every extra km/s of delta-v multiplies the
propellant fraction — so payload mass falls steeply as the destination rises. A
concrete, well-documented example: the **Delta IV Heavy could lift ~14,200 kg to
GTO but only ~6,750 kg directly to GEO** — under half the payload for the same
rocket, just to finish the climb
([ULA: Delta IV](https://www.ulalaunch.com/rockets/delta-iv)). Direct GEO insertion
is so costly that satellites are usually dropped off in GTO and then **use their
own propulsion** to circularize — which is why GEO comsats carry years of fuel and
take weeks (chemical) or months (electric) to reach their final slot.

**Rule of thumb for our purposes:** for a medium-lift rocket, **GEO-class payload
is roughly one-third to one-half of its LEO payload**. MEO sits in between.

### Neutron is optimized for LEO/SSO

Rocket Lab designed Neutron explicitly for the **LEO megaconstellation market**,
forecasting it will be able to launch "98% of all payloads launched through 2029"
([Wikipedia: Rocket Lab Neutron](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron),
[Rocket Lab: Neutron unveiling](https://www.rocketlabusa.com/about-us/updates/rocket-lab-unveils-plans-for-new-8-ton-class-reusable-rocket-for-mega-constellation-deployment/) — the 2021 unveiling of the *original 8-ton-class design*; the current matured design is heavier, so this URL is the historical-design reference, not a source for today's payload figures).
Its published numbers are LEO numbers: **~13,000 kg to LEO** (reusable, downrange
landing), **~15,000 kg expendable**, and **~8,500 kg return-to-launch-site**
([Wikipedia: Rocket Lab Neutron](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron),
[NewSpace Economy: Neutron status](https://newspaceeconomy.ca/2025/07/10/neutron-rocket-development-status-and-future-plans-july-2025/)).
Neutron is **not** a GEO-direct or beyond-LEO vehicle; reaching GEO with it would
mean a much smaller payload plus a separate transfer stage or satellite propulsion.
**This is convenient for the project: our compute nodes belong in LEO/SSO anyway,
exactly Neutron's sweet spot.**

---

## 3. Communications at Each Level

Where a satellite sits trades off four linked properties: **latency**, **how long
it is visible** from a ground station, **coverage footprint**, and **revisit**.

### Latency — distance is the floor

Radio and laser signals travel at the speed of light (~300,000 km/s), so latency
is set primarily by distance:

- **LEO (~500 km):** one-way light delay is only a few milliseconds. Real-world
  round-trip latency for Starlink is about **25–50 ms**, comparable to terrestrial
  cable broadband ([Light Reading: Starlink vs GEO](https://www.lightreading.com/satellite/starlink-smokes-geo-satellite-operators-in-speed-latency-report),
  [IEEE ComSoc: GEO can't compete with LEO](https://techblog.comsoc.org/2025/07/18/geo-satellite-internet-from-hughesnet-and-viasat-cant-compete-with-leo-starlink-in-speed-or-latency/)).
- **GEO (~35,786 km):** the signal alone takes **~120 ms one way**. With the return
  trip plus processing, real round-trip latency is **~600–700 ms** — measured median
  latency for the Viasat GEO service was **~684 ms**
  ([Light Reading: Starlink vs GEO](https://www.lightreading.com/satellite/starlink-smokes-geo-satellite-operators-in-speed-latency-report),
  [IEEE ComSoc](https://techblog.comsoc.org/2025/07/18/geo-satellite-internet-from-hughesnet-and-viasat-cant-compete-with-leo-starlink-in-speed-or-latency/)).
- **MEO:** in between — tens to ~150 ms one way.

This single fact — **~120 ms vs. a few ms** — is the headline difference between GEO
and LEO connectivity.

### Visibility per pass — how long can you talk to it

- A **LEO** satellite races across the sky. From a single ground station, a good
  pass lasts only about **5–15 minutes**, and a station gets roughly **4–8 usable
  passes per day** with any given satellite
  ([Satellite Ground Station: Orbit types & ground station impacts](https://satellitegroundstation.com/resources/orbit-types-leo-meo-geo-heo-and-ground-station-impacts/)).
  The rest of the time that satellite is below the horizon and **out of contact**.
- A **GEO** satellite never moves relative to the ground — it is in view of its
  service area **100% of the time**, which is why GEO dishes can be bolted down and
  aimed once.

### Coverage footprint and revisit

- A **single GEO satellite** has line of sight to roughly **one-third of Earth's
  surface**. **Three GEO satellites**, spaced 120° apart in longitude, cover
  essentially the whole planet except the poles
  ([TechTarget: Geostationary satellite](https://www.techtarget.com/searchmobilecomputing/definition/geostationary-satellite),
  [The Planetary Society: GEO coverage](https://www.planetary.org/space-images/coverage-of-a-geostationary)).
- A **single LEO satellite** sees only a small footprint and is overhead any given
  location only briefly, so a LEO system needs **many satellites** to give any one
  spot continuous coverage (revisit). Iridium needs **66 satellites** for global
  coverage; Starlink operates **thousands**
  ([Wikipedia: Iridium satellite constellation](https://en.wikipedia.org/wiki/Iridium_satellite_constellation),
  [Wikipedia: Starlink](https://en.wikipedia.org/wiki/Starlink)).

### Why Starlink is LEO and traditional comsats are GEO

This is the trade in a nutshell:

- **Starlink chose LEO** for **low latency** (~40 ms, broadband-like) and strong
  link budgets at short range. The price is needing **thousands of satellites** —
  because each one covers little ground and is visible only briefly — plus
  inter-satellite links to route traffic between them.
- **Traditional comsats chose GEO** because **one satellite covers a third of the
  Earth and never moves**, so the ground network is dead simple and three
  satellites blanket the globe. The price is **~600+ ms latency** — fine for
  broadcast TV, painful for interactive use.

A LEO compute constellation inherits LEO's weakness: **each node only sees a given
ground station for minutes at a time.** That is the problem a relay layer solves.

---

## 4. Relay Satellites — a Data-Relay Layer

### The concept

A **data-relay satellite** does not look at the Earth or do science — it relays
*other satellites' data*. The classic architecture puts relay satellites in **GEO**,
where they have a constant, wide view of both the LEO satellites below them and a
fixed ground station. A LEO satellite that would otherwise have to wait for a brief
ground-station pass instead beams its data **up** to a GEO relay, which immediately
forwards it **down** to the ground — a "bent-pipe" path that is continuously open.

### NASA TDRS

NASA's **Tracking and Data Relay Satellite (TDRS)** system is the canonical example.
A handful of TDRS spacecraft in GEO relay telemetry and data for the ISS, Hubble,
and many Earth-observation missions. The payoff is dramatic: TDRS gives LEO missions
**~85–100% contact time, versus only ~5–15% from direct ground-station passes**
([NASA: Tracking and Data Relay Satellites](https://www.nasa.gov/mission/tracking-and-data-relay-satellites/),
[Wikipedia: TDRSS](https://en.wikipedia.org/wiki/Tracking_and_Data_Relay_Satellite_System)).
A LEO satellite that could otherwise talk to the ground for a few minutes per
90-minute orbit becomes **almost always connected**. (NASA stopped assigning new
missions to TDRS in late 2024 and is transitioning to commercial relay services,
but the architecture remains the model.)

### ESA EDRS — the "SpaceDataHighway"

ESA and Airbus operate the **European Data Relay System (EDRS)**, branded the
**SpaceDataHighway** — a modern, **laser-based** version of the same idea. EDRS
payloads in **GEO** receive data from LEO Earth-observation satellites over an
**optical (laser) link** and forward it to Europe in near-real time, at up to
**~1.8 Gbit/s** ([ESA: EDRS overview](https://www.esa.int/Applications/Connectivity_and_Secure_Communications/EDRS/Overview),
[Wikipedia: European Data Relay System](https://en.wikipedia.org/wiki/European_Data_Relay_System)).
ESA states the core motivation plainly: without EDRS, a satellite "can only dump
its information when in direct line-of-sight of a ground station... on average only
every 90 minutes"; with EDRS it relays continuously through a GEO satellite that
always sees the ground
([ESA: EDRS overview](https://www.esa.int/Applications/Connectivity_and_Secure_Communications/EDRS/Overview)).

### How a relay layer could help an SSO compute constellation

Our compute nodes will sit in dawn-dusk SSO — a LEO orbit — and therefore inherit
the LEO connectivity problem: any single optical ground station only sees a given
node for a few minutes per ~96-minute orbit. Two relay architectures could give the
constellation **continuous connectivity**:

1. **A GEO relay layer (TDRS/EDRS-style):** one or a few GEO relay satellites,
   each in constant view of both the SSO compute nodes and a fixed ground hub. The
   SSO node lasers its traffic up to GEO; the relay forwards it down continuously.
   Cost: the GEO relay adds the ~120 ms (~600+ ms round-trip) latency penalty, and
   reaching GEO is expensive (Section 2).
2. **A LEO relay mesh:** a layer of LEO relay satellites (or inter-satellite links
   between the compute nodes themselves) that hands traffic node-to-node until it
   reaches one that currently has a ground station in view — the Starlink approach.
   Keeps latency low (a few–tens of ms) but needs many satellites and a routed
   mesh.

This is a genuine design fork for the project — explored in Section 6 and in the
laser-comms research (`laser_comms/`).

---

## 5. Constellation Basics

A single satellite is rarely enough; useful systems are **constellations** —
multiple satellites flown as a coordinated group.

### Orbital planes

A constellation's satellites are distributed across several **orbital planes** —
distinct orbital "tracks" at the same altitude but rotated around the Earth. Within
each plane, satellites are spaced evenly like beads on a ring. Iridium, for example,
flies **66 satellites in 6 planes (11 per plane), spaced 30° apart**, at ~780 km
and 86.4° inclination ([Wikipedia: Iridium satellite constellation](https://en.wikipedia.org/wiki/Iridium_satellite_constellation)).
Starlink's first shell used **72 planes of 20 satellites each**
([Wikipedia: Starlink](https://en.wikipedia.org/wiki/Starlink)). More planes and
more satellites per plane = denser, more continuous coverage.

### Why you need many satellites

Because a LEO satellite covers only a small footprint and moves fast, **no single
LEO satellite can continuously cover anything**. Continuous global coverage requires
enough satellites that, as one moves out of view, another is already moving in.
This is why LEO systems need tens (Iridium: 66) to thousands (Starlink) of
satellites, while GEO needs only **three** for near-global coverage. Coverage is the
fundamental reason LEO constellations are *large*.

### Station-keeping

Orbits are not "set and forget." Satellites drift due to atmospheric drag (in LEO),
the Earth's uneven gravity, and solar/lunar pull. **Station-keeping** is the use of
onboard propulsion to correct that drift and hold the assigned slot or plane. In
LEO, drag is the dominant nuisance — and it is **worse for satellites with large
area-to-mass ratios**, e.g. big solar arrays and radiators (directly relevant to a
compute node — see `orbits_environment.md`). GEO satellites spend fuel mainly on
north-south station-keeping. Either way, the satellite needs propulsion and a
multi-year propellant budget.

### Deorbit / end-of-life by regime

What happens at end of mission depends heavily on the regime:

- **LEO:** the new standard is the **FCC "5-year rule"** — satellites in LEO must
  be disposed of **within 5 years** of mission completion (down from the old
  25-year guideline). It took effect **29 September 2024** and applies to all
  newly FCC-licensed satellites launched after that date
  ([FCC: 5-year rule](https://www.fcc.gov/document/fcc-adopts-new-5-year-rule-deorbiting-satellites-0),
  [SpaceNews: FCC five-year deadline](https://spacenews.com/fcc-to-set-five-year-deadline-for-deorbiting-leo-satellites/)).
  Below ~500–600 km, atmospheric drag will naturally pull a satellite down within
  a few years; **above that, natural decay takes much longer than 5 years, so the
  satellite needs active deorbit propulsion** to lower its orbit and reenter
  ([NASA: Deorbit Systems](https://www.nasa.gov/smallsat-institute/sst-soa/deorbit-systems/)).
- **GEO:** satellites do **not** deorbit — reentry from GEO is energetically
  prohibitive. Instead they are boosted ~300 km **above** GEO into a **"graveyard
  orbit"** at end of life, clearing the valuable GEO belt
  ([SpaceNexus: 5-year rule](https://spacenexus.us/blog/space-debris-five-year-rule-what-operators-need-know)).

For our SSO compute constellation, the 5-year rule is a real design constraint:
each node must be designed for **controlled disposal**, and the constellation plan
must budget a **replacement cadence** as nodes age out.

---

## 6. Implications for Our Project

A short read-through of what the above means for an orbital AI-inference data
center launched on Neutron.

**1. Compute nodes belong in dawn-dusk SSO — a LEO orbit.** This is the project's
baseline and it is well-founded. SSO is *not* a higher, harder-to-reach orbit; it
is a LEO at ~500–800 km, squarely inside Neutron's optimized performance band. The
dawn-dusk variant gives near-continuous sunlight for the solar arrays (the power
rationale is in `orbits_environment.md`). Nothing in this primer challenges that
choice — it reinforces it.

**2. Neutron's optimization aligns with the orbit choice.** Neutron is a LEO/SSO
megaconstellation launcher. Putting compute nodes in MEO or GEO would slash payload
per launch (GEO ≈ one-third to one-half of LEO payload) and demand a transfer stage —
a poor fit. The orbit choice and the launch vehicle choice are mutually consistent.

**3. The real connectivity weakness is pass duration, and a relay layer can fix
it.** A LEO/SSO node only sees a given ground station for ~5–15 minutes per
~96-minute orbit. Options:

  - **GEO relay layer** (TDRS/EDRS-style): a small number of GEO relay satellites
    would give the compute constellation **near-continuous** connectivity to a
    fixed ground hub — the proven architecture (TDRS lifts contact time from
    ~5–15% to ~85–100%). **Tradeoffs:** adds ~120 ms one-way (~600+ ms round-trip)
    latency on the relayed leg; building/launching to GEO is expensive; but a relay
    is a *one-time infrastructure* cost, and inference traffic is relatively
    latency-tolerant compared to interactive web use.
  - **LEO relay mesh / inter-satellite links** (Starlink-style): keep latency low
    (a few–tens of ms) by routing traffic node-to-node until a node with ground
    contact is reached. **Tradeoffs:** needs more satellites and a routed optical
    mesh; more complex; but latency stays low and it avoids the cost of reaching
    GEO.
  - **More diverse ground stations** (the non-relay option): enough geographically
    spread optical ground hubs that *some* hub is always in view of *some* node.
    Covered in `laser_comms/optical_ground_stations.md`.

**4. End-of-life is a constraint, not a blocker.** Under the FCC 5-year rule, each
SSO compute node must be disposable within 5 years of retirement. At the lower SSO
band (~500–600 km) natural decay can do much of the work; higher up, the node needs
deorbit propulsion. This argues mildly for the lower SSO band and feeds the
constellation's replacement-cadence and economics planning.

**Bottom line:** the orbit menu does not change the project's direction. Dawn-dusk
SSO (a LEO) remains the right home for the compute nodes and matches Neutron's
design. The one open architectural question the orbit landscape raises is **how to
keep an SSO constellation continuously connected** — GEO relay vs. LEO mesh vs.
diverse ground stations — which is a real trade to carry into the comms and
synthesis work.

---

## Sources

- [Wikipedia — Low Earth orbit](https://en.wikipedia.org/wiki/Low_Earth_orbit)
- [Wikipedia — Medium Earth orbit](https://en.wikipedia.org/wiki/Medium_Earth_orbit)
- [Wikipedia — Geostationary orbit](https://en.wikipedia.org/wiki/Geostationary_orbit)
- [Wikipedia — Geosynchronous orbit](https://en.wikipedia.org/wiki/Geosynchronous_orbit)
- [Wikipedia — Geostationary transfer orbit](https://en.wikipedia.org/wiki/Geostationary_transfer_orbit)
- [Wikipedia — Delta-v budget](https://en.wikipedia.org/wiki/Delta-v_budget)
- [Wikipedia — Sun-synchronous orbit](https://en.wikipedia.org/wiki/Sun-synchronous_orbit)
- [Wikipedia — Tracking and Data Relay Satellite System](https://en.wikipedia.org/wiki/Tracking_and_Data_Relay_Satellite_System)
- [Wikipedia — European Data Relay System](https://en.wikipedia.org/wiki/European_Data_Relay_System)
- [Wikipedia — Iridium satellite constellation](https://en.wikipedia.org/wiki/Iridium_satellite_constellation)
- [Wikipedia — Starlink](https://en.wikipedia.org/wiki/Starlink)
- [Wikipedia — Rocket Lab Neutron](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron)
- [ESA — Types of orbits](https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits)
- [ESA — EDRS Overview (SpaceDataHighway)](https://www.esa.int/Applications/Connectivity_and_Secure_Communications/EDRS/Overview)
- [NASA — Tracking and Data Relay Satellites](https://www.nasa.gov/mission/tracking-and-data-relay-satellites/)
- [NASA — Small Spacecraft SOA: Deorbit Systems](https://www.nasa.gov/smallsat-institute/sst-soa/deorbit-systems/)
- [FCC — Adopts New "5-Year Rule" for Deorbiting Satellites](https://www.fcc.gov/document/fcc-adopts-new-5-year-rule-deorbiting-satellites-0)
- [SpaceNews — FCC to set five-year deadline for deorbiting LEO satellites](https://spacenews.com/fcc-to-set-five-year-deadline-for-deorbiting-leo-satellites/)
- [SpaceNexus — The FCC 5-Year Deorbit Rule](https://spacenexus.us/blog/space-debris-five-year-rule-what-operators-need-know)
- [ULA — Delta IV](https://www.ulalaunch.com/rockets/delta-iv)
- [Rocket Lab — Neutron unveiling (8-ton-class reusable rocket)](https://www.rocketlabusa.com/about-us/updates/rocket-lab-unveils-plans-for-new-8-ton-class-reusable-rocket-for-mega-constellation-deployment/)
- [NewSpace Economy — Neutron Rocket development status (July 2025)](https://newspaceeconomy.ca/2025/07/10/neutron-rocket-development-status-and-future-plans-july-2025/)
- [Light Reading — Starlink smokes GEO operators in speed, latency](https://www.lightreading.com/satellite/starlink-smokes-geo-satellite-operators-in-speed-latency-report)
- [IEEE ComSoc — GEO satellite internet can't compete with LEO Starlink](https://techblog.comsoc.org/2025/07/18/geo-satellite-internet-from-hughesnet-and-viasat-cant-compete-with-leo-starlink-in-speed-or-latency/)
- [Satellite Ground Station — Orbit Types LEO/MEO/GEO/HEO and Ground Station Impacts](https://satellitegroundstation.com/resources/orbit-types-leo-meo-geo-heo-and-ground-station-impacts/)
- [TechTarget — Geostationary satellite](https://www.techtarget.com/searchmobilecomputing/definition/geostationary-satellite)
- [The Planetary Society — Coverage of a geostationary satellite](https://www.planetary.org/space-images/coverage-of-a-geostationary)

## Open Questions / Uncertainties

- **Relay architecture decision.** GEO relay vs. LEO relay mesh vs. diverse ground
  stations is unresolved — it is a real trade with cost, latency, and complexity
  implications. Needs a dedicated comparison (link to `laser_comms/` work).
- **MEO never seriously evaluated.** This primer treats MEO as background. If a
  relay or specialty layer at MEO were ever considered, its delta-v, latency, and
  radiation profile (MEO crosses the proton belts) would need their own analysis.
- **Exact LEO→SSO and LEO→GEO delta-v figures vary by source** depending on the
  reference LEO altitude and the launcher's GTO design. The ranges here (LEO→GTO
  ~2.3–2.5 km/s, GTO→GEO ~1.5–1.85 km/s) are representative, not exact for any
  specific Neutron trajectory.
- **Neutron has no published SSO or beyond-LEO performance number.** All
  non-LEO payload statements here are qualitative; see `orbits_environment.md` for
  the SSO payload *estimate* and its caveats.
- **Latency tolerance of inference traffic** through a GEO relay (~600+ ms
  round-trip) is assumed acceptable but not quantified — should be checked against
  the customer/usage model.
