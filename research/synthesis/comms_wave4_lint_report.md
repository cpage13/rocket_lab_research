# Communications Wave 4 Lint Report

**Date:** 2026-06-18
**Scope:** the seven wave-4 source docs, the wave-4 framework synthesis, and the
appended thesis Revision 4.
**Mode:** read-only on the source docs. This report records findings and a
prioritized fix list; it does NOT modify the source docs, the catalogs
(LIBRARY, RESEARCH_TRACKER, SOURCE_INDEX), or the thesis. The catalog and ledger
edits are applied separately as part of the wave-4 ingest by the lead.

Docs reviewed:

- [direct_communication/spectrum_generations_and_availability.md](../direct_communication/spectrum_generations_and_availability.md) (NEW; internal claims-ledger 1..28)
- [economics/comms_4g_5g_transition_cost.md](../economics/comms_4g_5g_transition_cost.md) (NEW; internal claims-ledger 1..29)
- [economics/comms_6g_demand_value.md](../economics/comms_6g_demand_value.md) (NEW; internal claims-ledger 1..15)
- [competitors/starlink_v3_specs.md](../competitors/starlink_v3_specs.md) (NEW; internal claims-ledger 1..24)
- [economics/comms_direct_to_cell.md](../economics/comms_direct_to_cell.md) (NEW; internal claims-ledger 1..25)
- [rocket_lab/neutron/neutron_comms_payload_fit.md](../rocket_lab/neutron/neutron_comms_payload_fit.md) (NEW; internal claims-ledger 1..22)
- [laser_comms/laser_dc_interconnect_viability.md](../laser_comms/laser_dc_interconnect_viability.md) (NEW; internal claims-ledger 1..15)
- [synthesis/comms_framework_synthesis.md](comms_framework_synthesis.md) (NEW framework synthesis; internal claims-ledger 1..13)
- [vision/comms_thesis.md](../vision/comms_thesis.md) (MODIFIED; Revision 4 appended)

The catalog step ingests these into the global ledger continuing AFTER the
current highest global row, COMM-103 (see the numbering note in Section 7 below
for why the start id is COMM-104 and not COMM-118, despite COMM-104..COMM-117
strings appearing inside the wave-3 ledger notes).

---

## Verdict

