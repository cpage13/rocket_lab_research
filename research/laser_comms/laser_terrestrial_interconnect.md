# Terrestrial Laser Links for Ground and Data-Center Interconnect, Incremental Value and Security

*Research date: June 2026. Communications research-wiki effort (shared library).*

Builds on / does not duplicate:
- [`research/laser_comms/optical_ground_stations.md`](optical_ground_stations.md), weather availability, site diversity, ground-segment cost, the "lasers cannot punch through cloud" physics.
- [`research/laser_comms/optical_comms.md`](optical_comms.md), optical fundamentals, narrow-beam properties, Mynaric CONDOR, space-to-ground rates.
- [`research/llm_compute/multi_rack_inference.md`](../llm_compute/multi_rack_inference.md), which traffic actually needs to cross a link (TP cannot, PP/EP/replica can), and the fiber-vs-vacuum latency advantage.

This doc is a focused extension covering the **ground-to-ground** case: laser and free-space optical (FSO) links between buildings and data centers on Earth, the incremental-value question, and security as a differentiator. It is a neutral source doc for the shared library; no verdict on the Rocket Lab business is drawn here.

---

## Summary / Verdict

**Terrestrial laser interconnect is a real, shipping product class, but it is a niche tool, not a fiber replacement.** The honest framing:

1. **It exists today and works.** Free-space optical links carrying **10 to 25 Gbps over 1 to 20 km** are commercial products from at least half a dozen vendors, deployed in 12+ countries by major carriers. Alphabet's spin-out **Taara** is the clear category leader: its **Taara Beam** product does **up to 25 Gbps over up to 10 km** [FACT, COMM-001], and the earlier **Lightbridge** does **20 Gbps over up to 20 km** and is live with T-Mobile, Airtel, SoftBank, and Digicel [FACT, COMM-002]. The legacy enterprise/metro FSO vendors (fSONA, CableFree, LightPointe, Mostcom, Koruza) sell **1 Gbps-class** building-to-building bridges [FACT, COMM-003].

2. **Weather is the binding constraint, exactly as for the space link.** A laser cannot penetrate fog (fog causes **10 to 100 dB/km** of attenuation, the single worst case) [FACT, COMM-004]. The distance you can carry collapses as you raise the availability bar: **~5 km for "enterprise" availability, but only ~140 m for carrier-grade 99.999% ("five nines")** on a pure optical link [FACT, COMM-005]. To get five-nines at useful range you **must** add an **RF (or fiber) backup path** that takes over when fog rolls in. Hybrid FSO/RF is the standard answer and is a productized feature [FACT, COMM-006]. This is the ground-to-ground twin of the site-diversity story in [`optical_ground_stations.md`](optical_ground_stations.md): the laser alone is ~50 to 99% available, and the last decimal places come from a different medium, not a bigger laser.

3. **The incremental-value question has a clear shape: laser's strong case is where fiber does NOT already exist; its weaker, conditional case is where fiber DOES exist.** The dominant, well-proven use is **bridging a gap fiber cannot economically cross**, a river, a rail corridor, a property line, a building you do not own the trench rights to, or a site waiting months for fiber to be laid. Taara's own positioning is "links that go where fiber won't" and "dark fiber, but in the sky," deployable in **hours** versus the time and cost to **trench a kilometer of fiber** [FACT, COMM-007]. Where fiber **already** exists and is lit, a laser link rarely beats it on raw cost-per-bit or reliability. The three places it can still add value alongside existing fiber are narrower and situational: **(a) security/physical-layer privacy**, **(b) latency** (light is ~47% faster in air than in glass, the same physics as the ISL case in [`multi_rack_inference.md`](../llm_compute/multi_rack_inference.md)), and **(c) speed-of-deployment / no-trenching / no-spectrum-license** for temporary, redundant, or disaster-recovery paths.

4. **Security is a genuine differentiator, with caveats.** A laser beam is extremely narrow (spreading to only **~2 m at 1 km and ~5 m at 5 km**) and line-of-sight, so to tap it an eavesdropper must physically place hardware inside the beam path, which is detectable and hard to do covertly [FACT, COMM-008]. There is no RF side-lobe leaking the signal across a neighborhood. This is a real advantage over microwave and a different threat model than tapping buried fiber. But it is not unconditional secrecy: FSO is still an open line-of-sight channel and can be tapped if the beam footprint is much wider than the receiver, jammed, or physically obstructed [FACT, COMM-009].

