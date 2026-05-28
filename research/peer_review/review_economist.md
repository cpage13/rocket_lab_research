# Independent Economic Review — RKLB Company Valuation Model

*Reviewer: independent economist / financial analyst. Date: 17 May 2026.
Scope: `valuation/VALUATION_MODEL.md` and its code
(`data_science/src/rklb_analysis/valuation.py`, `valuation_main.py`,
`valuation_plots.py`), cross-checked against the sourced inputs
(`rklb_baseline_financials.md`, `rklb_forward_trajectory.md`) and the prior
project models (`cadence_revenue_model.md`, `INVESTOR_PROJECTION.md`,
`ambition_case.md`, `hyperscaler_margins.md`, `revenue_per_watt.md`,
`CONCLUSION.md`).*

> **This is a REPORT, not an edit.** No file other than this one was modified.
> Findings are ranked by materiality. Each carries a location and a recommended
> fix for the later fix-pass.

---

## Overall verdict

**The model is methodologically clean and unusually transparent — the
two-layer structure, the named-dial discipline, and the with/without-premium
bracketing are all sound — but it carries one genuine accounting error that
overstates venture profit by billions, and its headline operating-profit
numbers are economically incomplete in a way the document acknowledges but
under-weights.** The *revenue* layers are defensible as labelled scenario
outputs. The *profit* layers are not yet trustworthy: a depreciation bug
(Finding 1) and an unfinanced cost of capital (Finding 2) both push reported
profit up, and they compound. The "combined = baseline + venture" addition has
a real double-count the doc's Open Q5 dismisses too quickly (Finding 3). The
direction of the result (venture is material at this scale; premium is
second-order) survives all of this; the *operating-profit dollar figures* do
not. Treat every revenue number as a scenario and every profit number as
currently overstated.

---

## Findings, ranked by materiality

### 1. [CRITICAL — accounting error] Node depreciation is charged on the *attrition-weighted live* fleet, not on *deployed capital*. This understates depreciation by ~40% at steady state and overstates venture operating profit by billions.