The wave-4 set is strong and unusually well-disciplined. It is a framework wave,
not a new-primary-data wave: the framework synthesis and thesis Revision 4
assemble the wave-1-to-4 numbers into a model shape (the comms analogue of the
data-center conclusion's method) and the seven source docs supply the new inputs
(spectrum generations and SCS access, the 4G-to-5G transition cost "X", the 6G
no-premium demand read, the Starlink V3 capacity benchmark, the direct-to-cell
market and physics, the Neutron comms-payload fit, and the laser DC-interconnect
side track). Tag discipline is excellent (every hard number carries
[FACT]/[FACT, single-source]/[ESTIMATE]/[DERIVED], and single-source figures are
flagged inline, in the claims tables, and in the Confidence sections). China is
excluded from every market total with a labelled aside, as required. No em-dashes
appear in any wave-4 doc. Cross-doc number consistency with the wave-1-to-3 base
is high: the ~$480-680/sub/yr space cost, the ~$84-180/sub/yr marginal floor, the
two-flavor ratio, the ~$45-150B addressable pool, the ~$129B served slice, the
1.5x revenue multiple, the ~5-year replacement treadmill, and the ~450 Tbps / ~12M
subscriber Starlink anchors all carry forward unchanged.

**No blockers. Zero broken internal links** (192 internal relative .md links
across the eight docs were resolved; all resolve, including the framework's and
thesis Revision 4's link to `data_center/conclusion.md`, which exists). The thesis
Revision 4 is purely additive (Revisions 1 to 3 are untouched; a Revision 4
section and a Revision 4 history-table row were added).

The findings below are wording, single-source-tag, and intra-wave cross-doc
consistency notes. **One is material**: a genuine numeric contradiction between two
wave-4 docs on the AST BlueBird Block 2 antenna-array area (~90-100 m^2 in the
direct-to-cell doc versus ~223 m^2 in the Neutron-fit doc), where both cite the
same AST source and the same "~2,400 sq ft". The Neutron-fit value (~223 m^2) is
the correct one; the direct-to-cell figure should be reconciled. The rest are
minor. None blocks the catalog or the ledger. No verdict on the comms business is
implied or required.

A note on sequencing and scope: per the wave-4 ingest instruction, this report
catalogs ONLY wave-4 material. Three pre-existing, lead-owned items are visible
from here and are listed in Section 6 (the 75-to-95B versus 60-to-95B stale-number
propagation, the routing/catalog updates, and the three orphaned wave-1/2/3 lint
reports). They are NOT wave-4 defects and are NOT addressed here.

---

## 1. Consistency of the wave-4 numbers with the wave-1/2/3 base and with each other

**The cross-doc chain is consistent.** The load-bearing numbers were checked across
the seven source docs, the framework synthesis, and the wave-1-to-3 base:

- **Space all-in ~$480-680/sub/yr** and **space-specific ~$200-260/sub/yr** are
  carried (not re-derived) by the framework synthesis (Section 1.1) and the
  direct-to-cell doc, citing the wave-3 cost-ratio and supply-cost docs (global
  COMM-091, COMM-100, COMM-103). Same values throughout.
- **The incumbent marginal floor ~$84-180/sub/yr (~10-20% of ARPU)** is carried by
  the framework synthesis (Section 1.1, Section 2.3) consistent with wave-3
  COMM-096.
- **Both flavor ratios** (a: ~1.3-3.2x rural, ~65-90x tail; b: ~3-8x served) are
  carried by the framework synthesis (Section 2.3) and the thesis Revision 4,
  consistent with wave-3 COMM-100 and COMM-101.
- **The addressable pool ~$45-150B** and the **near-term D2C served revenue
  ~$12-14B ex-China** are consistent between the direct-to-cell doc and the
  framework synthesis; the ~$129B Morningstar served slice is carried unchanged.
- **The 1.5x revenue multiple / ~30% regular margin** is stated identically in the
  framework synthesis (Section 2.2), the thesis Revision 4, and the standing
  project rule (revenue minus the full per-subscriber cost, not gross profit), and
  is correctly noted as conservative against Starlink's disclosed ~38.6% operating
  margin (which implies ~1.6x).
- **The Starlink fleet anchors** (~450 Tbps aggregate end-2025, ~9,500 operational
  satellites of ~10,700 in orbit / ~12,300 launched, ~5-year replacement) are
  consistent between the V3-specs doc and wave-3 COMM-082 and COMM-088.
- **The EchoStar ~$17B / ~65 MHz deal** and the **AST ~45 MHz Ligado deal** are
  consistent across the spectrum doc, the V3-specs doc, and the direct-to-cell doc.
- **The 5G ground capex ~$1.5T** (GSMA) cross-check is consistent between the
  4G-to-5G doc (claim 22, ~$830B+ global 5G inside ~$1.1T) and the 6G doc (claim
  15) and the existing wave-1 COMM-025.

**1.1 (minor) Starlink subscriber metrics: total-broadband vs D2C-via-T-Mobile must
not be conflated.** Two different ~10-16M figures appear, correctly, for two
different things, but a cold reader could merge them:

- The V3-specs doc: "~12M+ active Starlink subscribers across 160+ countries (June
  2026)" (claim 17), which is TOTAL Starlink broadband.
- The direct-to-cell doc: "Starlink D2C US subscribers 16M unique / 10M monthly
  active (Mar 2026), targeting 25M end-2026" (claim 13), which is the
  T-Mobile-hosted DIRECT-TO-CELL base, a different product on a different date.

Both are individually sourced and individually correct; they are not in conflict.
The note for the ledger and any downstream cite: keep the "~12M total broadband"
and the "16M unique / 10M MAU D2C" figures explicitly labelled so they are never
summed or swapped. Minor; both docs already label them in context.

**1.2 (minor) Starlink D2C satellite count differs by date across two wave-4 docs.**
The V3-specs doc references the wave-3 fleet ("~9,500 operational, all gens") and a
"15,000-satellite dedicated D2C fleet" filing; the direct-to-cell doc says "650+
D2C satellites by early 2026." These are not in conflict (650+ is the count of
satellites carrying a D2C payload in early 2026; 15,000 is the separate FCC filing
ceiling; 9,500 is the all-gen operational fleet), but the three numbers sit close
enough in the same wave that the ledger note should state which is which. Minor.

---

## 2. The one material contradiction between wave-4 docs (AST Block 2 array area)

**2.1 (material) The AST BlueBird Block 2 antenna-array area is stated as two
different numbers in two wave-4 docs, both citing AST and both citing "~2,400 sq
ft".** This is a genuine numeric contradiction, not a framing difference.

- The direct-to-cell doc states the smaller value, in two places:
  > "Block 2 ~90-100 m^2 (~2,400 sq ft)" (Section 1.1 architecture table) and
  > "Block 2 ~90-100 m^2 (~2,400 sq ft, ~3x larger, ~10x data capacity)" (claim 7).
- The Neutron-fit doc states the larger value:
  > "Antenna array area ~223 m^2 ('nearly 2,400 sq ft'), largest commercial array
  > in LEO" (Section 1b table) and claim 11 ("~223 m^2 ('nearly 2,400 sq ft')").

Both cannot be right: 2,400 sq ft = ~223 m^2, not ~90-100 m^2. The ~223 m^2 figure
is the correct deployed-aperture area (it matches "2,400 sq ft" arithmetically, it
matches the Wikipedia/SpaceNews/AST lineage the Neutron-fit doc cites, and it is the
"largest commercial array in LEO" the press uniformly reports). The direct-to-cell
doc's "~90-100 m^2" appears to be an error: ~90-100 m^2 is roughly 970-1,076 sq ft,
which contradicts the "~2,400 sq ft" printed right beside it in the same cell. It
is possible the ~90-100 m^2 was meant as a different quantity (for example an
active-aperture or per-panel sub-area), but as written it is labelled "array size"
and paired with "~2,400 sq ft", so it reads as a direct contradiction of the
Neutron-fit doc.

