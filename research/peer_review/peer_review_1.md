# Peer Review 1 — Launch / Orbital / Comms Research Docs

**Reviewer:** Peer Reviewer 1
**Date:** 2026-05-17
**Scope audited (13 docs):**
`rocket_lab/overview.md`, `rocket_lab/neutron/neutron_specs.md`,
`rocket_lab/neutron/payload_and_block_upgrade.md`, `rocket_lab/electron/electron_specs.md`,
`rocket_lab/space_hardware_capabilities.md`, `orbital/orbits_environment.md`,
`orbital/thermal_analysis.md`, `orbital/orbit_types_primer.md`,
`laser_comms/optical_comms.md`, `laser_comms/rf_satcom.md`,
`laser_comms/rf_limited_service.md`, `laser_comms/optical_ground_stations.md`,
`laser_comms/constellation_mesh.md`
Cross-checked against `RESEARCH_TRACKER.md` and `LIBRARY.md`.

**Method:** Full read of every assigned doc; validity, source-attribution and
internal-consistency check; spot-confirmation of cited sources via web search
(Neutron LEO payload figures, CONDOR Mk3 data rate, TBIRD 200 Gbps, RKLB Q1 2026
financials — all confirmed accurate).

**Overall:** The corpus is in good shape. Numbers are well sourced, source spot-checks
held up, and the docs are honest about their estimates. The findings below are
almost entirely **internal-consistency / stale-figure** issues, not errors of fact.
Most are small. One significant stale figure (the RTLS LEO number in
`orbits_environment.md`) and one self-contradiction inside `optical_comms.md`.

---

## SIGNIFICANT ISSUES

### S1 — `orbital/orbits_environment.md` §2: wrong RTLS LEO payload (8,000 kg) — contradicts every other doc and the official figure
**Quote (§2, "Neutron's published baseline"):**
> "Rocket Lab quotes Neutron at ... **~8,000 kg return-to-launch-site (RTLS)**"

and the §2 estimate table row:
> "Reusable, RTLS | ~8.0 t | **~5.5-6.5 t** | ~25-30%"

**What is wrong — contradicted / stale.** The official Rocket Lab RTLS figure is
**8,500 kg**, not 8,000 kg. This is confirmed by Wikipedia/Rocket Lab and stated
correctly in `neutron_specs.md` (8,500 kg, "High confidence"), in
`payload_and_block_upgrade.md` (8,500 kg, "official"), and in `orbit_types_primer.md`
(§2, "~8,500 kg return-to-launch-site"). Only `orbits_environment.md` carries 8,000 kg.
Separately, the "~8,000 kg to LEO" number is itself the *original 2021 Neutron design
figure* (resolved in `payload_and_block_upgrade.md` §4 and `neutron_specs.md` open-Q5)
— so this doc has effectively mixed a superseded historical number into the current
RTLS row. The downstream RTLS-to-SSO estimate (~5.5–6.5 t) is built on the wrong base.
Low practical impact (RTLS is not the baseline mode), but it is a clear factual
inconsistency that should be corrected to 8,500 kg.

### S2 — `laser_comms/optical_comms.md`: internal self-contradiction on the CONDOR Mk3 modem ceiling (2.5 vs 100 Gbps)
**Quote (Summary):**
> "Officially, the Mk3 modem is described as **'configurable up to 100 Gbps,'** so
> the ~2.5 Gbps figure is the *as-delivered* operating point, not a hardware ceiling."

**Quote (§1 spec table, same doc):**
> "Data rate (as delivered, SDA T1) | **~2.5 Gbps** | Official: **'configurable modem
> up to 2.5 Gbps'** ([Via Satellite])"

**What is wrong — internal contradiction / likely misread of the source.** The summary
says the *official* description is "configurable up to 100 Gbps"; the table says the
*official* Via Satellite wording is "configurable modem up to 2.5 Gbps." These cannot
both be the official phrasing. My source check confirms the Via Satellite article
describes the Mk3's configurable modem at **up to 2.5 Gbps**, with **100 Gbps** being
the **Mk3.1** (next-generation) target — i.e. 100 Gbps is *not* a Mk3 hardware
ceiling. The summary sentence overstates the Mk3: it should say the Mk3 modem is
configurable up to ~2.5 Gbps and 100 Gbps is the Mk3.1 roadmap. (The table row is
correct; the summary sentence is the error.) Note `constellation_mesh.md` §1 hedges
correctly — "~100 Mbps to 100 Gbps hardware envelope" — and `space_hardware_capabilities.md`
§5 says "CONDOR Mk3: 0.1–10 Gbps." So the project carries **three different** Mk3
data-rate ceilings (2.5 / 10 / 100 Gbps) across docs — see M1 below.

