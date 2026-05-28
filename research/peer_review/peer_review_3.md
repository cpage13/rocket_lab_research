# Peer Review 3 — Economics, Competitor & Model Docs

*Reviewer: Peer Reviewer 3. Date: 2026-05-17. Scope: the 7 `economics/` docs,
the 2 `competitors/` docs, and the 3 simulation/data-science REPORT docs.
Report-only — no audited document was edited.*

Method: each document read in full; arithmetic re-derived; hard claims checked
for attribution; a sample of cited sources spot-checked via web search
(CoreWeave FY2025, Rocket Lab FY2025, NVIDIA Vera Rubin rack price, McKinsey
156 GW, Neutron ramp schedule, Starcloud-3). Cross-checked against
`RESEARCH_TRACKER.md` and `LIBRARY.md`.

---

## Significant findings

### S1. `economics/rack_cost_trajectory.md` — entire doc runs on the stale $50–55M launch-cost basis
This is the single most material issue in the slice. The doc's Summary, §6
table, and the worked payback sketch all use **"a fixed ~$50–55M Neutron
launch"** / "$52.5M launch midpoint." Quotes:

> "If an orbital node = 1 rack + a fixed ~$50–55M Neutron launch …"
> "Use $52.5M as the launch midpoint."
> "*Today, GB200 node ($55.5M CapEx):* payback ≈ 6.9 years."

This is **stale / contradicted.** The project re-based launch cost in wave 9
to Rocket Lab's **internal marginal cost of ~$10–20M** (tracker wave-9 input;
`CONCLUSION.md` Rev 4; `INVESTOR_PROJECTION.md`; `ambition_case.md` — all use
$20M base, $55M only as an external-price sensitivity). The whole §6 launch-
share ladder (94.6% → 72.4%) and every payback figure in this doc are computed
on a launch cost the rest of the project explicitly retired. The *direction*
of the doc's conclusion (launch share falls as rack price rises) survives a
re-base, but every number in it is off. The doc carries no superseded-figure
banner, unlike `ai_datacenter_tam.md` §5 which does flag its retired $3B/GW
proxy. Recommend the doc be banner-flagged or re-based.

### S2. `economics/rack_cost_trajectory.md` — Vera Rubin rack price misattributed to the wrong rack (NVL144 vs NVL72)
The doc repeatedly states the **Vera Rubin NVL144** rack costs ~$7.0–8.8M and
cites Tom's Hardware:

> "~$7.0M–$8.8M for the Vera Rubin NVL144 (shipping H2 2026)"
> source: "[Tom's Hardware — Vera Rubin NVL72/NVL144 racks up to $8.8M apiece]"

**Misread of the source.** The cited Tom's Hardware article headline is
"Price of Nvidia's Vera Rubin **NVL72** racks skyrockets to as much as
$8.8 million" — the $7–8.8M figure is for the **VR200 NVL72** rack, not the
NVL144. (Confirmed via web search, 2026-05-17.) The doc's price table row
labels it "Vera Rubin NVL144 (144 GPU dies)" and §3 builds rack-compute
ratios (NVL144 vs NVL72) on this price. The price-per-FLOP and revenue-per-
rack arithmetic in §3/§5 inherit the mislabel. The doc's own Open Question 1
correctly flags the Rubin figure as single-sourced and to-be-re-verified, but
does not catch that it is attached to the wrong product.

### S3. `economics/energy_operating_costs.md` — also runs on the stale $50–55M launch basis
The verdict, §6, and §7 all anchor on **"the ~$50–55M Neutron launch"**:

> "Against the **~$50–55M Neutron launch**, total avoided opex (~$1.15M)
> offsets only **~2–4%**."
> "launch first (~$50–55M, ~85–90% of node cost)"

Same staleness as S1 — this is the external customer price, not the ~$20M
internal marginal cost the project adopted in wave 9. The doc's qualitative
conclusion (avoided energy/water opex is second-order vs. launch) is robust to
the re-base — at a $20M launch, ~$1.15M avoided opex still offsets only ~6%,
not a material change to the verdict. But the explicit "~85–90% of node cost"
launch-share claim is wrong on the current basis: at a ~$45M central node
(`INVESTOR_PROJECTION.md`), a $20M launch is ~44% of node cost, not 85–90%.
The "85–90%" figure is itself a stale wave-4-era number. Flag as stale.

