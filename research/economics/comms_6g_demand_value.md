# 6G Reality and Demand Value: Will Users Pay a Premium, or Is It a Forced Cost?

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:** This doc extends the diminishing-returns finding established in two existing docs and does not repeat their derivations:

- [comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md), Section 4.1, the strongest finding in the whole base: broadband willingness-to-pay (WTP) is sharply concave (about $2.34/Mbps at 4-10 Mbps collapsing to about $0.02/Mbps at 100-1,000 Mbps), gigabit is available to over 91% of US homes but bought by only about 30%, the modal household sits at 200-500 Mbps, and ARPU is flat-to-declining. The value curve rewards reach and reliability, not raw bandwidth.
- [comms_cellular_5g_deployment_economics.md](comms_cellular_5g_deployment_economics.md): 5G is a low-teens-percent-of-revenue capex business (capex intensity peaked at about 19% in 2022, easing toward 14-15%), with a roughly 8-10 year payback, and "5G has largely not delivered an ARPU premium." Capex intensity is *falling*, not rising.

This doc adds the **next generation** to that picture. It asks a narrow question: what is 6G actually, and on the demand side, will end users pay extra for it? The thesis it tests is that 6G is a **cost operators are forced to bear that users will not pay extra for**, which squeezes ground margins and is therefore a *window* for a cheaper alternative delivery method, not a demand wave a new entrant must outrun.