**Which to adopt:** adopt **~223 m^2** (the Neutron-fit doc's value) as the Block 2
deployed-array area. Recommend the lead correct the direct-to-cell doc's Section 1.1
table and its claim 7 from "~90-100 m^2" to "~223 m^2" (keeping "~2,400 sq ft" and
the "~3x larger / ~10x capacity vs Block 1" framing, which are consistent with
~223 m^2 against Block 1's ~64 m^2). Note this does not change any downstream
conclusion in the direct-to-cell doc (its capacity, $/GB, and cannibalization
findings do not depend on the array area in m^2), so it is a source-accuracy fix,
not a logic error. The ledger should carry the Block 2 array area as ~223 m^2 with
the direct-to-cell doc's ~90-100 m^2 flagged as the figure to correct.

**2.2 (minor) AST MNO reach: ~2.8B vs ~3B (a carried wave-1 vintage gap, surfaced
again).** The direct-to-cell doc itself flags this:
> "~45-60 operators, ~3 billion (prior doc: 2.8B) subscribers" (Section 1.2 table,
> claim references the prior `comms_us_cellular_market.md`).

This is not a new wave-4 inconsistency; it is the wave-1 figure (~2.8B) being
updated to the AST Q1-2026 figure (~3B) and honestly noting the delta. No action
beyond quoting a single dated value (~3B per AST Q1 2026) going forward; the
direct-to-cell doc already handles it correctly.

---

## 3. Intra-wave cross-doc number reconciliations (minor, all already internally honest)

These are places where two wave-4 docs state nominally different numbers for the
same quantity, each defensible, that a downstream reader should see reconciled.

**3.1 (minor) The FR3 / 6G candidate study bands differ between the spectrum doc and
the 6G doc.** Both cite WRC-23 study items for WRC-27 identification, but list
slightly different bands:

- The spectrum doc: "**4.4 to 4.8, 7.125 to 8.4, and 14.8 to 15.35 GHz** as IMT
  study bands for identification at WRC-27" (Summary, Section 3.2, claim references
  COMM-13/14 in the doc's internal numbering).
- The 6G doc: "**7.125-8.4, 12.7-13.25, 14.8-15.35 GHz**" (Section 1.2 table, claim
  4).

The overlap (7.125-8.4 and 14.8-15.35 GHz) is identical; the difference is the
spectrum doc lists 4.4-4.8 GHz while the 6G doc lists 12.7-13.25 GHz. Both are real
candidate bands in the WRC-23/WRC-27 6G study set (the full set under study spans
4.4-4.8, 7.125-8.4, 12.7-13.25, and 14.8-15.35 GHz), so neither doc is wrong; each
listed a representative subset. The framework synthesis (Section 4.4) carries the
spectrum doc's "4.4-4.8, 7.125-8.4, 14.8-15.35 GHz" subset. Recommend the ledger
note the union of the candidate bands so a reader does not treat the two subsets as
contradictory; the load-bearing point (7-15 GHz upper mid-band, >400 MHz/operator,
identification at WRC-27) is identical in both. Minor.

**3.2 (minor) D2C delivery cost stated as "~$5-9/GB" and refined "~$5-6/GB", and as
"~17-30x" and "~20x".** The direct-to-cell doc gives "~$5-9/GB vs ~$0.30/GB,
roughly 20x" (Section 3.2, claim 18, single named analyst Joe Madden), and the
framework synthesis gives "~$5-9/GB (refined ~$5-6/GB) versus terrestrial 5G
~$0.20-0.30/GB, ~17-30x higher" (Section 1.2, claim 2). The framework's "refined
~$5-6/GB" and "~17-30x" come from a second Madden article ("price per gigabyte in
space") that the framework cites directly. These are consistent (the same analyst,
two articles, the range is the envelope across both), but the headline ratio is
quoted three ways across the two docs (20x, 17-30x). Prefer the structured
"~$5-9/GB vs ~$0.20-0.30/GB, ~17-30x" in the ledger, and note the figure rests on a
SINGLE named analyst (corroborated in direction by every capacity source, but not a
multi-analyst number). Already flagged single-source in both docs; the [FACT] tag is
slightly generous for a single-analyst figure (see Section 4.1). Minor.

**3.3 (minor) EchoStar deal date framing (announcement vs FCC approval).** The
spectrum doc and V3-specs doc frame the ~$17B EchoStar AWS-4/H-block deal as
"announced Sept 2025" with FCC approval "May 12, 2026"; the direct-to-cell doc's
table writes "~$17B ... (May 2026)" and "Approved May 12, 2026; license transfer
~Nov 30, 2027". The "(May 2026)" parenthetical in the direct-to-cell table could
read as the deal date rather than the approval date. All three docs agree on the
substance (announced Sept 2025, FCC-approved 12 May 2026, ~$17B, ~65 MHz). Recommend
the ledger record the dual date (announced Sept 2025 / approved May 2026) so the
"(May 2026)" shorthand is not mis-cited as the announcement. Minor.

**3.4 (minor) V3 mass: the wave-4 docs use three values, each flagged.** The
V3-specs doc carries "~1,900-2,000 kg (trade press) vs ~1,200 kg (catalog), ~3.3x a
V2 mini" (claim 6), the cost doc (wave 3) used ~1,500 kg as a midpoint, and the
Neutron-fit doc adopts "~1,900 kg working figure" (claim 1, explicitly treating the
Gunter's ~1,200 kg entry as stale for the full-size V3). This is consistent and
honest: every doc flags the spread, and the Neutron-fit doc states why it uses
~1,900 kg (the ~1,200 kg catalog entry predates the disclosed full-size V3). The
~1,900 kg working figure does not contradict the V3-specs doc's range; it is the
upper-cluster point within it. Note for the ledger: carry the V3 mass as a
~1,200-2,000 kg range with ~1,900 kg as the working point, both flagged. No action.

---

## 4. FACT-tagged numbers that are actually single-source

The wave-4 docs are disciplined about flagging single-source figures. The items
below are the ones a reader must not lift as hard multi-source facts; each is
already flagged in its source doc, and each should be carried with that flag into
the ledger.

**4.1 (minor) The D2C ~$5-9/GB delivery cost is a single named analyst.** Both the
direct-to-cell doc (claim 18) and the framework synthesis (claim 2) tag the
~$5-9/GB (and ~$0.20-0.30/GB terrestrial) [FACT], while their own inline text and
Confidence sections correctly state it is one named analyst (Joe Madden / Mobile
Experts), across two Fierce articles, corroborated only in DIRECTION by the other
capacity sources (WIA, Opensignal, Morningstar). This is the load-bearing $/GB
number for the lead market, and it propagates into the framework's per-GB unit, so
its single-analyst provenance matters. The [FACT] tag is slightly generous; the
ledger should record it as `sourced_estimate` with an explicit single-source flag.
The DIRECTION (satellite $/GB structurally far above terrestrial, rising with
density) is robust; the precise ~$5-9/GB and the ~17-30x multiple are soft.

**4.2 (minor) The AST narrowest-beam footprint (~20.3 km / ~324 km^2) and the
2,800-cell figure are single-source.** The direct-to-cell doc flags both (claims 4
and 3): the ~20.3 km beam footprint rests on one arXiv paper (2506.18672), and the
2,800-cell count on one analyst (Madden) above AST's own "~2,000+ / ~2,500" figures.
Correctly flagged single-source in the doc; the ledger should preserve the flag.

**4.3 (minor) The Starlink D2C per-beam throughput (~3.1 / ~6.2 / ~18.6 Mbps) is a
single technical lineage.** The direct-to-cell doc (claim 9) and the spectrum doc
(measured-per-beam table) both rest on one crowdsourced-measurement arXiv paper
(2506.00283). It is the cleanest measured D2C number available and is load-bearing
for the spectrum-to-capacity bridge, but it is single-lineage; the ledger should
carry the flag. The spectrum doc's own area-capacity ratios (~300x to ~30,000x) are
[DERIVED] from it and are correctly tagged order-of-magnitude.

**4.4 (minor) The 5 Pbit/s and 1 Pbit/s AI-DCI bandwidth figures (laser DC doc) rest
on SemiAnalysis.** The laser-DC doc flags this (claim 4, and the Confidence section):
the petabit campus-to-campus and inter-region requirements, and the Google
paired-campus distances, are single-source (SemiAnalysis). The bandwidth-scale
DISQUALIFICATION conclusion (FSO is two-to-five orders of magnitude short) is
arithmetic and robust regardless, but the specific petabit inputs are single-source.
Correctly flagged. Likewise the "504x" Cisco AI-traffic figure and the
tri-versity/quad-versity language rest on Big Fiber via Data Center Knowledge
(claim 3), and the NVIDIA Spectrum-XGS "~1.9x" on NVIDIA (claim 12); all flagged.

**4.5 (minor) The BlueBird Block 2 build cost (~$19-21M/sat) is a single-source
cluster.** The Neutron-fit doc flags it [FACT, single-source cluster] (claim 17,
AST disclosures via Wikipedia / investor commentary). Correctly flagged; the ledger
should keep the single-source-cluster note and treat it as order-of-magnitude.

**4.6 (minor) Several 6G demand figures are single-dataset-via-two-outlets.** The 6G
doc tags the Deloitte 54%/56%/priority-rank figures and the PwC "fewer than half
could define 5G" / 26% device-pull figures as [FACT, single dataset reported via two
outlets] (claims 9, 10), and the energy-efficiency 100x target and the specific
operator quotes as [FACT, single-source] (claims 3, 14), and the 6G-cycle capex
magnitude as [ESTIMATE, single-source] (claim 15). All correctly flagged. The
load-bearing demand conclusion (no consumer premium for a new G) is multi-lens
(McKinsey + PwC + Deloitte + Ericsson + Telecoms.com + Statista) and robust; the
individual perception statistics are single-dataset.

---

## 5. Stale claims, orphans, and broken links (wave-4 scope)

**5.1 Broken links: NONE.** All 192 internal relative .md links across the eight
wave-4 docs resolve to existing files, including:

- the spectrum doc's `spectrum_fundamentals_economics.md` and
  `bands_and_enabling_hardware.md` and `../laser_comms/rf_limited_service.md`
  cross-references;
- the 4G-to-5G and 6G docs' `comms_cellular_5g_deployment_economics.md` and
  `../synthesis/comms_baseline_synthesis.md` cross-references;
- the V3-specs doc's `../economics/comms_space_supply_cost.md`,
  `../laser_comms/rf_satcom.md`, `../laser_comms/constellation_mesh.md`,
  `starship_addendum.md`, and `../orbital/higher_orbit_tradeoffs_lifetime.md`
  cross-references;
- the direct-to-cell doc's `./comms_us_cellular_market.md`,
  `./comms_space_tam_claims.md`, and `./comms_ground_vs_space_cost_ratio.md`
  cross-references;
- the Neutron-fit doc's grounding-doc cross-references;
- the laser-DC doc's `laser_terrestrial_interconnect.md`, `optical_comms.md`,
  `optical_ground_stations.md`, and `comms_business_case.md` cross-references;
- the framework synthesis's and thesis Revision 4's links to all seven source docs,
  to `comms_baseline_synthesis.md`, to `../economics/comms_addressable_sizing.md`,
  to `../vision/comms_thesis.md`, and to `../../data_center/conclusion.md` (which
  exists at `data_center/conclusion.md`).

(External http sources were not fetched; this check covers internal repository links
only, consistent with the wave-1/2/3 lint reports.)

**5.2 No stale claims INTRODUCED by wave 4.** The wave-4 docs correctly mark prior
material they supersede or update rather than restating it as current:

- The direct-to-cell doc explicitly updates the wave-1/2 framing "they use MNO
  partner licensed spectrum, not their own" to the 2025-26 hybrid (own + leased
  dedicated spectrum), stating the prior framing "was true in 2024-25 and is still
  partly true" (Section 2). This is a correct supersession note, not a stale claim.
