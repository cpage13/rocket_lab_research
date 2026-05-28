# Optical / Laser Communications for an Orbital Data Center

*Research date: May 2026. Part of the Rocket Lab orbital AI-inference data center feasibility study.*

## Summary

Laser (free-space optical) communication is the only credible backbone for a mesh of orbital
compute satellites. Inter-satellite links (ISLs) are a **proven technology at scale**: SpaceX's
Starlink runs ~9,000+ satellites with ~3 laser terminals each, moving **42+ petabytes/day** at a
constellation throughput of ~5.6 Tbps, with each terminal rated **up to ~200 Gbps** and >99% link
uptime. Rocket Lab's acquired asset, **Mynaric's CONDOR Mk3**, is a flight-proven terminal but a
generation behind Starlink's in-house lasers: it is **configured to ~2.5 Gbps today** (Tranche 1
SDA hardware). The official Via Satellite description of the Mk3 is a **"configurable modem up
to ~2.5 Gbps"**; **100 Gbps is the next-generation CONDOR Mk3.1 roadmap target** for SDA
Tranche 2, not a Mk3 hardware ceiling. The Mk3 mesh therefore ships at ~2.5 Gbps today, and
the project's 100 Gbps aspiration depends on the Mk3.1 roadmap landing.

The hard problem is **ground↔space optical links**: lasers cannot penetrate cloud. A space-to-ground
optical downlink can hit **100–200 Gbps per link** (NASA TBIRD demonstrated 200 Gbps), but a single
ground site only achieves ~50–70% weather availability. Reaching 99–99.9% availability requires a
**diverse network of 4+ optical ground stations** spaced >1,000 km apart so their cloud cover is
uncorrelated. This is workable but adds cost, latency variability, and operational complexity.

**Bottom line for the data center:** laser ISLs are the right choice for the orbital mesh.
Ground-link feasibility is the binding constraint and the main open risk.

---

## 1. Inter-Satellite Optical Links (ISL)

### Mynaric CONDOR Mk3 — Rocket Lab's in-house terminal