> **Reading guide.** Every hard number is tagged **[FACT]** (sourced to 2+ independent bodies), **[FACT, single-source]** (one source only), **[ESTIMATE]** (research-firm sizing or soft figure), or **[DERIVED]** (this doc's own inference). Numbers carry sources inline.

> **Scope.** Isolated to the 6G demand-value question. **China is excluded** from all market figures and noted only once as a labelled aside. **No verdict** on the Rocket Lab comms business is offered; this is a demand-side input to the model.

> **Forward-looking framing.** This is a roughly ten-year-out question. Exact 2026 figures are a base; the trajectory matters more. The 6G commercial window (around 2030) and the next ground upgrade cycle it represents are the point of the doc.

---

## Summary / Verdict

**Confidence: high on the demand-side conclusion (it is the same diminishing-returns curve, now corroborated by 6G-specific operator statements); medium-high on the technical reality (standards bodies and vendors converge, but targets are still draft and span wide ranges); the forced-cost framing is stated as a well-supported working hypothesis, not a settled verdict.**

Four findings.

1. **6G is real as a standards program, with a firm timeline, but its targets are an incremental extension of 5G's, not a step-change in what an end user experiences.** The ITU approved the "IMT-2030" framework in 2023 [FACT]; 3GPP's first 6G specifications (Release 21) are due to complete by end-2028 [FACT], with first commercial networks in late 2029 to 2030 [FACT]. The headline targets (peak rate 50-200 Gbps depending on scenario, user-experienced rate 300 Mbps to 1 Gbps, latency 0.1 ms) are real but are the *same dimensions* 5G already pushed, and the dimensions the demand evidence shows users do not pay for past a low-hundreds-of-Mbps threshold.

2. **The demand-side answer is the same as the broadband curve, now confirmed for cellular generations directly: users do not pay a premium for "more G."** The cleanest cellular analog: McKinsey found **two-thirds of customers are unwilling to pay more than 5 euros/month for ten-times-higher speed** [FACT]. PwC found only **about one-third** of consumers would pay extra for 5G, at an average of **$4.40/month (mobile) to $5.06/month (home)** [FACT], and **fewer than half could even define the technology** [FACT, single-source]. Deloitte found **54% of consumers could not tell the difference between 4G and 5G** [FACT, single-source]. And the revealed outcome confirms the stated one: **5G delivered no ARPU premium**, with mobile ARPU forecast to *decline* about 1.3-2%/year through 2028 despite the 5G build [FACT].

3. **There are no 6G-specific consumer WTP surveys yet, and that absence is itself a finding.** Consumer 6G surveys "are not yet widely available" because there is no consumer-recognizable use case to ask about (multiple sources). The use cases the vendors put forward (immersive XR, holographic communication, digital twins, integrated sensing) are enterprise- and experience-led, not a consumer-pull "killer app." The 5G evidence is the best available proxy, and it is the relevant one because the *axes* are the same.

4. **The likely shape: 6G is a forced cost, not a demand pull.** Operators are openly skeptical: Orange asks "do our customers really need another G?" [FACT, single-source], and trade press describes governments and vendors "driving the 6G bandwagon at speed, while those footing the bill just want to get off" (Light Reading). An independent capex analyst frames it as unavoidable physics regardless of the label: "More cars, more lanes. You cannot avoid building it." The combination, a build operators must do for capacity and competitive parity, against a user base that will not pay extra for it, is exactly the margin squeeze the founder's thesis predicts, and it widens the cost-down window for any cheaper delivery method (space included) that competes on reach and reliability rather than peak speed.

**The $10/month test (the founder's specific framing), answered:** A typical user would almost certainly *not* pay an extra $10/month for 6G. The revealed ceiling for the previous generation was about **$4.40-5.06/month** (PwC), and even that aspirational figure did not show up in ARPU. McKinsey's threshold was tighter still: **two-thirds balk above 5 euros/month even for a 10x speed jump** [FACT]. A $10 6G premium is roughly **twice** the level users would not reliably pay for 5G, against a generation whose user-visible improvement is smaller than 4G-to-5G was. The honest read is that the marginal-value-per-generation curve has flattened to near zero for the typical consumer, exactly as the broadband-per-Mbps curve did past 100 Mbps. [DERIVED, from the PwC/McKinsey WTP evidence below.]

---

## 1. What 6G Actually Is

### 1.1 Performance targets (ITU IMT-2030)

The ITU Radiocommunication Assembly (RA-23, Dubai) confirmed "IMT-2030" as the name for 6G and approved the Framework for IMT-2030 in 2023 [FACT] ([6G-AI / ITU](https://6g-ai.com/news/itu-imt-2030-vision-requirements-6g), [ITU-R IMT-2030 page](https://www.itu.int/en/ITU-R/study-groups/rsg5/rwp5d/imt-2030/pages/default.aspx)). The draft capability targets, against 5G (IMT-2020), are below. Note the **wide ranges and the draft status**: the two best sources disagree on several figures, which is expected this early and is captured honestly as a range.

| Capability | 5G (IMT-2020) | 6G (IMT-2030) target | Tag |
|---|---|---|---|
| Peak data rate | 20 Gbps | **50, 100, or 200 Gbps** (scenario-dependent; "1 Tbps" common in literature, not an ITU minimum) | [FACT] |
| User-experienced data rate | 100 Mbps | **300-500 Mbps** (ITU-R) to **1 Gbps** (some summaries) | [FACT, range] |
| Latency (air interface) | 1 ms | **0.1-1 ms** (sub-0.1 ms targeted for specialized HRLLC) | [FACT] |
| Spectral efficiency | baseline | **1.5-3x** higher | [FACT] |
| Connection density | 10^6 /km^2 | **10^7 /km^2** | [FACT] |
| Area traffic capacity | 10 Mbps/m^2 | **30-100+ Mbps/m^2** | [FACT] |
| Energy efficiency | baseline | **up to 100x** improvement | [FACT, single-source] |

Sources: [6G-AI / ITU summary](https://6g-ai.com/news/itu-imt-2030-vision-requirements-6g); [ResearchGate, Demystifying IMT-2030](https://www.researchgate.net/publication/379372873_Demystifying_IMT-2030_aka_6G-_Capabilities_Usage_Scenarios_and_Candidate_Technologies) (the 50/100/200 Gbps scenario split and 300/500 Mbps user-experienced figures); [IEEE ComSoc, ITU-R IMT-2030 backgrounder](https://techblog.comsoc.org/2024/07/06/itu-r-imt-2030-6g-backgrounder-and-envisioned-capabilities/).

**The demand-relevant read:** every one of these is a *bigger number on an axis 5G already pushed*. The user-experienced rate target (300 Mbps to 1 Gbps) sits *above* the 200-500 Mbps tier where the broadband WTP evidence shows the typical household already refuses to pay more (baseline synthesis Section 4.1). 6G's genuinely new dimensions (integrated sensing, AI-native air interface, sub-THz) are infrastructure and enterprise capabilities, not things a consumer perceives or buys directly (Section 1.4).

### 1.2 Candidate bands

6G spectrum is being studied in three tiers; the prize, as always, is the band that balances coverage and capacity.

| Tier | Bands under study | Role | Tag |
|---|---|---|---|
| **Upper mid-band (FR3)** | **7.125-8.4, 12.7-13.25, 14.8-15.35 GHz** (within the broader 7-24 GHz "FR3") | The front-runner: balances coverage and capacity; the "workhorse" 6G layer | [FACT] |
| **cmWave / existing FR1, FR2** | reuse and refarm of current 5G bands | Coverage and continuity; MRSS spectrum sharing with 5G | [FACT] |
| **Sub-THz / THz** | **92-300 GHz** region | Extreme peak rate in tiny hotspots; backhaul; sensing | [FACT] |

Sources: [arXiv, 6G in 7-24 GHz band](https://arxiv.org/html/2310.06425v2); [Murata, FR3 for 6G](https://article.murata.com/en-us/article/band-fr3-for-6g); [TRS-RenTelco, 6G Spectrum Landscape white paper](https://www.trsrentelco.com/sites/default/files/content/resource/pdf/2024-04/Exploring%20the%206G%20Spectrum%20Landscape.pdf); [Nature npj Wireless Technology, spectrum opportunities](https://www.nature.com/articles/s44459-025-00008-9).

**The regulatory milestone is WRC-27.** WRC-23 identified the FR3 bands above as 6G study items, and the actual IMT identification (including any sub-THz allocation under Resolution 255) is deferred to **WRC-27 in 2027** [FACT] ([arXiv 7-24 GHz](https://arxiv.org/html/2310.06425v2), [Nature/npj](https://www.nature.com/articles/s44459-025-00008-9)). This is the same dynamic the spectrum docs in this corpus already establish: the mid-band that a terrestrial operator most wants is the most contested, and acquiring it is a national-auction cost layered on top of equipment capex. 6G does not change that structure; it reopens it.

### 1.3 Standards and commercial timeline

The timeline is firm and consistent across the standards body and the major vendor.

| Milestone | Date | Tag |
|---|---|---|
| ITU IMT-2030 framework approved (RA-23) | **2023** | [FACT] |
| 3GPP 6G study work begins (in Release 19) | **2024** | [FACT] |
| 3GPP technical study phase (about 21 months) | **Q3 2025 onward** | [FACT] |
| First 6G specifications (Release 21) complete | **end-2028** | [FACT] |
| 3GPP self-evaluation submitted to ITU | **end-2028 / early-2029** | [FACT] |
| First commercial 6G networks/devices | **late 2029 to 2030** | [FACT] |
| ITU final IMT-2030 designation | **~2030** | [FACT] |

Sources: [Ericsson, 6G standardization timeline](https://www.ericsson.com/en/blog/2024/3/6g-standardization-timeline-and-technology-principles); [6G-AI, 3GPP Release 21 roadmap](https://6g-ai.com/news/3gpp-6g-standardization-roadmap-release-21); [Cloud News, standard 2028 / first uses 2030](https://cloudnews.tech/6g-already-has-a-timeline-standard-in-2028-and-first-uses-in-2030/); [IEEE ComSoc, 3GPP and ITU-R roles in IMT-2030](https://techblog.comsoc.org/2026/01/02/roles-of-3gpp-and-itu-r-wp-5d-in-the-imt-2030-6g-standards-process/).

**For the model:** the ground "next upgrade cycle" the founder wants to compare against is concrete and dated. Operators face a 6G capex wave landing **roughly 2029-2032**, which is squarely inside the ten-year forward window this research is built for.

### 1.4 The use cases are enterprise/immersive, not a consumer killer app

What is 6G *for*? The vendor roadmaps (Nokia, Ericsson) center on **immersive XR, holographic and multisensory communication, digital twins, and integrated sensing and communication (ISAC)** ([Nokia, transforming the 6G vision](https://www.nokia.com/asset/f/214027/), [Nokia, immersive experience](https://www.nokia.com/blog/6g-your-passport-to-the-immersive-experience-revolution/), [The Voltpost, 6G use cases 2026](https://thevoltpost.com/6g-networks-use-cases-flagship-products-in-2026/)). These are experience- and enterprise-led. None is a mass-market consumer service with demonstrated willingness to pay, and the industry knows it: consumer 6G WTP surveys "are not yet widely available" precisely because there is no consumer-recognizable product to survey ([from the 5G/6G WTP literature](https://www.pwc.com/us/en/services/consulting/library/consumer-intelligence-series/promise-5g.html)). This is the same pattern 5G ran into, where the one genuine consumer "killer app" that emerged (fixed wireless access) was a *coverage/substitution* play, not a *speed-premium* play ([Fierce Network, FWA as 5G killer app](https://www.fierce-network.com/wireless/op-ed-fixed-wireless-access-emerges-killer-app-5g)), which is exactly the reach-not-bandwidth axis the baseline synthesis identifies.

---

## 2. The Demand Side: Will Users Pay a Premium?

This is the analytically load-bearing section, and it builds directly on baseline-synthesis Section 4.1. The broadband evidence there established a concave WTP curve for *speed*. The cellular-generation evidence below shows the **same curve for "the next G"**, from three independent angles: stated WTP, perception, and revealed ARPU.

### 2.1 Stated willingness-to-pay for the last generation (the best 6G proxy)

There is no direct 6G consumer survey. The 5G WTP evidence is the proxy, and it is the *relevant* proxy because 6G sells on the same axes (speed, latency) that users already declined to pay for in 5G.

| Evidence | Value | What it shows | Tag |
|---|---|---|---|
| Customers unwilling to pay >5 euros/month for **10x speed** | **two-thirds (~67%)** | The marginal value of a 10x speed jump is below 5 euros/month for most | [FACT] |
| Consumers willing to pay extra for 5G at all | **~one-third (33% home, 31% mobile)** | Two-thirds would not pay any premium | [FACT] |
| Average extra they would pay, 5G home | **$5.06/month** | The aspirational ceiling, even among the willing third | [FACT] |
| Average extra they would pay, 5G mobile | **$4.40/month** | Same, for mobile | [FACT] |
| Respondents who could **define** 5G | **fewer than half** | The premium is for something most cannot name | [FACT, single-source] |
| Would buy a 5G phone before an upgrade was due | **26%** | Even the device pull was weak | [FACT, single-source] |

Sources: McKinsey, two-thirds unwilling above 5 euros for 10x speed ([McKinsey, unlocking the value of 5G in B2C](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/unlocking-the-value-of-5g-in-the-b2c-marketplace), corroborated via [I'M A BRIDGE summary of the McKinsey piece](https://huguesrey.wordpress.com/2022/03/03/unlocking-the-value-of-5g-in-the-b2c-marketplace-source-mckinsey/)); PwC Consumer Intelligence Series, the one-third / $4.40 / $5.06 / "fewer than half could define" / 26% figures ([PwC, the promise of 5G](https://www.pwc.com/us/en/services/consulting/library/consumer-intelligence-series/promise-5g.html), corroborated by [TechTarget, PwC 5G survey finds consumers not ready to pay](https://www.techtarget.com/searchnetworking/news/252451743/PwC-5G-survey-finds-consumers-not-ready-to-pay)).

> **Note on the optimistic surveys.** Some headlines claim "70% would pay more for 5G" ([TechRepublic](https://www.techrepublic.com/article/70-of-consumers-willing-to-pay-more-for-5g/)) and Ericsson cites a "20% premium" from early adopters ([Ericsson, harnessing the 5G consumer potential](https://www.ericsson.com/en/reports-and-papers/consumerlab/reports/harnessing-the-5g-consumer-potential)). These are real but must be read with care: the "70%" is the *same* PwC dataset where the willing share *drops to ~33%* once a concrete bill increase is named, and Ericsson notes the pandemic *halved* the share still willing to pay the 20% premium. The revealed-ARPU evidence (Section 2.3) is the tiebreaker: the premium did not materialize. Stated WTP for a new G is systematically higher than realized WTP.

### 2.2 Perception: most users cannot tell the generations apart

A premium requires a perceived difference. For cellular generations past 4G, the perceived difference is small to absent.

| Evidence | Value | Tag |
|---|---|---|
| Consumers who could **not tell the difference** between 4G and 5G | **54%** | [FACT, single-source] |
| Consumers who say they do not know enough about 5G / its benefits | **~56%** | [FACT, single-source] |
| Where 5G ranked on a consumer priority list | **#10** (i.e., not a priority) | [FACT, single-source] |
| Satisfaction gap, 5G vs 4G users (very-high satisfaction) | **~38% vs ~28%** (a 10-point gap; some markets larger, some near-zero) | [FACT] |

Sources: Deloitte Digital Consumer Trends 2021, the 54% / 56% / priority-rank figures ([Deloitte Ireland, 5G benefits and barriers](https://www.deloitte.com/ie/en/Industries/tmt/research/digital-consumer-trends/5g-benefits-and-barriers-to-adoption.html), corroborated by [Advanced Television, "50% don't know the difference"](https://advanced-television.com/2021/10/19/survey-50-dont-know-difference-between-4g-and-5g/)); the satisfaction gap from [Ericsson ConsumerLab](https://www.ericsson.com/en/reports-and-papers/consumerlab/reports/harnessing-the-5g-consumer-potential) (note Ericsson, a network vendor, is the more optimistic source and still lands at a 10-point gap).

**The read:** if a majority cannot perceive the 4G-to-5G jump, the 5G-to-6G jump (a smaller user-visible delta on the same axes) is even less likely to support a premium. The satisfaction gap that does exist shows up mostly in *high-demand contexts* (crowded events), i.e., reliability-under-load, which is the reach/reliability axis again, not raw peak speed.

### 2.3 Revealed outcome: 5G delivered no ARPU premium, and ARPU is falling

Stated WTP can mislead; the revealed outcome is decisive. Despite a roughly **$1.5 trillion** global 5G capex cycle (cellular-economics doc, COMM-025), the price users actually pay did not rise.

| Evidence | Value | Tag |
|---|---|---|
| Global mobile ARPU trajectory | declining **~1.3%/year (CAGR) through 2028** | [FACT] |
| Blended telecom ARPU (mobile + fixed + voice) | declining **~2%/year through 2028** | [FACT] |
| US mobile ARPU since 5G launch | **roughly flat** | [FACT] |
| 5G's effect on ARPU | "largely **not** delivered an ARPU premium"; bundles give only "the illusion of a 5G ARPU uplift" | [FACT] |

Sources: [Telecoms.com, revenue per user falling despite 5G and fibre](https://www.telecoms.com/5g-6g/telecoms-revenue-per-user-is-falling-despite-5g-and-fibre-rollouts); [PwC Global Telecoms Outlook, ARPU -2%/yr to 2028](https://www.pwc.com/gx/en/news-room/press-releases/2025/pwc-global-telecoms-outlook.html); [Statista, 5G launch impact on ARPU by country](https://www.statista.com/statistics/1423051/5g-launch-mobile-arpu-change-selected-countries/). This matches the cellular-economics doc's own finding (COMM, that doc's Section 5: "5G has largely not delivered an ARPU premium," global ARPU forecast to decline ~2%/yr).

**The synthesis across 2.1-2.3:** stated WTP for a new G is modest (a third of users, ~$5/month) and *realized* WTP is near zero (ARPU fell). The gap between the two is the systematic over-optimism of "would you pay" surveys. For 6G, the prior is that the realized premium will again be near zero.

### 2.4 The escape operators are attempting, and why it does not change the answer for raw speed

Operators and their advisors know speed alone will not sell. The proposed escape is **differentiated connectivity**: selling guaranteed quality, low-latency slices, and bundled experiences rather than "more Mbps." McKinsey estimates differentiated connectivity could lift 5G ARPU by **5-12%**, versus only **3-6%** from "simply upselling speed" ([McKinsey, B2C 5G](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/unlocking-the-value-of-5g-in-the-b2c-marketplace); [Ericsson, elevating 5G with differentiated connectivity](https://www.ericsson.com/en/reports-and-papers/consumerlab/reports/elevating-5g-with-differentiated-connectivity)). Event-goers will pay up to ~15% more for *guaranteed seamless* connectivity in a crowd ([Ericsson ConsumerLab](https://www.ericsson.com/en/reports-and-papers/consumerlab/reports/harnessing-the-5g-consumer-potential)).

This *reinforces* the baseline-synthesis thesis rather than contradicting it: even the operators' own monetization path concedes that **raw bandwidth is not the product; reliability and guaranteed experience are.** That is the reach-and-reliability axis the baseline synthesis says coverage-oriented supply (FWA, satellite) wins on. 6G does not create consumer pull for peak speed; the industry's best hope is to monetize *reliability*, which is precisely where a cheaper alternative delivery method competes.

---

## 3. The Likely Shape: A Forced Cost, Not a Demand Pull

The founder's framing is the right one, and the 6G-specific evidence supports it directly. 6G is shaping up as a **supply-push** technology (driven by vendors, standards bodies, and governments, plus the unavoidable physics of traffic growth) rather than a **demand-pull** one (users clamoring and paying). The result is a cost operators must bear without a matching revenue line, which compresses ground margins on the next upgrade cycle.

### 3.1 Operators are reluctant, and say so

| Signal | Source | Tag |
|---|---|---|
| "Do our customers really need another G?" (Orange, Strategy/Architecture/Standards Director) | [The Mobile Network, 6G reality check](https://the-mobile-network.com/2026/04/6g-reality-check-and-update/) | [FACT, single-source quote] |
| Governments and vendors "driving the 6G bandwagon at speed, while those footing the bill just want to get off" | [Light Reading, the specter of a capex drought looms over 6G](https://www.lightreading.com/6g/the-specter-of-a-capex-drought-looms-over-6g) | [FACT, single-source quote] |
| Operators "have just about maxed out their core connectivity business and have no visibility on a return to margin growth" | [Light Reading](https://www.lightreading.com/6g/the-specter-of-a-capex-drought-looms-over-6g) | [FACT, single-source] |
| The telecom "value capture" problem: networks improved but revenue stayed tied to legacy billing; no new high-margin services consumers recognize | [SiliconANGLE, can AI solve the telco monetization paradox](https://siliconangle.com/2026/03/13/6g-horizon-can-ai-finally-solve-telco-monetization-paradox/) | [FACT, single-source] |
| Operators must find "clear additional and monetizable use cases that will justify the investment" *before* committing | [The Mobile Network](https://the-mobile-network.com/2026/04/6g-reality-check-and-update/) | [FACT, single-source] |

The two strongest quotes ("do our customers really need another G?" and "those footing the bill just want to get off") come from different outlets (The Mobile Network/Orange and Light Reading respectively), so the *reluctance* finding is two-source even though each individual quote is single-source.

### 3.2 But the build happens anyway: the cost is forced by physics, not by demand

The reason this is a *forced* cost, not an avoidable one, is that traffic growth and competitive parity compel the spend regardless of whether a premium exists. An independent capex analyst puts it plainly: **"Even if you erased the label '6G,' operators would still need to add spectrum where available, extend fiber backhaul, and multiply sites in hot zones... More cars, more lanes. You cannot avoid building it"** ([Sebastian Barros, 6G capex forecast](https://sebastianbarros.substack.com/p/6g-capex-a-data-driven-forecast-without)). The same analyst notes 5G network capex ran about **$1.38 trillion (2023-2030)** and models 6G's decade of global capex as a comparable "below one trillion to over a trillion" figure [ESTIMATE, single-source, partly paywalled]; this is directionally consistent with the cellular-economics doc's GSMA figure of **~$1.5 trillion global mobile capex 2023-2030** (COMM-025).

This is the precise structure the founder's thesis identifies:

- **Demand plateaus** (Section 2): users will not pay extra; ARPU falls.
- **Capacity costs are forced** (Section 3.2): operators must keep building for traffic and parity, at low-teens-percent-of-revenue capex intensity that the cellular-economics doc shows is already a long-payback drag.
- **Therefore margins compress** on the next ground cycle, and the compression is structural, not cyclical.

### 3.3 Why this is a window for a cheaper alternative

The squeeze matters for the model because it changes the *forward comparison* the founder wants to make. The relevant benchmark is not what ground has *already paid for*, but what it must spend on its **next** upgrade. 6G is that next upgrade, and it is one operators bear without a revenue offset. Three consequences for a space entrant:

1. **The cost-down hurdle is measured against a rising-cost, falling-revenue incumbent.** Ground's per-subscriber economics on the next cycle get *worse* (forced 6G capex, declining ARPU), not better. A space delivery method that competes on the reach-and-reliability axis is racing a target whose own unit economics are deteriorating.
2. **6G does not unlock a consumer premium that a space entrant would have to match.** If 6G *had* created a $10/month consumer premium for peak speed, space would face a higher bar. It has not, and the evidence says it will not, so the bar stays where the baseline synthesis put it: reach, reliability, sovereignty, latency-for-specific-uses, not raw bandwidth.
3. **The one axis 6G monetization is chasing (guaranteed reliability/experience) is the axis the corpus already says coverage-oriented supply wins.** This is corroboration, not a new claim: the baseline synthesis Section 4.1 and the broadband WTP curve both point to reliability and reach as the value drivers, and Section 2.4 here shows operators conceding the same.

**Stated as a hypothesis, not a verdict (consistent with the corpus):** whether a *space* communications business actually captures this window depends on its own cost stack (handled in other docs), but the *demand environment* it would enter is favorable in exactly the way the founder framed: 6G is a cost ground must bear that users will not fund, which compresses the incumbent and shifts competition onto the axes a cheaper alternative can contest.

---

## 4. China (excluded): noted aside

China is excluded from every market and WTP figure above. For scale and contrast only: China leads the world on 5G Standalone reach (about 80% of population per GSMA) and China Mobile alone targeted about **2.35M 5G base stations** by end-2024 (cellular-economics doc, COMM-035), and China is moving aggressively on 6G standards under a state-directed model. Its per-site economics, ARPU dynamics, and policy-driven deployment are non-comparable to the Western operator model this doc uses (Chinese ARPU also *fell* post-5G, per Section 2.3 sources), so it is noted once here and added to no figure. The Western demand-side conclusion (no consumer premium for a new G) is the load-bearing one for this project.

---

## 5. Open Questions

1. **A direct 6G consumer WTP survey, if one appears.** None exists yet (Section 1.4). The first credible one (likely 2027-2028 as devices near) would replace the 5G proxy used here. The prior, from three independent angles, is that realized premium will be near zero.
2. **The size of the differentiated-connectivity escape.** McKinsey's 5-12% ARPU uplift from quality-of-service slicing (Section 2.4) is the operators' best monetization hope. If it works at scale in the 6G era, it modestly lifts the incumbent benchmark; if it stalls (as the raw-speed premium did), the squeeze deepens. Worth tracking as a swing factor.
3. **6G capex intensity vs the 5G cycle.** Whether 6G capex intensity exceeds, matches, or undershoots 5G's ~14-19%-of-revenue peak (cellular-economics doc) determines how hard the forced-cost squeeze bites. The early analyst read (Section 3.2) is "comparable order of magnitude," but the figures are soft and partly paywalled; a GSMA or Dell'Oro 6G capex series would harden this.
4. **The sub-THz reality timeline.** The genuinely new 6G capability (sub-THz, sensing) is the part with the *least* proven demand and the *most* uncertain cost. If it slips well past 2030 (as mmWave largely underdelivered in 5G), 6G's user-facing reality is mostly an FR3 mid-band refarm, reinforcing the "incremental, not step-change" read.
5. **Enterprise/B2B 6G value (out of scope here).** This doc is consumer-demand-focused. The enterprise use cases (digital twins, ISAC, private networks) may carry real WTP that the consumer market does not, but that is a different buyer and a different model lane; flagged, not sized.

---

## Sources

*6G technical reality, targets, bands, timeline*
- [ITU-R, IMT-2030 (6G) study page](https://www.itu.int/en/ITU-R/study-groups/rsg5/rwp5d/imt-2030/pages/default.aspx)
- [6G-AI, ITU IMT-2030 vision and requirements](https://6g-ai.com/news/itu-imt-2030-vision-requirements-6g)
- [ResearchGate, Demystifying IMT-2030 (capabilities, usage scenarios, candidate technologies)](https://www.researchgate.net/publication/379372873_Demystifying_IMT-2030_aka_6G-_Capabilities_Usage_Scenarios_and_Candidate_Technologies)
- [IEEE ComSoc, ITU-R IMT-2030 backgrounder](https://techblog.comsoc.org/2024/07/06/itu-r-imt-2030-6g-backgrounder-and-envisioned-capabilities/)
- [IEEE ComSoc, 3GPP and ITU-R WP5D roles in the IMT-2030 process](https://techblog.comsoc.org/2026/01/02/roles-of-3gpp-and-itu-r-wp-5d-in-the-imt-2030-6g-standards-process/)
- [Ericsson, 6G standardization timeline and technology principles](https://www.ericsson.com/en/blog/2024/3/6g-standardization-timeline-and-technology-principles)
- [6G-AI, 3GPP 6G standardization roadmap (Release 21)](https://6g-ai.com/news/3gpp-6g-standardization-roadmap-release-21)
- [Cloud News, 6G standard in 2028, first uses 2030](https://cloudnews.tech/6g-already-has-a-timeline-standard-in-2028-and-first-uses-in-2030/)
- [arXiv, 6G Wireless in the 7-24 GHz band](https://arxiv.org/html/2310.06425v2)
- [Murata, FR3 frequency band for 6G](https://article.murata.com/en-us/article/band-fr3-for-6g)
- [TRS-RenTelco, Exploring the 6G Spectrum Landscape (white paper)](https://www.trsrentelco.com/sites/default/files/content/resource/pdf/2024-04/Exploring%20the%206G%20Spectrum%20Landscape.pdf)
- [Nature, npj Wireless Technology, spectrum opportunities (D2D satellite to 6G)](https://www.nature.com/articles/s44459-025-00008-9)

*6G use cases (enterprise/immersive)*
- [Nokia, transforming the 6G vision to action](https://www.nokia.com/asset/f/214027/)
- [Nokia, 6G and the immersive experience revolution](https://www.nokia.com/blog/6g-your-passport-to-the-immersive-experience-revolution/)
- [The Voltpost, 6G networks and use cases 2026](https://thevoltpost.com/6g-networks-use-cases-flagship-products-in-2026/)
- [Fierce Network, FWA as the 5G killer app](https://www.fierce-network.com/wireless/op-ed-fixed-wireless-access-emerges-killer-app-5g)

*Demand-side / willingness-to-pay (5G as 6G proxy)*
- [McKinsey, unlocking the value of 5G in the B2C marketplace](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/unlocking-the-value-of-5g-in-the-b2c-marketplace)
- [Summary of the McKinsey B2C 5G piece (two-thirds / 5 euros / 10x)](https://huguesrey.wordpress.com/2022/03/03/unlocking-the-value-of-5g-in-the-b2c-marketplace-source-mckinsey/)
- [PwC, Consumer Intelligence Series: the promise of 5G](https://www.pwc.com/us/en/services/consulting/library/consumer-intelligence-series/promise-5g.html)
- [TechTarget, PwC 5G survey finds consumers not ready to pay](https://www.techtarget.com/searchnetworking/news/252451743/PwC-5G-survey-finds-consumers-not-ready-to-pay)
- [Deloitte Ireland, 5G benefits and barriers to adoption (Digital Consumer Trends 2021)](https://www.deloitte.com/ie/en/Industries/tmt/research/digital-consumer-trends/5g-benefits-and-barriers-to-adoption.html)
- [Advanced Television, survey: 50% do not know the difference between 4G and 5G](https://advanced-television.com/2021/10/19/survey-50-dont-know-difference-between-4g-and-5g/)
- [Ericsson ConsumerLab, harnessing the 5G consumer potential](https://www.ericsson.com/en/reports-and-papers/consumerlab/reports/harnessing-the-5g-consumer-potential)
- [Ericsson, elevating 5G with differentiated connectivity](https://www.ericsson.com/en/reports-and-papers/consumerlab/reports/elevating-5g-with-differentiated-connectivity)
- [TechRepublic, 70% of consumers willing to pay more for 5G (the optimistic framing, flagged)](https://www.techrepublic.com/article/70-of-consumers-willing-to-pay-more-for-5g/)

*Revealed ARPU outcome*
- [Telecoms.com, revenue per user falling despite 5G and fibre](https://www.telecoms.com/5g-6g/telecoms-revenue-per-user-is-falling-despite-5g-and-fibre-rollouts)
- [PwC, Global Telecoms Outlook (ARPU -2%/yr to 2028)](https://www.pwc.com/gx/en/news-room/press-releases/2025/pwc-global-telecoms-outlook.html)
- [Statista, 5G launch impact on ARPU by country](https://www.statista.com/statistics/1423051/5g-launch-mobile-arpu-change-selected-countries/)

*Forced-cost / operator reluctance*
- [Light Reading, the specter of a capex drought looms over 6G](https://www.lightreading.com/6g/the-specter-of-a-capex-drought-looms-over-6g)
- [The Mobile Network, 6G reality check and update](https://the-mobile-network.com/2026/04/6g-reality-check-and-update/)
- [SiliconANGLE, can AI solve the telco monetization paradox](https://siliconangle.com/2026/03/13/6g-horizon-can-ai-finally-solve-telco-monetization-paradox/)
- [Sebastian Barros, 6G capex: a data-driven forecast without the hype](https://sebastianbarros.substack.com/p/6g-capex-a-data-driven-forecast-without)

*Grounded-in (existing corpus, not re-derived)*
- [comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md) (Section 4.1, diminishing-returns curve)
- [comms_cellular_5g_deployment_economics.md](comms_cellular_5g_deployment_economics.md) (capex intensity, no-ARPU-premium, payback)

---

## Confidence

- **Demand-side conclusion (Section 2): high.** It is the same diminishing-returns curve the baseline synthesis already rates as the most robust finding in the base, now corroborated for cellular generations specifically by three independent lenses (stated WTP: McKinsey + PwC; perception: Deloitte + Ericsson; revealed ARPU: Telecoms.com + PwC Outlook + Statista). The "would not pay $10/month" answer is a [DERIVED] inference, but it is a conservative one (the proxy ceiling is ~$5 and realized premium was ~0).
- **6G technical reality (Section 1): medium-high.** The standards timeline is firm and two-source (Ericsson + 3GPP-roadmap outlets). The performance *targets* are draft and span wide ranges (the two best sources disagree on peak rate and user-experienced rate), captured honestly as ranges. The candidate bands are well-sourced; the WRC-27 milestone is the firm regulatory anchor.
- **Forced-cost framing (Section 3): medium-high as a hypothesis.** The operator-reluctance quotes are vivid and come from multiple outlets (so reluctance is two-source), but several individual quotes are single-source and are flagged as such. The capex magnitude is soft (partly paywalled analyst model) but is cross-checked against the GSMA ~$1.5T figure already in the corpus. Stated as a well-supported working hypothesis consistent with the founder's thesis, not a settled verdict.
- **Single-source items flagged in-line:** the Deloitte 54%/56%/priority-rank figures, the "fewer than half could define 5G" and 26% device-pull figures (PwC), the energy-efficiency 100x target, the specific operator quotes, and the 6G capex magnitude. Each is marked [FACT, single-source] or [ESTIMATE] at point of use.

---

## Claims ledger

For the catalog step to ingest (no COMM- IDs assigned here, per the lead's instruction). Each hard claim with its 2+ independent sources; single-source claims are marked.

1. **ITU approved the IMT-2030 (6G) framework in 2023.** Sources: [ITU-R IMT-2030 page](https://www.itu.int/en/ITU-R/study-groups/rsg5/rwp5d/imt-2030/pages/default.aspx); [6G-AI / ITU](https://6g-ai.com/news/itu-imt-2030-vision-requirements-6g). [FACT]
2. **6G peak data rate target: 50/100/200 Gbps (scenario-dependent); user-experienced rate 300 Mbps-1 Gbps; latency 0.1-1 ms; spectral efficiency 1.5-3x over 5G.** Sources: [ResearchGate, Demystifying IMT-2030](https://www.researchgate.net/publication/379372873_Demystifying_IMT-2030_aka_6G-_Capabilities_Usage_Scenarios_and_Candidate_Technologies); [6G-AI / ITU](https://6g-ai.com/news/itu-imt-2030-vision-requirements-6g); [IEEE ComSoc backgrounder](https://techblog.comsoc.org/2024/07/06/itu-r-imt-2030-6g-backgrounder-and-envisioned-capabilities/). [FACT, range]
3. **6G energy-efficiency target: up to 100x improvement over 5G baseline.** Source: [6G-AI / ITU](https://6g-ai.com/news/itu-imt-2030-vision-requirements-6g). [FACT, single-source]
4. **6G candidate upper-mid-band (FR3) study bands: 7.125-8.4, 12.7-13.25, 14.8-15.35 GHz; sub-THz 92-300 GHz; IMT identification deferred to WRC-27 (2027).** Sources: [arXiv 7-24 GHz](https://arxiv.org/html/2310.06425v2); [Murata FR3](https://article.murata.com/en-us/article/band-fr3-for-6g); [Nature/npj](https://www.nature.com/articles/s44459-025-00008-9). [FACT]
5. **3GPP first 6G specs (Release 21) complete end-2028; first commercial 6G late-2029 to 2030.** Sources: [Ericsson](https://www.ericsson.com/en/blog/2024/3/6g-standardization-timeline-and-technology-principles); [6G-AI Release 21 roadmap](https://6g-ai.com/news/3gpp-6g-standardization-roadmap-release-21); [Cloud News](https://cloudnews.tech/6g-already-has-a-timeline-standard-in-2028-and-first-uses-in-2030/). [FACT]
6. **6G lead use cases are enterprise/immersive (XR, holographic, digital twins, ISAC), not a mass consumer killer app; no consumer 6G WTP surveys exist yet.** Sources: [Nokia vision](https://www.nokia.com/asset/f/214027/); [The Voltpost](https://thevoltpost.com/6g-networks-use-cases-flagship-products-in-2026/); [PwC (notes absence of 6G consumer data)](https://www.pwc.com/us/en/services/consulting/library/consumer-intelligence-series/promise-5g.html). [FACT]
7. **Two-thirds of customers are unwilling to pay more than 5 euros/month for 10x-higher speed (McKinsey).** Sources: [McKinsey B2C 5G](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/unlocking-the-value-of-5g-in-the-b2c-marketplace); [I'M A BRIDGE summary of the McKinsey piece](https://huguesrey.wordpress.com/2022/03/03/unlocking-the-value-of-5g-in-the-b2c-marketplace-source-mckinsey/). [FACT]
8. **Only about one-third of consumers would pay extra for 5G (33% home / 31% mobile), averaging $5.06/month home and $4.40/month mobile (PwC).** Sources: [PwC](https://www.pwc.com/us/en/services/consulting/library/consumer-intelligence-series/promise-5g.html); [TechTarget on PwC](https://www.techtarget.com/searchnetworking/news/252451743/PwC-5G-survey-finds-consumers-not-ready-to-pay). [FACT]
9. **Fewer than half of PwC respondents could define 5G; only 26% would buy a 5G phone before an upgrade was due.** Sources: [PwC](https://www.pwc.com/us/en/services/consulting/library/consumer-intelligence-series/promise-5g.html); [TechTarget on PwC](https://www.techtarget.com/searchnetworking/news/252451743/PwC-5G-survey-finds-consumers-not-ready-to-pay). [FACT, single dataset reported via two outlets]
10. **54% of consumers could not tell the difference between 4G and 5G; ~56% said they did not know enough about 5G; 5G ranked #10 on a consumer priority list (Deloitte 2021).** Sources: [Deloitte Ireland](https://www.deloitte.com/ie/en/Industries/tmt/research/digital-consumer-trends/5g-benefits-and-barriers-to-adoption.html); [Advanced Television](https://advanced-television.com/2021/10/19/survey-50-dont-know-difference-between-4g-and-5g/). [FACT, single dataset reported via two outlets]
11. **5G vs 4G "very high satisfaction" gap is about 10 points (~38% vs ~28%), concentrated in high-load contexts.** Source: [Ericsson ConsumerLab](https://www.ericsson.com/en/reports-and-papers/consumerlab/reports/harnessing-the-5g-consumer-potential). [FACT, single-source]
12. **5G delivered no ARPU premium; global mobile ARPU declining ~1.3%/yr and blended telecom ARPU ~2%/yr through 2028; US ARPU roughly flat post-5G.** Sources: [Telecoms.com](https://www.telecoms.com/5g-6g/telecoms-revenue-per-user-is-falling-despite-5g-and-fibre-rollouts); [PwC Global Telecoms Outlook](https://www.pwc.com/gx/en/news-room/press-releases/2025/pwc-global-telecoms-outlook.html); [Statista](https://www.statista.com/statistics/1423051/5g-launch-mobile-arpu-change-selected-countries/). [FACT]
13. **Differentiated-connectivity (quality, not raw speed) could lift 5G ARPU 5-12%, vs 3-6% from upselling speed alone; event-goers pay up to ~15% more for guaranteed connectivity.** Sources: [McKinsey B2C 5G](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/unlocking-the-value-of-5g-in-the-b2c-marketplace); [Ericsson differentiated connectivity](https://www.ericsson.com/en/reports-and-papers/consumerlab/reports/elevating-5g-with-differentiated-connectivity). [FACT]
14. **Operators are openly reluctant on 6G: "do our customers really need another G?" (Orange); those "footing the bill just want to get off" (Light Reading); no line of sight to margin growth.** Sources: [The Mobile Network](https://the-mobile-network.com/2026/04/6g-reality-check-and-update/); [Light Reading](https://www.lightreading.com/6g/the-specter-of-a-capex-drought-looms-over-6g); [SiliconANGLE](https://siliconangle.com/2026/03/13/6g-horizon-can-ai-finally-solve-telco-monetization-paradox/). [FACT, reluctance is multi-source; individual quotes single-source]
15. **6G capex is a forced cost regardless of branding ("more cars, more lanes... you cannot avoid building it"); decade-scale global 6G capex modeled near the 5G cycle's ~$1.38-1.5T order of magnitude.** Sources: [Sebastian Barros analyst model](https://sebastianbarros.substack.com/p/6g-capex-a-data-driven-forecast-without); cross-check [GSMA via cellular-economics doc, ~$1.5T mobile capex 2023-2030](comms_cellular_5g_deployment_economics.md). [ESTIMATE, single-source for the 6G figure; the $1.5T 5G cross-check is FACT]