**Location:** `valuation.py`, `_project_venture()`, line ~988:
`node_depreciation = fleet_live * node_total / config.service_life`. Documented
in `VALUATION_MODEL.md` §3.5 ("Node depreciation | live-fleet × node-cost ÷
5-yr life").

**The error.** `fleet_live` is the *linear-glide attrition-weighted* fleet — a
rack in its deployment year counts 1.0, then 0.8 / 0.6 / 0.4 / 0.2 as it ages
(`cohort_live_fraction`). The model multiplies *that* declining number by
node-cost ÷ 5. But depreciation is the write-off of **capital actually spent**.
Every rack cost a full ~$45M the year it was built and must be depreciated in
full over its 5-year life — $9M/yr for five years — regardless of how the
attrition curve scores its "liveness." Straight-line depreciation of a $45M
asset is $9M in *each* of years 1–5, not $9M × (1.0, 0.8, 0.6, 0.4, 0.2).

By weighting depreciation with the 0.6-mean attrition glide, the model expenses
only ~60% of the depreciation it should. Over the model window the gap is
**~$26B of un-charged depreciation**: deployed capital years 0–15 is 2,897
racks × $45M = **~$130.4B**; correct straight-line depreciation booked within
the window is **~$86.0B**; the model books only **~$59.8B**. At steady state
the live-fleet depreciation line runs **~40% below** the true straight-line
charge.

**Why this is a true error, not a modelling choice.** The attrition glide is
the right tool for *revenue* (a degraded rack earns less) and arguably for
*opex* (though see Finding 6). It is the *wrong* tool for depreciation:
depreciation does not decline because a rack is ageing — that is precisely when
a straight-line schedule keeps charging. The two uses of `fleet_live` are
conflated. The model even half-acknowledges the asset is fully spent: node
*cost* (`NodeCost.node_total_musd`) is the full ~$45M, but the write-off is then
scaled down by attrition.

**Materiality.** This is the single largest cost line in the venture. Correcting
it lifts venture depreciation at year 15 from ~$12.6B toward ~$21B+ (a
deployed-capital basis) and **cuts venture operating profit by roughly $7–9B at
year 15** — i.e. the with-premium year-15 venture operating profit of ~$9.2B is
closer to ~$1–3B once depreciation is charged correctly, and the
without-premium case (~$4.9B reported) likely goes **negative or near-zero**.
The headline "combined operating profit" and the venture-operating-margin
figures (§3.5: "~38% with premium, ~25% without") are all overstated as a
direct result.

**Recommended fix.** Depreciate **deployed capital**, not live fleet. Compute
annual depreciation as the sum over the trailing 5 cohorts of
`racks_deployed[d] × node_total / service_life` for each cohort still inside its
5-year depreciation schedule (a flat $9M/rack/yr for 5 years). Equivalently:
depreciation in year *y* = node_total/5 × (racks deployed in years *y-4…y*).
This is *un-attrited* cohort accounting. Keep the attrition glide for revenue.
Re-run; expect venture and combined operating profit to fall materially, and
re-state every profit figure in `VALUATION_MODEL.md` §3.5, §4, and the Summary.

---

### 2. [CRITICAL — completeness] The headline stops at operating profit and omits the venture's entire cost of capital. The ~$1–20B+ funding need, interest, dilution, and tax are not netted — so "operating profit" is not an investor-relevant return, and presenting it as the headline is misleading.

**Location:** `VALUATION_MODEL.md` Summary table, §4 headline tables, Open Q6
and Q8; `valuation.py` has no financing, interest, tax, or share-count logic.

**The gap.** The model's headline is "combined operating profit ~$8.7–13.0B at
year 15." But the venture consumes, on the project's own prior numbers,
**~$14–22B of cumulative capital** (`ambition_case.md` §4; `CONCLUSION.md`).
`INVESTOR_PROJECTION.md` shows even the *conservative* ~$500M/yr venture is
cumulative-cash-negative for ~19–20 years. This model's venture is ~20–40×
larger. None of the following is in the model:

- **Node capex timing.** The model expenses depreciation but never models the
  *cash* outlay for nodes, which is spent years ahead of the earnings. A P&L is
  not a cash-flow statement; the venture is deeply cash-negative for ~15+ years
  even where the P&L shows "operating profit."
- **Interest / financing cost.** ~$14–22B raised as debt carries billions/yr of
  interest; raised as equity it is dilution. Either way it sits *below* the
  operating line the model stops at.
- **Tax.** The combined company is a large taxpayer by the back half of the
  horizon (offset partly by RKLB's NOLs — `rklb_baseline_financials.md` Open
  Q8). A 21%+ federal rate on multi-billion operating profit is a material
  haircut to anything an equity holder receives.
- **The baseline's own below-the-line items.** RKLB FY2025 GAAP *operating*
  loss (−$229M) was larger than its *net* loss (−$198M) because of interest
  income on cash (`rklb_baseline_financials.md` §4). The baseline layer
  inherits the same operating-vs-net divergence and the model ignores it on
  both layers.

**Why it matters.** The doc is candid about this (Open Q6, Q8, and the lens
caveat), and that candour is to its credit. But candour in the Open Questions
does not fix a **headline** built on operating profit. An investor or CFO
reading the Summary table sees "$13.0B operating profit at year 15" with no
flag *in the table* that this is pre-financing, pre-tax, and ignores a
~$14–22B capital hole. Operating profit on a capital-intensive venture whose
capital is unfunded in the model is not a return — it is an intermediate line.
Combined with Finding 1, the reported profit is overstated *twice over*.

**Recommended fix.** Two options, in order of rigour: (a) **Best** — extend the
model to a combined-company *cash-flow* statement: node capex as a cash outlay,
a financing schedule (debt or equity) for the venture's funding need, interest,
and a tax line with NOL carryforward. This is the "next workstream" the doc
defers; until it exists, the headline should not be operating profit. (b)
**Minimum** — relabel every "operating profit" figure in the Summary and §4 as
"operating profit (pre-financing, pre-tax; excludes the venture's ~$14–22B
cumulative capital need — see Open Q6/Q8)" *in the table itself*, and add a
"memo: venture cumulative capital required" row so the reader cannot miss the
hole. Do not let the operating-profit number stand unqualified next to a
dollar figure.

---

### 3. [MAJOR — double-count] "Combined = baseline + venture" double-counts launch activity and shared corporate overhead. Open Q5 addresses only launch *revenue* and waves away the rest; the treatment is incomplete.

