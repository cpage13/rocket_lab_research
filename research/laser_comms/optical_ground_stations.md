# Large Optical Ground Stations — the Ground End of a Space-to-Ground Laser Link

*Research date: May 2026. Part of the Rocket Lab orbital AI-inference data center feasibility study.*
*Companion to `optical_comms.md` (ISLs + downlink overview) and `rf_satcom.md`.*

## Summary / Verdict

The founder's "monster optical ground station" idea is **half right**. Going *capable* at a hub
helps a lot; going *physically gigantic* at a single site does **not**, and it does **nothing** for
the binding constraint, which is weather.

Three findings drive the verdict:

1. **A modest ground telescope is already enough.** NASA's TBIRD demonstrated **200 Gbps**
   space-to-ground — the fastest optical downlink ever — into a ground terminal with a
   sub-meter-class aperture. The trick was putting the *power and complexity on the satellite*,
   not the ground. Ground apertures for near-Earth links are universally in the **0.5–1.0 m**
   range (ESA Tenerife OGS: 1 m; commercial Cailabs/Safran stations: 0.6–0.8 m). Telescope cost
   scales as roughly **aperture^2.5**, so a "monster" 5–10 m dish costs 30–100× a 1 m station and
   buys only a few dB of link margin you can get far more cheaply by adding satellite transmit
   power. Aperture gain is real but **sharply diminishing** and **capped in practice** by
   atmospheric turbulence: beyond the ~0.5–1 m point you stop coupling cleanly into a single-mode
   fiber/coherent receiver without ever-more-elaborate adaptive optics.

2. **The weather problem is not solved by size — only by *number of sites*.** A laser cannot
   punch through cloud, period. A single ground site achieves only ~50–70% availability no matter
   how big the telescope. Published diversity studies are consistent: you need **≥4 stations
   >1,000 km apart** for ~99%, and **~10–12 stations** for carrier-grade 99.9% ("three nines").
   So the architecture is **"several capable hubs," not "one monster."** Building bigger at one
   site is the wrong axis to optimize.

3. **Aggregate throughput is plausible — but it's a *network* number, not a *station* number.**
   A top-tier station can sustainably field **multiple ~100–200 Gbps downlinks** (one per
   satellite in view, limited by how many telescope mounts/terminals you co-locate). A handful of
   diverse hubs, each with several terminals, can aggregate into the **multi-Tbps** range —
   comparable to what ESA's HydRON program targets. Crucially, **AI inference is bandwidth-light**
   relative to training: inference traffic is prompts up / tokens down, megabytes not petabytes
   per query. The ground network is unlikely to be the throughput bottleneck for an
   *inference* data center. It *is* the availability and latency-variability risk.

**Bottom line:** the model should be **"a few diverse, fiber-connected hub stations, each with
~0.6–1 m terminals (possibly several per site),"** not "one giant telescope." Going big at one
site wastes capital on aperture and still leaves you weather-grounded. Going diverse is the answer.
Confidence: **high** on the physics and the diversity conclusion; **medium** on cost figures and
on the exact per-hub terminal count, which depends on constellation geometry.

---

## 1. State of the Art — Real Optical Ground Stations

All data rates below are **demonstrated** unless flagged as *target/spec*.