---

## MINOR ISSUES

### M1 — CONDOR Mk3 data-rate ceiling stated three different ways across docs
- `optical_comms.md` table: as-delivered ~2.5 Gbps; "configurable range 100 Mbps–100 Gbps."
- `space_hardware_capabilities.md` §5: "CONDOR Mk2: 0.1–1.25 Gbps; **CONDOR Mk3: 0.1–10 Gbps**."
- `constellation_mesh.md` §1: "~100 Mbps to 100 Gbps hardware envelope."

These are not all reconcilable. The cleanest sourced statement is: Mk3 as-delivered
~2.5 Gbps (configurable modem), Mk3.1 targets up to 100 Gbps. The "0.1–10 Gbps" in
`space_hardware_capabilities.md` and the "100 Gbps hardware envelope" in
`constellation_mesh.md` should be harmonized to that. Unsourced/under-sourced as
written. Low impact (all docs agree the *usable* figure today is ~2.5 Gbps and the
mesh needs the Mk3.1 roadmap), but it is an inconsistency.

### M2 — `orbital/orbits_environment.md` §2: "15 t expendable ... quoted to a 500 km, 40° inclination LEO"
**Quote:** "The 15 t expendable figure is quoted to a **500 km, 40° inclination** LEO."
**What is wrong — unsourced / unconfirmed.** Rocket Lab does not publish the reference
altitude/inclination behind its LEO numbers — `payload_and_block_upgrade.md` open-Q3
explicitly says "Rocket Lab does not state the exact altitude/inclination behind
13,000 kg DRL." This doc states a specific "500 km, 40°" reference as if it were a
fact, with no citation. It should be flagged as an assumption or removed.

### M3 — `rocket_lab/neutron/neutron_specs.md`: Archimedes combustion cycle described inconsistently
**Quote (§3 table):** "Propellant | **LOX / liquid methane (methalox)** | Oxidizer-rich
staged combustion"
**Quote (summary table, line 27):** "Propellant | LOX / liquid methane (methalox) |
**Oxidizer-rich staged combustion**"
**Quote (§3 Archimedes bullet):** "**Oxidizer-rich** staged-combustion cycle, methalox."
The LIBRARY glossary instead says "Archimedes — Neutron's engine (**oxygen-rich**
staged combustion)." "Oxidizer-rich" and "oxygen-rich" denote the same thing for a
LOX engine, so this is terminology drift rather than an error — but the project should
pick one term. Minor.

### M4 — `rocket_lab/overview.md` §5 vs `neutron_specs.md`: RTLS payload phrasing
**Quote (`overview.md` §5):** "up to ~13,000 kg to LEO with downrange booster landing
(up to ~15,000 kg expended; **~8,500 kg with return-to-launch-site**)."
This is correct and consistent with the official figure — noted here only to confirm
`overview.md` agrees with `neutron_specs.md` and against `orbits_environment.md` (S1).
No action on `overview.md`; it is a clean cross-check.

### M5 — `orbital/thermal_analysis.md` §5: superseded "1–2 racks/launch" / "~2 racks/launch" working figure left in body text
The doc carries a wave-5 "Superseded" banner at the head of §5 correctly noting the
~10 t budget and "1–2 racks/launch" are superseded by the settled **1 rack/node, 1
node/launch** architecture. However, the body of §5 still then states, uncorrected,
*"Realistic / working number: ~2 racks/launch ... **This doc carries ~2 racks/launch.**"*
and the Summary up top says a Neutron flight "plausibly carries **~2 racks**." The
banner flags the staleness but the doc still asserts the stale conclusion as its
"working number." This is exactly the "dead note" pattern the QA pass is meant to
catch — a reader skimming §5 or the Summary gets the superseded answer. Recommend the
fix pass either strike the "2 racks/launch" conclusion or make the supersession
inline. (Tracker item 7 and LIBRARY both already mark this doc's racks-per-launch as
superseded, so the project position is clear — only the doc body lags.)

