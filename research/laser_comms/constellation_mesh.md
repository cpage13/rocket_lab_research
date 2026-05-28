# Constellation Geometry & Laser-Mesh Network Design

*Research date: May 2026. Part of the Rocket Lab orbital AI-inference data center feasibility study.*
*Builds on `laser_comms/optical_comms.md`, `llm_compute/multi_rack_inference.md`,
`synthesis/wave5_synthesis.md`. Companion to `laser_comms/optical_ground_stations.md`.*

## Summary

Laser inter-satellite links (ISLs) are a **solved problem at the ranges we need**. Starlink's
operational laser mesh routinely holds links across **hundreds to a few thousand km**, with a rated
**maximum of ~5,400 km** per link; Mynaric's CONDOR is rated to ~6,500 km. Range is therefore *not*
the binding constraint — the binding constraint for a compute cluster is **latency**, which is pure
speed-of-light geometry: ~3.3 µs per km of separation, one way. A tight compute cluster wants its
cooperating racks **as close as collision-safety allows**, because pipeline-parallel traffic crosses
ISLs every micro-batch and latency is additive over many hops.

The realistic floor on spacing is **collision-avoidance and station-keeping, not optics**: a
passively-safe tight formation sits at roughly **1–10 km** rack-to-rack. At 1–10 km the link adds
only **~3–33 µs** one way — negligible against the ~hundreds of µs of a transformer layer — so a
compute cluster of 4–8 racks is essentially "free" from a latency standpoint. The problem only
appears when racks are flung across orbital planes (hundreds–thousands of km), where per-hop latency
reaches **0.5–5 ms** and starts to rival compute time.

**Strawman for a first useful service: 8 compute satellites** in a single tight along-track string
(~5 km spacing, passively safe, ~17 µs/link), each carrying **3–4 ISL terminals** (2 for the
in-string daisy chain, 1–2 spare/cross-link for resilience), plus **3–4 optical ground hubs**
spaced >1,000 km apart for weather diversity. This is one orbital "node" of compute; a globally
*reachable* service (a hub always in view) is a separate, larger problem needing **dozens** of
relay satellites — but the v1 service does not need that and should not pay for it.

**Confidence: medium-high.** Laser ISL ranges, Starlink topology, and speed-of-light latency are
all well-sourced and physical. The minimum-safe-spacing number (1–10 km) is an *informed estimate*
extrapolated from CubeSat formation-flying practice and is the softest number here.

---

## 1. Laser ISL range — how far can the links actually reach?

### Starlink — the proven reference

