# Bear Case — Rocket Lab Should Not (Yet) Commit to an Orbital AI-Inference Data Center on Neutron

*Round 1 — Bear's opening statement and cross-examination of the Bull.
Author: Bear. Date: 2026-05-17.*
*Every claim cites a project research doc (path + section) or an independent
source (URL). The Bear's job is not to deny the venture is interesting — it is
to show, honestly, that the case to **commit** is far weaker than the Bull
presents, and that the affirmative verdict rests on a stack of unverified
numbers and unannounced hardware that, if any one fails, collapses it.*

> **Superseded economics (wave-9, 2026-05-17).** This three-round debate ran
> entirely on the **~$55M external Neutron launch price** and a **~$85M node**.
> Wave 9 re-based the launch to Rocket Lab's **internal marginal cost of
> ~$10–20M**, dropping the node to **~$35–65M (~$45M mid)** and moving central
> V2 gross payback from ~5.3 yr to **~2.8 yr** and the break-even premium from
> ~70%+ to **~25–40%** (`CONCLUSION.md` Rev 4). The debate's *numbers* are
> therefore superseded; its **qualitative convergence — "fund a bounded
> build-to-learn programme with an honest chance of a no-go" — stands**. This
> file is preserved unedited as a dated, append-only debate record; for current
> economics see `CONCLUSION.md` Rev 4–7.

---

## Summary thesis

**The Bull is right that there is no physics wall. That is also the least
decision-relevant thing the project found.** "No physics wall" was settled by
wave 1; the four waves since were a steady retreat from it as the binding
question — *can a node pay back before its silicon is obsolete* — got harder,
not easier. The honest state of the evidence is this:

1. **The baseline product does not pay back.** A GB300-class node on a baseline
   Neutron has a ~3.1-year inference-service payback — *at the upper edge of*,
   i.e. *past*, the 2–3-year GPU obsolescence window — and a ~10-year payback if
   sold as raw GPU capacity (`synthesis/wave5_synthesis.md` §3, §4.1). The
   project's own word for V1 is "**not a standalone profit centre**"
   (`wave5_synthesis.md` §4.1). A venture whose buildable-today product loses
   money is not a venture you commit to; it is a research program.

2. **The profitable product does not exist and is not on anyone's roadmap.**
   V2 — the only configuration that pays back inside the window — requires
   *simultaneously*: (a) a Vera Rubin GPU generation not yet shipping; (b) a
   "hot-loop" radiator running a thermal regime nobody has flown; (c) a
   100 Gbps Mynaric Mk3.1 terminal that is "roadmap," not product
   (`laser_comms/optical_comms.md`; LIBRARY `optical_comms.md` row); (d) a
   block-upgraded Neutron that **Rocket Lab has not announced and has no public
   roadmap for** (`rocket_lab/neutron/payload_and_block_upgrade.md` §5); and
   (e) a deployable radiator subsystem Rocket Lab **cannot currently build**
   (`rocket_lab/space_hardware_capabilities.md` §6). Five speculative
   dependencies stacked in series is not a "path to profit" — it is five
   independent ways to fail.

3. **The whole flyability verdict rests on two numbers Rocket Lab has never
   published.** The favorable verdict depends on Neutron's reusable-SSO payload
   (~9.5 t — *an analyst estimate*, "the single most important unverified number
   in the entire feasibility analysis," `payload_and_block_upgrade.md` §2,
   open Q1) and on usable fairing volume (also unpublished, `wave5_synthesis.md`
   §6 Rev-4 §2). And Neutron itself **has not flown** — its Stage-1 tank
   *ruptured* in qualification testing in January 2026, slipping first flight to
   "at least Q4 2026" ([Space.com](https://www.space.com/space-exploration/rocket-labs-new-neutron-rocket-suffers-fuel-tank-rupture-during-test);
   [SpaceNews](https://spacenews.com/rocket-lab-delays-neutron-debut-to-late-2026/)).

4. **Willingness-to-pay is entirely unobserved.** The entire business case rests
   on a buyer paying a ~50% premium for orbital inference. The project says
   plainly: there is "**no observed willingness-to-pay data for orbital
   inference specifically**" (`wave5_synthesis.md` §6.2; `premium_value_case.md`
   open Q4). The most load-bearing number in the revenue case is a guess.

The Bull frames every one of these as "a number to pin down or a subsystem to
build — the ordinary work of a hard engineering venture." That reframing is the
core sleight of the Bull case. **Each item individually is "ordinary." The
venture's economics require all of them to land favorably *at once*, and the
project's own synthesis describes the result as closing only "**marginally**"
and only in its "**most optimistic corner**" (`wave5_synthesis.md` §1, §3;
`wave4_synthesis.md` §2c).** The honest verdict is not "build this" — it is
"this is not yet a decision; it is a set of unresolved unknowns, and the
project's own next-steps list (`wave5_synthesis.md` §8) has ten of them."

---

## 1. The economics do not close — and "marginal" is being read as "yes"

The Bull's headline (§ Summary, point 1) is that "the economics close at the
next GPU generation." Read the project's own synthesis on that:

> "the wave-5 levers move it from 'explicitly will not close' to '**closes,
> marginally**, at the Vera-Rubin generation, on the right Neutron
> configuration.'" (`synthesis/wave5_synthesis.md` §1)

And on V2 specifically:

> "Even the inference-service model only reaches the obsolescence window in its
> **most optimistic corner**" (`wave4_synthesis.md` §2c)

This is not a closed case. It is a case that closes only when *every* favorable
assumption is taken together. Walk the conditions the project itself attaches
(`wave5_synthesis.md` §3, "Important honesty check on payback"):

- **(a) Revenue model.** Payback closes "*only*" if Rocket Lab sells
  frontier-model *tokens*, not GPU-hours. At raw-GPU-rental (IaaS) rates "the
  same nodes pay back ~2–3× slower and do **not** clear the obsolescence window
  at any generation" (`wave5_synthesis.md` §3). Selling tokens means Rocket Lab
  — a launch company — must *own or operate a competitive frontier model*, or
  capture the model-owner's margin. Nothing in the project establishes that
  Rocket Lab can do this. It is assumed.
- **(b) Spacecraft-hardware cost.** Payback closes only if the
  spacecraft-hardware line lands "at/below the ~$18M mid." That line is quoted
  as **$8–35M** — a greater-than-4× spread — and is "**the weakest cost input
  in the whole project**… no direct quote exists" (`wave5_synthesis.md` §3, §7;
  `wave4_synthesis.md` §2a). At the $35M high end, V2 payback moves well outside
  the window (`wave4_synthesis.md` §2c table: high-cost column).
- **(c) The rack-cost tailwind holding.** Real, but conditional.

Stack the conditions and the V2 payback table (`wave4_synthesis.md` §2c,
inference-service case) shows the truth plainly. The *central* inference-service
case is **~5.3 years** — roughly 2× too slow. Only the **low-cost + high-revenue
corner** (~2.6 yr) clears the window. The Bull's "~2 yr payback" for V2 is the
*best corner of the optimistic revenue model* presented as the expected case.

**And note what the payback test is measuring.** Payback period is gross
top-line revenue ÷ node cost. It "**exclude[s] the node's own operating cost**
(ground-station network, ops staff, station-keeping)… a true business case would
haircut it for opex" (`wave4_synthesis.md` §2b). The ground segment alone is a
**$100–500M** capital line (`wave5_synthesis.md` §5;
`laser_comms/optical_ground_stations.md` §6). So even the "~2 yr" V2 figure is
*gross revenue to recover node capital* — not profit, and not inclusive of the
constellation's shared infrastructure. A node that "pays back" in 2 years gross
is not necessarily a node that *earns a return*.

**The cruel-timing problem the Bull does not resolve.** The trajectory model
found the venture's window is "**a brief opening that is already nearly shut**"
for the baseline vehicle — GB200/GB300 racks in 2025–2026 (`data_science/REPORT.md`
§4). The Bull turns this into an argument *for* moving now ("the opportunity has
a clock on it," bull §6). But the data-science report's actual finding is
darker: "**the generations worth flying economically are the ones you can't
fly**" (`data_science/REPORT.md` §4). The flyable generations (GB200, GB300)
have the *worst* economics; the economic generations (Rubin, Rubin Ultra) need
hardware that does not exist. Wave 5 narrowed that gap with the hot-loop and SSO
re-baseline — but only enough to make a *power-capped* Rubin "marginally"
flyable. The structural tension — economics improve as flyability degrades, both
coupled to the same variable — is *softened*, not *resolved*. The Bull's section
2 title "the architecture flies, and keeps flying" overstates a verdict the
project itself calls marginal.

## 2. The favorable case is a stack of five unannounced or unproven dependencies

The Bull's "configuration ladder" (§2) is presented as four sturdy, independently
sourced rungs. Examined honestly, the rungs that *reach the profitable
generation* are not built — they are hoped for. The profitable product (V2)
requires **all** of the following to be true at once:

**(i) A block-upgraded Neutron.** The Bull calls this "credible by direct
precedent" (§2 Rung 3). The project's own source is blunter: "**As of May 2026
Rocket Lab has not announced** a specific uprated or 'block 2' Neutron variant,
and there is **no published Neutron growth roadmap**. Everything in this section
is **projection by analogy** and must be labelled speculative"
(`payload_and_block_upgrade.md` §5). The Electron precedent (+33%) is real, but
Electron's upgrade "came ~3 years after debut" (`payload_and_block_upgrade.md`
§5). A block-upgraded Neutron is therefore realistically a **~2030+** vehicle —
and Neutron has not flown the *baseline* version yet. V2's central dependency is
a rocket variant that does not exist, on a base rocket that has not flown.

**(ii) The hot-loop radiator.** The single largest mass lever in wave 5 (−40–55%
radiator mass) depends on running the radiator surface at ~70–80 °C while
keeping the silicon junction safe via loop ΔT. The project flags this as
**unmodeled**: "the hot-loop analysis assumes the junction can be defended with
ΔT budget — plausible but **unmodeled in detail**" (`wave5_synthesis.md` §7,
"Radiator area" item; `node_design/hot_chip_thermal_trajectory.md` open Q1–Q3).
The ~300 kW flyability ceiling — "the single most important number-change of the
whole project" (bull §2) — rests on a thermal model that has not been built.

**(iii) A deployable radiator Rocket Lab cannot build.** This is the gating
subsystem and the Bull concedes it is "honestly the venture's hardest subsystem"
(§5). But the Bull then minimizes it: "one subsystem against a stack of a
dozen." That framing is misleading. The radiator is not one subsystem among
equals — it is *the* mass driver, *the* biggest deployment risk, *the* biggest
un-quoted cost line, **and** the one Rocket Lab has "**no public evidence**" of
building (`space_hardware_capabilities.md` §6;
`node_design/node_mass_model.md` §7; `wave4_synthesis.md` §5). Unfolding a
~300 m²-class radiator — "**larger than the ISS's main radiators**" — from one
fairing is "a serious, unmodelled mechanical-reliability challenge"
(`wave4_synthesis.md` §5, deployment-mechanics item). "Composites and robotics
are adjacent but **not equivalent**" (`space_hardware_capabilities.md` §6). A
venture whose hardest, heaviest, costliest, highest-deployment-risk subsystem is
one the prime cannot currently build is not a venture with "one bridgeable gap"
— it is a venture gated on a first-of-kind development.

