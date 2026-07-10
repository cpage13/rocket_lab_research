# Communications Default Assumptions (The Iridium Model)

This is the human-readable ledger for the Iridium model's default assumptions.
The machine-readable default scenario is `code/scenarios/iridium.yaml`; the
promoted model is `communications/models/iridium/default.json`; the claim
ledger is `research/SOURCE_INDEX.md`.

The project is not a DCF. It asks whether a Neutron-launched next-generation
fleet on Iridium's owned L-band could plausibly serve a large subscriber base
at visible cost under stated assumptions. The default scenario is
creator-selected, reviewable, and expected to improve.

The canonical default output is dynamic JSON. The conclusion is static
editorial prose tied to the promoted default. If defaults change, update this
ledger and the promoted JSON, then review `communications/conclusion.md` before
treating it as current.

## Source-Status Taxonomy

| Source status | Meaning |
|---|---|
| `certified` | Directly supported by a primary or official source. |
| `sourced_estimate` | Estimated from credible external sources, but not an official exact value. |
| `derived_estimate` | Computed from sourced or scenario inputs using a stated formula. |
| `projection` | A forward-looking market or technical projection from an external source. |
| `extrapolation` | A project extrapolation from known or sourced behavior. |
| `scenario` | A chosen modeling assumption for feasibility analysis. |
| `placeholder` | A known open slot that should not support settled public claims. |
| `stale` | Known old material retained only for historical context. |

Public documentation must not present `placeholder` or `stale` items as settled
evidence.

## Key Sourced And Derived Dials

The dials below carry the physics. Every one is a named constant in
`code/src/communications/constants.py` with its derivation in the docstring.

| Dial | Default | Source status | Source |
|---|---|---|---|
| Exclusive spectrum | 8.0 MHz | `scenario` on a sourced basis | `COMM-611`: 1616 to 1626.5 MHz is a 10.5 MHz span, 7.775 MHz exclusive plus 0.95 MHz shared with Globalstar; 7.775 rounded up to 8.0, stated in code. The Big LEO split is confirmed at `COMM-656`. |
| Coordinated spectrum variant | 10.5 MHz | `sourced_estimate`, contingent | Same `COMM-611` span. Authorized today is 7.775 plus 0.95 shared; the full 10.5 depends on the live FCC petition over the Globalstar sliver. Upside variant, never the baseline. |
| Phone-class spectral efficiency | 0.65 bps/Hz (band 0.5 to 0.8) | `sourced_estimate`, measured | `COMM-428/429`: Starlink direct-to-cell measured mean 0.79 and median 0.64 bps/Hz at about 0 dB median SINR (arXiv 2506.00283, fetched and verified verbatim). Central is the band midpoint. |
| Small-terminal spectral efficiency | 2.0 bps/Hz (band 1.5 to 2.5) | `derived_estimate` | Shannon chain on the phone-class anchor plus the founder's device spec (about 10 dBi unpointed patch): plus 10 dB gives 1.6 to 2.2 bps/Hz at 60 to 80 percent of Shannon. |
| Terminal-class spectral efficiency | 2.5 bps/Hz (band 2.0 to 3.0) | `sourced_estimate` | `COMM-650` and the capacity doc's modern-ACM band (about 2 to 3 bps/Hz to a gain terminal); `COMM-428` carries the AST claim to about 3. |
| Reuse calibration | 0.15 Gbps per MHz per unit SE | `derived_estimate` (calibration) | `COMM-410`: a flat 25 square meter class array on about 25 MHz produces about 5 to 15 Gbps (central 8 to 10). 25 x 2.5 x 0.15 = 9.375 sits inside the central band; the implied 150x effective reuse sits inside `COMM-411`'s 130 to 200x. |
| Aperture reference | 25.0 square meters | `sourced_estimate` | The corpus flat-array class (`COMM-408/410`, about 20 to 24 square meters, called 25-square-meter class). Flatellite's own dimensions are unpublished; the 25 is a render-read working number, flagged as such. |
| No-fold aperture limit | 25.0 square meters | `derived_estimate` (geometry) | A 60 square meter flat square is about 7.7 meters across, past Neutron's 5.5 meter fairing; a 25 square meter square is 5.0 meters and fits. The no-deployable design philosophy is `COMM-251`. |
| Satellites per launch | 12 | `derived_estimate`, estimate-bound | `COMM-258/260`: about 9,500 kg to SSO over the roughly 800 kg single-source mass estimate (`COMM-253/256`) gives about 12. |
| Satellite build cost | 1.05 million dollars | `scenario` | Founder-set, in-band below the Starlink V3 hardware anchor of about 1.2 million dollars (`COMM-082`, a projection, hardware-cost analogy only). |
| Satellite lifetime | 5 years | `scenario` | The corpus Starlink operating-life lineage (`COMM-097`). |
| Coverage floor | 340 satellites | `scenario` on a computed basis | The project coverage simulation's 95 percent column reads 341 at 450 km and a 25 degree mask, founder-rounded to 340; inside `COMM-216`'s 290 to 960 floor band. |
| Saturation cap | 2,000 satellites | `scenario` | Founder-set dial encoding the tiling/interference ceiling (`COMM-413` to `COMM-416` own the mechanism; `COMM-550/553` the fleet scale). |
| Busy-hour concurrency | 2.5 percent | `scenario`, corpus-central | `COMM-543`: working direct-to-cell concurrency about 1 to 5 percent, central 2 to 3. |
| Subscriber base at coverage | 10,000,000 people | `scenario` | Founder-set conservative slice of the coverage-gap pool (`COMM-021`: about 300 million people without mobile coverage; context `COMM-390`, `COMM-065`). |
| IoT devices | 10,000,000 devices | `scenario`, cosmetic | Contention-limited, not population-capped (`COMM-654/659`); zero sizing effect on the subscriber service. |
| Cost-plus revenue multiple | 1.5x | `scenario` | Mirrors the data-center central band (`RLDC-REVENUE-MULTIPLE-1_5X`); produces the flat 33.3 percent margin. |

