# RF Satellite Communications & Laser-vs-RF Comparison

*Research date: May 2026. Part of the Rocket Lab orbital AI-inference data center feasibility study.*

## Summary

Conventional RF satellite comms is mature and weather-robust but **fundamentally bandwidth-limited
and regulation-constrained**. Modern Ka-band high-throughput satellites deliver ~**500 Gbps per
spacecraft**; next-gen V-band systems target ~**1.5 Tbps** — impressive, but those are large
purpose-built telecom satellites, and the capacity is shared spectrum. The decisive issue for
Rocket Lab is **spectrum access**: usable RF bands (Ka, V) are a finite, internationally
coordinated resource allocated on a **first-come-first-served** basis through the ITU, with
**coordination against incumbents (SpaceX, Amazon Kuiper, OneWorldOnline/Eutelsat, etc.) taking
years**. The working assumption — that Rocket Lab would *not* obtain significant RF spectrum — is
**broadly correct**: a new entrant can get *some* spectrum, but not enough, fast enough, or
interference-free enough to be a primary data-center backbone.

**Verdict: the orbital data center should rely on laser (optical) comms as its primary backbone
and ground link.** RF has a real but limited role — telemetry/tracking/command (TT&C), and a
low-rate weather backup for the ground link when optical ground stations are clouded out. RF is a
safety net, not the highway.

---

## 1. RF Satellite Communications

### Spectrum bands

| Band | Frequency | Typical use | Relevance here |
|---|---|---|---|
| Ku-band | 12–18 GHz | Legacy broadband, TV | Congested, mostly GEO incumbents |
| **Ka-band** | 26.5–40 GHz | Modern HTS, Starlink/Kuiper user links | Dominant HTS band; heavily contested |
| **V-band** | 40–75 GHz | Next-gen HTS, NGSO constellations | More capacity, more rain fade; FCC opening 36–51.4 GHz for non-gov use |
| W-band | 75–110 GHz | Experimental | FCC seeking comment; immature |

