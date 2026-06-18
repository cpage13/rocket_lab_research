# Communications Wave 1: Lint Report

*Lint date: 2026-06-11. Read-only QA pass over the 12 communications wave-1 docs against each other and the existing comms corpus. No source doc was modified; this report is for the lead to triage.*

## Scope and method

This pass checks the 12 wave-1 docs:

- Markets: `economics/comms_us_broadband_market.md`, `economics/comms_us_cellular_market.md`, `economics/comms_global_regional_market.md`, `economics/comms_space_tam_claims.md`
- Deployment economics: `economics/comms_broadband_deployment_economics.md`, `economics/comms_cellular_5g_deployment_economics.md`
- Technology: `direct_communication/spectrum_fundamentals_economics.md`, `direct_communication/bands_and_enabling_hardware.md`, `laser_comms/laser_terrestrial_interconnect.md`
- Competitor cadence: `competitors/falcon9_cadence_ramp.md`
- Synthesis and thesis: `synthesis/comms_baseline_synthesis.md`, `vision/comms_thesis.md`

against the existing comms corpus: `laser_comms/*.md` (`optical_comms`, `optical_ground_stations`, `constellation_mesh`, `rf_satcom`, `rf_limited_service`, `comms_business_case`), `rocket_lab/space_hardware_capabilities.md`, and `competitors/starship_addendum.md`.

It checks five things: (1) contradictions (new-vs-existing and new-vs-new); (2) stale/superseded claims; (3) broken or wrong relative links; (4) numbers presented as FACT that are actually single-source or estimate; (5) untracked gaps. The prioritized fix list is at the end (blocker / material / minor).

**Headline:** the corpus is in good shape and unusually disciplined about tagging (FACT/ESTIMATE/PROJECTION) and flagging single-source figures. There are **no blockers**. The one genuinely material item is a set of carrier-financial inconsistencies between the two US market docs, which the synthesis already reconciles into ranges but the source docs state as conflicting point values. Everything else is minor.

---

## 1. Contradictions

### 1.1 [MATERIAL] Verizon and AT&T financials differ between `comms_us_broadband_market` and `comms_us_cellular_market`

The same companies carry different point values in the two US market docs (different aggregator timestamps, same June 17 2026 nominal date):

| Figure | `comms_us_broadband_market` | `comms_us_cellular_market` |
|---|---|---|
| Verizon market cap | ~$191B | ~$201B |
| AT&T market cap | ~$156B | ~$160B |
| AT&T FY2025 revenue | ~$125.7B | $125.6B |
| Verizon FY2025 net income | ~$17.2B | $17.6B |

These are real cross-doc disagreements, not roundings (the Verizon cap gap is ~$10B / ~5%). **Mitigant:** the synthesis (`comms_baseline_synthesis` Section 1.4) already handles this correctly: it shows Verizon "~$191-201B", AT&T "~$156-160B", Verizon NI "~$17.2-17.6B" as ranges bracketing both, and explicitly notes "The two docs report Verizon and AT&T market cap and net income in slightly different point ranges (different aggregator timestamps); both ranges are shown." So the synthesis is the reconciler. The issue lives only in the two source docs presenting conflicting *point* values, both tagged `[FACT]`. Recorded in `SOURCE_INDEX` `COMM-003`/`COMM-011` and added to the "Claims To Repair" list. Fix: have each source doc cite one reconciled, dated value (or a range), not two conflicting points.

### 1.2 [MATERIAL] Carrier fixed-broadband subscriber counts differ between `comms_global_regional_market` and the US anchor docs

`comms_global_regional_market` Section 4 (North America operator row) lists US fixed operators as "Comcast (~31M), Charter (~30M), AT&T (~14.5M), Verizon (~13M), T-Mobile FWA (~8.9M)", citing one Broadband Breakfast source. The US anchor docs give different numbers for the same carriers:

| Carrier | `comms_global_regional_market` | US anchor docs |
|---|---|---|
| Verizon broadband | ~13M | **>16.3M** (post-Frontier; `comms_us_broadband_market`, `comms_us_cellular_market`) |
| AT&T broadband | ~14.5M | ~14.3M (`comms_us_broadband_market`) |
| T-Mobile FWA | ~8.9M | ~8M (`comms_us_broadband_market`) |

The Verizon `~13M` vs `>16.3M` gap is the notable one: `~13M` reads as a **pre-Frontier-close** figure, while the US docs are explicitly post-Frontier (the Verizon-Frontier deal closed Feb 2026, adding ~2.2M fiber subs). Within the same wave, one doc carries a stale-looking pre-close Verizon broadband count. AT&T ~14.5M vs ~14.3M and T-Mobile ~8.9M vs ~8M are smaller but still inconsistent. The global doc's numbers come from a single secondary aggregator; the US-doc numbers come from the filings. Fix: reconcile the global doc's North America operator row to the (post-Frontier, filing-based) US-anchor figures, or annotate it as a differently-dated secondary snapshot.