- The Neutron-fit doc explicitly treats the Gunter's "~1,200 kg?" V3 entry as stale
  for the full-size V3 and says why (claim 1, Section 1a). Correct.
- The spectrum doc notes US carriers have "sunset" DSS, correctly describing it as a
  bridge that was superseded, not a current practice (Section 2.2). Correct.

**5.3 Orphans (wave-4 internal): NONE that wave 4 introduces.** Every wave-4 source
doc is referenced by the framework synthesis and by thesis Revision 4, so none is an
orphan. The framework synthesis and thesis Revision 4 are themselves the entry
points the catalog will link from LIBRARY and RESEARCH_TRACKER. The one orphan-shaped
observation that touches wave 4: the wave-4 lint report (this file) will itself be an
orphan unless the catalog links it, exactly as the three prior wave lint reports are
currently orphaned (Section 6.3, lead-owned).

---

## 6. Pre-existing, lead-owned items visible from here (NOT wave-4 defects, listed and left)

Per the wave-4 ingest scope, these are NOT addressed in this pass. They are a
separate batch the lead owns. Listed so they are not lost, then left alone.

**6.1 The 75-to-95B versus 60-to-95B stale-number propagation (lead-owned).** The
premium/sovereign gross-pool figure was lead-reconciled from ~$75-95B to ~$60-95B in
wave 3, applied in SOURCE_INDEX COMM-070, thesis Revisions 2 and 3, and both wave-2
sizing docs, with residual ~$75-95B mentions still surviving in the wave-3
cost-ratio doc's Section 7 note and in several non-comms and tracker locations
(`research/RESEARCH_TRACKER.md`, `research/peer_review/`, others). This is the
wave-2/wave-3 carry the wave-3 lint report already logged. **No wave-4 doc contains
"75-95B"** (verified), so this is entirely out of wave-4 scope and is not touched
here.

