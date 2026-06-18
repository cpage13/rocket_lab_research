# Communications Wave 3 Lint Report

**Date:** 2026-06-17
**Scope:** the three wave-3 cost-side docs plus the appended thesis Revision 3.
**Mode:** read-only on the source docs. This report records findings and a
prioritized fix list; it does NOT modify the source docs. The catalog and ledger
edits (LIBRARY, RESEARCH_TRACKER, SOURCE_INDEX) were applied separately as part of
the wave-3 ingest.

Docs reviewed:

- [economics/comms_space_supply_cost.md](../economics/comms_space_supply_cost.md) (NEW; internal COMM-080..108)
- [economics/comms_incumbent_margins_competitive_floor.md](../economics/comms_incumbent_margins_competitive_floor.md) (NEW; internal COMM-080..103 with gaps)
- [economics/comms_ground_vs_space_cost_ratio.md](../economics/comms_ground_vs_space_cost_ratio.md) (NEW consolidation; internal COMM-109..117)
- [vision/comms_thesis.md](../vision/comms_thesis.md) (MODIFIED; Revision 3 appended)

Reconciled into the global ledger as COMM-080..103 (see
[SOURCE_INDEX.md](../SOURCE_INDEX.md)), continuing contiguously from the wave-2 tail
(COMM-079). Wave 1 occupies COMM-001..056; wave 2 occupies COMM-057..079.

---

## Verdict

The wave-3 set is structurally sound and internally consistent in the ways that
matter most. The space numerator (~$480-680/sub/yr all-in, ~$200-260 space-specific)
is anchored to the audited Starlink S-1 segment financials and flows cleanly into the
cost-ratio doc; the ground-marginal floor (~10-20% of ARPU = ~$84-180/sub/yr fixed,
~$0.50-1.50/GB mobile) is consistent between the margins doc and the ratio doc; both
flavor ratios are arithmetic on those sourced inputs; the data-center 1.92x mirror is
carried (not re-derived) in all three docs; and the addressable pool is cited
consistently with wave-2 COMM-075. The annualization assumptions for flavor (a) (a
~25-year fiber life at a ~9% capital charge) are stated and defended in the ratio doc.
Thesis Revision 3 was appended without altering Revision 1, and the only edits to
Revision 2 are the lead-reconciled gross-pool number (~$75-95B to ~$60-95B), not a
substantive rewrite. There are no broken links.

The findings below are wording, tagging, and in-flight-reconciliation issues, not
deletion issues. **No blockers.** One is material (an internal headline tension in the
space supply-cost doc's summary, where the same paragraph states ~$700-850/sub/yr and
~$480-490/sub/yr while the rest of the doc uses ~$480-680). The rest are minor
single-source-FACT-tag and post-reconciliation-residue notes. None blocks the catalog
or the ledger. No verdict on the comms business is implied or required.

A note on sequencing: the wave-2 lint report's single material item (the
premium/sovereign gross-pool roll-up stating ~$75-95B while its components sum to
~$60-70B) is the item the lead has now reconciled to ~$60-95B. That fix is applied in
SOURCE_INDEX (COMM-070) and is already propagated into thesis Revisions 2 and 3 and both
wave-2 sizing docs; one stale ~$75-95B mention survives in the cost-ratio doc's Section 7
note and is logged in Section 3 below as a follow-up, not a new defect.

---

## 1. Consistency of the wave-3 numbers with the wave-1/2 base and with each other

**The cross-doc chain is consistent.** The load-bearing numbers were checked across
all three docs:

- **Space all-in ~$480-680/sub/yr** and **space-specific ~$200-260/sub/yr** appear in
  the supply-cost doc (the source) and the cost-ratio doc (the consumer) with the same
  values; the margins doc correctly does not carry them (it is the ground-side doc).
  The cost-ratio doc's flavor-(b) numerator uses exactly this band.
- **The incumbent marginal floor is internally consistent across its two forms.** The
  margins doc states it as ~10-20% of ARPU / ~$7-15 per sub per month (fixed
  broadband). The cost-ratio doc annualizes that to **~$84-180/sub/yr** for the flavor-
  (b) denominator. $7-15/mo x 12 = $84-180/yr, so the two forms agree. Note for the
  reader: the ~$84-180/sub/yr figure is the cost-ratio doc's annualization; the margins
  doc itself never prints "$84-180", it prints the monthly/percentage form. The ledger
  records this (COMM-096 carries the monthly form as the source; the annual form is
  derived in the ratio at COMM-101).
- **Mobile marginal ~$0.50-1.50/GB** is consistent between the margins doc and the
  cost-ratio doc's per-GB table (Section 3.2).
- **Both flavor ratios** (a: ~1.3-3.2x rural, ~65-90x tail; b: ~3-8x served) live only
  in the cost-ratio doc, which is correct, it is the consolidation. The supply-cost and
  margins docs each hand off to it without pre-empting the ratio.