### M6 — `orbital/thermal_analysis.md` radiator-area figure is the optimistic bound, repeatedly self-flagged
The doc derives "~120–210 m²/rack" and flags (cross-ref banner) that the reconciled
project range is "~200–430 m²/rack, working ~300 m²." This is handled honestly — the
doc explicitly calls its own number "the optimistic bound." Noted as **not a defect**;
flagging only so the fix pass is aware the standalone "~120–210 m²" must never be
quoted without the reconciliation. Consistent with `lint_report.md` §1.1 and the
tracker.

### M7 — `orbital/thermal_analysis.md` header mislabeled "Doc 6 (companion)"
Both `orbits_environment.md` and `thermal_analysis.md` are headed "Doc 6" ("Doc 6 of
foundational research" and "Doc 6 (companion)"). The tracker lists thermal as **item 7**.
Cosmetic, but a numbering inconsistency.

### M8 — `rocket_lab/overview.md`: market cap "~$72–73B" vs tracker "~$72B EV"
`overview.md` gives market cap ~$72–73B (13 May 2026 snapshot, explicitly flagged
volatile). Tracker item 28 references "the ~$72B EV." Market cap and enterprise value
are not the same quantity; the two docs use them loosely as interchangeable. Minor,
and `overview.md` itself flags the figure as a volatile snapshot — no factual error,
just imprecision. Out-of-slice (tracker), noted for the end-doc reviewer.

### M9 — `laser_comms/constellation_mesh.md` §1: CONDOR earlier-generation range "~7,800 km"
**Quote:** "earlier CONDOR generations were specified for intra/inter-plane link
distances up to **~7,800 km** in densely-packed constellations ([MSA Components],
[satsearch])."
This ~7,800 km figure exceeds the doc's own stated geometric horizon limit (~5,400 km
for Starlink, "~5,000–6,500 km before Earth's horizon intervenes"). The doc does not
reconcile how an earlier CONDOR could be "specified" to 7,800 km when its own §1
argues the horizon caps practical ISL range well below that. Likely a vendor
spec-sheet number (free-space optical reach, not horizon-limited geometry) — but as
written it sits unexplained next to a contradicting horizon argument. Recommend a
one-line clarification that 7,800 km is an optics/spec figure, horizon-limited in
practice. Low impact (the doc's conclusion "range never binds" is unaffected).

### M10 — `laser_comms/optical_comms.md` §1: Starlink satellite count "~9,000+" vs terminal count
**Quote:** "SpaceX's Starlink runs **~9,000+ satellites** with ~3 laser terminals each
... across **9,000+ space lasers**."
The two figures are inconsistent with each other: ~9,000 satellites × ~3 terminals
would be ~27,000 lasers, not 9,000. The "9,000+ space lasers" almost certainly comes
from an older Starlink state (~3,000 sats × 3). `constellation_mesh.md` §1 repeats
"~9,000+ space lasers" too. This is a sourced-but-internally-incoherent pair of
numbers — the satellite count and the laser count were likely lifted from different
vintages of the same Hackaday article. Low impact on any conclusion (the point is
only "laser meshes work at scale"), but the arithmetic does not close.

### M11 — `orbital/orbit_types_primer.md` §2: cites a Rocket Lab "8-ton-class" Neutron URL for current payload
**Quote (§2 sourcing):** current Neutron LEO numbers (13/15/8.5 t) are footnoted to,
among others, "[Rocket Lab: Neutron unveiling](https://www.rocketlabusa.com/about-us/updates/rocket-lab-unveils-plans-for-new-8-ton-class-reusable-rocket-for-mega-constellation-deployment/)."
The cited page is the **2021 unveiling of the original 8-ton-class design** — it does
*not* support the current 13/15/8.5 t figures (those come from the matured design).
The other citations on that sentence (Wikipedia, NewSpace Economy) do support the
current numbers, so the claim is still sourced — but the 8-ton-class URL is a
mismatched citation for a current-spec sentence. Minor; recommend dropping that URL
from that footnote or labelling it as the historical-design reference.

---

## DOCS JUDGED CLEAN (no material issues)

- **`rocket_lab/electron/electron_specs.md`** — clean. Figures (300 kg LEO / 200 kg
  500 km SSO, ~80+ launches, 21/21 in 2025, ~$8.4M, 4 lifetime failures) are
  internally consistent, sourced, and consistent with `overview.md` and
  `payload_and_block_upgrade.md` §4 (Electron +33% growth). Honest about source
  variance on thrust and launch count.
- **`rocket_lab/neutron/payload_and_block_upgrade.md`** — clean and is the
  authoritative SSO doc. The ~9.5 t working / 8.5–10.5 t range is derived
  transparently (0.65–0.80 retention factor), every LEO figure is correctly marked
  official, the block upgrade is correctly marked speculative. LEO figures confirmed
  against the live source.
- **`rocket_lab/space_hardware_capabilities.md`** — clean. Acquisition figures
  (SolAero ~$80M, Geost $275M, Mynaric ~$155.3M, Motiv $40M, Sinclair, PSC ~$81.4M),
  dates, and the radiator-gap conclusion are all sourced and consistent with
  `overview.md`. Honest that the radiator gap is "inference from absence of evidence."
- **`rocket_lab/overview.md`** — clean. Q1 2026 financials ($200.3M revenue,
  $136.7M/$63.7M segment split, $2.2B backlog, Q2 guidance $225–240M) confirmed
  against the Rocket Lab release. Market-cap volatility properly flagged.
- **`orbital/orbit_types_primer.md`** — substantively clean (only the minor M11
  citation mismatch). Orbit regimes, delta-v figures, TDRS/EDRS contact-time numbers,
  FCC 5-year rule all well sourced; SSO-is-a-LEO framing correct and consistent with
  the tracker.
- **`laser_comms/rf_satcom.md`** — clean. Spectrum/ITU argument is well sourced;
  HTS-capacity caveat ("shared, not per-link") is correctly stated; conclusion
  consistent with `rf_limited_service.md` (which explicitly refines, not contradicts, it).
- **`laser_comms/rf_limited_service.md`** — clean. Honest, well-flagged estimates
  (every throughput/user number marked "estimate, needs a real link budget");
  Open Cosmos / Liechtenstein precedent correctly sourced; correctly framed as a
  refinement of `rf_satcom.md`.
- **`laser_comms/optical_ground_stations.md`** — clean. Aperture^2.5 cost scaling,
  the 0.5–1.0 m norm, the ≥4-sites-for-99% / ~10–12-for-99.9% diversity numbers,
  TBIRD 200 Gbps, uplink/downlink asymmetry all sourced; cost figures explicitly
  flagged as estimates. Strong doc.
- **`laser_comms/constellation_mesh.md`** — substantively clean (minor M9/M10 only).
  Speed-of-light latency math, Starlink topology, formation-flying spacing all
  well sourced; the soft ~1–10 km spacing number is honestly self-flagged as the
  weakest figure.
- **`orbital/orbits_environment.md`** — clean *apart from* S1 and M2. The radiation
  analysis (~1–3 krad(Si)/yr behind 4–6 mm Al, SEU architecture), eclipse-fraction
  geometry, debris / FCC-5-year discussion are all well sourced and sound.
- **`orbital/thermal_analysis.md`** — analysis is sound and the Stefan-Boltzmann
  treatment is correct; issues M5/M6/M7 are stale-conclusion / labelling, not physics.

---

## SUMMARY

Thirteen docs audited. **Eight are clean**; the rest carry only minor or
stale-figure issues. No physics error, no fabricated source, and no broken/misread
citation that changes a conclusion was found — spot-checks of the load-bearing
sources (Neutron LEO payloads, CONDOR Mk3 rate, TBIRD 200 Gbps, RKLB Q1 financials)
all confirmed accurate.

The two issues worth fixing first: **(S1)** `orbits_environment.md` carries a wrong
RTLS LEO payload — 8,000 kg instead of the official 8,500 kg every other doc uses —
and has mixed in the superseded 2021 design figure; and **(S2)** `optical_comms.md`
contradicts itself on the CONDOR Mk3 modem ceiling, with its summary overstating the
Mk3 as "configurable up to 100 Gbps" when 100 Gbps is the Mk3.1 roadmap. Beyond
those, the CONDOR Mk3 ceiling is stated three different ways across three docs (M1),
and `thermal_analysis.md` still asserts a superseded "~2 racks/launch" working number
in its body despite a correct supersession banner (M5) — a textbook dead note.

**Confidence: high.** The corpus is fundamentally sound; the findings are
consistency hygiene, not validity failures.
