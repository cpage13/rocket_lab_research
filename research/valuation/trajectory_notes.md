# Trajectory Notes — AI Compute Economics & the Orbital Venture Over Time

*Working notes, 2026-05-17. Captures the founder ↔ assistant discussion on the
"dynamic / trajectory" critique of the valuation calculator. This is a living
scratchpad — NOT a finished research doc. It will brief a trajectory research
agent, and after that a trajectory layer in the calculator.*

---

## The core critique (founder)

The valuation calculator (`valuation/calculator/`) is **static on per-rack
economics**. It models the fleet ramping up, but the per-rack *unit* is frozen
at a 2026-class rack. There is no technology trajectory in it. For a 10–15-year
valuation that is a real gap — and it is why the revenue numbers feel
disconnected from how fast AI hardware is actually moving.

## What the calculator models dynamically vs. holds static

**Dynamic (changes year to year):** launch cadence, fleet size, attrition, the
orbital premium (decays as the fleet grows), R&D spend, the block-upgrade step.

**STATIC — frozen at 2026 values (the gap):**
- per-rack revenue ~$11M/rack-yr (a today's-rack number)
- rack cost $7M, spacecraft $18M, launch $20M
- rack power / FLOPS / performance — *not modeled at all*; no GPU-generation concept
- service life 5 yr

## Trajectory variables to model, 2026 → 2041

- **Rack FLOPS / performance** per GPU generation (founder: ~100× over the window)
- **Rack cost** per generation (founder: rises a lot — $30–50M plausible; $100M as an extreme thought experiment)
- **Rack power** per generation (130 kW → 300 → 600+ kW) — *this*, not rack mass, drives node mass
- **Node mass** over time (radiator + solar scale with power → the flyability ceiling tightens; may force racks/launch 2 → 1 at Rubin-Ultra-class power)
- **Per-rack revenue** — $/rack-yr, and the underlying $/token, $/GPU-hr, $/FLOP, $/kW
- **Energy cost** trajectory (terrestrial — rising; orbital = solar capex, no recurring bill — the relative advantage grows over time)
- **Launch cost** over time

## The key economic principle — and the founder's pushback

**Principle (assistant):** a rack's FLOPS exploding does not make the rack
*owner* richer — it makes compute cheaper for the *buyer*. $/token has fallen
~10×/yr; capability and price fall together. The FLOPS gain is consumer
surplus. A compute seller earns what competition allows — unless it has a moat.

**Founder pushback (valid, recorded):** the H100 $8 → $2/GPU-hr rental collapse
is the **middleman / neocloud rental layer** — the *least* differentiated
layer. NVIDIA did not see margins collapse (~75% GM); it has a genuine scarce
position. The orbital venture **owns its racks** — it is an infrastructure
owner, not the squeezed renter — so it should not be modelled as the collapsing
commodity-rental layer.

**Synthesis:** the founder is right that the layer matters. Owning the asset
avoids the renter's markup (real, favorable — the $11M IaaS anchor may be too
low a base for an owner-operator). BUT owning an asset does not by itself
confer pricing power — an owner still competes with other owners. The layers
that hold value (NVIDIA, integrated hyperscalers) hold it because they have
**moats**. The orbital venture holds value only if the orbital niche is
genuinely scarce / differentiated — i.e. the **premium is real**. Conclusion
unchanged (the premium is the load-bearing variable), but the layer distinction
is a cleaner justification for *why* a premium is economically real, and a flag
to re-examine the revenue anchor (owner-operator vs. rental rate).

## What the premium is applied to — to clarify

The calculator's premium is a multiplier on the per-rack revenue anchor (the
rack-rental / IaaS rate). The research must be explicit about what is in/out:
- **Energy:** orbital = one-time solar capex, no recurring power bill;
  terrestrial pays for power, and AI power cost is large and rising. The
  premium should be framed against the customer's **total cost**, not just a
  rack-rental markup. (Founder: energy maybe not huge today — but on a rising
  trajectory it matters more.)
- Cooling / water, real-estate — same point.

## Locked assumptions / founder positions (this discussion)

- **Service life:** 5-year base case. 7-year is an upside but with *diminishing
  returns* (revenue decays with age); satellites unlikely to last past ~7.
  Returns clearly diminishing by year 5.