**Bottom line:** terrestrial laser interconnect is best understood as a **gap-filler and a specialty link**, strongest where trenching fiber is slow, expensive, or impossible, and as a fast-to-deploy redundant/secure path. It is **not** a general-purpose replacement for existing lit fiber. Any data-center-interconnect pitch that leans on "replaces fiber everywhere" is weak; one that leans on "reaches where fiber can't, deploys in hours, harder to tap, and slightly lower latency" is supportable. **Confidence: medium-high** on the product landscape, weather limits, and the incremental-value framing (multiple independent sources agree); **medium** on the exact market-size numbers (wide vendor spread) and on how much the security and latency edges are worth in a real DC procurement.

---

## 1. What terrestrial laser / FSO interconnect actually is

Free-space optical (FSO) communication, also called optical wireless or "laser link," sends a modulated near-infrared laser beam (typically **~1550 nm**, the same eye-safe optical C-band the space terminals use, see [`optical_comms.md`](optical_comms.md)) through open air between two line-of-sight terminals. It is the **same physics as a fiber link with the glass removed**, and the same physics as a space-to-ground downlink confined to the ground. No fiber is trenched and no radio spectrum is licensed.

The terminals are small and self-contained: a transmit/receive optical head, pointing/tracking (Taara's units use gyroscopes and accelerometers to hold alignment, and the new silicon-photonics generation steers the beam electronically with an optical phased array of 1,000+ emitters). A unit is roughly the size of a traffic light (Lightbridge, ~13 kg) down to a shoebox (Taara Beam) and mounts on a rooftop, pole, or existing structure.

**Two distinct product tiers exist today:**

| Tier | Typical rate | Typical range | Representative products | Status |
|---|---|---|---|---|
| **Modern high-rate** | **20 to 25 Gbps** | **up to 10 to 20 km** | Taara Beam (25 Gbps / 10 km); Taara Lightbridge (20 Gbps / 20 km) | Shipping; Taara deployed in 12+ countries [COMM-001, COMM-002] |
| **Legacy enterprise/metro** | **0.1 to 1+ Gbps** (Fast/Gigabit Ethernet) | **few hundred m to ~2 to 5 km** | fSONA SONAbeam, CableFree, Mostcom/ARTOLINK, Koruza (IRNAS, open-source) | Shipping; LightPointe exited the FSO line, a sign of a thin legacy market [COMM-003] |

The gap between the two tiers is the story of the last few years: FSO was a sleepy ~1 Gbps niche until Alphabet's Project Loon optical work spun out as **Taara** (independent company, March 2025, backed by Alphabet and Series X Capital) and pushed rates and ranges up by ~20x while shrinking the hardware. Taara explicitly markets "fiber-like speeds through the air."

---

## 2. The weather constraint, same wall as the space link, on the ground

[`optical_ground_stations.md`](optical_ground_stations.md) establishes the core fact for space-to-ground: a laser cannot penetrate cloud, and availability comes from **site diversity**, not aperture. The ground-to-ground case hits the same wall, with the relevant obstacle being **fog** (and to a lesser extent heavy rain and snow) rather than high cloud.

**The attenuation numbers:**

| Condition | Optical attenuation | Effect on a terrestrial laser link |
|---|---|---|
| **Clear air** | < ~0.5 dB/km | Full range, full rate |
| **Haze / light mist** | ~few dB/km | Range derated; usually survivable |
| **Rain** | ~3 to 30 dB/km (rate-dependent) | Range derated; tropical rain is the dominant limiter in those climates [COMM-004] |
| **Fog** | **10 to ~100 dB/km** | The killer. Thick fog (visibility 50 to 250 m) drops the link entirely beyond a few hundred metres [COMM-004] |

Because fog attenuation is so steep, **the achievable range is a strong function of the availability target.** The published carrier-engineering result is stark:

- **Enterprise-grade availability:** an FSO link can run **up to ~5 km** [FACT, COMM-005].
- **Carrier-grade 99.999% ("five nines"):** a **pure optical** link must normally be **under ~140 m** (based on a ~53 dB link budget), though dry-climate cities like Phoenix or Las Vegas push this out considerably [FACT, COMM-005].
- A single un-backed-up FSO site is therefore in the same ~50 to 99% availability band as a single optical ground station, and for the same reason: one bad-weather day takes it down.

**The standard fix is a backup path, not a bigger laser.** A **hybrid FSO/RF** link pairs the 1550 nm optical beam (high bandwidth, used the majority of the time) with a lower-rate RF link (e.g. a millimeter-wave or microwave path) that carries traffic through exactly the thick-fog conditions that kill the laser. This combination is what reaches **99.999%** at useful range, and it is sold as a built-in automatic-failover feature [FACT, COMM-006]. The RF backup is the ground-to-ground analogue of the multi-site weather-diverse OGS network in [`optical_ground_stations.md`](optical_ground_stations.md): the laser gives you the bandwidth, a second medium gives you the last decimal places of availability.

> **Implication for any DC-interconnect use:** a terrestrial laser link is a high-bandwidth path that **needs a defined fallback** (RF backup, or a fiber path it is augmenting) before it can carry anything that demands five-nines. A laser link offered as the *sole* path between two data centers is an enterprise-grade (not carrier-grade) link unless paired with RF.

---

## 3. The incremental-value question, where does laser add value?

This is the crux the founder flagged. The cleanest way to frame it: **does laser add value only where fiber does not already exist, or also where fiber is present?** The evidence supports a two-part answer.

### 3.1 The strong case: where fiber does NOT (economically) exist

This is the dominant, proven use and the entire commercial thesis of the modern FSO players. A laser link earns its keep when laying fiber is **slow, expensive, or physically blocked**:

- **Crossing an obstacle fiber cannot cheaply cross.** Taara connected Brazzaville and Kinshasa across the Congo River, avoiding a **~400 km** fiber detour [FACT]. Rivers, rail corridors, highways, canyons, and historic districts are classic FSO wins.
- **Property and right-of-way you do not own.** A laser shot over a public street or a third party's land needs no trenching permit or right-of-way (the beam just needs line of sight). Crossing public barriers without ownership rights is a textbook FSO use case.
- **Sites waiting on fiber.** Taara's framing: "by the time you have to dig and trench a kilometer of fiber, Taara's solution is going to be very economical," deployable in **hours** and described as "**dark fiber, but in the sky**" [FACT, COMM-007]. Roughly **50% of the world is within 25 km of a fiber point of presence** but not connected to it; FSO bridges that middle-mile gap [FACT].
- **The honest scope limit:** Taara's own CEO frames the product as links that **"go where fiber won't."** That is the center of gravity. Where fiber is already in the ground and lit, the laser's cost-per-bit and reliability advantage largely disappears.

### 3.2 The conditional case: where fiber DOES already exist

Here laser does **not** generally win on raw economics, but three specific attributes can still justify a laser link **alongside** existing fiber:

| Value lever | Does it beat existing fiber? | Notes |
|---|---|---|
| **Cost per bit** | No (usually) | Lit fiber already paid for is cheaper to keep using. Laser wins only on *new* builds that avoid trenching. |
| **Reliability** | No, on its own | Pure FSO is enterprise-grade (≤5 km); buried fiber is more weather-robust. Laser needs RF backup just to match. |
| **Security / privacy** | **Sometimes yes** | Narrow line-of-sight beam is hard to tap covertly; different (and for some threat models, stronger) than protecting buried fiber. See §4. |
| **Latency** | **Marginally yes** | Light is **~47% faster in air than in glass fiber**, and a laser shoots a straight line-of-sight path while fiber follows conduits around obstacles. This is the same vacuum/air advantage quantified for ISLs in [`multi_rack_inference.md`](../llm_compute/multi_rack_inference.md). Decisive only for latency-arbitrage use (HFT-style), negligible for most DC traffic. |
| **Deployment speed / flexibility** | **Yes** | Hours to stand up, no trench, no spectrum license, redeployable. Wins for *temporary*, *redundant*, or *disaster-recovery* paths even where fiber exists. |

The latency lever has a real-world precedent worth noting: the **high-frequency-trading** industry already pays a premium for wireless (microwave and FSO) links on routes like Chicago to New York precisely because air beats glass on speed, with the medium alone accounting for **>3.5 ms** round-trip on that ~1,400-mile route [FACT]. That validates the latency physics, but it is a narrow market; it does not generalize to ordinary data-center interconnect, where a fraction of a millisecond rarely matters.

**Synthesis of the incremental-value question:**

- **Where fiber is absent or uneconomical to lay:** laser adds **clear, primary value** (the whole point of the product).
- **Where fiber is present and lit:** laser adds **conditional, secondary value**, mainly as a **fast-deploy redundant/secure path** or for **latency arbitrage**, not as a cheaper or more reliable everyday link.

A DC-interconnect story that claims "replaces fiber even where fiber exists" is not supported by the evidence. A story that claims "fills the gaps fiber can't reach, stands up in hours as a redundant or secure overlay, and is slightly faster" is well supported.

---

## 4. Security as a differentiator

Security is the most defensible "value even where fiber exists" claim, so it deserves its own section.

### 4.1 Why a laser link is hard to intercept

- **Pencil-thin beam.** An FSO beam spreads to only **~2 m at 1 km and ~5 m at 5 km** [FACT, COMM-008]. There is no broad RF footprint blanketing the area. By contrast a microwave beam can spread to cover a building's length at 1 km and a city block at 5 km, leaking signal an eavesdropper can collect at a distance [FACT].
- **Physical-access requirement.** To intercept the beam, an attacker must place a receiver **inside the line-of-sight path** (within inches of a terminal or directly in the beam), and align it precisely enough to capture usable signal. That is conspicuous, physically intrusive, and tends to disturb the link (alerting the operator) [FACT, COMM-008].
- **No side lobes, no near-zone reflections, immune to electromagnetic interference.** Nothing radiates sideways to be passively swept up; the channel is also immune to RF jamming and EMI [FACT, COMM-009].
- **Different threat model than fiber.** Buried fiber can be tapped by splicing or bend-coupling at an access point, often without the endpoints noticing. A free-space beam has no buried run to splice; the attack surface is the open path, which is observable. For some adversary models (e.g. concern about covert physical taps on a leased fiber run), the laser's "you must stand in the beam" property is genuinely stronger. This is why defense and intelligence users (NATO, QinetiQ) list **low probability of intercept/detection** as a primary reason for FSO in tactical networks [FACT].

### 4.2 The caveats (do not oversell it)

- FSO is **still an open line-of-sight channel** and **remains vulnerable to eavesdropping, jamming, and physical-layer attack**, especially when the beam footprint at the receiver is **much wider than the receiver aperture** (spilled light can be collected at the edge) [FACT, COMM-009].
- It is not cryptographic security. It is **physical-layer obscurity plus tamper-evidence**: a high bar for a covert passive tap, not an absolute guarantee. Sensitive traffic should still be encrypted end-to-end; the laser link reduces interception risk, it does not eliminate the need for crypto.
- Research adds physical-layer techniques on top (e.g. ranging-based phase encryption) to harden FSO further, which signals the base channel is good-but-not-perfect.

**Net:** security is a real, citable differentiator that holds **even where fiber exists**, the strongest leg of the "value alongside fiber" argument, provided it is described as "much harder to intercept covertly and tamper-evident," not as "unbreakable."

---

## 5. What exists today, vendors, deployments, and limits

A consolidated view of the real, deployed terrestrial laser/FSO landscape (excludes the space-to-ground stations covered in [`optical_ground_stations.md`](optical_ground_stations.md)):

| Vendor / system | Data rate | Range | Real deployment evidence | Notes |
|---|---|---|---|---|
| **Taara Beam** (Alphabet spin-out) | **up to 25 Gbps** | **up to 10 km (~6.2 mi)** | Launched Feb 2026; targets urban, enterprise campuses, **data-center clusters**, event venues [COMM-001] | Silicon-photonics optical phased array (1,000+ emitters), shoebox form factor, ~50 µs-class latency; deployable in hours, no spectrum license |
| **Taara Lightbridge** | **20 Gbps** | **up to 20 km** | Live in **12+ countries** with **T-Mobile, Airtel, SoftBank, Digicel**; Congo River crossing (avoided ~400 km detour) [COMM-002] | First-gen, ~13 kg (traffic-light size); the proven workhorse |
| **fSONA (SONAbeam)** | up to ~1.25 Gbps (GbE) | ~few hundred m to few km | Long-standing enterprise/metro vendor [COMM-003] | Native Fast/Gigabit Ethernet, TDM+IP |
| **CableFree (Wireless Excellence)** | 1 Gbps+ aggregate | urban high-capacity, ~km | Enterprise/metro, carrier-class hybrid options [COMM-003, COMM-006] | Markets hybrid FSO/RF for high availability and low-latency/HFT links |
| **Mostcom / ARTOLINK (RU)** | up to ~10 Gbps (high-end) | ~km class | Enterprise/metro | Legacy high-rate FSO line |
| **Koruza (IRNAS)** | ~1 Gbps | short (~100 m class) | Open-source / community | Low-cost campus/last-mile design |
| **LightPointe** | up to 1 Gbps | up to ~2 km | **Discontinued its FSO line** | Its exit is a signal the *legacy* FSO market was thin before Taara reignited it [COMM-003] |

**The five canonical edge-case deployments** (where terrestrial laser is actually used):

1. **Campus / building-to-building links.** LAN-to-LAN between buildings you own at Fast/Gigabit Ethernet, avoiding a trench across a parking lot or road. The original FSO bread-and-butter.
2. **Last-mile / middle-mile access.** Connecting a building or cell site to a nearby fiber point of presence without digging; bridging the "last mile" from the fiber backbone to the user. Taara's core market.
3. **Disaster recovery / emergency restoration.** When fiber is cut or infrastructure is destroyed (flood, earthquake, conflict), portable FSO terminals re-establish high-bandwidth links in hours. A recognized emergency-comms tool.
4. **Defense / tactical.** Low-probability-of-intercept, jam-resistant, high-bandwidth links for ISR, command-and-control, and on-the-move operations. NATO names four tactical use classes; QinetiQ and others productize it.
5. **Data-center interconnect (emerging).** Taara is **explicitly sizing the data-center opportunity**: as a bridge for DCs **still waiting on fiber**, and as a **redundant path once fiber arrives** [FACT, COMM-007]. Taara itself flags these conversations as **"early stages"**, i.e. this is a forward-looking, not-yet-proven market, not a track record. (Single-vendor signal, the lead should treat DC-interconnect-via-FSO as nascent.)

**Market size (treat with caution, wide spread):** analyst estimates of the FSO market diverge a lot, from roughly **$0.86B (2025) growing to ~$2.2B by 2030** (CAGR ~20%) at the conservative end, up to **$1.6B to ~$5B by 2030** (CAGR ~26%) and even **30% CAGR** at the aggressive end [ESTIMATE, COMM-010]. The spread reflects differing scope (some include space FSO, some only terrestrial). The directional read, a small but fast-growing market, is robust; the exact dollar figure is not.

---

## 6. How this connects to the broader thesis (neutral pointers, no verdict)

For the shared library, three connections are worth recording without drawing a business conclusion:

1. **Same weather wall, same fix-by-diversity logic.** The ground-to-ground laser and the space-to-ground laser fail for the same physical reason (fog/cloud) and are rescued the same way: a second, weather-independent path (RF backup on the ground; site diversity for the space link). See [`optical_ground_stations.md`](optical_ground_stations.md).
2. **Same latency advantage.** Air/vacuum beats glass by ~47%. [`multi_rack_inference.md`](../llm_compute/multi_rack_inference.md) quantifies this for inter-satellite links; the identical effect is what the HFT industry buys terrestrially. It is a real edge but matters only for latency-sensitive traffic.
3. **The incremental-value framing is reusable.** "Laser wins where fiber can't reach; adds only conditional value (security, latency, fast deploy) where fiber exists" is the same shape of argument that applies to the space-to-ground link competing against terrestrial fiber backbones, and to the communications-business case generally. It is a useful lens for whichever track picks this up.

---

## Sources

Taara (modern high-rate FSO leader):
- [SiliconANGLE, Taara launches Taara Beam (25 Gbps / 10 km)](https://siliconangle.com/2026/02/23/google-x-spinout-taara-launches-taara-beam-deliver-fiber-like-speeds-air/)
- [IEEE Spectrum, Taara free-space optical communication (Lightbridge 20 Gbps / 20 km, ~13 kg, 12+ countries, Congo River)](https://spectrum.ieee.org/free-space-optical-communication-taara)
- [Light Reading, Taara expands into video distribution, sizes up data-center opportunity ("dark fiber in the sky," DC-interconnect, "early stages")](https://www.lightreading.com/wireless/taara-expands-into-video-distribution-sizes-up-data-center-opportunity)
- [Light Reading, Taara's Lightbridge Pro targets 20-Gig](https://www.lightreading.com/wireless/taara-s-lightbridge-pro-wireless-platform-targets-20-gig)
- [Optica OPN, Taara spins out of Alphabet's X (T-Mobile, Airtel, SoftBank, Digicel; 20 countries)](https://www.optica-opn.org/home/industry/2025/march/taara_spins_out_of_alphabet_s_x_to_expand_fso_communications/)
- [The Fast Mode, Taara makes light networks real: 25 Gbps wireless without fiber](https://www.thefastmode.com/technology-solutions/47243-taara-makes-light-networks-real-25-gbps-wireless-without-fiber)
- [5gstore, Taara Beam: 25 Gbps via beams of light](https://5gstore.com/blog/2026/02/25/taara-beam-25gbps-via-beams-of-light/)

Weather, availability, range, and hybrid FSO/RF:
- [Wikipedia, Free-space optical communication (fog 10–100 dB/km; range; use cases; security)](https://en.wikipedia.org/wiki/Free-space_optical_communication)
- [CableFree, FSO Carrier-Class Features (99.999%, hybrid FSO/RF, ~140 m limit)](https://www.cablefree.net/wirelesstechnology/free-space-optics/fso-carrier-class-features/)
- [McMaster/SPIE, Availability of FSO and hybrid FSO/RF systems (140 m / 53 dB budget, RF backup) (PDF)](https://www.ece.mcmaster.ca/faculty/hranilovic/woc/resources/local/spie2001b.pdf)
- [ScienceDirect, Availability of terrestrial FSO link using visibility data, tropical region](https://www.sciencedirect.com/science/article/abs/pii/S0030402617316236)
- [IET Communications, High-speed inter-building connectivity by FSO with RF backup](https://digital-library.theiet.org/doi/abs/10.1049/iet-com.2011.0569)
- [IDST, Hybrid FSO/RF systems improve FSO performance](https://idstch.com/technology/photonics/hybrid-free-space-optics-fso-radio-frequency-rf-communication-systems-can-improve-the-performance-of-free-space-optical-communications/)

Vendors and legacy market:
- [CableFree, Free Space Optics (FSO)](https://www.cablefree.net/cablefree-free-space-optics-fso/)
- [fSONA, Enterprise FSO (SONAbeam)](http://fsona.com/fso-enterprise.php)
- [Gigabit Wireless, Free Space Optics (LightPointe discontinuation, vendor landscape)](https://www.gigabit-wireless.com/tag/free-space-optics/)
- [IRNAS, Koruza open-source FSO (GitHub README)](https://github.com/IRNAS/FSO-systems/blob/master/README.md)

Security / physical-layer:
- [CableFree, FSO Guide (narrow beam ~2 m at 1 km, ~5 m at 5 km; vs microwave footprint)](https://www.cablefree.net/wirelesstechnology/free-space-optics/fso-guide/)
- [ResearchGate, Physical-Layer Security in Free-Space Optical Communications](https://www.researchgate.net/publication/273395337_Physical-Layer_Security_in_Free-Space_Optical_Communications)
- [ResearchPublish, A Comprehensive Review on Security in FSO (eavesdropping/jamming caveats) (PDF)](https://www.researchpublish.com/upload/book/A%20Comprehensive%20Review%20on%20Security-28092024-6.pdf)
- [Optica JLT, Ranging-based phase encryption for enhanced FSO security](https://opg.optica.org/jlt/abstract.cfm?uri=jlt-44-8-2907)
- [QinetiQ, Free Space Optical Communications (defense, low probability of intercept)](https://www.qinetiq.com/en/what-we-do/services-and-products/free-space-optical-communications)
- [NATO STO, Free Space Optical Communication Networks (tactical use cases)](https://www.sto.nato.int/document/free-space-optical-communication-networks-2/)

Latency / HFT precedent (validates the air-vs-glass edge):
- [Gigabit Wireless, Low-latency wireless networks for high-frequency trading](https://www.gigabit-wireless.com/gigabit-wireless/low-latency-wireless-networks-for-high-frequency-trading/)
- [CableFree, Low-latency technology for wireless networks (air ~50% faster than fiber; Chicago–NY >3.5 ms)](https://www.cablefree.net/wirelesstechnology/low-latency-technology/)
- [Fibre Systems, Free-space optics to speed stock exchange](https://www.fibre-systems.com/news/free-space-optics-speed-stock-exchange)

Use cases (disaster recovery, last mile, campus, defense):
- [Axiom Optics, Free-Space Optical Communications (applications)](https://www.axiomoptics.com/application/free-space-optical-communications/)
- [Springer, Disaster management using free-space optical communication system](https://link.springer.com/article/10.1007/s11107-019-00865-9)

Market size:
- [Vynz Research, Free Space Optics Market ($1.9B by 2030, 30% CAGR)](https://www.vynzresearch.com/semiconductor-electronics/free-space-optics-market)
- [360iResearch, Free Space Optics Market 2025–2030 ($0.86B 2025 → $2.19B 2030, 20.5% CAGR)](https://www.360iresearch.com/library/intelligence/free-space-optics)
- [MaximizeMarketResearch, FSO Market ($1.85B 2025 → $4.2B 2032)](https://www.maximizemarketresearch.com/market-report/global-free-space-optics-fso-market/7034/)

(See also project docs: [`laser_comms/optical_ground_stations.md`](optical_ground_stations.md), [`laser_comms/optical_comms.md`](optical_comms.md), [`llm_compute/multi_rack_inference.md`](../llm_compute/multi_rack_inference.md).)

---

## Confidence

**Overall: medium-high.**

- **High** on the existence and core specs of the product class (Taara Beam 25 Gbps / 10 km; Lightbridge 20 Gbps / 20 km; legacy 1 Gbps vendors), multiple independent sources, including the vendor and trade press.
- **High** on the weather constraint and the hybrid-FSO/RF answer, the fog attenuation, the ~140 m five-nines limit, and the RF-backup pattern are consistently reported across engineering sources and match the space-link physics in [`optical_ground_stations.md`](optical_ground_stations.md).
- **Medium-high** on the incremental-value framing ("strong where fiber absent, conditional where fiber present"), well supported by Taara's own positioning and the use-case literature, but it is an analytical synthesis, not a single quoted fact.
- **Medium** on the security differentiator, the beam-spread numbers and the "hard to tap covertly" property are well sourced, but how much a procurement actually values this over encrypted fiber is judgment, not data.
- **Medium / low** on market-size dollars, analyst forecasts span 12% to 30% CAGR and $2B to $5B by 2030 with inconsistent scope; directionally "small but fast-growing," precisely uncertain.

---

## Open Questions

1. **Is the data-center-interconnect use real yet, or just a Taara pitch?** Taara is the only vendor explicitly sizing it, and calls it "early stages." No public production DC-to-DC FSO deployment was found. The lead should treat FSO-for-DC-interconnect as **nascent / aspirational**, not proven.
2. **What is the real five-nines range in a temperate maritime climate?** The ~140 m figure is a worst-case engineering number; Phoenix/Las Vegas push it far out. The relevant number for any specific deployment depends entirely on local fog climatology and needs a site-specific availability study (mirrors the OGS site-selection problem).
3. **Pricing.** No hard per-link or per-km cost figure was obtained (Taara markets "cheaper than fiber for new builds" qualitatively but publishes no price). A vendor quote would be needed to compare laser-link capex against trenched fiber on a real route.
4. **How much is the security edge actually worth?** The physical-layer advantage is real but situational. Whether a data-center or defense buyer pays a premium for "tamper-evident, hard-to-tap" over encrypted fiber is unquantified here.
5. **Does the latency edge ever matter outside HFT?** Air beats glass by ~47%, but for ordinary DC interconnect the absolute saving is sub-millisecond. The set of workloads that would pay for a laser link *for latency alone* (beyond latency-arbitrage trading) is unclear.
6. **Silicon-photonics maturity.** Taara's phased-array chip (fingernail-size, 1,000+ emitters) is the cost/scale lever and is slated to ship by end of 2026. How much it actually drops unit cost and improves availability is unproven as of June 2026.

---

## Claims

| COMM- id | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-001 | Taara Beam terrestrial FSO data rate and range | up to **25 Gbps over up to 10 km (~6.2 mi)** | FACT | [SiliconANGLE](https://siliconangle.com/2026/02/23/google-x-spinout-taara-launches-taara-beam-deliver-fiber-like-speeds-air/), [The Fast Mode](https://www.thefastmode.com/technology-solutions/47243-taara-makes-light-networks-real-25-gbps-wireless-without-fiber), [5gstore](https://5gstore.com/blog/2026/02/25/taara-beam-25gbps-via-beams-of-light/) |
| COMM-002 | Taara Lightbridge rate/range and deployment footprint | **20 Gbps over up to 20 km**; live in **12+ countries** (T-Mobile, Airtel, SoftBank, Digicel) | FACT | [IEEE Spectrum](https://spectrum.ieee.org/free-space-optical-communication-taara), [Optica OPN](https://www.optica-opn.org/home/industry/2025/march/taara_spins_out_of_alphabet_s_x_to_expand_fso_communications/) |
| COMM-003 | Legacy enterprise/metro FSO vendor rate class; LightPointe exit | **~0.1 to 1+ Gbps**, ~km range (fSONA, CableFree, Mostcom, Koruza); LightPointe discontinued its FSO line | FACT | [fSONA](http://fsona.com/fso-enterprise.php), [CableFree](https://www.cablefree.net/cablefree-free-space-optics-fso/), [Gigabit Wireless](https://www.gigabit-wireless.com/tag/free-space-optics/) |
| COMM-004 | Fog (and rain) optical attenuation | **Fog 10 to ~100 dB/km**; rain ~3 to 30 dB/km | FACT | [Wikipedia](https://en.wikipedia.org/wiki/Free-space_optical_communication), [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0030402617316236) |
| COMM-005 | Achievable range vs availability target (pure optical) | **~5 km enterprise-grade; ~140 m for 99.999% (53 dB budget)**, extended in dry climates | FACT | [CableFree](https://www.cablefree.net/wirelesstechnology/free-space-optics/fso-carrier-class-features/), [McMaster/SPIE PDF](https://www.ece.mcmaster.ca/faculty/hranilovic/woc/resources/local/spie2001b.pdf), [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1364682616300876) |
| COMM-006 | Hybrid FSO/RF reaches carrier-grade availability | **99.999%** via optical link + RF backup with automatic failover | FACT | [CableFree](https://www.cablefree.net/wirelesstechnology/free-space-optics/fso-carrier-class-features/), [IET Communications](https://digital-library.theiet.org/doi/abs/10.1049/iet-com.2011.0569), [IDST](https://idstch.com/technology/photonics/hybrid-free-space-optics-fso-radio-frequency-rf-communication-systems-can-improve-the-performance-of-free-space-optical-communications/) |
| COMM-007 | Laser link value vs fiber; deployable in hours, "dark fiber in the sky"; DC-interconnect emerging | Deploy in **hours** vs trench a km of fiber; DC bridge while awaiting fiber and as redundant path ("early stages") | FACT | [Light Reading](https://www.lightreading.com/wireless/taara-expands-into-video-distribution-sizes-up-data-center-opportunity), [IEEE Spectrum](https://spectrum.ieee.org/free-space-optical-communication-taara) |
| COMM-008 | Beam narrowness / interception difficulty | Beam spreads to only **~2 m at 1 km, ~5 m at 5 km**; tap requires being inside the beam path | FACT | [CableFree FSO Guide](https://www.cablefree.net/wirelesstechnology/free-space-optics/fso-guide/), [Wikipedia](https://en.wikipedia.org/wiki/Free-space_optical_communication) |
| COMM-009 | FSO security caveats | Still vulnerable to eavesdropping/jamming when beam footprint >> receiver; physical-layer obscurity, not crypto | FACT | [ResearchPublish review PDF](https://www.researchpublish.com/upload/book/A%20Comprehensive%20Review%20on%20Security-28092024-6.pdf), [ResearchGate](https://www.researchgate.net/publication/273395337_Physical-Layer_Security_in_Free-Space_Optical_Communications) |
| COMM-010 | Terrestrial FSO market size | ~**$0.86B (2025) → $2.2B (2030)** at ~20% CAGR (conservative); up to **~$5B / 30% CAGR** (aggressive); scope varies | ESTIMATE | [360iResearch](https://www.360iresearch.com/library/intelligence/free-space-optics), [Vynz Research](https://www.vynzresearch.com/semiconductor-electronics/free-space-optics-market), [MaximizeMarketResearch](https://www.maximizemarketresearch.com/market-report/global-free-space-optics-fso-market/7034/) |

> **FLAGGED ESTIMATE note:** COMM-010 (market size) is an analyst-forecast range with wide vendor disagreement (12% to 30% CAGR; $2B to $5B by 2030) and inconsistent scope (some include space FSO). Use the direction ("small, fast-growing") not the precise dollar figure. All other claims above are sourced facts; the **incremental-value synthesis in §3 is analytical**, built on sourced inputs but not itself a single quoted number.

> **China aside (excluded from main analysis):** China has an active FSO and laser-comms research and deployment program (academic and commercial), but per the scope rule it is excluded from the analysis above and noted only here.
