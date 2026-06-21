# Laser (Optical) Direct Data-Center-to-Data-Center Links, an Independent Early-Application Market, Viability

*Research date: June 2026. Communications research-wiki effort (shared library).*
*Side track to the RF consumer model. This is the laser (optical) point-to-point market, NOT part of the direct-to-cell / home-broadband RF spine.*

Builds on / does not duplicate (read these first):
- [`research/laser_comms/laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md), the terrestrial FSO product class, Taara, the weather wall, the security differentiator, the incremental-value framing (laser wins where fiber is absent; conditional value where fiber exists), and the vendor landscape. **That doc already opened the data-center-interconnect question and flagged it as "nascent / aspirational."**
- [`research/laser_comms/optical_comms.md`](optical_comms.md), ISL + space-to-ground physics, the 1550 nm optical C-band, Starlink's laser mesh, NASA TBIRD 200 Gbps.
- [`research/laser_comms/optical_ground_stations.md`](optical_ground_stations.md), the ground segment, aperture physics, site-diversity-not-size.
- [`research/laser_comms/comms_business_case.md`](comms_business_case.md), the broad space-comms business (sovereignty, resilience, latency) and the orbital-data-center tie-in.

**This doc's job:** sharpen the one question the existing corpus left open, *is there a real direct laser DC-to-DC (and enterprise point-to-point) market, how would it work, and who pays?* It adds the new material the prior docs do not cover: the **AI-buildout demand engine** (distributed training across gigawatt campuses, the dark-fiber land rush), and the **hard bandwidth-scale reckoning** that decides where laser can and cannot play. No verdict on the Rocket Lab business is drawn here; this is a neutral source doc.

---

## Summary / Verdict

**The established baseline, stated plainly:** laser is **proven and standard for satellite-to-satellite inter-satellite links** (Starlink runs ~27,000 space lasers moving 42+ PB/day, see [`optical_comms.md`](optical_comms.md)); **RF is the space-to-ground workhorse** (all-weather, cheap terminals); and **no one puts a laser on a phone** (a laser needs precise line-of-sight pointing, the opposite of a handset). The question here is the narrow terrestrial-and-orbital point-to-point case: *direct laser links between data centers.*

**Verdict: there is a real but narrow market, and it is NOT the headline AI-interconnect job.** The shape, in five findings:

1. **The demand engine is real and large: the AI buildout has turned data-center-to-data-center interconnect (DCI) into a first-order problem.** AI labs now train single models across **multiple gigawatt-scale campuses** because no single site can get the power. Google's paired campuses sit ~15 to 50 miles apart; Microsoft/OpenAI are explicitly building to interconnect campuses across the country [FACT]. A dark-fiber "land rush" is underway (Big Fiber raised **$250M** in May 2026 to build AI-DCI routes; AI has "overtaken traditional telecom as the primary growth engine for optical fiber") [FACT]. This is a genuinely new, fast-growing interconnect market that the prior docs did not size.

2. **But the headline AI-DCI job needs petabit-scale capacity, and that disqualifies free-space optics for it.** The bandwidth required between AI campuses is **~5 Pbit/s within a region and ~1 Pbit/s between regions** [FACT, single-source: SemiAnalysis], met by trenching **thousands of fiber pairs** (each pair carrying **up to ~121.6 Tbps** via DWDM, 800G x 152 wavelengths) [FACT]. A commercial free-space-optical link (Taara Beam) carries **~25 Gbps per beam** [FACT]. Matching a single fiber pair would take **~4,900 laser beams**; matching the 5 Pbit/s campus-to-campus number would take **~200,000 beams** [DERIVED]. Free-space optics is **two-to-five orders of magnitude short** of the synchronous-training interconnect and cannot be the primary path for it.

3. **The distances, however, are exactly in laser's wheelhouse, so the disqualifier is bandwidth, not reach.** Synchronous training that tolerates ~1 ms inter-site latency is physically confined to roughly a **100 km radius** (fiber adds ~4.9 microseconds/km; 100 km is ~0.49 ms one-way) [FACT]. Paired AI campuses sit at campus (~2 km) to metro (~120 km) scale [FACT]. A Taara Beam reaches **up to ~25 km** [FACT] and the FSO class spans a few hundred metres to ~20 km, squarely inside the paired-campus band. So laser *can* span the right distance; it just cannot carry the petabit load over it.

4. **The real terrestrial laser DC niche is therefore the same narrow set the prior doc identified, now sharpened for AI campuses:** **(a) gap-fill** where fiber to a new AI site is months away (deploy in hours, "dark fiber in the sky"); **(b) route-diversity / redundancy**, a lower-bandwidth secondary or tertiary path (the AI buildout explicitly demands "tri-versity / quad-versity" routing); **(c) the over-an-obstacle hop** (river, rail, highway, property line) between nearby buildings; and **(d) security / fast-deploy / no-license** specialty links. In every one of these, laser is a **supplement measured in tens of Gbps**, not the petabit backbone. Note its direct competitor in this niche is not only fiber but also **millimeter-wave / microwave wireless DCI** (also multi-Gbps, also weather-limited), which competes with FSO for the same redundancy slot rather than displacing fiber.

5. **Where direct laser DC-to-DC genuinely wins outright is the case with no fiber option at all: orbital data-center to orbital data-center (and DC-to-ground from orbit).** In space there is no trench to dig and no fiber to lose to; laser ISLs are the *only* credible medium, are proven at scale, and the 2026 market has already fused orbital compute with orbital optical relay (Axiom + Kepler; SpaceX's compute-and-connectivity mesh; Google's Project Suncatcher TPU constellation) [FACT, see [`comms_business_case.md`](comms_business_case.md)]. This is the one place the "direct laser link between data centers" story is not a niche supplement but the load-bearing architecture, and it is the natural home for Rocket Lab's Mynaric optical-terminal asset.

**Bottom line:** a direct laser DC-to-DC / enterprise point-to-point market exists and is real, but on the ground it is a **specialty supplement** (gap-fill, redundancy, obstacle-hop, secure fast-deploy), explicitly **not** the petabit AI synchronous-training interconnect, which belongs to trenched coherent fiber. The one arena where direct laser links between data centers are the primary, winning architecture is **in orbit**, where fiber is not an option. A pitch that says "laser replaces fiber for AI-DCI" is false on bandwidth; a pitch that says "laser is a fast-deploy redundant/gap-fill terrestrial supplement, and the primary interconnect for orbital data centers" is supportable. **Confidence: high** on the bandwidth-scale disqualification and the distance physics (multiple independent, current sources); **medium-high** on the narrow-niche framing (analytical synthesis on sourced inputs); **medium** on terrestrial market size (wide analyst spread, mixed scope, see [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) COMM-010).

---

## 1. The new demand engine: the AI buildout makes DCI a first-order problem

The prior docs treated terrestrial laser as a general connectivity tool. What has changed in 2025 to 2026, and what makes the DC-to-DC question worth its own analysis, is that **AI training has made data-center-to-data-center interconnect a primary bottleneck**, distinct from ordinary enterprise DCI.

**Why AI forces distributed, multi-campus builds.** No single site can secure the power a frontier training run now wants, so AI labs spread one logical training job across multiple physical campuses:

- Google already runs multi-region training; Microsoft and OpenAI are "constructing ultra-dense liquid-cooled datacenter campuses approaching the Gigawatt-scale" and "plan to interconnect various ultra large campuses together and run giant distributed training runs across the country" [FACT] ([SemiAnalysis](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais), [Data Centers Inc](https://www.datacenters.com/news/ai-training-clusters-are-reaching-1-gw-infrastructure-scale)).
- Multi-data-center training is already in production: it was used for **GPT-4.5 and Gemini-1.5** [FACT] ([SemiAnalysis](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais), [arXiv 2507.07765](https://arxiv.org/pdf/2507.07765)).
- The interconnect, not the GPU, is increasingly the limit: "in many large deployments, network port density and optical component supply now limit cluster size more than GPU availability" [FACT] ([Towards AI](https://pub.towardsai.net/how-data-centers-actually-work-from-cooling-systems-to-gpu-clusters-a23918104762), [ADTEK](https://adtek-fiber.com/ai-data-center-interconnect-2026-cpo-optical-interconnect-and-deployment-challenges/)).

**The dark-fiber land rush is the market's response.** New fiber is being financed and trenched specifically for AI-DCI:

- **Big Fiber** secured a **$250M** debt facility (Stonepeak Credit + La Caisse, formerly CDPQ) in May 2026 to expand dark-fiber routes for AI, bringing its Atlanta + SF Bay Area footprint to **850 route miles / 3M+ fiber miles**, with new routes in the SF Bay Area, Hillsboro, and Atlanta tied to AI data-center expansion [FACT] ([PR Newswire](https://www.prnewswire.com/news-releases/big-fiber-secures-250-million-financing-led-by-stonepeak-credit-and-la-caisse-to-accelerate-digital-infrastructure-expansion-302775649.html), [Data Center Knowledge](https://www.datacenterknowledge.com/infrastructure/big-fiber-financing-signals-ai-s-next-infrastructure-land-rush)).
- AI demand "has overtaken traditional telecom as the primary growth engine for optical fiber and cable" (CRU Group, April 2026), tightening supply for high-density fiber and upstream preforms [FACT] ([Data Center Knowledge](https://www.datacenterknowledge.com/infrastructure/big-fiber-financing-signals-ai-s-next-infrastructure-land-rush), [IEEE ComSoc](https://techblog.comsoc.org/2026/05/19/big-fibers-250m-financing-deal-to-buildout-dark-fiber-routes-for-ai-data-center-expansion/)).
- The traffic is qualitatively different: AI "scale-up" traffic inside data centers generates **~504x more bandwidth** than traditional DCI flows (Cisco), and AI customers demand "extreme route diversity, often moving toward tri-versity or quad-versity networks," with networks "redesigned around persistent machine-to-machine synchronization" rather than enterprise traffic patterns [FACT, single-source: Big Fiber CCO via Data Center Knowledge] ([Data Center Knowledge](https://www.datacenterknowledge.com/infrastructure/big-fiber-financing-signals-ai-s-next-infrastructure-land-rush)).

**Why this matters for the laser question.** This is a real, large, fast-growing interconnect market with an explicit appetite for *route diversity and redundancy*, the two attributes a fast-deploy laser link can supply. The demand is genuine. The decisive question is whether laser can carry the load it implies. Section 2 shows it cannot, for the primary job.

---

## 2. The bandwidth-scale reckoning, the heart of the viability question

This is the new, decisive analysis. The prior doc noted FSO is "not a fiber replacement" qualitatively; here is the quantitative reason, grounded in AI-DCI's actual numbers.

### 2.1 What the AI-DCI job actually requires

| Interconnect tier | Bandwidth needed | Source |
|---|---|---|
| **Within a region** (campus-to-campus) | **~5 Pbit/s** between sites | [SemiAnalysis](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais) |
| **Between regions** | **~1 Pbit/s** | [SemiAnalysis](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais) |
| **Single DWDM fiber pair** (the building block) | **up to ~121.6 Tbps** (800 Gbps x 152 wavelengths) | [SemiAnalysis](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais) |
| **Per-wavelength coherent DCI today** | **800 Gbps** (OIF 800ZR, up to 80 km; 800LR to 10 km); **1.6T** coherent-lite for 2 to 20 km campus/metro | [Effect Photonics / OIF](https://effectphotonics.com/insights/data-center-interconnects-coherent-or-direct-detect/), [Marvell](https://www.marvell.com/blogs/macsec-for-scale-across-networking.html) |

The petabit figures are met by laying **thousands of fiber pairs**, where "most of the cost is in labor and equipment to dig up the trenches as opposed to the physical fiber" [FACT] ([SemiAnalysis](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais)). NVIDIA's Spectrum-XGS and Google's Cloud Interconnect both target petabit-per-second cross-DC fabrics (Google: 400 Gbps links scaling in 3.2 Tbps increments to petabit capacity) [FACT] ([NVIDIA](https://nvidianews.nvidia.com/news/nvidia-introduces-spectrum-xgs-ethernet-to-connect-distributed-data-centers-into-giga-scale-ai-super-factories), [Google Cloud](https://cloud.google.com/blog/products/networking/data-center-and-global-networks-built-for-ai-era)).

### 2.2 What free-space optics delivers

| FSO option | Per-link capacity | Status | Source |
|---|---|---|---|
| **Taara Beam** (commercial, shipping 2026) | **~25 Gbps** per beam, up to ~25 km | Product | [Tom's Hardware](https://www.tomshardware.com/tech-industry/optical-transceiver-achieves-up-to-25-gbps-throughput-with-ultra-low-latency-and-10km-range-taara-beam-uses-silicon-photonics-technology-device-about-as-big-as-a-shoebox), [5gstore](https://5gstore.com/blog/2026/02/25/taara-beam-25gbps-via-beams-of-light/) (see also [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) COMM-001) |
| **NICT 2 Tbps FSO** | **2 Tbit/s** (5 x 400G WDM) over 7.4 km urban | **Field experiment, not a product**; satellite/HAPS terminal class (~13 to 28 kg) | [NICT](https://www.nict.go.jp/en/press/2025/12/16-1.html) |
| **Lab multiplexed FSO** (OAM/WDM/PDM) | up to **~1 Pbit/s** demonstrated | **Laboratory only**, not deployable terrestrial hardware | [arXiv 2305.12208](https://arxiv.org/pdf/2305.12208), [Nature Comms](https://www.nature.com/articles/s41467-022-35327-w) |

The honest read: **commercial, deployable terrestrial FSO is ~25 Gbps per link.** Tbps-and-up FSO exists only as field experiments (NICT) or lab demonstrations (OAM multiplexing), not as something you can buy and hang between two buildings. The lab-to-product gap is large and the high-rate demos use satellite/HAPS-grade terminals under controlled conditions.

### 2.3 The gap, quantified

- To match **one** 121.6 Tbps fiber pair with Taara Beams: 121,600 / 25 = **~4,860 beams** [DERIVED].
- To match the **5 Pbit/s** within-region AI-DCI requirement: 5,000,000 / 25 = **~200,000 beams** [DERIVED].
- Even using the NICT 2 Tbps field-experiment terminal (not a product), matching 5 Pbit/s needs **~2,500 such terminals** [DERIVED], each a ~13 to 28 kg precision optical assembly needing its own clear line of sight and weather backup.

**Conclusion.** Free-space optics is categorically disqualified from the **primary high-bandwidth AI synchronous-training interconnect**. That job is owned by trenched coherent fiber (DWDM, 800ZR/1.6T, thousands of pairs). This is not a marketing nuance; it is two-to-five orders of magnitude. Any DC-to-DC laser story must be built on the *narrower* set of jobs in Section 4, not on replacing the petabit backbone.

> A note on physics, not just product maturity. FSO's ceiling is real: a single eye-safe beam over open air through turbulence and fog has a far lower practical aggregate capacity than a fiber pair carrying 152 independent wavelengths in a controlled glass waveguide. Multiplexing (WDM/OAM) raises FSO capacity in the lab but compounds the pointing, alignment, and atmospheric-distortion problem in the field. Productized terrestrial FSO has stayed at the ~10 to 25 Gbps tier for good reason (see [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) §1).

---

## 3. The distance and latency envelope, why reach is not the problem

If bandwidth disqualifies FSO from the primary job, the natural next question is whether laser at least reaches the right distances for the secondary jobs. It does, comfortably.

**The synchronous-training distance limit is set by light-speed-in-fiber latency.** Light in single-mode fiber adds **~4.9 microseconds per km** (~5 ns/m) [FACT] ([Lynx Planning](https://lynxplanning.com/us/designing-fiber-data-center-ai/), [Corning](https://www.corning.com/optical-communications/worldwide/en/home/the-signal-network-blog/ai-data-center-design-strategies.html)). The one-way budget:

| Distance | One-way latency | Round-trip | Source |
|---|---|---|---|
| 20 km | ~0.098 ms | ~0.196 ms | [Lynx Planning](https://lynxplanning.com/us/designing-fiber-data-center-ai/) |
| 50 km | ~0.245 ms | ~0.490 ms | [Lynx Planning](https://lynxplanning.com/us/designing-fiber-data-center-ai/) |
| 100 km | ~0.490 ms | ~0.980 ms | [Lynx Planning](https://lynxplanning.com/us/designing-fiber-data-center-ai/) |

A cluster that can tolerate ~1 ms of inter-node latency for collective operations (AllReduce, AllGather) is therefore physically confined to roughly a **100 km radius** [FACT] ([Lynx Planning](https://lynxplanning.com/us/designing-fiber-data-center-ai/), corroborated by the per-km figure in [Corning](https://www.corning.com/optical-communications/worldwide/en/home/the-signal-network-blog/ai-data-center-design-strategies.html)). NVIDIA's Spectrum-XGS scale-across explicitly targets sites "in different buildings or separated by hundreds of kilometers," with distance-aware congestion control, and reports ~1.9x communication improvement while managing end-to-end latency [FACT, single-source: NVIDIA / reporting] ([NVIDIA blog](https://developer.nvidia.com/blog/how-to-connect-distributed-data-centers-into-large-ai-factories-with-scale-across-networking/), [SDxCentral](https://www.sdxcentral.com/news/nvidias-new-spectrum-xgs-aims-to-turn-multiple-data-centers-into-one-gigantic-gpu/)).

**The distance tiers AI campuses actually span:**

| Tier | Distance | Note |
|---|---|---|
| **Campus** (single mega-site) | ~2 km, cable runs approaching **20 km** across 5 to 6 buildings | [SDxCentral](https://www.sdxcentral.com/opinions/why-the-expansion-of-ai-ready-data-center-networks-depends-increasingly-on-coherent-optics/) |
| **Metro** (paired campuses) | up to **~120 km** | [Marvell](https://www.marvell.com/blogs/macsec-for-scale-across-networking.html) |
| **Long-haul** (inter-region) | 500 to 1,000+ km | [Marvell](https://www.marvell.com/blogs/macsec-for-scale-across-networking.html) |

Google's own paired campuses sit ~**15 to 50 miles** (~24 to 80 km) apart (Council Bluffs / Omaha / Papillion ~15 mi; Lincoln ~50 mi) [FACT, single-source: SemiAnalysis] ([SemiAnalysis](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais)).

**The overlap.** A Taara Beam reaches **up to ~25 km** [FACT]; the broader FSO class spans a few hundred metres to ~20 km (see [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md)). That covers the **campus tier and the near end of the metro tier**, exactly where the tightest-synchronization, highest-value interconnect lives. So laser's range is a fit for the right distances. The binding constraint is bandwidth (Section 2) and weather availability (carried over from [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) and [`optical_ground_stations.md`](optical_ground_stations.md): a pure FSO link is enterprise-grade to ~5 km, needs RF backup for carrier-grade), not reach.

---

## 4. Where a terrestrial laser DC link actually earns its keep

Combining Sections 2 and 3: laser reaches the right distances but cannot carry the petabit primary load and drops in fog. That leaves a specific, defensible set of DC-to-DC jobs, each a **supplement measured in tens of Gbps**, not the backbone. These sharpen, for AI campuses, the incremental-value framing already established in [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) §3.

| Job | Does laser win? | Why / caveat |
|---|---|---|
| **(a) Gap-fill: new AI site waiting on fiber** | **Yes, temporarily** | Trenched DCI fiber takes **12 to 24 months to permit and build** in dense areas [FACT] ([Global Data Center Hub](https://www.globaldatacenterhub.com/p/why-fiber-to-data-center-projects)). A laser link stands up in **hours**, "dark fiber in the sky," carrying a useful interim slice until fiber lands [FACT, see [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) COMM-007]. It is a bridge, not the destination. |
| **(b) Route-diversity / redundancy** | **Conditional** | The AI buildout explicitly wants "tri-versity / quad-versity" routing [FACT, single-source]. A laser link adds a physically independent path (no shared trench to cut). But it is a *low-bandwidth* redundant path (tens of Gbps), suitable for priority/control traffic or partial failover, not a full hot standby for a petabit primary. Its rival here is also **millimeter-wave/microwave** wireless DCI. |
| **(c) Over-an-obstacle hop between near buildings** | **Yes** | River, rail corridor, highway, property line you do not own, the classic FSO win (Taara's Congo River crossing avoided a ~400 km detour) [FACT, see [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md)]. Relevant when two DC buildings are close but separated by a barrier fiber cannot cheaply cross. |
| **(d) Security / fast-deploy / no-license specialty** | **Sometimes** | Narrow beam is hard to tap covertly and tamper-evident (see [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) §4); no spectrum license; redeployable. Matters for defense/sovereign-adjacent or disaster-recovery DC links, not mainstream commercial DCI. |
| **(e) Primary petabit AI synchronous-training interconnect** | **No** | Owned by trenched coherent fiber. Two-to-five orders of magnitude beyond FSO (Section 2). |

**The competitive context (new, vs the prior doc).** Laser's terrestrial DC competitor is not only fiber but **wireless RF DCI**: millimeter-wave (60 GHz, multi-Gbps to ~40 Gbps full-duplex) and microwave (10 to 11 GHz backup) point-to-point links are an established research and patent direction for data-center interconnect and backup, and they are **also weather-limited and multi-Gbps class** [FACT] ([IEEE](https://ieeexplore.ieee.org/abstract/document/5684121), [USPTO 8090411](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8090411)). So in the redundancy/fast-deploy niche, FSO competes with mmWave for the same slot (FSO offers higher peak rate and no license but worse fog tolerance; mmWave offers rain-not-fog tolerance and maturity). Neither displaces fiber for the primary job.

**An adjacent, non-shipping concept worth one line: FSO and mmWave *inside* the data center.** Academic and patent work proposes reconfigurable wireless intra-DC fabrics (rack-to-rack 60 GHz or FSO, steerable topologies) to flatten switch tiers [FACT] ([IEEE](https://ieeexplore.ieee.org/abstract/document/5684121), [USPTO 10924183](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10924183), [PMC WDM-FSO-for-DCN](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9781115/)). This is **research-stage, not a market**, and is distinct from the DC-to-DC question; noted only so the catalog records it as a known direction, not an opportunity.

---

## 5. Who the customers are

For a *direct laser DC-to-DC / enterprise point-to-point* offering, the realistic buyer set, ordered by how well laser actually fits:

| Customer | What they buy | Fit | Why |
|---|---|---|---|
| **Orbital data-center operators** | DC-to-DC and DC-to-ground optical links in space | **Primary / winning** | No fiber option exists in orbit; laser ISL is the only medium and is proven (Section 6). The strongest customer for "direct laser links between data centers." |
| **Hyperscalers / AI labs standing up a new campus** | Interim gap-fill link while fiber is trenched | **Strong but temporary** | 12 to 24 month fiber lead time; laser bridges the gap in hours. Reverts to fiber once lit. |
| **Hyperscalers / AI labs / colos needing route diversity** | A physically independent low-bandwidth redundant path | **Conditional** | Tri-versity/quad-versity demand is real; but the path is tens of Gbps and competes with mmWave. |
| **Enterprise / colo with a near-building obstacle** | Building-to-building hop over a river/rail/road/property line | **Good (classic FSO)** | The original FSO bread-and-butter, now applied to DC campuses. |
| **Defense / sovereign / disaster-recovery DC links** | Secure, no-license, fast-deploy point-to-point | **Niche** | Security and rapid-deploy attributes (carried from [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) §4); small, premium. |
| **Finance (latency arbitrage)** | Lowest-latency point-to-point on a specific route | **Narrow, pre-existing** | Air beats glass by ~47%; HFT already buys FSO/microwave on routes like Chicago to New York. A distinct, tiny market, not general DCI (see [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) §3.2 and [`comms_business_case.md`](comms_business_case.md) §1b). |

The pattern: **on the ground, every laser DC customer is buying a supplement** (bridge, redundancy, obstacle-hop, specialty). **In orbit, the orbital-DC operator is buying the primary interconnect.** The single vendor explicitly courting terrestrial DC-interconnect, Taara, calls those conversations "early stages" and frames the product as a bridge for DCs "still waiting on fiber" and a "redundant connection once fiber arrives," not a fiber replacement [FACT, see [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) COMM-007] ([Light Reading](https://www.lightreading.com/wireless/taara-expands-into-video-distribution-sizes-up-data-center-opportunity)). No public production DC-to-DC FSO deployment was found as of June 2026; the terrestrial market is nascent.

---

## 6. The orbital exception, where direct laser DC-to-DC is the architecture, not a niche

The one place the "direct laser link between data centers" thesis flips from niche supplement to primary, winning architecture is **in space**, because the disqualifiers reverse:

- **No fiber to compete with.** There is no trench to dig between two orbital compute nodes; the entire bandwidth-vs-trenched-fiber argument of Section 2 does not apply. Laser ISL is the *only* credible high-capacity medium between satellites (see [`optical_comms.md`](optical_comms.md), [`comms_business_case.md`](comms_business_case.md) §3).
- **Proven at scale.** Starlink runs ~27,000 space lasers at >99% link uptime, 100 to 200 Gbps per terminal; this is operational, not aspirational [FACT, see [`optical_comms.md`](optical_comms.md)].
- **The market has already fused orbital compute with orbital optical relay.** Axiom Space's orbital data-center nodes (launched Jan 2026) connect via **2.5 Gbps laser links** to Kepler's constellation and to ground; Kepler declared the first commercially operational optical data-relay network (March 2026); SpaceX filed for a million-satellite orbital data center linked by **1 Tbps optical links**; Google's Project Suncatcher envisions LEO TPU clusters interconnected by laser [FACT, see [`comms_business_case.md`](comms_business_case.md) §3 to §4] ([Data Center Frontier](https://www.datacenterfrontier.com/site-selection/article/55328204/when-the-cloud-leaves-earth-google-and-nvidia-test-space-data-centers-for-the-orbital-ai-era)).

This is the through-line connecting this side track back to the main project: the same Mynaric CONDOR optical terminals Rocket Lab acquired are the DC-to-DC interconnect for an orbital data center. **The honest framing is symmetric with the terrestrial finding:** laser is the wrong tool for the petabit *terrestrial* AI-DCI backbone (fiber wins), and the *right* tool for the *orbital* DC-to-DC link (no fiber exists). The terrestrial laser DC market is a real but narrow supplement; the orbital laser DC market is the primary architecture and the strategically relevant one for this project.

---

## 7. Connections to the rest of the library (neutral pointers, no verdict)

1. **Same weather wall, same fix.** Terrestrial DC-to-DC laser fails in fog and needs an RF/fiber backup to reach carrier-grade, exactly as established for general FSO in [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) and for the space-to-ground link in [`optical_ground_stations.md`](optical_ground_stations.md). A laser DC link sold as a *sole* path is enterprise-grade, not carrier-grade.
2. **Bandwidth scale is the new lens.** The prior doc said "not a fiber replacement"; this doc quantifies *why* for AI-DCI specifically (petabit need vs ~25 Gbps beam). That ~10,000x-class gap is the reusable test for any "laser replaces fiber" claim.
3. **The orbital tie-in is the payoff.** The terrestrial niche is small; the orbital DC-to-DC case (where laser is the only medium) is where this side track rejoins the main orbital-data-center thesis. See [`comms_business_case.md`](comms_business_case.md) §3 to §4 and [`optical_comms.md`](optical_comms.md).
4. **Security and latency edges carry over unchanged.** The narrow-beam tap-resistance and the air-beats-glass latency edge are the same levers documented in [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md); they apply to DC links but are decisive only for the security and HFT niches, not mainstream DCI.

---

## Sources

AI-DCI demand engine (distributed training, dark-fiber land rush):
- [SemiAnalysis, Multi-Datacenter Training: OpenAI's Ambitious Plan (5 Pbit/s intra-region, 1 Pbit/s inter-region, 121.6 Tbps/fiber-pair, ZR/ZR+ 120 to 500 km, dark fiber, Google campus distances)](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais)
- [Data Centers Inc, AI Training Clusters Are Reaching 1 GW Infrastructure Scale](https://www.datacenters.com/news/ai-training-clusters-are-reaching-1-gw-infrastructure-scale)
- [arXiv 2507.07765, Distributed and Decentralised Training (multi-DC training for GPT-4.5, Gemini-1.5)](https://arxiv.org/pdf/2507.07765)
- [PR Newswire, BIG Fiber Secures $250M (Stonepeak/La Caisse; 850 route miles; 3M+ fiber miles; AI demand)](https://www.prnewswire.com/news-releases/big-fiber-secures-250-million-financing-led-by-stonepeak-credit-and-la-caisse-to-accelerate-digital-infrastructure-expansion-302775649.html)
- [Data Center Knowledge, Big Fiber Financing Signals AI's Next Infrastructure Land Rush (504x Cisco figure; tri-versity/quad-versity; machine-to-machine sync; CRU Group)](https://www.datacenterknowledge.com/infrastructure/big-fiber-financing-signals-ai-s-next-infrastructure-land-rush)
- [IEEE ComSoc, Big Fiber's $250M financing deal](https://techblog.comsoc.org/2026/05/19/big-fibers-250m-financing-deal-to-buildout-dark-fiber-routes-for-ai-data-center-expansion/)
- [Towards AI, How Data Centers Work in 2026 (interconnect as bottleneck)](https://pub.towardsai.net/how-data-centers-actually-work-from-cooling-systems-to-gpu-clusters-a23918104762)
- [ADTEK, AI Data Center Interconnect 2026: CPO, Optical Interconnect and Deployment Challenges](https://adtek-fiber.com/ai-data-center-interconnect-2026-cpo-optical-interconnect-and-deployment-challenges/)

Bandwidth scale (coherent DCI, DWDM, scale-across fabrics):
- [Effect Photonics, Data Center Interconnects: Coherent or Direct Detect? (800ZR 80 km, 800LR 10 km)](https://effectphotonics.com/insights/data-center-interconnects-coherent-or-direct-detect/)
- [Marvell, MACsec for Scale-across Networking (800G coherent 10 to 1,000 km; 1.6T coherent-lite 2 to 20 km; campus/metro/long-haul tiers)](https://www.marvell.com/blogs/macsec-for-scale-across-networking.html)
- [NVIDIA Newsroom, Spectrum-XGS Ethernet (giga-scale AI super-factories, long-distance interconnect)](https://nvidianews.nvidia.com/news/nvidia-introduces-spectrum-xgs-ethernet-to-connect-distributed-data-centers-into-giga-scale-ai-super-factories)
- [NVIDIA blog, Scale-Across Networking (hundreds of km, distance-aware congestion control, ~1.9x)](https://developer.nvidia.com/blog/how-to-connect-distributed-data-centers-into-large-ai-factories-with-scale-across-networking/)
- [SDxCentral, Nvidia Spectrum-XGS "one gigantic GPU" (500m start, hundreds of km)](https://www.sdxcentral.com/news/nvidias-new-spectrum-xgs-aims-to-turn-multiple-data-centers-into-one-gigantic-gpu/)
- [Google Cloud, Data center and global networks built for AI era (400 Gbps links, 3.2 Tbps increments, petabit)](https://cloud.google.com/blog/products/networking/data-center-and-global-networks-built-for-ai-era)

Free-space optics capacity (commercial, field, lab):
- [Tom's Hardware, Taara Beam (up to 25 Gbps, up to 25 km, shoebox, silicon photonics)](https://www.tomshardware.com/tech-industry/optical-transceiver-achieves-up-to-25-gbps-throughput-with-ultra-low-latency-and-10km-range-taara-beam-uses-silicon-photonics-technology-device-about-as-big-as-a-shoebox)
- [5gstore, Taara Beam: 25 Gbps via beams of light](https://5gstore.com/blog/2026/02/25/taara-beam-25gbps-via-beams-of-light/)
- [Optica OPN, Taara Launches Photonics Communications Platform](https://www.optica-opn.org/home/industry/2026/february/taara_launches_photonics_communications_platform/)
- [Light Reading, Taara expands into video distribution, explores data centers ("early stages," bridge while awaiting fiber, redundant path)](https://www.lightreading.com/wireless/taara-expands-into-video-distribution-sizes-up-data-center-opportunity)
- [NICT, World's First 2 Tbit/s FSO with small satellite/HAPS-mountable terminals (field experiment, 7.4 km, 5 x 400G WDM)](https://www.nict.go.jp/en/press/2025/12/16-1.html)
- [arXiv 2305.12208, OAM multiplexing FSO (toward Pbit/s, lab)](https://arxiv.org/pdf/2305.12208)
- [Nature Communications, High-capacity FSO using WDM and mode-division-multiplexing](https://www.nature.com/articles/s41467-022-35327-w)

Distance / latency physics:
- [Lynx Planning, Designing AI Data Center Fiber Routes (4.9 microseconds/km; 20/50/100 km latency table; route diversity)](https://lynxplanning.com/us/designing-fiber-data-center-ai/)
- [Corning, AI Data Center Design Strategies (per-km fiber latency, ~100 km sync limit)](https://www.corning.com/optical-communications/worldwide/en/home/the-signal-network-blog/ai-data-center-design-strategies.html)
- [SDxCentral, Why AI-ready data center networks depend on coherent optics (campus 2 km / runs to 20 km; metro/long-haul)](https://www.sdxcentral.com/opinions/why-the-expansion-of-ai-ready-data-center-networks-depends-increasingly-on-coherent-optics/)

Fiber build cost and lead time:
- [Global Data Center Hub, Why Fiber-to-Data Center Projects Cost So Much ($60k to $120k/mile; 45% civil works; 12 to 24 month permitting; 864 to 1,728 strands)](https://www.globaldatacenterhub.com/p/why-fiber-to-data-center-projects)
- [The Network Installers, Dark Fiber Network (per-strand-mile lease pricing context)](https://thenetworkinstallers.com/blog/dark-fiber-network/)

Wireless (mmWave/microwave) DCI and intra-DC FSO (adjacent, research-stage):
- [IEEE Xplore, Wireless Data Center with Millimeter Wave Network (60 GHz, 40 Gbps full-duplex)](https://ieeexplore.ieee.org/abstract/document/5684121)
- [USPTO 8090411, Wireless millimeter wave communication system (10.7 to 11.7 GHz microwave backup)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8090411)
- [USPTO 10924183, Reconfigurable wireless data center network using free-space optics](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10924183)
- [PMC, Bidirectional WDM FSO for Data Center Networks](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9781115/)

Orbital DC-to-DC laser context:
- [Data Center Frontier, When the Cloud Leaves Earth: Google and NVIDIA Test Space Data Centers (Project Suncatcher, orbital AI)](https://www.datacenterfrontier.com/site-selection/article/55328204/when-the-cloud-leaves-earth-google-and-nvidia-test-space-data-centers-for-the-orbital-ai-era)

(See also project docs: [`laser_comms/laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md), [`laser_comms/optical_comms.md`](optical_comms.md), [`laser_comms/optical_ground_stations.md`](optical_ground_stations.md), [`laser_comms/comms_business_case.md`](comms_business_case.md).)