Citation-precision note: a two-round traceability audit (converged 2026-07-08)
verified 91 numbers across the constants, dials, scenario, and frozen anchors
with zero numeric discrepancies, and found four citation ids pointing at the
wrong ledger rows. All four were corrected in code on 2026-07-08: the
build-cost anchor now cites `COMM-082` (previously `COMM-080`, the V1 row),
the 5-year lifetime now cites `COMM-097` (previously `COMM-091`), the aperture
reference now cites the flat-array class `COMM-408/410` for area (the
`COMM-253/256` rows are the mass estimate and now say so), and the
terminal-class band now cites `COMM-650` (previously `COMM-647`, the aggregate
row). Values were untouched.

## The Assumptions Register

Distilled from the converged audit: the 30 assumption-class values in the
model, with provenance. Founder-set means the founder chose or confirmed the
value; convention means a stated modeling or engineering convention. The last
six rows are modeling posture the audit surfaced and stated explicitly.

### Founder-Set Values

| # | Assumption | Value |
|---|---|---|
| 1 | Exclusive-spectrum baseline (7.775 rounded up) | 8.0 MHz |
| 2 | Active rate baseline, standard smartphone activity | 1.0 Mbps |
| 3 | Rich active-rate variant | 2.5 Mbps |
| 4 | Busy-hour peak concurrency (corpus-central) | 2.5 percent |
| 5 | Off-peak concurrency (no corpus row exists; founder pair) | 0.5 percent |
| 6 | Device-class baseline | phone class |
| 7 | Aperture dial default (flat-body class) | 25.0 square meters |
| 8 | Operations cost, a line to research later, stated in output | 0.0 dollars per year |
| 9 | Subscriber target (people) | 10,000,000 |
| 10 | Coverage floor (simulation 341, rounded) | 340 satellites |
| 11 | Saturation cap (the tiling/interference dial) | 2,000 satellites |
| 12 | Communications share of Neutron cadence | 0.18 |
| 13 | Satellite build cost (below the V3 anchor) | 1.05 million dollars |
| 14 | Cost-plus revenue multiple (data-center mirror) | 1.5x |
| 15 | IoT device passthrough (devices, not people) | 10,000,000 |
| 16 | ARPU 50 dollars per month: a High-Bandwidth Cellular Pure Play case value; for the Iridium model the ARPU case is deferred until the per-tier sheet is set (founder range stated 2026-07-09: 10 to 20 dollars per month for the standard phone-class tier; IoT about 8 dollars per device per month) | deferred |

### Why The Cadence Share Is 0.18

The communications share of Neutron cadence (row 12) is a founder-set scenario
dial, not a derived number, and the reasoning behind the value is worth
recording. Communications shares Neutron with the data-center application and
with external launch customers, so it takes a minority of the manifest. At the
modeled cadence ramp (90 launches a year by 2036), an 18 percent share is about
16 launches a year at maturity. That is enough to do the job the baseline asks
of it: the 340-satellite coverage floor deploys by 2035 (about 29 cumulative
launches of 12 satellites, spread over the ramp years), and the five-year
replacement treadmill at steady state needs about 68 satellites a year, roughly
6 launches, well inside the share. It also deliberately leaves the large
majority of Neutron capacity for the rest of the business. The dial is the
deployment-speed lever: at a higher share the same 29-launch build lands
years earlier instead of about 10 (model runs: a 0.5 share completes coverage
in 2033, 0.8 in 2032, 0.9 in 2031, and 2031 is the ramp-bound floor even at a
1.0 share; the conclusion states the sweep), and the rich-tier and saturation
scenarios need a higher share to complete inside the model horizon. The model reports below-target deployment truthfully rather than
hiding it, so an under-provisioned share is visible in the output, not papered
over.