**Location:** `VALUATION_MODEL.md` §4 ("Combined = baseline + venture"), Open
Q5; `valuation.py` `CombinedYear` (simple addition of the two layers).

Open Q5 makes one correct point: venture launches are priced at *internal cost*,
so they do not inflate baseline launch *revenue*. But "combined = baseline +
venture" has at least three real overlaps the doc does not resolve:

**(a) Launch *cost* and *capacity*, not just revenue.** The venture flies up to
285 dedicated launches/yr. The baseline (Layer 1) is RKLB's existing launch +
Space Systems business growing on a 38%→8% glide. But the baseline's margin
glide to ~50% gross / ~25% operating is *implicitly* a function of Neutron
reaching scale — and Rocket Lab's own 50%-launch-margin target is pegged to
~24 launches/yr (`rklb_forward_trajectory.md` §2.2). A venture flying 100–285
launches/yr **massively spreads Rocket Lab's launch fixed costs** — pads,
range, engine line, mission ops. That fixed-cost absorption would *lift the
baseline launch margin*, or equivalently *lower the venture's internal launch
cost below $20M* (exactly the `ambition_case.md` §3 amortization argument). The
model takes neither benefit: baseline margins are independent of venture
cadence, and venture launch cost is a flat $20M. The two layers are modelled as
if they share no infrastructure — but they share all of it. This is a
*conservative* inconsistency (it understates the synergy), but it is still an
inconsistency, and it means "baseline + venture" is not a clean sum.