- **Neutron payload:** assume a block-upgraded Neutron reaches a **reliable
  ~13 t to SSO** (consistent with the project's block-upgrade estimate of
  ~12–13 t; baseline is ~9.5 t).
- **racks/launch:** 2 on a block-upgraded Neutron — but as rack power climbs
  toward Rubin-Ultra class (~600 kW), the node may exceed even the
  block-upgraded mass budget → drop back to **1 rack/launch**. Model this
  reversal in the trajectory.
- **Horizon:** 10-year is the clean primary number; 15-year also shown.
- **Market:** the venture is **not** selling to the general consumer — it is a
  premium / niche play (sovereign, frontier-lab, dedicated). The
  commodity-price-collapse argument is partially blunted by that.

## The extreme thought experiment (founder)

If a rack becomes very expensive (founder's extreme: ~$100M), the ~$20M launch
becomes trivial (~17% of the node vs. ~45% today) — the launch-cost drag
vanishes and even a 1-rack node is a major asset. **Counter:** a $100M rack
must still earn back $100M+ over its life (~$25M+/rack-yr just to break even on
the rack), and a more powerful $100M-class rack is heavier → flyability
tightens. Costlier racks do not automatically improve economics — revenue must
rise with cost, and mass must stay flyable. Both directions go in the model.

## Deferred calculator code fixes (do not lose these)

- **Pydantic.** Switch the calculator's config (de)serialization from plain
  frozen dataclasses to **Pydantic** — validation + self-documenting schema.
  Founder directive: top-quality code; use Pydantic wherever there is
  (de)serialization. (Fix later.)
- **Per-rack report inconsistency.** The per-rack table prints a +$5M/+37%
  margin that contradicts the negative steady-state FCF (mixes live-basis
  revenue with deployed-basis cost). Report layer only — engine math is fine.
- **EV-multiple non-monotonicity.** The multiple-based EV dips near break-even
  (averaging 6×revenue with 20×near-zero-earnings) — non-monotonic across a
  premium sweep. Fix the methodology.

## Next step

A research agent that: (1) reads these notes + the full existing research
corpus (especially `economics/revenue_per_watt.md`,
`economics/rack_cost_trajectory.md`, `economics/energy_operating_costs.md`, the
M2 trajectory data-science model); (2) does further sourced research; and
(3) produces honest, sourced, directional **trajectories 2026 → 2041** for: rack
cost, rack power, rack FLOPS, $/rack-yr, $/token, $/GPU-hr, $/FLOP, $/kW, energy
cost, node mass, and how value-capture splits across the layers (chipmaker /
infrastructure owner / renter / inference-seller). Output feeds a trajectory
layer in the calculator. Nothing perfect — directional and sourced.

## Wave-14 — build directives (the trajectory layer is now being built)

The trajectory research (`ai_compute_trajectory.md`) is done; the calculator's
trajectory layer is being built. Founder directives for this build:

- **Code quality.** Refactor config to **Pydantic** (v2) — solid defaults,
  validation, field descriptions. Pristine typing, logical well-written
  comments, readable — top-quality Python throughout.
- **Trajectory variables as per-year knobs / rates.** Rack cost, rack power,
  node mass, per-rack revenue, launch cost become time-varying — the user turns
  knobs (a start value + a growth rate, or a per-year path). The exact config
  design is left to the coding agent for a first pass, to be reviewed.
- **Rack cost** rises ~75–100%/yr (≈2×/generation) — founder's framing,
  consistent with the research.
- **racks/launch → 1 by the Rubin generation.** Revised from the earlier
  "default 2." By Rubin, even a block-upgraded Neutron carries **1 rack** — the
  block upgrade is consumed keeping the single, far more powerful rack flyable,
  not adding a second. 1 rack/launch is the honest baseline from ~Rubin on; and
  because the rack is now so valuable, 1/launch is fine.
- **The Rubin-Ultra crossover** ("something interesting"): by Rubin Ultra the
  rack costs ~$15–25M+ while launch is ~$20M — launch cost ≈ rack cost; later,
  launch is a minor line. The launch-cost drag that historically broke the
  model structurally fades. The report should surface this.
- **Launch cost** — a knob, default ~$20M, may trend flat-to-**down** over time
  (competition, scale). Not expected to beat Starship $/kg — accepted.
- **Per-rack revenue** grows ~1.5–2×/generation (tracks the rack's *price*, NOT
  its FLOPS — the research's decisive finding). The revenue **anchor base** is
  lifted: $11M is the competed-down neocloud rental rate; an owner-operator
  sits higher (~$11–16M).
- **Bulk discounts** — do NOT model NVIDIA rack bulk discounts (NVIDIA discounts
  little; note "not accounted for"). Other costs (solar, bus) do get cheaper
  with scale — a modest knob or a noted assumption.

## Wave-15 — flyability wall confirmed; the bootstrap reframe

The v2 trajectory layer surfaced a hard finding: on the rising rack-power curve,
node mass crosses Neutron's ~12.5 t SSO payload at ~year 4 (FY2030) and reaches
~60 t by FY2036. The full-power flagship node stops fitting Neutron ~2030.

Resolved in discussion:
- **The ceiling is a POWER ceiling (~250–320 kW node), not a generation lock.**
  The venture flies the newest silicon every generation (Rubin, Rubin Ultra,
  beyond) — **power-capped** to the flyable node (run below peak wattage / fewer
  dies). It still gets each generation's efficiency (more compute per flyable
  watt); it just cannot fly the full power envelope. ("Frozen at GB300" was
  wrong — corrected.)
- **The bootstrap reframe (the honest case).** Neutron is the bootstrap vehicle
  — get the first racks up, prove the concept, ~2026–2031. A **heavy vehicle**
  (a block-2 Neutron or a new heavy) is needed for the full-power scale era from
  ~2032. The project's standing two-act conclusion, now dated.
- **Conservatism to flag:** the model assumes terrestrial racks bolted up (node
  mass ∝ terrestrial rack power, no space-specific hardware evolution). Once
  orbital DC is a real product line, hardware co-designed for space (power-dense
  radiators, space-optimized racks) would push the flyability wall *later*. The
  ~2030 wall is a deliberately conservative, worst-case read.

v3 calculator fix (proposed — scope pending founder confirm): enforce the
flyability power ceiling; fly power-capped newest silicon past the wall; add a
"heavy-vehicle arrives year N" dial that uncaps the power (so the tool shows
both the bounded-Neutron-bootstrap value and the with-heavy-vehicle scale
value). Flag the no-space-hardware-evolution conservatism in the output.

## Wave-16 — v3 build spec: the flyability dials + the flyable-window output

v3 fix (task 10): enforce the flyability ceiling, and make the load-bearing
physical assumptions explicit, sweepable dials so the founder can run the
what-ifs — "if we got to 15 t, if the rack were more efficient, how much
further does the window go, how many more racks?"

Dials v3 must expose:
- **SSO payload (vehicle capacity)** — default 12.5 t (block-upgraded Neutron);
  sweepable up (15 t = a heavier Neutron variant / bigger upgrade; higher =
  Starship-class). A continuous capacity dial — replaces the earlier binary
  "heavy-vehicle" idea. Optional step-up year (the vehicle gets heavier in
  year N).
- **Node-mass model** — node mass driven by rack power; radiator areal density
  (~3–8 kg/m²) and radiator surface temperature (the hot-loop, ~40→80→100 °C)
  as dials — the genuinely uncertain inputs; let the founder sweep
  optimistic vs conservative.
- **Rack power / efficiency** — the rack-power growth rate as a dial; a
  more-efficient rack (better perf-per-watt, or slower power escalation) gives
  a lighter flyable node and a later wall.
- **Tjmax** — the GPU junction-temperature cap (~85 °C default). Raising it
  (the future-silicon bet) opens the hotter radiator columns and pushes the
  wall out.

Output v3 must surface — the **flyable window**: the year the flagship-rack
node first outgrows the vehicle, the power-cap level past the wall, and how
many racks/nodes are deployable within the window — responding to every dial
above, so "15 t SSO + better efficiency → wall moves to year X, +N racks" is a
one-run answer. Past the wall the venture flies power-capped racks (newest
silicon, capped to the flyable power) unless the SSO-payload dial is raised.

## Wave-19 — v4 rebuild directives + the revenue / self-build research

Two research passes (2026-05-18) and a founder discussion reshaped the model.
The calculator is being rebuilt as **v4**.

**Research that landed (2026-05-18):**
- `economics/revenue_economics_2026.md` — current sourced revenue economics.
  Three layers per NVL72-class rack-year: renter/reseller ~$1–2M net;
  **owner-operator ~$10–12M** (our layer); integrated inference-service
  ~$15–25M+. Verdict on the calculator: the $13M anchor is the *top* of the
  band — re-anchor to **~$11–12M**; the 15%/yr growth is too high — **~10–12%/yr**,
  decelerating. The non-hardware terrestrial cost orbit converts to one-time
  capex (energy + real estate + cooling) is **~$4M per rack over 5 years, rising** —
  the premium should ultimately be framed against the customer's *total* cost,
  not a rack-rental sticker. Flags: a possible premium-on-a-premium double-count;
  a frozen-silicon node drifts toward a much lower blended rate as it ages.
- `node_design/self_built_rack.md` — fractional-rack feasibility. The NVLink
  moat blocks rival *chip* vendors, not a buyer who pays NVIDIA's toll and
  re-houses the result; NVLink Fusion productizes exactly the self-build idea;
  the realistic path is "buy the NVLink fabric subsystem, self-design the
  orbital airframe." A self-built ~36-GPU **half-rack (NVL36, a shipping SKU) is
  realistic Phase-2 (~2031–2033)**; the tight fabric matters far less for
  inference. The fractional-rack model is grounded.

**Founder directives for the v4 rebuild:**
- **One node per launch — always.** Drop the derived racks-per-launch / the
  2-per-launch case.
- **The fractional-rack model — replaces continuous power-capping.** The flown
  unit is a discrete fraction of a full rack — **1.0 / 0.5 / 0.25** (full / half
  / quarter) — the largest fraction whose node mass fits the SSO payload. As
  rack power climbs, the flown unit shrinks. The "rack" stays the benchmark for
  industry comparison; what flies is a fraction of one.
- **Rack-power trajectory decelerates.** Naive constant 30%/yr compounding ran
  to a physically absurd ~1.9 MW single rack by 2036. v4 uses a decelerating
  (S-curve) curve anchored to the confirmed roadmap (~140 kW 2026 → ~600 kW
  Rubin Ultra ~2028–29), tapering hard after — full-rack power approaches a soft
  ceiling, not 1.9 MW. ~600 kW is the founder's sense of the largest *full* rack
  that flies whole on Neutron; past it, fractional racks.
- **Launch cost is cadence-indexed**, not flat. ~$25M near-term / low cadence
  (the sourced figure), falling to ~$12–15M at ~100 launches/yr as fixed costs
  amortize.
- **Service life — 5 years, hard stop.** The satellite is gone after 5 years.
  Revenue declines across the 5 years (silicon ages off the frontier) then goes
  to **zero** at year 5. 3-yr downside / 7-yr upside as scenarios. (5 yr is a
  mandatory design target — engineer to meet it; 3 yr = the design failed; 7 yr
  = a revenue bonus.)
- **Revenue re-grounded** — anchor ~$11–12M (not $13M), growth ~11%/yr
  (not 15%), per `revenue_economics_2026.md`.
- **The premium stays a simple multiplier dial for v4** — default +50% — plus a
  new **`no_premium.yaml`** scenario (premium 0) so the raw, terrestrial-parity
  numbers are visible. The **total-cost-of-ownership re-framing** (premium over
  the customer's all-in terrestrial cost incl. energy) is deferred — a
  deliberate separate step, to be done with the founder once v4 is in hand.

**Framing captured in the discussion:**
- **The venture is a tiny market sliver — and that is the pitch.** By 2035 it is
  on the order of ~0.01–0.03% of the AI-specific data-center market (~50 MW of a
  ~300–500 GW market). It never competes for share — it is buildout-limited, not
  demand-limited. The model is the early-EV one: a small, premium, specialized
  product (sovereign / isolated / dedicated capacity), sold top-of-market, where
  a rounding-error market slice is still a multi-billion-dollar business.
- **A flagged research gap:** the radiator/mass model may be too pessimistic for
  hotter-running future silicon (Rubin Ultra and beyond run hotter → less
  radiator per watt → a higher flyability ceiling). Under-researched; v4 keeps
  the current radiator physics; a dedicated research pass is warranted.
- Early thin or negative margins are acceptable to the founder; the test is
  whether the venture reaches genuine profitability and scale.

---

## The core flaw — rack cost and revenue diverge (found 2026-05-18)

**The finding.** The calculator's two trajectory dials `rack_cost_growth`
(+37%/yr) and `revenue_anchor_growth` (+11%/yr) are INDEPENDENT — nothing
couples them. So they diverge linearly across the 10-year horizon, and by
FY2036 cost has overtaken revenue: a frontier rack — and, broken down, each
individual GPU — costs more to buy than it earns over its entire service life.

**The marginal proof.** At the FY2036 vintage, one GPU's compute (its share of
the rack hardware) is ~$1.91M; its lifetime revenue is ~$1.60M. The GPU does
not earn back its own silicon — before a dollar of solar, radiator, bus or
launch. A marginal GPU added to a node costs ~$2.79M (compute + its own solar +
its own radiator; the bus and the launch are FIXED and add $0 at the margin)
and earns ~$1.60M — a −$1.20M marginal unit. That is why adding GPUs widens the
loss: each one is contribution-negative.

**Why it is wrong.** A rack's PRICE is bounded by its EARNING POWER — a buyer
purchases a rack only if its lifetime revenue clears its cost plus a return. So
`revenue >= cost` is a market FLOOR, not an output. The 37%-vs-11% divergence
is real for a while — it is margin compression (a 2026 GB300 rack earns ~6x its
cost; competition compresses that) — but the model lets the compression run
linearly THROUGH break-even into permanently underwater, instead of asymptoting
to a positive equilibrium margin. Margin compression is real; compression past
zero is not.

**The fix direction.** Couple revenue and cost. Model the MARGIN (the
revenue/cost ratio), anchored to what real operators run (Oracle OCI ~30-40%
gross; ~77% rack-level before depreciation), so cost and revenue move together
and the gap compresses toward a positive floor — NOT two independent diverging
growth dials. NOT a revenue-per-FLOPS re-parameterization (that risks the
opposite error — revenue riding the ~10x/3-gen FLOPS curve, wildly overstated;
the FLOPS gain is the buyer's consumer surplus).

**Status.** The v5 work — the five-line node-cost decomposition, the two
co-design dials, the bottom-up launch-cost research — confirmed the model's
MECHANICS are sound and isolated the problem to this one divergence. The
coupled revenue/cost rework is the next major fix; it is the thing standing
between the calculator and results that cohere.

---

## The fix — the revenue/cost coupling (v6, 2026-05-19)

**What was done.** The independent `revenue_anchor_growth` dial is REMOVED. The
revenue anchor is no longer a free compound — the engine now computes it as
`revenue_anchor(y) = rack_cost(y) × R`, where `R` is the constant base-year
revenue/cost ratio (`owner_operator_anchor_musd / rack_hardware_musd` ≈
$11.5M / $6M ≈ **1.92×/yr**). Revenue rides rack cost's own growth path; the
ratio is held fixed across the horizon. The two can no longer diverge — the
coupling is structural, not a dial setting. The `_check_trajectory_coherence`
validator (which policed `revenue_anchor_growth` against `rack_cost_growth`) is
removed with the dial it guarded.

This is the modelling expression of the founder's directive: "what is the
current margin for the industry? Maybe we keep that … hyperscalers are going to
make the same margins in the future, if not more — it's never going to be
less." `R` is that current industry margin; the coupling holds it constant.

**Before / after.** Nothing changed but the revenue coupling. The central-case
(default) DCF moved **−$20.4B → +$20.8B**; per-node lifetime margin **−132% →
+60%**; steady-state FCF **−$3.1B/yr → +$6.6B/yr**. The old −$20.4B was an
artefact of the impossible divergence (a 2036 rack out-pricing its own lifetime
earnings), never an economic finding. At terrestrial parity — premium 0,
charging exactly the ground rate — the venture clears a positive value.

**The polarity flips the coupling causes.** Coupling revenue to cost INVERTS
the sign of several dials, because the model crossed from loss-making to
profitable:
- `rack_cost_growth` was a headwind (cost outran revenue). It is now an
  *amplitude* dial: revenue rides it, and because compute+revenue is the
  high-margin line, a *faster* trajectory means a *larger* venture. The
  `conservative` / `ambitious` scenarios had it set the old way (conservative
  high, ambitious low) — both were re-polarised (conservative 0.30,
  ambitious 0.45).
- Any "fly more GPUs" dial (a lighter node, a gentler power curve, the
  `solar_radiator_mass_factor`) was a loss-amplifier; with positive unit
  economics it is now a value-amplifier. This is the capacity-amplifier
  insight, already flagged for the mass factor — it now applies model-wide.

**The premium is now a separate dial, defaulting to zero.** v6 also acted on
the founder's premium directive. The orbital premium is the uplift ON TOP of
the cost-coupled terrestrial rate ("premium" in its literal sense — over what a
hyperscaler charges on the ground). It DEFAULTS TO ZERO: the default scenario
values the venture at terrestrial parity, to see "how we compete head-on with
the market." `no_premium.yaml` (redundant now that the default *is* the
no-premium case) was renamed `with_premium.yaml` and carries a +50% premium —
the clean default-vs-premium pair isolates what the premium is worth (~+$19B
DCF).

**The load-bearing assumption.** Everything now rests on the revenue/cost ratio
`R` ≈ 1.92×/yr (~7.5× gross over a 5-year life). It is *derived* from the two
sourced base-year anchors and held flat. Whether it *should* hold flat — versus
compress as AI compute commoditises — is the genuine open question. The central
assumption (per the founder) is that hyperscalers keep their margins. To model
a thinner margin, lower `owner_operator_anchor_musd` (the `conservative`
scenario's $10M is the thin-margin read).

**A caveat surfaced — `ambitious` is now an outlier.** With the model healthy,
the `ambitious` scenario — every favourable dial at its optimistic extreme,
multiplied together (a +75% premium × a richer $13M margin × a fast 0.45/yr
trajectory × a near-record cadence) — computes to ~$1.4T. Each dial is
individually defensible; their product is not a credible point estimate. It is
the upper bound of the cone, not a forecast. `default` (parity) and
`with_premium` are the trustworthy reads. The `ambitious` scenario is a
candidate for re-calibration — it was tuned for the old loss-making model.

**Status — RESOLVED.** The coupling is implemented across config / engine /
report / the five scenarios / the tests (73/73 passing) and documented in
`projection_2026_2036.md`. The core flaw above is fixed: revenue can no longer
fall below cost at the rack level. The calculator's results now cohere.

---

## The next problem — the model is not GPU-grounded (found 2026-05-19)

**Handoff note — this section is the live state of the calculator workstream.**
Read it first if resuming after a compaction.

**What was done after the coupling fix.**
- A JSON output mode was added to the calculator (`rklb-value <cfg> --json`,
  and `--input-schema`). It was then rebuilt into a documented, self-describing
  artifact: an `about` preface, a `manifest`, a `known_issues` block, a
  `data_dictionary` defining every field (meaning, unit, stock/flow, formula
  or source), the input dials, the year-by-year model grouped into
  `fleet`/`rack`/`costs`/`revenue`/`profit`, and the summary. Generated files
  live in `calculator/output/` (the five scenarios + `input_schema.json`). The
  field documentation lives in `calculator/src/rklb_value/glossary.py`. Tests:
  74/74. `config.DialModel` now sets `use_attribute_docstrings=True` so the
  Pydantic schema carries every dial's sourced description.
- Two independent audits were run (sub-agents). They confirmed a real bug and
  produced the field documentation.

**The CONFIRMED BUG (in the JSON's `known_issues`).** The model fixes
`GPUS_PER_FULL_RACK = 72`, but `rack_cost_growth` (+37%/yr, $6M→$140M) is taken
from `ai_compute_trajectory.md`'s cost table — where the rack itself GROWS in
GPU count (GB200 NVL72 = 72 GPUs → Rubin Ultra NVL576 = 576 GPUs). The model
therefore prices a ~576-GPU-class rack as if it had 72 GPUs, overstating
per-GPU cost — and, via the v6 coupling, per-GPU revenue — by an estimated
~8x. The headline default numbers ($10.8B revenue / $5.6B operating profit
FY2036) and `ambitious`'s $1.4T are inflated by roughly that factor.

**The DEEPER GAP — the model is rack-dollar-based, not GPU-grounded.** It has
whole-rack dollar figures and rack power, and divides by a fixed 72. It does
NOT ground three things, and without them no per-GPU number can be
sanity-checked:
1. **Per-GPU cost**, generation by generation (real $/GPU: B200, GB300, Rubin,
   Rubin Ultra…) — and how many GPUs are in "a rack" by generation.
2. **Per-GPU performance / output** — what a GPU actually delivers (inference
   throughput, FLOPS) and how much it grows per generation. The model tracks
   power (kW) but power ≠ output. This is what makes "$425/GPU-hour at the
   2036 horizon" judgeable or not.
3. **A grounded GPU-hour rental rate** — today's real rate (~$2-6/GPU-hr) and
   its trend. The model back-solves revenue from an $11.5M/rack-year anchor; it
   never uses a market rate.

**THE PLAN (next session).** Brainstorm → strategy → a feasibility-forge
research cycle to source the three missing data points above → then rework the
calculator GPU-FIRST: GPU cost × GPU count = rack cost; GPU output × a
GPU-hour rate = revenue. The "rack" and "rack fraction" become derived display
quantities. The v6 revenue/cost coupling stays — it just couples grounded
quantities instead of an ungrounded rack price.

**Fixed assumptions (NOT gaps — decided inputs).** SSO payload 12.5 t (assumes
the Neutron block-upgrade is flown); the rack-cost and rack-power trajectories
are given inputs; service life 5 yr is a base-case design target.

---

## The fix — rack cost re-anchored to a flat $/kW (v7, 2026-05-19)

**The bug, restated.** The audit above (`rack-gpu-count-conflation`) was
confirmed and fixed. The model fixes `GPUS_PER_FULL_RACK = 72`, but `rack_cost`
was grown on an independent compound dial, `rack_cost_growth` (≈0.37/yr),
lifted straight from NVIDIA's roadmap — where the rack itself grows in GPU
count (GB200 NVL72 = 72 GPUs → Rubin Ultra NVL576 = 576 GPUs). So `rack_cost`
ran $6M (2026) → ~$140M (2036), a 23× rise, while the rack's *power* rose only
~7.8× (140 kW → ~1,093 kW). The model priced a ~576-GPU-class rack as if it had
72 GPUs — and, via the v6 coupling, did the same to revenue.

**The per-kW re-anchor.** A 72-GPU rack's cost should scale with its POWER at a
roughly-flat cost-per-kW. The independent `rack_cost_growth` compound is
REMOVED entirely (no replacement dial); rack cost is now DERIVED from the
existing rack-power logistic:

    rack_cost(year y) = rack_hardware_musd * full_rack_power_kw(y) / rack_power_base_kw

At y=0 it equals `rack_hardware_musd` ($6M) exactly. By 2036 a ~1,093 kW rack
costs $6M × 1093/140 ≈ **$46.9M** (vs the old ~$140M). Rack cost is now
controlled via the rack-power dials (`rack_power_initial_growth`,
`rack_power_ceiling_kw`). The v6 revenue/cost coupling is UNCHANGED — because
rack cost now tracks power, the coupled revenue anchor tracks power too. Engine
schema version stays 6; `known_issues` is now empty.

**The new headline numbers (FY2036, post-fix).**

| scenario      | venture revenue | operating profit | operating margin |
|---------------|----------------:|-----------------:|-----------------:|
| conservative  |          $995M  |        −$1,575M  |          −158.3% |
| default       |        $4,745M  |          +$674M  |           +14.2% |
| upside_7yr    |        $5,381M  |        +$2,074M  |           +38.5% |
| with_premium  |        $6,628M  |        +$2,557M  |           +38.6% |
| ambitious     |       $21,456M  |       +$15,160M  |           +70.7% |

Default FY2036 per-node: rack cost (72-GPU) $46.9M, per-node all-in cost
$65.5M, revenue per GPU per year ~$1.25M, per-node lifetime margin +21.8%. The
pre-fix default was ~$10.8B revenue / ~$5.6B operating profit — the re-anchor
removes roughly the estimated ~8× per-GPU inflation, as expected.

**A calibration flag.** `conservative` now shows a deep negative margin
(−158%). This is the fix working, not a new bug: that scenario stacks a 3-year
service life, the low $10M anchor and a heavy node, and the old 23× rack-cost
inflation (fed through the coupling into revenue) had been masking the loss.
Post-fix the scenario shows its true thin-margin economics. Scenario ordering
is otherwise monotone and sane. Tests: 74/74. (Note: `README.md` and
`projection_2026_2036.md` still carry the pre-fix numbers.)