### S4. `data_science/REPORT.md` — headline crossover computed on a superseded payload budget; node-mass figures conflict with the simulation REPORT
The doc's central table and §2 give Vera Rubin node mass ~12.7 t, GB300 ~8.4 t,
and the crossover at **~163 kW** against an **~8.75 t** reusable-SSO ceiling.
The doc *does* carry a prominent "Superseded inputs (wave-5)" banner up top
saying the ~163 kW figure is superseded by the ~9.5 t re-base and the
~200–250 kW reconciled ceiling — good. **But the banner is not enough:** the
entire body, the table, §2, §3, and §4 ("the actionable read is: move now",
"window of roughly 2025–2026", "GB300 is the *last* flyable generation") are
left standing on the old numbers, and a reader who skips the banner is led to
a materially wrong conclusion. More concretely, this REPORT's node-mass curve
**directly contradicts** the re-run `simulations/REPORT.md`: the simulation
finds a GB300-class 150 kW 1-rack node masses **6.79 t** and flies with ~2.7 t
of margin; this REPORT puts a 150 kW GB300 node at **8.4 t** with only ~0.4 t
margin, and a 300 kW Rubin node at 12.7 t. The two project models disagree by
~1.5–2 t on the same node at the same power. The simulation was re-run; this
data-science REPORT was not. It should be re-run or much more aggressively
caveated — the body text, not just the banner, asserts a superseded verdict.

### S5. `economics/ambition_case.md` §5.2 — the "crosses over sooner" conclusion is asserted, not derived
The doc's headline claim — a ~$17–22B program crosses cumulative break-even at
**~year 13–16, *earlier* than the conservative case's ~year 19–20**:

> "going bigger crosses over **sooner**, not later — in proportional terms
> decisively, and even in raw calendar terms."

is tagged `[DERIVED, order-of-magnitude]` but **no derivation is shown.** The
conservative `INVESTOR_PROJECTION.md` is a year-by-year model with a published
pro-forma table; the ambition case's year-13–16 crossover has no equivalent
table, no cohort schedule, and no cumulative-cash trajectory — it is reasoned
narratively ("revenue scales ~10× while capital scales ~13–18×"). The claim is
counter-intuitive (a 13–18× larger capital program crossing *earlier* in
calendar time) and load-bearing for the doc's verdict, yet it rests on
assertion. The doc's own confidence section concedes the verdict "rests on two
uncited, unobserved assumptions," but the crossover-year mechanics deserve at
least a sketched cumulative-cash table to be credible. Treat the year-13–16
figure as weakly supported.

### S6. Internal contradiction — Neutron first-launch / reusable-mode date
`INVESTOR_PROJECTION.md` states "Neutron's reusable mode is NET 2027" and
deploys zero nodes in years 0–1. Web check (2026-05-17): Rocket Lab's Neutron
**first launch** is NET Q4 2026, with the ramp 1 (2026) → 3 (2027) → 5 (2028).
`ambition_case.md` §2.2 cites "3 Neutron launches in 2027, 5 in 2028, monthly
thereafter" — correct for 2027/2028 but silently drops the 1-launch 2026 debut.
Neither doc is badly wrong, but they describe the Neutron timeline slightly
differently and the "reusable mode NET 2027" phrasing conflates first-flight
with reusable-recovery readiness without sourcing that distinction. Minor-to-
moderate; worth reconciling to a single sourced timeline.

---

## Minor findings

### M1. `economics/ai_datacenter_tam.md` — clean, well-flagged
Cross-checked: McKinsey 156 GW AI / 219 GW total / $5.2T AI capex / $6.7T total
by 2030 all confirmed against McKinsey (web check). The retired $3B/GW proxy is
correctly banner-flagged as superseded (§5). FACT/PROJECTION/ILLUSTRATIVE
tagging is disciplined. No material issue. One small internal-consistency note:
the doc uses "~30 GW operational AI (late 2025)" and "~44 GW AI workload 2026"
and "~156 GW 2030" — the doc itself flags the inconsistent boundary definitions
in Open Question 1, so this is disclosed, not a defect.

### M2. `economics/revenue_per_watt.md` — sound; one residual cross-doc inconsistency it flags itself
CoreWeave $5.13B FY2025 / $66.8B backlog / ~250k GPUs / ~850 MW confirmed via
web check. The §3 reconciled range ($15–20B/GW central) is arithmetically
consistent with both Method A and Method B. The doc openly flags the ~5–10×
conflict with the TAM doc's $3.3B/GW (its §6 cross-check and Open Q1) — that
conflict is resolved at the synthesis level (tracker confirms the $3B/GW proxy
was retired), so the doc is honest about a known issue. No unflagged error.

### M3. `economics/revenue_per_watt.md` — minor stale-revenue caveat
Doc states OpenAI "projected ~$14B loss in 2026" and CoreWeave operating margin
"~-2%". The hyperscaler_margins doc gives CoreWeave operating margin "~-1%".
Small (~1 pt) inconsistency between two project docs citing the same company;
both are "roughly breakeven/slightly negative" so immaterial, but the two docs
should pick one figure.

