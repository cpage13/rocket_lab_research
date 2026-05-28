# A Limited RF Communications Capability — Feasibility Refinement

*Research date: May 2026. Part of the Rocket Lab orbital AI-inference data center feasibility study.
Refines the earlier finding in [`rf_satcom.md`](./rf_satcom.md), which concluded RF spectrum is
"effectively closed to a new entrant."*

---

## Summary / Verdict

The earlier finding was correct **for a mass-market allocation** but **too pessimistic for a
narrow, limited B2B service**. A small RF spectrum sliver is **realistically attainable** for a
new entrant — and the strongest evidence is in Rocket Lab's own backyard: in January 2026 Rocket
Lab *launched the two prototype satellites* that activated the Liechtenstein high-priority Ka-band
filings now held by **Open Cosmos** — a company that, like Rocket Lab, was a satellite *builder*,
not an established telecom operator, until it acquired those filings
([Via Satellite](https://www.satellitetoday.com/connectivity/2026/01/14/open-cosmos-awarded-liechtenstein-spectrum-filings-for-leo-broadband-constellation/),
[Digitimes](https://www.digitimes.com/news/a20260417PD229/leo-data-market-2026-manufacturing.html)).
Open Cosmos's stated strategy — "sovereign LEO networks over mass connectivity," serving
government and enterprise — is almost exactly the limited-B2B concept in this brief.

**What a small sliver buys you (estimate):** a plausible narrow allocation of **~100–250 MHz** of
Ka-band, paired with large, high-gain professional ground antennas, supports on the order of
**a few Gbps of aggregate downlink per satellite-beam**. That is enough to serve **1,000–10,000
professional users** at meaningful (tens-of-Mbps committed, contended) rates — *not* a Starlink,
but a credible "boutique" B2B link. This is **confirmed-feasible in principle** and demonstrated
by multiple comparable ventures (Open Cosmos/ConnectedCosmos ~200 sats; Blue Origin TeraWave
targeting ~100k data-center/telco users).

**Verdict on architecture:** **Yes — retain a modest RF capability alongside the optical
primary.** RF's role is (a) all-weather backup for the optical ground link, (b) TT&C, and
(c) optionally a *low-rate direct B2B channel / out-of-band control plane* for customers when the
optical ground path is clouded out. A small allocation is attainable; a *mass-market* one is not.
The honest caveat: obtaining the sliver still costs **years and real money** (filing,
coordination, a bring-into-use launch within ITU deadlines) — it is attainable, not cheap or
fast. Confidence: **moderate-to-high** on attainability of a sliver; **moderate** on the throughput
estimates (link-budget-dependent, not independently modeled here).

---

## 1. Spectrum Access, Realistically Scoped

The earlier doc framed spectrum as binary ("closed"). It is better understood as a **gradient by
allocation size**. A huge swath for a mass-market constellation is genuinely closed to a 2026
entrant; a narrow sliver for a limited service is not. Five concrete paths exist:

### Path A — Acquire/inherit an existing priority filing (strongest, proven)
The cleanest route is to **take over a lapsed or distressed high-priority ITU filing** rather than
file fresh. This is exactly what happened with the Liechtenstein Ka-band filings: originally
Rivada Space Networks', **rescinded by Liechtenstein's regulator in 2024**, and **reassigned to
Open Cosmos** in January 2026
([Via Satellite](https://www.satellitetoday.com/connectivity/2026/01/14/open-cosmos-awarded-liechtenstein-spectrum-filings-for-leo-broadband-constellation/),
[SatNews — Rivada loses Liechtenstein rights](https://satnews.com/2025/07/20/forresters-digest-rivada-loses-liechtenstein-rights/)).
Small administrations (Liechtenstein, and historically others) act as **filing hosts** and have
priority-dated filings that periodically come free when a holder misses milestones. Inheriting a
filing gives you the **priority date** (the single most valuable asset in ITU coordination)
without the multi-year wait. **Confirmed** path.

### Path B — Lease spectrum / capacity from an existing holder
Satellite spectrum rights are **leasable and transferable**. An active market exists: operators
lease GEO Ka-band capacity to seed service before launching their own LEO craft
([The Fast Mode — SLI Ka-band leasing](https://www.thefastmode.com/technology-solutions/46202-sli-enables-operators-to-access-advanced-ka-band-geo-satellites-via-leasing-terms),
[Global Insight Services — transponder leasing market](https://www.globalinsightservices.com/press-releases/satellite-transponders-leasing-market/)).
In the direct-to-device world, AST SpaceMobile got FCC approval to use AT&T/Verizon spectrum, and
Grain Management expects to lease spectrum to satellite operators within ~90 days of a deal
closing ([Broadband Breakfast](https://broadbandbreakfast.com/grain-aiming-to-lease-direct-to-device-spectrum-90-days-after-deal-closing/)).
Leasing **sidesteps the filing queue entirely** but creates a dependency on the lessor and
recurring cost. **Confirmed** path.

### Path C — Partner with an established satellite operator
Ride an incumbent's existing filing/license as a hosted payload, MVNO-style wholesale
arrangement, or a joint venture. The B2B/D2D market in 2025–26 is built largely on such
partnerships rather than fresh spectrum grabs
([SpaceNews — MSS spectrum/D2D dealmaking](https://spacenews.com/fcc-throws-out-satellite-spectrum-challenges-as-d2d-dealmaking-heats-up/)).
This is the **lowest-regulatory-risk** path but dilutes Rocket Lab's vertical-integration story.
**Confirmed** path.

### Path D — Experimental / non-commercial licenses
FCC Part 5 experimental licenses are **fast and cheap** but **cannot be used for commercial
service** — "licensees are not permitted to provide commercial service, charge fees, or receive
payments," and terms run only 2–5 years
([FCC — Part 5 Experimental Licensing](https://www.fcc.gov/space/part-5-experimental-licensing),
[SpaceNexus — FCC Satellite Licensing Guide 2026](https://spacenexus.us/blog/fcc-satellite-licensing-guide-2026)).
Useful only for **technology demonstration and de-risking a payload** before a Part 25 commercial
filing — not a service path. **Confirmed** limitation.

### Path E — Lightly-used / shared / newly-opened bands
The 2025–26 FCC reforms genuinely change the calculus for *small* allocations. The FCC's
"Satellite Spectrum Abundance" / "Modernizing Spectrum Sharing" proceedings replace the 1990s
EPFD limits with a **performance-based coordination framework** and open upper-microwave bands
(24, 28, 37–40, 47, 50 GHz) to more intensive satellite use
([Federal Register — Modernizing Spectrum Sharing, May 2026](https://www.federalregister.gov/documents/2026/05/13/2026-09565/modernizing-spectrum-sharing-for-satellite-broadband),
[Wilson Sonsini — FCC satellite spectrum sharing framework](https://www.wsgr.com/en/insights/fcc-sets-new-satellite-spectrum-sharing-framework.html),
[Astrolytics — FCC 2026 band reform for smallsat operators](https://astrolytics.space/2025/12/29/expanding-spectrum-access-and-sharing-fccs-2026-band-reform-and-what-smallsat-operators-should-know/)).
A small operator can plausibly secure a narrow shared-band channel **if** it demonstrates
coexistence/interference-management with incumbents and terrestrial users — a real but tractable
engineering task for a *limited* footprint. **Confirmed** direction; outcomes still settling.

### Why narrow ≠ wide
- **Coordination scales with overlap.** ITU coordination burden grows with the number of
  earlier-filed networks whose frequency *and* geographic service area you overlap. A narrow
  channel, modest power, and a **limited service area / limited user count** overlaps fewer
  incumbents and is far easier to coordinate to non-interference than a global mass-market swath.
  *(Inference from the ITU coordination process described in `rf_satcom.md`; not a single cited
  source — flagged as reasoned estimate.)*
- **Milestones are easier to hit.** ITU bring-into-use and 50%/100% deployment milestones (e.g.,
  Liechtenstein's "144 sats by June, 144 more by September" for the 576-sat filing —
  [Digitimes](https://www.digitimes.com/news/a20260417PD229/leo-data-market-2026-manufacturing.html))
  are punishing for a mega-constellation but achievable for a small one — especially for a
  *launch company* that controls its own ride to orbit.
- **Incumbents fight swaths, not slivers.** Incumbent opposition (Globalstar, Iridium, EchoStar
  in MSS) is fiercest where a new entrant threatens core mass-market spectrum
  ([SpaceNews](https://spacenews.com/fcc-throws-out-satellite-spectrum-challenges-as-d2d-dealmaking-heats-up/)).
  A boutique B2B service with bigger antennas and a few thousand users is not a competitive
  threat worth a protracted fight.

**Net:** the earlier "effectively closed" verdict holds for *mass-market*. For a *sliver*,
Paths A, B, and C are all confirmed-viable, and Path E is opening up.

---

## 2. What a Small Sliver Buys You (throughput & user count)

**All figures in this section are estimates** built from cited spectral-efficiency and capacity
data points; they are not an independent link budget.

Reference data points:
- Ka-band spectral efficiency realistically ranges **~0.5 to ~3 bits/s/Hz** depending on
  modulation/coding and link margin; 250 MHz at 3 bits/s/Hz ≈ **750 Mbps**, and a 16-APSK LDPC
  link achieved **775 Mbps** over a Ka-band relay channel
  ([NASA — Bandwidth-Efficient Ka-band Relay](https://ntrs.nasa.gov/api/citations/20170001297/downloads/20170001297.pdf)).
- A LEO satellite with **400 MHz** of Ka-band serving VSATs has a downlink capacity of
  **~7 Gbps** ([satsig.net — Ka-band capacity](https://www.satsig.net/ka-band/ka-band-satellites.htm)).
- HTS spot beams use **50–600 MHz per beam** with frequency reuse up to ~20×
  ([SatMagazine — Ka-Band Capacity Planning](http://www.satmagazine.com/story.php?number=192941478)).

**Plausible limited allocation:** assume a sliver of **~100–250 MHz** of Ka-band (the kind of
narrow channel attainable via Paths A/B/E).

| Allocation | Spectral efficiency assumed | Aggregate downlink (per beam/sat) |
|---|---|---|
| 100 MHz | 2 bits/s/Hz | ~0.2 Gbps |
| 250 MHz | 3 bits/s/Hz (large high-gain ground antenna, good margin) | ~0.75 Gbps |
| 250 MHz, modest frequency reuse (~4×) across a small constellation | 3 bits/s/Hz | ~3 Gbps aggregate |

**The large-antenna advantage is real and material.** Because the B2B use case permits
professional ground terminals (e.g., 1–2.4 m dishes, not phone-sized), the link operates at
**high G/T and high SNR**, pushing toward the **3 bits/s/Hz** end and improving rain-fade margin.
A teleport-class antenna has very high gain and effectively unlimited power
([Qorvo — link budget review](https://www.qorvo.com/design-hub/blog/designing-efficient-satellite-links-a-review-of-the-link-budget-analysis)).
This is the single biggest reason a *limited* service is more efficient per-MHz than a
direct-to-phone service.

**User count:** with ~1–3 Gbps aggregate and B2B contention typical of enterprise VSAT
(capacity is shared — e.g., "30 VSATs may share the same 512k/64k" at the low end, but enterprise
service is provisioned far higher —
[satsig.net VSAT intro](https://www.satsig.net/vsat_int.htm)):
- At a **committed ~1–5 Mbps per professional user** with reasonable oversubscription,
  ~1–3 Gbps comfortably serves the **1,000–10,000 simultaneous-ish users** in the brief.
- This is **not** broadband-for-everyone; it is a **dedicated, provisioned enterprise link** —
  exactly the boutique profile intended.

**Estimate, flagged as such.** Confidence: moderate. A real link budget (antenna sizes, satellite
EIRP, rain zone, elevation angle, constellation geometry) should be run before committing
numbers to a customer-facing spec — see Open Questions.

---

## 3. RF's Genuine Advantages for a Direct Link

RF's edge over the optical primary (consistent with `rf_satcom.md`'s head-to-head):

1. **Penetrates clouds.** RF suffers only graceful rain fade; it does not *drop* in cloud/fog the
   way an optical link does. This is decisive for an **all-weather backup to the optical ground
   link**.
2. **Simpler, cheaper, more rugged ground terminals.** Wide RF beams need no microradian pointing,
   no adaptive optics, no multi-second acquisition. A professional Ka VSAT is a commodity-ish,
   field-deployable product. A customer can stand one up where an optical ground station is
   impractical.
3. **Works in motion / works anywhere.** RF terminals function on moving platforms (maritime,
   aviation, vehicles) and at sites with no clear-sky guarantee — broadening the addressable B2B
   footprint beyond what optical ground stations alone can reach.
4. **Mature, low-risk, flight-proven.** Decades of operational heritage; no acquisition-failure
   modes.

**Where a modest RF capability genuinely adds value in this architecture:**
- **All-weather backup for the optical ground link** *(highest value)* — carries priority traffic
  when optical ground stations are clouded out, lifting overall service availability. Already
  endorsed in `rf_satcom.md`; the refinement is that the same RF asset can do double duty.
- **Direct low-rate B2B channel / out-of-band control plane** — a modest RF link lets customers
  reach the data center directly (job submission, results, telemetry, management) without an
  optical ground station, and serves as an independent control plane if the optical path is down.
- **TT&C** — standard practice; keep RF here regardless.

RF is **not** the primary customer data highway — optical remains that. RF is the resilient,
weather-proof, simple-terminal complement.

---

## 4. LEO vs GEO for This RF Service

| | GEO | LEO |
|---|---|---|
| Latency (one-way) | ~120 ms; round-trip ~240–500 ms+ | ~20–50 ms round-trip |
| Coverage | Continuous from a single satellite | Needs a constellation for continuous coverage |
| Path loss / EIRP demand | Very high (35,786 km) | Much lower (~550 km) |
| Suits real-time apps | Poorly — "GEO cannot deliver the low latency modern apps need" | Yes |

Sources: [Telarus — LEO/MEO/GEO explained](https://www.telarus.com/blog/modern-satellite-connectivity-explained/),
[Via Satellite — GEO/MEO/LEO](https://www.satellitetoday.com/content-collection/ses-hub-geo-meo-and-leo/),
[Telesat — LEO reshaping enterprise telecom](https://www.telesat.com/blog/from-last-resort-to-crucial-partner-how-leo-networks-are-reshaping-enterprise-telecom/).

**Recommendation: LEO.** Three reasons:
1. **The data center is itself a LEO constellation.** The RF payload should fly on the same
   satellites — co-located with the compute, no separate GEO program, no separate spacecraft bus.
2. **Latency.** An AI-inference service benefits from low round-trip time; GEO's ~half-second
   round trip is a poor fit for an interactive B2B compute service.
3. **Path loss / terminal size.** LEO's far lower path loss keeps ground terminals modest even at
   the high-gain end, and keeps satellite EIRP demands compatible with a smallsat bus.

GEO's only genuine advantage — continuous coverage from one satellite — is moot, because the
constellation already exists for the optical mesh. A modest RF payload **rides the LEO
constellation Rocket Lab is already building.** (A handful of beams need not cover the globe
continuously; a limited B2B service can tolerate scheduled or regional coverage.)

---

## 5. The "Limited Starlink for Business" Concept

**Is a small-scale B2B satellite broadband service (1k–10k users, larger antennas) feasible for a
new entrant? Yes — and it is a recognized 2025–26 market category.** Multiple new entrants are
explicitly pursuing exactly this niche rather than competing with Starlink on mass market:

- **Open Cosmos / ConnectedCosmos** — a satellite *builder* turned operator, ~200-satellite
  Ka-band LEO constellation, "sovereign LEO networks over mass connectivity," targeting
  **government and enterprise** customers
  ([Digitimes](https://www.digitimes.com/news/a20260417PD229/leo-data-market-2026-manufacturing.html),
  [Via Satellite](https://www.satellitetoday.com/connectivity/2026/01/14/open-cosmos-awarded-liechtenstein-spectrum-filings-for-leo-broadband-constellation/)).
- **Blue Origin TeraWave** — explicitly targeting **~100,000 users** (data centers, telcos, cloud
  providers, governments) needing fiber-comparable links — i.e., a deliberately *bounded* user
  base
  ([Connectasat — enterprise satellite internet 2025–26](https://www.connectasat.com/insights/enterprise-satellite-internet-hits-its-inflection-point-and-the-race-is-on/)).
- **Eutelsat/OneWeb** — deliberately B2B/government, "distinct from Starlink's mass-market
  consumer focus" ([Kavout — Eutelsat LEO strategy](https://www.kavout.com/market-lens/is-eutelsat-s-leo-strategy-a-viable-counter-to-spacex-s-dominance)).
- New players **Logos Space, SpinLaunch's Meridian Space** — niche enterprise/government plays.

The dominant strategy among smaller operators in 2025–26 is **exactly** targeting regulated
industries, government, and enterprise verticals — differentiating on **security, sovereignty,
reliability, interoperability**, not raw bandwidth
([Via Satellite — Coming Wave of Competition in LEO](https://interactive.satellitetoday.com/via/march-2026/the-coming-wave-of-competition-in-leo-constellations)).

**What it would realistically take for Rocket Lab:**
1. **Spectrum** — acquire/inherit a priority filing (Path A) or lease (Path B). Realistic but
   takes negotiation and likely 1–3 years; an ITU bring-into-use launch must hit milestones.
2. **RF payload** — a Ka-band payload on the LEO data-center satellites. Modest mass/power vs. a
   dedicated telecom satellite.
3. **Ground segment** — professional VSAT terminals (commodity-adjacent) plus gateway/teleport.
4. **Capital** — manageable. Cumulative *industry* investment in LEO broadband + D2D is ~$10B
   *across all players since 2019* ([Deloitte — next-gen satellite internet](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/next-gen-satellite-internet.html));
   SpinLaunch raised just **$30M** to *start* a 280-microsat constellation
   ([Via Satellite — SpinLaunch $30M](https://www.satellitetoday.com/connectivity/2025/08/18/spinlaunch-raises-30m-for-leo-constellation-meridian-space/)).
   A *limited* RF capability bolted onto an already-funded data-center constellation is a small
   marginal cost.
5. **Strategic fit** — Rocket Lab builds satellites and launches them, and *already launched the
   Open Cosmos prototype satellites* for these exact filings. The capability and supply chain
   exist in-house.

**Regulatory feasibility: yes, for a limited footprint.** Technical feasibility: yes. The honest
constraint is **time and milestone risk**, not impossibility.

---

## 6. Verdict

**Retain a modest RF capability alongside the optical primary — and a small spectrum sliver is
realistically attainable.** This refines, rather than overturns, `rf_satcom.md`:

- **Mass-market RF spectrum: still closed.** A new entrant cannot win enough licensed,
  interference-free, globally usable spectrum to run a Starlink-scale primary backbone.
  `rf_satcom.md`'s conclusion stands here.
- **A narrow sliver for a limited B2B service: attainable.** Via inheriting a distressed priority
  filing (proven — Open Cosmos), leasing, partnering, or the newly opening shared bands. The
  difficulty is genuinely *lower* for a narrow channel + limited service area than for a swath.
- **What it buys:** roughly **0.2–3 Gbps aggregate** per satellite/beam from a ~100–250 MHz
  sliver — enough for **1,000–10,000 professional B2B users** with large high-gain antennas at
  provisioned enterprise rates. *(Estimate — needs a real link budget.)*
- **Architecture recommendation:** **optical primary + a modest LEO RF payload.** The RF payload
  serves three roles — all-weather backup for the optical ground link, a direct low-rate B2B
  channel / out-of-band control plane, and TT&C. It rides the constellation already being built.

**Honest caveats:** (1) Securing the sliver still costs **years and capital** — attainable, not
free or fast; (2) ITU bring-into-use/deployment milestones impose schedule risk (mitigated by
Rocket Lab owning its launch); (3) the throughput numbers are estimates pending a real link
budget; (4) the RF capability should remain *limited and complementary* — the moment it is scoped
toward mass market, `rf_satcom.md`'s "closed" verdict reasserts itself.

**Confidence:** moderate-to-high that a small sliver is attainable (multiple proven precedents,
strongest being Open Cosmos which Rocket Lab itself launched); moderate on the throughput/user
estimates (link-budget-dependent).

---

## Sources

- [Via Satellite — Open Cosmos Awarded Liechtenstein Spectrum Filings](https://www.satellitetoday.com/connectivity/2026/01/14/open-cosmos-awarded-liechtenstein-spectrum-filings-for-leo-broadband-constellation/)
- [Digitimes — Open Cosmos wins Ka-band spectrum, targets sovereign LEO networks](https://www.digitimes.com/news/a20260417PD229/leo-data-market-2026-manufacturing.html)
- [SatNews — Rivada loses Liechtenstein rights](https://satnews.com/2025/07/20/forresters-digest-rivada-loses-liechtenstein-rights/)
- [Space Intel Report — Can Open Cosmos meet 2026/2028 ITU deadlines](https://www.spaceintelreport.com/can-open-cosmos-field-a-broadband-constellation-to-meet-2026-and-2028-itu-deadlines-liechtenstein-regulator-says-yes/)
- [The Fast Mode — SLI enables Ka-band GEO access via leasing](https://www.thefastmode.com/technology-solutions/46202-sli-enables-operators-to-access-advanced-ka-band-geo-satellites-via-leasing-terms)
- [Global Insight Services — Satellite Transponder Leasing Market](https://www.globalinsightservices.com/press-releases/satellite-transponders-leasing-market/)
- [Broadband Breakfast — Grain aiming to lease D2D spectrum](https://broadbandbreakfast.com/grain-aiming-to-lease-direct-to-device-spectrum-90-days-after-deal-closing/)
- [SpaceNews — FCC throws out satellite spectrum challenges as D2D dealmaking heats up](https://spacenews.com/fcc-throws-out-satellite-spectrum-challenges-as-d2d-dealmaking-heats-up/)
- [FCC — Part 5 Experimental Licensing](https://www.fcc.gov/space/part-5-experimental-licensing)
- [SpaceNexus — FCC Satellite Licensing Guide 2026](https://spacenexus.us/blog/fcc-satellite-licensing-guide-2026)
- [Federal Register — Modernizing Spectrum Sharing for Satellite Broadband (May 2026)](https://www.federalregister.gov/documents/2026/05/13/2026-09565/modernizing-spectrum-sharing-for-satellite-broadband)
- [Wilson Sonsini — FCC Sets New Satellite Spectrum Sharing Framework](https://www.wsgr.com/en/insights/fcc-sets-new-satellite-spectrum-sharing-framework.html)
- [Astrolytics — FCC 2026 Band Reform and SmallSat Operators](https://astrolytics.space/2025/12/29/expanding-spectrum-access-and-sharing-fccs-2026-band-reform-and-what-smallsat-operators-should-know/)
- [NASA — Bandwidth-Efficient Communication through 225 MHz Ka-band Relay Satellite Channel](https://ntrs.nasa.gov/api/citations/20170001297/downloads/20170001297.pdf)
- [satsig.net — Ka-band satellites worldwide / capacity](https://www.satsig.net/ka-band/ka-band-satellites.htm)
- [satsig.net — Introduction to VSAT terminals](https://www.satsig.net/vsat_int.htm)
- [SatMagazine — Ka-Band Capacity Planning](http://www.satmagazine.com/story.php?number=192941478)
- [Qorvo — Designing Efficient Satellite Links: Link Budget Analysis](https://www.qorvo.com/design-hub/blog/designing-efficient-satellite-links-a-review-of-the-link-budget-analysis)
- [Telarus — Modern Satellite Connectivity Explained (LEO/MEO/GEO)](https://www.telarus.com/blog/modern-satellite-connectivity-explained/)
- [Via Satellite — GEO, MEO, and LEO](https://www.satellitetoday.com/content-collection/ses-hub-geo-meo-and-leo/)
- [Telesat — LEO networks reshaping enterprise telecom](https://www.telesat.com/blog/from-last-resort-to-crucial-partner-how-leo-networks-are-reshaping-enterprise-telecom/)
- [Connectasat — Enterprise Satellite Internet 2025–2026](https://www.connectasat.com/insights/enterprise-satellite-internet-hits-its-inflection-point-and-the-race-is-on/)
- [Kavout — Is Eutelsat's LEO Strategy a Viable Counter to SpaceX](https://www.kavout.com/market-lens/is-eutelsat-s-leo-strategy-a-viable-counter-to-spacex-s-dominance)
- [Via Satellite — The Coming Wave of Competition in LEO Constellations (March 2026)](https://interactive.satellitetoday.com/via/march-2026/the-coming-wave-of-competition-in-leo-constellations)
- [Via Satellite — SpinLaunch Raises $30M for Meridian Space](https://www.satellitetoday.com/connectivity/2025/08/18/spinlaunch-raises-30m-for-leo-constellation-meridian-space/)
- [Deloitte — Next-gen satellite internet (2026 predictions)](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/next-gen-satellite-internet.html)

## Open Questions / Uncertainties

- **Which specific filing or band?** This refinement establishes that a sliver is *attainable*;
  it does not identify the exact filing to acquire or band to target. A dedicated filings-and-
  coordination analysis (which distressed priority filings exist, lease availability, costs) is
  the obvious next step.
- **Real link budget needed.** The 0.2–3 Gbps and 1k–10k-user figures are estimates from cited
  spectral-efficiency data, not an independent link budget. Antenna sizes, satellite EIRP, rain
  zone, elevation angles, and constellation geometry must be modeled before any customer-facing
  spec.
- **Coverage model for a limited LEO RF service.** A handful of RF beams will not give continuous
  global coverage; the acceptable coverage pattern (regional, scheduled, follow-the-customer)
  needs definition and affects user-count math.
- **ITU milestone risk.** Inheriting a priority filing means inheriting its bring-into-use and
  deployment deadlines. Whether Rocket Lab's launch cadence comfortably clears them depends on
  the specific filing — flagged but not resolved.
- **Make-vs-partner decision.** Acquiring a filing (Path A) maximizes vertical integration but
  carries milestone risk; partnering (Path C) de-risks regulation but dilutes ownership. A
  business-model call, not a technical one — see `economics/` workstream.
- **Cost not quantified.** The marginal cost of an RF payload + ground segment on the existing
  constellation is described as "small" but not modeled. Defer to `economics/`.
