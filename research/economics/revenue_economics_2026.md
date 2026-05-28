# Revenue Economics of Frontier AI Compute — What a Rack Actually Earns (2026)

*Research date: 2026-05-18. Prepared for the Rocket Lab orbital AI-inference data center feasibility project. Companion to and partial update of `economics/revenue_per_watt.md`, `economics/hyperscaler_margins.md`, `economics/energy_operating_costs.md`, and `../valuation/ai_compute_trajectory.md`.*

> **Purpose.** The valuation calculator's single most-contested input is **per-rack revenue** — what one NVL72-class rack of GPUs earns per year. The calculator anchors it at **$13M/rack-year (2026)** as an "owner-operator" rate, growing **~15%/yr**, with a separate orbital premium on top. This document re-grounds that number in current (2026) disclosures and market data, traces its trajectory, reframes it against the customer's *total* cost of owning compute (so an "orbital premium" is a premium over something concrete), and delivers a verdict on whether the $13M anchor and 15% growth are defensible.

> **Reading guide.** Claims are tagged **[FACT]** (company-disclosed / reported 2025–26 data), **[ESTIMATE]** (third-party estimate for a private figure), **[DERIVED]** (our arithmetic), or **[PROJECTION]** (directional forecast — explicitly subjective). Hard numbers are cited inline and cross-checked against ≥2 sources where possible. Every per-rack figure normalizes to a **GB200/GB300 NVL72-class rack: 72 GPUs, ~130–145 kW IT load** — the current frontier unit and the calculator's base-year rack.

---

## Summary

**The three layers, current (2026), per NVL72-class rack-year.** The most common error in this debate is quoting one number for three different businesses. They are genuinely different:

| Layer | What it sells | 2026 rate, per NVL72-class rack-year | Confidence |
|---|---|---|---|
| **(1) Renter / reseller clears** | Re-sells GPU-hours it does not own; earns the spread over its own rental/lease cost | **~$1–2M net** (gross billings ~$8–14M, but most is pass-through) | the margin is thin and contested |
| **(2) Owner-operator earns** | Owns the hardware outright, sells its capacity as IaaS | **~$8–14M gross billings; ~$10–12M central** | Moderate-high — anchored to CoreWeave, Oracle, Crusoe disclosures |
| **(3) Integrated inference-service earns** | Runs its own model, bills per token | **~$15–25M+ gross** *if* the model is competitive — but this is model-value capture, not compute capture | Moderate — conditional on owning a competitive model |

- **The calculator's $13M owner-operator anchor (2026) is defensible — it sits in the top half of a credibly-sourced ~$8–14M band, and is justifiable as a 2026 *frontier* (GB300-class) owner-operator rack sold at strong utilization.** It is *not* conservative. A more central owner-operator figure is **~$10–12M/rack-year**; $13M is the optimistic-but-not-indefensible end. The honest read: $13M is at the high end of "defensible," and the calculator should know that — it is not a midpoint. See §5.
- **Per-rack revenue *is* a growing number, but ~15%/yr is at the upper edge of defensible.** The growth driver is real — each NVIDIA generation costs ~2×/generation more (GB200 ~$3M → GB300 ~$6M → Rubin ~$5–8.8M), and rental rates rise with hardware cost (GB200 on-demand +21% since mid-2025; B200 index +24% in a single month in early 2026 on an HBM price hike). But over a *full* generational cycle, per-rack gross revenue has historically risen **~2–3× over ~3 generations** — a CAGR of roughly **8–13%**, not 15%. **~10–12%/yr is the better-supported central trajectory; 15% is aggressive.** See §3.
- **Revenue should NOT be framed as a rack-rental sticker price alone.** The customer's real alternative is the *total cost of owning and running compute terrestrially*: hardware + real estate + the recurring **energy** bill + cooling/water. An orbital operator converts the recurring energy cost into one-time solar capex. On Epoch AI's 1 GW model, energy is **~$0.6B/yr of an ~$8.5B/yr TCO (~7%)** when capex is annualized — but it is **~65–70% of cash opex**, it is **rising fast** (PJM wholesale +75% YoY into Q1 2026), and the *non-energy* facility/real-estate/cooling layer adds another large slice. The orbital premium is a premium over the *delta* a customer would pay terrestrially for power + real estate + cooling — quantified in §4 at very roughly **$2–4M per NVL72 rack over a 5-year life today, and rising**. This is real money, but it is second-order against the rack hardware itself.
- **Verdict.** Keep the **$13M (2026)** anchor but treat it as the **high end of a $10–13M defensible band**, not a midpoint — consider $11–12M as the central case. **Cut the growth rate from 15% to ~10–12%/yr.** The qualitative direction of the calculator (revenue grows, but slower than rack cost) is correct and well-supported; the magnitudes are slightly hot. See §5 for the full verdict.

**Confidence: Moderate-high** on public-company disclosures (CoreWeave, Oracle, Nebius are listed reporters); **moderate** on the per-rack translation (the rack is not a unit any company reports — every $/rack figure is our division of a $/GW or $/GPU disclosure); **moderate** on the trajectory (direction robust, magnitude ±30–50%); **lower** on the orbital-premium-over-TCO framing (willingness-to-pay for *orbital* compute is entirely unobserved).

---

## 1. The three layers — why one number cannot answer the question