- **The data-center 1.92x mirror** is referenced in all three docs and is consistently
  described as carried from the data-center track, not re-derived. The directional
  claim (flavor (a) runs OPPOSITE to 1.92x; flavor (b) is a comparison the data-center
  track never makes) is stated identically in the supply-cost doc, the margins doc
  (Section 4), and the cost-ratio doc (Section 4).
- **The addressable pool** is cited in the cost-ratio doc and the margins doc as
  ~$45-60B conservative to ~$110-150B optimistic, consistent with wave-2 COMM-075. See
  the minor shorthand note in Section 1.1 below.

**1.1 (minor) The "~$45-150B" shorthand compresses the structured wave-2 band.** The
cost-ratio doc states the addressable target precisely as "~$45-60B/yr conservative to
~$110-150B/yr optimistic" in its load-bearing inputs (the builds-on list and Section
5), but twice compresses it to "~$45-150B" (Summary, and the Sources line). The
shorthand spans the conservative-low to optimistic-high, so it is an outer envelope
rather than a misstatement, but it reads looser than the structured band and could be
mis-cited as a single ~$45-150B range. Prefer the structured "~$45-60B to ~$110-150B"
form. Minor.

**1.2 (minor) ARPU figure is internally consistent.** The supply-cost doc gives Q1-2026
ARPU as ~$66/mo and uses ~$790/yr as the annualized ARPU base (66 x 12 = $792, rounds
to ~$790); the cost-ratio doc uses ~$790 ARPU throughout. Consistent. The doc also
carries a ~$790-1,100/yr revenue-per-subscriber range (reflecting the $99-to-$66 ARPU
glide) which is correctly distinguished from the ~$790 current-ARPU anchor. No action.

---

## 2. The two-flavor ratio logic and the annualization assumptions (sound)

**2.1 The two-flavor split is logically sound.** The core claim, that the ground "cost
to deliver" is two different numbers depending on whether the ground plant already
exists, and that this produces two opposed ratios, is internally coherent and is the
honest answer to the founder's single-ratio request. The supply-cost doc establishes
that the space side is a single flat-per-location cost; the margins doc establishes
that the ground side bifurcates into a fresh-build cost and a sunk-plant marginal cost;
the cost-ratio doc puts both on the same per-subscriber-per-year basis and derives the
two ratios. Each step follows from the one before. The asymmetry conclusion (space wins
where there is no sunk-plant floor, loses where there is one) is correctly derived, not
asserted, and is independently corroborated (Section 2.3 below).

**2.2 The annualization assumptions are stated.** Flavor (a) annualizes the fresh
rural-fiber build over a **~25-year fiber asset life** at a **~9% capital charge**
(capital-recovery-factor method), divides the passing capex by the ~46% take-rate to
get per-subscriber capex, and adds ~$150/sub/yr ground opex. All four inputs are stated
explicitly (Section 1 and Section 2.1), and the asset life and capital charge are
sourced (IRS class life 24 yr; industry 20-25 yr; the ~9% sits at the low end of the
sourced ~10-15% fiber IRR hurdle). The doc correctly observes that both chosen values
make the annualized ground number LOWER, hence more favorable to ground, so the
resulting ratio is conservative against space. This is the right direction to err in a
neutral base doc and is flagged as such.

**2.3 The flavor-(a) result is corroborated outside the model.** The 2025-26 BEAD
procurement evidence (fiber at ~$100k/location being rejected for satellite; Maine
subsidizing Starlink for ~9,000 locations; Colorado satellite ~$363M vs fiber ~$464M
requests) is a genuine independent cross-check that the arithmetic matches real
procurement behavior in the high-cost tail. Multi-source. This raises the confidence on
the flavor-(a) direction from "model output" to "model output confirmed by live
procurement," which the doc claims appropriately (medium-high on the asymmetry).

---

## 3. FACT-tagged numbers that are actually single-source

The wave-3 docs are generally disciplined about flagging single-source figures inline
and in their claims tables and Confidence sections. The items below are the ones a
reader must not lift as hard multi-source facts; each is already flagged in its source
doc, and each is carried with its flag into the ledger.

**3.1 (minor, lineage) The ~$6-8B/yr satellite-replacement capex is single-lineage, and
it is load-bearing.** The supply-cost doc's ~$6-8B/yr replacement capex and ~1,000
sats/yr replacement rate come from one 2024 analyst lineage (Motley Fool). The doc
flags this explicitly and even notes the figure is arithmetically low against a
~10,000-sat fleet on a 5-year life (which mechanically implies ~2,000+ replacements/yr).
The reason this matters beyond a normal single-source flag: this number is the input to
the **~$200-260/sub/yr space-specific cost split**, which is in turn the space-specific
portion the cost-ratio doc carries. So a soft single-lineage figure propagates two docs
downstream into a load-bearing split. The doc handles it honestly (the ~$200-260 split
is tagged DERIVED/ESTIMATE, not FACT, and the Confidence section calls it out), but the
lead should be aware the space-specific cost line rests on a 2024 single-analyst
maintenance-capex estimate. Ledger: COMM-088 (the capex) and COMM-091 (the split that
inherits it) both carry the flag. No fix required in the doc; logged for visibility.