**(iv) A 100 Gbps Mynaric terminal that is roadmap, not product.** The Bull
lists Mynaric CONDOR as an owned capability (§5) and elsewhere notes the
"100 Gbps roadmap part" in passing. The reality:
**shipping CONDOR Mk3 is ~10 Gbps** (`space_hardware_capabilities.md` §5; the
LIBRARY summary says 2.5 Gbps for current shipping hardware —
`LIBRARY.md` `optical_comms.md` row), and the Mk3.1 100 Gbps part is "**in
development**." The project lists "Mynaric 100 Gbps timeline" as an open **RISK**
(`wave5_synthesis.md` §7; `wave4_synthesis.md` §5). The always-reachable
laser-mesh architecture (`wave5_synthesis.md` §5) is sized assuming the
roadmap part ships.

**(v) The Vera Rubin GPU generation.** V2 is a Rubin-class node. Rubin is
NVIDIA's *next* generation; its rack mass is "**unpublished, estimated heavier
than GB300**" (`wave5_synthesis.md` §4.2), and its power is "the softest input"
in the model, quoted across a wide 250–600 kW band (`data_science/REPORT.md`
§5). The favorable-generation verdict is calibrated to a chip whose key specs
are estimates.

**The compounding problem.** The Bull addresses these one at a time and shows
each is individually plausible. But V2 profitability requires the *conjunction*
of all five. If a block-upgraded Neutron slips to 2031, or the hot-loop junction
model fails, or the radiator development overruns, or Mk3.1 underdelivers, or
Rubin lands at 400 kW instead of 300 kW — any single miss pushes V2 back outside
the window. The Bull never multiplies the probabilities. The project's honest
framing does: V2 is "a **multi-year-out proposition**, gated on Rocket Lab
actually pursuing the uprate" (`wave5_synthesis.md` §4.2).

## 3. The verdict rests on numbers Rocket Lab has never published — and a rocket that has not flown

The single most important physical input to the entire feasibility analysis is
Neutron's reusable payload to sun-synchronous orbit. The project's verdict on
that number could not be clearer:

> "This **remains the single most important unverified number in the entire
> feasibility analysis.** It must be confirmed directly with Rocket Lab… before
> any economic conclusion is treated as firm. Confidence: **Low–Medium**."
> (`payload_and_block_upgrade.md` §2)

The working ~9.5 t figure is an analyst inference — a ~70% retention factor
applied to the official 13 t LEO number, with a *defensible band of
8.5–10.5 t*. The Bull calls ~9.5 t "a *conservative* analyst estimate" (§7).
That is not what the source says. The source says ~9.5 t sits in the *middle*
of the band and the prior 8.5 t was "on the conservative (low) side"
(`payload_and_block_upgrade.md` §2). The real number could be 8.5 t. At 8.5 t,
the baseline-Neutron ceiling re-derives to **~165 kW** — "the pessimistic
corner" (`wave5_synthesis.md` §2.2) — and the comfortable "~2.7 t margin" the
Bull leans on for V1 (§2 Rung 0) shrinks substantially. **A ±1 t swing in an
unpublished number swings the flyability ceiling ±~40 kW** (`wave5_synthesis.md`
§7) — and the entire crossover-resolution argument lives inside that ±40 kW.

The second unpublished number is **usable fairing volume**. The project asserts
the node is "volume-comfortable, never volume-bound" — but the fairing's usable
internal volume is itself unpublished (`wave5_synthesis.md` §7;
`vision/initial_thesis.md` Rev 4 §2; the lint report notes the project has not
even standardized whether the fairing is 5.0 m or 5.5 m —
`synthesis/lint_report_2.md` §1.5). "Volume-comfortable" is asserted against an
unconfirmed envelope.

And underneath both: **Neutron has not flown.** Worse, in **January 2026 its
Stage-1 propellant tank ruptured during a hydrostatic qualification test** —
a test Rocket Lab's own CEO said "we had anticipated… would pass"
([Space.com](https://www.space.com/space-exploration/rocket-labs-new-neutron-rocket-suffers-fuel-tank-rupture-during-test);
[Rocket Lab](https://rocketlabcorp.com/updates/rocket-lab-neutron-test-update/)).
First flight slipped to "at least Q4 2026," and early flights are expendable;
the project's own assumption is "operational reusable flights **NET 2027**"
(`payload_and_block_upgrade.md` open Q6; `wave4_synthesis.md` §5). The *reusable
downrange-landing mode* — the entire economic baseline of this venture — has
never been demonstrated by Neutron and will not be for years. The Bull's case is
built on a vehicle whose payload to the target orbit is an estimate, whose
fairing volume is an estimate, and which has not yet survived a tank-pressure
test.

## 4. Un-serviceable hardware that fails at ~7–9%/year, with the leading kill-mode un-redundant by default

An orbital node cannot be repaired. The reliability research is candid about
what that means:

- **GPUs fail at ~7–9% annualized**, dominated by *constant-rate random*
  failure that burn-in cannot remove (`reliability_failure_handling.md` §1, §2).
  Over a 3-year life the node glides to "**~75–85% of beginning-of-life
  compute**" — and the business "**must be underwritten against end-of-life
  capacity**" (`wave5_synthesis.md` §4.1; `reliability_failure_handling.md`
  §5, §7). The revenue model must therefore be haircut for an asset that is
  worth ~80% of its rated compute *on average* over life — a haircut the payback
  tables do not visibly apply.
- **The leading whole-node-kill mode is the coolant loop.** "A pump or CDU
  failure thermally shuts the rack within seconds; terrestrial pump MTBF
  (~30,000 h) is **inadequate** for a 3-yr un-serviceable node without N+1
  redundancy" (`wave5_synthesis.md` §7; `reliability_failure_handling.md` §4).
  ~30,000 h is ~3.4 years — barely above mission life, with no margin. And
  "**hot-loop operation slightly worsens the Arrhenius wear-out component**"
  (`wave5_synthesis.md` §7) — i.e. the radiator-mass lever the Bull relies on
  *trades against* coolant-loop reliability. The Bull's §2 never mentions this
  coupling.
- **All hard GPU failure data is H100-era.** GB200/GB300/Rubin "run hotter and
  have **no published field-reliability data yet**" (`synthesis/lint_report_2.md`
  §5.5; `reliability_failure_handling.md` open Q2). The ~7–9% planning figure
  "likely **understates** a space node" (`reliability_failure_handling.md` §1).

None of this is a wall. But it is a stack of real cost and risk — redundant
cooling mass, derating that sacrifices FLOPS, an ~80%-of-rated revenue haircut —
that the Bull's economic summary does not carry, and that makes the already-thin
payback thinner.

## 5. Willingness-to-pay for orbital inference is unobserved — the revenue case is a hypothesis

The Bull's section 4 is its most confident: the premium is "plausible and
modest," "the thesis never needs more than" ~50%. But strip the framing and the
load-bearing fact is this, in the project's own words:

> "there is **no observed willingness-to-pay data for *orbital* inference
> specifically** — the ~50% figure is a reasoned estimate, and
> customer-discovery is the highest-value open research item."
> (`wave5_synthesis.md` §6.2; `premium_value_case.md` open Q4)

The Bull argues the *components* of demand are observed — the terrestrial supply
crunch, the $19B→$177B sovereign-AI market. That is true and fair. But "buyers
are capacity-constrained on the ground" does not establish "buyers will pay 50%
more *per token* for *orbital* compute *with the specific drawbacks orbit
imposes*." Those drawbacks are real and the premium must clear them:

- **Latency.** Orbital links "**rule out real-time interactive serving**"; the
  addressable market is "latency-tolerant batch/async inference" only
  (`wave5_synthesis.md` §7; `premium_value_case.md` §8). The TAM is a *subset*
  of inference that the project has **not yet sized** (`wave5_synthesis.md` §8
  item 8). The Bull cites the full ~90 GW 2030 inference figure; the addressable
  slice is smaller and unquantified.
- **Bandwidth.** "Orbital aggregate bandwidth is orders of magnitude lower" than
  a terrestrial facility (`premium_value_case.md` §8).
- **Disposability.** The node is un-upgradeable and stranded at obsolescence —
  the project calls this "the strongest argument *against* the venture"
  (`premium_value_case.md` §8, §verdict).

The premium-value doc's own verdict is more guarded than the Bull's: the premium
is "**justifiable in principle**" for a narrow buyer profile, but "**whether the
premium those buyers will pay is large enough to clear the obsolescence hurdle
is the open question this document cannot answer**" and "**the business case
remains unproven**" (`premium_value_case.md` §verdict). The Bull cites this same
doc as support for "the premium is justifiable" while omitting the sentence
immediately after it.

## 6. The competitive and strategic case is thinner than presented

The Bull's section 5 argues vertical integration is a moat that frees Rocket Lab
from the Starship dependency gating Starcloud. Two honest qualifications:

- **The "whole intact racks" differentiator is real but narrow.** The project's
  own rack-internals work found that launching a near-COTS rack vs. a
  dispenser-redesigned one saves "~50–90 kg — real but **second-order**"
  (`LIBRARY.md` `rack_internals.md` row). The differentiation is more about
  schedule and integration than a decisive cost moat.
- **Starcloud is ahead on the things that matter for a market nobody has
  proven.** Starcloud has *flown hardware* (Starcloud-1, an H100, Nov 2025),
  raised **$170M at a $1.1B valuation**, and has a funded manufacturing facility
  (`competitors/starcloud.md` §4). Rocket Lab has flown *nothing* for this use
  case and Neutron's first flight is still pending. The Bull's "strategic
  position… before Starcloud's Starship-gated product arrives" assumes Rocket
  Lab can field an operational orbital-compute node before ~2028–2029. With
  Neutron reusable ops NET 2027, a radiator subsystem undeveloped, and a
  block-upgrade unannounced, that timing is optimistic. And Starcloud is not the
  only competitor: Google (Project Suncatcher, prototype launch early 2027) and
  Cowboy Space (Q1 2027 target) are also moving (`competitors/starcloud.md` §5).
- **TechCrunch's read on the sector** — cited in the project's own competitor
  doc — is headlined "**Why the economics of orbital AI are so brutal**"
  (`competitors/starcloud.md` Sources). The independent press consensus on this
  market is not bullish.

The strategic-fit case is genuinely Rocket Lab's strongest leg — it really does
own most of the stack. But "best-positioned company to attempt a hard,
unproven, money-losing-at-V1 venture" is not the same as "should commit capital
to it now."

## 7. What the Bear concedes

A strong bear case concedes what is solid, so the surviving criticisms carry
weight:

- **No physics wall is genuine and well-tested.** Heat rejection, power,
  radiation, comms, and inference topology really do resolve to engineering and
  economics at the target scale (`wave5_synthesis.md` §7;
  `synthesis/lint_report_2.md` §7). The Bear does not dispute this.
- **The terrestrial supply crunch is real, quantified, and worsening** — grid
  queues, transformer lead times, moratoria, water (`premium_value_case.md`
  §1, §6). The *demand pressure* is not manufactured.
- **Zero water is a clean, unqualified differentiator** (`premium_value_case.md`
  §3, §verdict).
- **Rocket Lab's in-house stack is genuinely deep** — solar, bus, mechanisms,
  RF, laser comms (`space_hardware_capabilities.md` §1–5). The radiator gap is
  the exception, not the rule.
- **The rack-cost tailwind is real** — a fixed launch cost amortizes better as
  rack prices rise (`economics/rack_cost_trajectory.md` §6).
- **The "1 rack/node, 1 node/launch, scale by replicas" architecture is sound**
  and the 2-rack node is correctly rejected (`node_mass_model.md` §6;
  `wave5_synthesis.md` §2.4).

The Bear's case is not "this is impossible." It is "this is not yet a decision
to commit — the profitable configuration is unbuilt, the verdict rests on
unpublished numbers, and the project's own synthesis calls the result marginal."

---

## Cross-examination of the Bull

Specific claims in `bull_case.md` that are unsourced, overstated, or contradicted
by the project's own evidence.

**CX-1 — "the economics close at the next GPU generation" (Bull, Summary point 1
and §6).** Overstated. The project's word is "**closes, marginally**"
(`wave5_synthesis.md` §1) and, for the revenue model it depends on, "only
reaches the obsolescence window in its **most optimistic corner**"
(`wave4_synthesis.md` §2c). "Close" and "close marginally in the best corner"
are different verdicts. The Bull presents the optimistic corner as the expected
case.

**CX-2 — "~2.7 t of margin, comfortable, not mass-tight" for the V1 node (Bull
§2 Rung 0).** True *only* at the ~9.5 t SSO estimate. At the equally-defensible
low end of the band (8.5 t — `payload_and_block_upgrade.md` §2), the margin
roughly halves and the data-science model's node mass (~8.4 t for a GB300 node,
heavier solar/radiator curve — `data_science/REPORT.md` §1;
`synthesis/lint_report_2.md` §1.4) leaves almost nothing. The Bull quotes the
single most reassuring corner of a wide envelope as the result.

