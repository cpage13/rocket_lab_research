# Competitors — Orbital Data Centers

> Status: **deep-research pass** — completed 2026-05-17. Facts cross-checked
> against 2+ sources where possible; rumor/estimate vs. confirmed flagged inline.

## Summary

**Starcloud** (Redmond, WA; founded Jan 2024 as "Lumen Orbit") is the most
advanced pure-play orbital data center company and the closest analogue to our
thesis. It has flown hardware (Starcloud-1, an NVIDIA H100, ~Nov 2025), raised a
**$170M Series A** (March 2026, led by Benchmark + EQT Ventures) at a **~$1.1B
valuation**, and has a clearly articulated technical roadmap.

The single most important finding for our planning: **Starcloud's serious
commercial product, Starcloud-3, is explicitly designed around SpaceX Starship.**
It is a ~3-tonne, 200 kW spacecraft sized to fit Starship's "PEZ dispenser"
deployment system, with a target launch window of **2028–2029**. Starcloud's
own economics depend on Starship reaching **~$500/kg** launch cost. Their
near-term Starcloud-1/-2 missions are demonstrators, not the business. **The
business case is gated on Starship-class lift.** This is the central strategic
fact a Neutron-based (~8–13 t) approach must reckon with.

On **thermal**: Starcloud relies entirely on **passive radiative cooling** —
rejecting heat as infrared into deep space (no fans, no convection possible in
vacuum). Starcloud-1 used an ISS-derived heat-rejection system; scale-up
requires large **deployable radiators**. Multiple independent analyses call
thermal management — not power or compute — the *primary launch-mass-limiting
factor* for orbital data centers at scale.

---

## 1. Starcloud's technical architecture

### Satellite / spacecraft design

| Mission | Status | Payload | Power | Mass | Launcher |
|---|---|---|---|---|---|
| **Starcloud-1** | Flown ~Nov 2025 | 1× NVIDIA H100 GPU | ~few kW (small) | ~60 kg / ~130 lb | SpaceX rideshare (Falcon 9) |
| **Starcloud-2** | Planned, before end of 2026 | NVIDIA Blackwell (B200-class), AWS server blade, Crusoe cloud module, a bitcoin-mining computer; ~100× Starcloud-1 power | ~100× S-1 (tens of kW range — *estimate*) | larger | SpaceX |
| **Starcloud-3** | In development; target launch **2028–2029** | "Hypercluster"-class GPU cluster | **200 kW** (confirmed) | **~3 tonnes** (confirmed) | **SpaceX Starship**, via PEZ dispenser |
| **Long-term vision** | Aspirational | — | **5 GW** | — | Starship fleet |

- **Orbit:** Sun-synchronous orbit (SSO), **~500–600 km altitude**. SSO is chosen
  so the satellite can sit in **near-continuous sunlight** ("dawn-dusk" SSO),
  minimizing eclipse and giving a >95% solar capacity factor. (Confirmed across
  white paper + multiple analyses.)
- **5 GW endgame:** Starcloud describes an eventual single facility with solar
  and radiator panels roughly **4 km × 4 km (~16 km²)**. This is a long-range
  vision, not a funded program — treat as aspirational.

### Power generation

- Large deployable **solar arrays**. Claimed advantages: **~40% higher solar
  irradiance** than ground panels (no atmospheric attenuation) and **>95%
  capacity factor** in dawn-dusk SSO vs. a ~24% median for US terrestrial solar
  farms. (Confirmed — white paper and corroborating coverage.)
- No batteries / backup generators / grid interconnect needed in the
  perpetual-sunlight orbit — a stated cost advantage over terrestrial buildout.

### Thermal / cooling approach — **the key technical question**

- **Method: passive radiative cooling.** In vacuum there is no air for
  convection and no water for evaporative cooling. Heat from the GPUs must be
  carried to **radiator panels** and emitted as **infrared radiation** into deep
  space (effective sink temperature ~3 K / cosmic microwave background, ~−270°C).
- **Starcloud-1** used a heat-rejection system **adapted from ISS technology**
  (the ISS uses pumped-ammonia loops to deployable radiators). (Confirmed.)