Starlink's laser mesh is the largest operational ISL network ever built: **~9,000+ satellites
with ~3 laser terminals each — on the order of ~27,000 space lasers** across the constellation,
moving **42+ PB/day** at ~5.6 Tbps aggregate, with **100 Gbps** per
terminal ([Hackaday](https://hackaday.com/2024/02/05/starlinks-inter-satellite-laser-links-are-setting-new-record-with-42-million-gb-per-day/),
[Advanced Television](https://www.advanced-television.com/2024/02/02/spacex-reveals-starlink-laser-capacity/)).

Range figures (multiple independent sources agree):

| Link type | Typical range | Source |
|---|---|---|
| Intra-plane (same orbital plane, fore/aft neighbor) | ~hundreds of km | [arXiv 2103.00056](https://arxiv.org/pdf/2103.00056) |
| Inter-plane (adjacent plane) | ~1,000–1,700 km | [arXiv 2103.00056](https://arxiv.org/pdf/2103.00056), [Connectivity.tech](https://www.connectivity.technology/2022/02/laser-inter-satellite-links-lisls-in.html) |
| Cross-seam / crossing-plane (transient) | up to ~1,700 km | [arXiv 2103.00056](https://arxiv.org/pdf/2103.00056) |
| **Rated maximum per link** | **~5,400 km** | [Hackaday](https://hackaday.com/2024/02/05/starlinks-inter-satellite-laser-links-are-setting-new-record-with-42-million-gb-per-day/), [Advanced Television](https://www.advanced-television.com/2024/02/02/spacex-reveals-starlink-laser-capacity/) |
| SpaceX "mini" laser | 25 Gbps at up to ~4,000 km | [Advanced Television](https://www.advanced-television.com/2024/02/02/spacex-reveals-starlink-laser-capacity/) |

The research literature studies LISL "range budgets" of 1,000–5,000 km and finds that **longer rated
range lets a satellite form more simultaneous links** (more candidate neighbors in reach): at
~1,500 km a satellite reaches its same-plane neighbors plus nearest adjacent-plane neighbors; at
~1,700 km it can hold up to ten links including transient crossing-plane links
([arXiv 2103.00056](https://arxiv.org/pdf/2103.00056),
[MDPI Electronics](https://www.mdpi.com/2079-9292/11/14/2232)). The geometric ceiling is the
horizon: two LEO satellites lose line-of-sight (Earth blocks the beam) once separation exceeds a few
thousand km, which is why the practical maximum sits at ~5,400 km even though the optics could
theoretically reach further.

### Mynaric CONDOR — Rocket Lab's in-house terminal

CONDOR Mk3 is rated to **up to ~6,500 km** link range; earlier CONDOR generations were specified for
intra/inter-plane link distances up to ~7,800 km in densely-packed constellations
([MSA Components](https://msa-components.com/entering-the-next-era-of-laser-communication-with-the-condor-mk3/),
[satsearch](https://satsearch.co/products/mynaric-condor-mk3)). *(The ~7,800 km is an
optics/spec-sheet free-space figure; in practice ISL range is **horizon-limited** to
~5,000–6,500 km — see below — so 7,800 km is never the binding number.)* Data rate:
the Mk3 ships **configured at ~2.5 Gbps as-delivered** (SDA Tranche 1); **100 Gbps is
the next-generation CONDOR Mk3.1 roadmap target, not a Mk3 ceiling** — see
`optical_comms.md` and `rocket_lab/space_hardware_capabilities.md` for the harmonized
project figures.

**Practical maximum (confirmed):** an ISL can reach **~5,000–6,500 km** before Earth's horizon
intervenes — i.e. essentially any two satellites that can see each other. **Range is not a
constraint for this project.** Our cooperating racks will sit far closer than the limit; the
relevant question is *how close*, and *what longer links cost*.

---

## 2. The distance ↔ performance tradeoff

Three things get worse as ISL separation grows: **latency**, **pointing/aperture difficulty**, and
(at the extremes) **achievable data rate**.

### 2a. Latency — pure speed-of-light geometry

Light in vacuum travels at ~299,792 km/s, so propagation latency is fixed and unavoidable:

> **~3.336 µs per km, one way** (~6.67 µs/km round trip).

(Vacuum is ~47% faster than fiber — see `optical_comms.md` — so the space link is *better* than a
terrestrial equivalent of the same length, but the geometry is what it is.)

| ISL separation | One-way latency | Round-trip | Regime |
|---|---|---|---|
| 1 km | 3.3 µs | 6.7 µs | tight formation |
| 5 km | 16.7 µs | 33 µs | tight formation (strawman) |
| 10 km | 33 µs | 67 µs | tight formation |
| 100 km | 334 µs | 667 µs | loose cluster (prior "sub-ms is fine" point) |
| 1,000 km | 3.3 ms | 6.7 ms | inter-plane relay |
| 5,400 km | 18 ms | 36 ms | max-range relay hop |

This is an *estimate-free* calculation — it is just physics.

### 2b. Where an ISL bottlenecks pipeline-parallel traffic

Tensor parallelism must stay in-rack (`multi_rack_inference.md`); the traffic that crosses ISLs is
**pipeline/expert-parallel** — activations handed rack-to-rack at each pipeline stage boundary. The
relevant comparison is link latency vs. the compute time of a pipeline stage.

A transformer decode step on a single NVL72-class rack runs on the order of **hundreds of µs to a
few ms** per pipeline stage. Therefore:

- **At ≤10 km separation (≤33 µs/link):** ISL latency is **~1–5% of stage time** — negligible. A
  multi-rack model pipelined across a tight cluster behaves almost like a single machine.
- **At ~100 km (~334 µs/link):** latency is now *comparable* to a fast stage time. Tolerable for
  a 2–4-rack pipeline, but it begins to eat the latency budget — consistent with the prior
  project note that "sub-ms at 100 km is fine."
- **At ~1,000 km (~3.3 ms/link):** latency **exceeds** typical stage time. Pipelining across links
  this long is a real bottleneck: every micro-batch boundary stalls. This is the regime to avoid
  for cooperating racks.

**Rule of thumb: keep cooperating racks within ~100 km, and ideally within ~10 km.** Beyond a few
hundred km, an ISL stops being a "backplane extension" and becomes a "WAN link."

Bandwidth is a *secondary* concern: CONDOR/Starlink-class terminals deliver 100–200 Gbps roadmap
regardless of distance within their rated range — geometric/diffraction loss grows with distance but
within a tight cluster (≤100 km) there is **no bandwidth penalty at all**. Pipeline-parallel
activation traffic is modest (activations, not weights), so 100+ Gbps is ample. The distance penalty
is **latency, not bandwidth**, until you approach the rated range limit.

### 2c. Pointing and aperture

Longer links demand finer pointing and/or larger apertures: beam divergence from diffraction means
the spot grows with distance, so a distant receiver captures a smaller fraction of transmitted power
([Frontiers in Physics](https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2021.778734/full),
[SPIE](https://spie.org/news/photonics-focus/mayjune-2024/transforming-tech-of-laserfree-space-optical-comms)).
A tight cluster is *easier* on the optics: at 1–10 km the pointing problem is trivial relative to a
2,000 km inter-plane link, the apertures can be small, and link margin is generous. This is a real
(if secondary) argument for keeping the compute cluster tight — it relaxes terminal cost and SWaP.

---

## 3. Satellite spacing for a compute cluster

Cooperating compute satellites want to be **close** (short links → low latency, easy pointing). The
floor on how close is **not optical** — it is **collision-avoidance, deployment dispersion, and
station-keeping**.

### What sets the minimum

- **Passive collision safety.** Standard formation-flying practice keeps satellites on slightly
  offset relative orbits (an "along-track string" or a helix) so that even with total loss of
  control they will not collide. Demonstrated close-proximity formations operate at relative
  distances **below ~2 km**, using helix geometry for passive safety; one mission held a steady
  **2 km** along-track separation
  ([CEAS Space Journal](https://link.springer.com/article/10.1007/s12567-026-00702-6),
  [CEAS Space Journal](https://link.springer.com/article/10.1007/s12567-020-00308-6)).
- **Deployment dispersion.** Satellites released from one launch vehicle separate with small
  relative velocities; without active control they drift apart over days. Holding a tight cluster
  requires either propulsion or differential-drag control.
- **Station-keeping.** At dawn-dusk SSO altitudes, differential atmospheric drag perturbs relative
  spacing. Differential-drag control can hold formations without propellant but is slow — a 3U
  CubeSat needs ~100 days to move 180° of true anomaly relative to a neighbor at 550 km
  ([MIT DSpace](https://dspace.mit.edu/handle/1721.1/112471)). A rack-class satellite is far more
  massive and less drag-agile, so it will need **modest active propulsion** for formation-keeping.

### Realistic minimum safe separation — *estimate*

For a tight compute cluster of rack-class satellites we estimate a practical rack-to-rack spacing of:

> **~1–10 km, with ~5 km as a sensible design point.**

Rationale: ~5 km is comfortably inside demonstrated close-proximity formation practice (≤2 km has
been flown), gives generous margin for the larger, less agile rack-class bus, allows a passively-safe
along-track-string or helix geometry, and tolerates realistic navigation/control error. Going tighter
than ~1 km is achievable but raises collision risk and station-keeping workload for no latency benefit
that matters (the difference between 1 km and 5 km is 13 µs — irrelevant).

**Latency cost of this spacing:** at 5 km, **~17 µs one-way per link** (~33 µs round trip). For an
8-rack daisy-chained string, end-to-end propagation across the whole cluster is ~7 hops × 17 µs ≈
**120 µs one way** — still well under a single pipeline-stage compute time. **The spacing is
effectively free.**

**Confidence:** the 1–10 km figure is the softest number in this document — it is an informed
extrapolation from CubeSat/smallsat formation-flying literature, not a flown rack-class result. It
should be firmed up with a dedicated GNC/collision-probability analysis (see Open Questions).

---

## 4. How many satellites for a full network?

Two distinct requirements, two very different answers.

### Requirement (a): cooperating nodes can always reach each other — the *compute cluster*

This is **easy**. A tight formation (Section 3) keeps all cooperating racks in permanent mutual
line-of-sight at ~km separations. **4–8 racks in one along-track string** satisfies (a) outright —
they fly together, links never break, no orbital-geometry problem to solve. This is the v1 service.

### Requirement (b): at least one node always reachable from a ground hub — the *constellation*

This is the **hard, expensive** part, and it is a classic constellation-coverage problem.

- A LEO satellite is in view of a given ground station only for **~5–15 minutes per pass, ~6–8
  passes/day** ([ResearchGate — LEO ground station communication duration](https://www.researchgate.net/publication/229022121_Practical_horizon_plane_and_communication_duration_for_Low_Earth_Orbiting_LEO_satellite_ground_stations)).
  A single satellite over a single hub is connected only a small fraction of the day.
- **Continuous coverage of one ground point** requires a string of satellites in the orbital plane
  spaced so the next one rises before the previous one sets — on the order of **10+ satellites per
  plane** at LEO altitude for one plane to keep one point covered as the plane rotates under it.
- **Global** continuous coverage needs a **Walker constellation**: notation `i: N/P/F` (N total
  satellites, P planes, F phasing). Real systems: Iridium is a Walker-Star `86.4°: 66/6/2` —
  **66 satellites in 6 planes** for global voice coverage
  ([Wikipedia — Satellite constellation](https://en.wikipedia.org/wiki/Satellite_constellation)).
  LEO global-navigation Walker designs need **180–264 satellites** depending on altitude
  ([MDPI Remote Sensing](https://www.mdpi.com/2072-4292/12/11/1845)).

**The key distinction:** a *tight compute cluster* (requirement a) and a *globally-distributed
constellation* (requirement b) are different machines. The compute cluster is 4–8 co-flying racks.
A constellation that guarantees a ground hub is always in view is **tens of satellites minimum** —
either many co-located clusters spread around one or more planes, or a small cluster plus a ring of
**cheap relay satellites** that hand the cluster's traffic down to whichever hub is currently
sunlit/cloud-free.

**Crucial point for v1:** you do **not** need requirement (b) for a first useful service. A single
compute cluster in dawn-dusk SSO passes over any given mid-latitude ground site several times a day;
with **3–4 geographically diverse ground hubs** the cluster has a downlink opportunity on most
orbits. The service is *batch / asynchronous inference* (jobs queued, results returned next contact)
or *near-real-time during passes* — not a 24/7 always-on endpoint. Building a 50+ satellite relay
constellation just to remove the contact gaps is a v2+ decision, not a v1 requirement.

---

## 5. Topology — all-to-all vs. meshed relay

**All-to-all is unnecessary and not how anyone builds this.** Starlink's ~9,000-satellite mesh is a
**sparse, locally-connected mesh**: each satellite carries only **3–4 laser terminals** and links to
its **immediate fore/aft neighbors in-plane and 1–2 neighbors in adjacent planes** — a lattice, not
a clique ([arXiv 2103.00056](https://arxiv.org/pdf/2103.00056),
[Casey Handmer — Starlink packet routing](https://caseyhandmer.wordpress.com/2020/09/23/starlink-packet-routing/)).
Traffic that needs to cross the constellation **multi-hops**: a packet relays satellite-to-satellite,
potentially thousands of km and many hops, before downlinking
([Hackaday](https://hackaday.com/2024/02/05/starlinks-inter-satellite-laser-links-are-setting-new-record-with-42-million-gb-per-day/),
[Medium — Engineering the LEO Mesh](https://mehmetozgenozdogan.medium.com/engineering-the-leo-mesh-starlink-routing-algorithms-and-optical-backbone-ee32f24c4aa3)).
Routing is dynamic — the constellation continuously reconfigures which links are up and recomputes
paths as satellites move ([MDPI Electronics](https://www.mdpi.com/2079-9292/11/14/2232)).

**The lesson for our design:**

- **A meshed relay topology is sufficient.** Each rack needs only **2–4 terminals**, not N–1.
- **Within the compute cluster**, the natural topology is a **daisy-chained ring/string**: rack *k*
  links to rack *k±1*. This exactly matches pipeline parallelism — pipeline stages are sequential,
  so activations flow rack→rack→rack down the string, one hop per stage. A ring (close the chain end
  to end) adds a second path for fault tolerance. **2 terminals/rack** suffices for a pure chain;
  **3–4** gives ring closure plus a cross-link or spare.
- **For ground delivery**, one or two racks in the cluster act as **downlink gateways** (or the
  cluster hands off to dedicated relay satellites in a v2 architecture).
- **Don't over-connect.** Every terminal is mass, power, cost, and a pointing system. Match terminal
  count to the actual traffic graph (a pipeline is a line graph), not to a worst-case all-to-all.

---

## 6. Strawman constellation spec (first useful orbital inference service)

A v1 service: an 8-rack pipeline-parallel inference cluster, batch/near-real-time, in dawn-dusk SSO.

| Parameter | Value | Basis |
|---|---|---|
| **Compute satellites** | **8** rack-class (NVL72-class) nodes | First-useful-service range was 4–8 nodes (`wave5_synthesis.md`); pick 8 for headroom to host a large pipelined model |
| **Formation** | Single **along-track string** (passively-safe; helix option for extra margin) | Demonstrated close-proximity formation practice |
| **Rack-to-rack spacing** | **~5 km** (range 1–10 km) | Section 3 — *estimate*; collision-safety floor, not optics |
| **ISL latency per link** | ~17 µs one-way (~33 µs RTT) | 3.336 µs/km × 5 km |
| **Cluster end-to-end latency** | ~120 µs one-way across all 8 racks | 7 hops × 17 µs — well under pipeline-stage compute time |
| **ISL terminals per satellite** | **3–4** CONDOR-class | 2 for the daisy chain (fore/aft), 1 for ring closure, 1 spare/cross-link or downlink |
| **Cluster topology** | Daisy-chained **ring** (chain + closure link) | Matches pipeline parallelism; ring gives a second path for fault tolerance |
| **ISL data rate** | 100 Gbps roadmap (CONDOR Mk3.1); ~2.5 Gbps as-delivered today | `optical_comms.md` — ample for activation traffic |
| **Downlink** | 1–2 racks act as optical downlink gateways | Section 5 |
| **Ground hubs** | **3–4** optical ground stations, >1,000 km apart | Weather diversity for 99%+ availability (`optical_ground_stations.md`); gives a downlink opportunity on most orbits |
| **Orbit** | Dawn-dusk sun-synchronous, LEO (~500–600 km) | Project baseline — continuous solar power, predictable thermal |
| **Coverage model** | Batch / pass-based, **not** 24/7 always-on | A single cluster is not globally always-reachable; v1 accepts contact gaps |

**What this strawman is NOT:** it does not provide an always-in-view ground link (requirement 4b).
Doing so needs a v2 architecture — either replicate the cluster into several planes, or add a ring
of ~dozens of cheap relay satellites. That is a deliberate v2 scope decision; v1 should not pay for
it.

**Scaling note:** a larger model simply lengthens the string (more racks, more pipeline stages) —
the topology and per-link latency are unchanged. The string can grow to dozens of racks before
cumulative propagation latency (still tens of µs per hop) becomes a concern. The constraint that
bites first is **station-keeping a long tight string**, not optics or latency.

---

## Sources

- [Hackaday — Starlink's Inter-Satellite Laser Links Set New Record (42M GB/day)](https://hackaday.com/2024/02/05/starlinks-inter-satellite-laser-links-are-setting-new-record-with-42-million-gb-per-day/)
- [Advanced Television — SpaceX reveals Starlink laser capacity](https://www.advanced-television.com/2024/02/02/spacex-reveals-starlink-laser-capacity/)
- [arXiv 2103.00056 — Laser Inter-Satellite Links in a Starlink Constellation](https://arxiv.org/pdf/2103.00056)
- [Connectivity.technology — Laser Inter-Satellite Links (LISLs) in a Starlink Constellation](https://www.connectivity.technology/2022/02/laser-inter-satellite-links-lisls-in.html)
- [MDPI Electronics — Laser ISL Visibility and Topology Optimization for Mega Constellation](https://www.mdpi.com/2079-9292/11/14/2232)
- [MSA Components — Entering the Next Era of Laser Communication with the CONDOR Mk3](https://msa-components.com/entering-the-next-era-of-laser-communication-with-the-condor-mk3/)
- [satsearch — Mynaric CONDOR Mk3](https://satsearch.co/products/mynaric-condor-mk3)
- [CEAS Space Journal — In-orbit demonstration of propulsive and drag-based formation control (2U CubeSats)](https://link.springer.com/article/10.1007/s12567-026-00702-6)
- [CEAS Space Journal — Orbit deployment and drag control strategy for formation flight](https://link.springer.com/article/10.1007/s12567-020-00308-6)
- [MIT DSpace — CubeSat constellation implementation and management using differential drag](https://dspace.mit.edu/handle/1721.1/112471)
- [MDPI Remote Sensing — Optimal Walker Constellation Design of LEO-Based Global Navigation System](https://www.mdpi.com/2072-4292/12/11/1845)
- [Wikipedia — Satellite constellation (Walker notation, Iridium)](https://en.wikipedia.org/wiki/Satellite_constellation)
- [ResearchGate — Practical horizon plane and communication duration for LEO satellite ground stations](https://www.researchgate.net/publication/229022121_Practical_horizon_plane_and_communication_duration_for_Low_Earth_Orbiting_LEO_satellite_ground_stations)
- [Casey Handmer — Starlink packet routing](https://caseyhandmer.wordpress.com/2020/09/23/starlink-packet-routing/)
- [Medium — Engineering the LEO Mesh: Starlink Routing Algorithms and Optical Backbone](https://mehmetozgenozdogan.medium.com/engineering-the-leo-mesh-starlink-routing-algorithms-and-optical-backbone-ee32f24c4aa3)
- [Frontiers in Physics — Free-Space Optical Communication Link for Diverse Beam Divergence Profiles](https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2021.778734/full)
- [SPIE — The transformative technology of laser/free-space optical communications](https://spie.org/news/photonics-focus/mayjune-2024/transforming-tech-of-laserfree-space-optical-comms)

## Open questions

1. **Minimum safe rack-to-rack spacing for rack-class satellites (the softest number here).** The
   1–10 km estimate is extrapolated from CubeSat/smallsat formation flying. A rack-class satellite
   is far more massive, has different ballistic coefficient and drag-agility, and may have larger
   deployable solar/radiator structures that change collision cross-section. Needs a dedicated
   GNC + collision-probability analysis to firm up the ~5 km design point.
2. **Station-keeping cost of a long tight string.** Holding 8+ rack-class satellites at ~5 km
   spacing in dawn-dusk SSO against differential drag — propellant budget, propulsion sizing, and
   how long a string can grow before station-keeping dominates the ops budget.
3. **Pipeline-stage compute time vs. ISL latency — exact numbers.** This doc uses "hundreds of µs
   to a few ms" per stage as a rule of thumb. The precise per-stage time for the target model on an
   NVL72-class rack would sharpen the "keep within ~100 km" threshold (cross-ref `multi_rack_inference.md`).
4. **Deployment geometry from a single Neutron launch.** Can one Neutron deliver 8 racks into a
   tight string directly, or is post-deployment formation acquisition (drift + propulsive
   capture) required? Affects time-to-service and propellant budget.
5. **v2 relay-constellation sizing.** If/when always-in-view ground reachability is required, how
   many relay satellites in how many planes — and whether relays should be cheap comms-only
   satellites or additional compute racks doing double duty.
6. **Inter-cluster links.** If multiple compute clusters are flown, do they need ISLs *between*
   clusters (a cluster-of-clusters mesh), or does each cluster operate independently with its own
   ground hubs? Drives total terminal count and routing complexity.
