# Communications Wave 2 Lint Report

**Date:** 2026-06-11
**Scope:** the three wave-2 dollar-sizing docs plus the appended thesis Revision 2.
**Mode:** read-only on the source docs. This report records findings and a
prioritized fix list; it does NOT modify the source docs. The catalog and ledger
edits (LIBRARY, RESEARCH_TRACKER, SOURCE_INDEX) were applied separately as part of
the wave-2 ingest.

Docs reviewed:

- [economics/comms_rural_fringe_sizing.md](../economics/comms_rural_fringe_sizing.md) (NEW; internal COMM-057..081)
- [economics/comms_premium_sovereign_sizing.md](../economics/comms_premium_sovereign_sizing.md) (NEW; internal COMM-057..078)
- [economics/comms_addressable_sizing.md](../economics/comms_addressable_sizing.md) (NEW consolidation; internal COMM-082..090)
- [vision/comms_thesis.md](../vision/comms_thesis.md) (MODIFIED; Revision 2 appended)

Reconciled into the global ledger as COMM-057..079 (see
[SOURCE_INDEX.md](../SOURCE_INDEX.md)). Wave 1 occupies COMM-001..056.

---

## Verdict

The wave-2 set is structurally sound and internally consistent in the ways that
matter most. It is faithful to the wave-1 base (the $1.6T cited TAM, the $129B
realistic served estimate, the ~90% haircut, and the ~300M / ~3.1B coverage-vs-
usage gap split are all carried correctly), the overlap de-duplication in the
consolidation is correct, the bands are honestly flagged ILLUSTRATIVE, and the
thesis Revision 2 was appended without altering Revision 1. There are no broken
links.

The findings below are wording and roll-up issues, not deletion issues. One is
material (a premium-pool roll-up that exceeds the sum of its own components); the
rest are minor consistency and tagging notes. None blocks the catalog or the
ledger. No verdict on the comms business is implied or required.

---

## 1. Consistency with the wave-1 base and across the wave-2 docs

**Consistent with the wave-1 base.** Every load-bearing wave-1 anchor reappears
unchanged:

- The cited `$1.6T` connectivity TAM and the Morningstar `~$129B` realistic served
  estimate are quoted exactly as the base established them
  ([comms_space_tam_claims.md](../economics/comms_space_tam_claims.md), wave-1
  COMM-035 and COMM-037).
- The `~90%` haircut / "served is ~5-10% of cited" prior is respected: the rural
  fringe lands at ~2.5-8% of $1.6T, the consolidated pool at ~3-9%, the premium
  open slice at ~0.5-2%. All sit inside or just below the 5-10% band, which is the
  expected place for a subset of the served market. No wave-2 number silently
  treats a cited TAM as reachable.
- The `~300M` coverage gap / `~3.1B` usage gap split is carried from wave-1
  COMM-021 and is the structural spine of the rural-fringe doc (only the coverage
  gap plus underserved-but-payable rural is space-addressable; the usage gap is an
  income problem satellite supply does not fix). This is used identically in all
  three docs.

**Consistent across the three wave-2 docs.** The rural-fringe headline
(~$40-55B / ~$95-130B) and the premium gross pool (~$75-95B) and open slice
(~$8-30B) are carried into the consolidation verbatim, not silently re-derived.
The share-of-anchor figures agree across docs to rounding:

| Figure | Rural doc | Premium doc | Consolidation | Agree? |
|---|---|---|---|---|
| vs $1.6T (the relevant pool) | ~2.5-8% (fringe) | ~6-7% pool / ~0.5-2% open | ~3-9% (consolidated) | Yes, each is the correct pool's share |
| vs $129B | ~30-100% (fringe) | ~60-75% pool / ~6-23% open | ~35-45% to at-or-above (consolidated) | Yes, different pools, internally coherent |

**Internal arithmetic that checks out.**

- Rural Pool A conservative tiers A+B+C ($13-20B + $20-28B + $5-8B = ~$38-56B)
  reconcile to the stated ~$40-55B; optimistic A+B+C+D ($25-35B + $30-40B +
  $15-25B + $20-30B = ~$90-130B) reconcile to ~$95-130B.
- Consolidation conservative buckets 1-4 ($13-20B + $5-8B + $20-28B + $5-10B =
  ~$43-66B) reconcile to ~$45-60B; optimistic buckets 1-5 add ~$105-160B,
  reconciling to ~$110-150B. The "slightly above a naive A + B-open sum"
  explanation (bucket 4 adds the open-government layer; bucket 3 removes the
  mobility double-count) is correct and the two adjustments partly offsetting is
  the right read.

---

## 2. The overlap de-duplication in the consolidation (sound)

The consolidation's core job, not double-counting the mobility/enterprise
verticals that legitimately appear in both the rural-fringe build (its Tier B) and
the premium-niche build (its premium-enterprise block), is done correctly.