A frontier AI lab buying compute pays a price. That price is earned by *someone* — but "who, and how much" depends on which of three businesses you are. The calculator's "$13M owner-operator" is layer 2. The project must keep the layers distinct because they differ by **5–10×**.

### Layer 1 — what a renter / reseller *clears*

A pure reseller (the classic "neocloud" model in its thinnest form, or a broker) buys or leases GPU capacity it does not own and re-sells GPU-hours. Its **gross billings** look large — an NVL72 rack rents on-demand for ~$756–1,944/hr (§2), i.e. **~$6–17M/year of gross billings** at high utilization. But it must pay for the capacity it resold. **What it *clears* is the spread**, and that spread is thin:

- The bare GPU-rental layer is **competed down to roughly break-even operating margin** once honest depreciation is counted. CoreWeave — the largest pure-play — posted a **FY2025 net loss of $1.17B on $5.13B revenue** (a ~−23% net margin) and roughly breakeven-to-negative operating margin during buildout. [FACT — `hyperscaler_margins.md`; Constellation Research]
- A reseller that does not even own the hardware (true arbitrage) clears less still — only the markup over its lease cost, typically a few percent to low-double-digit points of gross.
- **Net to a reseller: order ~$1–2M per NVL72 rack-year of *cleared* (gross-margin-after-capacity-cost) revenue** — and that is before its own SG&A, financing, and R&D. [DERIVED]

The renter layer is not the calculator's anchor and should not be. It is included only to make the point: a large gross billings number (~$8–14M/rack) is *not* what a thin-layer player keeps.

### Layer 2 — what an owner-operator *earns* (the calculator's anchor)

An owner-operator **owns the GPUs outright** and sells their capacity. It does not pay a renter's markup to anyone — it captures the IaaS rate directly. This is the right layer for the orbital venture (Rocket Lab would own its racks) and is the calculator's `owner_operator_anchor_musd`.

What an owner-operator's capacity earns, per NVL72-class rack-year, from real disclosures:

- **CoreWeave (the cleanest public anchor).** FY2025 revenue **$5.13B against ~850 MW of active power at year-end** ⇒ a naive **~$6.0M per MW-year** ([implied $5,131M ÷ 850 MW](https://www.fool.com/investing/2026/04/15/coreweave-has-a-massive-88-billion-revenue-backlog/)). But 2025 was a steep ramp — much of that 850 MW energized *during* the year, so average revenue-generating capacity was well below 850 MW and the *mature-capacity* rate is materially higher. CoreWeave's **FY2026 guidance — $12–13B revenue against an exit-2026 target of ~1.7 GW active power** — implies, on the exit run-rate, roughly **$17–19B ARR ÷ ~1.7 GW ≈ $10–11M per MW-year** on more-mature capacity. [FACT — Constellation Research; DCD]
- An **NVL72 rack draws ~130–145 kW IT**; at a facility level (PUE ~1.2–1.3) it occupies ~165–185 kW of *total* MW capacity. So CoreWeave's ~$10–11M/MW-year ⇒ **~$1.7–2.0M per NVL72 rack-year if you measure against *total facility* MW**, or **~$1.4M per rack-year against IT MW** — *wait*. This translation needs care, and it is the crux of the whole debate. See the boxed reconciliation below.

> **The MW-to-rack reconciliation — read this carefully.** There are two different "per rack" numbers and conflating them is the error that produces both the $2M and the $13M figures.
>
> 1. **Revenue per MW of *capacity* × kW per rack.** CoreWeave earns ~$6M/MW-year (FY2025 average) to ~$10–11M/MW-year (mature exit-rate). An NVL72 rack at ~0.13–0.18 MW ⇒ **~$0.8–2.0M per rack-year.** This looks far below $13M.
> 2. **But CoreWeave's "MW" is dominated by H100/H200/GB200 mixed-generation capacity, much of it older and cheaper-renting silicon, and its revenue-per-MW is depressed by (a) ramp timing and (b) contract discounts on take-or-pay backlog.** A *frontier-generation* NVL72 rack sold near current on-demand pricing earns far more per rack than the fleet average per MW implies. The bottom-up rack math (§2) — 72 GPUs × current Blackwell $/GPU-hr × 8,760 hr × ~85–90% utilization — lands at **~$8–14M per rack-year of gross billings.**
>
> **Both are correct; they measure different things.** Figure (1) is the *blended-fleet, mixed-generation, ramp-and-contract-discounted* realized rate. Figure (2) is the *frontier-generation, high-utilization, near-on-demand* rate. The calculator's $13M anchor is a figure-(2) number — a *brand-new frontier rack sold well*. That is a legitimate thing to model for a venture deploying brand-new racks, but **the calculator should know it is anchoring to the optimistic, frontier-rack, sold-well end — not to the ~$2M/rack blended-fleet reality that CoreWeave's average MW actually clears.** This is the single most important caveat in this document.

- **Crusoe / NextBigFuture owner-operator framing.** An independent, widely-cited 2026 analysis ([NextBigFuture, "Economics of a Megawatt of AI Data Center"](https://www.nextbigfuture.com/2026/05/economics-of-a-megawatt-of-ai-data-center.html), built on Crusoe CEO figures) puts the **pure infrastructure/IaaS lease layer at ~$15M per MW-year**, with a higher-value managed-services layer adding another **~$15M/MW-year** (total toward ~$30M/MW-year). At ~0.13–0.18 MW/rack that is **~$2.0–2.7M per rack-year (IaaS layer)** measured against *total MW* — again far below $13M *on a per-MW basis*, but consistent with the bottom-up rack figure once you price a *frontier rack at high utilization* rather than a blended MW. [ESTIMATE]
- **Oracle (OCI).** Oracle's AI-infrastructure cloud is explicitly a **30–40% gross-margin business** (management guidance, Q-FY2026), versus Oracle's ~68% blended/legacy software margin — confirming that the *owner-operator IaaS layer* is a moderate-margin business, not a software-margin business. OCI's RPO backlog is **~$553B** (Q3 FY2026, +325% YoY); cloud revenue ~$8.9B/qtr (+44% YoY). [FACT — Futurum; FinancialContent]

**Owner-operator synthesis: a frontier NVL72-class rack, owned outright and sold near current pricing at high utilization, earns ~$8–14M/rack-year of gross IaaS billings (2026), central ~$10–12M.** The $13M anchor is the top of that band. Measured instead as a *blended-fleet* realized rate (CoreWeave's actual ~$/MW × rack kW), it is far lower (~$2M/rack) — the difference is frontier-vs-mixed-generation and high-vs-blended utilization. **The calculator is anchoring to the frontier, sold-well case. That is defensible for a new-rack venture but should be stated as such.** [DERIVED, cross-checked]

### Layer 3 — what an integrated inference-service *earns*

If you run *your own model* and bill per token, revenue decouples from the hardware-rental rate and is set by the **value of the model output**. This is the highest-revenue layer — but the extra revenue is **model-value capture**, not compute capture, and it carries model-quality risk.

- Frontier API pricing, 2026: **GPT-5.5 ~$5 in / $30 out per 1M tokens; Claude Opus 4.7 $5 / $25; GPT-5.2 Pro $21 / $168.** [FACT — Finout; DevTk]
- Independent cost-to-serve analysis ([Martin Alderson, 2026](https://martinalderson.com/posts/are-openai-and-anthropic-really-losing-money-on-inference/)) estimates the *raw compute cost* of frontier output at **~$3/1M output tokens** (and ~$0.003/1M input) against API prices of $15–30, implying **~80–95% gross compute margins** on inference. Anthropic's disclosed inference margin reportedly **rose from ~38% to ~70% in a single year** as pricing caught up to cost.
- Translating to a rack: an NVL72 rack fully tasked serving competitive frontier tokens can gross **~1.5–2.5× the IaaS rate** of the same rack — i.e. **~$15–25M+/rack-year** — *if* the model is competitive and the rack is fully sold. This is the figure `revenue_per_watt.md` called the "~$16M inference-service rate."

**Layer 3 is not the calculator's anchor and should not be.** The calculator correctly uses the owner-operator IaaS rate (layer 2) and applies the orbital premium separately, explicitly *not* baking in an inference-service markup ("no premium-on-a-premium" — calculator README correction #3). This document confirms that is the right call: layer-3 economics require owning a competitive frontier model, which the orbital venture does not.

---

## 2. Bottom-up — the GPU-rental math behind the owner-operator rate

The owner-operator rate is, mechanically, GPU-hours sold × price. Here is the current (2026) build-up.

### Per-GPU-hour pricing, 2026 [FACT]

| GPU class | Neocloud on-demand | Hyperscaler on-demand | Reserved / multi-year | Source |
|---|---|---|---|---|
| **H100** (700 W) | ~$2.00–4.15/hr (avg ~$2.85–3.50; spot lower) | AWS ~$6.88; Azure list ~$12 | ~$1.65–2.35/hr (1-yr) | [IntuitionLabs](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison); [Silicon Data](https://www.silicondata.com/blog/h100-rental-price-over-time) |
| **B200** | avg ~$4.71/hr (range $2.25 reserved – $16) | ~$6–7/hr | ~$2.25/hr (36-mo) | [GetDeploying B200](https://getdeploying.com/gpus/nvidia-b200) |
| **GB200 (NVL72 superchip)** | on-demand avg ~$16–20/hr per GPU; **low ~$10.50/hr** | — | — | [GetDeploying GB200](https://getdeploying.com/gpus/nvidia-gb200) |
| **GB200 NVL72 rack (72 GPUs)** | **~$756–1,944/hr per rack** ($10.50–27/GPU-hr) | — | — | [Spheron](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/) |
| **GB300 (B300)** | from ~$2.45/hr (dedicated) per GPU; rack ~$6–6.5M to buy | — | — | [Spheron B300](https://www.spheron.network/gpu-rental/b300/) |

**The key 2026 pricing wrinkle: rates are rising at the frontier, falling for old silicon.** H100 fell ~64% peak-to-trough (2023 ~$8 → late-2025 ~$2) — the commoditization of aging silicon. But **GB200 on-demand pricing rose ~21% since mid-2025** (~$13.25 → ~$16/GPU-hr), and the **B200 rental index jumped ~24% in a single month** (March 2026), driven by Samsung/SK Hynix raising HBM3e contract prices ~20% and NVIDIA revising MSRPs upward. Frontier capacity is supply-constrained; old capacity is not. [FACT — [Silicon Data B200 update](https://www.silicondata.com/blog/b200-rental-price-march-2026-update); tech-insider]

### Translating to annual revenue per NVL72 rack [DERIVED]

A **GB200 NVL72 rack = 72 GPUs**:

- At **$756–1,944/hr** and **85–90% utilization**: 8,760 hr × 0.875 × ($756–1,944) = **~$5.8M–14.9M per rack-year of gross billings.**
- Central case — blended contract-leaning pricing (~$1,000–1,400/hr) at ~88% utilization: **~$7.7–10.8M per rack-year.**
- An NVL72 rack costs **~$3M (GB200) to ~$6–6.5M (GB300)** to buy. Morgan Stanley pegged GB200 NVL72 "AI-factory" rack-level profit margin at ~77.6% (before financing/depreciation timing) — i.e. gross billings can pay back hardware in well under a year at high utilization. [FACT — `revenue_per_watt.md`]

> **Note vs. `revenue_per_watt.md`.** That document's §2 gave the same ~$5.6–14.5M/rack-year on-demand band but its §6 illustrative model then quoted **~$8M/rack-year** as the "blended contract" central IaaS figure. **This document supersedes that with ~$10–12M central for a frontier owner-operator** — the upward revision reflects (a) the 2026 frontier-pricing rebound (GB200 +21%, B200 index +24%) that postdates the earlier doc's pricing, and (b) the explicit owner-operator framing (no reseller markup deducted). The ~$8M figure remains valid as a *blended-contract, conservative* read; ~$10–12M is the better central owner-operator number for 2026.

---

## 3. The trajectory — how the rate has moved and where it goes

The calculator grows the revenue anchor at **15%/yr**. Is that right? Map the history first, then project.

### 3.1 How per-rack revenue has actually moved (historical) [FACT / DERIVED]

Per `ai_compute_trajectory.md` §7, indexed and cross-checked here:

| Generation | Era | GPUs/rack | Blended $/GPU-hr | **Gross $/rack-year** | vs. prior |
|---|---|---|---|---|---|
| DGX H100 (8-GPU) | 2022–23 | 8 | ~$3–6 | ~$0.2–0.4M | — |
| H100, 72-GPU-equiv | 2023–24 | 72 | ~$3–6 | ~$1.6–3.2M | — |
| GB200 NVL72 | 2024–25 | 72 | ~$3.50–7 | **~$5.6–11.9M** (mid ~$8M) | ~2.5–3× |
| GB300 NVL72 | 2025–26 | 72 | ~$4–8 | **~$6–13M** (mid ~$9–10M) | ~1.1–1.3× |
| Rubin VR200 NVL72 | H2 2026 | 72 | ~$5–9 (proj.) | **~$7–15M** (mid ~$10–11M) | ~1.1–1.2× |

**Reading the history.** Per-NVL72-rack gross revenue rose from ~$1.6–3.2M (H100-equivalent rack, 2023–24) to ~$8M (GB200, 2024–25) to ~$9–10M (GB300, 2025–26) — roughly **~2.5–3× over ~2.5 years**, but the *step sizes are shrinking*: the H100→GB200 jump was large (~2.5–3×) because the NVL72 rack redefinition packed 72 GPUs into the unit; the GB200→GB300 step is only ~1.1–1.3×. The growth is real but **decelerating per generation**.

### 3.2 What drives the growth, and what caps it

- **Driver (real): rack hardware cost rises ~2×/generation.** GB200 ~$3M → GB300 ~$6–6.5M → Rubin VR200 ~$5–8.8M. Rental rates broadly track hardware cost — a pricier rack must rent for more to clear an acceptable return — and the 2026 HBM-driven price rebound (§2) is this mechanism in action. [FACT]
- **Cap (real): revenue tracks the rack's *price*, not its *FLOPS*.** This is the central finding of `ai_compute_trajectory.md` §7 and it holds: per-rack compute rose ~10×/3 generations while per-rack revenue rose only ~2–3×. The exploding FLOPS are *consumer surplus* — they make compute cheaper per token for the buyer, not the rack owner richer. So revenue grows with the **price curve (~2×/gen)**, not the **FLOPS curve (~10×/3-gen)**.
- **Cap (real): in-generation decay.** Within a generation, rates fall as silicon ages — H100 fell ~64% peak-to-trough. An owner-operator's rack earns front-loaded revenue that decays over its service life (the calculator's `in_life_revenue_decay`, 12%/yr, captures this).

### 3.3 Converting "~2×/generation rack price" into an annual growth rate

A generation is ~12–18 months. If per-rack *gross revenue* rises ~2–3× over **3 generations** (~3–4 years) — the observed H100→Rubin span — that is a CAGR of:

- 2.5× over 3.5 years ⇒ **~29%/yr**? No — that overstates, because the H100→GB200 step was a one-time unit redefinition (8-GPU node → 72-GPU rack). **Strip the redefinition** and compare like-for-like 72-GPU racks: GB200 (~$8M) → GB300 (~$9–10M) → Rubin (~$10–11M) is ~$8M → ~$10.5M over ~2 years ⇒ **~15%/yr at the high end, ~10–12%/yr central.**
- Over a longer horizon the rate decelerates further: `ai_compute_trajectory.md` §5 is explicit that growth *rates* decelerate as the easy gains exhaust, and the rack-cost step itself softens (GB200→GB300 was ~2×, GB200→Rubin only ~1.2–2.3×).

> **Trajectory verdict.** Per-rack revenue *is* a growing number — confirmed, not assumed. But **~15%/yr is the high end, supported only by the most recent (frontier-pricing-rebound) data and the steepest rack-cost steps.** A like-for-like NVL72 comparison and the documented per-generation deceleration both point to **~10–12%/yr as the better-supported central trajectory.** The calculator's 15% is not crazy — early-cycle, frontier-rack, supply-constrained — but it should be treated as an *aggressive* dial setting, with ~11% as the central case and 15% as the optimistic scenario. Over a 10-year horizon the difference compounds heavily: $13M growing at 15% reaches ~$53M by 2036; at 11% it reaches ~$37M — a ~30% gap in the terminal-year revenue.

### 3.4 Projected per-rack owner-operator revenue [PROJECTION — directional]

| Year | Generation (flagship) | Owner-operator $/rack-year, central | Tag |
|---|---|---|---|
| 2026 | GB300 / early Rubin | **~$10–13M** | [FACT/DERIVED] |
| 2028 | Rubin Ultra-class | ~$14–19M | [PROJECTION] |
| 2030 | post-Rubin | ~$18–26M | [PROJECTION] |
| 2033 | — | ~$26–40M | [PROJECTION] |
| 2036 | — | ~$35–55M | [PROJECTION] |

Growth ~10–12%/yr central; the band widens with horizon (±40% by 2036). Note this is the *flagship-rack* figure — a power-capped orbital node flying a throttled rack earns proportionally less, as the calculator's v3 flyability layer already models.

---

## 4. The total-cost-of-ownership reframe — what an "orbital premium" is a premium *over*

**The project must not frame orbital revenue as a rack-rental sticker price competing with a terrestrial rack-rental sticker price.** The customer's real decision is: *what does it cost me to own and run this compute for its whole life?* That total includes hardware **plus** real estate **plus** the recurring **energy** bill **plus** cooling/water. An orbital operator's structural pitch is that it **converts the recurring energy cost into one-time solar capex** and **eliminates the real-estate and water lines entirely**. So the orbital premium is a premium over the *terrestrial total* — and to size it you must quantify the non-hardware terrestrial costs.

### 4.1 The terrestrial TCO of 1 GW of AI compute [FACT — Epoch AI]

[Epoch AI's 1 GW AI data center model](https://epoch.ai/data-insights/ai-datacenter-cost-breakdown) is the cleanest current breakdown:

| Line item | Annualized cost | Share of TCO |
|---|---|---|
| **Servers & network (GPUs)** | ~$5.0B/yr | **~59%** |
| Facility construction (real estate + shell) | ~$2.5B/yr | ~29% |
| **Energy / electricity** | **~$0.6B/yr** | **~7%** |
| Maintenance, labor, land, taxes, water | ~$0.3B/yr | ~4% |
| **Total cost of ownership** | **~$8.5B/yr** | 100% |

- Upfront capex **~$38B/GW**; annual opex **~$0.9B/GW**. Assumes 5-yr IT life, 14-yr facility life, PUE 1.14, 71% utilization.
- **Sensitivity:** shortening IT life to 3 yr raises TCO to ~$12B/yr; extending to 7 yr lowers it to ~$7B/yr — depreciation is the dominant swing factor, consistent with `hyperscaler_margins.md`.

### 4.2 The key reframe — energy is small in TCO but large in *opex*, and rising fast

Two facts that look contradictory but both matter:

1. **Energy is only ~7% of fully-annualized TCO.** When you annualize the ~$5B/yr of GPU capex, the ~$0.6B/yr energy bill is a single-digit share. This is why `energy_operating_costs.md` correctly concluded energy is **not** the dominant lifetime cost — and why "free electricity in orbit" is a *second-order* launch justifier. That conclusion stands.
2. **But energy is ~65–70% of *cash operating cost*** ($0.6B of ~$0.9B/yr opex) — and it is the line that is **rising fastest**. PJM wholesale power costs jumped **+75.5% YoY into Q1 2026**; PJM's 2025–26 capacity auction cleared at a record ~$329/MW-day (~+22%); data-center-heavy regions saw retail prices **+267% over five years** (Bloomberg). US investor-owned utilities have announced **~$1.4T of capex through 2030** driven by data-center demand. Residential rates +~40% cumulative since 2021. [FACT — E&E News; IEEFA; tech-insider]

> Large *contracted* hyperscale buyers are partially insulated by long-term PPAs (`energy_operating_costs.md` §2) — the worst spikes hit residential and uncontracted wholesale. But the contracted-buyer rate is rising too, just more slowly. And **the binding terrestrial constraint is increasingly not the *price* of power but *getting* power at all** — interconnection queues run ~5 years median (up to ~12 for data centers); transformer lead times ~5 years. That is a *schedule* problem, and it is the genuine power-related orbital advantage (`energy_operating_costs.md` §6).

### 4.3 Quantifying the per-rack non-hardware terrestrial cost — what the premium is *over*

Per NVL72-class rack (~135 kW IT, PUE ~1.25, ~85% utilization, 5-year life), the terrestrial costs an orbital operator avoids or converts:

| Cost line | Per NVL72 rack, 5-year | Basis | Orbital treatment |
|---|---|---|---|
| **Energy (electricity)** | **~$0.5–1.2M** (mid ~$0.6M at $0.085/kWh; high ~$1.2M at $0.13/kWh) | `energy_operating_costs.md` §3 — 6.5 GWh delivered × rate | Converted to one-time solar capex |
| **Energy, escalated** | **~$0.8–2M** if rates rise ~40% by 2030 and the *rack draws more power each generation* (a 600 kW Rubin-Ultra-class node terrestrially could spend ~$3–6M+ over 5 yr) | `ai_compute_trajectory.md` §9 | Converted to one-time solar capex |
| **Real estate / facility shell** | **~$1.5–3.5M** (allocated; Epoch's ~29% facility share ≈ ~$2.5B/GW-yr ⇒ ~$2–3M per ~0.16 MW rack over 5 yr) | Epoch AI §4.1 | Eliminated — no building |
| **Cooling / water capex + water opex** | **~$0.6–1.0M** (liquid-cooled AI hall cooling infra ~$3–5M/MW; water opex ~$10–100k/rack) | `energy_operating_costs.md` §4; Introl/Build.inc cooling-cost data | Replaced by radiative cooling (one-time radiator capex) |
| **Total non-GPU terrestrial cost avoided/converted, per NVL72 rack, 5-yr** | **~$2.6–7.5M; central ~$4M today, rising** | sum of above | — |

**The reframe, stated plainly.** A terrestrial customer pays, over a 5-year rack life, **~$2.6–7.5M (central ~$4M) per NVL72 rack on energy + real estate + cooling/water — on top of the rack hardware itself.** That figure is **rising** — energy rates are climbing and rack power is exploding (~130 kW → ~600 kW over the horizon), so the avoided/converted terrestrial cost per node grows several-fold. **An orbital operator's "premium" is, in part, a recovery of this avoided cost** — the customer should be willing to pay more for orbital capacity precisely because they are *not* separately paying the terrestrial energy/real-estate/cooling bill.

**But keep the magnitude honest.** Against a rack hardware cost of ~$3–6M and (for the orbital venture) a launch + spacecraft cost of ~$30–45M per node, the ~$4M of avoided 5-year terrestrial energy/RE/cooling is **real but second-order** — it is a supporting argument for the premium, not the whole premium. This is exactly the conclusion `energy_operating_costs.md` reached and it is unchanged: orbit does not *win* on energy economics; it converts a recurring, rising opex into a one-time capex, which is a genuine but modest structural edge, strongest as a *schedule/permitting* advantage rather than a dollar saving. **What this section adds** is the framing: the orbital premium is a premium over the terrestrial *total* (hardware + energy + RE + cooling), not over a hardware-rental sticker — and that total is ~$4M/rack-larger than the sticker, and growing.

---

## 5. Verdict — is the calculator's $13M anchor and 15% growth defensible?

The current Python generator under `code/` uses:
- `owner_operator_anchor_musd: 13.0` — owner-operator raw-rack revenue, 2026, $M/rack-year
- `revenue_anchor_growth: 0.15` — 15%/yr growth
- a separate `orbital_premium_headline: 0.50` on top

### On the $13M (2026) anchor — **defensible, but it is the high end of the band, not the midpoint**

| Reference point | Per NVL72-class rack-year (2026) | Read |
|---|---|---|
| Renter/reseller *cleared* | ~$1–2M net | far below — wrong layer |
| CoreWeave blended-fleet realized ($/MW × rack kW) | ~$0.8–2.0M | far below — mixed-generation, ramp-discounted |
| Bottom-up GB200 NVL72, blended-contract pricing | ~$7.7–10.8M | the conservative-central owner-operator read |
| Bottom-up GB200/GB300 NVL72, frontier pricing, ~88% util | ~$10–14M | **the band the $13M anchor sits in** |
| Crusoe/NextBigFuture IaaS layer (~$15M/MW × rack MW) | ~$2.0–2.7M per total-MW basis; consistent with ~$10M+ on a frontier-rack basis | supports the frontier-rack read |
| `revenue_per_watt.md` prior central IaaS figure | ~$8M | superseded — see §2 note |
| `ai_compute_trajectory.md` owner-operator suggested range | ~$11–16M | $13M is mid-this-range |

**$13M is defensible** as a 2026 *frontier-generation* (GB300-class) rack, owned outright, sold near current pricing at high utilization. It sits in the upper half of a credibly-sourced ~$8–14M band. It is **not conservative** and it is **not a midpoint** — a more central owner-operator figure is **~$10–12M**. The $13M anchor implicitly assumes the venture always fields and sells *frontier* racks *well*; it does **not** reflect the ~$2M/rack that CoreWeave's *blended, mixed-generation* fleet actually clears per unit of MW capacity.

**Recommendation:** keep $13M available but **treat it as the optimistic end of a $10–13M band; consider $11–12M as the central-case dial setting.** If the calculator's default is meant to be a central case, $13M is ~10–20% hot.

### On the 15%/yr growth — **too high; ~10–12% is better supported**

Per-rack revenue *is* a growing number — this is confirmed by the rack-cost-rises-~2×/generation mechanism and the 2026 frontier-pricing rebound (§3). But:
- A **like-for-like NVL72 comparison** (GB200 ~$8M → GB300 ~$9–10M → Rubin ~$10–11M) implies **~10–12%/yr**, not 15%.
- The per-generation step is **decelerating** (GB200→GB300 only ~1.1–1.3×), and `ai_compute_trajectory.md` §5 explicitly expects growth *rates* to decelerate over the horizon.
- 15% is supported only by the steepest, most recent, supply-constrained data — it is an early-cycle rate, unlikely to hold for a decade.

**Recommendation:** **cut `revenue_anchor_growth` from 0.15 to ~0.10–0.12.** This still keeps revenue growth *below* rack-cost growth (`rack_cost_growth: 0.37`), preserving the trajectory's central headwind (revenue grows slower than the rack gets expensive — `ai_compute_trajectory.md` §11 H2). The direction is right; the magnitude is hot. The compounding matters: over 10 years, 15% vs 11% is a ~30% difference in terminal-year per-rack revenue.

### On the framing — **the TCO reframe strengthens the premium's logic but does not change its magnitude**

The orbital premium (`orbital_premium_headline: 0.50`) should be understood as a premium over the customer's *total* terrestrial cost of compute — hardware + energy + real estate + cooling/water — not over a rack-rental sticker. §4 quantifies the non-hardware piece at **~$4M per NVL72 rack over 5 years (central, 2026), rising**. That is a real, sourced component of why a customer would pay more for orbital capacity. But it is second-order against the rack hardware and the launch cost, so it **supports** the premium thesis without **sizing** it — the premium remains the load-bearing, largely-unobserved dial, exactly as `premium_value_case.md` and `ai_compute_trajectory.md` §11 conclude.

### Bottom line

> **The calculator's $13M (2026) owner-operator anchor is defensible but optimistic — it is the high end of a $10–13M band; ~$11–12M is the better central case. The 15%/yr growth is too high — ~10–12%/yr is the better-supported trajectory. Both corrections are modest and in the same direction (the calculator is ~10–30% hot on per-rack revenue over the horizon). The qualitative structure — revenue grows, but slower than rack cost, with a separate premium on top — is correct and well-supported. The orbital premium should be framed as a premium over the terrestrial *total cost of ownership* (hardware + energy + real estate + cooling), which runs ~$4M/rack of non-hardware cost above the rack sticker and is rising — a genuine supporting argument, but not large enough to carry the premium on its own.**

---

## Where this document supersedes earlier figures

| Earlier figure | Source doc | This doc's update |
|---|---|---|
| "~$8M/rack-year" central blended-contract IaaS rate | `revenue_per_watt.md` §6 | Superseded for the *owner-operator frontier* case → **~$10–12M central** (2026 frontier-pricing rebound + no reseller markup). ~$8M remains valid as a conservative blended-contract read. |
| "~$11–16M/rack-year for owner-operator" suggested range | `ai_compute_trajectory.md` §7.3, Open Q1 | Tightened → **~$10–13M defensible band, ~$11–12M central**; $13M is the high end. |
| Per-rack revenue growth "~1.5–2×/generation" / calculator's 15%/yr | `ai_compute_trajectory.md` §7; calculator `revenue_anchor_growth` | Refined → **~10–12%/yr** on a like-for-like NVL72 basis; 15% is the aggressive end. |
| Energy as a launch justifier | `energy_operating_costs.md` | **Unchanged and reaffirmed** — energy is ~7% of TCO, second-order. This doc adds the TCO *framing* (premium is over hardware+energy+RE+cooling) without changing the energy conclusion. |
| TAM doc's ~$3B/GW-yr proxy | `ai_datacenter_tam.md` §5 | Already retired by wave-4 synthesis; this doc does not use it. Per-GW gross IaaS is ~$10–11B/GW-yr (CoreWeave mature exit-rate), consistent with `revenue_per_watt.md`'s ~$15–20B/GW central once frontier pricing is applied. |

---

## Sources

**CoreWeave (FY2025 actuals, FY2026 guidance)**
- [CoreWeave Reports Strong Q4 and FY2025 Results — investor relations](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Fourth-Quarter-and-Fiscal-Year-2025-Results/)
- [CoreWeave tops $5B revenue for 2025, projects hypergrowth 2026–2027 — Constellation Research](https://www.constellationr.com/insights/news/coreweave-tops-5-billion-revenue-2025-projects-more-hypergrowth-2026-2027)
- [CoreWeave Q4 earnings, revenue guidance — CNBC](https://www.cnbc.com/2026/02/26/coreweave-crwv-q4-earnings-report-2025.html)
- [CoreWeave $88B+ backlog, revenue-per-MW context — Motley Fool](https://www.fool.com/investing/2026/04/15/coreweave-has-a-massive-88-billion-revenue-backlog/)
- [CoreWeave aims to add 5 GW by 2030; 1.7 GW exit-2026 — DCD](https://www.datacenterdynamics.com/en/news/coreweave-aims-to-add-5gw-more-data-center-capacity-by-2030-anticipates-capex-in-2026-to-double/)

**Oracle / OCI**
- [Oracle Q3 FY2026 earnings — OCI AI infrastructure demand — Futurum](https://futurumgroup.com/insights/oracle-q3-fy-2026-earnings-driven-by-oci-ai-infrastructure-demand/)
- [Oracle $553B RPO backlog, 30–40% AI-infra gross margin guidance — FinancialContent](https://markets.financialcontent.com/stocks/article/marketminute-2026-3-11-oracle-orcl-surges-8-as-ai-infrastructure-demand-drives-record-550-billion-backlog)

**Nebius**
- [Nebius Q1 2026 financial results / Pennsylvania 1.2 GW AI factory](https://nebius.com/newsroom/nebius-reports-first-quarter-2026-financial-results)
- [Nebius 2026 guidance — $3–3.4B revenue, $7–9B ARR, 3 GW+ contracted — Motley Fool](https://www.fool.com/investing/2026/05/07/why-nebius-group-stock-popped-33-in-april-and-why/)

**GPU rental pricing (2026)**
- [H100 rental prices across 15+ providers, 2026 — IntuitionLabs](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)
- [H100 rental price over time (2023–2025) — Silicon Data](https://www.silicondata.com/blog/h100-rental-price-over-time)
- [B200 cloud pricing, 22+ providers — GetDeploying](https://getdeploying.com/gpus/nvidia-b200)
- [B200 index +24% in March 2026 on HBM price hike — Silicon Data](https://www.silicondata.com/blog/b200-rental-price-march-2026-update)
- [GB200 cloud pricing, 9+ providers (on-demand avg ~$16–20/GPU-hr) — GetDeploying](https://getdeploying.com/gpus/nvidia-gb200)
- [GB200 NVL72 guide — rack ~$756–1,944/hr — Spheron](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)
- [B300 / GB300 rental and rack pricing — Spheron](https://www.spheron.network/gpu-rental/b300/)
- [NVIDIA Blackwell GPU pricing — B200/B300/GB300 — tech-insider](https://tech-insider.org/nvidia-blackwell-gpu-pricing/)

**Total cost of ownership / data center economics**
- [Total cost of ownership of a 1 GW AI data center — Epoch AI](https://epoch.ai/data-insights/ai-datacenter-cost-breakdown)
- [Economics of a Megawatt of AI Data Center (~$15M/MW IaaS) — NextBigFuture](https://www.nextbigfuture.com/2026/05/economics-of-a-megawatt-of-ai-data-center.html)
- [GB200 NVL72 TCO ~1.6× H100, ~$3.1–3.9M all-in per rack — SemiAnalysis (via search)](https://newsletter.semianalysis.com/p/h100-vs-gb200-nvl72-training-benchmarks)
- [AI data center cooling cost share (15–20% of facility; liquid ~$3–5M/MW) — Build.inc](https://build.inc/insights/data-center-cooling-technology-2026)

**Inference / token economics**
- [Are OpenAI and Anthropic really losing money on inference? (~80–95% gross margin estimate) — Martin Alderson](https://martinalderson.com/posts/are-openai-and-anthropic-really-losing-money-on-inference/)
- [OpenAI vs Anthropic API pricing comparison 2026 — Finout](https://www.finout.io/blog/openai-vs-anthropic-api-pricing-comparison)

**Energy cost trajectory**
- [Data centers drive 76% surge in PJM power prices — E&E News](https://www.eenews.net/articles/data-centers-drive-76-surge-in-pjm-power-prices/)
- [PJM capacity prices spike on data-center growth — IEEFA](https://ieefa.org/resources/projected-data-center-growth-spurs-pjm-capacity-prices-factor-10)
- [US utilities plan $1.4T capex through 2030 for AI data centers — tech-insider](https://tech-insider.org/us-utility-1-4-trillion-ai-data-center-energy-2026/)
- [Who is footing the AI energy bill — CNBC](https://www.cnbc.com/2026/03/13/ai-data-centers-electricity-prices-backlash-ratepayer-protection.html)

---

## Open Questions

1. **The MW-to-rack translation gap.** The single largest uncertainty: CoreWeave's blended fleet clears ~$2M per NVL72-rack-equivalent of MW capacity, while a bottom-up frontier-rack calculation lands at ~$10–14M. Both are defensible (mixed-generation/ramp-discounted vs. frontier/high-utilization). The calculator anchors to the frontier read. A cleaner resolution would model the *fleet-average degradation* an orbital venture suffers as its racks age and trail the frontier — the orbital node cannot refresh silicon, so it may drift toward the lower (blended) figure faster than a terrestrial operator that continuously adds new racks. This belongs in the calculator as an explicit derate.
2. **Owner-operator vs. the calculator's premium — possible double-count.** If $13M is already a *frontier, sold-well* owner-operator rate, and a +50% orbital premium is applied on top, the combined figure (~$19.5M/rack-year) approaches the *inference-service* (layer 3) rate. The project should check that the premium is not implicitly re-capturing the layer-3 markup the calculator explicitly excluded.
3. **Contracted vs. merchant mix.** Take-or-pay backlog (CoreWeave $99.4B, Oracle $553B RPO) smooths revenue but at discounted rates; merchant/on-demand earns more per hour with utilization risk. The realized owner-operator rate depends on this mix — and an orbital operator that cannot re-task idle capacity may be forced toward lower-rate take-or-pay contracts.
4. **How fast does the frontier-pricing rebound fade?** The 2026 GB200/B200 price increases are HBM-supply-driven. If HBM supply normalizes, frontier rates could resume falling — which would pull the central trajectory below even 10%/yr. Worth a scenario.
5. **Orbital energy-conversion value over a longer horizon.** §4 sizes the avoided terrestrial energy/RE/cooling at ~$4M/rack today. As rack power climbs to ~600 kW+ and energy rates rise, this could reach ~$10M+/rack over a 5-year life by ~2030 — still second-order against launch, but a growing tailwind worth tracking explicitly rather than treating as static.
6. **Real-estate cost allocation.** The ~$2–3M/rack facility-shell figure is allocated from Epoch's ~29% facility share of a 1 GW TCO. AI-tier liquid-cooled builds run $20M+/MW of fit-out — the per-rack real-estate avoided cost could be materially higher for the most advanced terrestrial builds, strengthening the TCO reframe.