### 1.3 [MINOR] `comms_us_cellular` Section 1 vs the lead's existing US-wireless context

`comms_us_cellular` flags this itself (Open Questions): "The lead may already hold a competing figure in the shared SOURCE_INDEX" for US wireless service revenue. As of this pass the existing `SOURCE_INDEX` `REV` block carries no US-total-wireless-service-revenue line, so there is no actual collision today; the ~$326B is newly added as `COMM-009`. No action beyond noting the figure is single-source (see 4.1).

### 1.4 [NOT A CONTRADICTION] Optical scale, RF band capacity, and Mynaric figures match the existing corpus

Checked and consistent, recorded here to show the cross-check was done:

- **Optical scale.** `bands_and_enabling_hardware` and the synthesis cite TBIRD 200 Gbps space-to-ground, ~27,000 Starlink space lasers (~9,000+ sats x ~3 terminals), 42+ PB/day, >99% uptime, and "4+ ground stations for 99-99.9%." These match `optical_comms.md` and `optical_ground_stations.md` exactly. No drift.
- **RF capacity.** `bands_and_enabling_hardware` gives Ka HTS ~500 Gbps/sat and V-band VHTS ">1 Tbps/sat"; the synthesis says V-band "targets ~1.5 Tbps." Existing `rf_satcom.md` says ~500 Gbps Ka and "~1.5 Tbps" V-band. ">1 Tbps" is consistent with (vaguer than) "~1.5 Tbps", not a contradiction. Recorded in `COMM-045`.
- **Mynaric CONDOR.** Synthesis 3.5 says "Mk3 ships at ~2.5 Gbps as-delivered; Mk3.1 roadmap up to 100 Gbps" and "Mynaric CONDOR (acquired April 2026)." This matches `optical_comms.md` (Mk3 ~2.5 Gbps, Mk3.1 up to 100 Gbps; acquisition 14 April 2026, ~$155M) and `space_hardware_capabilities.md` (harmonized 2026-05-17). No drift; the synthesis just omits the exact date/price (fine for a synthesis).
- **Starship timeline.** `falcon9_cadence_ramp` references `starship_addendum`'s 2028-2031 cheap-cadence window, the Starbase FAA cap of 25 launches/yr, AI-1 first deployments ~2028, and the Starship 5-of-25 2025 miss. All match `starship_addendum.md`. The Falcon-9 doc adds historical evidence consistent with, not contradicting, the addendum.

### 1.5 [MINOR / metric mismatch to watch] Starlink "subscribers" vs "D2D users" vs "ISL count"

Three different Starlink numbers appear and should not be conflated:

- `comms_global_regional_market`: Starlink ~9M subscribers (Dec 2025), >12M (mid-2026) -- these are broadband subscribers.
- `comms_us_cellular_market`: Starlink Direct to Cell 16M unique users (Mar 2026) -- these are D2D users, a different product/metric.
- `optical_comms` / `bands_and_enabling_hardware`: ~9,000+ Starlink satellites, ~27,000 space lasers -- constellation hardware, not users.

No doc actually conflates them, but the >12M broadband-subs and 16M D2D-users figures sit close enough that a careless reader could merge them. Worth a one-line clarifying footnote if these ever appear together.

---

## 2. Stale / superseded claims

- **[MATERIAL, see 1.2] The Verizon ~13M broadband figure in `comms_global_regional_market`** is effectively superseded by the post-Frontier >16.3M used in the US docs and elsewhere in the same wave. Treat the global doc's North America operator row as the stale one.
- **[MINOR] No stale links to retired artifacts.** None of the 12 docs references the retired root `conclusion.md`, old `code/` paths, or superseded model summaries. They correctly point to `data_center/` only where appropriate (e.g. `comms_space_tam_claims` and `falcon9_cadence_ramp` reference `starship_addendum`, which itself points to `data_center/ai1_comparison.md`). Clean.
- **[MINOR] `THR-010`-style staleness analogue.** `comms_cellular_5g_deployment` references a McKinsey "road to 5G" TCO figure that it explicitly did NOT place in its claims table because the primary page was unreachable. That is correct discipline (a known-unverified figure kept out of the ledger), not a stale claim. No action.

---

## 3. Broken or wrong relative links

A structural check of the cross-references. All internal links resolve to files that exist; spot-checks of the relative path depth:

- **[OK] `direct_communication/` docs to `laser_comms/` and `rocket_lab/`.** `spectrum_fundamentals_economics` and `bands_and_enabling_hardware` use `../laser_comms/rf_satcom.md`, `../laser_comms/rf_limited_service.md`, `../rocket_lab/space_hardware_capabilities.md`. Correct depth (both folders are siblings under `research/`). Files exist.
- **[OK] `synthesis/comms_baseline_synthesis` to economics/laser_comms/etc.** Uses `../economics/...`, `../direct_communication/...`, `../laser_comms/...`, `../competitors/...`, `../rocket_lab/...`. Correct from `synthesis/`. Files exist.
- **[OK] `vision/comms_thesis` to synthesis and within-folder.** Uses `../synthesis/comms_baseline_synthesis.md` (correct) and `./initial_thesis.md` (correct same-folder; `vision/initial_thesis.md` exists).
- **[OK] `economics/comms_*` to `ai_datacenter_tam.md`.** The "Builds on" lines use `./ai_datacenter_tam.md` or `ai_datacenter_tam.md` (same-folder); that file exists under `economics/`.
- **[OK] `laser_comms/laser_terrestrial_interconnect` to `optical_ground_stations.md`, `optical_comms.md` (same folder) and `../llm_compute/multi_rack_inference.md`.** Correct depth; files exist.
- **[OK] `competitors/falcon9_cadence_ramp` to `starship_addendum.md` (same folder), `../rocket_lab/neutron/launch_cost_economics.md`, `../peer_review/review_engineer.md`.** Correct; files exist.

**No broken or wrong-depth relative links found.** One stylistic note (not a break): the docs mix `[text](path)` markdown links with inline `` `path` `` code-span references to other docs (e.g. `` `rf_satcom.md` `` without a link). Both are readable; not a defect, but if the lead wants uniform clickable navigation, the code-span references in `comms_us_cellular`, `spectrum_fundamentals`, and `bands_and_enabling_hardware` could be promoted to real links.

---

## 4. Numbers presented as FACT that are actually single-source or estimate

The docs are generally honest here (most are flagged in-doc). The ones worth surfacing for the lead, because they are load-bearing and tagged `[FACT]` or read as fact:

- **[MATERIAL] US wireless service revenue ~$326B [FACT-tagged as ESTIMATE, single source].** `comms_us_cellular` correctly tags it `[ESTIMATE] single major source` (IBISWorld) and cross-checks against a ~$200B big-three bottom-up sum, but the headline-summary framing can read as harder than it is. Recorded as `sourced_estimate` in `COMM-009` and added to "Claims To Repair." This is the single most load-bearing US comms number and rests on one research firm.
- **[MATERIAL] The extreme-rural fiber cost ~$200,000-230,000/passing and the ~4% third-overbuilder ROI [FACT, single primary source].** Both in `comms_broadband_deployment`, both tagged `[FACT]` but each flagged in-doc as resting on a single primary source (Fierce Network; EY). They are load-bearing for the "space value is in the tail" conclusion. Recorded in `COMM-032`/`COMM-033` as `sourced_estimate`. Keep the single-source caveat attached wherever quoted.
- **[MINOR] The Morningstar ~$129B served market and the ~90% haircut.** Correctly tagged `[PROJECTION]` and `[ESTIMATE]` in `comms_space_tam_claims`; the haircut is corroborated by four analysts, so the *direction* is high-confidence, but the exact $129B is one analyst model. Recorded as `projection`/`derived_estimate` in `COMM-037`/`COMM-038`. No over-claim, noted for completeness.
- **[MINOR] Cox financials (~$6.7B / ~6M subs) and AT&T ~14.3M combined fiber+FWA.** Both flagged single-source in `comms_us_broadband` and folded into the `COMM-008` long-tail summary with the flag preserved. No over-claim.
- **[MINOR] The $15.4B ASTS commercial model and the $200B combined-bank figure.** Both flagged single-source in `comms_space_tam_claims` (one X post; one rate-limited trade-press summary). Folded into `COMM-039` with the flag. No over-claim.
- **[MINOR] Several European per-MHz-POP decimals, the global $140B/$37.7B spectrum totals, the W-band PA specs, the NTT 160 Gbps/300 GHz record, the NxBeam V-band part.** All flagged single-source/single-demo/single-vendor in `spectrum_fundamentals` and `bands_and_enabling_hardware`, and folded into `COMM-043`/`COMM-047` with the flag. No over-claim.
- **[MINOR] The ~8-10 year 5G payback.** `comms_cellular_5g_deployment` tags it `[ESTIMATE] single-source` and flags it for corroboration. Recorded in `COMM-028`. No over-claim.

**Net:** the docs do not pass off single-source figures as hard facts in a misleading way; the in-doc flagging is consistently present. The two items worth the lead's explicit attention are the ~$326B US wireless figure (because it anchors the US sizing) and the ~$200K/passing and ~4% ROI figures (because they anchor the "value is in the tail" thesis). All are now in `SOURCE_INDEX` with `sourced_estimate` status and the single-source caveat.

---

## 5. Untracked gaps

