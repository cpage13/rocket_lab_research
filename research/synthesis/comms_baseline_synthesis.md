# Communications Baseline Synthesis: Markets and the Current State of the Technologies

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:** this is a SYNTHESIS that pulls together the communications wave-1 ingest docs and the existing comms corpus. It cites them by path and does not repeat their derivations. The load-bearing inputs are:

- Markets: [comms_us_broadband_market.md](../economics/comms_us_broadband_market.md), [comms_us_cellular_market.md](../economics/comms_us_cellular_market.md), [comms_global_regional_market.md](../economics/comms_global_regional_market.md), [comms_space_tam_claims.md](../economics/comms_space_tam_claims.md).
- Deployment economics (the cost side that underpins the diminishing-returns and DC-comparison sections): [comms_broadband_deployment_economics.md](../economics/comms_broadband_deployment_economics.md), [comms_cellular_5g_deployment_economics.md](../economics/comms_cellular_5g_deployment_economics.md).
- Technology: [spectrum_fundamentals_economics.md](../direct_communication/spectrum_fundamentals_economics.md), [bands_and_enabling_hardware.md](../direct_communication/bands_and_enabling_hardware.md), [rf_satcom.md](../laser_comms/rf_satcom.md), [rf_limited_service.md](../laser_comms/rf_limited_service.md), [optical_comms.md](../laser_comms/optical_comms.md), [optical_ground_stations.md](../laser_comms/optical_ground_stations.md), [laser_terrestrial_interconnect.md](../laser_comms/laser_terrestrial_interconnect.md), [constellation_mesh.md](../laser_comms/constellation_mesh.md).
- Rocket Lab assets and the existing scoped business case: [space_hardware_capabilities.md](../rocket_lab/space_hardware_capabilities.md), [comms_business_case.md](../laser_comms/comms_business_case.md).
- Competitor cadence context (the data-center vs comms timeline aside): [falcon9_cadence_ramp.md](../competitors/falcon9_cadence_ramp.md), [starship_addendum.md](../competitors/starship_addendum.md).

> **Reading guide.** Every hard number is tagged **[FACT]** (reported / filed 2025-26 data), **[ESTIMATE]** (market-research sizing or our own arithmetic), or **[PROJECTION]** (forward forecast / illustrative ceiling). Numbers carry their source doc inline; the underlying 2+ source citations live in those docs and are not re-pasted. Single-source figures are flagged.

> **Scope.** This synthesis is ISOLATED TO COMMUNICATIONS. It draws from the shared library but targets only the communications outcome. **No verdict on the Rocket Lab comms business is offered here.** The working hypotheses live in the companion thesis ([comms_thesis.md](../vision/comms_thesis.md)); this doc is the neutral base. **China is excluded** from all totals and noted only as a labelled aside where relevant.

> **Claim-ID note for the lead.** The ten ingest docs each restart their COMM- claim numbering at COMM-001, so the IDs collide across docs. To avoid adding to that collision, this synthesis uses a separate **COMM-S##** namespace in its own claims table. The lead reconciles all of these into the shared SOURCE_INDEX.

---

## Summary / Verdict

**Confidence: medium-high on the market base and the technology state; medium on the per-region dollar splits; low (by design) on the illustrative addressable framings.**

The communications base has five headline findings.

1. **The market is enormous, mobile-dominated, mature, and barely growing.** Consumer connectivity (mobile plus fixed broadband) is roughly **$1.55T/year global** / **~$1.2-1.3T ex-China** [ESTIMATE]; the broad all-services market (adding enterprise, wholesale, and voice) is roughly **$2.0-2.1 trillion/year global** / **~$1.6-1.7T ex-China** [ESTIMATE]. It splits very unequally: **mobile/cellular ~$1.19T** [FACT, GSMA, global series] versus **fixed broadband ~$360-390B** [ESTIMATE, global series], with enterprise/wholesale/voice making up the rest. The US alone is about a quarter of the global market: **US wireless service ~$326B** [ESTIMATE, single major source] and **US fixed broadband ~$70-95B** [ESTIMATE]. Top-line growth is low single digits everywhere in the developed world.

2. **The ground carriers are huge but de-rated, and the largest subscriber bases carry the smallest market caps.** The investor value sits with the wireless balance sheets (T-Mobile ~$216B, Verizon ~$191-201B, AT&T ~$156-160B), while the pure-play broadband operators with the biggest subscriber counts are valued lowest (Charter ~$20B against ~$55B revenue and ~30M subscribers). A new entrant selling connectivity is entering a market whose incumbents' core product is flat-to-shrinking.

3. **Diminishing returns past baseline broadband is the most robust finding in the whole base.** Willingness-to-pay for speed is sharply concave: about **$2.34 per Mbps** at the low end (4 to 10 Mbps) collapsing to about **$0.02 per Mbps** from 100 to 1,000 Mbps [FACT]. Gigabit is available to over 91% of US homes but only about 30% buy it [FACT]; the modal household sits at 200-500 Mbps and refuses the premium. ARPU is flat-to-declining. The value curve rewards **reach and reliability, not raw bandwidth** past a low-hundreds-of-Mbps threshold.

4. **The addressable market for space depends entirely on which number you cite, and the honest one is far smaller than the headline.** Cited space-comms TAMs run to the trillions (SpaceX connectivity **$1.6T**, AST **$1.1T**). Independent bottoms-up sizing lands roughly **two orders of magnitude lower**: Morningstar's realistic Starlink-served market is about **$129B** globally [PROJECTION], and the cross-analyst consensus is that the served market is about **5-10% of the cited total** (the "90% haircut"). Space holds about **0.5% of global fixed broadband subscribers today** [FACT].