**(b) Corporate / program overhead.** The venture layer carries its own R&D
ramp ($80M→$40M/yr) and the baseline carries RKLB's full GAAP operating-margin
glide (which includes all of RKLB's SG&A and R&D). A combined company runs
**one** finance/legal/HR/exec function, not two. Some of the venture's "program
overhead" would in reality be absorbed by — or would inflate — corporate SG&A
already inside the baseline operating margin. Adding a standalone venture
overhead line on top of a baseline that already contains a full corporate cost
structure modestly double-counts overhead. The doc does not address this at
all.

**(c) The 2-racks/launch block upgrade is a vehicle the baseline arguably also
benefits from.** From year 5 the venture assumes an uprated Neutron carrying
2 racks. That uprated vehicle, if it exists, also serves baseline launch
customers (more payload, better economics). The baseline is frozen as if the
block upgrade never happened. Again conservative for the baseline, but it means
the two layers describe two inconsistent versions of Rocket Lab's vehicle.

**Materiality.** (a) and (c) bias the *combined* result *down* (unmodelled
synergy); (b) biases it *up* (double-counted overhead). They do not cleanly
cancel and they are not quantified. The deeper point: **a true company
valuation should be a sum-of-the-parts with a shared cost structure, not an
arithmetic sum of two independently-grown P&Ls.** The doc's own §7 and lens
caveat gesture at sum-of-the-parts as "a later step" — that later step is
exactly what is needed to make "combined" legitimate.

**Recommended fix.** (i) Rewrite Open Q5 to cover launch *cost/capacity*
synergy and corporate-overhead overlap, not only launch revenue. (ii) At
minimum, state explicitly that the combined figure is a *gross sum that ignores
both the fixed-cost-absorption synergy (which would help) and the
corporate-overhead overlap (which is double-counted)*, and that the net of the
two is unquantified. (iii) Ideally, model the venture's launch cadence as
feeding Rocket Lab's launch fixed-cost base — i.e. let venture cadence pull the
internal launch cost down a curve (the `ambition_case.md` §3.2 curve), which
also partially answers Finding 7.

---

### 4. [MAJOR — internal consistency] The reconciliation with `cadence_revenue_model.md` is only *partly* valid. The block upgrade explains the fleet size, but the per-rack revenue is anchored differently, and the doc presents the reconciliation as cleaner than it is.

**Location:** `VALUATION_MODEL.md` Summary ("A note on scale"), §3.2, §7.

The doc claims its >$10–15B venture revenue is consistent with
`cadence_revenue_model.md`'s "~$10–15B Neutron ceiling" because this model
carries the 2-racks/launch block upgrade, which is the cadence model's
"2-nodes-per-launch" variant (~$19B/yr at year 12). **The fleet-size half of
that reconciliation is valid** — 2 racks/launch genuinely doubles the fleet and
the cadence model's 2-node variant does reach ~$19B. But two things are glossed:

**(a) Different per-rack revenue anchors.** `cadence_revenue_model.md` §3 uses a
per-*node* revenue curve decaying **$15.5M → $10.0M**. This valuation model uses
a hyperscaler-anchor-×-premium construction yielding per-rack revenue of
**$24.0M → $17.1M** (with premium) or **$16.0M → $14.1M** (without). These are
*not the same revenue basis* — the valuation model's per-rack revenue is
**~40–70% higher** than the cadence model's at comparable fleet sizes, even in
the without-premium case ($14.1M vs ~$10–11.5M at ~1,000+ nodes). So this model
reaches a higher number than the cadence model's *2-node variant* would on the
cadence model's *own* revenue curve. The reconciliation attributes the whole
gap to the block upgrade; in fact part of it is a richer per-rack assumption.
The two models are *not* "consistent in method" on revenue, contrary to §7's
claim ("the same $16M inference-service anchor"): the cadence model does **not**
use a $16M anchor — it uses a $15.5M→$10M decay curve that already bakes the
premium in, whereas this model uses $16M **plus** a separate +50% premium. That
is a real divergence in construction.

**(b) The cadence model calls ~365/yr "~2.2× the all-time world launch record"
and "the outer edge of physical credibility."** This model's ramp peaks at
285/yr — below 365, but still ~1.7× SpaceX's 2025 record of 165 and ~24× Rocket
Lab's published ~12/yr plan. The doc flags the ramp as "aggressive" (§3.1) but
does not carry across the cadence model's much starker framing that a single
operator at this rate is near a physical wall requiring multiple pads and an
industrial engine line.

**Materiality.** Moderate-to-major for credibility. The headline "this is
consistent, not contradictory" is *half* true and is stated with more
confidence than the underlying numbers support. A CFO comparing the three
project models will find the revenue bases do not line up.

**Recommended fix.** In "A note on scale" and §7, state plainly: (i) the
block upgrade explains the *fleet-size* doubling; (ii) *separately*, this model
uses a higher per-rack revenue basis ($16M anchor + explicit premium) than the
cadence model's $15.5M→$10M decay curve, and that difference also contributes
to the higher number — quantify it; (iii) drop or correct the §7 claim that
this model uses "the same $16M inference-service anchor" as `cadence_revenue_
model.md` (it does not — the cadence model uses a different, premium-inclusive
curve). Carry across the cadence model's "near the physical launch ceiling"
framing for the 285/yr ramp.

---

### 5. [MAJOR — load-bearing assumption] The +50% premium is applied *on top of* a $16M anchor that, per the project's own sources, may *already include* a large premium. This risks double-counting the orbital premium.

**Location:** `valuation.py` `HYPERSCALER_RACK_REVENUE_MUSD = 16.0`,
`OrbitalPremium.headline_premium = 0.50`, `PerRackRevenue.per_rack_musd`;
`VALUATION_MODEL.md` §3.4 Steps A–B.

The model's revenue methodology is: per-rack revenue = $16M hyperscaler anchor
× (1 + orbital premium). The doc calls $16M "what a hyperscaler makes per rack
today" — the *without-premium* base. But check the source. `revenue_per_watt.md`
§2–3 finds a GB200 NVL72 rack grosses **~$5.6–14.5M/rack-year at the IaaS
layer** — i.e. the *hyperscaler / GPU-rental* number is **below $16M**. The
$16M figure is the **inference-service (token-selling)** rate (`revenue_per_
watt.md` §6, §4), which `revenue_per_watt.md` itself says earns "**a multiple of
the underlying GPU rental cost**" — the token-value markup is *already a
premium* over the raw-rack hyperscaler rate.

So the "without-premium" base is not actually hyperscaler-rack parity; it is the
**inference-service** rate, which already sits above IaaS. Then the model adds
another +50% on top. The +50% headline case is therefore plausibly a
**premium-on-a-premium**: inference-value markup × orbital scarcity premium.
`hyperscaler_margins.md` Open Q3 flags exactly this trap ("the orbital premium
is a premium on an already-elevated base"). The model's §3.4 does not
acknowledge that its $16M anchor is itself the elevated (inference-service)
basis rather than the hyperscaler-IaaS basis the prose implies.

**Materiality.** Major. If the "without-premium" case should really be anchored
at the IaaS rate (~$8–14.5M, not $16M), the *with-premium* case is overstated by
the gap. This is load-bearing for the entire venture revenue layer.

**Recommended fix.** Either (a) re-anchor the without-premium case to the IaaS
rack rate (`revenue_per_watt.md` §2–3, ~$8–14.5M) and keep $16M-equivalent as
the *with-inference-model* case — making explicit that selling tokens is itself
a value-capture choice — or (b) keep the $16M anchor but state clearly in §3.4
that $16M is the **inference-service** rate (already above hyperscaler IaaS),
that the model presupposes Rocket Lab captures a competitive frontier model's
token margin (the `CONCLUSION.md` §3 caveat: "the favorable verdict holds *only*
under the inference-service model"), and that the +50% premium therefore stacks
on an already-elevated base. The current §3.4 prose ("what a hyperscaler makes
per rack today") is misleading and should be corrected regardless.

---

### 6. [MODERATE] Node opex is also charged on the attrition-weighted live fleet — defensible but worth a second look — and the venture has no commissioning lag, both of which flatter early-year venture profit.

**Location:** `valuation.py` `node_opex = fleet_live * vc.node_opex_musd_per_year`;
`VALUATION_MODEL.md` §3.5; Confidence section ("no commissioning-lag haircut").

Two smaller items that compound with Finding 1:

(a) **Opex on live fleet.** Unlike depreciation, charging opex on the
attrition-weighted fleet is arguably *defensible* — a partly-failed rack does
need less station-keeping/ops. But it is not obviously right either: a
satellite still needs station-keeping, ground contact, and ops staff regardless
of how many of its GPUs still work. At minimum the choice should be stated. A
more conservative model would charge opex on the **physically-on-orbit** fleet
(cohorts within the 5-year life, un-attrited), which would raise the opex line
~40% at steady state.

(b) **No commissioning lag.** The doc states (Confidence section) that a node
earns from its deployment year — "the optimistic choice." `INVESTOR_PROJECTION
.md` deliberately applies a one-year lag; `cadence_revenue_model.md` deliberately
does *not*. This model follows the cadence model. That is internally defensible
but it means revenue (and profit) in every ramp year is pulled forward ~12
months versus the investor pro-forma. Combined with Finding 1, early-year
venture profit is flattered from two directions.

**Materiality.** Moderate. (a) is a judgement call worth surfacing; (b) is
already disclosed but its profit effect is not quantified.

**Recommended fix.** State the opex basis explicitly and consider charging it on
the un-attrited on-orbit fleet. Quantify the commissioning-lag effect (re-run
with a one-year lag as a sensitivity) so the reader sees the swing.

---

### 7. [MODERATE] The flat $20M internal launch cost is internally inconsistent with a model whose venture cadence ramps to 285/yr — the project's own sources say launch cost moves with cadence in *both* directions.

**Location:** `valuation.py` `LAUNCH_COST_INTERNAL_MUSD = 20.0`;
`VALUATION_MODEL.md` §3.5 launch-cost caveat, Open Q3.

The doc flags the $20M launch cost honestly (the caveat is good) and notes
~$25M is implied by Rocket Lab's 50%-margin-at-24-launches target, while
`ambition_case.md` argues it amortizes toward ~$10M at high cadence. The doc
calls holding it flat "the conservative choice." **But it is not unambiguously
conservative — it is internally inconsistent.** This model's venture flies
1 → 285 launches/yr. Over that range:

- At the *low* end (1–3/yr, years 1–2), `rklb_forward_trajectory.md` §2.2 says
  the supportable figure is **~$25M** (the 24/yr-cadence implied cost) or
  *higher* — early, low-cadence launches cost *more* than $20M, not less. The
  model uses $20M, understating early node cost.
- At the *high* end (100–285/yr, years 10–15), `ambition_case.md` §3.2 puts the
  cost at **~$8–10M** through fixed-cost spreading and reuse. The model uses
  $20M, *overstating* late node cost — and therefore *overstating* late-year
  depreciation.

So a flat $20M is too low early and too high late. It is not "conservative"; it
is a single point standing in for a curve that the project's own documents
describe. The interaction with Finding 1 matters: the correct late-year launch
cost (~$10M) is *lower*, which partially offsets the depreciation correction —
but the correct *early* cost is *higher*. The net is unclear precisely because
the model refuses to use the curve.

**Materiality.** Moderate. Launch is ~45% of node cost; node cost drives the
single largest venture cost line.

**Recommended fix.** Replace the flat `LAUNCH_COST_INTERNAL_MUSD` with a
cadence-indexed launch-cost curve (the `ambition_case.md` §3.2 schedule:
~$25M at low cadence → ~$20M → ~$12M → ~$10M as annual cadence rises). This
makes node cost — and depreciation — vary correctly by deployment year, and it
also feeds Finding 3's launch-fixed-cost synergy. If a flat value is retained
for simplicity, stop calling it "conservative"; call it "a single-point
approximation of a cost that the project's sources say falls from ~$25M to
~$10M across the cadence range."

---

### 8. [MODERATE] The baseline 38%→8% growth glide is broadly reasonable but the *near* years are internally inconsistent, and the deceleration is arguably too shallow given the consensus already implies a fade.

**Location:** `valuation.py` `BaselineGrowth` (`start_growth = 0.38`,
`terminal_growth = 0.08`); `VALUATION_MODEL.md` §2.2.

The construction (FY2026/27 consensus, then a geometric fade) is sound and the
endpoints are individually defensible. Three observations:

(a) **The year-2 growth is internally inconsistent with the consensus it
follows.** Consensus growth FY2025→26 is +46.7% and FY26→27 is +47.2% (baseline
CSV). The glide then *drops* to 38% in FY2028. A fade from ~47% to 38% in one
year, then a smooth geometric decay, is a kink, not a glide — the deceleration
is discontinuous at the consensus/model seam. `rklb_baseline_financials.md` §7
gives the post-2022 organic CAGR as ~41.9%; setting `start_growth` *below* that
(38%) while the immediately-prior two years run at ~47% is a modelling choice
that should at least be smoothed (e.g. start the fade at ~44–45% and decay from
there).

(b) **The terminal 8% is reasonable** for a mature space prime and is not the
issue.

(c) **The glide produces a ~16× revenue increase over 15 years** ($601.8M
FY2025 → $15.19B FY2041), a ~19.5% CAGR sustained for 15 years. That is
defensible *if* Neutron and Space Systems both scale as bulls expect, but it is
on the *optimistic* side for a "baseline without the venture" — it is closer to
a success-case baseline than a neutral one. The doc calls the glide "the most
important and most uncertain dial in Layer 1" (correct) but does not note that
the chosen path is a fairly bullish read. A genuine *range* (a low/central/high
glide) would be more honest than a single 38%→8% path, given there is no
analyst anchor past FY2027.

**Materiality.** Moderate. The baseline drives the "without venture" comparator
and the lens denominator; a materially lower glide would shrink the baseline by
billions and *raise* the venture's apparent uplift %.

**Recommended fix.** (i) Smooth the consensus→glide seam so year-2 growth is not
a downward kink. (ii) Present the baseline as a low/central/high band rather
than one path, or explicitly label the 38%→8% path as a "moderately bullish
baseline" and show one lower alternative. (iii) Note in §2.2 that a 15-year
~19.5% CAGR is itself an aggressive read for a pre-venture baseline.

---

### 9. [MINOR — but should be fixed] The illustrative 12× revenue multiple is applied to *baseline* and *combined* revenue identically — but a launch/Space-Systems company and an orbital-compute platform do not trade at the same multiple. The lens's "ratio is multiple-invariant" defence partly fails.

**Location:** `valuation.py` `valuation_lens()`, `ValuationLens`;
`VALUATION_MODEL.md` §4 "The illustrative valuation lens."

The lens is correctly and repeatedly labelled illustrative, and the doc's
instinct that "the ratio is the informative part" is reasonable. But the lens
applies **one** 12× multiple to both the baseline and the combined company. The
doc's own claim that the ratio is "multiple-invariant" is only true *if both
businesses warrant the same multiple*. They plausibly do not: a recurring,
services-style orbital-compute revenue stream would, on the doc's own
`hyperscaler_margins.md` §4 reasoning, command a *different* (likely higher)
multiple than lumpy launch revenue. If the venture revenue deserves, say, 15×
and the baseline 10×, the combined-vs-baseline EV ratio is **not** the revenue
ratio, and the "multiple-invariant" claim breaks.

**Materiality.** Minor — the lens is explicitly illustrative and the doc says
not to read the dollars. But the *specific* claim that the ratio is
multiple-invariant is overstated and a reader may lean on it.

**Recommended fix.** Either soften the claim ("the ratio is multiple-invariant
*only if the two businesses warrant the same multiple, which they may not*"), or
make the lens a genuine 2-multiple sum-of-the-parts (one multiple for the
launch/Space-Systems baseline, one for the orbital-compute venture). The latter
is also the honest precursor to the "rigorous sum-of-the-parts" the doc defers.

---

### 10. [MINOR] The `HYPERSCALER_RACK_MARGIN = 40%` dial is defined, documented, and then never used in any computed result — it is dead weight that implies a margin cross-check the model does not actually perform.

**Location:** `valuation.py` `HYPERSCALER_RACK_MARGIN = 0.40` and the
`PerRackRevenue` / docstring references; `VALUATION_MODEL.md` §3.4 Step A.

The 40% hyperscaler margin anchor is presented as a dial with a full basis
(`hyperscaler_margins.md` §1.1). The doc says "the model's *actual* venture
profit is built bottom-up … not from this margin; the 40% figure is the
reference anchor." But it is never used as a *cross-check* either — no result,
figure, or table compares the model's bottom-up venture margin against the 40%
reference. It is a defined constant with zero effect on any output.

**Materiality.** Minor / cosmetic — but in a model whose entire selling point is
"every dial matters and nothing is buried," an inert dial that implies a
cross-check that does not happen is a small credibility cost.

**Recommended fix.** Either (a) actually perform the cross-check — add a line or
figure comparing the venture's modelled operating margin to the 40% hyperscaler
reference (this would, post-Finding-1, usefully show the corrected venture
margin landing *below* 40%, which is the honest result) — or (b) remove the
constant and the §3.4 Step A reference to it.

---

## What the model gets right (for balance)

- **The two-layer structure** (baseline / venture / combined) is the correct
  frame for a "what is the venture worth to the company" question, and is a
  genuine advance over the three prior venture-only models.
- **Named-dial discipline.** Every assumption is a documented, defaulted,
  CITED/ASSUMPTION-tagged field. This is exemplary and makes the model
  auditable — it is *why* this review could find Finding 1 at all.
- **The FY2025 base and FY2026/27 consensus anchors** are correctly sourced and
  match `rklb_baseline_financials.md` / `rklb_forward_trajectory.md` exactly.
- **With/without-premium bracketing** is the honest way to handle an unobserved
  willingness-to-pay, and the doc consistently reports both.
- **The premium decay** (log-linear, headline→floor with fleet size) is a
  sound shape and is correctly carried from `cadence_revenue_model.md` §3 in
  *method*.
- **The node-cost build-up** ($7M rack + $18M spacecraft + $20M launch = ~$45M)
  is correctly carried from `CONCLUSION.md` Rev 4 — the *level* is consistent
  with the prior docs (the launch-cost *curve* issue in Finding 7 aside).
- **The Confidence and Open Questions sections** are unusually candid and flag
  most of the right risks — the failure is one of *placement* (Findings 1–3
  belong in the headline, not only the Open Questions) and of *one missed
  error* (the depreciation bug, which no Open Question catches).

---

## Bottom line for the fix-pass

Priority order: **Finding 1 (depreciation bug) must be fixed first** — it is a
true accounting error, it is mechanical to correct, and every profit number in
the document is wrong until it is. **Finding 2** (relabel/extend past operating
profit) and **Finding 3** (the double-count in "combined") are next — they are
about not letting an incomplete number stand as a headline. **Findings 4 and 5**
(the cadence-model reconciliation and the premium-on-a-premium anchor) are
about honest presentation of the revenue layer. Findings 6–10 are refinements.

After Finding 1 alone, expect venture and combined *operating profit* to fall by
several billion dollars at years 10 and 15, the venture *operating margins* in
§3.5 to drop well below the stated 38%/25%, and the without-premium venture to
move close to break-even. The *revenue* headlines and the qualitative
conclusion (venture is material; premium is second-order; fleet scale is
first-order) are not affected and remain sound. The model's bones are good; its
profit numbers are not yet trustworthy.