**6.2 Routing / catalog updates (lead-owned).** The LIBRARY and RESEARCH_TRACKER
"how to read the comms workstream" routing pointers currently route to the wave-1
baseline synthesis and the Revision-1 thesis framing. Wave 4 adds the framework
synthesis as the natural new top-of-funnel for the comms track and advances the
thesis to Revision 4, so the routing pointers will want updating when the catalogs
are reconciled. That catalog reconciliation is the lead's step (the standing rule is
that this lint pass does not touch LIBRARY/RESEARCH_TRACKER/SOURCE_INDEX); it is
noted here only so the routing refresh is on the list.

**6.3 The three orphaned wave-1/2/3 lint reports (lead-owned).** `comms_wave1_lint_report.md`,
`comms_wave2_lint_report.md`, and `comms_wave3_lint_report.md` are NOT referenced in
LIBRARY, RESEARCH_TRACKER, SOURCE_INDEX, or README (verified). They are orphaned
artifacts. This wave-4 lint report will join them as a fourth orphan unless the
catalog links the set. Whether to catalog the lint reports (for example a
"Synthesis / lint reports" sub-list in LIBRARY) is a lead decision; it is a
pre-existing condition, not a wave-4 defect, and is left for the same batch.

---

## 7. Claims-ledger numbering note (the COMM-104 start, and the COMM-108 anomaly)