- **Scale-up requires large deployable radiators.** This is repeatedly
  identified — by external analysts, not just critics — as the **binding
  constraint**:
  - Radiated power scales with the *fourth power* of radiator temperature
    (Stefan–Boltzmann). Rejecting **1 MW** of heat at a comfortable ~20°C silicon
    temperature needs **~1,200 m²** of radiator ("four tennis courts"). Running
    hotter (~60°C) roughly halves the area but stresses the silicon.
  - Unlike thin-film roll-out solar arrays, **radiators do not stow compactly**;
    current designs have poor mass/volume packing density. One analysis
    estimates a 40 MW-class system's radiators alone could need **9–16 Starship
    launches**. (*Estimate / external analysis — flag as contested.*)
  - Counterpoint (also external): at the **~100 kW** scale of Starcloud-3,
    radiators are only ~10–20% of spacecraft mass and ~7% of planform area —
    solar arrays dominate. At that scale cooling is "an engineering trade-off,
    not a hard physics blocker." The thermal wall bites hardest at the
    multi-MW-to-GW scale.
- **Net read:** Starcloud's thermal approach is conventional (radiative) and
  proven at small scale; the open risk is whether deployable radiators can scale
  with mass/packing efficiency anywhere close to solar arrays. This is the
  single most cited barrier to the GW-scale vision.

### Communications

- **Optical / laser links.** Satellites carry **Optical Inter-Satellite Links
  (OISL)** — laser terminals for gigabit-class satellite-to-satellite mesh
  networking. Starcloud also emphasizes **direct satellite-to-ground** optical
  links, bypassing terrestrial networks (pitched as a cybersecurity / data-
  sovereignty advantage). (Confirmed across multiple sources.)
- Ground-link capacity is a latent constraint for data-heavy workloads, which
  is part of why Starcloud positions around workloads that are compute-heavy but
  not bandwidth-heavy (training, batch inference, on-orbit data processing).

### Scale roadmap

Demonstrator (S-1, single H100) → multi-vendor testbed (S-2, Blackwell + AWS +
Crusoe) → first commercial product (**S-3, 200 kW, Starship-launched,
2028–2029**) → "Hypercluster" clusters → 5 GW facility (aspirational).

---

## 2. Business proposition

- **Two-phase go-to-market** (per company statements):
  1. **Near term:** sell **inference-as-a-service** to Earth-observation
     constellation operators, including **US DoD and NASA** customers — run AI
     inference on satellite imagery *in orbit* so only results are downlinked.
     Starcloud has cited running inference on **Capella Space** SAR imagery.
  2. **Longer term:** sell **H100/Blackwell GPU capacity for AI training and
     inference** to cloud providers — competing with the likes of CoreWeave and
     Lambda, and selling into AWS / Azure / cloud brokers.
- **Training vs. inference:** Starcloud markets *both*. Starcloud-1 claimed the
  "first LLM trained in space," first in-orbit inference (a Gemini variant), and
  first on-orbit fine-tuning. Practically, **latency-tolerant, compute-bound
  workloads** (training, batch/async inference, EO data processing) fit the
  orbital model best; real-time low-latency inference does not.
- **Stated advantages over terrestrial:**
  - "Free" 24/7 solar power (no fuel, no grid, ~40% more irradiance).
  - "Free" cooling — deep space as an infinite heat sink (no water, no
    chillers).
  - No land acquisition, no multi-year permitting (terrestrial DC buildout
    cited at 18–24 months *plus* permitting up to a decade).
  - Scales independently of terrestrial grid/land constraints; targets the
    "marginal" AI compute that can't be built fast enough on Earth.
- **Pricing:** No public price list. Starcloud's stated target is
  **~$0.05/kWh** energy cost for Starcloud-3 — roughly at parity with
  hyperscaler power-purchase agreements — and a claimed **~10× reduction in the
  energy cost of inference** at scale. *These are company projections, not
  demonstrated.* The investor thesis (Benchmark) is explicitly: "the cost of
  power on Earth is rising faster than the cost of launch is falling."

---

## 3. Stated barriers and the central bet — **launch vehicle**

**Confirmed:** Starcloud's commercial spacecraft, **Starcloud-3, is designed
specifically for SpaceX Starship.** It is sized (~3 t, 200 kW) to fit the
Starship **"PEZ dispenser"** — the deployer SpaceX built for Starlink V2. Target
launch: **2028–2029**.