5. **The technology base has no physics wall, but it has clear shape: optical wins on bandwidth and (decisively) on no-spectrum-fight; RF wins on weather and mobility; spectrum is the binding constraint and the chips are not.** Through W-band the enabling silicon is already off-the-shelf or near-it; the binding constraint is spectrum coordination, rain fade, and pointing, not chip development. For a new entrant, terrestrial cellular spectrum is effectively closed (the last greenfield mid-band slice, US C-band, cost **$81B**), while a narrow satellite spectrum sliver is attainable through a different regulatory door.

The founder's central comparison falls out of points 3 and 4: **data centers justify premium economics (continual hardware upgrades, demand outrunning supply, rapid capacity expansion) precisely where communications does not (diminishing returns once users pass baseline broadband).** Section 4 develops this directly.

---

## 1. Where the Communications Market Is Today

### 1.1 The global picture, by product

The single most important structural fact is that **communications is mobile-dominated**: mobile is about 3x the revenue of fixed broadband and about 6x the connection count. The mobile and fixed-broadband lines below are global GSMA-class series (China included); the China-excluded counterparts are noted where they matter to the addressable math.

| Product line (2025) | Service revenue | Connections | Status | Source |
|---|---|---|---|---|
| Mobile / cellular (global) | **~$1.19 trillion** | ~9.2B subscriptions (~5.8B unique people) | [FACT] | [global_regional](../economics/comms_global_regional_market.md) (GSMA, ITU) |
| Fixed broadband (global) | **~$360-390 billion** | ~1.53B subscriptions | [FACT subs / ESTIMATE revenue] | [global_regional](../economics/comms_global_regional_market.md) (Point Topic, Grand View) |
| Consumer connectivity (mobile + fixed broadband) | **~$1.55 trillion** global / ~$1.2-1.3T ex-China | n/a | [ESTIMATE] | [global_regional](../economics/comms_global_regional_market.md) |
| Total telecom services (mobile + fixed + enterprise + wholesale + voice) | **~$2.0-2.1 trillion** global / ~$1.6-1.7T ex-China | n/a | [ESTIMATE] | [global_regional](../economics/comms_global_regional_market.md) (Precedence, Grand View) |

> **Do not double-count.** The widely quoted GSMA "$7.6 trillion" and "$11.3 trillion by 2030" are the **economic value mobile adds to GDP**, not operator revenue. They must never be summed with the market-size lines. The revenue the industry actually collects is the ~$1.19T mobile line. (Confirmed this distinction against GSMA directly; the €1.1T "Europe mobile" figure is likewise GDP-contribution, not revenue.)

### 1.2 By region (ex-China-adjusted)

Rank order is stable across sources; the dollar figures are softer than the shares (different firms, different bucket definitions). Treat shares as more reliable than absolute dollars.

| Region | Approx. 2025 telecom service revenue | Share of global | Note | Source |
|---|---|---|---|---|
| Asia Pacific (incl. China in the published figure) | ~$700-717B | ~34% | Ex-China it is far smaller; China carved out in 1.5 | [global_regional](../economics/comms_global_regional_market.md) |
| North America | ~$600-611B | ~29% | US is the bulk (~$520B+) | [global_regional](../economics/comms_global_regional_market.md) |
| Europe | ~$546B | ~26% | Mature, low single-digit growth, highest fixed penetration | [global_regional](../economics/comms_global_regional_market.md) |
| Middle East and Africa | ~$345B (MNO scope) | high-growth | Fastest region (~10.8% CAGR); largest connectivity gap | [global_regional](../economics/comms_global_regional_market.md) |
| Latin America | ~$159B | smaller | ~6.3% CAGR; thin, uneven fixed layer | [global_regional](../economics/comms_global_regional_market.md) |

### 1.3 The US in detail: broadband and cellular segments

The US is the best-reported sub-market and the natural reference for any entrant.

| US segment (2025-26) | Size | Subscribers / connections | Status | Source |
|---|---|---|---|---|
| Fixed (ground) broadband service revenue | **~$70-95B/yr** (range: $63.6B narrow to $100.5B North-America-wide) | ~115-130M connections (~76M cable, ~30.7M telco, ~13-14M FWA) | [ESTIMATE] | [us_broadband](../economics/comms_us_broadband_market.md) |
| Wireless carrier service revenue | **~$326B/yr** | 579M total wireless connections; 259M+ 5G | [ESTIMATE size, single major source / FACT connections] | [us_cellular](../economics/comms_us_cellular_market.md) |
| US MVNO (wholesale) layer | **~$13-15B/yr** (central); ~$44B outlier flagged | cable MVNOs alone >20M lines | [ESTIMATE] | [us_cellular](../economics/comms_us_cellular_market.md) |

Two structural notes the base records:
- **Cable broadband is losing subscribers; FWA and fiber are taking the net adds.** T-Mobile (all-FWA home broadband) and the telcos take the majority of new broadband net adds; cable (Comcast, Charter) is shrinking. The market is also consolidating (Charter-Cox ~$34.5B; Verizon-Frontier ~$20B, closed Feb 2026).
- **The wholesale layer proves a non-carrier can build a large mobile base on rented capacity.** Cable MVNOs (Xfinity Mobile, Spectrum Mobile) run >20M lines on Verizon's network. This is the same "carriers will wholesale to a third party" logic that makes them willing to host satellite direct-to-cell.

### 1.4 The ground-carrier financial benchmarks, in one table

This is the financial spine of the base: the companies a space-comms business would compete with or sell into. Market caps are as of June 17, 2026 (they move daily); revenue/net income are FY2025; subscriber and ARPU figures are the most recent reported. **These are whole-company financials** (Comcast includes media/parks; AT&T/Verizon include large wireless segments); broadband is a segment inside them, not the whole company. The cleanest broadband pure-play is Charter.

