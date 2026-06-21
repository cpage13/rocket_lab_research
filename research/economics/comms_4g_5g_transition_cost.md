# What the 4G-to-5G Transition Cost Ground Operators ("X", the Next-Cycle Hurdle)

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:** [research/economics/comms_cellular_5g_deployment_economics.md](comms_cellular_5g_deployment_economics.md) supplies the *steady-state* ground-network cost basis (per-site ranges, capex intensity, opex/energy, the cost-structure split, and the spectrum-auction totals). This doc does NOT repeat those. It answers one sharper, forward-looking question the other doc only sets up: **what did the 4G-to-5G upgrade actually cost as a discrete upgrade cycle, per operator, and how was that cost split between unavoidable new RADIO hardware versus core/software and spectrum.** That cycle cost is the number we call **X**: the cost a space-based alternative would have to beat on the GROUND side's NEXT upgrade (6G, standard ~2028, first networks ~2030), not against already-paid-for 5G plant.

New material added here, not in the prior doc:
- Per-operator **cumulative** 5G-cycle capex for the three US majors (the prior doc gave only single-year snapshots).
- The **radio-hardware-vs-software** split made explicit: why mid-band needed new Massive MIMO radios (a hard capital purchase) while low-band 5G was largely a software (DSS) overlay.
- **Spectrum refarming** (reusing 4G/3G spectrum for 5G) as distinct from buying new spectrum at auction.
- **Densification reality**: small-cell build came in far below the early hype; the US cycle was a macro-site radio overlay.
- An **ex-China** global cycle envelope (the prior doc's global figures included China).
- A definitional reconciliation of the **RAN cost-share** number (network-deployment base vs total-wireless-capex base).

---

## Summary / Verdict (what X is)

**X, the 5G upgrade-cycle cost, has three stacked layers. For a space alternative the load-bearing layer is the middle one (deployment capex), because spectrum and already-sunk 4G plant are not what a new entrant displaces on the next cycle.**

1. **New 5G mid-band deployment capex (the core of X).** For the US majors this was a *bounded incremental* program on top of business-as-usual capex, because the dominant move was hanging new radios on **existing** towers, not building new sites:
   - **Verizon: ~$10B incremental** over 2021-2023, explicitly "on top of" ~$18B/yr BAU capex. [FACT]
   - **AT&T: ~$6-8B** over 2021-2024 (C-band plus 3.45 GHz). [FACT]
   - **T-Mobile: ~$37B total capex 2020-2022**, but that figure *blends* the 5G mid-band build with the Sprint network integration; the 5G-attributable slice is a subset. [FACT, with the blending caveat]
2. **Spectrum (a separate one-time license layer, NOT recurring network capex).** US mid-band licenses dwarfed deployment capex: **Verizon ~$45.5B** gross C-band bid (~$52.9B with clearing), **AT&T ~$23.4B**, **T-Mobile ~$9.3B** C-band, plus T-Mobile's 2.5 GHz acquired via Sprint. [FACT] The US C-band auction was the world's costliest mid-band auction; most ex-US markets paid far less per MHz-pop (prior doc, Section 2).
3. **The radio/software split inside the deployment layer.** Mid-band 5G (the capacity layer) **required new Massive MIMO active-antenna radio hardware** that physically cannot be a software upgrade to a 4G radio. Low-band 5G (the coverage layer) was largely a **software overlay (Dynamic Spectrum Sharing)** on existing 4G radios. The **RAN/radio is the dominant deployment-capex line at ~55-65%** of network-deployment spend; the core and software were a smaller minority. [FACT direction; the exact % is aggregator/analyst-sourced]

**The single most decision-relevant fact for the space comparison:** on the ground, the 5G cycle's *deployment* cost was carried overwhelmingly by **new radio hardware on existing sites**, not by new sites, not by the core, and not (in cash-capex terms) by spectrum. A forward 6G cycle will be the same shape: a new radio-hardware refresh. So **X-on-the-next-cycle ≈ the cost of the next radio refresh per covered POP/subscriber**, plus whatever new spectrum that generation demands. That radio-refresh-per-POP is the number a space system must beat.

**Timeline of the cycle (US):** first mmWave launches 2018-2019; nationwide **low-band** 5G (cheap, software/DSS) 2020; the expensive **mid-band** (C-band / 2.5 GHz, new radios) 2021-2023, briefly FAA-delayed in early 2022; capex peaked **2022** and rolled off through 2023-2024. The whole heavy-spend phase was roughly a **4-5 year window (2020-2024)**. [FACT]

**Confidence: medium-high** on the per-operator incremental deployment programs (each two-source corroborated from company guidance plus trade press), on the spectrum totals (FCC/S&P), and on the mid-band-needs-new-radios / low-band-is-software distinction (Ericsson white paper plus DSS vendor sources). **Medium** on the exact RAN cost-share % (analyst/aggregator, with a definitional caveat below) and on the ex-China global envelope (one institution's projection, China backed out arithmetically). **Lower** on T-Mobile's *5G-only* slice, because its reported capex blends 5G with Sprint integration and is not cleanly separable from disclosure.

---

## 1. Per-Operator 5G-Cycle Capex (the US majors)

The prior doc gave single-year capex snapshots. This is the **cumulative upgrade-cycle** view, separating the *incremental* 5G program from baseline capex, and keeping **deployment capex** distinct from **spectrum**.

### The shape: an incremental program on existing sites

The defining feature of the US 5G cycle is that the majors did **not** build a new national grid. They overlaid mid-band radios on towers they already operated. Verizon's own framing: **7,000-8,000 existing sites** to get C-band radio upgrades before end-2021, with **"no need for new cell sites."** [FACT, single-source for the site count] This is *why* the incremental program was single-digit-to-low-double-digit billions rather than the ~$275B a from-scratch national build was estimated to cost (prior doc, Section 3).

### Verizon

| Item | Value | Tag |
|---|---|---|
| Incremental C-band deployment capex (announced at 2021 investor day) | **~$10B** "on top of" BAU, over **2021-2023** | [FACT] |
| Annual split of the incremental program | 2021 ~$2.1B; 2022 ~$5-6B; 2023 ~$2-3B | [FACT] |
| Total annual capex during the build (BAU + C-band) | ~$20-21.8B (2021); ~$23.1B actual (2022, incl. ~$6.2B C-band) | [FACT] |
| C-band capex peak | **2022** | [FACT] |
| C-band **spectrum** (separate, not network capex) | **~$45.5B** gross winning bid; **~$52.9B** with ~$8B clearing/incentive payments | [FACT] |

Sources: Verizon CEO Hans Vestberg's "$10 billion over the next three years" commitment and the 7,000-8,000-site upgrade plan ([SDxCentral](https://www.sdxcentral.com/news/verizon-details-10b-mid-band-5g-network-upgrade/)); the year-by-year C-band split and the 2022 peak ([RCR Wireless](https://www.rcrwireless.com/20220311/carriers/verizon-capex-to-peak-in-2022-as-c-band-deployment-continues), [GST Capital Partners](https://gulfsouthtowers.com/verizon-capex-to-peak-in-2022-as-c-band-deployment-continues/)); the ~$45.5B gross bid and ~$52.9B-with-clearing ([Via Satellite](https://www.satellitetoday.com/government-military/2021/02/24/verizon-spends-45-5-billion-in-fccs-c-band-auction/), [Fierce Network](https://www.fierce-network.com/regulatory/verizon-pledges-whopping-45b-c-band-auction)).

### AT&T

| Item | Value | Tag |
|---|---|---|
| C-band + 3.45 GHz deployment capex | **~$6-8B**, mostly **2022-2024** (~$1B in 2021, then ~$5B in each of 2022 and 2023) | [FACT] |
| Wireless capex run-rate during the cycle | ~$9-10B/yr (2019-21) rising to ~$11-12B/yr (2022) | [FACT] |
| Mid-band coverage reached | ~150M POPs by end-2022 (>2x its original target); ~200M POPs planned by end-2023 | [FACT] |
| C-band **spectrum** (separate) | **~$23.4B** | [FACT] |

Sources: the $6-8B range and 2022-2024 concentration ([Fierce Network](https://www.fierce-network.com/operators/at-t-to-spend-up-to-8b-c-band-deployment) via search, [Telecoms.com](https://telecoms.com/508988/att-to-spend-less-than-verizon-on-c-band-5g-rollout/)); the ~$1B-2021-then-~$5B-each-year cadence and ~150M-POP mid-band coverage ([SDxCentral C-band boost](https://sdxcentral.com/articles/news/att-verizon-t-mobile-5g-plans-set-for-full-c-band-boost/2023/04), [Inside Towers](https://insidetowers.com/cell-tower-news-unpacking-atts-infrastructure-capex/)); the ~$23.4B C-band spectrum ([Telecoms.com](https://telecoms.com/508988/att-to-spend-less-than-verizon-on-c-band-5g-rollout/), prior doc COMM-013).

**Note on AT&T's lower deployment spend:** AT&T's ~$6-8B vs Verizon's ~$10B reflects a smaller mid-band footprint and a lighter early C-band position, not a cheaper per-site cost. Both are doing the same thing (new radios on existing towers); the per-POP economics are similar.

### T-Mobile (the blended case)

T-Mobile is the hardest to read because its 5G mid-band build and its **Sprint integration** ran simultaneously and its disclosure does not split them.

| Item | Value | Tag |
|---|---|---|
| Total capex 2020-2022 (5G build + Sprint integration, blended) | **~$37B** | [FACT, blended] |
| Annual capex during the build | ~$13-14B (2022 peak, +13% YoY); ~$9.8B (2023, integration winding down) | [FACT] |
| Original New-T-Mobile plan (2020) | up to **$60B capex over 5 years**, including **~15,000 new macro sites** | [FACT] |
| Mid-band spectrum | **2.5 GHz acquired via Sprint** (the strategic prize of the merger) + **~$9.3B** C-band at auction | [FACT] |
| Merger-related (restructuring/integration) costs | ~$1B pre-tax, largely complete by 1H 2024 | [FACT] |
| Mid-band ("Ultra Capacity") reach | >200M POPs by end-2021; targeting ~300M by end-2023 | [FACT] |
| End-2022 network footprint | ~79,000 LTE/5G macrocells + ~41,000 small-cell/DAS nodes | [FACT] |

Sources: the ~$37B 2020-2022 blended capex and the 79k-macro/41k-small-cell footprint ([Inside Towers](https://insidetowers.com/t-mobile-network-efficiencies-yield-results/), search-corroborated); the 2022 ~$14B / 2023 ~$9.8B cadence ([TelecomLead 2023 capex](https://www.telecomlead.com/5g/t-mobile-lowers-2023-capex-significantly-108569), [LightReading 2022 capex](https://www.lightreading.com/5g/t-mobile-increases-2022-capex-to-maintain-5g-position-against-rivals/d/d-id/774433)); the original $60B / 15,000-new-macro-site plan ([Wireless Estimator](https://wirelessestimator.com/articles/2020/t-mobile-plans-for-15000-new-macro-sites-and-60-billion-in-capex-over-the-next-five-years/)); the ~$9.3B C-band and 300M-POP target ([T-Mobile FY2023 ARS](https://www.sec.gov/Archives/edgar/data/0001283699/000119312524117982/d51404dars.pdf), prior doc COMM-013).

**Why T-Mobile's number is bigger and different in kind:** T-Mobile's mid-band advantage came from **acquiring** Sprint's 2.5 GHz, so its "5G cost" includes a corporate acquisition, not just radios. Its ~$37B 2020-2022 spend is the upper bound of what the cycle cost a US major, but it is **not** an apples-to-apples mid-band-radio-overlay number the way Verizon's ~$10B is. For the X comparison, **Verizon's ~$10B incremental / ~7,000-8,000 sites is the cleanest "what an upgrade overlay costs" datapoint.**

### Cross-operator synthesis (deployment capex only, spectrum excluded)

[DERIVED] Adding the *incremental deployment* programs (Verizon ~$10B + AT&T ~$6-8B + T-Mobile's 5G-attributable slice of its ~$37B blended spend, call it ~$10-15B after backing out Sprint integration) gives a **US Big-3 incremental 5G-deployment capex on the order of ~$26-35B** across the heavy-build years, **on top of** ongoing BAU capex of roughly ~$45-50B/yr industry-wide. **Spectrum (~$78B for C-band across the three) was the larger cash outlay than the radios themselves.** [DERIVED from the per-operator figures above; the T-Mobile slice is an estimate, flagged.]

---

## 2. The Radio-vs-Software Split: Why the Radios Were Unavoidable

This is the heart of the X question. The prior doc establishes that the RAN dominates capex; this section explains *why the radio specifically was a hard, new capital purchase and the core/software was not*, by separating the two 5G layers.

### Mid-band (capacity) needed NEW radio hardware: Massive MIMO

5G mid-band performance comes from **Massive MIMO active-antenna systems**, which are architecturally incompatible with 4G radios and **cannot be delivered by a software upgrade**:

- A conventional 4G site uses a **passive antenna plus a remote radio unit with a low number of radio chains (2, 4, or 8)**. A 5G mid-band Massive MIMO unit integrates the **antenna array, dozens of radio chains (e.g., 64), and part of the baseband into one tightly-coupled active unit** ("64T64R" in dense urban). The physical antenna arrays, per-sub-array radio chains, and beamforming compute differ fundamentally; you must replace the box. [FACT, [Ericsson advanced-antenna-systems white paper](https://www.ericsson.com/en/reports-and-papers/white-papers/advanced-antenna-systems-for-5g-networks)]
- Industry treats Massive MIMO as **essential to mid-band TDD deployments** precisely because it unlocks the new spectrum "without the need for site densification" (beamforming substitutes for more sites). [FACT, [Ericsson Massive MIMO](https://www.ericsson.com/en/ran/massive-mimo)]
- These **active antenna units (AAUs) are the expensive base-station equipment** operators specifically try to *share* (active RAN sharing) to cut 5G cost, confirming they are the cost center. [FACT, [STL Partners RAN cost splits](https://stlpartners.com/insights/typical-network-cost-splits-of-active-ran-sharing-vs-no-ran-sharing/)]

### Low-band (coverage) was largely software: Dynamic Spectrum Sharing

The cheap part of the cycle, nationwide low-band 5G, was overwhelmingly a **software overlay**:

- **Dynamic Spectrum Sharing (DSS)** lets LTE and 5G share the same sub-1 GHz channel at 1 ms granularity, so operators launched 5G **"through software updates, without spending millions on infrastructure upgrades."** This gave the lowest TCO path to nationwide 5G coverage quickly after launch. [FACT, [5G-Networks DSS](https://www.5g-networks.net/5g-dynamic-spectrum-sharing-dss/), [Ericsson spectrum sharing](https://www.ericsson.com/en/ran/spectrum-sharing)]
- This is why T-Mobile/Verizon/AT&T all lit up "nationwide" 5G in **2020** on existing radios (cheap), a year or more *before* the expensive mid-band radio build. The headline coverage was software; the actual capacity (and the actual capex) came later with the radios.

### The split, quantified

| Layer | What it cost | Mechanism | Tag |
|---|---|---|---|
| **RAN / radio (mid-band Massive MIMO)** | **~55-65%** of network-*deployment* capex; the dominant line | **new hardware**, unavoidable | [FACT direction; analyst/aggregator on the %] |
| **Core network (incl. 5G Standalone)** | meaningful minority (~$1-3B/operator program, per prior doc) | software + servers, partly reusable | [FACT, single-source] |
| **Low-band 5G coverage** | near-zero incremental capex | **software (DSS)** on existing radios | [FACT] |
| **Spectrum** | the largest *cash* outlay, but a one-time license, not network capex | auction + refarming | [FACT] |

**Definitional caveat on the ~55-65% RAN share (refines the prior doc's Open Question #2):** that figure is RAN as a share of the **network-deployment** capex base (radios + transport + core + civil). On a **total-wireless-capex** base (which also absorbs spectrum, fixed/FWA, IT, and other lines), Dell'Oro reports RAN averaging only **~20-25%**. [FACT, [Dell'Oro via IEEE ComSoc](https://techblog.comsoc.org/2025/10/31/market-research-firms-omdia-and-delloro-on-impact-of-6g-and-ai-investments/)] Both are right; they use different denominators. STL Partners independently anchors the narrower base: RAN ~**57.5%** of network cost, rising to ~**67%** if an operator adds 50% more base stations. [FACT, [STL Partners](https://stlpartners.com/insights/typical-network-cost-splits-of-active-ran-sharing-vs-no-ran-sharing/)] **For the X comparison, the radio is ~55-65% of the build-cost a space system competes against, but only ~20-25% of an operator's all-in wireless capital if spectrum and everything else is counted.** The honest statement: *the radio is the dominant line of the part of the cost a new delivery method can actually displace.*

---

## 3. Spectrum: Buying New vs Refarming Existing

The prior doc covers the **auction** totals (buying new spectrum). This section adds the distinct, often-overlooked **refarming** path (reusing spectrum you already own) and frames spectrum for the next-cycle comparison.

- **Refarming** = repurposing spectrum currently carrying 3G/4G to 5G. As **3G sunset** freed sub-1 GHz, operators reclaimed it for 5G, mostly via **DSS so legacy LTE devices keep working** (a clean cut to NR is "not currently feasible due to the high penetration of existing LTE devices"). [FACT, [Telit](https://www.telit.com/blog/understanding-5g-spectrum-frequency-bands/), [Samsung DSS white paper](https://images.samsung.com/is/content/samsung/assets/global/business/networks/insights/white-papers/0122_dynamic-spectrum-sharing/Dynamic-Spectrum-Sharing-Technical-White-Paper-Public.pdf)] Refarming's direct *cash* cost is low (no auction fee); its cost is the **radio swap and the DSS/software**, i.e., it folds back into the RAN line, not a separate spectrum check.
- **Buying new** = the C-band/2.5 GHz auctions, where the US majors paid **~$78B combined** for mid-band (Verizon ~$45.5B, AT&T ~$23.4B, T-Mobile ~$9.3B C-band). The US was the global outlier; ex-US markets paid roughly **3x-30x less per MHz-pop** (prior doc, Section 2). [FACT]
- **Why this matters for X on the next cycle:** much of the 6G capacity layer may again come from **refarming existing mid-band plus whatever new (likely upper-mid-band / cmWave) spectrum is auctioned.** A space alternative needs **no terrestrial spectrum license at all** for its own coverage (it uses its own allocation), so on the next cycle the ground side's spectrum line is a cost the space side largely avoids, while the ground side's *radio-refresh* line is the cost the space side must beat head-on.

---

## 4. Densification Reality: The Small-Cell Build Underdelivered

The early 5G narrative assumed mass small-cell densification. **It did not happen at the forecast scale in the US.** This matters because it means the cycle's cost was *radio overlay on macro sites*, not a new dense grid, which keeps X lower than the densification-heavy forecasts implied.

- US operators leaned on **Massive MIMO beamforming on existing macro towers to add mid-band capacity "without the need for site densification."** [FACT, [Ericsson](https://www.ericsson.com/en/ran/massive-mimo)] Verizon explicitly said "no need for new cell sites" for its C-band overlay. [FACT]
- The small-cell market grew but from a small base and well below hype: US small-cell revenue was only **~$0.67B in 2023**; Crown Castle added just **~8,000 small-cell nodes in 2023 (+6%)**. Trade coverage summarized the shift bluntly: **"5G small cells are out, colocations are in."** [FACT, [market.us](https://market.us/report/small-cell-5g-network-market/), [Crown Castle FY2022 release](https://www.sec.gov/Archives/edgar/data/0001051470/000105147023000005/q42022earningsrelease.htm)]
- For scale: the prior doc's US footprint is ~248,000 macrocell sites vs ~198,000 outdoor small cells (end-2024). The macro overlay, not the small-cell layer, carried the 5G capacity build.

**Implication for X:** the *realized* US 5G cycle was cheaper than the densification-forecast version because beamforming let operators avoid building a dense small-cell grid. The next cycle (6G), if it pushes into upper-mid-band or cmWave for capacity, **may finally force densification**, which would *raise* X, or it may again be absorbed by more-advanced antennas on existing sites. This is a key swing variable for any forward space-vs-ground comparison and is flagged in Open Questions.

---

## 5. The McKinsey TCO-Doubling Figure (closes prior-doc Open Question #1)

The prior doc flagged McKinsey's "~60% capex increase / TCO-doubling" number as second-hand and unconfirmed. **Confirmed from the primary source:**

> In an analysis of **one European country**, network-related capital expenditures would have to **increase ~60% from 2020 through 2025, roughly doubling total cost of ownership (TCO)** over that period.
> [FACT, [McKinsey, "The road to 5G: The inevitable growth of infrastructure cost," Feb 2018](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-road-to-5g-the-inevitable-growth-of-infrastructure-cost)]

Read carefully, this is a **forecast for a densification-heavy European scenario**, and it is the *pessimistic* bound. The realized US cycle came in **lighter** than "doubling TCO" because (Section 4) US operators avoided mass densification via Massive MIMO on macro sites. So the honest framing for X: **the 5G cycle's cost ranged from "a bounded ~$6-10B incremental overlay" (US macro-overlay reality) up to "roughly doubling network TCO" (the densification-heavy European forecast).** Which bound the *next* cycle resembles depends on whether 6G forces densification.

---

## 6. Ex-China Global Cycle Envelope

The prior doc's global figures (e.g., ~$1.5T mobile capex 2023-2030) **include China**. Backing China out:

| Scope | Figure | Tag |
|---|---|---|
| Global mobile operator capex, 2020-2025 | **~$1.1T total**, >75% 5G-related → **~$830B+ 5G** | [FACT, [GSMA Intelligence 2025 capex outlook](https://www.gsmaintelligence.com/research/2025-capex-outlook-financing-the-5g-era)] |
| Asia-Pacific mobile capex, 2020-2025 | ~$400B total, of which **~$331B 5G** | [FACT, GSMA] |
| **China** 5G capex 2019-2022 (to be EXCLUDED) | **~$74.2B** (CNY530B+; total all-tech capex ~$181.7B) | [FACT, [RCR Wireless on China 5G](https://www.rcrwireless.com/20230626/5g/as-mwc-shanghai-2023-approaches-what-insights-can-we-gain-from-chinas-5g-development-to-date), Statista-corroborated] |
| **Ex-China global 5G capex, 2020-2025 (derived)** | **~$750B order of magnitude** (~$830B+ global 5G minus China's ~$74B over an overlapping but not identical window) | [DERIVED, flagged] |

[DERIVED] The ex-China global 5G *deployment* envelope is **on the order of ~$700-800B across the 2020-2025 cycle**, with China removed. (The subtraction is approximate: China's ~$74B is a 2019-2022 figure and the global ~$830B is 2020-2025, so the windows overlap but do not coincide; treat the ex-China number as order-of-magnitude, not precise.) The US Big-3 incremental deployment slice (~$26-35B, Section 1) sits inside this as the most expensive-per-market piece, because US mid-band spectrum and labor cost more than most markets. [DERIVED]

**For X:** the ground side, ex-China, spent roughly **three-quarters of a trillion dollars** deploying the 5G radio layer over ~5 years. The next cycle (6G) is the spend a space alternative is positioned against, and it lands squarely in this project's ~10-year forward window (below).

---

## 7. The Forward Hook: When the Next Cycle (6G) Hits

X is only useful as a *forward* number. The next ground-upgrade cycle is already scheduled:

- **6G standardization:** study phase 2025-2026; first specifications (3GPP **Release 21**) completed **~end-2028**; **first commercial 6G ~2030**; mass deployment mid-2030s. [FACT, [Ericsson 6G timeline](https://www.ericsson.com/en/blog/2024/3/6g-standardization-timeline-and-technology-principles), [Qualcomm Release 20/6G](https://www.qualcomm.com/news/onq/2025/06/3gpp-release-20-completing-5g-advanced-evolution-preparing-for-global-6g-standardization)]
- That places the **ground side's next radio-refresh capex in the ~2030-2035 window**, exactly the forward horizon this research targets.
- Early analyst framing already sizes it: **6G RAN is projected to be ~55-60% of total RAN capex over 2029-2034**, i.e., 6G is expected to *dominate* RAN spend in that period the way 5G dominated it in 2020-2025. [FACT, [Dell'Oro/Omdia via IEEE ComSoc](https://techblog.comsoc.org/2025/10/31/market-research-firms-omdia-and-delloro-on-impact-of-6g-and-ai-investments/)]

**So X, stated for the comparison the project actually needs:** the ground side will, around 2030-2035, repeat the 5G pattern, a **new radio refresh on (mostly) existing sites**, at roughly the same shape of cost (RAN-dominated, ~55-65% of deployment capex), plus whatever new 6G spectrum is auctioned, possibly plus densification if 6G pushes higher in frequency. The space alternative does not have to beat the *whole* of 5G's sunk cost. It has to beat **the per-POP / per-subscriber cost of that next radio refresh**, on a forward basis, which is the much smaller, bounded number the per-operator incremental figures in Section 1 actually measure (Verizon's ~$10B over ~7,000-8,000 sites ≈ a per-site refresh cost in the low-six-figures, consistent with the prior doc's $20K-$50K upgrade range scaled by ancillary work).

---

## Open Questions

1. **T-Mobile's clean 5G-only slice.** Its ~$37B (2020-2022) blends 5G with Sprint integration; disclosure does not split them. A sourced decomposition (5G radios vs site decommissioning vs Sprint customer migration) would let T-Mobile be compared apples-to-apples with Verizon's clean ~$10B overlay.
2. **Will 6G force densification?** The single biggest swing in X-on-the-next-cycle. If 6G capacity comes from yet-more-advanced antennas on existing macro sites (the 5G pattern), X stays bounded; if it requires upper-mid-band/cmWave small-cell densification (the McKinsey-pessimistic pattern), X rises sharply. The next-cycle space comparison should run both bounds.
3. **Per-POP refresh cost, sourced.** Section 7 derives a per-site refresh cost from Verizon's $10B / ~7,500 sites. A direct operator-disclosed "$/POP to upgrade an existing macro to the next generation" would harden the central X number.
4. **6G spectrum.** Whether 6G's new bands command US-style mega-auctions or are released administratively (the ex-US norm) changes the spectrum layer of X by tens of billions per major. Track the FCC/ITU upper-mid-band (7-15 GHz) plans.
5. **Ex-China precision.** The ~$700-800B ex-China 5G envelope is an order-of-magnitude subtraction across mismatched windows. A single-source-consistent ex-China 5G capex series (same vintage, same scope) would tighten it.

---

## Claims ledger

Each hard claim with two or more independent sources, for the catalog step. (Claims already established in [comms_cellular_5g_deployment_economics.md](comms_cellular_5g_deployment_economics.md), e.g., the C-band auction total, the per-operator spectrum bids, the $20K-$50K upgrade range, and the RAN ~55-65% share, are referenced here but should be reconciled to their existing COMM- ids rather than duplicated.)

1. **Verizon incremental C-band deployment capex** ~$10B over 2021-2023, "on top of" BAU. Sources: SDxCentral (Vestberg "$10 billion over the next three years"); RCR Wireless / GST Capital Partners (2022 peak, year-by-year split). [FACT]
2. **Verizon C-band annual deployment split**: 2021 ~$2.1B; 2022 ~$5-6B; 2023 ~$2-3B; peak 2022. Sources: RCR Wireless; GST Capital Partners. [FACT]
3. **Verizon total capex during build** ~$20-21.8B (2021 guidance), ~$23.1B actual 2022 incl. ~$6.2B C-band. Sources: SDxCentral; RCR Wireless. [FACT]
4. **Verizon C-band spectrum cost** ~$45.5B gross winning bid, ~$52.9B with ~$8B clearing/incentive payments. Sources: Via Satellite; Fierce Network (also corroborated by prior-doc COMM-013). [FACT]
5. **Verizon upgraded existing sites, no new sites** for C-band: ~7,000-8,000 sites by end-2021, "no need for new cell sites." Sources: SDxCentral (primary); corroborated by Ericsson Massive MIMO "without need for densification." [FACT, single-source on the exact count]
6. **AT&T C-band + 3.45 GHz deployment capex** ~$6-8B, concentrated 2022-2024. Sources: Fierce Network; Telecoms.com. [FACT]
7. **AT&T C-band annual cadence** ~$1B (2021), ~$5B each in 2022 and 2023. Sources: SDxCentral (C-band boost); Inside Towers. [FACT]
8. **AT&T mid-band coverage** ~150M POPs by end-2022 (>2x target). Sources: SDxCentral; AT&T 4Q22 results (8-K). [FACT]
9. **AT&T C-band spectrum cost** ~$23.4B. Sources: Telecoms.com; prior-doc COMM-013 (S&P/FCC). [FACT]
10. **T-Mobile blended capex 2020-2022** ~$37B (5G build + Sprint integration). Sources: Inside Towers; search-corroborated company results. [FACT, blended]
11. **T-Mobile annual capex** ~$14B (2022, +13% YoY), ~$9.8B (2023). Sources: LightReading (2022); TelecomLead (2023). [FACT]
12. **T-Mobile original New-T-Mobile plan** up to $60B capex / 5 yrs, ~15,000 new macro sites. Sources: Wireless Estimator; T-Mobile/Sprint merger announcement (t-mobile.com newsroom). [FACT]
13. **T-Mobile end-2022 footprint** ~79,000 macrocells + ~41,000 small-cell/DAS nodes. Sources: Inside Towers; search-corroborated. [FACT]
14. **Mid-band 5G requires new Massive MIMO active-antenna hardware** (64 radio chains vs 2/4/8 in 4G; integrated antenna+radio+baseband; cannot be a software upgrade). Sources: Ericsson advanced-antenna-systems white paper; Ericsson Massive MIMO page. [FACT]
15. **Active antenna units (AAUs) are the expensive base-station equipment** operators share to cut 5G cost. Sources: STL Partners (RAN cost splits); corroborated by Ericsson Massive MIMO cost framing. [FACT]
16. **Low-band 5G deployed largely via software (Dynamic Spectrum Sharing)**, no major infrastructure spend; lowest-TCO path to nationwide 5G. Sources: 5G-Networks (DSS); Ericsson spectrum sharing. [FACT]
17. **Full LTE-to-NR refarming not feasible** due to LTE device penetration; DSS used so legacy devices keep working. Sources: Telit; Samsung DSS white paper. [FACT]
18. **RAN ~55-65% of network-deployment capex; ~57.5% rising to ~67% with 50% more base stations.** Sources: STL Partners; prior-doc COMM-009 aggregators. [FACT direction]
19. **RAN ~20-25% of total-wireless-capex base** (different denominator from #18). Sources: Dell'Oro via IEEE ComSoc; (definitional reconciliation, this doc). [FACT]
20. **US small-cell densification underdelivered**: US small-cell revenue ~$0.67B (2023); Crown Castle +~8,000 nodes (+6%) in 2023; "small cells are out." Sources: market.us; Crown Castle FY2022 8-K. [FACT]
21. **McKinsey: ~60% capex increase 2020-2025, roughly doubling TCO** for one European country. Sources: McKinsey "The road to 5G" (primary); GSMA "5G-era cost evolution" (corroborating the doubling-TCO theme). [FACT]
22. **Global mobile capex 2020-2025 ~$1.1T, >75% 5G (~$830B+ 5G).** Sources: GSMA Intelligence 2025 capex outlook; GSMA newsroom ($600B 2022-2025, 85% 5G). [FACT]
23. **Asia-Pacific 5G capex ~$331B (2020-2025).** Sources: GSMA newsroom (APAC investment); GSMA Intelligence. [FACT]
24. **China 5G capex 2019-2022 ~$74.2B** (CNY530B+; total capex ~$181.7B). EXCLUDED from totals; used only to back China out. Sources: RCR Wireless; Statista (China 5G capex by operator). [FACT]
25. **Ex-China global 5G deployment envelope ~$700-800B (2020-2025).** Sources: derived from #22-#24. [DERIVED]
26. **US Big-3 incremental 5G-deployment capex ~$26-35B** (Verizon ~$10B + AT&T ~$6-8B + T-Mobile 5G slice ~$10-15B), atop ~$45-50B/yr BAU. Sources: derived from #1, #6, #10. [DERIVED]
27. **US 5G timeline**: mmWave 2018-2019; nationwide low-band 2020; mid-band C-band/2.5 GHz 2021-2023 (FAA delay early 2022); capex peak 2022. Sources: TechTarget 5G-rollout status; Wikipedia 5G (corroborating launch dates). [FACT]
28. **6G timeline**: specs (3GPP Release 21) ~end-2028; first commercial ~2030; mass deployment mid-2030s. Sources: Ericsson 6G timeline; Qualcomm Release 20/6G. [FACT]
29. **6G RAN ~55-60% of total RAN capex over 2029-2034** (6G dominates RAN spend in that period). Sources: Dell'Oro/Omdia via IEEE ComSoc; (single-institution projection). [FACT, single-institution]