**3.2 (minor) The mobile ~$0.50-1.50/GB delivery cost is single-source but tagged
[FACT].** The margins doc tags the mobile per-GB delivery cost [FACT] in its claims
table (internal COMM-096) while its own Confidence section and the inline text correctly
state it is single-source (one industry commentator, Tom Allen / LinkedIn), cross-
checked only against the MVNO-wholesale logic. The [FACT] tag is therefore slightly
generous for a single-source figure; the prose and Confidence section are accurate. The
ledger records it as `sourced_estimate` with an explicit single-source flag (COMM-095),
which is the correct status. No fix required in the doc beyond the existing flag;
prefer not to quote the ~$0.50-1.50/GB as a settled fact.

**3.3 (minor) The ~80-90% broadband gross margin is triangulated, not audited.** The
margins doc tags this [FACT] but is careful (inline and in Confidence) to state it is
triangulated across four press/operator outlets, several of which predate 2015 (the
Time Warner 97% example, the WSJ 90% piece), and is not a single audited analyst
decomposition. The doc's own guidance ("treat ~90% as order-of-magnitude correct, not a
precise constant") is the right read. Ledger: COMM-094 records it as `sourced_estimate`
with the triangulation-and-vintage caveat. The direction and magnitude are robust; the
precise percentage is soft.

**3.4 (minor) The ~$15-25B cumulative constellation capex is a reconstruction.** The
supply-cost doc is explicit that this is a reconstructed estimate, not a disclosed S-1
line, and tags it ESTIMATE. The only primary anchor is SpaceX's own May 2018 "at least
$10B" statement. Correctly flagged; ledger COMM-083 records the reconstruction status.

**3.5 (minor, post-reconciliation residue) One source paragraph still prints the pre-fix
~$75-95B gross pool.** The lead's premium/sovereign reconciliation to ~$60-95B has been
applied widely: SOURCE_INDEX COMM-070, thesis Revisions 2 and 3, and both wave-2 sizing
docs (`comms_premium_sovereign_sizing.md`, including its internal COMM-074 row, and
`comms_addressable_sizing.md`, including its internal COMM-083 row) all now read ~$60-95B.
The single remaining residue is the **cost-ratio doc's Section 7 "Note for the Lead"**
reconciliation paragraph, which still states the gross pool as ~$75-95B (vs the ~$60-70B
component roll-up) and references it as "COMM-083" (the wave-2 docs' internal id; the
global ledger id is COMM-070). That paragraph is in fact the note that PROMPTED the lead
fix, so it reads as the still-open flag it raised; now that the fix is applied, the
paragraph is stale. Because this report is read-only on source docs, it is logged here as
a one-line lead follow-up: update the cost-ratio doc's Section 7 note to ~$60-95B (or mark
it resolved) so it matches the ledger, the thesis, and the two sizing docs. The cost-ratio
doc's own conclusions are unaffected (it consumes only the downstream ~$45-150B addressable
band, not the gross pool), so this is cosmetic consistency, not a logic error.

---

## 4. Broken links

**None.** Every internal relative link in the three wave-3 docs resolves to an existing
file:

- supply-cost doc: the five `../laser_comms/`, `../competitors/`, and
  `../rocket_lab/neutron/` cross-references all resolve.
- margins doc: the five `./comms_*` economics cross-references all resolve.
- cost-ratio doc: the five `./comms_*` economics cross-references (space supply cost,
  incumbent margins, broadband deployment, cellular deployment, addressable sizing) all
  resolve.
- thesis Revision 3: the new `../economics/comms_space_supply_cost.md`,
  `../economics/comms_incumbent_margins_competitive_floor.md`, and
  `../economics/comms_ground_vs_space_cost_ratio.md` links, plus the carried Revision 1/2
  links, all resolve.

External (http) sources were not fetched; this check covers internal repository links
only, consistent with the wave-1 and wave-2 lint reports.

---

## 5. Thesis Revision 3 appended without altering Revision 1 or Revision 2 (confirmed)

