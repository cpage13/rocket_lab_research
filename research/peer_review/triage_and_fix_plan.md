# Triage & Fix Plan — Peer-Review Consolidation

*Triage agent. Date: 2026-05-17. Inputs: `peer_review_1.md` (launch/orbital/comms),
`peer_review_2.md` (AI-hardware/compute/node-design), `peer_review_3.md`
(economics/competitors/models), `peer_review_4.md` (end-documents/consistency).
This document triages and prioritizes — it applies no fixes.*

---

## 1. Overall judgment — NO significant issue was found

**Headline: the peer review found no significant issue.** Across ~30 documents
and four independent reviewers, **nothing invalidates a conclusion, a physics
result, or a load-bearing number.** All four reviewers state this explicitly and
independently:

- PR1: "No physics error, no fabricated source, and no broken/misread citation
  that changes a conclusion." Eight of 13 docs clean.
- PR2: "No invalidating errors found." Engineering arithmetic reproduces correctly
  on spot-check.
- PR3: qualitative conclusions of the affected economics docs "survive a re-base";
  six of 12 docs clean.
- PR4: "`CONCLUSION.md` Rev 7 ... is internally consistent, fully sourced ...
  traceable end-to-end. The verdict and its reasoning hold up."

**Every finding is staleness or hygiene**, not validity. The pattern is uniform:
the project ran eleven waves of founder input and revised the conclusion to Rev 7,
but **upstream framing/index/synthesis documents were frozen at earlier waves and
never caught up.** The most consequential change — the wave-9 launch-cost re-base
from ~$50–55M (external price) to ~$10–20M (internal marginal cost) — was correctly
absorbed by `CONCLUSION.md`, `INVESTOR_PROJECTION.md`, and `ambition_case.md`, but
several documents that pre-date wave 9 still run the old number with no superseded
banner. The physics, the source spot-checks (Neutron payloads, CONDOR Mk3 rate,
GB300 power, McKinsey TAM, CoreWeave/Rocket Lab financials, ISS radiator areas) all
held up. The corpus is fundamentally sound; this is a clean-up pass, not a
correction pass.

**One caveat for the owner:** "no significant issue" means no *error*. It does not
mean "no work" — several stale docs (the thesis, the README, two economics docs,
the data-science REPORT) would actively mislead a reader who lands on them, because
they assert superseded numbers as live. They must be fixed or banner-flagged before
the project can be certified "meticulously correct." See §4 for the items that need
owner judgment rather than a mechanical edit.

---

## 2. Consolidated fix list (deduplicated, prioritized)

Severity: **P1** = consistency-critical, a reader could be actively misled ·
**P2** = hygiene, stale-but-flagged or low-traffic · **P3** = trivial/cosmetic.

Cross-reviewer duplicates have been merged; the "Raised by" column shows which
reviews flagged each item.

### P1 — consistency-critical