| Station | Aperture | Demonstrated rate | Link served | Notes |
|---|---|---|---|---|
| **NASA Table Mountain (TBIRD ground terminal), CA** | sub-meter class (~0.5 m) | **200 Gbps** downlink; 4.8 TB in one ~5-min pass | LEO 6U CubeSat (PTD-3/TBIRD) | Fastest space-to-ground optical link ever, Apr 2023. Deliberately *small/simple* ground terminal — power put on the design via high satellite EIRP + ARQ. ([NASA](https://www.nasa.gov/centers-and-facilities/goddard/nasa-partners-achieve-fastest-space-to-ground-laser-comms-link/), [NASA NTRS PDF](https://ntrs.nasa.gov/api/citations/20230007959/downloads/TBIRD-smallsat-2023.pdf)) |
| **NASA LCRD OGS-1 (Table Mountain, CA)** & **OGS-2 (Haleakalā, HI)** | ~0.6–1 m class | **1.2 Gbps** each direction (GEO relay) | GEO Laser Communications Relay Demonstration | Deliberately a *two-site* network; sites chosen so weather is anti-correlated (CA cloudy ⇄ HI clear). Both use adaptive optics. ([NASA](https://www.nasa.gov/technology/getting-nasa-data-to-the-ground-with-lasers/), [NASA Goddard ESC](https://esc.gsfc.nasa.gov/projects/LCRD/?tab=overview)) |
| **ESA Optical Ground Station (OGS), Teide, Tenerife** | **1.0 m** | Multi-Gbps class in tests; historic ARTEMIS GEO link (~50 Mbps era) | LEO/GEO test terminal, ARTEMIS, quantum links | At 2,400 m altitude, above most cloud. First stable ground-satellite laser link (ARTEMIS, 2001). 25+ years of service. ([Wikipedia](https://en.wikipedia.org/wiki/ESA_Optical_Ground_Station), [ESA](https://www.esa.int/Enabling_Support/Space_Engineering_Technology/Space_Optoelectronics/Optical_Ground_Station_OGS)) |
| **Caltech Hale Telescope, Palomar, CA (DSOC downlink receiver)** | **5.1 m** (200-inch) | **267 Mbps** from deep space (Psyche, ~19M mi) | NASA DSOC deep-space demo | The one genuinely "monster" aperture in the set — needed *only* because the source is ~10^8–10^9 km away and photon-starved. Fitted with a cryogenic superconducting-nanowire single-photon detector. ([JPL DSOC press kit](https://www.jpl.nasa.gov/press-kits/psyche/dsoc/), [NASA DSOC](https://www.nasa.gov/directorates/stmd/tech-demo-missions-program/deep-space-optical-communications-dsoc/nasas-tech-demo-streams-first-video-from-deep-space-via-laser/)) |
| **NASA OCTL / Table Mountain uplink (DSOC ground transmitter)** | ~1 m transmit telescope | n/a (uplink beacon + low-rate command) | DSOC uplink | 5 kW-class ground laser for beacon/uplink. Illustrates uplink/downlink asymmetry (see §4). ([JPL](https://www.jpl.nasa.gov/images/pia26661-table-mountain-facility-sends-dsoc-laser-beacon-to-nasas-psyche-infrared-image/)) |
| **Cailabs TILBA-OGS / "L10" (commercial, France)** | **0.8 m** | **>10 Gbps** target, two-way; remotely operable | LEO direct-to-Earth; SDA/CCSDS compliant | Being deployed with SES; a 12-unit Transportable-OGS lot with DataPath integrating from Q2 2026. The emerging commercial baseline. ([Cailabs](https://www.cailabs.com/aerospace-defense/laser-communications/optical-ground-stations/), [Via Satellite](https://www.satellitetoday.com/technology/2025/12/15/cailabs-partners-with-datapath-to-build-transportable-optical-ground-stations/)) |
| **Safran IRIS OGS (commercial, France)** | sub-meter class | multi-Gbps; productized | LEO direct-to-Earth | Productized commercial OGS line. ([Safran](https://www.safran-group.com/products-services/iris-optical-ground-station-space-laser-communications)) |
| **SSC Space optical ground network (NODES, ESA ScyLight)** | sub-meter (Cailabs-supplied units) | multi-Gbps; first site Western Australia | LEO downlink network | ESA-funded *network* — note the explicit framing as a network, not a single big site. ([SSC](https://sscspace.com/ssc-awarded-1-1me-contract-by-esa-for-optical-ground-network/)) |
| **JAXA / NICT (Japan) optical ground stations** | ~1 m class | multi-Gbps in LEO/GEO tests (SOTA, LUCAS/HICALI) | LEO CubeSat (SOTA), GEO (HICALI) | Long-running optical comms program; consistent with the global ~1 m norm. ([eoPortal context](https://www.eoportal.org/satellite-missions/tbird)) |
| **Heriot-Watt HOGS (UK)** | **0.7 m** terminal + 0.4 m piggyback | QKD-focused; single-photon class | Quantum key distribution | Build cost **£2.5M (~$3.3M)** — a useful cost datapoint (see §6). ([Laser Focus World](https://www.laserfocusworld.com/quantum/article/55234082/optical-ground-stations-push-boundaries-of-space-technology)) |

**The pattern is unmistakable:** every *near-Earth* optical ground station — government and
commercial alike — clusters at **0.5–1.0 m aperture.** The only large-aperture ground telescope
in optical comms is Palomar's 5.1 m Hale, and it is large *solely* because deep-space links are
photon-starved by inverse-square loss over astronomical distances. A LEO/sun-synchronous data
center is ~500–1,200 km away, ~10^5–10^6× closer than Psyche. **It does not need a monster
telescope.**

---

## 2. Does Aperture / Size Help? — The Link-Budget Physics

### How aperture enters the link budget

A receive telescope is a "photon bucket." Received power scales with collecting area, i.e. with
**aperture diameter squared (D²)**. The receive antenna gain is `G_rx ≈ (π·D/λ)²`. So doubling the
aperture quadruples collected power — **+6 dB of link margin.** That sounds great, and at the
margin it is. But three effects cap the benefit:

1. **Diminishing returns into rate.** With efficient coding, channel capacity rises only
   *logarithmically* with received power once you are above threshold. Going from a 0.5 m to a
   1.0 m dish (+6 dB) is meaningful near the link edge; going from 1 m to 4 m (+12 dB) buys
   progressively less *usable* data rate and is wildly cheaper to obtain by other means.

2. **The atmosphere caps the *useful* aperture.** A modern high-rate receiver (coherent
   detection, or single-mode-fiber-coupled) needs the wavefront focused to near the diffraction
   limit. Atmospheric turbulence scrambles the wavefront over a coherence length (Fried parameter
   r₀) of only **~5–20 cm** at good sites in the near-IR. A telescope much larger than r₀ collects
   more light but spreads it into a turbulence-blurred blob that **won't couple into a single-mode
   fiber** without adaptive optics — and AO gets exponentially harder as D/r₀ grows (more actuators,
   faster loops, higher cost). So past ~0.5–1 m you are paying for aperture you can't cleanly use.
   Demonstrated high-rate links (e.g. the **100 Gbps coherent LEO-rate demo**, and **0.94 Tbit/s**
   over a 53 km mountain path) all rely on AO-corrected single-mode coupling, not raw aperture.
   ([Nature — 100 Gbps coherent](https://www.nature.com/articles/s41598-022-22027-0),
   [PMC — Tbit/s feeder link](https://pmc.ncbi.nlm.nih.gov/articles/PMC10282091/))

3. **TBIRD proves the point in reverse.** NASA hit **200 Gbps** — still the record — into a
   *small, simple* ground terminal. Their own design philosophy: *"exploit the large increase in
   power delivered from the space terminal to considerably reduce the size and complexity of the
   ground terminal."* Margin is far cheaper to buy with **satellite transmit power and aperture,
   plus ARQ (automatic retransmit)** than with a giant ground telescope.
   ([NASA NTRS PDF](https://ntrs.nasa.gov/api/citations/20230007959/downloads/TBIRD-smallsat-2023.pdf))

### How big can a practical ground telescope be?

- **Near-Earth optical comms:** practical/economic optimum is **0.5–1.0 m.** This is the global
  norm and there's a physics reason for it (r₀, AO complexity, cost^2.5 scaling).
- **Deep space:** NASA studies call for **>10 m equivalent** ground apertures — but explicitly
  because deep-space links are photon-starved. Not relevant to a LEO/SSO data center.
- A 4–10 m "monster" comms telescope is buildable (astronomy does it), but it is an
  **astronomical-observatory-class capital project** ($100M+), needs a full AO system to be
  useful at high rate, and still delivers only single-digit-dB more margin than a 1 m station.

### Verdict on "going big"

Bigger beats smaller **only near the link edge, and only weakly** (logarithmic rate gain, capped
by turbulence). The gains are **real but sharply capped.** A far better use of capital: **more
terminals and more sites.** The "monster telescope" is the wrong thing to scale.

---

## 3. The Cloud Problem — and Why Size Doesn't Fix It

This is the crux, and the honest answer is uncomfortable for the "monster hub" thesis.

**Lasers do not penetrate cloud.** Adaptive optics corrects *turbulence* (clear-air wavefront
distortion); it does **nothing** for an opaque cloud deck. A 10 m telescope under a cloud is as
blind as a 0.3 m telescope under the same cloud. Aperture is irrelevant to the dominant outage
cause.

What actually moves availability:

- **Site selection.** High, dry sites above the boundary layer (Tenerife OGS at 2,400 m;
  Haleakalā; Table Mountain) clear most low cloud and cut turbulence. A single *excellent* site
  still tops out around **~50–70% availability** — useless on its own for a commercial service.
- **Adaptive optics.** Recovers data rate / fiber coupling on *clear* nights and through haze.
  Necessary, but it raises the *quality* of good-weather links, not the *fraction* of good weather.
- **Ground-station diversity — the real answer.** Multiple stations far enough apart that their
  cloud cover is statistically independent. Published consensus:
  - Stations must be **>1,000 km apart**; closer than that and weather is correlated and you gain
    little. ([DLR — Optical Satellite Downlinks to OGS](https://elib.dlr.de/55548/1/OLEO-DL_to_OGS_and_HAPs-IST07.pdf))
  - **≥4 stations** to reach ~99%.
  - **~10–12 stations** for carrier-grade **99.9% ("three nines").**
  ([arXiv — OGS network configurations](https://arxiv.org/html/2410.23470v2),
  [SatNews — "Downlink Deficit"](https://satnews.com/2026/04/03/the-downlink-deficit-the-pentagons-optical-mesh-network-and-the-terrestrial-bottleneck/))

**So: does going BIG at one site help? No.** A single site, however monstrous, is weather-capped
at ~50–70%. The "few monster hubs" model is acceptable **only if "few" means ≥4 and they are
geographically diverse (>1,000 km apart, anti-correlated climates).** That is exactly how NASA
built LCRD (CA + HI) and how ESA's NODES and HydRON are structured — as *networks*. The founder's
instinct to consolidate into hubs is fine **for the fiber-aggregation and capex side**; it is
**wrong if it reduces the number of geographic sites.** Capability per site: yes. Count of sites:
do not cut.

Industry reality check: the April 2026 SatNews analysis estimates the industry has built only
**~10% of the optical ground infrastructure it needs**, with satellite operators and ground
providers each waiting for the other to invest first ("the downlink deficit"). Ground-segment
build-out — not the space segment — is currently the limiting factor for optical-downlink
constellations. ([SatNews](https://satnews.com/2026/04/03/the-downlink-deficit-the-pentagons-optical-mesh-network-and-the-terrestrial-bottleneck/))

---

## 4. Uplink vs. Downlink — the Asymmetry

The data center's customer traffic goes **UP** to the satellites (prompts/requests) and inference
**results come DOWN** (generated tokens). Both directions exist; they are not symmetric.

**Downlink (space → ground): the easy direction.**
- The satellite's beam traverses clear vacuum, then hits the atmosphere only in the **last ~20 km**.
  By then the beam is wide; turbulence causes *scintillation* (intensity flicker) and wavefront
  distortion, both correctable with AO + the large-ish receive aperture.
- This is where the 200 Gbps / 100 Gbps demonstrations live.

**Uplink (ground → space): the hard direction.**
- The ground laser enters turbulence **immediately, while the beam is still narrow.** Turbulent
  eddies larger than the beam cause **beam wander** — the spot dances around the satellite, with
  displacements that can reach **hundreds of meters** at the spacecraft. This directly costs
  uplink power and link margin.
- **Point-ahead:** because the satellite moves and light is finite-speed, the uplink must be aimed
  *ahead* of where the satellite appears. The point-ahead angle is small (~tens of µrad) but it
  means the uplink beam travels a *slightly different atmospheric path* than the downlink — so AO
  sensing on the downlink only **partially** pre-corrects the uplink (anisoplanatism). Uplink
  pre-compensation is an active research area, not a fully solved one.
  ([MDPI — AO pre-compensation field review](https://www.mdpi.com/2304-6732/10/7/858),
  [DLR — AO pre-compensated uplink](https://elib.dlr.de/140930/1/oe-29-4-6113.pdf))
- Mitigations: transmit through **multiple sub-apertures** (ESA Tenerife splits the uplink into
  4 beams to average out turbulence), use **higher ground laser power** (DSOC's ground transmitter
  is **~5 kW**, vs. the spacecraft's mere **4 W** transmitter — a stark illustration of the
  asymmetry: the ground side compensates with brute power), and aim with fast tip/tilt + point-ahead.

**Implication for the data center.** Inference is naturally **down-heavy**: a short prompt up, a
longer generated response down. The harder uplink direction carries the *lighter* load, which is
fortunate. But uplink is real, non-trivial engineering and **not free** — budget for high-power,
multi-sub-aperture ground transmitters and AO pre-compensation at every hub. Uplink is the more
likely place for a per-link rate ceiling, and uplink reliability deserves explicit attention in
any deeper study.

---

## 5. Throughput Aggregation — Can a Hub Carry the Data Center?

**Per terminal:** demonstrated **100–200 Gbps** per space-to-ground link (TBIRD 200 Gbps; coherent
LEO-rate 100 Gbps). Call **100 Gbps** a conservative, near-Earth sustained per-link planning
number, **200 Gbps** a demonstrated peak.

**Per station:** a single satellite is in view of a given ground site for only a few minutes per
pass. A "hub" raises *station* throughput by **co-locating multiple optical terminals** (each its
own mount/telescope), each tracking a different satellite. With, say, 4–8 terminals at a hub, a
station can sustain on the order of **0.5–1.5 Tbps aggregate** when satellites are in view. This
is a real and sensible thing to "go big" on — **breadth (terminal count) per site, not aperture.**

**Per network:** a handful of diverse hubs (≥4, each multi-terminal) aggregates into the
**multi-Tbps** range. ESA's **HydRON** program explicitly targets **terabit/s-class** optical
space networks with a *core network of ground stations* feeding terrestrial fiber — a direct
analogue of the proposed architecture, and a sign the "fiber-connected optical hubs" model is
considered credible. (HydRON in-orbit demo: 2028–2029.)
([ESA HydRON](https://www.esa.int/Applications/Connectivity_and_Secure_Communications/HydRON_Satellites_using_lasers_for_faster_data_sharing))

**Does this match an inference data center's needs?** Almost certainly yes — with room to spare:

- **Inference is bandwidth-light vs. training.** Training shuffles petabytes of gradients/weights.
  Inference is request → response: a text prompt is kilobytes; a generated response is typically
  **kilobytes to a few megabytes**; even image/video generation outputs are megabytes, not
  gigabytes. Inference throughput is **memory-bandwidth-bound *inside* the GPU box**, not
  network-bound at the data-center boundary. ([Databricks — LLM inference performance](https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices))
- **Order-of-magnitude:** at, say, ~10 kB per response, **100 Gbps ≈ ~1.2 million responses/sec**
  through a single link. A multi-Tbps network is comfortably oversized for inference *volume*.

So the ground network is **unlikely to be the throughput bottleneck** for an inference data center.
The genuine constraints are (a) **availability** — covered only by site diversity, §3 — and
(b) **latency variability**: handing a customer off between geographically scattered hubs as
satellites and weather change introduces jitter. For latency-sensitive interactive inference, that
jitter, not raw bandwidth, is the thing to engineer around.

---

## 6. Cost & Feasibility — Is "Monster Hub + Fiber" Practical?

**Cost datapoints (validated, multi-source where possible):**

- **Heriot-Watt HOGS:** **£2.5M (~$3.3M)** for a 0.7 m AO-equipped, single-photon-class station
  (QKD-grade — i.e. high end of the sub-meter class). ([Laser Focus World](https://www.laserfocusworld.com/quantum/article/55234082/optical-ground-stations-push-boundaries-of-space-technology))
- **Cailabs / DataPath:** an agreement valued **up to ~$61M for ~12+ transportable OGS units** —
  i.e. roughly **$3–5M per production-class commercial OGS** at modest scale.
  ([Via Satellite](https://www.satellitetoday.com/technology/2025/12/15/cailabs-partners-with-datapath-to-build-transportable-optical-ground-stations/),
  [Payload](https://payloadspace.com/cailabs-lands-e57m-to-up-optical-ground-station-capacity/))
- **Telescope cost scaling:** monolithic telescope cost scales as roughly **aperture^2.5**. A 5 m
  comms telescope is therefore an astronomical-observatory-class project — order **$50–150M+** for
  the telescope and dome alone, before AO and detectors — for only a few dB over a 1 m unit.
  ([arXiv — telescope cost scaling](https://arxiv.org/abs/2107.09605))
- *FLAGGED ESTIMATE:* a high-capability **multi-terminal hub** (4–8 sub-meter terminals, shared
  AO, single-photon/coherent receivers, fiber backhaul, building) plausibly runs **~$20–60M**
  per site — extrapolated from the per-unit figures plus site/integration overhead; not a quoted
  number.

**Feasibility of the "monster hub + fiber to customers" model:**

- ✅ **Fiber-connect customers to hubs:** sound. Customers should *not* each operate a laser
  terminal; consolidating the optical link at professionally run hubs and backhauling over
  terrestrial fiber is the right call (this is exactly the ESA HydRON / SSC NODES philosophy).
- ✅ **"Capable" hubs:** sound — multiple terminals, top-grade AO, single-photon/coherent
  receivers per site.
- ❌ **"One monster telescope":** not sound. Don't spend capital on a giant aperture; the physics
  caps the payoff and weather ignores it entirely.
- ⚠️ **"A *few* hubs":** acceptable **only if "few" ≥ 4 and they are >1,000 km apart in
  anti-correlated climates.** For 99.9% you need ~10–12 sites. If "few" means 1–3, the model
  fails on availability.
- ⚠️ **Industry-wide,** the optical ground segment is the current bottleneck ("downlink deficit,"
  ~10% of needed infrastructure built). Real estate, fiber backhaul, and dozens of stations are
  a multi-billion-dollar industry-level capex problem — though a *single operator* serving its
  own constellation needs only its own ~4–12 site network, which is far more tractable
  (order **$100–500M** for the ground segment — *FLAGGED ESTIMATE*).

**Recommended architecture:** **4–12 geographically diverse hub stations**, each with **multiple
0.6–1.0 m terminals** (not one giant telescope), full adaptive optics, single-photon or coherent
receivers, high-power multi-sub-aperture uplink transmitters, and **terrestrial-fiber backhaul** to
customers. Spend on **site count and terminal count**, not aperture.

---

## Sources

- [NASA — Fastest Space-to-Ground Laser Comms Link (TBIRD 200 Gbps)](https://www.nasa.gov/centers-and-facilities/goddard/nasa-partners-achieve-fastest-space-to-ground-laser-comms-link/)
- [NASA NTRS — Operations and Results from the 200 Gbps TBIRD Mission (PDF)](https://ntrs.nasa.gov/api/citations/20230007959/downloads/TBIRD-smallsat-2023.pdf)
- [NASA — Getting NASA Data to the Ground With Lasers (LCRD OGS-1/OGS-2)](https://www.nasa.gov/technology/getting-nasa-data-to-the-ground-with-lasers/)
- [NASA Goddard ESC — Laser Communications Relay Demonstration (LCRD)](https://esc.gsfc.nasa.gov/projects/LCRD/?tab=overview)
- [Wikipedia — ESA Optical Ground Station](https://en.wikipedia.org/wiki/ESA_Optical_Ground_Station)
- [ESA — Optical Ground Station (OGS)](https://www.esa.int/Enabling_Support/Space_Engineering_Technology/Space_Optoelectronics/Optical_Ground_Station_OGS)
- [JPL — Deep Space Optical Communications (DSOC) press kit](https://www.jpl.nasa.gov/press-kits/psyche/dsoc/)
- [NASA — DSOC Streams First Video From Deep Space via Laser (267 Mbps)](https://www.nasa.gov/directorates/stmd/tech-demo-missions-program/deep-space-optical-communications-dsoc/nasas-tech-demo-streams-first-video-from-deep-space-via-laser/)
- [JPL — Table Mountain DSOC laser beacon (uplink transmitter)](https://www.jpl.nasa.gov/images/pia26661-table-mountain-facility-sends-dsoc-laser-beacon-to-nasas-psyche-infrared-image/)
- [Cailabs — Optical Ground Stations (TILBA-OGS)](https://www.cailabs.com/aerospace-defense/laser-communications/optical-ground-stations/)
- [Via Satellite — Cailabs/DataPath Transportable Optical Ground Stations](https://www.satellitetoday.com/technology/2025/12/15/cailabs-partners-with-datapath-to-build-transportable-optical-ground-stations/)
- [Payload — Cailabs €57M for OGS capacity](https://payloadspace.com/cailabs-lands-e57m-to-up-optical-ground-station-capacity/)
- [Safran — IRIS Optical Ground Station](https://www.safran-group.com/products-services/iris-optical-ground-station-space-laser-communications)
- [SSC — ESA contract for optical ground network (NODES)](https://sscspace.com/ssc-awarded-1-1me-contract-by-esa-for-optical-ground-network/)
- [DLR — Optical Satellite Downlinks to OGS and HAPs (diversity, PDF)](https://elib.dlr.de/55548/1/OLEO-DL_to_OGS_and_HAPs-IST07.pdf)
- [arXiv — Performance Analysis of Optical Ground Station Network Configurations](https://arxiv.org/html/2410.23470v2)
- [SatNews — The Downlink Deficit (Apr 2026)](https://satnews.com/2026/04/03/the-downlink-deficit-the-pentagons-optical-mesh-network-and-the-terrestrial-bottleneck/)
- [Nature — 100 Gbps coherent free-space optical at LEO tracking rates](https://www.nature.com/articles/s41598-022-22027-0)
- [PMC — Tbit/s line-rate satellite feeder links with full adaptive optics](https://pmc.ncbi.nlm.nih.gov/articles/PMC10282091/)
- [MDPI — Atmospheric Pre-Compensation with Adaptive Optics: A Field Review](https://www.mdpi.com/2304-6732/10/7/858)
- [DLR — Adaptive Optics pre-compensated laser uplink to LEO (PDF)](https://elib.dlr.de/140930/1/oe-29-4-6113.pdf)
- [ESA — HydRON: Satellites using lasers for faster data sharing](https://www.esa.int/Applications/Connectivity_and_Secure_Communications/HydRON_Satellites_using_lasers_for_faster_data_sharing)
- [arXiv — Scaling Relationship Between Telescope Cost and Aperture Size](https://arxiv.org/abs/2107.09605)
- [Laser Focus World — Optical ground stations push boundaries (HOGS cost)](https://www.laserfocusworld.com/quantum/article/55234082/optical-ground-stations-push-boundaries-of-space-technology)
- [Databricks — LLM Inference Performance Engineering](https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices)
- [eoPortal — TBIRD mission](https://www.eoportal.org/satellite-missions/tbird)

## Open Questions

1. **Optimal hub count and terminal-per-hub for a specific SSO constellation.** The 4 (→99%) /
   10–12 (→99.9%) figures are general; the exact number depends on the data center's orbit,
   constellation size, target availability, and chosen site climates. Needs a constellation-
   specific contact/weather simulation.
2. **Uplink rate ceiling.** Downlink demos reach 100–200 Gbps; sustained high-rate *uplink*
   through turbulence is less mature. What's the realistic per-link uplink rate, and does it
   constrain prompt ingest at scale? (Likely fine for bandwidth-light inference, but unverified.)
3. **Latency / handoff jitter.** Geographic site diversity means customer traffic is handed
   between hubs as weather and satellite geometry change. Quantify the latency variance and
   whether it's acceptable for interactive inference SLAs.
4. **Hub capex precision.** The ~$20–60M/hub and ~$100–500M/network figures are flagged
   estimates extrapolated from sub-meter-unit pricing. A vendor quote (Cailabs, Safran) for a
   multi-terminal AO hub would tighten this materially.
5. **Single-photon vs. coherent receivers at scale.** TBIRD-style direct-detection vs.
   coherent/SMF-coupled receivers have different cost, AO demands, and rate ceilings. Which
   architecture best fits a high-throughput inference hub is unresolved here.
6. **Regulatory / eye-safety / airspace** for high-power (kW-class) ground uplink lasers at
   multiple sites — not researched in this pass.