- The five-bucket decomposition (Section 2) is genuinely non-overlapping: developed
  rural, emerging rural, the shared mobility/enterprise block (counted once),
  premium/sovereign-specific additions, and the optimistic-only direct-to-cell
  add-on. Each vertical is assigned to exactly one bucket, and the assignment table
  (maritime, aviation, energy, remote-government all to bucket 3, "count once") is
  explicit.
- Remote-government field sites are correctly assigned to ONE place (the government
  layer) rather than being counted both as Tier B and as the open-government layer.
- The shared block is sized using the rural-fringe doc's Tier B (~$20-28B
  conservative), which is the right call because that build already values the same
  physical demand (the vessels, aircraft, remote sites) the premium doc's
  enterprise block values. The doc states this attribution is reasoned, not
  modeled, which is the honest caveat.
- The overlap is independently corroborated from the operator segment data
  (Starlink maritime ~$1.94B and enterprise ~$1.68B run-rate, Value Add VC / Skift),
  so the de-dup is grounded, not asserted.

No double-count survives the consolidation. This is the strongest part of the set.

---

## 3. FACT-tagged numbers that are actually single-source

The docs' reading-guide `[FACT]` tag is mostly used correctly (primary/official or
multi-source). A few `[FACT]`-tagged rows rest on a single source and should be
read as `sourced_estimate`-grade, not certified. These are flagged in the docs'
own text in most cases, but the tag itself overstates them:

- **Rural COMM-072 (US "broadband desert" ~6% of households) and COMM-073 (US
  rural-with-weak-terrestrial ~12%)** are tagged `[FACT]` but rest on a single
  source (Via Satellite, March 2026). They are load-bearing for the US Tier A
  household count (~8-13M HH). Single-source; treat as sourced_estimate.
- **Rural COMM-074 (OECD ~78.5% rural coverage at 30 Mbps)** is tagged `[FACT]`
  from one OECD release. The percentage is clean, but the developed-ex-US absolute
  household count (~20-30M) derived from it is the doc's own arithmetic and is
  correctly flagged softer in-text, the tag on the underlying row is fine, the
  derived count is the soft part.
- **Premium COMM-064 (pLEO $13B ceiling / ~$660M spent) and COMM-065 (FY26
  COMSATCOM/SATCOM budget lines)** are tagged `[FACT]` and are individually
  sourced, but the load-bearing derived number built on them, the ~$3-8B/yr
  annually-contestable open layer (COMM-066), is an `[ESTIMATE]` and is correctly
  tagged as such. The ceiling-vs-outlay trap is called out. No fix needed beyond
  noting the open-layer figure is the doc's own estimate, not a published annual
  outlay.

Correctly handled (not flagged here as problems, listed for completeness): the
Starlink FY2025 $11.39B revenue and the -33% ARPU trajectory carry two sources
each; the SDA Transport (>300 sats) and SDN ($2.29B) figures carry two sources
each; the IRIS2 EUR 10.6B and GOVSATCOM figures are multi-source. The genuinely
single-source items the docs DO flag honestly: the ~$2,000/yr Starlink residential
ARPU, the Value Add VC developed-vs-emerging split, the Quilty 25-30M capacity
cap, the Oxford Economics 78M-421M user range, the Morningstar ~$10B US-Niche PDF
excerpt, the finance/low-latency spend (dated TABB 2010), and the enterprise-satcom
umbrella. The ledger records all of these as `sourced_estimate` / `projection` with
the single-source flag preserved.

---

## 4. Broken links

None. All eleven internal relative markdown links across the three wave-2 docs
resolve to existing files:

- rural-fringe doc -> comms_global_regional_market, comms_space_tam_claims,
  comms_baseline_synthesis. All present.
- premium doc -> comms_business_case, rf_limited_service, comms_baseline_synthesis,
  ai_datacenter_tam. All present.
- consolidation -> comms_baseline_synthesis, comms_thesis,
  comms_premium_sovereign_sizing, comms_rural_fringe_sizing. All present.

External (http) source links were not fetched in this pass (read-only,
offline-checkable links only); the docs carry 2+ source links per hard number per
their own reading guide.

---

## 5. Thesis Revision 2 appended without altering Revision 1 (confirmed)

Revision 1 is structurally intact. The file opens with the unchanged Revision 1
title and belief record (the four hypotheses, the tying-thread section, the
Revision 1 open questions, and the "what this revision deliberately does not do"
section all remain in place above the Revision 2 heading). Revision 2 is a clean
append:

- Revision 2 is correctly scoped: it updates ONLY the confirm/break notes for
  Hypothesis 2 (space as a step change) and Hypothesis 4 (security/sovereignty),
  the two gated on the now-sized numbers, and explicitly does NOT touch Hypothesis
  1 or Hypothesis 3 (no wave-2 evidence bore on them). This matches the
  instruction.