| Provider | Broadband subs | Wireless / total subs | Market cap | FY2025 revenue (co.) | FY2025 net income (co.) | ARPU note | Status |
|---|---|---|---|---|---|---|---|
| **Comcast** | **31.3M** (declining, -711K YoY) | 9.7M wireless lines | ~$81B | ~$123.7B | ~$20.0B | Broadband ARPU $73.65, -3.1% YoY | [FACT] |
| **Charter** | **29.7M** (declining) | ~11M Spectrum Mobile lines | ~$20B | ~$54.8B | ~$5.0B | EBITDA ~$22.7B; cleanest pure-play | [FACT] |
| **Verizon** | **>16.3M** (fiber+FWA, post-Frontier) | ~146M wireless retail | ~$191-201B | ~$138.2B | ~$17.2-17.6B | Postpaid ARPA $147.36 | [FACT] |
| **AT&T** | **~14.3M** (fiber+FWA) | 74.2M postpaid phone | ~$156-160B | ~$125.6-125.7B | ~$21.9-22.0B (base-effect jump) | Postpaid phone ARPU $56.57 | [FACT] |
| **T-Mobile** | **~8M (FWA)** | 142.4M total customers | ~$216B | ~$88.3B | ~$11.0B | Postpaid phone ARPU $50.37 | [FACT] |
| **Cox** (private) | **~6M** | n/a | private | ~$6.7B | n/a | Merging into Charter | [ESTIMATE, single source] |
| **Altice/Optimum** | **4.2M** (shrinking) | n/a | small-cap | ~$8.4B (annualized) | n/a | Fiber base ~703K | [FACT] |

Sources: [us_broadband](../economics/comms_us_broadband_market.md), [us_cellular](../economics/comms_us_cellular_market.md). The two docs report Verizon and AT&T market cap and net income in slightly different point ranges (different aggregator timestamps); both ranges are shown.

**The structural read (recorded neutrally):** the largest *broadband* subscriber bases (Comcast, Charter) carry the *smallest* market caps and the *weakest* growth. Investor value sits with the wireless balance sheets. A new entrant selling broadband connectivity enters a market where the incumbents' core product is flat-to-shrinking and de-rated, and where incumbent ARPU is a *falling*, not static, benchmark.

### 1.5 China (excluded): noted aside

China is excluded from every figure above. For scale only: China's three carriers hold roughly **630M+ fixed broadband subscriptions** (more than 40% of the entire global fixed base) and about **$303B** of fixed communications service revenue, under a separate state-directed regime closed to a Western operator ([global_regional](../economics/comms_global_regional_market.md)). It is noted here once and added to no addressable figure.

---

## 2. The Addressable Market: Aggregated-to-Space, Substitution, and an Honest Base Case

This section assembles the founder's three addressable framings. **Every figure here is illustrative.** The cited trillion-dollar numbers are real as population-times-spend ceilings; they are not the market any single operator can address. The whole point of the section is to separate the ceiling from the room.

### 2.1 The two kinds of TAM (read this first)

A cited space-comms TAM is almost always one of two non-comparable things ([space_tam](../economics/comms_space_tam_claims.md)):

| Type | What it measures | Typical magnitude | Good for |
|---|---|---|---|
| **Total-market / cited TAM** | The entire spend pool a service could in principle touch (population x spend) | Hundreds of billions to trillions | Narrative, IPO positioning |
| **Served-addressable / bottoms-up** | The slice an operator can realistically win, after physics and competition | Single-digit to low-hundreds of billions | Revenue modeling, business cases |

### 2.2 Framing (a): all broadband aggregated to space [ILLUSTRATIVE]

If every broadband connection were a candidate for space delivery, how big is the pool today?

| Pool (2025, ex-China) | Size | Implied revenue at current prices | Status |
|---|---|---|---|
| All fixed broadband subscriptions | ~1.53B | ~$360-390B/yr | [PROJECTION, illustrative ceiling] |
| of which satellite today | **~0.5%** (~7-8M subs) | tiny | [FACT] |
| If "broadband" is read to include mobile broadband | mobile broadband is 89% of ~9.2B mobile subs | toward the full ~$1.5T+ consumer connectivity market | [PROJECTION] |

The honest reading: the fixed-broadband pool (~$360-390B/yr) is the pool fixed satellite broadband competes inside today, and satellite holds ~0.5% of it. Treating 100% as addressable ignores that fiber (about 73% of the base) is cheaper, faster, and lower-latency where it exists. Source: [global_regional](../economics/comms_global_regional_market.md).

### 2.3 Framing (b): space replaces ground, full substitution [ILLUSTRATIVE]

The size of the thing being displaced if space fully replaced terrestrial.

| Scenario (2025, global series) | Market being substituted | Status |
|---|---|---|
| Replace all fixed broadband | ~$360-390B/yr (global) | [PROJECTION, illustrative] |
| Replace all fixed broadband + all mobile | ~$1.55T/yr (global; ~$1.2-1.3T ex-China) | [PROJECTION, illustrative] |
| Replace the entire telecom services market | ~$2.0-2.1T/yr (global; ~$1.6-1.7T ex-China) | [PROJECTION, illustrative] |

**Flagged strongly as illustrative.** No credible path has space replacing urban terrestrial at current cost structures: a satellite beam is capacity-constrained where users concentrate, which is the opposite of terrestrial economics (fiber/5G get cheaper per user in density). The figure is useful only as the outer wall and as the denominator against which real space share (~0.5% of fixed) is measured. The economically meaningful version is **the rural and unserved fringe**, sized by the coverage gap (~300M people with no mobile coverage) and the underserved rural base, not the whole figure. Source: [global_regional](../economics/comms_global_regional_market.md).

### 2.4 The honest base case: how large IF a comms business dominated communications

The gap base sets the realistic outer bound on the demand a satellite uniquely serves:

| Demand-gap metric (2025) | Value | Why it matters for space | Status |
|---|---|---|---|
| Coverage gap (no mobile coverage at all) | **~300M people (4%)** | The part a satellite can uniquely serve | [FACT] |
| Usage gap (covered but offline) | **~3.1B people** | An affordability/device problem; satellite supply does **not** address it | [FACT] |
| Satellite share of global fixed broadband today | **~0.5%** | The denominator-grounded reality | [FACT] |

**The honest base case, stated plainly:** even a company that *dominated* the space-served slice of communications is dominating the **served-addressable tier, not the cited trillions.** The independent bottoms-up sizing for the most mature constellation (Starlink, across more tiers and more geographies than a niche entrant) is **~$129B** globally [PROJECTION] (Section 4.3). That is the realistic ceiling on a broad consumer/enterprise LEO connectivity business that wins its served niche, and it is roughly **5-10% of the $1.6T headline.** A premium/sovereign niche (the scoped Rocket Lab opportunity in [comms_business_case.md](../laser_comms/comms_business_case.md)) is a different, smaller, higher-margin, government-weighted market again, referenced not re-sized here. Source: [space_tam](../economics/comms_space_tam_claims.md), [global_regional](../economics/comms_global_regional_market.md).

---

## 3. The Current State of the Technologies