---

## Confidence

**Overall: medium-high.**

- **High** on the bandwidth-scale disqualification (§2). The petabit AI-DCI requirement, the 121.6 Tbps fiber-pair building block, and the ~25 Gbps commercial FSO link are each independently sourced; the resulting two-to-five orders-of-magnitude gap is arithmetic, not opinion.
- **High** on the distance/latency physics (§3). The 4.9 microseconds/km figure, the 20/50/100 km latency table, the ~100 km sync radius, and the campus/metro distance tiers are consistent across multiple sources and match the FSO range envelope.
- **High** on the orbital exception (§6), built on the existing, well-sourced [`optical_comms.md`](optical_comms.md) and [`comms_business_case.md`](comms_business_case.md) findings (Starlink, Kepler, Axiom, SpaceX, Suncatcher).
- **Medium-high** on the narrow-niche terrestrial framing (§4 to §5). It is an analytical synthesis on sourced inputs (gap-fill lead time, redundancy demand, obstacle-hop, mmWave competition), not a single quoted fact, and no production terrestrial DC-to-DC FSO deployment exists yet to confirm it.
- **Medium** on terrestrial FSO market size. Deferred to [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) COMM-010; analyst forecasts span a wide range with mixed scope (some include space FSO; the DC-interconnect slice is not separately and reliably sized).
- **Single-source flags:** the 5 Pbit/s and 1 Pbit/s AI-DCI bandwidth figures and the Google campus-distance figures rest on SemiAnalysis; the 504x Cisco figure and tri-versity/quad-versity language rest on Big Fiber via Data Center Knowledge; the Spectrum-XGS 1.9x figure rests on NVIDIA. These are tagged single-source in the ledger and should be treated as directional.