The docs themselves enumerate their open questions well. The gaps that should be tracked at the wiki level (and which I have added to `RESEARCH_TRACKER`'s backlog) are:

- **[TRACKED NOW] US-only fixed-broadband revenue boundary** ($63.6B narrow vs ~$92B broad vs $100.5B North America). Needs one agreed definition before any comms TAM math.
- **[TRACKED NOW] Ex-China Asia split.** Published Asia Pacific totals include China; a clean ex-China Asia figure is not directly published.
- **[TRACKED NOW] Dollar size of the satellite-addressable rural/remote fringe.** The realistic slice is "coverage gap + underserved rural," not the whole pool; sizing it in dollars (where ARPU is low) is the missing number.
- **[TRACKED NOW] Premium/sovereign niche size.** Rocket Lab's actual market, referenced from `comms_business_case` but unsized in dollars. The central unanswered business number.
- **[TRACKED NOW] Direct-to-cell revenue per user.** Large user counts (Starlink 16M) but thin/unclear per-user revenue; AST pre-scale. Unit economics of "fill the dead zones" unproven.

Two further gaps that are not yet in the backlog and the lead may want to add:

- **[GAP, not yet tracked] A de-duplicated served-market map across D2D vs fixed broadband.** The $1.1T (ASTS, D2D-to-phone) and $1.6T (SpaceX connectivity, broadband-to-terminal) overlap in ways no doc cleanly decomposes. Both `comms_space_tam_claims` and the synthesis flag this; it is a natural next-wave sizing.
- **[GAP, not yet tracked] Space-grade radiation-hardened silicon photonics.** `bands_and_enabling_hardware` could not find space-qualified SiPh coherent-transceiver modules as catalog products (every space optical link today is a purpose-built terminal or an adapted fiber-telecom transceiver). This is a real hardware open question that bears on any optical-backbone cost model and is currently only an in-doc open question, not a tracked gap.

---

## Prioritized fix list

### Blocker
*(none)*

### Material
1. **Reconcile the Verizon/AT&T financial point values** between `comms_us_broadband_market` and `comms_us_cellular_market` (cap ~$191B vs ~$201B, ~$156B vs ~$160B; revenue $125.7B vs $125.6B; NI $17.2B vs $17.6B). The synthesis already shows ranges; the source docs should cite one reconciled, dated value each rather than two conflicting `[FACT]` points. (Section 1.1; `SOURCE_INDEX` COMM-003/COMM-011 + Claims-To-Repair.)
2. **Fix the stale/inconsistent carrier broadband subscriber counts** in `comms_global_regional_market` Section 4 (Verizon ~13M reads pre-Frontier vs the >16.3M post-Frontier used everywhere else; AT&T ~14.5M vs ~14.3M; T-Mobile FWA ~8.9M vs ~8M). Reconcile to the filing-based US-anchor figures or annotate as a differently-dated secondary snapshot. (Sections 1.2, 2.)
3. **Keep the single-source caveat welded to the three anchor numbers when quoted externally:** US wireless service revenue ~$326B (one firm), extreme-rural ~$200K/passing (one source), third-overbuilder ~4% ROI (one source). Now in `SOURCE_INDEX` as `sourced_estimate` with the caveat; ensure any promotion into a public claim carries it. (Section 4.)

### Minor
4. Add a one-line footnote distinguishing Starlink broadband subscribers (>12M) from Starlink Direct-to-Cell users (16M) wherever they could appear together. (Section 1.5.)
5. Optionally promote the inline code-span doc references (`` `rf_satcom.md` `` etc.) in `comms_us_cellular`, `spectrum_fundamentals`, and `bands_and_enabling_hardware` to real markdown links for uniform navigation. (Section 3.)
6. Add the two untracked gaps to the `RESEARCH_TRACKER` backlog if the lead agrees they warrant it: the de-duplicated D2D-vs-broadband served-market map, and space-grade radiation-hardened silicon photonics. (Section 5.)

---

## What is clean (recorded so the cross-check is auditable)

- No broken or wrong-depth relative links across all 12 docs.
- Optical scale numbers, RF band-capacity figures, Mynaric CONDOR specs, and the Starship/AI-1 timeline are all consistent with the existing corpus (`optical_comms`, `optical_ground_stations`, `rf_satcom`, `space_hardware_capabilities`, `starship_addendum`). No new-vs-existing contradiction found.
- The China-excluded scope is applied consistently and labelled in every doc.
- FACT/ESTIMATE/PROJECTION tagging and single-source flagging are present and consistent across the wave; the synthesis carries its findings' confidence explicitly.
- The synthesis correctly reconciles the one real cross-doc financial contradiction (1.1) into ranges and says so.
- The thesis (`comms_thesis`) correctly renders no verdict and is cleanly separated from the neutral base.