**The economic bet:** Starcloud's cost model crosses into competitiveness when
Starship reaches **~$500/kg** launch cost. (Some analyses note the break-even
moves toward ~$1,000/kg as terrestrial land/power costs rise.) Starship has
**not yet demonstrated** $500/kg or routine heavy-lift cadence — so the business
case rests on a launch-cost assumption that is not yet proven.

**Implied constraint chain:** mass is the binding economic variable → cheap
mass-to-orbit requires Starship-class lift → therefore Starcloud's
*commercially serious* architecture is unavoidably coupled to Starship.

**Comparison to Neutron (~8–13 t to LEO):**
- A single Starcloud-3 spacecraft (~3 t) is **well within Neutron's payload
  class** — Neutron could physically launch a 200 kW-class orbital DC node.
- The gap is **not per-launch capability — it is $/kg and cadence.** Starcloud's
  GW-scale vision assumes a high-cadence, very-low-$/kg Starship fleet.
- **Implication for a Neutron-based thesis:** A Neutron approach is
  *most defensible if it targets the 100 kW–single-MW node class* (one
  spacecraft per launch — EO-inference and government/sovereign-compute
  customers) rather than competing on GW-scale hyperscale training, which is
  where Starship-economics dominate. The thermal analyses reinforce this:
  cooling is "an engineering trade-off, not a physics blocker" at ~100 kW, but
  becomes the launch-mass wall at multi-MW/GW scale. Neutron's niche is the
  scale where cooling is tractable and a single launch delivers a whole node —
  i.e., compete on *time-to-orbit and node-level service*, not on raw $/kg
  against Starship.

---

## 4. Recent news (2025–2026)

- **Nov 2025:** Starcloud-1 launched (SpaceX rideshare); first NVIDIA H100 in
  space. Reported industry firsts: first AI model trained in orbit, first
  in-orbit inference (Gemini variant), first on-orbit fine-tuning. (Confirmed,
  multiple sources; "firsts" are company claims.)
- **Dec 2025:** CNBC and others cover the "first AI model trained in space"
  milestone as the orbital DC race heats up.
- **Feb 3, 2026:** FCC filing for a constellation of up to **88,000 satellites**
  for orbital data centers. (Confirmed.)
- **March 30, 2026:** **$170M Series A** (Benchmark lead + EQT Ventures);
  **~$1.1B valuation**; ~$200M raised total; "fastest YC unicorn" (~17 months
  post-demo-day). Announced: a new **manufacturing facility** for Starcloud-3
  and headcount growth from ~13 to ~50 by end-2026. Confirmed multi-vendor
  payloads on **Starcloud-2** (NVIDIA Blackwell, AWS server blade, Crusoe cloud
  module, a bitcoin miner).
- **Roadmap update:** Starcloud-3 (Starship, ~3 t, 200 kW) formally added to the
  roadmap alongside the Series A.
- **White paper:** "Why we should train AI in space" (originally published
  ~Sept 2024 under the old name "Lumen Orbit") — still the foundational public
  document for the economics (solar capacity factor, ~$500/kg break-even,
  radiative cooling).

---

## 5. Other players (brief)

- **Google — Project Suncatcher.** Research "moonshot" to scale ML compute in
  space using solar-powered satellite constellations carrying **Google TPUs**
  (Trillium / v6e) linked by free-space optical links. Google has proton-beam
  radiation-tested Trillium TPUs and found them "surprisingly radiation-hard"
  (no hard failures to ~15 krad(Si)). Design concept: **81-satellite clusters
  in a ~1 km-radius formation**. First step is a **learning mission with Planet
  Labs — two prototype satellites targeted for early 2027**. Well-capitalized,
  research-stage; not yet a commercial product.

- **Aetherflux (now rebranded "Cowboy Space Corporation," May 2026).** Founded
  by Baiju Bhatt (Robinhood co-founder); raised a **$50M Series A** (April).
  Origin is **space-based solar power** — beaming energy from LEO to ground via
  infrared lasers — and it has expanded into orbital compute with the **"Galactic
  Brain"** project: first LEO compute node targeted for **Q1 2027**, scaling to
  thousands of satellites. Approach emphasizes continuous solar power +
  radiative cooling; the May 2026 rebrand signals expansion into in-orbit
  compute and launch.