---

## Open Questions

1. **Is the terrestrial DC-to-DC FSO use real yet, or still a Taara pitch?** As of June 2026, Taara is the only vendor courting it, calls it "early stages," and no public production DC-to-DC FSO deployment was found. Treat terrestrial laser-for-DC-interconnect as nascent, the gap-fill and redundancy roles are plausible but unproven in production.
2. **What is the realistic aggregate of a multi-beam FSO DC link?** A site could stack several beams. How many Taara-class beams can realistically co-point between two DC buildings, and at what cost, before fiber or mmWave is simply better? Unquantified; the field FSO record (NICT 2 Tbps) uses satellite-grade terminals, not a stack of commercial Beams.
3. **Pricing.** No hard per-link FSO price was obtained (Taara markets "cheaper than burying a few km of fiber" qualitatively). A vendor quote is needed to compare a laser redundancy link against an 800ZR coherent fiber pair or a mmWave link on a real route.
4. **FSO vs millimeter-wave for the DC redundancy slot.** Both are multi-Gbps, weather-limited, fast-deploy. Which wins for a given climate, distance, and bandwidth target (FSO: higher peak rate, no license, fog-vulnerable; mmWave: rain-not-fog, mature, licensed bands) is route-specific and unresolved here.
5. **Does the orbital DC-to-DC link rate scale to AI needs?** Current orbital laser DC links are 2.5 Gbps (Axiom/Kepler) to a 1 Tbps aspiration (SpaceX filing); whether orbital optical interconnect can reach the bandwidth an orbital AI cluster needs is the open question on the orbital side (cross-ref [`optical_comms.md`](optical_comms.md), Mk3.1 roadmap).

