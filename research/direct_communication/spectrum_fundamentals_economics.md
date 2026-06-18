# Spectrum Fundamentals and Economics

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:** the satellite-band table and ITU/FCC coordination mechanics in
[`research/laser_comms/rf_satcom.md`](../laser_comms/rf_satcom.md), and the five
spectrum-acquisition paths (inherit a filing, lease, partner, experimental license, newly-opened
shared bands) in [`research/laser_comms/rf_limited_service.md`](../laser_comms/rf_limited_service.md).
This doc adds the **terrestrial cellular side**, the **cost-today numbers in real dollars**, and a
plain **speed-vs-connections** explanation. It does not repeat the satellite Ka/V/Ku table or the
acquisition-path detail; cite those docs for the space side.

---

## Summary / Verdict

Spectrum is a licensed range of radio frequencies. It is scarce because the usable range is finite,
two transmitters on the same frequency in the same place interfere, and governments hand out
exclusive rights to specific slices. That scarcity is why spectrum is **expensive and slow to get**.

The single most useful mental model for this wiki is the **speed-versus-connections tradeoff**.
A given amount of spectrum can be tuned toward raw peak speed (wide channels, high frequency bands)
or toward many simultaneous connections and wide coverage (low frequency bands, density features).
You do not get both for free from the same slice. This is governed by Shannon's law (capacity rises
with channel width and signal quality) plus the physics of propagation (low frequencies travel
farther and through walls; high frequencies carry more bandwidth but die over short distances)
([GeeksforGeeks - Shannon channel capacity](https://www.geeksforgeeks.org/computer-networks/maximum-data-rate-channel-capacity-for-noiseless-and-noisy-channels/),
[Nokia - 5G spectrum bands explained](https://www.nokia.com/thought-leadership/articles/spectrum-bands-5g-world/)).

**Cost today, terrestrial, the headline numbers:**

- US **C-band** (3.7 GHz, Auction 107, 2021): **about $80.9 billion** raised, roughly
  **$0.94 per MHz-POP** on average. The most expensive mid-band 5G auction ever held, anywhere
  ([EE Times](https://www.eetimes.com/c-band-auction-brings-home-80-9b/),
  [SpaceNews](https://spacenews.com/c-band-raises-81-billion/)).
- US **3.45 GHz** mid-band (Auction 110, 2021-2022): **about $22.5 billion** raised, roughly
  **$0.72 per MHz-POP**
  ([IEEE ComSoc](https://techblog.comsoc.org/2022/01/14/fcc-auction-110-rakes-in-22-5-billion-in-gross-proceeds-for-3-45-ghz-service/),
  [Fierce Network](https://www.fierce-network.com/wireless/fcc-closes-historic-345-ghz-auction-218b)).
- US **mmWave** (24 GHz and up): an order of magnitude cheaper per MHz-POP, around **$0.007**
  at 24 GHz and **$0.0019** at 37/39/47 GHz, because the spectrum is plentiful and the coverage
  per dollar is poor
  ([Fierce Network](https://www.fierce-network.com/regulatory/fcc-mmwave-auction-brings-more-than-7-5b-as-clock-phase-ends),
  [IEEE ComSoc - Auction 103](https://techblog.comsoc.org/2019/12/10/analysis-and-results-of-fcc-auction-103-for-5g-mmwave-spectrum/)).
- **Europe** runs much cheaper than the US: mid-band (3.5 GHz) prices cluster around
  **EUR 0.08 to EUR 0.36 per MHz-POP** depending on country, well below the US C-band level
  ([Aetha - Italian 5G auction](https://www.aethaconsulting.com/the-italian-5g-auction-why-so-expensive/),
  [telecoms.com - UK auction](https://www.telecoms.com/5g-6g/uk-extracts-1-36-billion-from-uk-operators-for-700-mhz-and-3-6-ghz-spectrum)).
- **Global**, all bands, 2021 was a record year: total spectrum awards reached about
  **$140 billion**, up from about **$37.7 billion** in 2020, driven by the US mid-band auctions
  ([PolicyTracker via search](https://www.policytracker.com/blog/auctions-for-700-mhz-and-3-5-ghz-bands-drive-awards-in-q4-2020/)).

**Who controls it:** governments allocate it; in the US a tight oligopoly holds the prime bands.
T-Mobile holds the best low-band (600 MHz) and the deepest mid-band (2.5 GHz from Sprint). Verizon
and AT&T together bought essentially all the C-band. mmWave is split among all three plus cable
entrants ([Light Reading - carrier 5G plans](https://www.sdxcentral.com/analysis/verizon-att-t-mobile-5g-plans-spectrum-specific/),
[T-Mobile newsroom](https://www.t-mobile.com/news/network/t-mobile-further-solidifies-5g-leadership-position-with-successful-c-band-auction)).

**What this means for a fresh entrant (the relevant verdict for Rocket Lab):** buying terrestrial
cellular spectrum outright is not a realistic path. The prime mid-band is already owned, and the
last comparable greenfield slice (C-band) cost $81 billion. A new entrant's realistic options are
the ones already documented for the space side in
[`rf_limited_service.md`](../laser_comms/rf_limited_service.md): inherit a distressed filing, lease,
partner, use experimental licenses to de-risk, or chase newly-opened shared bands. **Satellite
spectrum is obtained through a different door than terrestrial spectrum** (ITU coordination and
first-come priority dates, not national cash auctions), which is why the satellite path is the one
worth pursuing and the terrestrial-auction path is not.

**Confidence: medium-high.** The auction dollar figures and per-MHz-POP prices are well-sourced and
cross-checked against 2+ independent sources each. The speed-vs-connections physics is standard
textbook material. Confidence is lower only on a few single-source per-MHz-POP figures flagged below
and on the exact current carrier MHz holdings, which shift with each deal.

---

## 1. What Spectrum Is, and Why It Is Scarce

**Spectrum is a license to use a range of radio frequencies, in a place, exclusively.** A wireless
signal is an electromagnetic wave at some frequency (measured in hertz: kHz, MHz, GHz). A "band" is a
named, bounded frequency range (for example 3.7 to 3.98 GHz is the US C-band). A license is a
government grant of the exclusive right to transmit in a specific band over a specific geography.

Scarcity comes from three hard facts:

1. **The usable range is finite.** Only frequencies from roughly the high kHz up to tens of GHz
   propagate usefully for terrestrial mobile and satellite service. Above that, signals are absorbed
   or need line of sight. The good, low-and-mid range is a small ribbon, and almost all of it is
   already assigned to someone (mobile, broadcast, military, GPS, aviation, weather radar).
2. **Co-channel transmitters interfere.** Two transmitters on the same frequency in the same area
   jam each other. To make a frequency usable, a regulator must grant it to one party and protect it
   from others. That exclusivity is the product being sold.
3. **Allocation is slow and political.** Reassigning a band from an incumbent use (a TV broadcaster,
   a government radar) to a new use (5G) takes years of regulatory process, clearing, and sometimes
   relocation payments. The 600 MHz "incentive auction" literally paid TV stations more than
   $10 billion to vacate so the band could be re-sold for mobile
   ([CommLaw Monitor](https://www.commlawmonitor.com/2017/04/articles/internet/fcc-announces-the-results-of-the-19-8-billion-broadcast-incentive-auction/)).

The ITU/FCC mechanics for *satellite* spectrum (first-come-first-served priority dates, coordination
against incumbents, 7-year bring-into-use deadlines) are covered in
[`rf_satcom.md`](../laser_comms/rf_satcom.md) and not repeated here. The terrestrial process is
different: a national regulator (the FCC in the US, Ofcom in the UK, the Bundesnetzagentur in
Germany) clears a band and **auctions exclusive licenses for cash**, usually nationwide or by
regional blocks.

---

## 2. The Speed-vs-Connections Tradeoff (the core idea)

This is the single most important concept to carry through the rest of this wiki. Plainly: **you can
tune a chunk of spectrum toward peak speed, or toward many connections and wide coverage, but the
same chunk cannot maximize both.** Two independent levers drive it.

**Lever 1, channel width and band height, drives peak speed.** Shannon's law says the maximum data
rate of a channel is

> capacity = bandwidth x log2(1 + signal-to-noise ratio)

so a **wider channel carries proportionally more bits per second**
([GeeksforGeeks - channel capacity](https://www.geeksforgeeks.org/computer-networks/maximum-data-rate-channel-capacity-for-noiseless-and-noisy-channels/)).
Wide channels (say 100 MHz) are only available up high, where there is room. A low-band carrier
might have 5 to 10 MHz; an mmWave carrier can have 400 to 800 MHz. That is why mmWave delivers
multi-gigabit peak speeds and low-band does not: there is simply more room to be wide up high.

**Lever 2, frequency, drives reach and penetration (and therefore how many users and how much area
one cell covers).** Low frequencies have long wavelengths that travel far and pass through walls;
high frequencies have short wavelengths that carry more data but die over short distances and are
blocked by buildings, foliage, even rain
([Nokia - 5G bands](https://www.nokia.com/thought-leadership/articles/spectrum-bands-5g-world/),
[Verizon - 5G frequency bands](https://www.verizon.com/about/news/5g-frequency-bands-explained)).
A single low-band tower can blanket a rural county and hold a large number of low-rate devices; an
mmWave node covers a city block.

**Putting it together:**

| Goal | What you reach for | Why | Cost consequence |
|---|---|---|---|
| Highest peak speed | Wide channels, high band (C-band, mmWave) | Shannon: width = bits/s; only high bands have room to be wide | High band is cheap per MHz but you need lots of MHz and many sites |
| Most simultaneous connections + coverage | Low band, plus 5G density features | Long range covers more area and devices per cell; designed for many low-rate links | Low band is scarce and expensive per MHz |
| Balance of both | Mid-band (1 to 6 GHz) | Decent width, decent reach, penetrates walls | The contested "sweet spot," hence the most expensive |

The "many connections" end has a concrete target. The 5G standard (IMT-2020) requires support for a
**connection density of 1 million devices per square kilometer** for the massive-machine-type
(IoT-sensor) use case, achieved with low-band, narrowband air interfaces (NB-IoT, LTE-M) precisely
because their long range and deep penetration reach the most devices
([Cambridge Wireless - mMTC](https://www.cambridgewireless.co.uk/resource/mmtc-in-5g--the-backbone-of-the-iot-revolution.html),
[Verizon - eMBB/URLLC/mMTC](https://www.verizon.com/about/news/5g-understanding-embb-urllc-mmtc)).
The opposite extreme, enhanced mobile broadband, chases peak gigabit speeds on wide high-band
channels for a smaller number of high-rate users in a small area.

**One-line takeaway:** high band and wide channels buy *speed* but little *reach*; low band buys
*reach and connection count* but little raw speed; mid-band splits the difference and is therefore
the prize everyone fights over.

This same tradeoff governs the satellite side. The Ka and V bands the data-center work cares about
are high bands chosen for raw throughput, with the matching downside of rain fade and short reach,
exactly as documented in [`rf_satcom.md`](../laser_comms/rf_satcom.md).

---

## 3. The Terrestrial Cellular Bands

US carrier 5G is built on three tiers. (Frequencies are the common round-number labels.)

| Tier | Range | What it is good for | What it is bad at | Typical channel width |
|---|---|---|---|---|
| **Low-band** | Under 1 GHz (600, 700, 850 MHz) | Wide-area coverage, rural reach, in-building penetration, holding many devices | Low peak speed (narrow channels) | ~5 to 10 MHz per carrier |
| **Mid-band** | 1 to 6 GHz (incl. **C-band** 3.7-3.98 GHz, 2.5 GHz, 3.45 GHz) | The balance: good speed AND useful range, penetrates walls; the workhorse of modern 5G | Less reach than low-band, less raw speed than mmWave | ~40 to 100 MHz per carrier |
| **mmWave (high-band)** | 24 GHz and up (24, 28, 37, 39, 47 GHz) | Extreme peak speed (multi-Gbps) in dense hotspots (stadiums, airports, downtown) | Tiny coverage, blocked by walls/rain/foliage; uneconomic for wide coverage | ~100 to 800+ MHz |

Sources: [Spectrum.com - 5G bands](https://www.spectrum.com/resources/mobile/5g-bands),
[T-Mobile - why mid-band matters](https://www.t-mobile.com/business/resources/articles/why-mid-band-5g-matters),
[Nokia - 5G bands](https://www.nokia.com/thought-leadership/articles/spectrum-bands-5g-world/).

**Mid-band is "the sweet spot."** It is the only tier that gives both usable speed and usable
coverage while still penetrating buildings, which is why carriers, regulators, and bidders treat it
as the most valuable cellular spectrum on Earth, and why it commands the highest auction prices
([T-Mobile - why mid-band matters](https://www.t-mobile.com/business/resources/articles/why-mid-band-5g-matters)).
mmWave, despite its headline gigabit speeds, has turned out to be a niche capacity tool for specific
crowded locations, not a coverage layer
([Ericsson - 5G mmWave](https://www.ericsson.com/en/reports-and-papers/further-insights/leveraging-the-potential-of-5g-millimeter-wave)).

---

## 4. How Spectrum Is Obtained

Three mechanisms, in rough order of how a fresh entrant would encounter them.

**Auctions (the primary terrestrial route).** A national regulator clears a band and sells exclusive
licenses to the highest bidders, usually in an ascending clock auction over many rounds, by
geographic block and frequency block. This is how essentially all prime US cellular spectrum since
the mid-1990s has changed hands. The winner pays cash up front and gets a license (typically 10 to
15 years, renewable) with build-out obligations. Auctions are how the headline dollar figures in
Section 5 were set.

**Licenses and administrative awards.** Some spectrum is assigned by application or "beauty contest"
rather than auction (more common historically and outside the US), and some is licensed for specific
private or shared use (for example the US CBRS 3.5 GHz band uses a tiered shared-license model). A
license is the underlying legal instrument; an auction is just one way to decide who gets it.

**Leases and secondary-market transfers.** Spectrum licenses can be **bought, sold, and leased**
after the fact, subject to regulator approval. A holder who is not using a band can lease it to
someone who will. This secondary market is the realistic near-term route for a new entrant who
cannot win a primary auction, and it is exactly the leasing/partnering path already laid out for the
satellite side in [`rf_limited_service.md`](../laser_comms/rf_limited_service.md) (Paths B and C
there). The mechanism is the same idea on the ground.

For the satellite-specific routes (inheriting a distressed ITU priority filing, experimental Part 5
licenses, newly-opened shared satellite bands), see
[`rf_limited_service.md`](../laser_comms/rf_limited_service.md) rather than repeating them here.

---

## 5. The Cost Today, in Real Dollars

The standard unit is **dollars per MHz-POP**: dollars paid, divided by megahertz of bandwidth,
divided by the population covered (POPs = points of presence = people in the license area). It lets
you compare a nationwide block against a single city on the same scale.

### US auctions

| Auction | Band | Year | Total raised | Price (per MHz-POP) | Note |
|---|---|---|---|---|---|
| **107 (C-band)** | 3.7-3.98 GHz (mid) | 2021 | **~$80.9B** | **~$0.94** avg ($1.30 in top 46 markets) | Most expensive mid-band auction ever, worldwide |
| **110** | 3.45-3.55 GHz (mid) | 2021-22 | **~$22.5B** | **~$0.72** | 3rd-highest-grossing FCC auction ever |
| **97 (AWS-3)** | 1.7/2.1 GHz (mid) | 2014-15 | **~$44.9B** | **~$2.72** (paired) | Record at the time; very high paired-spectrum price |
| **1002 (600 MHz)** | 600 MHz (low) | 2017 | **~$19.8B** | (see note) | Incentive auction; paid TV broadcasters >$10B to vacate; T-Mobile won most |
| **102 (24 GHz)** | 24 GHz (mmWave) | 2019 | **~$2.0B** | **~$0.007** | Cheap per MHz-POP: lots of spectrum, little coverage value |
| **103 (37/39/47 GHz)** | upper mmWave | 2019-20 | **~$7.56B** | **~$0.0019** | ~5x cheaper per MHz-POP than 24 GHz; largest-ever auction by license count |

Sources: C-band [EE Times](https://www.eetimes.com/c-band-auction-brings-home-80-9b/),
[SpaceNews](https://spacenews.com/c-band-raises-81-billion/),
[FCC winning-bidders release](https://www.fcc.gov/document/fcc-announces-winning-bidders-c-band-auction);
Auction 110 [IEEE ComSoc](https://techblog.comsoc.org/2022/01/14/fcc-auction-110-rakes-in-22-5-billion-in-gross-proceeds-for-3-45-ghz-service/),
[Fierce Network](https://www.fierce-network.com/wireless/fcc-closes-historic-345-ghz-auction-218b);
AWS-3 [Fierce Network](https://www.fierce-network.com/wireless/it-s-over-fcc-s-aws-3-spectrum-auction-ends-at-record-44-9b-bids),
[Wikipedia - AWS-3 auction](https://en.wikipedia.org/wiki/AWS-3_auction),
[Cramton - AWS-3 prices](https://cramton.umd.edu/papers2015-2019/cramton-aws-3-auction-prices.pdf);
600 MHz [CommLaw Monitor](https://www.commlawmonitor.com/2017/04/articles/internet/fcc-announces-the-results-of-the-19-8-billion-broadcast-incentive-auction/),
[Light Reading](https://www.lightreading.com/mobile-core/t-mobile-dish-comcast-big-winners-in-19-8b-600mhz-auction);
mmWave [Fierce Network](https://www.fierce-network.com/regulatory/fcc-mmwave-auction-brings-more-than-7-5b-as-clock-phase-ends),
[IEEE ComSoc - Auction 103](https://techblog.comsoc.org/2019/12/10/analysis-and-results-of-fcc-auction-103-for-5g-mmwave-spectrum/).

**The shape of the data tells the whole story.** Mid-band (C-band, AWS-3) costs roughly
**$0.70 to $2.70 per MHz-POP**. mmWave costs roughly **$0.002 to $0.007 per MHz-POP**, hundreds of
times less. The market is paying for *coverage and penetration* (the speed-vs-connections tradeoff
in Section 2 priced in dollars), not for raw bandwidth. Bandwidth up high is nearly free; the
reach of mid-band is what is expensive.

### European auctions (cheaper than the US)

| Country | Band | Year | Price (per MHz-POP) | Note |
|---|---|---|---|---|
| Italy | 3.7 GHz (mid) | 2018 | **~EUR 0.36** | Highest in Europe; total auction ~EUR 6.5B |
| Germany | 3.6 GHz (mid) | 2019 | **~EUR 0.16 to 0.17** | Total ~EUR 6.5B incl. other bands |
| UK | 3.6-3.8 GHz (mid) | 2021 | **~EUR 0.08** | Total auction ~GBP 1.36B; "material discount to EUR 0.19 European average" |
| Belgium | 700 MHz (low) | 2021 | **~$0.49** | Above-average 700 MHz price |
| Greece / Czechia | 700 MHz + 3.5 GHz | 2020 | **~$0.02 to $0.033** | Central/Eastern Europe, an order of magnitude below US |
| Greece | 26 GHz (mmWave) | 2020 | **~$0.0016** | mmWave near-floor, consistent with US |

Sources: [Aetha - Italian 5G auction](https://www.aethaconsulting.com/the-italian-5g-auction-why-so-expensive/),
[Light Reading - Germany 5G](https://www.lightreading.com/mobile/5g/germanys--euro-6b-5g-auction-should-be-a-break-point-for-telecom/d/d-id/751720),
[telecoms.com - UK auction](https://www.telecoms.com/5g-6g/uk-extracts-1-36-billion-from-uk-operators-for-700-mhz-and-3-6-ghz-spectrum),
[Ofcom - final auction results](https://www.ofcom.org.uk/spectrum/spectrum-awards/final-spectrum-auction-results),
[PolicyTracker - 700 MHz pricing](https://www.policytracker.com/Bands/700-mhz-pricing/).

The European mid-band stays in a roughly **EUR 0.08 to 0.36 per MHz-POP** band, far below the US
C-band's ~$0.94. The two patterns hold across both continents: **mid-band is the priciest tier, and
mmWave sits near a floor.** The US simply pays a multiple of European prices for comparable mid-band,
a recurring finding in the auction literature
([Oxera - 5G spectrum pricing](https://www.oxera.com/insights/agenda/articles/5g-spectrum-the-varying-price-of-a-key-element-of-the-5g-revolution/)).

### Global scale

Spectrum awards worldwide hit about **$140 billion in 2021** (a record), versus about
**$37.7 billion in 2020**, with the US mid-band auctions driving most of the jump
([PolicyTracker via search](https://www.policytracker.com/blog/auctions-for-700-mhz-and-3-5-ghz-bands-drive-awards-in-q4-2020/)).
The point for this wiki: prime terrestrial cellular spectrum is a market measured in **tens of
billions of dollars per major-country auction**. It is not a resource a new entrant buys into
casually.

---

## 6. Who Controls It

**Governments are the allocators.** Spectrum is sovereign: each country's regulator decides what each
band is used for and who holds the license. The FCC (US), Ofcom (UK), and the Bundesnetzagentur
(Germany) are the relevant allocators above; the ITU coordinates internationally, most bindingly for
satellites (see [`rf_satcom.md`](../laser_comms/rf_satcom.md)).

**In the US, three carriers hold the prime cellular spectrum**, and they are differentiated by which
tier they won:

| Carrier | Low-band | Mid-band | mmWave |
|---|---|---|---|
| **T-Mobile** | **600 MHz** (won most of Auction 1002): best coverage layer | **2.5 GHz** (deep, from the Sprint acquisition) + Auction 108: deepest mid-band | Holds mmWave but de-emphasizes it |
| **Verizon** | 850 MHz / 700 MHz | **C-band** (n77, branded "5G Ultra Wideband"): bought heavily in Auction 107 | Early aggressive mmWave buyer |
| **AT&T** | 850 MHz / 700 MHz | **C-band** + **3.45 GHz** (n77): biggest Auction 110 spender | Holds mmWave |

Sources: [Light Reading / SDxCentral - carrier 5G plans](https://www.sdxcentral.com/analysis/verizon-att-t-mobile-5g-plans-spectrum-specific/),
[T-Mobile newsroom - C-band](https://www.t-mobile.com/news/network/t-mobile-further-solidifies-5g-leadership-position-with-successful-c-band-auction),
[Dgtl Infra - 3.45 GHz results](https://dgtlinfra.com/3-45-ghz-auction-110-results/).

The structural read: **the prime mid-band is fully spoken for.** T-Mobile's 2.5 GHz plus
Verizon/AT&T's C-band cover the sweet spot, and there is no comparable unassigned greenfield mid-band
block left to auction in the US. Low-band is similarly carved up among the three. That is the wall a
fresh entrant hits.

---

## 7. Ground vs Space Allocation

A frequency is allocated to a *service* (mobile, fixed, satellite, broadcast, radionavigation),
sometimes to several on a shared or primary/secondary basis. **Terrestrial and satellite uses are
governed and obtained through different doors**, which is the crux for Rocket Lab:

| | Terrestrial cellular | Satellite |
|---|---|---|
| Who decides | National regulator (FCC, Ofcom) | National regulator + **ITU international coordination** |
| How you get it | **Cash auction** (or administrative license) | **ITU filing with a priority date**, coordinated against earlier filers, first-come-first-served |
| What you pay | Up-front billions to the government | Mostly **time and coordination effort**, plus filing/lease cost, not a national cash auction |
| Key constraint | Prime bands already owned; price | Priority date, incumbent coordination, 7-year bring-into-use deadline |
| New-entrant reality | Effectively closed (must buy on secondary market) | A *narrow sliver* is attainable via the five paths in `rf_limited_service.md` |

The satellite column is the detailed subject of
[`rf_satcom.md`](../laser_comms/rf_satcom.md) and
[`rf_limited_service.md`](../laser_comms/rf_limited_service.md); it is summarized here only to draw the
contrast. The headline contrast: **you cannot out-bid Verizon for C-band, but you can plausibly
inherit or lease a satellite filing.** Some bands (C-band itself, 3.7-4.2 GHz) were historically
satellite downlink bands that regulators *re-allocated* to terrestrial mobile, which is why the
ground/space boundary is not fixed and is itself a regulatory battleground.

---

## 8. What a Fresh Entrant Would Pay and Do to Get Usable Spectrum

Putting the cost numbers against the new-entrant reality:

**The terrestrial-auction path is effectively closed.** To get a nationwide US mid-band footprint a
new entrant would need to win a primary auction, and the last greenfield mid-band slice (C-band) cost
**$81 billion**. There is no comparable unassigned mid-band left to auction, and the prime bands are
held by three incumbents who will defend them. Buying a national cellular spectrum position is not a
realistic move for an entrant the size of Rocket Lab.

**The realistic terrestrial options are secondary and partial**, and they mirror the satellite paths
already documented:

- **Lease** unused spectrum from a holder (secondary market, regulator-approved). Recurring cost,
  dependency on the lessor, but no auction. This is the ground-side version of Path B in
  [`rf_limited_service.md`](../laser_comms/rf_limited_service.md).
- **Partner / wholesale** onto an incumbent's licensed spectrum (an MVNO-style or hosted
  arrangement). Lowest regulatory risk, least vertical integration. Path C in that doc.
- **Shared / lightly-licensed bands** (US CBRS 3.5 GHz tiered access, newly-opened bands). Cheap or
  free to access, but lower power, shared, and locally constrained.

**For Rocket Lab specifically, the conclusion is that the spectrum fight should be fought in the
satellite domain, not the terrestrial one.** The terrestrial side is a closed, $10-billions market.
The satellite side is obtained through ITU coordination where a narrow sliver is attainable by
inheriting a distressed filing, leasing, or chasing newly-opened bands. That space-side path, its
feasibility, and what a sliver buys in throughput and users are fully worked out in
[`rf_limited_service.md`](../laser_comms/rf_limited_service.md) and not re-derived here. This doc's
contribution is to show, with the real auction numbers, *why* the terrestrial door is the wrong one
to knock on.

---

## Aside: China (excluded from the main analysis)

China is outside this analysis and noted only for completeness. China does **not** auction mobile
spectrum; the state administratively assigns it to the three state-controlled carriers (China Mobile,
China Unicom, China Telecom) at little or no direct cost, so Chinese "prices per MHz-POP" are not
comparable to the auction figures above and are excluded from the cost tables.

---

## Sources

US auctions:
- [EE Times - C-band auction brings home $80.9B](https://www.eetimes.com/c-band-auction-brings-home-80-9b/)
- [SpaceNews - FCC C-band auction raised nearly $81 billion](https://spacenews.com/c-band-raises-81-billion/)
- [FCC - Announces Winning Bidders in C-band Auction](https://www.fcc.gov/document/fcc-announces-winning-bidders-c-band-auction)
- [IEEE ComSoc - FCC Auction 110 rakes in $22.5 billion (3.45 GHz)](https://techblog.comsoc.org/2022/01/14/fcc-auction-110-rakes-in-22-5-billion-in-gross-proceeds-for-3-45-ghz-service/)
- [Fierce Network - FCC closes historic 3.45 GHz auction at $21.8B](https://www.fierce-network.com/wireless/fcc-closes-historic-345-ghz-auction-218b)
- [Dgtl Infra - 3.45 GHz Auction 110 results](https://dgtlinfra.com/3-45-ghz-auction-110-results/)
- [Fierce Network - AWS-3 auction ends at record $44.9B](https://www.fierce-network.com/wireless/it-s-over-fcc-s-aws-3-spectrum-auction-ends-at-record-44-9b-bids)
- [Wikipedia - AWS-3 auction](https://en.wikipedia.org/wiki/AWS-3_auction)
- [Cramton - Bidding and Prices in the AWS-3 Auction](https://cramton.umd.edu/papers2015-2019/cramton-aws-3-auction-prices.pdf)
- [CommLaw Monitor - $19.8 billion broadcast incentive auction (600 MHz)](https://www.commlawmonitor.com/2017/04/articles/internet/fcc-announces-the-results-of-the-19-8-billion-broadcast-incentive-auction/)
- [Light Reading - T-Mobile, Dish, Comcast big winners in 600 MHz auction](https://www.lightreading.com/mobile-core/t-mobile-dish-comcast-big-winners-in-19-8b-600mhz-auction)
- [Fierce Network - mmWave auction brings in more than $7.5B](https://www.fierce-network.com/regulatory/fcc-mmwave-auction-brings-more-than-7-5b-as-clock-phase-ends)
- [IEEE ComSoc - Analysis and results of FCC Auction 103 (mmWave)](https://techblog.comsoc.org/2019/12/10/analysis-and-results-of-fcc-auction-103-for-5g-mmwave-spectrum/)

European and global auctions:
- [Aetha Consulting - The Italian 5G auction: why so expensive?](https://www.aethaconsulting.com/the-italian-5g-auction-why-so-expensive/)
- [Light Reading - Germany's EUR 6B 5G auction](https://www.lightreading.com/mobile/5g/germanys--euro-6b-5g-auction-should-be-a-break-point-for-telecom/d/d-id/751720)
- [telecoms.com - UK extracts GBP 1.36 billion (700 MHz + 3.6 GHz)](https://www.telecoms.com/5g-6g/uk-extracts-1-36-billion-from-uk-operators-for-700-mhz-and-3-6-ghz-spectrum)
- [Ofcom - 700 MHz and 3.6-3.8 GHz final auction results](https://www.ofcom.org.uk/spectrum/spectrum-awards/final-spectrum-auction-results)
- [PolicyTracker - 700 MHz pricing](https://www.policytracker.com/Bands/700-mhz-pricing/)
- [PolicyTracker - 700 MHz and 3.5 GHz drive Q4 2020 awards](https://www.policytracker.com/blog/auctions-for-700-mhz-and-3-5-ghz-bands-drive-awards-in-q4-2020/)
- [Oxera - 5G spectrum: the varying price](https://www.oxera.com/insights/agenda/articles/5g-spectrum-the-varying-price-of-a-key-element-of-the-5g-revolution/)

Bands, tradeoff, and carriers:
- [Nokia - 5G spectrum bands explained (low, mid, high)](https://www.nokia.com/thought-leadership/articles/spectrum-bands-5g-world/)
- [Verizon - 5G spectrum and frequency bands explained](https://www.verizon.com/about/news/5g-frequency-bands-explained)
- [Spectrum.com - Understanding 5G bands](https://www.spectrum.com/resources/mobile/5g-bands)
- [T-Mobile - Why mid-band matters for 5G](https://www.t-mobile.com/business/resources/articles/why-mid-band-5g-matters)
- [Ericsson - Leveraging the potential of 5G millimeter wave](https://www.ericsson.com/en/reports-and-papers/further-insights/leveraging-the-potential-of-5g-millimeter-wave)
- [GeeksforGeeks - Maximum data rate (Shannon channel capacity)](https://www.geeksforgeeks.org/computer-networks/maximum-data-rate-channel-capacity-for-noiseless-and-noisy-channels/)
- [Cambridge Wireless - mMTC: backbone of the IoT revolution](https://www.cambridgewireless.co.uk/resource/mmtc-in-5g--the-backbone-of-the-iot-revolution.html)
- [Verizon - eMBB, URLLC and mMTC explained](https://www.verizon.com/about/news/5g-understanding-embb-urllc-mmtc)
- [SDxCentral - Verizon, AT&T, T-Mobile 5G plans, spectrum specific](https://www.sdxcentral.com/analysis/verizon-att-t-mobile-5g-plans-spectrum-specific/)
- [T-Mobile newsroom - C-band auction](https://www.t-mobile.com/news/network/t-mobile-further-solidifies-5g-leadership-position-with-successful-c-band-auction)

---

## Confidence

**Overall: medium-high.**

- **High confidence:** the US auction totals and the per-MHz-POP prices for C-band ($0.94),
  Auction 110 ($0.72), AWS-3 ($2.72 paired), and the mmWave floor ($0.002 to $0.007). Each is
  carried by 2+ independent sources. The speed-vs-connections physics (Shannon plus propagation) and
  the band-tier characteristics are standard, well-sourced material. The identity of which carrier
  holds which tier (T-Mobile low/2.5 GHz, Verizon/AT&T C-band) is well-established.
- **Medium confidence:** the exact European per-MHz-POP figures, several of which come from a single
  trade source each (flagged below). The directional finding (Europe well below the US, mid-band the
  priciest tier, mmWave near a floor) is robust; the precise decimals are not all double-sourced.
- **Lower confidence / time-sensitive:** exact current carrier MHz holdings, which change with every
  acquisition and secondary-market deal, and the precise 600 MHz per-MHz-POP figure, which is
  complicated by the incentive-auction two-sided structure.

**Single-source figures the lead should double-check** before relying on the exact decimal:
the UK ~EUR 0.08 and the "EUR 0.19 European average" (telecoms.com / Ofcom), Germany ~EUR 0.16-0.17
(Light Reading), Italy ~EUR 0.36 (Aetha), Belgium 700 MHz ~$0.49 and Greece/Czechia ~$0.02-0.033
(PolicyTracker), and the global $140B / $37.7B 2021-vs-2020 totals (PolicyTracker via search
snippet, not yet confirmed against a second source). The AWS-3 $2.72/MHz-POP paired figure comes
from a single search snippet attributed to FCC/Cramton data; the $44.9B total and 65 MHz are
double-sourced, but the per-MHz-POP decimal should be re-verified against the Cramton paper directly.

---

## Open Questions

- **What did the C-band incumbents (satellite operators) receive to vacate?** C-band was a satellite
  downlink band re-allocated to terrestrial 5G; the satellite operators (Intelsat, SES) received
  accelerated-relocation payments. The size of those payments is relevant to the ground-vs-space
  reallocation story and is not quantified here.
- **Is there any greenfield US mid-band left to auction?** The structural claim that the mid-band is
  fully spoken for should be checked against the FCC's forward auction pipeline (for example any 4.0
  to 4.2 GHz, 7/8 GHz, or upper-C extension proceedings) before being stated as settled.
- **What does a terrestrial spectrum lease actually cost per MHz-POP?** Auction prices are public;
  secondary-market lease rates are not, and the lease path is the realistic one for an entrant. A
  dedicated look at recent lease/transfer deals (for example any 600 MHz or 2.5 GHz leases) would put
  a number on the entrant's realistic cost.
- **How do CBRS / shared-band economics compare?** The US CBRS 3.5 GHz tiered model is the cheapest
  legitimate way onto mid-band; its Priority Access License auction (Auction 105) prices and the
  General Authorized Access (free) tier deserve their own short treatment.
- **Confirm the global $140B / $37.7B totals** against a primary GSMA or PolicyTracker report rather
  than a search snippet.

---

## Claims Table

| Claim ID | Claim | Value | Status | Sources |
|---|---|---|---|---|
| COMM-001 | US C-band (Auction 107, 2021) total raised | ~$80.9 billion | FACT | [EE Times](https://www.eetimes.com/c-band-auction-brings-home-80-9b/), [SpaceNews](https://spacenews.com/c-band-raises-81-billion/) |
| COMM-002 | US C-band average price | ~$0.94 per MHz-POP (~$1.30 in top 46 markets) | FACT | [EE Times](https://www.eetimes.com/c-band-auction-brings-home-80-9b/), [SpaceNews](https://spacenews.com/c-band-raises-81-billion/) |
| COMM-003 | US 3.45 GHz (Auction 110) total raised | ~$22.5 billion | FACT | [IEEE ComSoc](https://techblog.comsoc.org/2022/01/14/fcc-auction-110-rakes-in-22-5-billion-in-gross-proceeds-for-3-45-ghz-service/), [Fierce Network](https://www.fierce-network.com/wireless/fcc-closes-historic-345-ghz-auction-218b) |
| COMM-004 | US 3.45 GHz price | ~$0.72 per MHz-POP | FACT | [IEEE ComSoc](https://techblog.comsoc.org/2022/01/14/fcc-auction-110-rakes-in-22-5-billion-in-gross-proceeds-for-3-45-ghz-service/), [Dgtl Infra](https://dgtlinfra.com/3-45-ghz-auction-110-results/) |
| COMM-005 | US AWS-3 (Auction 97, 2014-15) total raised | ~$44.9 billion for 65 MHz | FACT | [Fierce Network](https://www.fierce-network.com/wireless/it-s-over-fcc-s-aws-3-spectrum-auction-ends-at-record-44-9b-bids), [Wikipedia](https://en.wikipedia.org/wiki/AWS-3_auction) |
| COMM-006 | US AWS-3 paired-spectrum price | ~$2.72 per MHz-POP (paired) | FACT (single source) | [Fierce Network](https://www.fierce-network.com/wireless/it-s-over-fcc-s-aws-3-spectrum-auction-ends-at-record-44-9b-bids) (cites FCC/Cramton); re-verify against [Cramton](https://cramton.umd.edu/papers2015-2019/cramton-aws-3-auction-prices.pdf) |
| COMM-007 | US 600 MHz incentive auction (2017) total | ~$19.8 billion; >$10B paid to broadcasters | FACT | [CommLaw Monitor](https://www.commlawmonitor.com/2017/04/articles/internet/fcc-announces-the-results-of-the-19-8-billion-broadcast-incentive-auction/), [Light Reading](https://www.lightreading.com/mobile-core/t-mobile-dish-comcast-big-winners-in-19-8b-600mhz-auction) |
| COMM-008 | US 24 GHz mmWave (Auction 102) total raised | ~$2.0 billion | FACT | [Fierce Network](https://www.fierce-network.com/regulatory/fcc-mmwave-auction-brings-more-than-7-5b-as-clock-phase-ends), [IEEE ComSoc](https://techblog.comsoc.org/2019/12/10/analysis-and-results-of-fcc-auction-103-for-5g-mmwave-spectrum/) |
| COMM-009 | US 24 GHz mmWave price | ~$0.007 per MHz-POP | FACT (single source) | [IEEE ComSoc - Auction 103](https://techblog.comsoc.org/2019/12/10/analysis-and-results-of-fcc-auction-103-for-5g-mmwave-spectrum/) |
| COMM-010 | US 37/39/47 GHz (Auction 103) total raised | ~$7.56 billion net | FACT | [Fierce Network](https://www.fierce-network.com/regulatory/fcc-mmwave-auction-brings-more-than-7-5b-as-clock-phase-ends), [IEEE ComSoc](https://techblog.comsoc.org/2019/12/10/analysis-and-results-of-fcc-auction-103-for-5g-mmwave-spectrum/) |
| COMM-011 | US 37/39/47 GHz price | ~$0.0019 per MHz-POP (~5x below 24 GHz) | FACT (single source) | [IEEE ComSoc - Auction 103](https://techblog.comsoc.org/2019/12/10/analysis-and-results-of-fcc-auction-103-for-5g-mmwave-spectrum/) |
| COMM-012 | Italy 3.7 GHz price (2018) | ~EUR 0.36 per MHz-POP; total ~EUR 6.5B | FACT (single source) | [Aetha](https://www.aethaconsulting.com/the-italian-5g-auction-why-so-expensive/) |
| COMM-013 | Germany 3.6 GHz price (2019) | ~EUR 0.16 to 0.17 per MHz-POP | FACT (single source) | [Light Reading](https://www.lightreading.com/mobile/5g/germanys--euro-6b-5g-auction-should-be-a-break-point-for-telecom/d/d-id/751720) |
| COMM-014 | UK 3.6-3.8 GHz price (2021) | ~EUR 0.08 per MHz-POP; total ~GBP 1.36B | FACT (single source) | [telecoms.com](https://www.telecoms.com/5g-6g/uk-extracts-1-36-billion-from-uk-operators-for-700-mhz-and-3-6-ghz-spectrum), [Ofcom](https://www.ofcom.org.uk/spectrum/spectrum-awards/final-spectrum-auction-results) |
| COMM-015 | European mid-band average | ~EUR 0.19 per MHz-POP (4 major markets) | ESTIMATE (single source) | [telecoms.com](https://www.telecoms.com/5g-6g/uk-extracts-1-36-billion-from-uk-operators-for-700-mhz-and-3-6-ghz-spectrum) |
| COMM-016 | Greece/Czechia 700 MHz + 3.5 GHz (2020) | ~$0.02 to $0.033 per MHz-POP | FACT (single source) | [PolicyTracker via search](https://www.policytracker.com/blog/auctions-for-700-mhz-and-3-5-ghz-bands-drive-awards-in-q4-2020/) |
| COMM-017 | Belgium 700 MHz price (2021) | ~$0.49 per MHz-POP | FACT (single source) | [PolicyTracker - 700 MHz pricing](https://www.policytracker.com/Bands/700-mhz-pricing/) |
| COMM-018 | Global spectrum awards, 2021 vs 2020 | ~$140 billion (2021) vs ~$37.7 billion (2020) | FACT (single source) | [PolicyTracker via search](https://www.policytracker.com/blog/auctions-for-700-mhz-and-3-5-ghz-bands-drive-awards-in-q4-2020/) |
| COMM-019 | 5G connection-density requirement (mMTC) | 1 million devices per square kilometer | FACT | [Cambridge Wireless](https://www.cambridgewireless.co.uk/resource/mmtc-in-5g--the-backbone-of-the-iot-revolution.html), [Verizon](https://www.verizon.com/about/news/5g-understanding-embb-urllc-mmtc) |
| COMM-020 | Shannon channel-capacity relationship | capacity = bandwidth x log2(1 + SNR) | FACT | [GeeksforGeeks](https://www.geeksforgeeks.org/computer-networks/maximum-data-rate-channel-capacity-for-noiseless-and-noisy-channels/) |
| COMM-021 | US prime mid-band holders | T-Mobile (2.5 GHz); Verizon + AT&T (C-band, n77) | FACT | [SDxCentral](https://www.sdxcentral.com/analysis/verizon-att-t-mobile-5g-plans-spectrum-specific/), [T-Mobile newsroom](https://www.t-mobile.com/news/network/t-mobile-further-solidifies-5g-leadership-position-with-successful-c-band-auction) |
| COMM-022 | US best low-band (600 MHz) holder | T-Mobile (won most of Auction 1002) | FACT | [Light Reading](https://www.lightreading.com/mobile-core/t-mobile-dish-comcast-big-winners-in-19-8b-600mhz-auction), [SDxCentral](https://www.sdxcentral.com/analysis/verizon-att-t-mobile-5g-plans-spectrum-specific/) |