- **Aethero.** Not a data-center company — an **edge-compute hardware** vendor.
  Builds space-rated AI compute modules (**NxN** on NVIDIA Jetson Orin NX;
  newer **NxA** on Jetson AGX Orin, up to ~550 TOPS, with a Jetson AGX
  Thor option up to ~4,000 TOPS). Strategy is **radiation-hardening-by-system-
  design** (radiation-tolerant COTS silicon + checkpointing, ECC, scrubbing),
  partnering with Cosmic Shielding (physical shielding) and Antmicro
  (open-source software stack). Relevant as a **supplier/reference point** for
  rad-tolerant on-orbit compute, not a direct orbital-DC competitor.

---

## What this means for our Neutron thesis

1. **Starcloud's real product needs Starship; ours doesn't have to.** Their
   commercial spacecraft (S-3) is Starship-coupled and gated on unproven
   ~$500/kg economics and ~2028–2029 timing. A Neutron-class node (~3 t, 200 kW
   fits comfortably in Neutron's 8–13 t envelope) can fly *one complete data
   center node per launch* — sooner, on a vehicle that is closer to operational.

2. **Pick the scale where physics is on our side.** External thermal analyses
   converge: at ~100 kW, radiative cooling is a manageable engineering
   trade-off; at multi-MW/GW it becomes the launch-mass wall. A Neutron thesis
   should target the **100 kW–~1 MW node class** and avoid competing with
   Starship economics on GW-scale hyperscale training.

3. **The defensible customer is government / EO / sovereign compute.** This is
   exactly Starcloud's *phase-1* market (DoD, NASA, EO operators like Capella).
   It values security, data sovereignty, and time-to-orbit over raw $/kWh — and
   rewards a vehicle that can deliver a node fast.

4. **Compete on cadence and time-to-orbit, not $/kg.** We will not beat Starship
   on launch cost. We can potentially beat Starship-dependent competitors on
   *schedule* and on delivering turnkey node-scale capacity now.

5. **Thermal is the shared hard problem.** Whatever the launcher, deployable
   radiator mass/packing efficiency is the key technical risk. Any Neutron
   architecture should treat radiator design as a first-order subsystem, and
   node sizing should be set by what one Neutron launch can cool, not just power.

---

## Sources

- [GeekWire — Starcloud $1.1B valuation](https://www.geekwire.com/2026/orbital-ai-seattle-area-startup-starcloud-hits-1-1b-valuation-to-build-space-based-data-centers/)
- [Starcloud (company site)](https://www.starcloud.com/)
- [Starcloud-1 page](https://www.starcloud.com/starcloud-1)
- [Starcloud-2 page](https://www.starcloud.com/starcloud-2)
- [Starcloud white paper — "Why we should train AI in space"](https://starcloudinc.github.io/wp.pdf)
- [Y Combinator — Starcloud](https://www.ycombinator.com/companies/starcloud)
- [TechCrunch — Starcloud $170M Series A](https://techcrunch.com/2026/03/30/starcloud-raises-170-million-series-ato-build-data-centers-in-space/)
- [TechCrunch — Why the economics of orbital AI are so brutal](https://techcrunch.com/2026/02/11/why-the-economics-of-orbital-ai-are-so-brutal/)
- [SpaceNews — Starcloud achieves unicorn status](https://spacenews.com/starcloud-achieves-unicorn-status-with-170-million-raise-for-orbital-data-centers/)
- [Wikipedia — Starcloud](https://en.wikipedia.org/wiki/Starcloud)
- [Via Satellite — Starcloud $170M](https://www.satellitetoday.com/finance/2026/03/30/starcloud-raises-170m-to-fund-orbital-data-center-plans/)
- [Data Center Dynamics — Starcloud Series A](https://www.datacenterdynamics.com/en/news/space-data-center-company-starcloud-secures-170-million-series-a/)
- [NVIDIA Blog — How Starcloud Is Bringing Data Centers to Outer Space](https://blogs.nvidia.com/blog/starcloud/)
- [CNBC — Starcloud trains first AI model in space](https://www.cnbc.com/2025/12/10/nvidia-backed-starcloud-trains-first-ai-model-in-space-orbital-data-centers.html)
- [GeekWire — Starcloud plans its next power plays](https://www.geekwire.com/2025/starcloud-power-training-ai-space/)
- [SatNews — The "Physics Wall": orbiting data centers face a cooling challenge](https://satnews.com/2026/03/17/the-physics-wall-orbiting-data-centers-face-a-massive-cooling-challenge/)
- [Intelligent Living — Are Data Centers in Space Actually Feasible? The Three Real Bottlenecks](https://www.intelligentliving.co/data-centers-space-starcloud-bottlenecks/)
- [SpaceComputer blog — Cooling for Orbital Compute: A Landscape Analysis](https://blog.spacecomputer.io/cooling-for-orbital-compute/)
- [Scientific American — Space-Based Data Centers Could Power AI with Solar Energy](https://www.scientificamerican.com/article/data-centers-in-space/)
- [Fierce Network — Space data centers: Starcloud, SpaceX and Project Suncatcher explained](https://www.fierce-network.com/cloud/space-data-centers-starcloud-spacex-and-project-suncatcher-explained)
- [Sequoia — podcast with Philip Johnston (Starcloud)](https://sequoiacap.com/podcast/greetings-earthlings-philip-johnston-of-starcloud-on-data-centers-in-space/)
- [Google Research — Exploring a space-based, scalable AI infrastructure system design](https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design/)
- [Google Blog — Project Suncatcher](https://blog.google/technology/research/google-project-suncatcher/)
- [DCD — Project Suncatcher / Planet Labs partnership](https://www.datacenterdynamics.com/en/news/project-suncatcher-google-to-launch-tpus-into-orbit-with-planet-labs-envisions-1km-arrays-of-81-satellite-compute-clusters/)
- [SpaceNews — Aetherflux enters orbital data center race](https://spacenews.com/space-based-solar-power-startup-aetherflux-enters-orbital-data-center-race/)
- [Via Satellite — Aetherflux rebrands as Cowboy Space](https://www.satellitetoday.com/finance/2026/05/11/aetherflux-rebrands-as-cowboy-space-expanding-plans-to-in-orbit-compute-and-launch/)
- [DCD — Aetherflux orbital data center operational by Q1 2027](https://www.datacenterdynamics.com/en/news/aetherflux-orbital-data-center-to-be-operational-by-q1-2027/)
- [SpaceNews — Cosmic Shielding works with Aethero on Jetson Orin NX](https://spacenews.com/cosmic-shielding-works-with-aethero-to-protect-nvidia-jetson-orin-nx-gpu/)
- [Antmicro — supports Aethero NxN and NxA space computers](https://antmicro.com/blog/2026/03/antmicro-supports-aethero-with-nxn-and-nxa-space-computers)
- [Wikipedia — Space-based data center](https://en.wikipedia.org/wiki/Space-based_data_center)

## Open questions

- **Starcloud-3 radiator design:** What deployable radiator architecture and
  areal mass density does Starcloud actually assume for the 200 kW spacecraft?
  Not publicly disclosed; this drives the whole mass budget.
- **Actual Starcloud-1 results:** The "firsts" (LLM trained, fine-tuning) are
  company claims — what was the scale (model size, throughput, thermal
  performance, uptime)? No independent verification found.
- **Eclipse / battery strategy:** Even dawn-dusk SSO has some eclipse near
  solstices. How much battery mass does Starcloud carry, and does the "no
  batteries" claim hold for S-3?
- **GPU lifetime in orbit:** Radiation degradation and the hot-radiator vs.
  silicon-longevity trade-off — what replacement/servicing cadence is assumed?
- **Downlink bottleneck:** Optical ground-link capacity vs. workload data
  volumes — quantified ground-segment plan is not public.
- **Starship dependency timing:** If Starship $500/kg slips past 2029, what is
  Starcloud's fallback launch path — and does that open a window for a
  Neutron-class entrant?
- **Pricing:** No public $/GPU-hour or $/kWh figure beyond the projected
  ~$0.05/kWh energy-cost target — real customer pricing unknown.