**Revision 3 is purely additive.** The new `## Revision 3` section sits after Revision 2
and before the Revision history table, and a `Revision 3` row was added to that table.
The section order is Revision 1 (top) to Revision 2 to Revision 3 to Revision history,
unchanged except for the append. Revision 3 is correctly scoped: it updates only
Hypothesis 2's confirm/break notes (the hypothesis the cost test bears on), explicitly
leaves Hypotheses 1, 3, and 4 unchanged, and renders no verdict (the ratio is a cost-
and-competitive base; the entrant-specific non-Starlink cost stack and competitive share
remain open, which the section states three times).

**Revision 1 is untouched.** No line in the Revision 1 body changed.

**The only edits to Revision 2 are the lead-reconciled number, not a rewrite.** Revision
2's gross-pool figure was updated from ~$75-95B to ~$60-95B in three places (the "what
landed" bullet, the Hypothesis-4 "confirming half" bullet, and the Revision 2 history-
table row). This is the lead's premium/sovereign reconciliation propagating into the
thesis, not a substantive change to Revision 2's reasoning; every other Revision 2 line
is unchanged. This is the correct and consistent place for that number to land, and it
means the thesis already matches the reconciled SOURCE_INDEX COMM-070. Confirmed, no
action.

---

## Prioritized fix list

The lead reviews before committing. This report does not apply any of these; the catalog
and ledger edits were applied separately.

### Blocker

None.

### Material

1. **Resolve the space all-in cost headline tension in the supply-cost doc Summary
   (source-doc edit, lead's call).** Summary point 1 of
   [comms_space_supply_cost.md](../economics/comms_space_supply_cost.md) states, in a
   single paragraph, that the mature incumbent "delivers for roughly **$700-850/yr**
   all-in" and then that "the all-in delivery cost is therefore on the order of
   **$480-490/subscriber/yr**", while Section 5.1 (the table), Section 6 (the handoff),
   and the claims table (COMM-105) all use the canonical **~$480-680/yr**. Three
   different framings of the same headline number appear, and the ~$700-850 line is the
   outlier (it is neither the revenue-minus-operating-income figure nor the canonical
   band; at $11.4B / ~10.3M subs the per-sub revenue is ~$1,107 and the cost at 38.6% op
   margin is ~$680, so ~$700-850 reads like a stale or mis-transcribed figure). The
   downstream docs and the ledger all use ~$480-680, so nothing downstream is wrong, but
   the source doc's own summary contradicts itself. Recommend the lead reconcile Summary
   point 1 to the canonical ~$480-680/sub/yr all-in (with the ~$480-490 figure retained
   only where it is explicitly the 38%-margin-at-$790-ARPU point, as Section 5.1 and the
   cost-ratio doc Section 5.1 already frame it). Material because it is the doc's single
   most load-bearing number stated inconsistently in its own summary; not a blocker
   because every consumer of the number already uses the correct band.

### Minor

2. **Prefer the structured "~$45-60B to ~$110-150B" band over the "~$45-150B" shorthand**
   in the cost-ratio doc Summary and Sources line (Section 1.1 above).

3. **The mobile ~$0.50-1.50/GB [FACT] tag is generous for a single-source figure**
   (margins doc internal COMM-096); the prose and Confidence already flag it single-
   source, and the ledger records it as `sourced_estimate` (COMM-095). Optional: soften
   the inline tag to match. Do not quote the figure as a settled fact (Section 3.2).

4. **Be explicit that the ~$200-260/sub/yr space-specific split inherits the single-
   lineage ~$6-8B/yr replacement-capex softness** (Section 3.1). Already tagged
   DERIVED/ESTIMATE and flagged in Confidence; no doc change strictly required, logged so
   the lead knows a load-bearing split rests on a 2024 single-analyst figure.

5. **Update the one residual ~$75-95B mention to the reconciled ~$60-95B** (Section 3.5):
   the cost-ratio doc's Section 7 "Note for the Lead" still states ~$75-95B and references
   the internal id "COMM-083" (global ledger id COMM-070). It is the note that prompted the
   fix, now stale because the fix is applied everywhere else (SOURCE_INDEX, the thesis, and
   both wave-2 sizing docs already read ~$60-95B). Source-doc edit, so logged for the lead
   rather than applied here. Cosmetic consistency only; no conclusion in any doc depends on
   it.

---

## What this report does not do

- It does not modify the three source docs or the thesis. The material and minor items
  above are recommendations for the lead, who reviews before committing.
- It does not re-fetch or re-verify the external (http) sources; it checks internal
  repository links, cross-doc number consistency, tag discipline, and the thesis-append
  integrity, the same scope as the wave-1 and wave-2 lint reports.
- It does not render a verdict on the comms business, and it does not re-open the wave-3
  docs' own conclusions: the two-flavor asymmetry, the ~$480-680/sub/yr Starlink-actual
  cost level, and the marginal-cost floor stand as written. The ratio is a cost-and-
  competitive base; the entrant-specific (non-Starlink) cost stack remains the open gate
  the thesis Revision 3 names.