The technology base has no physics wall (consistent with the wider project's finding) but a clear shape. This section summarizes RF and spectrum, laser and optical, and the bands/enabling hardware in plain terms, drawing from the tech docs.

### 3.1 RF and spectrum

**The core idea is the speed-versus-connections tradeoff.** A chunk of spectrum can be tuned toward peak speed (wide channels, high bands) or toward many connections and wide coverage (low bands), but not both from the same slice. Governed by Shannon's law (capacity = bandwidth x log2(1 + SNR)) plus propagation physics (low frequencies travel far and through walls; high frequencies carry more data but die over short distances). Mid-band (1-6 GHz) splits the difference and is therefore the prize everyone fights over. Source: [spectrum_fundamentals](../direct_communication/spectrum_fundamentals_economics.md).

| Tier | Range | Good for | Bad at |
|---|---|---|---|
| Low-band | <1 GHz | Wide-area coverage, rural reach, in-building, many devices | Low peak speed |
| Mid-band | 1-6 GHz (incl. C-band) | The workhorse balance: speed + range, penetrates walls | Less reach than low, less speed than mmWave |
| mmWave | 24 GHz+ | Extreme peak speed in dense hotspots | Tiny coverage, blocked by walls/rain |

**Spectrum cost and access are the binding RF constraint.** The auction prices tell the story: mid-band (US C-band) cost about **$0.94 per MHz-POP** (~$81B total in 2021, the most expensive mid-band auction ever); mmWave is hundreds of times cheaper per MHz-POP because its coverage value is poor. The market pays for *coverage and penetration*, not raw bandwidth. For a new entrant, **terrestrial cellular spectrum is effectively closed** (the prime bands are owned by three carriers; the last greenfield slice cost $81B), while **satellite spectrum is obtained through a different door** (ITU coordination and priority dates, not national cash auctions). A narrow satellite sliver (~100-250 MHz of Ka-band) is attainable via inheriting a distressed filing, leasing, partnering, or newly-opened shared bands. Sources: [spectrum_fundamentals](../direct_communication/spectrum_fundamentals_economics.md), [rf_satcom.md](../laser_comms/rf_satcom.md), [rf_limited_service.md](../laser_comms/rf_limited_service.md).

Conventional RF satcom is mature and weather-robust but bandwidth-limited and regulation-constrained: Ka-band HTS deliver ~500 Gbps/satellite, V-band targets ~1.5 Tbps, but that capacity is shared across beams and users, and a realistic per-link RF channel for a new entrant is far smaller. Source: [rf_satcom.md](../laser_comms/rf_satcom.md).

### 3.2 Laser and optical

Laser (free-space optical) is the only credible backbone for an in-space mesh, and it is **proven at scale**. Source: [optical_comms.md](../laser_comms/optical_comms.md), [constellation_mesh.md](../laser_comms/constellation_mesh.md), [optical_ground_stations.md](../laser_comms/optical_ground_stations.md).

- **Inter-satellite links work at constellation scale.** Starlink runs ~27,000 space lasers (~9,000+ sats x ~3 terminals), each rated up to ~200 Gbps, moving 42+ PB/day at >99% link uptime [FACT].
- **Space-to-ground optical is fast but weather-limited.** NASA TBIRD demonstrated 200 Gbps space-to-ground [FACT], but a single optical ground station only reaches ~50-70% annual availability because lasers cannot penetrate cloud. Reaching 99-99.9% needs a **diverse network of 4+ ground stations** spaced >1,000 km apart so cloud cover is uncorrelated. This is the binding ground-segment constraint, not raw throughput.
- **Terrestrial laser interconnect exists and ships.** Taara (Alphabet spin-out) does up to 25 Gbps over 10 km, deployed in 12+ countries; the same weather wall applies (fog 10-100 dB/km), and the standard fix is a hybrid FSO/RF link for five-nines availability. Its strong case is *where fiber does not exist*; alongside existing fiber it adds only conditional value (security, latency, fast deploy). Source: [laser_terrestrial_interconnect.md](../laser_comms/laser_terrestrial_interconnect.md).

### 3.3 Bands and enabling hardware (the chip question)

The decisive finding: **the silicon is not the bottleneck up through W-band.** Source: [bands_and_enabling_hardware.md](../direct_communication/bands_and_enabling_hardware.md).

| Band | Frequency | Enabling silicon | Off-the-shelf? |
|---|---|---|---|
| Ku/K/Ka | up to ~40 GHz | Silicon (SiGe/CMOS) beamformer ICs (Anokiwave, Renesas) | Yes, volume production |
| V-band | 37-51 GHz | GaN PA MMICs (NxBeam, Qorvo, Wolfspeed, MACOM) | Yes, catalog parts |
| E-band | 71-86 GHz | GaAs/SiGe chipsets + SiP modules | Yes, productized for point-to-point |
| W-band | 92-114 GHz | GaN/GaAs pHEMT PA MMICs (NASA, peer-reviewed) | Emerging, lab/low-volume |
| D-band / sub-THz | 110-325 GHz | InP-HEMT, SiGe BiCMOS, advanced CMOS | No, research-grade only |
| Free-space optical | ~193 THz (1550 nm) | Silicon photonics coherent transceivers (data-center heritage) | Yes (data-center parts); space-grade hardened modules an open question |

The binding constraint up through W-band is **spectrum coordination, rain fade (which worsens steeply with frequency), and pointing**, not chip development. The honest architecture is a **portfolio**: optical for the high-rate backbone, an upper-microwave RF band (V or E) as the all-weather complement, with the silicon for both already available.

### 3.4 The consolidated RF-vs-laser picture

| Dimension | RF (Ka through W-band) | Laser / optical | Edge |
|---|---|---|---|
| Bandwidth per dedicated link | Shared across beams/users; per-link share small for a new entrant | 100-200 Gbps proven dedicated; Tbps roadmap; 10-100x RF | **Optical** |
| Spectrum / regulatory burden | Severe and band-dependent (eases as you climb, never to zero) | **None** for the optical carrier | **Optical (decisive)** |
| Weather | Robust; rain fade rises with frequency but degrades gracefully | Cloud/fog/rain **break** the link; needs site diversity or RF backup | **RF** |
| Mass / power | Higher for equivalent capacity | Lower; smaller apertures | **Optical** |
| Pointing | Wide beams, easy acquisition (narrows at high bands) | Microradian pointing, multi-second acquisition | **RF** |
| Security / intercept | Wider beams: easier to intercept/jam | Narrow beam: very hard to intercept, low probability of detect | **Optical** |
| Maturity | Decades of heritage at Ka and below | Proven for ISLs (Starlink) and downlink (TBIRD); ground ops still maturing | mixed |

Source: [rf_satcom.md](../laser_comms/rf_satcom.md), [bands_and_enabling_hardware.md](../direct_communication/bands_and_enabling_hardware.md). The recurring conclusion across the corpus: **optical primary + RF complement** is the technically settled architecture for a space entrant, with optical winning on the two dimensions that dominate (bandwidth per dedicated link, no spectrum fight) and RF mandatory for weather, mobility, and cheap rugged terminals.

### 3.5 Rocket Lab's in-house comms assets (context, not a verdict)

Rocket Lab owns most of the comms value chain, which is why the corpus treats the comms question as packaging and go-to-market rather than physics. Source: [space_hardware_capabilities.md](../rocket_lab/space_hardware_capabilities.md), [comms_business_case.md](../laser_comms/comms_business_case.md).

- **Optical terminals:** Mynaric CONDOR (acquired April 2026). Mk3 ships at ~2.5 Gbps as-delivered; the Mk3.1 roadmap targets up to 100 Gbps. Optical terminals are an industry-wide bottleneck, so owning the line is both a moat and a potential second revenue line.
- **RF radios:** Frontier software-defined radios (L/S/C/X/Ka-band), deep flight heritage.
- **Launch:** Electron and Neutron (controls its own ride to orbit, de-risking the ITU bring-into-use milestone).
- **Bus:** Flatellite (high-power, stackable, mass-manufacturable; producing for the $816M SDA prime contract).
- **The honest gaps:** no significant RF spectrum (a sliver is attainable but costs years and capital); no optical ground-station network (industry-wide only ~10% of needed optical ground infrastructure exists); no operating comms constellation or customer base today.

---

## 4. The Comparison the Founder Wants: Why Data Centers Justify Premium Economics and Communications (the Working Hypothesis) Does Not

This is the load-bearing analytical section. It is stated as the founder's working hypothesis, grounded in the base, **not** as a verdict.

### 4.1 The communications side: diminishing returns past baseline broadband

The evidence that broadband value *plateaus* past a few hundred Mbps is the strongest finding in the entire base, converging across a peer-reviewed willingness-to-pay study, revealed purchase behavior, and operator ARPU trends. Source: [us_broadband](../economics/comms_us_broadband_market.md).

| Evidence | Value | What it shows | Status |
|---|---|---|---|
| WTP per Mbps, 4 to 10 Mbps | **~$2.34/Mbps** | Households value getting connected enormously | [FACT] |
| WTP per Mbps, 100 to 1,000 Mbps | **~$0.02/Mbps** | The marginal value of a megabit falls ~100x | [FACT] |
| US homes that can get gigabit | **>91%** | Supply is there | [FACT] |
| US homes that buy gigabit | **~30%** | ~70% decline it even when available | [FACT] |
| Modal chosen tier | **200-500 Mbps** | Everyday demand saturates well under 100 Mbps | [FACT] |
| Bandwidth for two 4K streams + gaming | **~60 Mbps** | The actual demand ceiling for most homes | [FACT] |
| Comcast broadband ARPU | **$73.65, -3.1% YoY** | Speed is not commanding a premium | [FACT] |

The conclusion the base draws (neutrally): **the ground-broadband value curve rewards reach and reliability, not raw bandwidth past a low-hundreds-of-Mbps threshold.** Selling "more Mbps" into the served market does not command price. Demand is about *getting connected at all* and *reliability*, which is exactly where coverage-oriented supply (FWA, satellite) is winning.

The deployment-cost side reinforces the same shape: where fiber or upgraded cable already exists, the incumbent can defend a passed home for about **$100-300** (cable D4.0 upgrade), so a new entrant (space included) adds little incremental value in served territory; the value concentrates in the unserved/remote tail where per-passing cost runs from $3,000-6,000 (rural) up to ~$200,000+ (extreme remote) against $50-150/month ARPU. Source: [broadband_deployment](../economics/comms_broadband_deployment_economics.md). The cellular side rhymes: 5G is a low-teens-percent-of-revenue capex business with a long (8-10 year) payback and flat-to-declining ARPU; 5G has largely **not** delivered an ARPU premium. Source: [cellular_5g_deployment](../economics/comms_cellular_5g_deployment_economics.md).

### 4.2 The data-center side: why premium economics hold there

The contrast the founder draws is grounded in the data-center track's own findings (referenced, not re-derived here). The structural differences:

| Dimension | Communications (working hypothesis) | Data centers (the contrast) |
|---|---|---|
| **Demand vs supply** | Demand plateaus once users pass baseline broadband; ~70% refuse the gigabit premium | Demand for AI compute is outrunning supply; the constraint is capacity, not willingness to pay |
| **Hardware upgrade cycle** | Slow; a broadband connection is "good enough" for years; ARPU flat-to-declining | Continual GPU upgrades; each generation commands a premium; rapid obsolescence is a *revenue* driver, not a cost problem |
| **Capacity expansion economics** | Adding capacity into a served market is overbuild (a third terrestrial overbuilder earns ~4% ROI) | Adding capacity is absorbed by unmet demand; expansion is rewarded, not punished |
| **Capex framing** | Capex is a low-teens **percent** of service revenue (~14-19%) | AI data-center capex is a **multiple** of current revenue; the two businesses sit at opposite ends of the capex-intensity spectrum |
| **Willingness to pay for "more"** | Marginal Mbps worth ~$0.02 past 100 Mbps | Marginal compute (more tokens/sec, lower latency, newer model) commands real price |

The cellular deployment doc states the capex-intensity contrast explicitly: mobile-network capex runs ~14-19% of service revenue and is *declining* post-2022, whereas AI data-center capex is a multiple of current revenue, "which is exactly why the ratio is the right axis to compare on." Source: [cellular_5g_deployment](../economics/comms_cellular_5g_deployment_economics.md).

**The founder's hypothesis, stated as a hypothesis:** premium economics in space are justified where demand outruns supply, hardware upgrades continually, and capacity expansion is rewarded (data centers); they are *harder to justify* where returns diminish once users pass baseline broadband, capacity expansion into served markets is overbuild, and willingness-to-pay for "more" collapses (communications). Whether a *space* communications business escapes this by competing on the axes the curve *does* reward (reach, reliability, sovereignty, security, latency) rather than raw bandwidth is the open thesis question, not settled here. The companion thesis ([comms_thesis.md](../vision/comms_thesis.md)) records it as a working hypothesis to be tested in later waves.

### 4.3 The ASTS and SpaceX cited TAM, clarified

The founder asked specifically to clarify the headline TAMs that drive the bull case. The base answer: **the cited number and the realistically served number are separated by roughly two orders of magnitude.** Source: [space_tam](../economics/comms_space_tam_claims.md).

| Player | Cited / headline TAM | Bottoms-up / served estimate | Served as % of cited | How the headline is built |
|---|---|---|---|---|
| **AST SpaceMobile** | **~$1.1T/yr** (GSMA mobile base) | ~$3B (bear) to ~$97B (bull) revenue-to-ASTS (BofA); ~$15.4B illustrative model (single source) | ~0.3-9% | Global mobile subscribers x annual spend |
| **SpaceX / Starlink (connectivity)** | **$1.6T** ($870B broadband + $740B mobile) | **~$129B** realistic (Morningstar); ~$80B floor | **~5-8%** | Entire telecom wallet ex-China/Russia |
| **SpaceX (all-in)** | **$28.5T** (93% is AI, not comms) | n/a (mostly AI) | n/a | Population/enterprise x spend across all sectors |
| **Amazon Kuiper / Leo** | 400-500M unconnected households | **~$20-36B/yr** (Quilty/internal) | tens of $B | Unconnected households x ARPU |
| **D2D segment (bottoms-up)** | (sector) | **$2.6B-$13.8B** near-term | n/a | Segment-by-segment research-house build |

The Morningstar rebuild is the cleanest illustration and is independently corroborated: of SpaceX's own $1.6T, Morningstar keeps only the **Niche (~$84B)** and **Add-on (~$45B)** tiers a LEO network can win, and throws out the **~$1.17T "core telecom"** tier that satellite cannot economically serve in dense areas (verified: US Niche ~$28B + US Add-on ~$15B = ~$43B US, x3 for global = ~$129B). Three more named analysts (Eurospace, Novaspace, Frost & Sullivan) independently call the headline "90% or more out of reach" / "a narrative tool" / "ultimately unfalsifiable." The load-bearing finding: **served market is ~5-10% of cited total; a 90% haircut is the reasonable default prior on any fresh space-comms TAM.**

**Three structural discounts to apply to any cited TAM** ([space_tam](../economics/comms_space_tam_claims.md)): the **density discount** (remove the dense-urban core telecom wallet a beam cannot serve, ~70-80% of the connectivity TAM); the **ARPU-reality discount** (do not multiply low-income underserved billions by a developed-market ARPU); and the **shared-market discount** (Starlink, Kuiper, AST, Eutelsat, Telesat split the same pie; no single operator captures it).

---

## 5. Open Numbers (the biggest gaps for the lead)

The base is solid on direction; the biggest open numbers are:

1. **Exact US-only fixed broadband revenue.** The $63.6B (narrow) vs $92B (broad) vs $100.5B (North America) spread needs one agreed boundary before any TAM math. Which definition does the comms track want?
2. **A single authoritative fixed-broadband-revenue series.** The global $360-390B band is wide; an all-services-vs-access-only reconciliation would tighten Section 1.1.
3. **Ex-China Asia split.** Published Asia Pacific totals include China; a clean ex-China Asia figure is not directly published and would need a bottom-up build.
4. **The dollar size of the satellite-addressable rural fringe.** The realistic space-addressable slice is "coverage gap (~300M people) + underserved rural," not the whole pool. Sizing that fringe *in dollars* (not just people, where ARPU is low) is the missing number that would make both founder framings actionable.
5. **Direct-to-cell revenue per user.** Starlink reports 16M D2D users but no clean per-user revenue for the D2D layer; AST is pre-scale (~$70.9M FY2025 revenue against a $1.1T cited TAM). The unit economics of "fill the dead zones" are unproven.
6. **The premium/sovereign niche size.** The scoped Rocket Lab opportunity (defense, sovereign, finance, critical-infrastructure, orbital-DC backhaul) is referenced from [comms_business_case.md](../laser_comms/comms_business_case.md) (reference points: EUR 10.6B IRIS2, $1.3B SDA optical-mesh contracts, $14.8B LEO-satcom forecast) but not sized in dollars here. That is the central unanswered business number.

---

## Sources

This synthesis cites the wave-1 ingest docs and the existing corpus by path; each of those carries the underlying 2+ independent web sources inline. The primary inputs:

*Markets*
- [comms_us_broadband_market.md](../economics/comms_us_broadband_market.md)
- [comms_us_cellular_market.md](../economics/comms_us_cellular_market.md)
- [comms_global_regional_market.md](../economics/comms_global_regional_market.md)
- [comms_space_tam_claims.md](../economics/comms_space_tam_claims.md)

*Deployment economics*
- [comms_broadband_deployment_economics.md](../economics/comms_broadband_deployment_economics.md)
- [comms_cellular_5g_deployment_economics.md](../economics/comms_cellular_5g_deployment_economics.md)

*Technology*
- [spectrum_fundamentals_economics.md](../direct_communication/spectrum_fundamentals_economics.md)
- [bands_and_enabling_hardware.md](../direct_communication/bands_and_enabling_hardware.md)
- [rf_satcom.md](../laser_comms/rf_satcom.md)
- [rf_limited_service.md](../laser_comms/rf_limited_service.md)
- [optical_comms.md](../laser_comms/optical_comms.md)
- [optical_ground_stations.md](../laser_comms/optical_ground_stations.md)
- [laser_terrestrial_interconnect.md](../laser_comms/laser_terrestrial_interconnect.md)
- [constellation_mesh.md](../laser_comms/constellation_mesh.md)

*Rocket Lab assets and scoped business case*
- [space_hardware_capabilities.md](../rocket_lab/space_hardware_capabilities.md)
- [comms_business_case.md](../laser_comms/comms_business_case.md)

*Competitor cadence context*
- [falcon9_cadence_ramp.md](../competitors/falcon9_cadence_ramp.md)
- [starship_addendum.md](../competitors/starship_addendum.md)

*Direct verification (this synthesis)*
- [Morningstar, Our Realistic Starlink Market Sizing](https://d1e00ek4ebabms.cloudfront.net/production/uploaded-files/Our_Realistic_Starlink_Market_Sizing-915d25bb-5968-4e1f-ae0b-ad5999a9aa87.pdf) (confirmed the $28B+$15B US tier split = $43B, x3 = $129B global, and the 45%-of-realistic-market base case)
- [GSMA, The Mobile Economy](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/) (confirmed $7.6T is GDP-contribution, not operator revenue; the ~$1.19T mobile operator revenue is the collected-revenue line)

---

## Confidence

- **The market base (Sections 1, 4.1): medium-high.** Provider financials and subscriber counts come from 2025-26 SEC filings and earnings (high). Global mobile revenue (~$1.19T, GSMA), fixed broadband subscriptions (~1.53B, Point Topic), and the satellite ~0.5% share are primary-body or multi-source (high). Total-market dollar sizing is medium (research-firm definitions diverge ~40%). The diminishing-returns conclusion is the most robust finding in the base (high): a peer-reviewed study, revealed purchase behavior, and operator ARPU all converge.
- **The addressable framings (Section 2): low by design.** They are arithmetic ceilings on a base of sourced numbers, explicitly not forecasts. The 0.5% satellite share and the gap base (~300M coverage gap, ~3.1B usage gap) underneath them are FACT.
- **The TAM clarification (Section 4.3): the cited figures are high confidence (what is claimed, in primary filings); the served-market estimates are medium (analyst models with stated assumptions); the size of the haircut (~90%, served ~5-10% of cited) is high, corroborated by four independent analysts plus the convergence of bottoms-up estimates.**
- **The technology state (Section 3): medium-high.** Optical at scale (Starlink, TBIRD), the spectrum-access constraint, the auction prices, and the chip-availability mapping are each multi-source or primary. Single-source items (extreme-rural per-passing, some European per-MHz-POP decimals, the $15.4B ASTS model, the $200B combined-bank figure) are flagged in the underlying docs.
- **The DC-vs-comms comparison (Section 4): medium-high on the communications side (grounded in the diminishing-returns evidence), and stated as the founder's working hypothesis, not a verdict, on the synthesis across to data centers.**

---

## Open Questions

These are the base-level open questions; the thesis-level questions (what the comms business should be) live in [comms_thesis.md](../vision/comms_thesis.md).

1. **Where exactly does space sit on the value curve?** Section 4.1 establishes the curve rewards reach + reliability, not raw speed. Quantifying the unserved/underserved households and their WTP (the high-WTP part of the curve) is the natural next sizing.
2. **Does a space comms business escape the diminishing-returns trap by competing on reach/reliability/sovereignty/security/latency rather than bandwidth?** This is the central thesis question the base cannot answer; it is recorded as a hypothesis.
3. **The dollar size of the satellite-addressable rural fringe and of the premium/sovereign niche** (see Section 5, items 4 and 6). These are the two numbers that would convert the framings into a real addressable market.
4. **Direct-to-cell and broadband boundary.** The $1.1T (ASTS, D2D-to-phone) and $1.6T (SpaceX connectivity, broadband-to-terminal) overlap in ways not cleanly decomposed. A de-duplicated served-market map is a useful next step.
5. **Pricing benchmark is a moving target.** Cable ARPU is ~$74 and *falling*; FWA undercuts it. Any space-comms unit economics must be benchmarked against a falling incumbent ARPU, not a static one.
6. **Consolidation endpoint.** With Charter-Cox and Verizon-Frontier closing, the 2027 competitive set is fewer, larger players; worth re-checking after both deals integrate.

---

## Claims (synthesis-level; COMM-S## namespace)

These are the headline synthesized claims. Each traces to an ingest doc (which holds the underlying 2+ source citations); the lead reconciles into SOURCE_INDEX. The COMM-S## prefix avoids colliding with the ingest docs' own COMM-### numbering.

| COMM-S id | Claim | Value | Status | Source doc(s) |
|---|---|---|---|---|
| COMM-S01 | Total telecom service revenue, all services (global; ~$1.6-1.7T ex-China) | ~$2.0-2.1T/yr | [ESTIMATE] | global_regional |
| COMM-S01b | Consumer connectivity, mobile + fixed broadband (global; ~$1.2-1.3T ex-China) | ~$1.55T/yr | [ESTIMATE] | global_regional |
| COMM-S02 | Global mobile/cellular service revenue | ~$1.19T/yr | [FACT] | global_regional (GSMA) |
| COMM-S03 | Global fixed broadband service revenue | ~$360-390B/yr | [ESTIMATE] | global_regional |
| COMM-S04 | US fixed broadband service revenue | ~$70-95B/yr | [ESTIMATE] | us_broadband |
| COMM-S05 | US wireless carrier service revenue | ~$326B/yr | [ESTIMATE] single major source | us_cellular |
| COMM-S06 | US MVNO (wholesale) market | ~$13-15B/yr (central); ~$44B outlier | [ESTIMATE] | us_cellular |
| COMM-S07 | Ground-carrier market caps (Jun 17 2026) | T-Mobile ~$216B; Verizon ~$191-201B; AT&T ~$156-160B; Comcast ~$81B; Charter ~$20B | [FACT] | us_broadband, us_cellular |
| COMM-S08 | Largest broadband subs carry smallest market caps | Comcast 31.3M/~$81B; Charter 29.7M/~$20B vs T-Mobile ~$216B | [FACT] | us_broadband |
| COMM-S09 | Broadband WTP collapse with speed | ~$2.34/Mbps (4-10) to ~$0.02/Mbps (100-1,000) | [FACT] | us_broadband |
| COMM-S10 | Gigabit availability vs adoption (US) | >91% can get / ~30% buy; modal 200-500 Mbps | [FACT] | us_broadband |
| COMM-S11 | Comcast broadband ARPU | $73.65, -3.1% YoY (Q1 2026) | [FACT] | us_broadband |
| COMM-S12 | Cable defend-cost for a passed home (D4.0 upgrade) | ~$100-300/home passed | [FACT] | broadband_deployment |
| COMM-S13 | Extreme-rural fiber cost per passing | up to ~$200,000-230,000 | [FACT] single primary | broadband_deployment |
| COMM-S14 | Mobile-network capex intensity | ~14-19% of service revenue (declining post-2022) | [FACT] | cellular_5g_deployment |
| COMM-S15 | US C-band spectrum auction (mid-band benchmark) | ~$81B total; ~$0.94/MHz-POP | [FACT] | spectrum_fundamentals |
| COMM-S16 | Satellite share of global fixed broadband | ~0.5% (growing ~+41.6% YoY) | [FACT] | global_regional |
| COMM-S17 | Coverage gap / usage gap (2025) | ~300M no coverage / ~3.1B covered-but-offline | [FACT] | global_regional |
| COMM-S18 | SpaceX cited connectivity TAM | $1.6T ($870B broadband + $740B mobile) | [FACT] as claimed | space_tam |
| COMM-S19 | AST cited TAM | ~$1.1T/yr (GSMA mobile base) | [FACT] as claimed | space_tam |
| COMM-S20 | Morningstar realistic Starlink served market | ~$129B global (~$84B Niche + ~$45B Add-on); ~$80B floor | [PROJECTION] | space_tam (verified) |
| COMM-S21 | Served-vs-cited haircut (load-bearing) | served ~5-10% of cited total (~90% haircut) | [ESTIMATE] synthesis | space_tam |
| COMM-S22 | Optical ISL proven scale (Starlink) | ~27,000 space lasers; up to ~200 Gbps/terminal; 42+ PB/day; >99% uptime | [FACT] | optical_comms |
| COMM-S23 | Space-to-ground optical rate vs single-site availability | 200 Gbps (TBIRD) but ~50-70% single-site; 4+ OGS for 99-99.9% | [FACT] | optical_comms, optical_ground_stations |
| COMM-S24 | Enabling silicon off-the-shelf through W-band | Yes Ka/V/E (catalog); W-band emerging; sub-THz research-only | [FACT] | bands_and_enabling_hardware |
| COMM-S25 | Attainable satellite spectrum sliver for a new entrant | ~100-250 MHz Ka-band → ~0.2-3 Gbps/beam, 1,000-10,000 pro users | [ESTIMATE] | rf_limited_service |
| COMM-S26 | Rocket Lab optical terminal state (Mynaric CONDOR) | Mk3 ~2.5 Gbps as-delivered; Mk3.1 roadmap up to 100 Gbps | [FACT] | space_hardware_capabilities, optical_comms |
| COMM-S27 | DC-vs-comms capex framing contrast | comms capex ~14-19% of revenue; AI DC capex a multiple of revenue | [FACT/ESTIMATE] | cellular_5g_deployment |