**CX-3 — "the working ~9.5 t SSO figure is a *conservative* analyst estimate"
(Bull §7).** Contradicted by the source. `payload_and_block_upgrade.md` §2 says
~9.5 t sits at the ~70% *mid-point* of a 65–80% retention band, and that the
*prior* 8.5 t figure "was on the conservative (low) side." ~9.5 t is the
*central* estimate, not a conservative one. The true value "could plausibly be
anywhere from ~8,500 to ~10,500 kg."

**CX-4 — "a credible block-upgraded Neutron" treated as a near-baseline lever
(Bull §2 Rung 3, §6).** The source explicitly forbids this framing: "**Do not
baseline the core thesis on a block-upgraded Neutron**" and "Everything in this
section is **projection by analogy**… speculative" (`payload_and_block_upgrade.md`
§5, §6). The Bull does treat it as a load-bearing rung of the "architecture
flies" ladder and as the vehicle for V2 profitability. V2 — the *only*
profitable configuration — is gated on a vehicle the project says must not be
baselined.

**CX-5 — "Mynaric CONDOR, with a 100 Gbps roadmap part" listed among owned
capabilities (Bull §5).** Misleading by omission. Shipping CONDOR is ~10 Gbps
(`space_hardware_capabilities.md` §5); the LIBRARY catalog says shipping hardware
is **2.5 Gbps** and "100 Gbps is **roadmap**" (`LIBRARY.md` `optical_comms.md`
row). The 100 Gbps Mk3.1 is an open **RISK** in both synthesis docs
(`wave5_synthesis.md` §7; `wave4_synthesis.md` §5). The mesh architecture is
sized on a part that does not ship.

**CX-6 — "one bridgeable gap" / "one subsystem against a stack of a dozen" for
the radiator (Bull §5, §7).** Understated. The radiator is simultaneously the
biggest mass line, the biggest deployment risk, the biggest un-quoted cost, and
the one subsystem with "**no public evidence**" Rocket Lab can build it
(`space_hardware_capabilities.md` §6; `node_mass_model.md` §7;
`wave4_synthesis.md` §5). Deploying a structure "**larger than the ISS's main
radiators**" from one fairing is an unmodeled mechanical-reliability problem
(`wave4_synthesis.md` §5). Counting it as "one of twelve" understates that it is
*the* critical path.

**CX-7 — "even a tiny orbital slice of the ~90 GW 2030 inference market is a
multi-billion-dollar annual business" (Bull §3, §Conclusion point 3).** The
~90 GW figure is total inference. The orbit-*addressable* market is only the
"latency-tolerant batch/async" subset (`premium_value_case.md` §8) — and the
project explicitly lists "**quantify the orbit-addressable inference TAM**" as
an *unfinished* research item (`wave5_synthesis.md` §8 item 8). The Bull sizes
the opportunity against a TAM the project has not yet bounded.

**CX-8 — "OpenAI runs ~70% compute gross margin on inference" used to justify
the inference-service revenue uplift (Bull §3 implicitly; the 1.5–2.5× markup,
`revenue_per_watt.md` §4).** The uplift is real *for a model owner*. But the Bull
never establishes that **Rocket Lab — a launch and satellite company — owns or
operates a competitive frontier model.** The favorable verdict is "**conditional
on owning a competitive model**" (`wave4_synthesis.md` §2b;
`wave5_synthesis.md` §6.1). Selling tokens at a markup requires being in the
model business. This is an unstated, large assumption.

**CX-9 — "the venture is structurally a multi-generation play whose economics
improve with every launch" (Bull, Summary).** Half-true. Per-generation
economics do improve via the rack-cost tailwind (`rack_cost_trajectory.md` §6).
But the *same* source the Bull cites notes "rising rack power may make the
pricier rack **unflyable**" (`LIBRARY.md` `rack_cost_trajectory.md` row) — Rubin
Ultra (~600 kW) is un-flyable on *any* Neutron configuration including
block-upgrade + expendable (`wave5_synthesis.md` §3). The economics improve
right up to the generation you can no longer launch. "Improves with every
launch" is true only for the ~one generation the venture can actually fly.

**CX-10 — "Five years of project research… hunted for a reason to say no. They
did not find one." (Bull, Summary).** Two problems. First, the research spanned
*weeks*, not five years — every project doc is dated 2026-05-17 or within days;
"five years" appears nowhere in the corpus and is an unsourced rhetorical
inflation. Second, the research *did* surface reasons for serious doubt — the
node-payback failure (`wave4_synthesis.md` §2), the un-quoted spacecraft cost,
the unpublished SSO number, the radiator capability gap, the unobserved WTP —
the project simply (correctly) classified them as economic/execution risks
rather than physics walls. "No physics wall" is not "no reason to say no." The
Bull conflates the two.

**CX-11 — "no competitor is positioned to deliver sooner" (Bull, Summary;
§Conclusion point 5).** Asserted, not shown. Starcloud has *already flown*
compute hardware and is funded to a manufacturing facility
(`competitors/starcloud.md` §1, §4); Google's Suncatcher prototype targets early
2027 (`competitors/starcloud.md` §5). Rocket Lab's node depends on a rocket that
has not flown and a radiator subsystem that does not exist. "Sooner" is not
established by the evidence.

**CX-12 — the payback figures are presented as profit (Bull §6).** The Bull says
V2 reaches "~2-year inference-service payback… this is where the venture becomes
a real business." But the project defines this payback as **gross top-line
revenue ÷ node cost, excluding opex and excluding the $100–500M ground segment**
(`wave4_synthesis.md` §2b; `wave5_synthesis.md` §5). A 2-year *gross* payback is
not a 2-year *profit* payback. The Bull's "real business" conclusion skips the
opex and shared-infrastructure haircut the project's own methodology demands.

---

## Sources

*Project research documents:*
- `synthesis/wave5_synthesis.md` — §1 ("closes, marginally"), §2.2 (ceiling
  re-derivation, pessimistic corner), §2.4 (ceilings), §3 (crossover conditions,
  honesty check on payback), §4.1 (V1 not a profit centre), §4.2 (V2 multi-year,
  Rubin rack mass unpublished), §5 (ground segment $100–500M, Mk3.1), §6 (premium
  tiers, no observed WTP), §7 (risks: SSO unknown, block-upgrade, radiator gap,
  coolant loop, Mynaric timeline, latency, WTP), §8 (ten open research items)
- `synthesis/wave4_synthesis.md` — §2a (spacecraft cost $8–35M, weakest input),
  §2b (payback excludes opex; inference uplift conditional on a competitive
  model), §2c (payback tables; "most optimistic corner"), §5 (radiator gap,
  deployment mechanics, Neutron schedule risk, Mynaric)
- `synthesis/lint_report_2.md` — §1.4 (node-mass spread), §1.5 (fairing diameter
  not standardized), §5.5 (no Blackwell/Rubin field-reliability data), §7
  (what is genuinely solid — no physics wall)
- `rocket_lab/neutron/payload_and_block_upgrade.md` — §2 (~9.5 t SSO is an
  estimate, band 8.5–10.5 t, "single most important unverified number"), §5
  ("not announced," "no published roadmap," "speculative," upgrade ~3 yr post
  debut), §6 ("do not baseline… block-upgraded Neutron"), open Q1, Q6 (reusable
  ops NET 2027)
