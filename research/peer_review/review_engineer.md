# Engineering Review — Physical Assumptions Behind the Company-Valuation Model

*Independent review, 2026-05-17. Reviewer: aerospace / systems engineer.
Scope: the **engineering and physical premises** that feed
`valuation/VALUATION_MODEL.md` and `data_science/src/rklb_analysis/valuation.py`
— not the finance. **Report only; no files edited** (a separate fix pass applies
corrections — the project's standard pattern).*

---

## Overall verdict

The model's *method* — a venture-dedicated cadence ramp → racks → attrition-weighted
live fleet → revenue/profit — is sound, transparent, and consistent with the prior
project models. The **node-mass / one-rack-per-launch architecture is correctly
carried**, and the model is honest that the cadence ramp is its load-bearing
assumption. But the engineering premises break in three material places, and in
each case **the model is more optimistic than the project's own prior research**:

1. The cadence ramp's **upper half is physically incredible** — it ends *above*
   the three-pad theoretical ceiling of the most cadence-optimized rocket on Earth.
2. The **5-year service life is the wrong number for the depreciation/attrition
   engine** — the reliability doc models a **3-year** GPU life; the project's
   "5-year life" is a *go/no-go unknown stated as a minimum requirement*, not a
   safe planning figure, and the model treats it as fact.
3. **"2 racks/launch from year 5"** is not how the project's own engineering says
   a bigger Neutron behaves — it contradicts `node_mass_model.md` and
   `simulations/REPORT.md` directly.

These are material because the venture layer's entire output scales with
(cadence × racks-per-launch ÷ service-life). The model's headline — venture
"roughly doubles" Rocket Lab — rests on a fleet size that the project's own
physics docs do not support at the upper end. **Confidence in the venture layer's
year-12–15 numbers: low.** The year-0–8 portion is far more defensible.

Findings are ranked by materiality below.

---

## Finding 1 — The cadence ramp's upper half is physically incredible (CRITICAL)

**Location:** `VENTURE_CADENCE_RAMP` in `valuation.py` (lines 315–340);
`VALUATION_MODEL.md` §3.1.

**The ramp:** `0,1,3,7,14,25,42,62,80,92,100,130,165,205,250,285` launches/yr.

**The problem.** The model and write-up flag years 3+ as "aggressive" and
"demand-pulled" — but they frame the *whole* feasibility question as "is there
demand?" That is the wrong frame for the back half. Even with the data center as
its own anchor (unlimited demand), the ramp runs into a hard **supply-side / pad
/ range wall** that the project has already quantified in `economics/moonshot_50b.md`
§3.2–3.3:

- **The all-time annual launch record by *any operator in history* is SpaceX's
  165 (2025)** — the progression 25→31→61→96→134→165 took SpaceX ~5 years with a
  mature, deeply-reused vehicle and multiple pads.
- **The *theoretical* three-pad Falcon 9 ceiling is ~209/yr** (assuming SpaceX's
  *record* 4-day pad turnaround, not its average) — per-pad turnaround is "the
  fundamental limiting factor."
- A single pad supports **~40–55/yr at a realistic 7–10-day turnaround, ~90/yr at
  a heroic 4-day** turnaround.

Against those reference points, the ramp's later years are not credible:

| Model year | Ramp value | Reality check |
|---|---|---|
| Year 10 (FY2036) | **100/yr** | ≈ `ambition_case.md`'s ~95/yr steady state — *aggressive but precedented in kind*. Needs **2–3 dedicated Neutron pads**, a hundreds/yr Archimedes line, an industrial 2nd-stage line. The credible upper edge. |
| Year 12 (FY2038) | **165/yr** | Equals **the entire human launch record**, set by SpaceX with ~15 years of reuse maturity. Neutron would be ~10 years from first flight. Not credible. |
| Year 13–15 | **205 → 250 → 285/yr** | **Above the ~209/yr three-pad theoretical Falcon 9 ceiling.** 285/yr ≈ one Neutron launch every ~1.3 days. Requires ~6–12+ Neutron pads on a finite set of US coastal SSO-capable ranges. **Physically incredible on Neutron within the model horizon.** |

`rklb_forward_trajectory.md` §5 independently confirms Rocket Lab's published
Neutron plan tops out at ~12/yr ("monthly") and the contestable external market
is ~30–50/yr; even `ambition_case.md` — the project's deliberately optimistic
document — caps its scenario at ~95–115/yr and calls *that* "the single largest
stretch... near the edge of credible." **This model's ramp exceeds the ambition
case by ~3× at year 15.**

**Where it breaks, and at what number.** It is defensible to ~100/yr (year 10)
*if* the venture funds 2–3 pads and the engine/stage lines. It breaks somewhere
in the **~150–200/yr band** — i.e. **years 12–13** — and is not physical above
~209/yr (the three-pad ceiling) regardless of capital. Roughly **half of the
year-11–15 ramp is unsupportable.**

**Materiality.** Very high. The cadence ramp is the first-order driver of fleet
size and therefore of venture revenue. The model's year-15 venture revenue
(~$24B) and the headline "+157%" rest substantially on launches 165→285/yr,
which the project's own moonshot analysis classifies as infeasible-on-Neutron
territory. Note the structural tie-in to `CONCLUSION.md` Revision 8: the project
*already concluded* "on Neutron this venture tops out at ~$5–10B/yr" precisely
because cadence cannot exceed ~100–150/yr. **This valuation model's venture layer
peaks at ~$24B/yr — 2–3× above the project's own stated Neutron ceiling — and the
reason is this ramp.**

**Recommended fix.** Cap the ramp at a physically defensible plateau. A ~100–130/yr
plateau from year 10–11 (consistent with `ambition_case.md` and a 2–3-pad,
fully-reused Neutron) is the honest upper bound. If the model wants to show
revenue above the ~$5–10B Neutron ceiling, it must explicitly invoke the
`CONCLUSION.md` "Act II" bigger-rocket — and then it is no longer a Neutron model.
At minimum, add a hard annotation that years 12–15 of the ramp exceed the all-time
world launch record and the three-pad Falcon 9 theoretical ceiling, and treat
those years as a labelled bigger-rocket scenario, not baseline.

---

## Finding 2 — 5-year service life is optimistic for the depreciation/attrition engine (HIGH)

**Location:** `SERVICE_LIFE_YEARS = 5` in `valuation.py` (line 289); used in the
live-fleet cohort sum, the linear-glide attrition, *and* the node-depreciation
cost line (lines 969–988); `VALUATION_MODEL.md` §3.3.

**The problem.** The model tags `SERVICE_LIFE_YEARS = 5` as "CITED — CONCLUSION.md
Rev 3 base case." That citation is technically accurate but materially misleading
about the *status* of the number:

- `CONCLUSION.md` §2 is explicit that the 5-year life is a **"proposal minimum
  requirement"** and **"an engineering requirement the design must meet and
  verify, not an optimistic hope"** — i.e. an *unproven target*, and one of the
  project's named **go/no-go unknowns**. The honest outcome band stated there is
  **~3.5–7 years**, "and the economics fail at the bottom of it."
- The dedicated reliability research, `node_design/reliability_failure_handling.md`,
  **models a 3-year life throughout** (§1, §5 degradation table: "over a 3-year
  life," 100%→92%→85%→78% surviving compute). Its planning numbers — ~7–9% GPU
  AFR, cumulative ~15–25% loss — are derived on a **3-year** mission. The 5-year
  figure is a *management/economics* choice layered on top of reliability work
  that itself assumes 3.

So the model's most-conservative-sounding "CITED" dial is in fact the optimistic
end of a contested range, and the reliability subsystem analysis points lower.

**Why it is doubly material — it feeds two lines, both the wrong way.**
1. **Fleet size.** Live fleet = trailing-5-year cohorts. A 3-year life cuts the
   steady-state fleet (cadence × life) by ~40%. The "~510 live racks at year 10 /
   ~1,400 at year 15" both shrink ~40% on a 3-year life.
2. **Node depreciation.** `node_depreciation = fleet_live × node_total ÷
   service_life`. The model divides ~$45M node cost over 5 years. On a 3-year
   life, annual depreciation per node rises from $9M to $15M — a +67% jump in the
   venture's *single largest cost line*. The two effects partly offset on revenue
   but **compound against profit**: smaller fleet *and* higher per-node
   depreciation.

This is the same load-bearing risk `INVESTOR_PROJECTION.md` and `ambition_case.md`
both flag ("a 2–3-yr effective life... breaks the margin"). The valuation model
inherits the risk but, unlike those docs, does not run a downside case on it.

**The attrition glide is internally inconsistent with the life.** A separate,
smaller issue: the model imports `cohort_live_fraction` to apply a linear glide
100%/80%/60%/40%/20%. The reliability doc's actual degradation curve is far
gentler — ~100%→92%→85%→78% over 3 years (a graceful glide to ~75–85% of BOL, not
to 20%). The model's linear glide is not modelling *capacity* degradation; it is
a crude proxy for *cohort retirement timing*. That is defensible as a
fleet-accounting smoother, but the write-up's claim that it reflects the
reliability doc's "graceful glide" is loose — the reliability doc's glide bottoms
at ~78%, not 20%. Low materiality, but the provenance claim should be corrected.

**Materiality.** High. The 5-year life is one of two or three numbers that move
the venture layer most, and the model presents it with more certainty than the
source documents carry.

**Recommended fix.** Keep 5 years as the base case (it is the project's stated
base case) but (a) re-tag it `ASSUMPTION — proposal minimum requirement, not yet
demonstrated; honest band 3.5–7 yr` rather than a flat `CITED`, and (b) run the
venture layer at 3-year and 7-year service life as a documented sensitivity, the
way `INVESTOR_PROJECTION.md` and `ambition_case.md` do. The 3-year case is the one
that matters — it is what the reliability doc actually models, and it cuts the
fleet ~40% while raising depreciation ~67%.

---

## Finding 3 — "2 racks/launch from year 5" misrepresents the block upgrade (HIGH)

**Location:** `BlockUpgrade` dataclass (`valuation.py` lines 345–374),
`racks_after = 2`; `VALUATION_MODEL.md` §3.2.

**The problem.** The model represents the Neutron block upgrade as a step from 1
to **2 racks per launch** at year 5. The project's own engineering work directly
contradicts this:

- `node_design/node_mass_model.md` §6–§7: a **2-rack node masses ~10.7–27.1 t
  (mid ~16.6 t)** and "**exceeds even the expendable budget**." The doc's verdict
  is unambiguous: "**one rack per node, one node per Neutron launch**" — at *every*
  configuration.
- `simulations/REPORT.md` §4–§6: a 2-rack node is "**over the mass budget from
  the very start**... **never flyable on Neutron in either recovery mode**,"
  including on the **block-upgraded** Neutron (~12.5 t SSO).
- `CONCLUSION.md` is explicit: "**No 2-rack Neutron node is ever needed**" and
  "**V2 needs no 2-rack node**." The block upgrade is described there as buying
  "**one more *power* generation per single-rack node, not a second rack**" — it
  lifts the per-node power ceiling from ~250 kW to ~363 kW, *not* the rack count.

So the model's central mechanism for the post-year-5 revenue step — literally
doubling racks-per-launch — is the **one architecture the project spent five
research waves ruling out.** A block-upgraded Neutron is still a *one-rack*
vehicle; the upgrade gives that single rack more mass/power headroom (a hotter,
denser Rubin-class rack), not a second rack.

**Note the write-up half-acknowledges this and then proceeds anyway.** `node_mass_model.md`
is cited in the docstring ("notes a 2-rack node needs a bigger / uprated
vehicle") — but `node_mass_model.md` does *not* say that; it says a 2-rack node
exceeds even the *expendable* and block-upgraded budgets and should not be built.
The model is reading the source backwards.

**Is "2 racks/launch" the right way to model a bigger vehicle?** No — and this is
the deeper point. A bigger/uprated vehicle, on this project's physics, shows up as
**more power and revenue *per single-rack node*** (a higher-power Rubin/Rubin-Ultra
rack flying where a GB300 flew), not as more racks per launch. If the model wants
a post-year-5 step-up, the engineering-correct levers are:
- **higher per-rack revenue** (a bigger node hosts a higher-power, higher-throughput
  rack — Rubin-class ~300 kW vs GB300 ~150 kW), or
- **two laser-meshed single-rack satellites** for a model too big for one rack
  (`CONCLUSION.md`: "split across two laser-linked single-rack satellites") —
  which is *two launches*, not one, so it does not multiply racks-per-launch
  either.

Modelling the upgrade as "2 racks/launch" is a clean arithmetic doubling that
happens to have no physical referent on Neutron.

**Materiality.** High. The block upgrade is, per the write-up's own §3.2, "**why
venture revenue here exceeds the 1-rack cadence ceiling**" — i.e. it is the second
of the two first-order venture drivers. From year 5 it doubles racks deployed for
a given cadence. If it is not physical, roughly **half the venture's deployed
racks from year 5 onward** are an artefact.

Also note the **timeline**: a ~5-year window to *any* block-upgraded Neutron is
itself optimistic. `payload_and_block_upgrade.md` §5 states no block upgrade is
announced, there is no public Neutron growth roadmap, and Electron's one
in-service uprate came **~3 years after its debut** — so a block upgrade ~5 years
after a *first flight* that is itself NET Q4 2026 (i.e. block upgrade ~FY2031) is
at the optimistic edge but not unreasonable *for a power uprate*. It is the
"2 racks" content, not the year-5 timing, that is wrong.

**Recommended fix.** Remove the racks-per-launch doubling. Model the block upgrade
the way the project's engineering does: as a **per-node power/revenue uplift**
(the post-upgrade node hosts a higher-power rack) applied to a fleet that stays
**1 rack = 1 node = 1 launch**. If the modeller wants to preserve the headline
revenue scale, the honest route is a higher `hyperscaler_anchor` for post-upgrade
Rubin-class nodes — not `racks_after = 2`. As written, the dial silently
re-introduces the 2-rack node the entire project rejected.

---

## Finding 4 — node = 1 rack = 1 satellite = 1 launch: SOUND (no change)

**Location:** `VALUATION_MODEL.md` §3; `valuation.py` header comment line 281.

This identity is correct and well-supported. `node_mass_model.md`,
`simulations/REPORT.md`, and `CONCLUSION.md` all converge on it: a 1-rack node at
GB300 power (~150 kW) masses ~6.8 t against a ~9.5 t reusable-to-SSO budget — it
flies reusable with margin, and the architecture is cleanly, near-linearly
scalable by adding replica satellites. **The model's base unit is right.** (The
only caveat is Finding 3 — the model then *breaks* this identity at year 5 by
putting 2 racks on one launch. Fix Finding 3 and the identity holds throughout,
which is the correct state.)

One genuinely missing physical caveat worth a line: `simulations/REPORT.md` shows
the 1-rack node is **mass-bound and stops flying reusable at ~251 kW**. The model
implicitly assumes every node flies reusable at the cheap $20M internal launch
cost. A Rubin-class node power-capped to ~190–250 kW stays inside that — but if a
post-upgrade node runs uncapped (~300 kW Rubin), `REPORT.md` says it needs the
block-upgraded vehicle (~363 kW ceiling) or an expendable flight. That interacts
with launch cost (expendable forfeits booster reuse). Not first-order, but the
model's flat $20M launch cost quietly assumes the node always stays in the
reusable mass box.

---

## Finding 5 — Fleet scale: burn-in throughput is an un-modelled cadence constraint (MEDIUM)

**Location:** the live-fleet computation generally; not represented anywhere in
`valuation.py`.

The raw fleet sizes — ~510 live racks at year 10, ~1,400 at year 15 — are not
themselves physically problematic *as constellation management*: LEO constellations
of 1,000–7,000+ satellites exist (Starlink). Deorbit/debris is benign here — the
project docs note dawn-dusk SSO at 500–600 km gives largely-natural FCC-5-year
deorbit compliance. Ground segment is costed (lean ~$150M). So fleet *size* per se
is fine.

**But one physical constraint on the *deployment rate* is entirely absent: ground
burn-in throughput.** `node_design/reliability_failure_handling.md` §3 and Open
Q6 are explicit:
- Credible space-acceptance burn-in is **~1–3 weeks per rack** (≥200 h), not the
  founder's original 1–2 days. `CONCLUSION.md` §2 accepts this ("burn-in (1–3
  weeks, not 1–2 days)").
- Open Q6 asks directly: "**A 1–3 week per-rack burn-in is a real constraint on
  launch cadence and capital turns. How many burn-in stations are needed to
  sustain the deployment rate?**"

At the ramp's peak (285 racks/yr deployed, or ~570/yr after the 2-rack doubling),
sustaining the flow needs **dozens of parallel rack-level burn-in + TVAC +
vibration stations** running continuously. That is real capital and real facility
throughput that (a) is not in the model's cost lines and (b) is itself a *rate
limiter* on how fast the fleet can physically be built — independent of launch
cadence. It is a second throughput wall behind the pad wall of Finding 1.

**Materiality.** Medium. It does not change the verdict, but it is a named
open question in the project's own reliability doc that the valuation model
neither costs nor flags. At the fleet scales this model runs, it is non-trivial.

**Recommended fix.** Add a burn-in / integration throughput note to the venture
cost discussion, and either (a) fold a rack-integration-and-test facility capex
line into `VentureCosts`, or (b) explicitly state it is excluded and flag it as a
deployment-rate constraint alongside the cadence ramp. Cross-reference
`reliability_failure_handling.md` Open Q6.

---

## Finding 6 — Commissioning lag: a node earns from its deployment year (MEDIUM)

**Location:** live-fleet cohort sum, `valuation.py` lines 969–980 — a cohort
contributes `cohort_live_fraction(age=0) = 100%` in its deployment year; revenue
= fleet_live × per_rack immediately.

**The problem.** The model books a rack at 100% revenue-generating capacity in
the same model year it launches. Physically, a freshly deployed node must: reach
orbit, commission (deploy the ~430 m² radiator and ~545 m² solar array — the
write-up's own `node_mass_model.md` calls the deployable radiator "the key
engineering risk"), check out, and ramp. The reliability doc also notes
launch-vibration latent damage can surface "weeks into orbit." A new cohort
realistically contributes a *fraction* of a year of revenue, not a full year.

`VALUATION_MODEL.md` Confidence §"Deliberately optimistic choices" *names this*
("no commissioning-lag haircut — a node earns from its deployment year"). So it
is disclosed — but disclosure is not correction. Given the ramp deploys an
ever-larger cohort each year, the most recent (largest) cohort is exactly the one
being over-credited; on the steep part of the ramp this is a systematic
~半-year-per-cohort overstatement of live, earning fleet.

**Materiality.** Medium. Smaller than Findings 1–3, and partly offsetting against
the conservative choices the write-up also lists. But on a fast-ramping fleet it
is a persistent upward bias on revenue.

**Recommended fix.** Apply a commissioning-lag haircut — e.g. a deployment-year
cohort contributes 0.5 (or a stated fraction) of a live-year, ramping to full the
next year. Cheap to implement; removes a known, disclosed optimism.

---

## Finding 7 — Launch cost held flat: directionally conservative, but note the tension (LOW / FYI)

**Location:** `LAUNCH_COST_INTERNAL_MUSD = 20.0` (`valuation.py` line 379), used
flat across all years and all cadences.

This is **the rare assumption the model makes conservatively**, and it is
correctly flagged in both the code docstring and `VALUATION_MODEL.md` §3.5. Two
observations, both already in the project docs, worth keeping visible:

- **$20M is below the only anchored datapoint.** `rklb_forward_trajectory.md`
  §2.2: Rocket Lab's 50%-margin-at-24-launches/yr target *implies* ~$25M/launch.
  $20M is the founder's working dial; ~$25M is the documented, sourced
  alternative. Holding $20M flat is a (small) optimism on cost.
- **Holding it flat ignores cadence amortization.** `ambition_case.md` §3 argues
  marginal launch cost falls toward ~$8–12M at ~95/yr. The model forgoes that
  benefit — a deliberate conservative choice on cost.

These roughly offset, and the net is mild and disclosed. **No fix required** —
but if Finding 1's ramp is capped, the cadence-amortization argument weakens
anyway (less cadence → less amortization), so $20M flat becomes a cleaner
assumption. Flagged only so the fix pass keeps the launch-cost dial coherent with
whatever cadence ramp it lands on.

---

## Summary table — findings ranked by materiality

| # | Finding | Verdict | Materiality | Fix |
|---|---|---|---|---|
| 1 | Cadence ramp 165→285/yr (yr 12–15) exceeds the all-time world launch record and the 3-pad Falcon 9 theoretical ceiling | **Physically incredible above ~150–200/yr** | **Critical** | Cap ramp at ~100–130/yr plateau from yr 10–11; or label yr 12+ a bigger-rocket scenario |
| 2 | `SERVICE_LIFE_YEARS = 5` tagged CITED, but it is an unproven "minimum requirement"; reliability doc models 3 yr | **Optimistic; mis-tagged** | **High** | Re-tag as ASSUMPTION; run 3-yr and 7-yr sensitivities (3-yr cuts fleet ~40%, raises depreciation ~67%) |
| 3 | Block upgrade modelled as 2 racks/launch — contradicts `node_mass_model.md` / `simulations/REPORT.md` / `CONCLUSION.md` (2-rack node never flies) | **Wrong mechanism** | **High** | Model the upgrade as per-node power/revenue uplift on a 1-rack node, not `racks_after = 2` |
| 4 | node = 1 rack = 1 satellite = 1 launch | **Sound** | — | None (but Finding 3 currently breaks it at yr 5) |
| 5 | Burn-in / integration throughput (~1–3 wk/rack) is an un-modelled deployment-rate constraint | **Missing** | **Medium** | Add throughput note + facility capex, or explicitly exclude and flag |
| 6 | New cohort booked at 100% revenue in its launch year (no commissioning lag) | **Optimistic (disclosed)** | **Medium** | Apply a deployment-year live-fraction haircut (~0.5) |
| 7 | Flat $20M internal launch cost | **Conservative; disclosed** | **Low** | None; keep coherent with the revised ramp |

---

## The bottom line for the fix pass

The valuation model's venture layer is **credible through roughly year 8–10 and
not credible thereafter**, and the reason is concentrated in Findings 1–3, which
all push the same direction (venture too big):

- The model's year-15 venture revenue (~$24B) sits **2–3× above the ~$5–10B/yr
  Neutron ceiling the project's own `CONCLUSION.md` Revision 8 concluded** — and
  it gets there by (1) a cadence that exceeds the world record, (2) a 5-year life
  the reliability work does not support, and (3) a 2-rack-per-launch step the
  engineering explicitly ruled out.
- Fix all three and the venture layer collapses back toward the `ambition_case.md`
  envelope (~$5B/yr, ~420 nodes, ~95 launches/yr) — which is the project's own
  honest top-of-Neutron-ladder number. That is the figure a company-valuation
  model should be carrying.
- The model's *direction* — venture is material to Rocket Lab, fleet scale is the
  first-order lever, premium is second-order — survives. But the **magnitude** of
  "material" is overstated: as written it roughly doubles+ the company; corrected
  to the Neutron-physical envelope it is a meaningful second pillar (~$5–10B
  venture revenue on a ~$15B baseline), not a doubling-and-then-some.

Nothing here is a finance error. Every issue is a *physical* premise where the
model is more optimistic than the engineering research that precedes it — and in
two cases (Findings 2 and 3) the model cites those very documents while assuming
the opposite of what they conclude.