---

## Claims ledger

(For the catalog step to ingest and assign COMM- ids. Each hard claim with two or more sources, single-source claims flagged.)

1. **AI labs train across multiple gigawatt-scale campuses; multi-DC training is in production (GPT-4.5, Gemini-1.5); interconnect, not GPU, is increasingly the limit.** Sources: [SemiAnalysis](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais), [arXiv 2507.07765](https://arxiv.org/pdf/2507.07765), [Towards AI](https://pub.towardsai.net/how-data-centers-actually-work-from-cooling-systems-to-gpu-clusters-a23918104762).

2. **A dark-fiber land rush is underway for AI-DCI: Big Fiber raised $250M (Stonepeak/La Caisse) for AI routes; AI has overtaken telecom as the primary growth driver for optical fiber (CRU Group).** Sources: [PR Newswire](https://www.prnewswire.com/news-releases/big-fiber-secures-250-million-financing-led-by-stonepeak-credit-and-la-caisse-to-accelerate-digital-infrastructure-expansion-302775649.html), [Data Center Knowledge](https://www.datacenterknowledge.com/infrastructure/big-fiber-financing-signals-ai-s-next-infrastructure-land-rush), [IEEE ComSoc](https://techblog.comsoc.org/2026/05/19/big-fibers-250m-financing-deal-to-buildout-dark-fiber-routes-for-ai-data-center-expansion/).

3. **AI scale-up traffic generates ~504x more bandwidth than traditional DCI flows; AI customers demand tri-versity/quad-versity route diversity.** [FACT, single-source: Big Fiber CCO via Data Center Knowledge] Source: [Data Center Knowledge](https://www.datacenterknowledge.com/infrastructure/big-fiber-financing-signals-ai-s-next-infrastructure-land-rush).

4. **AI campus-to-campus interconnect needs ~5 Pbit/s within a region and ~1 Pbit/s between regions.** [FACT, single-source: SemiAnalysis] Source: [SemiAnalysis](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais).

5. **A single DWDM fiber pair carries up to ~121.6 Tbps (800 Gbps x 152 wavelengths); petabit DCI is met by laying thousands of fiber pairs.** Sources: [SemiAnalysis](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais), [Google Cloud](https://cloud.google.com/blog/products/networking/data-center-and-global-networks-built-for-ai-era) (petabit-scale fabric corroboration).

6. **Coherent DCI today: 800ZR to 80 km, 800LR to 10 km per wavelength; 1.6T coherent-lite for 2 to 20 km campus/metro; 800G out to ~1,000 km.** Sources: [Effect Photonics / OIF](https://effectphotonics.com/insights/data-center-interconnects-coherent-or-direct-detect/), [Marvell](https://www.marvell.com/blogs/macsec-for-scale-across-networking.html).

7. **Commercial deployable terrestrial FSO (Taara Beam) carries ~25 Gbps per beam over up to ~25 km.** Sources: [Tom's Hardware](https://www.tomshardware.com/tech-industry/optical-transceiver-achieves-up-to-25-gbps-throughput-with-ultra-low-latency-and-10km-range-taara-beam-uses-silicon-photonics-technology-device-about-as-big-as-a-shoebox), [5gstore](https://5gstore.com/blog/2026/02/25/taara-beam-25gbps-via-beams-of-light/) (and [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) COMM-001).

8. **High-rate FSO (2 Tbps, 5 x 400G WDM, 7.4 km urban) exists only as a field experiment on satellite/HAPS-grade terminals; ~1 Pbit/s FSO exists only in the lab (OAM multiplexing).** Sources: [NICT](https://www.nict.go.jp/en/press/2025/12/16-1.html), [arXiv 2305.12208](https://arxiv.org/pdf/2305.12208), [Nature Communications](https://www.nature.com/articles/s41467-022-35327-w).

9. **[DERIVED] Matching one 121.6 Tbps fiber pair needs ~4,860 Taara Beams; matching 5 Pbit/s needs ~200,000 beams; FSO is two-to-five orders of magnitude short of the primary AI-DCI job.** Basis: claims 4, 5, 7 (arithmetic).

10. **Fiber adds ~4.9 microseconds/km; one-way latency is ~0.098 ms at 20 km, ~0.245 ms at 50 km, ~0.490 ms at 100 km; ~1 ms-tolerant synchronous training is confined to ~100 km radius.** Sources: [Lynx Planning](https://lynxplanning.com/us/designing-fiber-data-center-ai/), [Corning](https://www.corning.com/optical-communications/worldwide/en/home/the-signal-network-blog/ai-data-center-design-strategies.html).

11. **AI DC distance tiers: campus ~2 km (runs to ~20 km across 5 to 6 buildings), metro up to ~120 km, long-haul 500 to 1,000+ km; Google's paired campuses sit ~15 to 50 miles apart.** Sources: [SDxCentral](https://www.sdxcentral.com/opinions/why-the-expansion-of-ai-ready-data-center-networks-depends-increasingly-on-coherent-optics/), [Marvell](https://www.marvell.com/blogs/macsec-for-scale-across-networking.html); Google campus distances [single-source: SemiAnalysis](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais).

12. **NVIDIA Spectrum-XGS targets cross-DC AI fabrics over hundreds of km with distance-aware congestion control, reporting ~1.9x communication improvement.** [FACT, single-source: NVIDIA / reporting] Sources: [NVIDIA blog](https://developer.nvidia.com/blog/how-to-connect-distributed-data-centers-into-large-ai-factories-with-scale-across-networking/), [SDxCentral](https://www.sdxcentral.com/news/nvidias-new-spectrum-xgs-aims-to-turn-multiple-data-centers-into-one-gigantic-gpu/) (corroborating report).

13. **Trenched DCI fiber takes 12 to 24 months to permit and build in dense areas, costs ~$60k to $120k/mile (45% civil works), and uses 864 to 1,728 strands on DC routes.** Sources: [Global Data Center Hub](https://www.globaldatacenterhub.com/p/why-fiber-to-data-center-projects), corroborated by industry benchmark via [Data Center Knowledge search context](https://www.datacenterknowledge.com/infrastructure/big-fiber-financing-signals-ai-s-next-infrastructure-land-rush).

14. **Millimeter-wave (60 GHz, to ~40 Gbps full-duplex) and microwave (10 to 11 GHz backup) are an established wireless-DCI / intra-DC research and patent direction, also multi-Gbps and weather-limited; intra-DC FSO is similarly research-stage.** Sources: [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/5684121), [USPTO 8090411](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8090411), [USPTO 10924183](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10924183).

15. **Orbital data-center-to-data-center laser links are operational/announced today: Axiom + Kepler at 2.5 Gbps, SpaceX filing at 1 Tbps, Google Project Suncatcher laser-linked TPU clusters; laser ISL is the only credible orbital interconnect medium.** Sources: [Data Center Frontier](https://www.datacenterfrontier.com/site-selection/article/55328204/when-the-cloud-leaves-earth-google-and-nvidia-test-space-data-centers-for-the-orbital-ai-era), and (carried) [`comms_business_case.md`](comms_business_case.md) §3 to §4, [`optical_comms.md`](optical_comms.md).

---

> **China aside (excluded from main analysis per scope rule):** China has an active FSO and laser-DCI research program (academic and commercial); it is excluded from all market totals above and noted only here.

> **Lint note for the catalog step:** This doc deliberately does not re-derive claims already held in [`laser_terrestrial_interconnect.md`](laser_terrestrial_interconnect.md) (COMM-001 Taara Beam specs, COMM-007 Taara DC positioning, COMM-010 FSO market size, the security and weather claims). It references them and adds only the AI-DCI-specific, bandwidth-scale, distance-physics, and orbital-tie-in material. No COMM- ids assigned here by design.