- `rocket_lab/space_hardware_capabilities.md` — §5 (CONDOR Mk3 ~10 Gbps, Mk3.1
  in development), §6 (deployable-radiator gap, "no public evidence," "adjacent
  but not equivalent")
- `node_design/reliability_failure_handling.md` — §1 (~7–9% AFR, understates a
  space node), §2 (constant-rate failure), §4 (coolant loop leading kill-mode,
  pump MTBF ~30,000 h), §5, §7 (glide to ~75–85% compute), open Q2 (H100-era
  data only)
- `node_design/node_mass_model.md` — §6 (1 rack/node verdict), §7 (radiator =
  biggest mass line and deployment risk)
- `economics/premium_value_case.md` — §1, §6 (terrestrial supply crunch), §3
  (zero water), §8 (obsolescence "strongest argument against," latency/bandwidth
  limits), §verdict ("business case remains unproven"), open Q4 (no observed WTP)
- `economics/rack_cost_trajectory.md` — §6 (rack-cost tailwind)
- `economics/revenue_per_watt.md` — §4 (inference uplift conditional on owning a
  competitive model)
- `data_science/REPORT.md` — §4 ("generations worth flying are the ones you
  can't fly"; "brief opening already nearly shut"), §5 (Rubin power the softest
  input)
- `competitors/starcloud.md` — §1, §4 (Starcloud flew hardware, $170M / $1.1B,
  funded factory), §5 (Google Suncatcher, Cowboy Space timing), Sources
  (TechCrunch "Why the economics of orbital AI are so brutal")
- `vision/initial_thesis.md` — Rev 4 §2 (fairing volume unpublished)
- `LIBRARY.md` — `optical_comms.md` row (Mynaric ships 2.5 Gbps, 100 Gbps is
  roadmap), `rack_internals.md` row (optical interconnect saves only ~50–90 kg,
  second-order), `rack_cost_trajectory.md` row (rising rack power may make racks
  unflyable)

*Independent sources:*
- [Space.com — Rocket Lab's new Neutron rocket suffers fuel tank rupture during test](https://www.space.com/space-exploration/rocket-labs-new-neutron-rocket-suffers-fuel-tank-rupture-during-test)
- [SpaceNews — Rocket Lab delays Neutron debut to late 2026](https://spacenews.com/rocket-lab-delays-neutron-debut-to-late-2026/)
- [Rocket Lab — Neutron Test Update (Jan 2026 tank qualification issue)](https://rocketlabcorp.com/updates/rocket-lab-neutron-test-update/)
- [The Register — Rocket Lab ruptures a Neutron tank during testing](https://www.theregister.com/2026/01/22/rocket_lab_neutron_rupture/)

---

## Round 2 — Bear rebuttal

*Round 2. Author: Bear. Date: 2026-05-17. The Bull's Round 2 rebuttal — its
seven concessions and its narrowed "fund the work to the next gate" verdict —
has been read in full and cross-checked against the project corpus. This
section appends; it does not edit Round 1. Where the Bull caught a genuine
error, the Bear concedes it plainly. Where the Bull's concessions actually
strengthen the Bear's case, the Bear says so. The goal is the criticism that
survives both rounds.*

### R2.0 — Framing: the debate has converged more than it looks

Read the two Round 2 sections side by side and the gap between Bull and Bear
has closed to something narrow and honest. The Bull conceded that "no physics
wall" was over-weighted, that "the economics close" should have been "closes
marginally in the optimistic corner," that V1 is a money-loser as a compute
asset, that gross payback was presented as profit, that the ground segment was
unpriced, and that the radiator gap is *the* critical-path subsystem, not one
of twelve (`bull_case.md` R2.1 C-1 through C-8). The Bear accepts every one of
those as correctly conceded — they are the Bear's Round 1 case, now uncontested.

What remains in dispute is small and specific: (1) a few Round 1 Bear
overstatements the Bull correctly caught, conceded below; and (2) whether the
Bull's narrowed verdict — "fund the work to the next go/no-go gate" — is itself
honest about what that gate costs and what it will most likely find. The Bear's
Round 2 position is that the narrowed verdict is **defensible but still
half-a-step too optimistic**, for reasons the Bull's own concessions establish.

### R2.1 — Concessions: what the Bull got right

A bear case that will not concede is not doing its job. These are conceded
plainly.

**BC-1 — The "cruel timing" quote was superseded; the Bear cited a dead
finding as live (Bull R-3).** Round 1 §1 quoted `data_science/REPORT.md` §4 —
"the generations worth flying are the ones you can't fly" — and called the
structural tension merely "softened, not resolved." The Bull is right that this
was wrong. The LIBRARY explicitly marks that report's crossover figure
**superseded**: "its ~163 kW crossover is superseded by the wave-5 reconciled
ceiling" (`LIBRARY.md`, `data_science/REPORT.md` row). Wave 5's three levers
move the buildable ceiling to ~300 kW, which *is* Vera Rubin's rack power
(`wave5_synthesis.md` §2.4). The honest post-wave-5 statement is the project's
own: the crossover is "resolved at Vera Rubin… just barely, and exactly one
generation later than it would in a frictionless world" (`wave5_synthesis.md`
§3). Quoting the pre-wave-5 verdict as the live one was the Bear's error.
Conceded fully. **But note the surviving phrase — "just barely."** The
crossover is resolved; it is resolved *marginally*. That distinction is the
whole of Section R2.2 below.

**BC-2 — Vera Rubin is genuinely shipping, not speculative (Bull R-1, item
v).** Round 1 §2 listed "a Vera Rubin GPU generation not yet shipping" as one
of five speculative dependencies. That was wrong. The project's rack-cost
research states the Vera Rubin NVL144 is shipping in H2 2026 with a reported
$7.0–8.8M rack price (`economics/rack_cost_trajectory.md` §summary, price
table; `wave5_synthesis.md` §3 generation table, Rubin row). V2 is timed to a
near-term, announced, priced NVIDIA product. The Bear's "the profitable product
does not exist" overreached by sweeping Rubin itself into the doubt. Rubin's
rack *mass* remains an estimate "heavier than GB300" (`wave5_synthesis.md`
§4.2), and its power is still quoted across a wide band — those caveats stand —
but the *generation* is real and imminent. Conceded.

**BC-3 — "Five dependencies in series" overreached (Bull R-1).** Round 1 §2
framed V2 as requiring "five speculative dependencies stacked in series… five
independent ways to fail," and faulted the Bull for never multiplying the
probabilities. The Bull is right that this overstated the coupling. Rubin is
shipping and is independent of Rocket Lab entirely (BC-2); the hot-loop rides a
terrestrial warm-water-cooling trajectory NVIDIA is already on for its own
reasons (`node_design/hot_chip_thermal_trajectory.md`); and inference is
bandwidth-light, so the 100 Gbps Mynaric terminal is not on V2's payback
critical path — a first 4–8-node service can run on today's ~2.5 Gbps terminals
(`wave5_synthesis.md` §5; `llm_compute/inference_scaling.md` §3). "Five
independent coin-flips" was the wrong model. The honest count is **two genuine,
coupled, Rocket-Lab-controlled engineering unknowns** — the block-upgrade
decision and the deployable-radiator development — plus a set of *commercial*
unknowns (spacecraft cost, willingness-to-pay). Conceded — and the Bear adopts
the Bull's more accurate count. As R2.2 argues, that more accurate count does
not rescue the verdict; it sharpens where the real risk sits.

That is three substantive concessions. They were real Bear errors and the case
is more credible for naming them. The rest of this section is what survives —
and, in two places, what the Bull's own concessions made *stronger*.

### R2.2 — What still stands — and what the Bull's concessions strengthened

**S-1 — V2 does not actually pay back inside the obsolescence window at the
central case. The Bull conceded the number that proves it.** This is the single
most important point of Round 2, and it is now established by the Bull's own
concession, not the Bear's assertion.

The Bull conceded (R2.1 C-4): "the **central** inference-service case is **~5.3
years**… only the low-cost + high-revenue corner reaches ~2.6 yr. The '~2 yr'
V2 figure the Bull headlined is the *best corner of the favorable revenue
model*, not the expected case." Hold that against the project's own definition
of the target. The obsolescence window is ~2–3 years, and the project is
explicit that to clear it *with any return* "the node should pay back in well
under that — call **≤2 years** the target" (`wave4_synthesis.md` §2c). The
remaining ~0.5–1 yr of competitive life is the margin a viable business needs.

Now put the conceded central figure next to the target. **The central V2
inference-service payback (~5.3 yr) is not inside the 2–3 yr obsolescence
window. It is roughly double the window's upper bound, and roughly 2.5× the
≤2 yr viability target.** A node that pays back in 5.3 years, against silicon
with a 2–3 year competitive life, has *not paid back before it is obsolete* —
it pays back gross capital roughly two GPU generations too late. On the
project's own arithmetic, the *central case* for V2 is a money-loser, not a
"marginal-but-positive" business.

Where does the Bull's headline "~2.0 yr" come from, then? From
`data_science/REPORT.md` §1, which models Vera Rubin at a single point
estimate: $8.0M rack, 300 kW, ~$16M/rack-yr revenue → 2.0 yr
(`data_science/REPORT.md` table; `wave5_synthesis.md` §3, §4.2). But that same
$16M/rack-yr "mid revenue" row, in the wave-4 payback table, is the **5.3 yr**
cell at mid spacecraft cost (`wave4_synthesis.md` §2c: "Mid rev $16M/yr |
4.1 yr | **5.3 yr** | 7.5 yr"). The "~2.0 yr" figure is reachable only by
pairing mid revenue with *low* spacecraft cost — the left column, the
optimistic corner. The two project documents are not inconsistent; the
data-science REPORT simply picked the low-cost point. **The honest reading: V2
"pays back inside the window" only in the low-cost corner of the favorable
revenue model. At the central cost assumption — mid of an $8–35M range the
project calls "the weakest cost input in the whole project" (`wave4_synthesis.md`
§2a) — V2 pays back at ~5.3 yr and does not clear the window at all.**

The Bull's Round 2 verdict still says "V2's marginal-but-positive" economics
(`bull_case.md` S-6) and that the architecture "reaches the generation where
payback (~2 yr) clears the ~2–3 yr window" (it quotes ~2 yr again in S-6's
framing). But the Bull already conceded the central case is 5.3 yr. **Those two
statements cannot both be the expected case.** The Bear's surviving position:
the project has *not* shown V2 pays back inside the obsolescence window in
expectation. It has shown V2 pays back inside the window *in one corner* and
fails it at the center. That is the same structural finding wave 4 reached for
V1 — "only reaches the obsolescence window in its most optimistic corner"
(`wave4_synthesis.md` §2c) — and wave 5's levers, by the project's own honesty
check, moved it from "explicitly will not close" only to "closes, **marginally**"
(`wave5_synthesis.md` §1). Marginal, central-case-failing economics are not a
business decision; they are a reason to do exactly the bottom-up cost work the
project's own next-steps list puts first (`wave5_synthesis.md` §8 item 1).

**S-2 — The Bull's concessions did not weaken the Bear's case; on the
ground-segment and opex points they strengthened it.** The Bull conceded (C-2,
C-3) that the payback figures exclude opex *and* exclude the $100–500M ground
segment (`wave4_synthesis.md` §2b; `wave5_synthesis.md` §5;
`laser_comms/optical_ground_stations.md` §6). Layer that onto S-1. If the
*gross, opex-free, ground-segment-free* central V2 payback is already ~5.3 yr,
then the *true* business payback — node capital plus a share of a
$100–500M shared ground network plus station-keeping, ops staff, and the
end-of-life capacity haircut (the node glides to ~75–85% of beginning-of-life
compute — `wave5_synthesis.md` §4.1; `reliability_failure_handling.md` §5, §7) —
is *worse than 5.3 yr*. The Bull's concessions do not soften the Bear's
economic criticism. They confirm that even the optimistic-corner "~2 yr" figure
is gross-of-everything, and that the realistic central figure is comfortably
outside any plausible obsolescence window. **The economics criticism is the one
that survives both rounds intact, and the Bull's own Round 2 concessions are
now its strongest evidence.**

**S-3 — The two genuine, coupled, Rocket-Lab-controlled unknowns are not the
cheap part of the gate.** The Bear concedes the "five dependencies" framing
(BC-3) and adopts the Bull's count: two real engineering unknowns — the
block-upgrade and the radiator — plus commercial unknowns. But the Bull's
narrowed verdict ("fund the work to the next go/no-go gate") is not honest
about what resolving those two costs. They are not "resolvable in months,
several by Rocket Lab unilaterally" (`bull_case.md` surviving verdict) in the
way a *number* is:

- The **deployable radiator** is, by the Bull's own conceded C-8, "the venture's
  hardest single engineering item" — the biggest mass line, biggest deployment
  risk, biggest un-quoted cost, and the one subsystem with "no public evidence"
  Rocket Lab can build it (`rocket_lab/space_hardware_capabilities.md` §6;
  `node_design/node_mass_model.md` §7). Resolving it to a real go/no-go is not a
  desk study — it is a first-of-kind development program for a structure
  "larger than the ISS's main radiators" (`wave4_synthesis.md` §5). That is a
  multi-quarter, capital-consuming engineering effort, not a phone call.
- The **block-upgraded Neutron** cannot be "resolved in months" by Rocket Lab
  unilaterally either, because the base Neutron has not flown. The project's
  source is explicit: an Electron-style uprate "came ~3 years after debut"
  (`payload_and_block_upgrade.md` §5), and Neutron's operational reusable
  flights are NET 2027 (`payload_and_block_upgrade.md` open Q6;
  `wave4_synthesis.md` §5). A block-upgrade decision can be *made* on paper
  soon; it cannot be *resolved* — flown, payload-confirmed — before ~2030. V2,
  the only configuration the Bull claims as a real business, is gated on it for
  "full, un-power-capped" operation (`bull_case.md` R-1 item i).

So the "next gate" the Bull proposes funding is not a short cheap study. It is:
a real bottom-up spacecraft-cost build-up *plus* a deployable-radiator
development program *plus* a customer-discovery effort on an unobserved
willingness-to-pay *plus* waiting on Neutron's own flight campaign. That is a
substantial, multi-year, capital-committing program. The Bear does not oppose
funding it — but the honest label for it is "a funded R&D program with a
go/no-go several years out," not "a live, fundable venture" one decision away
from commitment. The Bull's verdict is directionally right and still slightly
oversells the proximity and cheapness of the gate.

**S-4 — Willingness-to-pay remains entirely unobserved, and the Bull conceded
it (C-7, R-5).** The Bull conceded the orbit-addressable TAM is unquantified
(C-7) and agreed the premium-value verdict must be quoted whole: "the premium
is justifiable in principle, the WTP is unmeasured, and customer discovery is
the highest-value open item" (`bull_case.md` R-5; `premium_value_case.md`
§verdict; `wave5_synthesis.md` §6.2, §8 item 8). The Bear accepts the Bull's
fair point that "unproven" describes the *number*, not the *demand components*
— the terrestrial supply crunch and the sovereign-AI market are observed and
quantified, and the Bear conceded that in Round 1 §7. But the surviving fact is
unchanged and load-bearing: the single most important input to the *revenue*
side of a venture whose central payback is already ~5.3 yr is a ~50% premium
that **has never been observed for orbital inference specifically**
(`wave5_synthesis.md` §6.2; `premium_value_case.md` open Q4). The entire
distance between the failing central case and the optimistic corner is
revenue-model and premium assumptions that no customer has yet confirmed. That
is not a criticism the Bull rebutted; it is one the Bull conceded.

**S-5 — The two unpublished Rocket Lab numbers and a not-yet-flown rocket still
stand.** The Bull conceded ~9.5 t SSO is the *central* estimate, not a
conservative one (C-5), with a defensible low end of 8.5 t at which the
baseline ceiling re-derives to ~165 kW and V1's margin "shrinks substantially"
(`wave5_synthesis.md` §2.2; `payload_and_block_upgrade.md` §2). That number is
"the single most important unverified number in the entire feasibility
analysis" (`payload_and_block_upgrade.md` §2). Fairing volume is likewise
unpublished (`wave5_synthesis.md` §7; `vision/initial_thesis.md` Rev 4 §2). And
the Bull's R-2 rebuttal — "a not-yet-flown Neutron is a timing risk, not a
verdict against the concept" — is *fair as far as it goes*: Rocket Lab flies
Neutron regardless of this venture, and a tank rupture in qualification testing
is what qualification testing is for ([Space.com](https://www.space.com/space-exploration/rocket-labs-new-neutron-rocket-suffers-fuel-tank-rupture-during-test)).
The Bear concedes that framing. But it cuts the other way too: if Neutron is a
timing input, then the *reusable downrange-landing payload to SSO* — the entire
economic baseline of this venture — is not merely unpublished, it is
**undemonstrated**, and will not be demonstrated until well after operational
reusable flights NET 2027 (`payload_and_block_upgrade.md` open Q6). The economic
model rests on a performance number for a flight mode the vehicle has not yet
flown once. That is not a reason the venture is *unsound* — the Bull is right
there — but it is a reason "commit" is premature, which is now common ground.

### R2.3 — The Bear's final position

After two rounds, the Bull and Bear have converged to within a narrow band, and
the honest verdict lives inside it.

**What both sides now agree on.** There is no physics wall (`wave5_synthesis.md`
§7) — necessary, not sufficient. The architecture is buildable today
(`node_mass_model.md` §6). The terrestrial supply crunch is real, quantified,
and worsening (`premium_value_case.md` §1, §3). Zero water is an unqualified
differentiator (`premium_value_case.md` §3). Rocket Lab is the best-positioned
company to *execute* this, owning all the node stack but the radiator
(`space_hardware_capabilities.md` §6). V1 is not a standalone profit centre
(`wave5_synthesis.md` §4.1). "The economics close" was an overstatement of
"closes marginally in the optimistic corner" (`bull_case.md` C-4). The right
decision today is *not* "build the constellation."

**Where the Bear still parts from the Bull.** The Bull's surviving verdict —
"fund the work to the next go/no-go gate… the case is genuinely strong" — rests
on two claims the evidence does not fully support:

1. **That V2 is "the standalone-profitable product."** It is not, in
   expectation. The Bull conceded the central V2 inference-service payback is
   ~5.3 yr (`bull_case.md` C-4) — roughly double the 2–3 yr obsolescence window
   and ~2.5× the ≤2 yr viability target the project itself sets
   (`wave4_synthesis.md` §2c). V2 pays back inside the window *only* in the
   low-cost corner of the favorable revenue model, and that figure is still
   gross of opex and the $100–500M ground segment (C-2, C-3). On the project's
   own arithmetic, V2's *expected* case is also a money-loser; only its best
   corner is not. "Standalone-profitable" is the optimistic corner relabeled as
   the expectation — the same move the Bull conceded for "the economics close."

2. **That the gate is short, cheap, and largely resolvable unilaterally in
   months.** Two of the five gate items — the deployable-radiator development
   and the block-upgrade — are a first-of-kind engineering program and a
   vehicle-upgrade gated on a rocket that flies operationally NET 2027
   (`space_hardware_capabilities.md` §6; `payload_and_block_upgrade.md` §5,
   open Q6). The gate is a multi-year, capital-committing R&D program, not a
   quick study.

**The Bear's final verdict.** The case *against committing to the venture*
survives both rounds, and survives it more cleanly than Round 1, because the
Bull conceded its load-bearing facts. The honest verdict the project should
carry forward is:

> This is a genuine, physics-cleared, well-differentiated engineering concept
> that Rocket Lab is uniquely equipped to attempt — and it is **not yet a
> venture to commit capital to, and not yet shown to be profitable even at
> V2**. The project's own central-case arithmetic puts V2 inference-service
> payback at ~5.3 yr against a 2–3 yr obsolescence window
> (`wave4_synthesis.md` §2c) — and that figure excludes opex and the
> $100–500M ground segment. V2 "closes" only in the optimistic corner of a
> revenue model whose central premium has never been observed
> (`wave5_synthesis.md` §6.2, §1). The defensible action is to **fund a
> bounded research-and-engineering program** — the bottom-up node cost model,
> the deployable-radiator make-vs-buy, customer-discovery on
> willingness-to-pay, and confirmation of Neutron's true SSO payload
> (`wave5_synthesis.md` §8) — with the explicit, honest understanding that
> this is a *multi-year program with a genuine chance of a no-go*, gated on a
> rocket that has not flown its reusable mode and a radiator subsystem that
> does not exist. That is a smaller, slower, and more conditional commitment
> than "this is a worthwhile venture — build it." It is the verdict the
> evidence supports.

The Bull's Round 2 narrowing — from "build this" to "fund the work" — moved
most of the way to the Bear's position. The remaining gap is whether the
project should say the venture's profitable configuration is *demonstrated*
(the Bull's "standalone-profitable V2") or *unproven and central-case-failing*
(the Bear's reading of the project's own ~5.3 yr table). On the documents, the
Bear's reading is the literal one. The project's conclusion should state the
economics as the project's own synthesis states them: closes **marginally**,
in the **optimistic corner**, at one generation — and not at all in the
central case.

### R2.4 — Sources added in Round 2

*Project research documents (cited again here):*
- `synthesis/wave4_synthesis.md` — §2b (payback excludes opex; "gross revenue
  to recover capital"), §2c (payback tables; central inference case 5.3 yr;
  ≤2 yr viability target; "most optimistic corner"), §2a ($8–35M spacecraft
  cost, "weakest cost input")
- `synthesis/wave5_synthesis.md` — §1 ("closes, marginally"), §2.2 (8.5 t →
  ~165 kW pessimistic corner), §2.4, §3 (crossover "resolved… just barely";
  generation table, Rubin row; honesty check on payback), §4.1 (V1 not a
  profit centre; end-of-life glide), §4.2 (V2 gated on block-upgrade; Rubin
  rack mass an estimate), §5 (ground segment $100–500M), §6.2 (no observed
  WTP), §8 (next-steps list; item 1 cost model, item 8 TAM)
- `data_science/REPORT.md` — §1 table (Vera Rubin 2.0 yr at $8.0M / 300 kW
  point estimate)
- `economics/rack_cost_trajectory.md` — §summary, price table (Vera Rubin
  NVL144 shipping H2 2026, $7.0–8.8M rack)
- `rocket_lab/neutron/payload_and_block_upgrade.md` — §2 (~9.5 t SSO central
  estimate, band 8.5–10.5 t), §5 (block-upgrade ~3 yr post-debut, speculative),
  open Q6 (reusable ops NET 2027)
- `rocket_lab/space_hardware_capabilities.md` — §6 (deployable-radiator gap)
- `node_design/node_mass_model.md` — §6 (1-rack architecture), §7 (radiator
  critical path)
- `node_design/reliability_failure_handling.md` — §5, §7 (end-of-life
  capacity glide)
- `economics/premium_value_case.md` — §1, §3 (supply crunch, zero water),
  §verdict (business case unproven), open Q4 (no observed WTP)
- `laser_comms/optical_ground_stations.md` — §6 (ground segment $100–500M)
- `llm_compute/inference_scaling.md` — §3 (inference bandwidth-light)
- `node_design/hot_chip_thermal_trajectory.md` — hot-loop on industry
  warm-water trajectory
- `LIBRARY.md` — `data_science/REPORT.md` row (crossover figure superseded)

*Independent sources:*
- [Space.com — Rocket Lab's new Neutron rocket suffers fuel tank rupture during test](https://www.space.com/space-exploration/rocket-labs-new-neutron-rocket-suffers-fuel-tank-rupture-during-test)

---

## Round 3 — Bear

*Round 3. Author: Bear. Date: 2026-05-17. The final round. Rounds 1–2 were
litigated against a 2–3-year GPU "obsolescence window." The project has since
re-based to a ~5-year GPU service life (`CONCLUSION.md` v2), demoted the 2–3-yr
case to a downside addendum, and the Bull has written a Round 3 on that basis.
This section reads the Bull's Round 3 in full and cross-checks it against the
project corpus and fresh independent research. It appends; it does not edit
Rounds 1–2. The Bear's job in this final round is two things: stress-test the
~5-year service-life assumption — now THE load-bearing assumption of the whole
venture — and re-run the economics honestly on that basis. Concede what is
genuinely achievable; press hard only where the evidence says press.*

### R3.0 — Framing: the corrected basis is legitimate, and that is the right place to start

The Bear will not dispute the re-basing on procedural grounds. The Bull's R3.0
argument — that nobody designs a payload to die in 2–3 years, that "obsolete ≠
broken," and that hyperscalers have normalized a six-year GPU depreciation life
— is sound and independently corroborated. The six-year depreciation norm is
real ([CNBC](https://www.cnbc.com/2025/11/14/ai-gpu-depreciation-coreweave-nvidia-michael-burry.html);
`economics/revenue_per_watt.md` §5), and the project's own revenue research
carried it before the debate began. **The Bear concedes the basis itself is
legitimate.** A 2–3-yr *obsolescence* window was the wrong denominator for a
*service-life* test; a declining-revenue curve over a longer life is the more
honest model.

But conceding the *framework* is not conceding the *number*. The re-basing did
two things at once: it (a) replaced a window with a service life — legitimate —
and (b) set that service life at ~5 years and asserted the design "can be built
to meet" it — a separate, load-bearing engineering claim that must now carry the
entire verdict. Round 3 of the Bear is about (b). And on the economics, the Bull
itself concedes in HC-1 that ~5.3 yr against ~5 years "leaves no margin." The
Bear's Round 3 position, stated up front: **the 5-year service life is *plausible
as a design target* but is not yet *demonstrated*, and the gap between "plausible
target" and "underwritten number" is exactly where this venture's risk now
lives — because on the project's own arithmetic, if the realized life is even
modestly short of 5 years, V2's central case fails again.**

### R3.1 — Stress-testing the 5-year service life: what the Bull gets right

A fair stress-test concedes the strong parts first.

**The radiation case is genuinely strong, and the Bear concedes it.** The Bull's
R3.2 Point 1 is well-sourced and the Bear's own Round 1 §4 already conceded SSO
radiation is benign. The new evidence the Bull brings strengthens it further:
Google proton-beam-tested its Trillium TPU and saw HBM irregularities only at
~2 krad(Si) — "nearly three times the expected (shielded) five-year mission dose
of 750 rad(Si)" — with no TID hard faults to 15 krad
([Google Research — Project Suncatcher](https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design/);
[DCD — Project Suncatcher](https://www.datacenterdynamics.com/en/news/project-suncatcher-google-to-launch-tpus-into-orbit-with-planet-labs-envisions-1km-arrays-of-81-satellite-compute-clusters/)).
Starcloud-1 ran a commercial H100 in orbit 30+ days without radiation-induced
crashes (`competitors/starcloud.md` §5). **On radiation specifically, a 5-year
life is not a hope — it is measured, with ~3× margin.** The Bear concedes this
fully and will not contest it.

**"Obsolete ≠ broken" and the declining-revenue tail are real.** The Bull's
"computing cascade" framing (years 1–2 frontier, 3–4 secondary, 5–6 batch) is a
genuine industry pattern, and the Bear conceded in R2.4 that inference is
bandwidth-light. A node past the frontier does keep earning. The Bear does not
dispute that the *shape* of the revenue curve is declining-but-positive.

That is the concession. It is real and it matters. What follows is where the
evidence does not support the Bull's "strong" verdict on achievability.

### R3.2 — Stress-testing the 5-year service life: the four threats the radiation case does not touch

The Bull's R3.2 leans heaviest on radiation — the one threat that is now
measured and benign. But radiation was never the dominant failure mode. The
project's own reliability doc says so explicitly: "SSO radiation at ~500–600 km
is fairly benign… **radiation is not the dominant mode**; terrestrial-style
attrition and thermal/cooling are" (`reliability_failure_handling.md` §4). The
Bull's strongest evidence addresses the *weakest* threat. The four threats that
actually bound the 5-year life are these — and on every one, the evidence is
thinner than R3.2 implies.

**Threat 1 — The coolant loop. The Bull conceded ~3.4-yr pump MTBF. Is it
disqualifying? No — but it is not the reassurance the Bull's framing implies.**
A representative AI-server cooling-pump MTBF is ~30,000 h ≈ **3.4 years**
(`reliability_failure_handling.md` §4) — *below* the 5-year mission. The Bull's
answer (R3.2 honest-bound, second bullet) is "N+1 redundancy makes this
tractable." Two honest problems with leaning on that:

- **N+1 does not multiply MTBF by the redundancy count when the loop is
  un-serviceable.** On the ground, N+1 works because a failed pump is *replaced*
  within hours and full redundancy is restored. In orbit there is no
  replacement: once the first pump fails (~3.4-yr characteristic life), the node
  runs on its backup with **zero remaining margin** for the rest of the mission.
  N+1 converts "the node dies at the first pump failure" into "the node dies at
  the second pump failure" — a real improvement, but for a 5-year life against a
  3.4-yr characteristic life, the probability that *both* pumps reach end-of-life
  inside the mission is not negligible. The honest framing is not "tractable"
  but "tractable only if the cooling subsystem is engineered with substantially
  more redundancy than N+1, and that redundancy mass is carried in a mass-bound
  node." The Bull's R3.2 does not carry that mass.
- **The hot-loop lever — the single biggest wave-5 mass saving — actively works
  against the coolant loop.** Running the loop hot "slightly worsens the
  Arrhenius wear-out component" (`wave5_synthesis.md` §7). Every 10 °C of loop
  temperature roughly *halves* electronics/pump MTBF under the Arrhenius
  relationship ([Wood Equipment — data-center pumps](https://woodequip.com/news/data-center-pumps-cooling-systems/)).
  The hot-loop is what makes a ~300 kW Rubin node flyable at all
  (`CONCLUSION.md` §ladder); it is also what erodes the MTBF of the subsystem
  the project itself calls "the leading whole-node killer." The venture's
  central mass lever and its central reliability risk are the *same knob turned
  in opposite directions*. The Bull's Round 3 names the coolant loop as the
  threat but does not engage this coupling — that the lever it relies on for
  flyability is the lever that worsens the 5-year-life risk.

  **Not disqualifying — but load-bearing.** A ~3.4-yr single-pump MTBF does not
  by itself sink a 5-year mission; mature spacecraft fly past single-string
  component lives routinely with block redundancy. But it does mean the 5-year
  life is *contingent on a cooling architecture that has never flown* — N+2 or
  better, hot-loop-derated, on a sealed orbital two-phase loop whose behavior the
  project's own open Q5 says "is not well characterized" for "a 3-year sealed,
  un-serviceable loop" (`reliability_failure_handling.md` open Q5) — let alone a
  5-year one. The Bull's "tractable" is doing a lot of unspoken work.

**Threat 2 — HBM wear, and the hot-loop runs HBM straight into its degradation
zone.** This is the threat the Bull's Round 3 does not mention at all, and it is
the most serious one fresh research surfaces. HBM is *already* the single
largest GPU failure mode — Meta's Llama-3 data put HBM at 17.2% of all
interruptions, and combined GPU-or-HBM at ~58.7% (`reliability_failure_handling.md`
§1). Independent analysis is blunt: **"HBM failures are the number one cause of
GPU failures," and HBM error rates "increase exponentially above 75 °C,
doubling for every 5 °C beyond that threshold"**
([Tom's Hardware — DRAM thermal](https://www.tomshardware.com/pc-components/cooling/the-data-center-cooling-state-of-play-2025-liquid-cooling-is-on-the-rise-thermal-density-demands-skyrocket-in-ai-data-centers-and-tsmc-leads-with-direct-to-silicon-solutions);
[IEEE Spectrum — HBM on GPU](https://spectrum.ieee.org/hbm-on-gpu-imec-iedm)).
Note what number that is: 75 °C. The hot-loop lever runs the *radiator surface*
at ~70–80 °C (`node_design/hot_chip_thermal_trajectory.md`). The project's
defense is that loop ΔT keeps the *junction* safe — but the project itself flags
that as "**plausible but unmodeled in detail**" (`wave5_synthesis.md` §7). For a
5-year life, the question is not whether the junction survives a single pass; it
is whether HBM stacks held near their exponential-degradation knee for ~16,000
eclipse thermal cycles over five years degrade gracefully or accelerate. **There
is no answer to that in the corpus or in public field data** — and the Google
proton test the Bull cites measured *radiation* tolerance, not *thermal wear-out
over a multi-year life*. The Bull's R3.2 cites HBM's radiation hardness and is
silent on HBM's thermal wear. Those are different failure mechanisms, and the
hot-loop helps the first while plausibly worsening the second.

**Threat 3 — Thermal cycling, and a packaging failure mode that is already
biting on the ground.** In LEO the node passes through eclipse ~15×/day —
~16,000 cycles over a 3-year life, ~27,000 over five
(`reliability_failure_handling.md` §4). Differential thermal expansion fatigues
solder joints and interconnects; this is a *primary* driver of the constant-rate
attrition burn-in cannot remove. Fresh research makes this concrete and current:
the GB200's own well-documented overheating problems were rooted in **"LSI
components in the substrate heating and cooling at a different rate, causing the
interfacing to warp over time, damaging the chip connections"**
([DCD — Nvidia redesigns NVL72 racks](https://www.datacenterdynamics.com/en/news/nvidia-redesigns-72-gpu-ai-server-racks-after-blackwell-gpus-overheat-report/);
[TrendForce](https://www.trendforce.com/news/2025/01/14/news-nvidia-gb200-racks-reportedly-overheat-major-clients-cut-orders/)).
That is a *thermal-cycling fatigue* failure — exactly the mechanism a node
cycling 27,000 times over five un-serviceable years is most exposed to. NVIDIA
addressed it on the ground with rack redesigns; an orbital node gets one design,
no redesign, no swap. The Bull's R3.2 treats degradation as a smooth, mature,
well-understood "graceful glide." The graceful-glide table in
`reliability_failure_handling.md` §5 is explicitly **a model output over a
3-year life on an assumed AFR, not a measured 5-year curve** — and the doc says
the AFR figure "likely *understates* a space node." Extrapolating a 3-year model
glide to a 5-year life is not the same as having a 5-year number.

**Threat 4 — All hard reliability data is H100-era; V2 flies Rubin.** The Bull
concedes this (R3.2 honest-bound, first bullet) and the Bear credits the
concession. But it is worth stating how large a hole it is. The entire ~7–9% AFR
planning figure, the entire graceful-glide model, the entire "mature, solved
problem" framing rests on H100 field data. GB200/GB300 "run hotter and have **no
published field-reliability data yet**" (`lint_report_2.md` §5.5;
`reliability_failure_handling.md` open Q2) — and as Threat 3 shows, the limited
GB200 data that *does* exist is a *story of a thermal-reliability defect serious
enough to make hyperscalers cut orders*. V2 flies *Rubin*, a generation beyond
even that, hotter still, with literally zero field-reliability data. The 5-year
life for the silicon V2 actually flies is not "strongly supported by evidence" —
it is an extrapolation from a two-generations-prior chip, adjusted in the
*adverse* direction by every trend line (hotter, denser, newer).

**The verdict on achievability.** Is ~5-year service life for a dense,
liquid-cooled, un-serviceable AI rack in SSO genuinely achievable? The honest
answer: **plausible as an engineering target, not yet demonstrated, and softer
than the Bull's "strong" verdict.** The radiation half is genuinely settled.
The thermal/cooling half — which the project itself says is the *dominant*
failure domain — is not: a sub-mission single-pump MTBF, a hot-loop lever that
trades against both pump life and HBM wear, a thermal-cycling fatigue mode
already biting the *previous* GPU generation on the ground, and zero field data
on the generation V2 flies. None of these is a *wall* — they are all
engineering problems with known mitigation directions. But "achievable with a
cooling and packaging architecture that has never flown, verified only by
flying V1 first" is a materially weaker claim than R3.2's "the evidence that
~5 years is achievable is strong." The Bear's position: **call it ~5 years as a
design *requirement*, treat anything from ~3.5 to ~5 years as the genuine
outcome band until V1 flies, and — critically — note that the economics (R3.4)
fail at the bottom of that band.**

### R3.3 — Cross-examining the Bull's specific claims on the 5-year basis

**CX3-1 — "A LEO satellite in dawn-dusk SSO has a ~5-year natural mission life
anyway" (Bull R3.0 point 1; R3.2 point 1).** Half-true, and the soft half
matters. The ~5-year *average* LEO life is real ([LinkedIn/industry — LEO vs GEO
lifespans, ~5 yr average](https://www.linkedin.com/advice/1/how-do-leo-geo-satellites-differ-terms)).
But "average life" is not "the life you can count on for an underwriting." Fresh
research: **Starlink deorbited nearly 500 satellites in the first half of 2025,
"all less than 5 years old"** ([Communications Daily — Starlink short life
expectancy](https://communicationsdaily.com/source/971084)), and across LEO
satellites surviving launch, **~4% fail within the first year**, with
mission-ending failures led by the *communications subsystem (26%)* and *power
system (18%)* ([Aerospace Corporation — satellite lifetime study](https://aerospace.org/story/majority-satellites-exceed-design-life);
[Medium/d*classified — in-orbit lifetime factors](https://medium.com/d-classified/analyzing-factors-of-in-orbit-lifetime-of-satellites-in-low-earth-orbit-1eaccfe61b16)).
Two consequences the Bull's framing omits: (a) the "~5-year natural life" is a
distribution with a real left tail, not a floor — a ~5.3-yr payback against a
*mean* 5-yr life means roughly *half* the fleet pays back after death; and (b)
the dominant satellite-bus failure modes (comms, power) are *additional* to the
GPU/cooling failure modes — they stack. A compute node must survive *both* its
bus and its payload for five years. The Bull's Round 3 models only the payload
side.

**CX3-2 — "The build-to-learn V1 program is literally the mechanism that
verifies the 5-year life" (Bull R3.2 Point 3).** The Bear agrees this is the
*correct* de-risking mechanism — and that agreement is itself the problem for
the Bull's verdict. If V1 is the qualification campaign for the 5-year life,
then the 5-year number is **not verified until V1 has flown for ~5 years.**
V1's own qualification flight depends on Neutron's reusable mode (operational
NET 2027, `payload_and_block_upgrade.md` open Q6); a V1 launched ~2028 yields a
verified 5-year-life number around **~2033**. The Bull's R3.2 Point 3 presents
"V1 verifies the life" as a *strength*; read on the calendar it is a statement
that the load-bearing assumption of the *V2* business case cannot be confirmed
until the early 2030s. That does not argue against funding V1 — the Bear has
supported funding the bounded program since Round 2. It argues against the Bull
treating the 5-year life as established enough to call V2 "borderline-viable" in
the present tense. The honest tense is future-conditional.

**CX3-3 — "A front-loaded declining curve pulls the crossover modestly earlier
than 5.3 yr" (Bull R3.1).** The Bull is careful here — it explicitly declines to
invent a number and concedes the project has not re-run the table on a declining
curve. The Bear credits that restraint. But the claim's *direction* deserves one
qualification. A declining curve front-loads revenue **only relative to a flat
curve of the same lifetime total**. The ~5.3-yr figure comes from the wave-4
table's flat "$16M/rack-yr mid revenue" row (`wave4_synthesis.md` §2c). If the
declining curve is anchored so that year-1 rate = $16M and it *declines* from
there, then yes, payback is modestly earlier. But if $16M was the *lifetime
average* (the more natural reading of a "mid revenue" planning figure), then a
declining curve has year-1 *above* $16M and the tail *below* — and the project
has not stated which. The Bull's "direction is unambiguous" holds only under the
first reading. Under the second it is ambiguous. This is minor — it is a "the
project has not modeled this" flag, not a refutation — but the Bull's "modestly
earlier" should be "modestly earlier *if* the curve is anchored at the early
rate, which the project has not specified."

**CX3-4 — "Borderline-viable, not a cliff failure" as a change of *category*
(Bull R3.1, R3.4).** This is the Bull's central Round 3 move and it is *partly*
fair. Moving from "fails by 2× a 2–3-yr window" to "lands at the edge of a 5-yr
life" is a real change — the Bear conceded the basis in R3.0. But "change of
category" overstates it. Examine what "borderline-viable" actually means on the
project's own numbers, which is the subject of R3.4.

### R3.4 — Re-running the economics honestly on the 5-year basis

The Bear concedes plainly: **V2 moving "within the service life" is real.** On a
~5-year life, a ~5.3-yr central payback is no longer a 2× failure; it is inside
the life's *outer edge*. That is a genuine improvement and the Bear does not
contest it. But "borderline-viable" is a verdict that has to survive three
honest tests, and on the project's own arithmetic it survives none of them
cleanly.

**Test 1 — Does ~5.3 yr actually sit *inside* a ~5-year life? No — it sits just
*outside* it.** This is arithmetic, not interpretation. The central V2
inference-service payback is ~5.3 years (`wave4_synthesis.md` §2c, mid-cost
mid-revenue cell). The service life is ~5 years. **5.3 > 5.0.** The Bull's R3.1
says ~5.3 yr "sits at the edge of the service life — it crosses gross-capital
break-even right around end-of-life." Read precisely, "right around end-of-life"
means *the node pays back its gross capital ~0.3 years after it is dead*. Even
the Bull's own `CONCLUSION.md` v2, quoted in HC-1, says ~5.3 yr "leaves no
margin" — but the literal arithmetic is slightly worse than no margin: at the
central case the node does not quite finish paying back its *gross node capital*
within its service life. "Borderline-viable" is the generous label; "central
case still does not close, now by a thin margin instead of a 2× margin" is the
literal one.

**Test 2 — Does it clear payback once opex and the ground segment load on? No —
and this is the test that actually decides it.** Here the Bull's own Round 2 and
Round 3 concessions are the Bear's evidence. The ~5.3-yr figure is **gross
top-line revenue ÷ node capital — it excludes node opex (station-keeping, ops
staff) and excludes the $100–500M shared ground segment** (`wave4_synthesis.md`
§2b; `wave5_synthesis.md` §5; conceded by the Bull at C-2, C-3 and again at
HC-1). Layer those on:

- Node opex over a 5-year life — station-keeping propellant, ops staff, the
  control plane — is not zero against a node billing ~$16M/yr.
- The ground segment is **$100–500M of capital** for a constellation
  (`laser_comms/optical_ground_stations.md` §6). Amortized across a first
  commercial constellation of ~4–8 nodes (`CONCLUSION.md` §deployed-system),
  that is **~$12–125M of shared capital *per node*** — a 15%-to-over-100%
  surcharge on a ~$85M node. Even at the favorable end it pushes the effective
  per-node capital materially above $85M, and payback scales with capital.
- The end-of-life capacity haircut: the node glides to ~75–85% of
  beginning-of-life compute (`wave5_synthesis.md` §4.1) — so lifetime-average
  billable capacity is ~80%, not 100%, and the revenue side of the ratio should
  be haircut accordingly.

**Each of these three corrections moves payback the wrong way. The Bull does not
dispute any of them — it concedes all three (HC-1). The honest conclusion: if
the *gross, opex-free, ground-free* central payback is already ~5.3 yr — already
past the ~5-year life — then the *true business* payback at the central case is
unambiguously outside the service life.** "Borderline-viable" describes the
gross figure; the all-in figure at the central case is "does not pay back within
the asset's life." The Bull states this itself in HC-1 — "the true business
crossover for the central case is at or beyond end-of-life, not inside it." The
Bear simply notes: that concession *is* the verdict. A central case that does
not return its capital before the asset dies is, in plain terms, a money-loser
at the central case. The 5-year basis changed the size of the miss from large to
thin. It did not change the sign.

**Test 3 — Is the ~70%+ premium needed for a comfortable crossover defensible?
Not yet — and the Bull conceded the re-basing made this *worse*, not better.**
This is the most important point of the Bear's Round 3 and it is established by
the Bull's own HC-2. `CONCLUSION.md`'s premium sweep is explicit: the cumulative
cash-flow crossover turns positive within the ~5-year life only at a **~70%-and-
above** premium; at ~50% it is borderline; below ~50% it does not cross
(`CONCLUSION.md` §Profitability-4). The Bull's Rounds 1–2 case rested on "a ~50%
premium is plausible and the thesis never needs more than that." The corrected
basis *breaks* that claim: at 50% the crossover is now only borderline; a
*comfortable* return needs ~70–100%+. The Bull concedes this in HC-2 — "the
thesis now needs a *larger* premium than Round 2 claimed."

Hold that against what is *known* about willingness-to-pay: **nothing.** There is
"no observed willingness-to-pay data for orbital inference specifically"
(`wave5_synthesis.md` §6.2; `premium_value_case.md` open Q4). The ~50% figure
was already a reasoned estimate, not a measurement; the venture now needs the
*realized, unobserved* premium to land not at that already-unverified ~50% but
at ~70%+ — a **~40% higher premium than the project's own anchor**, with the
same zero observations behind it. And it must clear that bar while the product
carries orbit's real disadvantages: latency that rules out interactive serving,
orders-of-magnitude-lower aggregate bandwidth, and un-upgradeable disposability
(`premium_value_case.md` §8). The Bull's Round 3 is honest enough to concede
HC-2; the Bear's job is to state what HC-2 means. **It means the corrected basis
did not strengthen the revenue case — it raised the bar the revenue case must
clear, while the evidence behind the revenue case stayed at zero.** A ~5.3-yr
payback against a ~5-yr life is only "borderline-viable" *if* the premium lands
at ~70%+; at the project's own ~50% anchor it is, in the sweep's own word,
merely "borderline" — crossing at end-of-life — and that is before opex and
ground segment (Test 2). The honest reading: the comfortable-crossover premium
is not defensible on current evidence, because there is no current evidence
either way.

**Is a ~5.3-yr payback against a ~5-yr life a margin-free knife-edge? Yes — and
the project says so.** `CONCLUSION.md` v2 itself: "~5.3 yr is still at the edge
of a ~5-year life, leaving no margin." A knife-edge is a fragile place to site a
capital commitment, because *everything* has to break favorably at once: the
spacecraft cost must land at the $18M mid of an $8–35M range the project calls
"the weakest cost input in the whole project" (not the high end); the realized
service life must hit ~5 years (not the ~3.5–4 yr the coolant-loop and Rubin-HBM
risks of R3.2 make a live possibility — the Bull concedes this exact downside in
HC-3); the premium must land at ~70%+ (unobserved); and the SSO payload must hold
near ~9.5 t (an estimate, range 8.5–10.5 t). The 5-year basis removed one
source of failure — the 2–3-yr cliff. It left every other one in place, and the
remaining margin is now so thin that any *single* adverse outcome among those
four re-opens the central-case failure. That is not "borderline-viable." It is
"viable only if four independent unknowns all land favorably," which is the same
structural critique the Bear made in Round 1 §2 — narrowed, but not dissolved,
by the corrected basis.

### R3.5 — The Bear's final position after three rounds

Three rounds in, the Bull and Bear have converged to a genuinely narrow band,
and the honest final verdict lives inside it. The Bear states it plainly.

**What three rounds of debate settled — common ground.** There is no physics
wall (`wave5_synthesis.md` §7). The architecture is buildable today
(`node_mass_model.md` §6). The terrestrial supply crunch is real, quantified,
worsening (`premium_value_case.md` §1, §3). Zero water is an unqualified
differentiator (`premium_value_case.md` §3). Rocket Lab is the best-positioned
company on Earth to *execute* this (`space_hardware_capabilities.md` §6). V1 is
not a standalone profit centre (`wave5_synthesis.md` §4.1). SSO radiation is
benign and now *measured* benign on the exact silicon class — a 5-year life is
not radiation-limited (`competitors/starcloud.md` §5; Google Suncatcher test).
The re-basing from a 2–3-yr obsolescence window to a ~5-year service life is
*legitimate* — "obsolete ≠ broken" is a real correction. And the right decision
today is *not* "build the constellation" — the Bull conceded this in Round 2 and
has not withdrawn it.

**What the Bear's final position is — and where it still parts from the Bull.**

1. **On the 5-year service life:** it is a **defensible engineering *target*,
   not a demonstrated *fact*.** Radiation is settled; the thermal/cooling
   domain — which the project itself calls the *dominant* failure domain
   (`reliability_failure_handling.md` §4) — is not. The coolant loop has a
   sub-mission single-pump MTBF (~3.4 yr) and the hot-loop lever worsens it;
   HBM sits near a 75 °C exponential-degradation knee that the hot-loop pushes
   toward and that the project's junction defense is "unmodeled in detail" on;
   thermal-cycling fatigue is already a documented GB200-generation defect; and
   V2's actual silicon, Rubin, has zero field-reliability data. The Bull's
   "strong" achievability verdict overstates a case that is genuinely only
   *plausible*. The honest outcome band is **~3.5–5 years**, resolved only by
   flying V1 — meaning the V2 business case's load-bearing number is not
   confirmable until the early 2030s.

2. **On the economics:** the Bear concedes V2 moving "within the service life"
   is real — but **"borderline-viable" is not "profitable," and on the
   project's own central-case arithmetic V2 does not clear payback.** The
   central ~5.3-yr gross payback is already slightly *past* a ~5-year life;
   once node opex and the $100–500M ground segment load on — both conceded by
   the Bull (HC-1) — the all-in central-case payback is unambiguously outside
   the asset's life. V2 "closes" only at a ~70%+ premium that the project's own
   sweep requires and that is entirely unobserved — and the re-basing *raised*
   that bar from the ~50% the Bull's earlier rounds relied on, while adding zero
   new evidence that any customer will pay it. A ~5.3-yr payback against a
   ~5-yr life is, in `CONCLUSION.md`'s own words, a margin-free knife-edge: it
   holds only if spacecraft cost, realized service life, premium, and SSO
   payload *all* land favorably. Any one miss re-opens the central-case failure.

3. **The Bear's final verdict.** The case *against committing to the venture*
   survives all three rounds. The corrected ~5-year basis genuinely improved
   the venture's standing — it removed the 2–3-yr cliff and is honestly come by
   — but it improved it from "fails the economic test by ~2×" to "fails the
   honest all-in economic test by a thin margin at the central case, and
   passes only in an optimistic corner that requires an unobserved ~70%+
   premium and an undemonstrated 5-year hardware life." That is a better place
   than Round 2, and it is still not a place from which a capital commitment is
   warranted. The Bear's final position is unchanged in kind and sharpened in
   detail:

   > This is a physics-cleared, well-differentiated engineering concept that
   > Rocket Lab is uniquely equipped to attempt — and on the corrected ~5-year
   > service-life basis it is **borderline-viable, not proven profitable, and
   > resting on a 5-year hardware life that is a design target rather than a
   > demonstrated fact.** The defensible action is exactly what both sides now
   > converge on: **fund a bounded, multi-year build-to-learn research-and-
   > engineering program** — the bottom-up node-cost build-up, the
   > deployable-radiator make-vs-buy, customer-discovery to *observe* the
   > willingness-to-pay premium, a coolant-loop and HBM-thermal reliability
   > program targeting a verified 5-year life, and confirmation of Neutron's
   > true reusable SSO payload — with the explicit, honest understanding that
   > V1 flying *is* the 5-year-life qualification campaign, that the V2 business
   > case therefore cannot be underwritten until the early 2030s, and that the
   > program carries a genuine, non-trivial chance of a no-go. That is the
   > verdict the evidence supports: not "build it," and not "it is profitable" —
   > but "fund the work to find out, eyes open about how much is still
   > unproven."

The gap between Bull and Bear after three rounds is now almost entirely one of
*tense and emphasis*. The Bull says V2 *is* borderline-viable; the Bear says V2
*would be* borderline-viable *if* a 5-year hardware life is achieved and *if* a
~70%+ premium is realized — and that both remain unproven. `CONCLUSION.md` v2
should carry the venture exactly as it is: physics-cleared, well-differentiated,
borderline-viable on a service-life basis that is itself a named, unresolved
go/no-go unknown — and not one step further.

### R3.6 — Sources added in Round 3

*Project research documents (cited again here):*
- `CONCLUSION.md` — §Verdict, §Profitability-2 (5-year service-life basis),
  §Profitability-4 (premium sweep; crossover positive only at ~70%+),
  §What-it-hinges-on, §deployed-system (4–8-node first constellation),
  §Revision-history (v2)
- `synthesis/wave4_synthesis.md` — §2b (payback excludes opex and ground
  segment), §2c (payback tables; central inference case 5.3 yr; ≤2 yr target)
- `synthesis/wave5_synthesis.md` — §4.1 (V1 not a profit centre; end-of-life
  glide to ~75–85%), §5 (ground segment $100–500M), §6.2 (no observed WTP),
  §7 (hot-loop "unmodeled in detail"; hot-loop worsens Arrhenius wear-out;
  coolant loop the leading kill-mode)
- `node_design/reliability_failure_handling.md` — §1 (HBM 17.2% of
  interruptions; AFR understates a space node), §4 (radiation not the dominant
  mode; thermal/cooling are; ~30,000 h pump MTBF; ~16,000 thermal cycles/3 yr),
  §5 (graceful-glide table is a 3-year model output, not a measured 5-yr
  curve), open Q2 (no Blackwell/Rubin field data), open Q5 (sealed orbital
  coolant loop not well characterized)
- `node_design/hot_chip_thermal_trajectory.md` — hot-loop runs radiator surface
  ~70–80 °C
- `synthesis/lint_report_2.md` — §5.5 (no GB200/Rubin field-reliability data)
- `economics/revenue_per_watt.md` — §5 (six-year hyperscaler depreciation norm)
- `economics/premium_value_case.md` — §8 (latency/bandwidth/disposability
  drawbacks), open Q4 (no observed WTP)
- `laser_comms/optical_ground_stations.md` — §6 (ground segment $100–500M)
- `competitors/starcloud.md` — §5 (Starcloud-1 H100 30+ days, TPUs
  radiation-hard)
- `rocket_lab/neutron/payload_and_block_upgrade.md` — open Q6 (reusable ops
  NET 2027)

*Independent sources (new in Round 3):*
- [Google Research — Exploring a space-based, scalable AI infrastructure system design (Project Suncatcher; Trillium TPU proton-beam test, HBM irregularities at ~2 krad ≈ 3× the five-year shielded dose)](https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design/)
- [Data Center Dynamics — Project Suncatcher: Google to launch TPUs into orbit](https://www.datacenterdynamics.com/en/news/project-suncatcher-google-to-launch-tpus-into-orbit-with-planet-labs-envisions-1km-arrays-of-81-satellite-compute-clusters/)
- [Tom's Hardware — The data center cooling state of play (2025): HBM error rates increase exponentially above 75 °C, doubling per 5 °C](https://www.tomshardware.com/pc-components/cooling/the-data-center-cooling-state-of-play-2025-liquid-cooling-is-on-the-rise-thermal-density-demands-skyrocket-in-ai-data-centers-and-tsmc-leads-with-direct-to-silicon-solutions)
- [IEEE Spectrum — HBM on GPU: thermal challenges](https://spectrum.ieee.org/hbm-on-gpu-imec-iedm)
- [Data Center Dynamics — Nvidia redesigns 72-GPU AI server racks after Blackwell GPUs overheat (thermal-cycling substrate warping)](https://www.datacenterdynamics.com/en/news/nvidia-redesigns-72-gpu-ai-server-racks-after-blackwell-gpus-overheat-report/)
- [TrendForce — NVIDIA GB200 racks reportedly overheat, major clients cut orders](https://www.trendforce.com/news/2025/01/14/news-nvidia-gb200-racks-reportedly-overheat-major-clients-cut-orders/)
- [Wood Equipment — How pumps support data center reliability (Arrhenius: every 10 °C roughly doubles/halves MTBF)](https://woodequip.com/news/data-center-pumps-cooling-systems/)
- [Communications Daily — The short life expectancy of Starlink's LEO satellites (≈500 deorbited H1 2025, all under 5 years old)](https://communicationsdaily.com/source/971084)
- [Aerospace Corporation — Majority of satellites exceed design life (LEO satellite lifetime study; ~4% first-year failure)](https://aerospace.org/story/majority-satellites-exceed-design-life)
- [Medium / d*classified — Analyzing factors of in-orbit lifetime of satellites in LEO (mission-ending failures: comms 26%, power 18%)](https://medium.com/d-classified/analyzing-factors-of-in-orbit-lifetime-of-satellites-in-low-earth-orbit-1eaccfe61b16)
- [CNBC — How long before a GPU depreciates (hyperscaler six-year useful-life norm)](https://www.cnbc.com/2025/11/14/ai-gpu-depreciation-coreweave-nvidia-michael-burry.html)
