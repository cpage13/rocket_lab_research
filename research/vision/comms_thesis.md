# Communications Thesis: Revision 1 (Belief Record Only)

*Research date: June 2026. Communications research-wiki effort (shared library).*

**Builds on / does not duplicate:** the neutral base is in [comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md), which sizes the markets and the current state of the technologies. This thesis records only the founder's working hypotheses and the open questions on top of that base; it does not repeat the market or technology numbers.

> **Status: no judgments have been made yet.** This is **Revision 1**, the starting belief record for the communications track. It captures the founder's initial hypotheses so each one can be tested against evidence in later waves. **There is no verdict here, for or against a Rocket Lab space-communications business.** Nothing below is validated. The base research is deliberately separated from these beliefs precisely so the beliefs can be revised (or discarded) as waves land. Read every line as "the current working hypothesis, to be tested," not as a finding.

> **Why a belief record exists at all.** The wider project keeps a versioned thesis so the mental model is written down and each piece can be pressure-tested against physics and economics (the data-center track's equivalent is [initial_thesis.md](./initial_thesis.md)). This is that artifact for communications, at its first revision. It will gain confidence ratings, supporting/contradicting evidence, and eventually a verdict only as later waves justify them.

---

## How to read this document

- Each hypothesis is stated plainly, then annotated with **what the base currently suggests** (a pointer to the baseline synthesis, not a re-derivation) and **what would confirm or break it**.
- Confidence is deliberately withheld at the thesis level for now. The base sections each carry their own confidence; the *beliefs* built on them are unrated until tested.
- The open questions at the end are the ones that decide whether each hypothesis survives.

---

## The working hypotheses

### Hypothesis 1: Diminishing returns past baseline broadband

**The belief:** once a user has baseline broadband (enough for everyday streaming, calls, gaming), additional speed and capacity command rapidly diminishing willingness-to-pay. Communications is therefore a market where "more bandwidth" is not, by itself, a premium product the way "more compute" is.

**What the base currently suggests:** this is the strongest-supported of all the hypotheses. The baseline synthesis (Section 4.1) records a sharply concave willingness-to-pay curve (about $2.34/Mbps at the low end collapsing to about $0.02/Mbps from 100 to 1,000 Mbps), gigabit available to over 91% of US homes but bought by only about 30%, a modal tier of 200-500 Mbps, and flat-to-declining operator ARPU. The value curve rewards **reach and reliability, not raw bandwidth** past a low-hundreds-of-Mbps threshold.

**What would confirm it:** the same plateau showing up outside the US (Europe, the gap regions), and a clean unserved/underserved WTP curve confirming high WTP only at the *connect-at-all* end.

**What would break it:** a new high-bandwidth use case (immersive/AI-native applications, something not yet mainstream) that re-steepens the WTP curve and makes raw bandwidth premium again. This is the main downside risk to the hypothesis and is called out as an open question below.

### Hypothesis 2: Space as a possible step change, whose value depends on economics and new use cases

**The belief:** space-delivered communications could be a genuine step change, but its value is *not* in beating ground broadband on raw speed or price in served markets. It depends on (a) the economics closing for the places ground cannot reach, and (b) new use cases that value what space uniquely offers (ubiquity, a path independent of terrestrial fiber, sovereignty, security, latency on long links).

**What the base currently suggests:** the base supports the *direction* and cautions on the *scale*. Space holds about 0.5% of global fixed broadband today; the realistically served slice of the cited trillion-dollar TAMs is roughly 5-10% of the headline (Morningstar's ~$129B for a mature Starlink versus SpaceX's $1.6T claim). The economically meaningful version of "space replaces ground" is the rural and unserved fringe (coverage gap ~300M people plus underserved rural), not the whole market. Where fiber or upgraded cable already exists, the incumbent defends a passed home for ~$100-300, so space adds little incremental value in served territory (baseline synthesis Sections 2 and 4).

**What would confirm it:** a dollar-sized rural/remote fringe (and premium/sovereign niche) where the space *supply* economics close, plus evidence of a real new use case (orbital-DC backhaul, sovereign networks, resilience-as-a-service) paying a premium.

**What would break it:** the supply-side space economics not closing even in the fringe (the space cost stack is a separate workstream and is not assumed here), or terrestrial reach (FWA, subsidized fiber) closing the gap faster than expected.

### Hypothesis 3: Laser, high bandwidth but weather-limited and possibly assuming fiber is already present

**The belief:** laser/optical is the high-bandwidth, no-spectrum-fight winner, but it is weather-limited (cloud/fog break the link, not degrade it), and much of its terrestrial value proposition may quietly assume fiber is already present (as a backup path, a redundant overlay, or a gap-filler between fiber points), rather than replacing fiber.

**What the base currently suggests:** strongly consistent. The base records optical proven at scale for inter-satellite links (Starlink) and downlink (TBIRD 200 Gbps), but a single optical ground site reaches only ~50-70% availability, needing 4+ diverse ground stations for 99-99.9%. Terrestrial laser (Taara) hits the same fog wall and uses a hybrid FSO/RF link for five-nines; its strong case is *where fiber does not exist*, and alongside existing fiber it adds only conditional value (security, latency, fast deploy). The "possibly assuming fiber is already present" instinct is borne out: the terrestrial-laser doc frames the product as "dark fiber in the sky" and a redundant path, i.e. it lives next to fiber as much as beyond it (baseline synthesis Section 3.2).

**What would confirm it:** a clean availability/cost model showing the weather-diversity overhead, and a use-case map showing where laser is a *primary* link versus a *complement* to fiber.

**What would break it:** a weather-mitigation advance (or a dry-climate-only deployment model) that lets optical stand alone at carrier-grade availability without an RF or fiber backup. The base treats the portfolio (optical + RF complement) as the settled architecture, so a pure-optical standalone would be the surprise.

### Hypothesis 4: Security as a differentiator

**The belief:** security and sovereignty (a controlled, hard-to-intercept, independent path) are a genuine differentiator for space communications, and may be a stronger basis to compete on than bandwidth or price.

**What the base currently suggests:** supported as a real but bounded differentiator. The base records that narrow optical beams are very hard to intercept covertly (a tap requires being inside the beam path), with no RF side-lobe leakage, which defense and intelligence users list as a primary reason for free-space optical. The existing scoped business case ([comms_business_case.md](../laser_comms/comms_business_case.md)) already centers sovereignty/security demand (GOVSATCOM operational, the EUR 10.6B IRIS2 program, "sharply increased" sovereign demand). The caveat the base preserves: it is physical-layer obscurity plus tamper-evidence, not cryptographic security; sensitive traffic should still be encrypted, and how much a buyer pays for the edge over encrypted fiber is judgment, not yet data (baseline synthesis Section 3.2, 3.4).

**What would confirm it:** a sized premium/sovereign/defense niche (the central missing dollar number) and evidence that buyers actually pay for the security/sovereignty edge at a margin.

**What would break it:** the security edge proving to be a feature buyers expect for free rather than pay a premium for, or the sovereign demand being captured by closed national programs (IRIS2-style) a new commercial entrant cannot win.

---

## The thread that ties the hypotheses together (working framing, not a verdict)

The four hypotheses point, *as a current working framing only*, toward a single tension the later waves must resolve:

> **Communications is a diminishing-returns market on the axis ground broadband competes on (raw bandwidth into served homes). The open question is whether space communications escapes that by competing on the axes the value curve actually rewards (reach, reliability, sovereignty, security, latency on long links) and on new use cases (orbital-DC backhaul, resilient/independent paths) rather than on bandwidth or price.**

This is explicitly the founder's comparison to the data-center track, where the economics run the other way (demand outrunning supply, continual hardware upgrades, capacity expansion rewarded; baseline synthesis Section 4.2). **Whether the comms case is strong, weak, or conditional is not decided here.** It is the question Revision 2+ exists to answer.

---

## Open questions (these decide whether the hypotheses survive)

1. **Does a new high-bandwidth use case re-steepen the broadband WTP curve?** Hypothesis 1 rests on demand plateauing; an AI-native or immersive application that makes raw bandwidth premium again would weaken it. (The single biggest risk to Hypothesis 1.)
2. **What is the dollar size of the satellite-addressable rural/remote fringe, and of the premium/sovereign niche?** These are the two missing numbers that turn Hypotheses 2 and 4 from direction into an addressable market (baseline synthesis Section 5).
3. **Do the space *supply* economics close in the fringe?** This thesis is isolated to communications demand and the market base; the space-side cost stack (constellation capex, optical ground-station network, launch cadence) is a separate workstream and is *not assumed* here. Hypothesis 2 depends on it.
4. **Is laser a primary link or a fiber complement, and at what weather-diversity cost?** Hypothesis 3 needs a clean availability/cost model and a primary-vs-complement use-case map.
5. **Will buyers pay a premium for the security/sovereignty edge, or expect it for free?** Hypothesis 4 needs evidence of paid margin, not just stated demand, and needs the closed-program risk (IRIS2-style capture) assessed.
6. **Where does a space comms business sit relative to direct-to-device versus fixed broadband versus premium/sovereign?** The base shows these are different (and partly overlapping) markets; the thesis has not chosen which one(s) the comms track targets. That choice is a later-wave decision, not a current belief.
7. **What is the realistic competitive timing?** The base notes a space entrant would be behind operational players (Kepler optical relay) and beside Starlink; whether the differentiation is enough to win share is unresolved and bears on every hypothesis.

---

## What this revision deliberately does not do

- It does not pick a product (direct-to-device, enterprise/B2B backhaul, wholesale capacity, premium/sovereign network). The base shows these are distinct markets; choosing is a later-wave decision.
- It does not size the Rocket Lab opportunity in dollars. The reference points exist (EUR 10.6B IRIS2, $1.3B SDA optical-mesh contracts, $14.8B LEO-satcom forecast) but the served premium/sovereign niche is unsized; that is the central open number.
- It does not assume the space supply economics. This thesis covers communications demand and the market/technology base only.
- It does not render a verdict. **No judgments have been made yet.** This is the starting belief record, to be revised in later waves.

---

## Revision history

| Revision | Date | What it records | Verdict? |
|---|---|---|---|
| **Revision 1** | June 2026 | Initial working hypotheses (diminishing returns past baseline broadband; space as a possible step change whose value depends on economics and new use cases; laser high-bandwidth but weather-limited and possibly fiber-dependent; security as a differentiator) and the open questions that test them. Built on [comms_baseline_synthesis.md](../synthesis/comms_baseline_synthesis.md). | **No.** Belief record only. |