- The dollar numbers in Revision 2 match the source docs exactly (rural fringe
  ~$40-55B to ~$95-130B; premium gross ~$75-95B with ~$8-30B open; consolidated
  ~$45-60B to ~$110-150B; ~3-9% of $1.6T; in the band of $129B).
- The revision-history table gained a Revision 2 row and the "No verdict" status is
  preserved on both rows.
- Revision 2 correctly keeps the sizes demand-side and ILLUSTRATIVE and explicitly
  moves the open question downstream (supply economics, single-operator capture
  rate, per-segment margin) rather than declaring the hypotheses confirmed. This is
  the honest framing and is consistent with the consolidation's "what this does not
  settle" section.

No alteration of Revision 1 detected.

---

## Prioritized fix list

### Blocker

None. Nothing here blocks the catalog, the ledger, or the thesis append.

### Material

1. **Premium/sovereign gross-pool roll-up exceeds the sum of its own components
   (`comms_premium_sovereign_sizing.md` Section 4.1; ledger COMM-070).** The
   component table sums to roughly `$60-70B/yr` (government ~$50B + enterprise
   ~$10-18B + finance ~$0.2-0.5B + orbital-DC backhaul ~$0.1-1B), but the stated
   total band is `~$75-95B/yr`. The headline band is ~$10-25B above its own
   addends. This propagates into the share-of-anchor figures (the ~$75-95B drives
   the "~6-7% of $1.6T" and "~60-75% of $129B" lines). It does not change the
   conclusion (the niche is still materially smaller than the mass market, and the
   open slice ~$8-30B is unaffected because it is built from the open sub-pools
   directly, not from the gross headline), but the gross number should either be
   reconciled to its components (~$60-70B) or the headline should be re-stated as a
   wider ~$60-95B span with the roll-up assumption shown. Recommended fix in the
   source doc: add one line under the Section 4.1 table explaining the upper-bound
   roll-up, or tighten the band to ~$60-80B. The ledger (COMM-070) and the
   claims-to-repair section already carry this caveat so external quoting is
   guarded in the meantime.

### Minor

2. **A few `[FACT]` tags are single-source (Section 3 above).** Rural COMM-072 /
   COMM-073 (US ~6% desert / ~12% rural, single Via Satellite source) are the
   clearest cases. Recommend downgrading the in-doc tag from `[FACT]` to
   `[ESTIMATE]` (single-source) for these two rows so the tag matches the evidence;
   the ledger already records them as `sourced_estimate` via the long-tail row
   (COMM-065).

3. **Direct-to-cell definitional ambiguity is live, not resolved
   (`comms_rural_fringe_sizing.md` Tier D; consolidation bucket 5).** The optimistic
   case includes a ~$20-30B carrier direct-to-cell add-on that both docs correctly
   flag as "not rural-fringe broadband." It is handled honestly (held out of the
   conservative case, and the strip-it-out ceiling ~$90-120B is given), but whether
   it belongs in a "space-comms addressable" number at all is a definitional call
   the docs explicitly punt to the lead. This is now recorded as an open question in
   RESEARCH_TRACKER. No fix to the docs needed; flagging that the optimistic
   headline (~$110-150B and ~$95-130B) is sensitive to this single call.

4. **Orbital-DC backhaul rests on an author-set assumption
   (`comms_premium_sovereign_sizing.md` Section 3.2).** The ~3-8%-of-compute
   backhaul fraction is the author's assumption, correctly flagged "for the founder
   to set, not a sourced figure," and the segment is deliberately held to a modest
   ~$0.1-1B so it cannot inflate the total. Per the project rule on not inventing
   modeling assumptions, this is the one number in the set the founder should set
   rather than the doc; it is small enough not to move the headline. No correction,
   just a pointer.

5. **Pre-existing em-dashes in `LIBRARY.md` (out of scope, noted for hygiene).**
   `LIBRARY.md` contains 24 em-dash characters, all in pre-existing content (the
   framing bullets and the glossary-term headers, lines 1-288), none introduced by
   the wave-2 edits. The wave-2 additions to LIBRARY, RESEARCH_TRACKER, and
   SOURCE_INDEX contain zero em-dashes. Flagged only because the project bans the
   character; cleaning the pre-existing 24 is a separate hygiene task outside the
   wave-2 edit scope.

---

## What this report does not do

- It does not modify the three source docs or the thesis. Findings only.
- It does not fetch or validate external (http) sources; only internal-link
  resolution was checked.
- It does not render a verdict on the comms business, and it does not re-open the
  ILLUSTRATIVE status of the bands. Those are correctly the docs' own framing and
  are out of scope for a lint pass.