| # | File(s) | What is wrong | Correct value / fix | Raised by |
|---|---|---|---|---|
| **F1** | `vision/initial_thesis.md` | Frozen at **Rev 4** (wave-5 vintage); never updated for waves 6–11. Still costs the V1 node at the retired ~$55M launch price, frames economics on the abandoned 2–3-yr GPU window, gives node cost ~$65–120M / V2 ~$75–95M, and defines V2 as **block-upgrade-dependent** — directly contradicting `CONCLUSION.md` Rev 6/7 ("V2 closes on baseline Neutron + hot-loop"). The biggest "dead document" in the project. | Append Rev 5, 6, 7 to bring the thesis level with `CONCLUSION.md`: record the launch-cost re-base, the 5-yr service-life base case, the venture J-curve, the converged build strategy + minimum-viable ~3–5-node deployment, the conservative/ambition dual case, the in-house-radiator decision, and the corrected V2 definition (baseline Neutron + hot-loop). | PR4 S1, S7, D-2…D-5, T-3 |
| **F2** | `README.md` §Status (l.64–70) and "Working thesis" box (l.15–24) | Every count wrong: "27 research docs" (actual 30), "2 simulations" (actual 3 models — M1/M2/M3), "2-round adversarial debate" (actual 3 rounds/side), "conclusion at v2" (actual **v7**). Front-door doc is badly stale; flagged by both lint passes and never fixed. | 30 research docs, 3 models, 3-round debate, conclusion at v7, thesis at Rev 7 (after F1). Add a pointer in the Working-thesis box noting how far the thesis has moved. | PR4 S2, D-1, M-5; PR1 M8 (adjacent) |
| **F3** | `economics/rack_cost_trajectory.md` | **Entire doc runs on the stale $50–55M / $52.5M-midpoint launch basis.** Summary, §6 launch-share ladder (94.6%→72.4%), and every payback figure are computed on the retired external price. No superseded banner (unlike `ai_datacenter_tam.md`, which models the correct hygiene). | Re-base to the ~$10–20M internal marginal launch cost **or** add a prominent superseded-figure banner. Direction of conclusion (launch share falls as rack price rises) survives a re-base; the numbers do not. | PR3 S1 |
| **F4** | `economics/rack_cost_trajectory.md` | **Vera Rubin rack price misattributed to the wrong product.** Doc states "~$7.0–8.8M for the Vera Rubin **NVL144**" citing Tom's Hardware — but the cited article's $8.8M figure is for the **VR200 NVL72**, not the NVL144. §3 rack-compute ratios and §5 revenue-per-rack arithmetic inherit the mislabel. | Relabel the ~$7.0–8.8M price as the **VR200 NVL72** rack; re-check the NVL144-vs-NVL72 compute ratios in §3 against the corrected attribution. | PR3 S2 |
| **F5** | `economics/energy_operating_costs.md` | Verdict, §6, §7 anchor on "~$50–55M Neutron launch" and the stale "~85–90% of node cost" launch-share. Same wave-9 staleness as F3. At the current ~$20M launch / ~$45M node, launch is ~44% of node cost, not 85–90%. | Re-base to ~$20M internal launch / correct the launch-share to ~44%, **or** banner-flag. Qualitative verdict (avoided opex is second-order) is robust either way. | PR3 S3 |
| **F6** | `data_science/REPORT.md` | Carries a wave-5 "Superseded inputs" banner — **but the entire body** (central table, §2–§4, "move now", "window of 2025–2026", "GB300 is the last flyable generation") still asserts the superseded ~163 kW crossover / ~8.75 t ceiling. **Node-mass curve directly contradicts the re-run `simulations/REPORT.md`** (which finds a 150 kW GB300 node at 6.79 t vs. this REPORT's 8.4 t — a ~1.5–2 t disagreement on the same node). | Re-run the data-science REPORT at the corrected ~9.5 t SSO budget so it agrees with `simulations/REPORT.md`, **or** rewrite the body text (not just the banner) to caveat every superseded verdict inline. | PR3 S4, M8; PR2 (consistency) |
| **F7** | `node_design/node_mass_model.md` Summary block | The headline Summary table says **"~5.4 t"** and verdict **"volume-bound, not mass-bound"** — the doc's own §6–§7 compute ~5.6/8.6/14.1 t and conclude **mass-bound**; tracker + LIBRARY say ~5.4–8.6 t / mass-bound. Summary also still cites the pre-wave-5 **"~140–210 m²"** radiator (own §4 derives ~430 m²) and the **~8.5 t** SSO budget (re-based to ~9.5 t). §5–§7 carry correct supersession notes; **only the Summary was missed.** | Rewrite the Summary to match §6–§7 and the tracker: ~5.4–8.6 t, mass-bound, radiator ~200–430 m² (working ~300 m²), SSO ~9.5 t. | PR2 S1, S2 |
| **F8** | `laser_comms/optical_comms.md` Summary | **Internal self-contradiction:** Summary says the official Mk3 modem is "configurable up to 100 Gbps"; the §1 spec table (correctly) says the official Via Satellite wording is "up to 2.5 Gbps." Source check confirms 100 Gbps is the **Mk3.1** roadmap target, not a Mk3 ceiling. Table is correct; the Summary sentence is the error. | Fix the Summary sentence: Mk3 modem configurable up to ~2.5 Gbps; 100 Gbps is the Mk3.1 roadmap target. | PR1 S2 |
| **F9** | `orbital/orbits_environment.md` §2 | Carries **8,000 kg** RTLS LEO payload — contradicts the official **8,500 kg** used by `neutron_specs.md`, `payload_and_block_upgrade.md`, `orbit_types_primer.md`, and `overview.md`. Also mixes in the superseded 2021 "~8,000 kg to LEO" original-design figure. Downstream RTLS-to-SSO estimate (~5.5–6.5 t) is built on the wrong base. | Correct to **8,500 kg**; re-derive the dependent RTLS-to-SSO row. | PR1 S1 |
| **F10** | `ai_hardware.md` §5.3; `node_design/node_mass_model.md` §4 | **Under-flagged hot-loop ↔ HBM-thermal tension** (a known project-level tension, tracker D1). `ai_hardware.md` presents running the coolant loop hotter as a "cost-free" radiator-shrink lever with **no mention** of the Tjmax ceiling (~83–85 °C) or the Arrhenius ~2× failure penalty per +10 °C. `node_mass_model.md`'s ~300 m² figure depends on hot-loop operation without the caveat. `hot_chip_thermal_trajectory.md` handles it honestly. | Add the Tjmax/reliability caveat + a cross-reference to `hot_chip_thermal_trajectory.md` at the `ai_hardware.md` §5.3 hot-loop mention and the `node_mass_model.md` §4 radiator sizing. | PR2 S3 |

### P2 — hygiene (stale-but-flagged, low-traffic, or already-disclosed)

| # | File(s) | What is wrong | Correct value / fix | Raised by |
|---|---|---|---|---|
| **F11** | `LIBRARY.md` | Catalog incomplete: omits **`hyperscaler_margins.md`, `minimum_viable_scale.md`, `ambition_case.md`, `INVESTOR_PROJECTION.md` (M3), `synthesis/lint_report.md`, `strategy/optimized_strategy.md`, `peer_review/`** — all load-bearing for CONCLUSION Rev 5–7. Also says thesis is "versioned Rev 1…Rev 4." | Add the ~7 missing entries with one-line descriptions; update the thesis line after F1. | PR4 S3 |
| **F12** | `synthesis/lint_report.md`, `synthesis/lint_report_2.md` | Both pre-date `CONCLUSION.md`; framed as a checklist for an "about to be written" conclusion. No note that they are superseded; fix-status of their P-items is indeterminate. | Add a "superseded by CONCLUSION.md (Rev 7)" banner to each, and/or annotate which P-items were applied. | PR4 S4 |
| **F13** | `debate/bull_case.md`, `debate/bear_case.md` | Three-round debate ran entirely on the ~$55M external launch / ~$85M node. Bull R3.4 carries "~5.3-yr payback / ~70%+ premium / CONCLUSION.md v2" — all dead notes after the Rev-4 re-base (which moved payback to ~2.8 yr, premium to ~25–40%). Defensible as versioned history, but **nothing flags the economics as superseded.** | Add a superseded-economics banner to each debate file pointing to CONCLUSION Rev 4. Do not rewrite (append-only artifact). | PR4 S5, D-7 |
| **F14** | `strategy/optimized_strategy.md` §2.1, §7 | Round-1 Engineer framing "the block-upgrade is the V2 critical path" was overturned by the CFO R1 + Engineer R2 convergence **in the same file** and by CONCLUSION Rev 6 — but §2.1/§7 are not cross-referenced forward. | Add a forward cross-reference note at §2.1/§7 pointing to the Round-2 demotion. Append-only — do not edit Round 1. | PR4 S6, D-8 |
| **F15** | `RESEARCH_TRACKER.md` narrative rows | Several stale narrative rows: **D1** repeats the dead "~70%+ premium / fails-by-a-thin-margin" debate verdict; **C1** says conclusion "at v6" (it is v7); **L2** says lint pass 2 "fix agents running"; **wave-9 founder note** carries a stale "~$35–90M" node range (final figure ~$24–63M / ~$45M mid). Index rows (1–30, M1–M3, etc.) are complete and correct. | Refresh D1 to the Rev-4 economics; C1 to v7; L2 to done + record fix outcomes; close the wave-9 note to the final ~$45M-mid figure. | PR4 D-6, D-14, D-15, D-16 |
| **F16** | `synthesis/wave4_synthesis.md`, `synthesis/wave5_synthesis.md` | wave4 carries an SSO banner but **none for the launch-cost/node-cost figures** ($52M/$63M/$80M launch, ~$85M-mid node) that Rev 4 retired. Both syntheses still run the "2–3-yr GPU obsolescence window" as the live test. wave5 §4.1 quotes the ~$50–55M figure as internal cost (it is the external price). | Add superseded-figure banners for the launch-cost/node-cost figures and the 2–3-yr-window framing, pointing to CONCLUSION Rev 3/4. | PR4 D-9, D-10, D-11 |
| **F17** | `synthesis/preliminary_findings.md` | Wave-1 doc: has an SSO banner only. Still carries ~6 t/~11 t node masses and surviving 2-rack-node sentences in §1/§5 — pre-node-mass-model framing, flagged by lint pass 1, never reconciled in-body. | Add a banner / reconcile the node-mass and 2-rack-node sentences against the settled 1-rack-node mass model. | PR4 D-13 |
| **F18** | `llm_compute/inference_scaling.md` §2 | GB300 power cell still lists **~120 kW** (the NVIDIA marketing figure the project agreed not to use) — superseded by `ai_hardware.md`'s web-confirmed ~135 kW TDP / 155 kW peak. Flagged by both lint passes; never fixed. Not load-bearing for `inference_scaling.md`'s own argument. | Update the GB300 power cell to ~135 kW TDP / 155 kW peak. | PR2 M2; PR4 M-3 |
| **F19** | `node_design/solar_radiator_trajectory.md` §Summary, §4.3 | Headline scaling table sizes the 130 kW radiator at a single-point ~371 m² without reconciling against the project's adopted ~200–430 m² (working ~300 m²) bracket. §4.5 SSO note is correct. Arithmetic is not wrong; the bracket is missing. | Add the project radiator-range bracket as a note next to the scaling table. | PR2 S4 |
| **F20** | `space_hardware_capabilities.md` §5, `constellation_mesh.md` §1 | CONDOR Mk3 ceiling stated three ways across docs: optical_comms ~2.5 Gbps (as-delivered), space_hardware "0.1–10 Gbps", constellation_mesh "100 Gbps hardware envelope". | Harmonize to: Mk3 as-delivered ~2.5 Gbps (configurable modem), Mk3.1 targets up to 100 Gbps. | PR1 M1, S2 |
| **F21** | `orbital/thermal_analysis.md` §5 + Summary | Correct wave-5 supersession banner at §5 head, **but the body still asserts "~2 racks/launch" as the "working number"** and the Summary says a flight "plausibly carries ~2 racks" — a textbook dead note (settled architecture is 1 rack/node, 1 node/launch). | Strike the "~2 racks/launch" working-number conclusion or make the supersession inline. | PR1 M5 |
| **F22** | `economics/ambition_case.md` §5.2 | Headline "crosses over sooner — ~year 13–16" claim tagged `[DERIVED]` but **no derivation shown** (no cumulative-cash table, unlike the conservative `INVESTOR_PROJECTION.md`). Counter-intuitive and load-bearing. *(See §4 — owner judgment.)* | Add a sketched cumulative-cash table for the crossover year, or down-tag the claim to `[ASSERTED]`. | PR3 S5 |

### P3 — trivial / cosmetic

| # | File(s) | What is wrong | Fix | Raised by |
|---|---|---|---|---|
| **F23** | `CONCLUSION.md` revision history (l.1521–1666) | All seven entries present, but ordering scrambled (v7, v6, v5, v1, v2, v4, v3). | Re-sort v1–v7 into monotonic order. | PR4 §Rule-compliance |
| **F24** | `orbital/orbits_environment.md` §2 | "15 t expendable quoted to a 500 km, 40° inclination LEO" stated as fact, unsourced — Rocket Lab does not publish the reference altitude/inclination. | Flag as an assumption or remove the specific reference. | PR1 M2 |
| **F25** | `laser_comms/constellation_mesh.md` §1 | Earlier-CONDOR "~7,800 km" link range sits unexplained next to the doc's own ~5,000–6,500 km horizon limit. | One-line note that 7,800 km is an optics/spec figure, horizon-limited in practice. | PR1 M9 |
| **F26** | `optical_comms.md` §1, `constellation_mesh.md` §1 | "~9,000+ satellites × ~3 terminals" but "~9,000+ space lasers" — arithmetic does not close (should be ~27,000); the laser count is from an older Starlink state. | Reconcile the satellite and laser counts to one vintage. | PR1 M10 |
| **F27** | `orbit_types_primer.md` §2 | Current Neutron payload sentence footnotes a 2021 "8-ton-class" unveiling URL that does not support current 13/15/8.5 t figures (other citations on the sentence do). | Drop the 8-ton-class URL or relabel it as the historical-design reference. | PR1 M11 |
| **F28** | `neutron_specs.md` vs `LIBRARY.md` | Archimedes cycle termed "oxidizer-rich" in specs, "oxygen-rich" in LIBRARY glossary. Same thing for a LOX engine — terminology drift. | Pick one term project-wide. | PR1 M3 |
| **F29** | `orbital/thermal_analysis.md` header | Both `orbits_environment.md` and `thermal_analysis.md` headed "Doc 6"; tracker lists thermal as item 7. | Renumber thermal header to Doc 7. | PR1 M7 |
| **F30** | `ai_hardware.md` §5.2 | ISS radiator "~840 m²" is the two-sided figure; compared against planform-based "~370 m²/rack" — apples-to-oranges. | Flag whether 840 m² is one-face or two-face for a like-for-like comparison. | PR2 M1 |
| **F31** | `node_mass_model.md` §1 vs `ai_hardware.md` | Rack depth quoted as 1,200 mm vs 1,068 mm (cabinet depth vs L-rail). Harmless. | Note both dimensions consistently in both summaries. | PR2 M3 |
| **F32** | `minimum_viable_scale.md` §4.1 | Revenue basis given as "~$8–16M/rack-year" (asserted as "the brief's basis") then derived as "~$5.6–14.5M". The $16M top is not derived in-doc. | Derive or cleanly attribute the $16M upper bound. | PR2 M5 |
| **F33** | `revenue_per_watt.md` vs `hyperscaler_margins.md` | CoreWeave operating margin given as ~-2% in one, ~-1% in the other. Immaterial. | Pick one figure. | PR3 M3 |
| **F34** | `INVESTOR_PROJECTION.md` / `ambition_case.md` §2.2 | Neutron timeline described slightly differently — "reusable mode NET 2027" vs. the 1(2026)→3(2027)→5(2028) ramp; the 1-launch 2026 debut is dropped. | Reconcile to one sourced Neutron timeline. | PR3 S6 |
| **F35** | `CONCLUSION.md` l.1014 vs l.1052–1066 | "≈8-satellite" strawman cluster never bridged to the "~3–4 → 12–24 node" phase ladder. | Add one bridging sentence noting "≈8" is illustrative. | PR4 M-1 |
| **F36** | `wave4/wave5_synthesis.md`, `optimized_strategy.md` | "first useful service ~4–8 nodes" survives upstream; CONCLUSION Rev 6 re-scoped to ~3–4 / minimum-viable ~3–5. | Annotate the "~4–8" figure as superseded in the upstream docs. | PR4 M-2 |

### Confirmed clean (no action) — recorded for completeness

PR1: 8 docs clean (electron_specs, payload_and_block_upgrade, space_hardware_capabilities,
overview, orbit_types_primer, rf_satcom, rf_limited_service, optical_ground_stations).
PR2: `inference_scaling.md` (apart from F18), `rack_internals.md`,
`reliability_failure_handling.md`. PR3: `ai_datacenter_tam.md`, `premium_value_case.md`,
`hyperscaler_margins.md`, `starcloud.md`, `starship_addendum.md`, `simulations/REPORT.md`,
`revenue_per_watt.md`. PR4: **`CONCLUSION.md` Rev 7 itself is sound, traceable, and
rule-compliant** — the dead notes are all *upstream* of it.

---

## 3. Fix groups for execution assignment

The 36 items cluster into eight work packages. They are independent and can be
assigned to separate fix agents.

- **Group A — Propagate the launch-cost re-base** (F3, F5, F16; relates to F1).
  The single recurring theme. Two economics docs (`rack_cost_trajectory.md`,
  `energy_operating_costs.md`) and two syntheses (`wave4/wave5_synthesis.md`) still
  run the retired ~$50–55M external price as if it were internal cost. Re-base to
  ~$10–20M or add superseded banners. **Largest group; highest reader-impact.**

- **Group B — Bring the thesis current** (F1). Append Rev 5, 6, 7 to
  `vision/initial_thesis.md` so it tracks waves 6–11 (launch re-base, 5-yr life,
  J-curve, build strategy, dual case, in-house radiator, corrected V2 definition).
  Append-only — never overwrite Rev 1–4. *Owner judgment touches this — see §4.*

- **Group C — Refresh the front-door & index docs** (F2, F11, F15, F23).
  `README.md` counts, `LIBRARY.md` missing ~7 catalog entries, `RESEARCH_TRACKER.md`
  stale D1/C1/L2/wave-9 narrative rows, `CONCLUSION.md` revision-history ordering.
  Purely mechanical.

- **Group D — Add superseded-banners to historical artifacts** (F12, F13, F14).
  The two lint reports, the three-round debate, and the strategy doc's Round-1
  framing are correct *as versioned history* but carry dead economics with no flag.
  Add banners / forward cross-references; do **not** rewrite these append-only docs.

- **Group E — Re-run / re-caveat the data-science REPORT** (F6). `data_science/REPORT.md`
  conflicts with the re-run `simulations/REPORT.md` by ~1.5–2 t on node mass. Either
  re-run it at the ~9.5 t SSO budget or rewrite the body text to caveat inline.
  *Owner judgment — see §4.*

- **Group F — Fix the node_mass_model stale summary & radiator brackets** (F7, F19).
  Rewrite the `node_mass_model.md` Summary to match its own §6–§7 (mass-bound,
  ~5.4–8.6 t, ~200–430 m², ~9.5 t SSO); add the radiator-range bracket to
  `solar_radiator_trajectory.md`.

- **Group G — Harmonize cross-doc figures** (F8, F9, F18, F20, F21, F30, F31, F33,
  F34). Point fixes where the same quantity is stated inconsistently across docs:
  CONDOR Mk3 rate, RTLS payload (8,500 kg), GB300 power (~135 kW), the "~2 racks/launch"
  dead note, ISS radiator basis, rack depth, CoreWeave margin, Neutron timeline.

- **Group H — Citation & cosmetic clean-up** (F24–F29, F32, F35, F36).
  Unsourced reference altitudes, mismatched citation URLs, terminology drift,
  header numbering, undocumented figure bounds, bridging sentences. All P3 + a few
  P2; trivial.

- **Cross-cutting — Hot-loop caveat** (F10). Touches `ai_hardware.md` and
  `node_mass_model.md`; can ride with Group F or be assigned alongside Group G.

Suggested order: **C and G first** (mechanical, unblocks readers fastest), then
**A, D, F**, then **B and E** (need owner judgment first).

---

## 4. Items needing the project owner's judgment

Five items are not purely mechanical and should get an owner decision before the
fix pass runs:

1. **F1 / Group B — How to bring the thesis current.** The thesis is the
   append-only "what we believe and why it changed" record. A fix agent *can*
   mechanically append Rev 5–7 by transcribing from `CONCLUSION.md`'s revision
   history — but the thesis is a *narrative belief* document, and the owner may
   want to write (or approve) the Rev 5–7 narrative themselves rather than have it
   machine-written. **Decision needed: auto-append from the conclusion, or
   owner-authored?**

2. **F3 / F5 / F6 — Re-base vs. banner-flag.** For the two stale economics docs
   and the data-science REPORT, there is a genuine choice: *re-compute* every
   number on the current basis (more work, makes the docs live again) or *add a
   superseded banner* and leave the historical numbers (less work, treats them as
   dated artifacts — the pattern `ai_datacenter_tam.md` already uses). The reviewers
   note the *conclusions* survive a re-base, so banner-flagging is defensible.
   **Decision needed: which docs get re-computed, which get banner-flagged?**
   (Recommendation: re-run `data_science/REPORT.md` since it actively contradicts
   the re-run simulation; banner-flag the two economics docs.)

3. **F22 — The ambition-case year-13–16 crossover.** PR3 flags this as a
   counter-intuitive, load-bearing claim tagged `[DERIVED]` with no derivation
   shown. This is the closest thing in the review to a *substantive* gap (a
   reviewer questioning whether a conclusion is supported), not mere staleness.
   The owner should decide whether to **(a)** produce the cumulative-cash table
   that would substantiate the year-13–16 figure, or **(b)** down-tag the claim to
   `[ASSERTED / order-of-magnitude]` and soften the verdict language. A fix agent
   should not silently do either.

4. **F4 — Vera Rubin rack-price re-attribution.** Mechanically the fix is a relabel
   (NVL144 → VR200 NVL72). But §3 of `rack_cost_trajectory.md` builds NVL144-vs-NVL72
   compute ratios on the price; the owner should confirm the corrected attribution
   does not change the doc's price-per-FLOP conclusion before the relabel is treated
   as cosmetic.

5. **T-1 (PR4) — The ~$20M internal launch cost traces to a founder note, not
   research.** Not a defect — the conclusion discloses it as open unknown #4 — but
   it is the single largest driver of the Rev-4 economic sign-change, and it rests
   on founder back-of-envelope, not a sourced research doc. **No fix is required**,
   but the owner should be consciously aware that the most consequential number in
   the project is the least independently sourced one. If a fix agent re-bases docs
   onto ~$20M (Group A), it is propagating a founder estimate — that is acceptable
   given the conclusion already does so, but it is an owner-level call, not an
   editorial one.

---

## 5. Bottom line

The peer review is a **clean bill of health on substance** — no physics error, no
fabricated or misread load-bearing source, no invalidated conclusion. `CONCLUSION.md`
Rev 7 is sound and traceable. What the review found is a **maintenance debt**: the
project moved fast through eleven waves and the conclusion kept up, but the thesis,
the README, the catalog, two economics docs, the data-science REPORT, the syntheses,
the debate, and the strategy doc did not. The fix pass is a propagation-and-banner
exercise, not a correction exercise. Once Groups A–H are applied and the five
owner-judgment items in §4 are decided, the corpus can be certified meticulously
correct.