**7.1 The global ledger currently ends at COMM-103; wave 4 begins at COMM-104.** The
global SOURCE_INDEX has exactly 103 distinct `COMM-` table ROWS, the highest being
COMM-103 (verified by counting table-row ids, not note text). Waves 1-3 occupy
global COMM-001..COMM-103 (wave 1: COMM-001..056; wave 2: COMM-057..079; wave 3:
COMM-080..103). So the wave-4 ingest assigns global ids continuing at **COMM-104**,
exactly as the ingest instruction states.

**7.2 The COMM-104..COMM-117 strings inside the wave-3 ledger are NOT global rows;
do not let them push the start id.** A naive `grep` for `COMM-1xx` in SOURCE_INDEX
returns COMM-104 through COMM-117, which could be misread as "the ledger already goes
to COMM-117, start wave 4 at COMM-118." It does not. Those strings appear only inside
the NOTE column of the wave-3 rows, where they record each source doc's OWN internal
claim numbers (for example global COMM-090's note reads "Internal claims COMM-101,
COMM-102, COMM-103, COMM-104"), and the wave-3 cost-ratio doc's internal COMM-109..117
which were remapped to global COMM-100..103. The wave-3 ledger header itself states
the mapping: "the space supply-cost doc ran internal COMM-080..108 ... the cost-ratio
doc ran internal COMM-109..117 ... This section assigns one continuous global range,
COMM-080..103." So the correct global start for wave 4 is **COMM-104**, and any
process that keyed off the raw `COMM-1xx` strings would wrongly start at COMM-118 and
leave a 14-id gap. Flagged so the catalog step keys off ROW ids, not note text.

**7.3 The "COMM-108" header anomaly the ingest instruction warned about (do not fix,
just note).** Two related cosmetic artifacts carry the COMM-108 string:

- The SOURCE_INDEX wave-1 header (line ~192) still reads "this section assigns one
  global, non-colliding `COMM-` namespace (`COMM-001` .. `COMM-108`)", an OUTDATED
  upper bound (wave 1 actually occupies COMM-001..056; the "..COMM-108" was a stale
  early-draft ceiling). It is a header-text artifact, not a real COMM-108 row.
- The space supply-cost doc's own internal claims table has a row literally numbered
  "COMM-108" (its internal beam-density claim), which global COMM-092's note cites as
  "Internal claims COMM-108". This is the doc's internal numbering, correctly
  remapped, not a stray global row.

Neither is a real global COMM-108 row, and per the ingest instruction neither is
fixed here and neither blocks the wave-4 numbering. They are logged for visibility as
the "stray/cosmetic COMM- header anomaly" the instruction anticipated. (The stale
"..COMM-108" header ceiling is a one-line lead cleanup if desired, in the same batch
as Section 6; it is cosmetic and changes no row.)

**7.4 Recommended contiguous global allocation for the wave-4 docs.** Each wave-4
doc ends with a curated "## Claims ledger" numbered hard-claim list. The counts are:

| Doc | Claims-ledger items | Recommended global range |
|---|---|---|
| spectrum_generations_and_availability.md | 28 | COMM-104..COMM-131 |
| comms_4g_5g_transition_cost.md | 29 | COMM-132..COMM-160 |
| comms_6g_demand_value.md | 15 | COMM-161..COMM-175 |
| starlink_v3_specs.md | 24 | COMM-176..COMM-199 |
| comms_direct_to_cell.md | 25 | COMM-200..COMM-224 |
| neutron_comms_payload_fit.md | 22 | COMM-225..COMM-246 |
| laser_dc_interconnect_viability.md | 15 | COMM-247..COMM-261 |
| comms_framework_synthesis.md | 13 | COMM-262..COMM-274 |

That is 171 items, global **COMM-104..COMM-274**, contiguous, no collision with
COMM-001..COMM-103. This is a one-id-per-ledger-item allocation; the catalog step may
choose (as waves 1-3 did) to fold a doc's purely cross-referential or
already-held-elsewhere items into a single `long-tail` row rather than minting a new
id, which would shorten the range. Two specific fold candidates:

- The **framework synthesis** claims are largely carried, not new: it states itself
  that the ~$480-680/sub/yr cost, the two-flavor ratio, the addressable pool, and
  the ARPU-premium-absence "should be reconciled to their existing COMM- ids rather
  than duplicated", and only ~13 framework-level claims are genuinely new. Several of
  its 13 ledger items (for example its restatements of the D2C $/GB, the V3 capacity,
  the Neutron fit, the X shape, the 6G demand) point at the source docs' claims by
  internal number and should map to whatever global ids those source-doc claims
  receive above, not to fresh ids. The genuinely new framework-level claims (the
  density-aware unit, the forked forward comparison, the 1.5x-conservative note, the
  side-track treatment) are the ones that warrant their own ids.
- The **Neutron-fit** and **V3-specs** docs share several V3 facts (mass, 1 Tbps,
  60/Starship, Starship-only); the catalog should mint the id once (on the V3-specs
  doc, which owns the capacity-and-physics stack) and have the Neutron-fit doc's
  duplicates reference it, exactly as the V3-specs doc already cross-references the
  cost doc for the per-Gbps cost.

The reading-guide tag mapping is unchanged from waves 1-3: doc [FACT] maps to
`certified` for a primary filing or official body (FCC, ITU, 3GPP, SEC, GSMA, a
vendor datasheet) and to `sourced_estimate` for a market-research or trade-press
sizing; doc [FACT, single-source] maps to `sourced_estimate` with a single-source
flag; doc [ESTIMATE] maps to `sourced_estimate` or `derived_estimate`; doc [DERIVED]
maps to `derived_estimate`. Every wave-4 figure is communications-track research
context, not a data-center model input, unless a future cycle promotes it.

---

## 8. Thesis Revision 4 appended without altering Revisions 1 to 3 (confirmed)

**Revision 4 is purely additive.** The new `## Revision 4` section sits after
Revision 3 and before the `## Revision history` table, and a `Revision 4` row was
added to that table. The section order is Revision 1 (top) to Revision 2 to Revision
3 to Revision 4 to Revision history, unchanged except for the append.

**Revisions 1, 2, and 3 are untouched.** No line in the Revision 1, Revision 2, or
Revision 3 bodies changed (including the wave-3 lead-reconciled ~$60-95B figures in
Revision 2 and Revision 3, which remain as wave 3 left them). The only edit beyond
the append is the new Revision 4 history-table row.

**Revision 4 is correctly scoped.** It records four working hypotheses (the framework
shape as new Hypothesis 5; the forward-comparison framing sharpening Hypothesis 2;
the direct-to-cell reframe sharpening the product question; spectrum-as-moat
sharpening Hypothesis 2's capacity input), names the forced-6G catalyst, and renders
NO verdict. It states three times that the framework is a structure not a populated
model and that the entrant-specific cost per subscriber remains the open gate
(consistent with the framework synthesis and the wave-3 thesis). It explicitly does
not change Hypothesis 3 on the consumer side and adds the laser DC-interconnect as a
separate non-consumer side track. This is the correct and consistent place for the
framework to land.

---

## 9. Cold-reader gaps (small; what a first-time reader of the wave-4 set would trip on)

These are not errors; they are places where a reader arriving cold (without the
wave-1-to-3 base in memory) could be briefly misled. Each is a candidate for a
one-line clarification the lead may or may not want.

1. **"Direct-to-cell is the lead market" lands before the reader has the wave-1/2
   context that fixed broadband is the larger CURRENT market.** The framework
   synthesis and thesis Revision 4 both open the per-market section by asserting D2C
   is the lead, then later note it is ~10x smaller than fixed broadband on near-term
   served revenue and is "the lead" on optionality/non-substitutability, not on
   current dollars. A cold reader could take "lead market" as "biggest market." Both
   docs do resolve it (the direct-to-cell doc's Section 5.2 decomposes "larger" by
   axis), but the resolution comes after the assertion. A one-line "lead by
   optionality and non-substitutability, not by current revenue" at first use would
   close the gap. Minor.

2. **The two ARPU anchors (~$66-92/mo Starlink blended vs ~$10/mo D2C retail) are
   both labelled "ARPU" and could be conflated.** The framework synthesis Section 1.1
   lists both in the same table; they are different products (broadband dish vs
   direct-to-cell phone add-on) with a ~7-9x ARPU gap. Already labelled, but the gap
   is large enough that a downstream cite could grab the wrong one. Minor.

3. **The "~$480-680/sub/yr closes the addressable pool" claim needs its scale caveat
   travelling with it.** Several wave-4 places (framework Section 1.1, thesis Revision
   4) restate that the ~$480-680/sub/yr level is "Starlink's disclosed actual" without
   immediately repeating "and unreachable for a small constellation (denominator-
   driven)." Both docs do carry the caveat nearby, and it is the central open gate, so
   the risk is only that a partial quote drops it. The ledger note on the relevant
   carried ids (global COMM-091, COMM-103) already states the scale caveat; keep it
   attached. Minor.

4. **The laser DC-interconnect doc is a side track and says so, but its strong AI-DCI
   demand framing could be mis-read as a comms-revenue opportunity for the project.**
   The doc is careful (the terrestrial market is a "narrow supplement", the orbital
   case is "the primary architecture" and "the strategically relevant one"), and the
   framework synthesis Section 3.3 reinforces that it is out of the RF consumer spine.
   The cold-reader risk is small but real: a reader skimming Section 1's "$250M
   dark-fiber land rush, AI-DCI is a first-order problem" could think the project
   should chase terrestrial laser DCI, which the doc explicitly disqualifies on
   bandwidth. The doc's own Summary closes this; no action needed beyond keeping the
   side-track label prominent in the catalog entry. Minor.

---

## 10. Prioritized fix list

The lead reviews before committing. This report does not apply any of these; the
catalog and ledger edits are applied separately.

### Blocker

None.

### Material

1. **Reconcile the AST Block 2 antenna-array area to ~223 m^2 in the direct-to-cell
   doc (source-doc edit, lead's call).** The direct-to-cell doc states "~90-100 m^2
   (~2,400 sq ft)" in its Section 1.1 table and claim 7, contradicting the Neutron-fit
   doc's "~223 m^2 ('nearly 2,400 sq ft')" (Section 1b, claim 11) and contradicting the
   "~2,400 sq ft" printed beside it (2,400 sq ft = ~223 m^2, not ~90-100 m^2). Adopt
   ~223 m^2. Recommend the lead correct the direct-to-cell doc's "~90-100 m^2" to
   "~223 m^2" (keeping "~2,400 sq ft" and the "~3x larger / ~10x capacity vs Block 1"
   framing), and the ledger record the Block 2 array area as ~223 m^2. Material because
   it is a direct numeric contradiction between two wave-4 docs on a named spec; not a
   blocker because no downstream conclusion in either doc depends on the array area in
   m^2 (Section 2.1).

### Minor

2. **Carry the D2C ~$5-9/GB as `sourced_estimate` with a single-source flag, not as a
   settled multi-source FACT** (Section 4.1). One named analyst across two articles;
   the direction is robust, the precise figure and the ~17-30x multiple are soft. Both
   the direct-to-cell doc and the framework synthesis tag it [FACT]; prefer the
   single-source flag in the ledger and do not quote ~$5-9/GB as settled.

3. **Note the union of the FR3 / 6G candidate bands** (Section 3.1): the spectrum doc
   lists 4.4-4.8 / 7.125-8.4 / 14.8-15.35 GHz and the 6G doc lists 7.125-8.4 /
   12.7-13.25 / 14.8-15.35 GHz; both are correct subsets of the WRC-23/WRC-27 6G study
   set (union: 4.4-4.8, 7.125-8.4, 12.7-13.25, 14.8-15.35 GHz). Record the union so the
   two subsets are not read as contradictory.

4. **Keep the Starlink subscriber metrics explicitly labelled** (Section 1.1): "~12M+
   total broadband (June 2026)" vs "16M unique / 10M MAU direct-to-cell via T-Mobile
   (Mar 2026)" are different products on different dates; never sum or swap them.

5. **Record the EchoStar deal dual date** (Section 3.3): announced Sept 2025,
   FCC-approved 12 May 2026; the direct-to-cell table's "(May 2026)" shorthand should
   not be mis-cited as the announcement.

6. **Carry the remaining single-source flags into the ledger** (Section 4): the AST
   ~20.3 km beam footprint and 2,800-cell figure (one arXiv / one analyst), the
   Starlink D2C per-beam ~3.1/6.2/18.6 Mbps (one arXiv lineage), the 5 Pbit/s and 1
   Pbit/s AI-DCI figures (SemiAnalysis), the BlueBird Block 2 build cost ~$19-21M
   (single-source cluster), and the 6G single-dataset perception statistics. Each is
   already flagged in its source doc; preserve the flag.

7. **Add a one-line "lead by optionality, not current revenue" qualifier at first use
   of "direct-to-cell is the lead market"** (Section 9.1), so a cold reader does not
   read "lead" as "biggest current market" before the per-axis decomposition resolves
   it. Optional.

8. **Key the catalog numbering off ROW ids, not the COMM-1xx strings in note text**
   (Section 7.2): wave 4 starts at global COMM-104; the COMM-104..117 strings in the
   wave-3 ledger are internal-claim references, not global rows. The stale
   "..COMM-108" header ceiling on the wave-1 section is a cosmetic one-line lead
   cleanup (Section 7.3), not fixed here per instruction.

---

## What this report does not do

- It does not modify the seven source docs, the framework synthesis, or the thesis.
  The material and minor items above are recommendations for the lead, who reviews
  before committing.
- It does not edit the catalogs (LIBRARY, RESEARCH_TRACKER, SOURCE_INDEX) and does
  not assign global COMM- ids; it recommends the COMM-104..COMM-274 allocation
  (Section 7.4) for the catalog step to apply.
- It does not re-fetch or re-verify the external (http) sources; it checks internal
  repository links (all 192 resolve), cross-doc number consistency, tag discipline,
  and the thesis-append integrity, the same scope as the wave-1/2/3 lint reports.
- It does not apply any pre-existing lead-owned batch item (the 75-to-95B versus
  60-to-95B stale-number propagation, the routing/catalog refresh, or the three
  orphaned prior lint reports); those are listed in Section 6 and left for the lead's
  separate batch.
- It does not render a verdict on the comms business, and it does not re-open the
  wave-4 docs' own conclusions: the density-aware cost-per-subscriber unit, the forked
  forward comparison, the direct-to-cell lead-market reframe, the spectrum-as-moat /
  SCS-lease entry path, and the forced-6G catalyst stand as written. The framework is
  a structure, not a populated model; the entrant-specific cost per subscriber, the
  SCS commercial terms, the sustained per-beam throughput, and the competitive share
  remain the open gates Revision 4 names.