Sources: [Wikipedia — Ka band](https://en.wikipedia.org/wiki/Ka_band),
[Holland & Knight — FCC Upper Microwave Rulemaking](https://www.hklaw.com/en/insights/publications/2025/11/fcc-rulemaking-on-space-station-licensing-and-spectrum-sharing).

### Throughput per satellite

- **Ka-band HTS:** large modern spacecraft now deliver **~500 Gbps per satellite**; the biggest
  systems exceed 1 Tbps. ViaSat-1 (2011) delivered 140 Gbps for historical scale
  ([Wikipedia — High-throughput satellite](https://en.wikipedia.org/wiki/High-throughput_satellite),
  [AD Little — High Throughput Satellites](https://www.adlittle.com/sites/default/files/viewpoints/ADL_High_Throughput_Satellites-Viewpoint.pdf)).
- **V-band:** next-generation systems **target ~1.5 Tbps** capacity
  ([Wikipedia — High-throughput satellite](https://en.wikipedia.org/wiki/High-throughput_satellite)).
- **LEO V/Ka demos:** GalaxySpace's YINHE-1, the first V/Ka LEO broadband satellite, had a
  ~24 Gbps communication capacity — representative of an *early LEO* node, not a flagship HTS
  ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0094576522004933)).

> Note: HTS "per-satellite" capacity is **shared across many spot beams and users** and is a
> regulated/coordinated resource. It is not directly comparable to a dedicated point-to-point
> optical link. A realistic per-link RF channel for a new entrant is far smaller than these
> headline numbers.

### Weather

RF degrades gracefully — Ka/V-band suffer **rain fade** (V-band worse), mitigated with margin,
adaptive coding, and ground-station diversity, but the link **does not drop the way an optical
link does in cloud**. This all-weather robustness is RF's single biggest advantage over optical.

---

## 2. Spectrum Access / Regulation — the Hard Constraint

Getting *significant* RF spectrum is the gating regulatory problem, and it is severe for a new
entrant:

- **ITU first-come-first-served.** Most bands (incl. Ka, V) are allocated via a priority-date
  "coordination before use" process. A new filer must **negotiate non-interference agreements with
  every earlier-filed network** whose service area/frequencies overlap
  ([Lexology — ITU and Access to Spectrum](https://www.lexology.com/library/detail.aspx?g=b5be7a4e-06c4-4f19-b68c-a5fb09b6a6a4),
  [ITU regulatory framework](https://www.itu.int/en/ITU-R/space/snl/Documents/ITU-Space_reg.pdf)).
- **Incumbents already hold the good spectrum.** Starlink, Amazon Kuiper, Eutelsat/OneWeb, Telesat
  and GEO operators filed years ago. A 2026 entrant is **junior in priority** and must protect all
  of them — meaning accepting interference constraints, reduced power, or restricted geographies.
- **Coordination takes years.** The FCC itself acknowledges approvals "often take years" under an
  uncertain process, with a backlog of duplicative NGSO filings
  ([Law & Economics Center](https://laweconcenter.org/resources/satellite-spectrum-policy-changes-are-needed/),
  [FCC blog — Spectrum Is Back Again](https://www.fcc.gov/news-events/blog/2025/04/04/spectrum-back-again)).
- **ITU 7-year bring-into-use deadline.** Filings lapse if the system is not in service within
  7 years — adding schedule pressure
  ([ITU regulatory framework](https://www.itu.int/en/ITU-R/space/snl/Documents/ITU-Space_reg.pdf)).
- **Regulatory regime is in flux (2025–2026).** The FCC is overhauling NGSO spectrum sharing and
  proposing new "Part 100" licensing rules and opening V-band (36–51.4 GHz) for non-government
  use ([Federal Register — Satellite Spectrum Abundance](https://www.federalregister.gov/documents/2025/06/27/2025-11966/satellite-spectrum-abundance),
  [Holland & Knight](https://www.hklaw.com/en/insights/publications/2025/11/fcc-rulemaking-on-space-station-licensing-and-spectrum-sharing)).
  This *could* help a new entrant — but the reforms are unfinished, and new V-band capacity will be
  contested by the same incumbents.

**Assessment:** the working assumption holds. Rocket Lab could plausibly secure *modest* RF
spectrum — enough for TT&C and a narrowband backup link — but **not enough licensed, interference-
free, globally usable spectrum to serve as the primary data pipe** for a commercial data center.
Spectrum is the wrong battle for a new entrant to fight. Optical sidesteps it entirely:
**optical frequencies require no spectrum license.**

---

## 3. Head-to-Head: Laser (Optical) vs RF

| Dimension | Laser / Optical | RF (Ka/V-band) | Edge |
|---|---|---|---|
| Per-link bandwidth | 100–200 Gbps proven (Starlink ISL, NASA TBIRD); Tbps-class roadmap | ~500 Gbps/sat Ka, ~1.5 Tbps V-band — but **shared** across beams/users | **Optical** for dedicated point-to-point |
| Regulatory burden | **None** — unlicensed optical frequencies | **Severe** — ITU/FCC coordination, years, junior priority, incumbent interference | **Optical** (decisive) |
| Weather sensitivity | High — cloud/fog/rain **break** the link; needs OGS diversity | Low — rain fade only, degrades gracefully, doesn't drop | **RF** |
| Terminal mass / power / size | Lower; receivers far smaller than RF antennas | Higher mass/power for equivalent capacity | **Optical** |
| Pointing complexity | High — microradian pointing, multi-second acquisition, adaptive optics, moving parts | Low — wide RF beams, simple acquisition | **RF** |
| Interference / security | Narrow beam: no interference, hard to intercept | Wide beam: interference-prone, easier to intercept/jam | **Optical** |
| Maturity | Proven at scale (Starlink 9,000+ sats; Mynaric 100+ terminals) but ground-link ops still maturing | Decades of operational heritage; fully mature | **RF** slightly; both flight-proven |

Sources: [NASA — Comparative Study of Optical and RF Communications](https://ntrs.nasa.gov/api/citations/20040191349/downloads/20040191349.pdf),
[ts2.tech — Lasers vs Radio 2025](https://ts2.tech/en/lasers-vs-radio-inside-the-laser-satellite-communication-revolution-2025/),
[Yesway — Optical SatComms vs RF](https://yesway.co.uk/optical-satellite-communications/).

### Conclusion

**The orbital data center should rely on laser/optical comms as its primary architecture** — for
both the inter-satellite mesh and the ground links — for three reasons that dominate:

1. **No spectrum licensing.** As a new entrant Rocket Lab cannot realistically win enough RF
   spectrum to run a primary backbone. Optical removes that fight entirely. This alone is decisive.
2. **Bandwidth.** Dedicated optical links deliver 100–200 Gbps+ today with multi-Tbps headroom;
   contested shared RF cannot match this per-link for a new entrant.
3. **Strategic fit.** Rocket Lab now owns Mynaric — optical is the in-house, vertically-integrated
   capability.

**RF still has a role — as backup and housekeeping, not the highway:**

- **TT&C** (telemetry, tracking, command): low-rate, all-weather, standard practice — keep RF here.
- **Weather-backup ground link:** a modest RF downlink can carry priority/low-rate traffic when
  optical ground stations are clouded out, improving overall service availability. This needs only
  a small, achievable spectrum allocation — within reach for a new entrant.
- RF is **not** viable as the primary customer-traffic pipe: bandwidth-limited and spectrum-gated.

Net: **optical primary + RF backup/TT&C** is the recommended communications architecture.

---

## Sources

- [Wikipedia — Ka band](https://en.wikipedia.org/wiki/Ka_band)
- [Wikipedia — High-throughput satellite](https://en.wikipedia.org/wiki/High-throughput_satellite)
- [AD Little — High Throughput Satellites: Delivering future capacity needs](https://www.adlittle.com/sites/default/files/viewpoints/ADL_High_Throughput_Satellites-Viewpoint.pdf)
- [ScienceDirect — V/Ka-band LEO HTS experiment, flight results](https://www.sciencedirect.com/science/article/abs/pii/S0094576522004933)
- [Lexology — Space Law: ITU and Access to Spectrum](https://www.lexology.com/library/detail.aspx?g=b5be7a4e-06c4-4f19-b68c-a5fb09b6a6a4)
- [ITU — Radio Regulatory Framework for Space Services](https://www.itu.int/en/ITU-R/space/snl/Documents/ITU-Space_reg.pdf)
- [Law & Economics Center — Satellite-Spectrum Policy Changes Are Needed](https://laweconcenter.org/resources/satellite-spectrum-policy-changes-are-needed/)
- [FCC — Spectrum Is Back Again (blog, Apr 2025)](https://www.fcc.gov/news-events/blog/2025/04/04/spectrum-back-again)
- [Federal Register — Satellite Spectrum Abundance](https://www.federalregister.gov/documents/2025/06/27/2025-11966/satellite-spectrum-abundance)
- [Holland & Knight — FCC Rulemaking on Space Station Licensing and Spectrum Sharing](https://www.hklaw.com/en/insights/publications/2025/11/fcc-rulemaking-on-space-station-licensing-and-spectrum-sharing)
- [NASA — Comparative Study of Optical and RF Communications](https://ntrs.nasa.gov/api/citations/20040191349/downloads/20040191349.pdf)
- [ts2.tech — Lasers vs Radio: Laser Satellite Communication Revolution 2025](https://ts2.tech/en/lasers-vs-radio-inside-the-laser-satellite-communication-revolution-2025/)
- [Yesway — Optical Satellite Communications: Laser Links vs RF](https://yesway.co.uk/optical-satellite-communications/)

## Open Questions / Uncertainties

- **How much RF spectrum could Rocket Lab realistically secure, and in which band?** Enough for
  TT&C is near-certain; a meaningful backup downlink needs a specific filing analysis.
- **Will the 2025–2026 FCC "Part 100" / V-band reforms materially lower the barrier?** The rules
  are unfinished; outcome and timing are uncertain.
- **Per-link vs shared capacity** — HTS "500 Gbps/satellite" headline figures are shared across
  beams/users; a realistic dedicated RF channel for a new entrant is much smaller and should be
  modeled before any RF-primary scenario is even considered.
- **Jamming/resilience** — for any government/defense customer angle, RF's jam-susceptibility vs
  optical's narrow-beam security may affect the architecture and is not analyzed here.
- **Cost** — RF vs optical terminal and ground-segment cost comparison is not quantified here;
  see `economics/` workstream.