Rocket Lab completed its acquisition of Mynaric on **14 April 2026** (~$155M total consideration),
gaining the CONDOR product line and a ~300-person Munich engineering team
([Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-completes-mynaric-acquisition-adding-laser-optical-communications-to-growing-space-systems-portfolio/),
[GlobeNewswire](https://www.globenewswire.com/news-release/2026/04/14/3273899/0/en/Rocket-Lab-Completes-Mynaric-Acquisition-Adding-Laser-Optical-Communications-To-Growing-Space-Systems-Portfolio.html)).

| Parameter | CONDOR Mk3 | Notes / confidence |
|---|---|---|
| Data rate (as delivered, SDA T1) | **~2.5 Gbps** | Official: "configurable modem up to 2.5 Gbps" ([Via Satellite](https://www.satellitetoday.com/government-military/2025/06/05/mynaric-reports-condor-mk3-delivery-milestone-progress-on-mk3-1-terminal-for-sda/)) |
| Data rate (hardware-configurable range) | 100 Mbps – **100 Gbps** | Vendor framing; the 100 Gbps end is aspirational/Mk3.1, see below ([satsearch](https://satsearch.co/products/mynaric-condor-mk3)) |
| Link range | up to **6,500 km** | Official spec ([satnow](https://www.satnow.com/products/laser-communication-terminals/mynaric/155-1475-condor-mk3)) |
| Optical head dimensions | 372 × 282 × 257 mm | Official; "30% smaller than Mk2" ([MSA Components](https://msa-components.com/entering-the-next-era-of-laser-communication-with-the-condor-mk3/)) |
| Supply voltage | 22–38 VDC | Official ([satnow](https://www.satnow.com/products/laser-communication-terminals/mynaric/155-1475-condor-mk3)) |
| Wavelength | 1536–1553 nm (C-band optical) | Official ([satnow](https://www.satnow.com/products/laser-communication-terminals/mynaric/155-1475-condor-mk3)) |
| Design life | 7+ years in LEO | Official ([satnow](https://www.satnow.com/products/laser-communication-terminals/mynaric/155-1475-condor-mk3)) |
| Mass | **Not publicly disclosed** (estimate ~10–15 kg full terminal) | FLAGGED ESTIMATE — Mynaric publishes "30% lighter than Mk2" but no absolute kg; class-typical LEO OCTs run ~8–15 kg |
| Power consumption | **Not publicly disclosed** (estimate ~60–120 W) | FLAGGED ESTIMATE — class-typical for LEO OCTs; verify with Mynaric datasheet under NDA |

**CONDOR Mk3.1** is in development targeting **up to 100 Gbps** for SDA Tranche 2 and commercial
use ([Via Satellite](https://www.satellitetoday.com/government-military/2025/06/05/mynaric-reports-condor-mk3-delivery-milestone-progress-on-mk3-1-terminal-for-sda/)).
This is the terminal class an orbital data center mesh would actually want.

> **Key caveat:** Mynaric has delivered 100+ CONDOR Mk3 units, but those are operating at
> ~2.5 Gbps. A data-center mesh needs ~100 Gbps-class links — that capability is **roadmap, not
> shipping product**, as of May 2026.

### Proven scale: Starlink's laser mesh

Starlink is the existence proof that laser meshes work at constellation scale:

- Each satellite carries **~3 optical ISL terminals**, each rated **up to ~200 Gbps**
  ([Hackaday](https://hackaday.com/2024/02/05/starlinks-inter-satellite-laser-links-are-setting-new-record-with-42-million-gb-per-day/),
  [Advanced Television](https://www.advanced-television.com/2024/02/02/spacex-reveals-starlink-laser-capacity/)).
- Constellation moves **>42 PB/day** across its laser mesh (~9,000+ satellites × ~3 terminals ≈ **~27,000 space lasers**), ~5.6 Tbps aggregate
  ([Hackaday](https://hackaday.com/2024/02/05/starlinks-inter-satellite-laser-links-are-setting-new-record-with-42-million-gb-per-day/)).
- SpaceX reports **>99% link uptime** on its 100G-class ISL fleet
  ([Hackaday](https://hackaday.com/2024/02/05/starlinks-inter-satellite-laser-links-are-setting-new-record-with-42-million-gb-per-day/)).

Takeaway: **per-terminal ISL rates of 100–200 Gbps are real and operational today** — just not from
Mynaric hardware yet. A data-center mesh node with 3–4 terminals could plausibly carry
0.3–0.8 Tbps of inter-node traffic with current-generation (non-Mynaric) technology, or with the
Mk3.1 once fielded.

---

## 2. Optical Ground ↔ Space Links

### Achievable data rate

Space-to-ground optical downlink is fast: NASA's **TBIRD demonstrated 200 Gbps** from a CubeSat,
the highest space-to-ground optical rate achieved, after a 100 Gbps demo in 2022
([NASA](https://www.nasa.gov/centers-and-facilities/goddard/nasa-partners-achieve-fastest-space-to-ground-laser-comms-link/),
[Via Satellite](https://www.satellitetoday.com/technology/2023/05/12/nasas-tbird-mission-demonstrates-breaks-its-own-record-with-200-gbps-optical-downlink/)).
So raw throughput per ground link (100–200 Gbps) is **not** the bottleneck.

### The cloud-cover problem

Optical links **cannot penetrate cloud, fog, heavy rain, or snow** — unlike RF, the link simply
drops ([Cailabs](https://www.cailabs.com/aerospace-defense/laser-communications/optical-ground-stations/),
[Reuniwatt](https://reuniwatt.com/en/applications/defence-space/free-space-optical-communications/)).
Atmospheric turbulence also distorts the beam, requiring **adaptive optics** (deformable mirrors)
at the ground station ([NASA JPL](https://www.jpl.nasa.gov/news/getting-nasa-data-to-the-ground-with-lasers/)).
A single optical ground station typically achieves only ~50–70% annual availability due to weather.

### Ground-station diversity (the solution)

The standard mitigation is a **geographically diverse network of optical ground stations (OGS)**:

- Stations must be **>1,000 km apart** so cloud cover is statistically uncorrelated — when one is
  clouded out, another is likely clear
  ([arXiv 2402.13282](https://arxiv.org/html/2402.13282v1),
  [arXiv 2410.23470](https://arxiv.org/html/2410.23470v2)).
- **At least four OGS** are generally needed for "reasonable" availability; a well-sited
  continental/global network converges to **~99.9%**
  ([arXiv 2410.23470](https://arxiv.org/html/2410.23470v2)).
- NASA explicitly pairs sites with anti-correlated weather (e.g. California OGS-1 ↔ Hawaii OGS-2)
  ([NASA JPL](https://www.jpl.nasa.gov/news/getting-nasa-data-to-the-ground-with-lasers/)).
- Requires autonomous cloud-monitoring and predictive weather scheduling to route downlinks to
  whichever station is clear ([Reuniwatt](https://reuniwatt.com/en/applications/defence-space/free-space-optical-communications/)).

**Implication for the data center:** customer traffic uplinked/downlinked optically needs a
multi-site ground network (5–10+ stations for high availability and capacity). This is a real
capital and operations line item, and it introduces variable latency as traffic is rerouted to
clear sites. An RF backup path for the ground link should be considered (see `rf_satcom.md`).

---

## 3. Mesh Topology and Latency

A compute constellation routes traffic node-to-node over ISLs, forming a dynamic mesh:

- Because LEO satellites move relative to each other, links between orbital planes ("inter-plane")
  change geometry constantly; **intra-plane links are more stable** than inter-plane
  ([arXiv 2406.01953](https://arxiv.org/html/2406.01953v1)).
- Establishing/re-acquiring an optical link incurs a **setup delay on the order of seconds**, so
  constellations precompute a largely static topology and update routes on a schedule
  ([arXiv 2406.01953](https://arxiv.org/html/2406.01953v1)).
- End-to-end latency = propagation delay + per-hop processing/queuing. Routing algorithms trade
  **fewer hops (longer individual ISLs)** against congestion; modern approaches use ML/DRL to
  balance latency and jitter ([arXiv 2512.20835](https://arxiv.org/html/2512.20835v1)).

**For an AI-inference data center this is mostly favorable:** inference workloads are latency-
tolerant compared to interactive web traffic, and most heavy traffic is *within* the mesh
(model weights, activations between compute nodes) where laser ISLs excel. Light-speed in vacuum
is ~50% faster than in fiber, so intra-mesh latency is competitive. The latency-sensitive leg is
the ground hop, which is dominated by which OGS is weather-available, not by the mesh itself.

---

## 4. Pros and Cons for an Orbital Data Center

**Pros**
- Enormous bandwidth headroom — 100–200 Gbps/terminal proven; multi-Tbps per node feasible with
  several terminals.
- **No spectrum licensing.** Optical frequencies are unregulated/unlicensed — a decisive advantage
  for a new entrant (see `rf_satcom.md`).
- Narrow beams: no inter-satellite interference, hard to intercept (security), good spatial reuse.
- Lower mass/power/size than equivalent-capacity RF; receivers can be far smaller than RF antennas.
- Proven at constellation scale (Starlink) and flight-proven hardware in-house (Mynaric CONDOR).

**Cons**
- **Ground links are weather-limited** — the central architectural risk; needs a diverse,
  multi-site OGS network and predictive scheduling.
- **Tight pointing requirement** — microradian-class pointing, acquisition can take seconds;
  moving parts and adaptive optics add complexity and failure modes.
- **Mynaric's shipping hardware is ~2.5 Gbps**, not 100 Gbps — the data-rate the data center needs
  depends on the Mk3.1 roadmap delivering.
- Vendor/Mynaric publishes no public mass/power figures — design planning needs NDA datasheets.
- Mesh topology is dynamic; routing and link re-acquisition add engineering complexity.

---

## Sources

- [Rocket Lab — Completes Mynaric Acquisition](https://rocketlabcorp.com/updates/rocket-lab-completes-mynaric-acquisition-adding-laser-optical-communications-to-growing-space-systems-portfolio/)
- [GlobeNewswire — Rocket Lab Completes Mynaric Acquisition](https://www.globenewswire.com/news-release/2026/04/14/3273899/0/en/Rocket-Lab-Completes-Mynaric-Acquisition-Adding-Laser-Optical-Communications-To-Growing-Space-Systems-Portfolio.html)
- [satnow — CONDOR Mk3 product spec](https://www.satnow.com/products/laser-communication-terminals/mynaric/155-1475-condor-mk3)
- [satsearch — CONDOR Mk3](https://satsearch.co/products/mynaric-condor-mk3)
- [MSA Components — Entering the Next Era of Laser Communication with the CONDOR Mk3](https://msa-components.com/entering-the-next-era-of-laser-communication-with-the-condor-mk3/)
- [Via Satellite — Mynaric Condor Mk3 Delivery Milestone, Mk3.1 for SDA](https://www.satellitetoday.com/government-military/2025/06/05/mynaric-reports-condor-mk3-delivery-milestone-progress-on-mk3-1-terminal-for-sda/)
- [Hackaday — Starlink's Inter-Satellite Laser Links 42M GB/day](https://hackaday.com/2024/02/05/starlinks-inter-satellite-laser-links-are-setting-new-record-with-42-million-gb-per-day/)
- [Advanced Television — SpaceX reveals Starlink laser capacity](https://www.advanced-television.com/2024/02/02/spacex-reveals-starlink-laser-capacity/)
- [NASA — Fastest Space-to-Ground Laser Comms Link (TBIRD 200 Gbps)](https://www.nasa.gov/centers-and-facilities/goddard/nasa-partners-achieve-fastest-space-to-ground-laser-comms-link/)
- [Via Satellite — TBIRD 200 Gbps Optical Downlink](https://www.satellitetoday.com/technology/2023/05/12/nasas-tbird-mission-demonstrates-breaks-its-own-record-with-200-gbps-optical-downlink/)
- [NASA JPL — Getting NASA Data to the Ground With Lasers](https://www.jpl.nasa.gov/news/getting-nasa-data-to-the-ground-with-lasers/)
- [Cailabs — Optical Ground Stations](https://www.cailabs.com/aerospace-defense/laser-communications/optical-ground-stations/)
- [Reuniwatt — Cloud observation for free-space optical communications](https://reuniwatt.com/en/applications/defence-space/free-space-optical-communications/)
- [arXiv 2410.23470 — Advancing FSO Architecture: OGS Network Configurations](https://arxiv.org/html/2410.23470v2)
- [arXiv 2402.13282 — German and Australasian Optical Ground Station Networks](https://arxiv.org/html/2402.13282v1)
- [arXiv 2406.01953 — On-Demand Routing in LEO Mega-Constellations with Dynamic Laser ISLs](https://arxiv.org/html/2406.01953v1)
- [arXiv 2512.20835 — QoS- and Physics-Aware Routing in Optical LEO Networks](https://arxiv.org/html/2512.20835v1)

## Open Questions / Uncertainties

- **CONDOR Mk3 mass and power are not public.** ~10–15 kg / ~60–120 W are class-typical estimates;
  must be confirmed against Mynaric's internal datasheet (now a Rocket Lab asset).
- **When does the 100 Gbps Mk3.1 actually ship?** The data center's mesh bandwidth assumption
  depends on this. Current product is ~2.5 Gbps.
- **OGS network sizing/cost** — how many ground stations, where, and at what capex/opex for the
  target availability and aggregate customer throughput? Not yet costed.
- **Aggregate ground throughput** — TBIRD's 200 Gbps was a single brief pass. Sustained,
  multi-station downlink capacity for a commercial data center is unproven at the needed scale.
- **Latency budget** — variable rerouting to weather-clear OGS could matter for some inference SLAs;
  needs a target-SLA analysis.
- Does Rocket Lab intend to build/operate its own OGS network, or partner (e.g. with an OGS-as-a-
  service provider)?