### Conventions And Modeling Posture

| # | Assumption | Value |
|---|---|---|
| 17 | Spectral-efficiency centrals are band midpoints | 0.65; 2.5 bps/Hz |
| 18 | Small-terminal band edges (ladder convention) | 1.5 / 2.5 bps/Hz |
| 19 | Small-terminal device spec (about 10 dBi unpointed) drives its computed SE | 2.0 bps/Hz |
| 20 | Density rounds half-up; launch coupling floors (two deliberate opposite roundings) | rounding pair |
| 21 | Off-peak per-user rate capped by the single-beam pool (the beam is the per-person ceiling) | min(pool, ratio) |
| 22 | Capacity linear in aperture area (conservative; ignores the SNR lift) | factor = area / 25 |
| 23 | Launch count inverse-linear in area, floored, minimum 1 | max(1, floor) |
| 24 | No-fold limit, calibration reference, and dial default coincide by design | all 25.0 |
| 25 | Scenario label lives in one place on the Iridium block | single home |
| 26 | Base year 2026, horizon 10 years (data-center mirror timeline) | FY2036 end |
| 27 | Cadence ramp anchors: 14 at year 5, 90 at year 10, ceiling 150, first launch index 1 (scenario, not Rocket Lab guidance) | shared spine |
| 28 | Launch-cost curve: 25.0 to 13.5 million dollars, log-linear over 5 to 100 launches per year | shared spine |
| 29 | Satellite lifetime, the five-year cohort cliff | 5 years |
| 30 | Satellites per launch at the reference aperture (estimate-bound on the single-source mass) | 12 |
| 31 | IoT load treated as exactly zero in sizing (contention-limited) | 0 load |
| 32 | One device class per run (mixed fleets are a future extension) | single class |
| 33 | Uniform-demand geography: every satellite counts as serving demand; ocean and empty-land time not modeled | fleet = target / density |
| 34 | The purpose-built L-band payload is assumed cost-identical to the cellular-family satellite at 25 square meters (1.05 million dollars, 12 per launch); the equivalence is asserted, not argued | carried unchanged |
| 35 | The 10.5 MHz variant assumes winning the live FCC coordination (authorized today: 7.775 plus 0.95 shared) | contingent |
| 36 | Deployment is generic build-and-hold from 2026, not deal-timed (close mid-2027; replacement window about 2035) | a shape, not a dated plan |
| 37 | No spares, no launch failures, no satellite failures inside the five-year life | perfect fleet |
| 38 | The equality tripwire premise: the Iridium baseline and the cellular default both bind at the 340 floor with the aperture identity at 25.0; a dial change breaks the test loudly by design | tripwire |

## Model Output Anchors

These values are derived from the promoted default JSON, not external facts.
All are `derived_estimate`.

| Output | Value |
|---|---|
| Per-satellite capacity | 0.78 Gbps |
| Subscribers per satellite | 31,200 |
| Fleet size (coverage binds) | 340 satellites |
| Phone beam pool | 5.2 Mbps |
| Per-user peak / off-peak | 1.0 / 5.0 Mbps |
| Fleet aggregate capacity | 265.2 Gbps |
| Build launches (12 per launch) | 29 |
| Coverage complete | 2035 |
| Cost-plus revenue at 33.3 percent margin | about 251.5 million dollars per year |
| Cash cost per subscriber (build-year artifact, see conclusion caveat) | about 7.95 dollars per year |

## Catalog Status

The catalog reconciliation is complete: `research/SOURCE_INDEX.md` carries
every claim block this model cites, end to end through `COMM-710` (the
spectrum fundamentals, Iridium acquisition, band designations, Iridium
capacity and modernization, the device gate, and MSS spectrum expansion were
indexed as Waves 8 and 9 on 2026-07-08). The only gaps in the id space are
the two documented reserved-unused ranges (`COMM-575..600` and
`COMM-677..685`).

## Maintenance Rule

When a default assumption changes, update this ledger, update
`research/SOURCE_INDEX.md` if the claim trail changes, re-promote the dynamic
JSON, and then review `communications/conclusion.md`. Promotion does not
rewrite the static conclusion for you.