### M4. `economics/premium_value_case.md` — clean
Strong document. FACT/PROJECTION/ARGUMENT tagging is consistent; every hard
number is cited inline; downside sections (§7–8) are genuinely load-bearing as
claimed. The 2–3-year GPU-life framing in §8 is the *old* obsolescence window
(the project moved to a 5-year base case in wave 8) — but §8 is explicitly the
"honest downside" section and presenting the harsh 2–3-yr figure there is
defensible, not a dead note. No material issue. (If anything, a one-line note
that the project's base case is now 5-yr would tighten it.)

### M5. `economics/hyperscaler_margins.md` — clean; one figure to verify
AWS $128.7B / ~35% margin, Rocket Lab $602M FY2025 / $72B cap / $2.2B backlog /
$1.48B cash, CoreWeave $5.1B / ~-1% op margin all internally consistent and
cross-checked where searchable (Rocket Lab FY2025 confirmed; CoreWeave FY2025
confirmed — note web check shows CoreWeave 2025 **GAAP net loss $1.17B**, i.e.
net margin ~-23%, which the doc states correctly). The "$816M SDA contract"
and backlog figures line up with Rocket Lab's release. NVIDIA ~75–76% GM and
"8–10× markup over BOM" are reported figures, cited. The doc's $500M/$86M
project projections are correctly labelled [PROJECTION] / "not validated here."
No material issue.

### M6. `competitors/starcloud.md` — clean
Starcloud-1 (H100, ~Nov 2025), $170M Series A at ~$1.1B (Mar 2026),
Starcloud-3 (~3 t / 200 kW / Starship / 2028–2029 / ~$500/kg break-even) all
confirmed via web check. Confirmed-vs-estimate flagging is careful. The 88,000-
satellite FCC filing and the 40-MW-class "9–16 Starship launches" radiator
estimate are correctly flagged as external/contested. No material issue.

### M7. `competitors/starship_addendum.md` — clean
Starship flight record (11 flights, 6/5), booster-reused / upper-stage-never-
reused, FCC 1M-satellite filing, xAI merger, ~$500/kg gated on reuse+cadence —
all carefully separated into confirmed vs. projected and cited. The doc's own
"~5 years not 8" correction of the founder's runway thesis is sound and matches
the tracker. No material issue. One tiny note: it states Flight 12 "targeted
~May 19, 2026" as of writing — a dated forward-looking claim, correctly flagged
in Open Questions as to-be-checked.

### M8. `simulations/REPORT.md` — clean and current
This is the re-run model at the corrected ~9.5 t SSO budget. Arithmetic is
internally consistent (1-rack 150 kW node = 6.79 t; reusable ceiling ~251 kW;
expendable ~307 kW; block-upgrade ~363 kW). It agrees with the wave-5 synthesis
~200–250 kW band as it claims. The caveats section is honest about the two
unpublished Rocket Lab numbers. The only cross-doc issue is that it disagrees
with `data_science/REPORT.md`'s node-mass curve (see S4) — but the fault there
is the un-re-run data-science REPORT, not this one. No material issue with this
doc itself.

### M9. `economics/ambition_case.md` — arithmetic spot-checks (otherwise sound)
The fleet/cadence/capital arithmetic checks out: $5B ÷ $16.5M/node ≈ 303 nodes;
420 nodes ÷ 5-yr life ≈ 84 launches/yr; 570 cumulative nodes × $34M ≈ $19B;
$5B − $2.5B depr − $0.6B opex − $0.2B ≈ $1.7B profit. Sourcing/labelling
([CITED]/[DERIVED]/[ASSUMPTION]) is disciplined throughout. The doc is honest
that the cadence ramp (~95/yr vs. Rocket Lab's published ~12/yr) and the
premium-holding assumption are unobserved. The one weak spot is S5 (the
crossover-year claim). Otherwise the doc is a careful, well-flagged scenario.

---

## Summary of severity

- **Significant (6):** S1 stale $50–55M launch basis in `rack_cost_trajectory.md`;
  S2 Vera Rubin rack-price misattributed to NVL144 (it is the NVL72);
  S3 stale $50–55M / "85–90% of node cost" launch basis in
  `energy_operating_costs.md`; S4 `data_science/REPORT.md` body stands on a
  superseded payload budget and conflicts with the re-run simulation; S5
  `ambition_case.md` crossover-year claim asserted, not derived; S6 minor
  Neutron-timeline inconsistency between the two model docs.
- **Minor (9):** M1–M9 — mostly clean docs with small notes.
- **Clean docs (6 of 12):** `ai_datacenter_tam.md`, `premium_value_case.md`,
  `hyperscaler_margins.md`, `starcloud.md`, `starship_addendum.md`,
  `simulations/REPORT.md`. (`revenue_per_watt.md` is effectively clean with two
  tiny notes M2/M3.)

The dominant theme is **launch-cost staleness**: two economics docs
(`rack_cost_trajectory.md`, `energy_operating_costs.md`) were written before
the wave-9 re-base to the ~$10–20M internal launch cost and still run on the
$50–55M external price without a superseded banner — unlike `ai_datacenter_tam.md`,
which models the correct hygiene by banner-flagging its own retired figure.
The data-science REPORT has the analogous problem on the SSO-payload re-base:
it carries a banner but the body still asserts the superseded verdict.
