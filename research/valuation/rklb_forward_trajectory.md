# Rocket Lab — Forward Trajectory & Launch-Services Economics

*Research/analysis date: 17 May 2026. Prepared for the Rocket Lab orbital
AI-inference data center feasibility project, as an input to the
company-valuation model. The companion to `economics/ambition_case.md` — this
document supplies the **external, sourced view of Rocket Lab the company**:
analyst consensus, company guidance, Neutron unit economics, the cadence ramp,
and the size of the launch market Neutron can actually sell into.*

> **What this document is.** A meticulously sourced snapshot of Rocket Lab's
> *forward* trajectory as of mid-May 2026 — after the Q1 2026 earnings release
> (8 May 2026) and the FY2025 results (26 Feb 2026). Every hard number is cited
> inline. Where the project's current modelling assumptions diverge from what is
> publicly supportable, this document **confirms or corrects** them explicitly.
> Headline figures are multi-sourced; anything unconfirmable is flagged.

> **Source status (2026-05-25):** See [SOURCE_INDEX.md](../SOURCE_INDEX.md) claim IDs NTR-001 through NTR-011 and REV-001 through REV-004. Neutron customer price, internal launch cost, SSO payload, and high-cadence assumptions have different evidence grades: price is a company/press target range, internal cost is cadence-specific estimate, SSO payload is not published, and ~100 launches/year is a venture scenario rather than Rocket Lab guidance.

---

## Summary (read this first)

**Forward revenue.** Rocket Lab closed **FY2025 at $602M revenue (+38% YoY)**
with a **$1.85B backlog**; Q1 2026 then printed a **record $200.3M (+63.5% YoY)**
and backlog jumped to **$2.2B**. Analyst consensus (22 analysts) puts **FY2026 at
~$883M** (range $778M–$1.1B) and **FY2027 at ~$1.3B** (range $951M–$1.7B). The
company does not give annual revenue guidance — only quarterly: **Q2 2026 guided
to $225–240M**. Longer-horizon analyst/narrative figures cluster around **~$1.5B
by 2029 and ~$2.5B by 2030**, but those are model outputs, not company targets.

**Neutron price/cost/cadence.** Neutron's quoted customer price is **~$50–55M**
(Rocket Lab's own "~$50M" target; press routinely cites "$50M" and "$55M"). The
project's **~$55M assumption is at the top of the supportable range — recommend
$50–55M, central $50M.** Rocket Lab targets **50% launch-segment gross margin,
reached at ~24 launches/year** — implying a long-run internal cost near
**~$25M/launch at scale**, *above* the project's ~$15–20M figure. Payload: **13t
to LEO** (downrange landing), 15t expended, 8.5t return-to-launch-site; **no
official SSO number is published — a gap.** The cadence ramp has **slipped**: the
"one-three-five" plan, with first flight now NET Q4 2026, implies roughly **1
launch 2027, 3 in 2028, 5 in 2029**, then a build toward "monthly." **The
project's "3 in 2027 / 5 in 2028 / ~12/yr thereafter" is now one year
optimistic — correct it.**

**Contestable market.** 2025 saw a record **~315–329 orbital launch attempts**
(254 in 2024). But **SpaceX (165) + China (90) = ~255 of them**, almost all
captive. The genuinely *contestable, non-captive, medium-lift-class* market is
realistically only **~30–50 launches/year today**. **Selling ~100 Neutrons/year
to external customers is not supported by the current addressable market** — it
would require either capturing nearly all contestable demand *and* a large new
demand source (e.g. the data-center venture itself as anchor), or displacing
SpaceX at scale.

**Confidence: moderate-to-high** on revenue/guidance/backlog (primary filings);
**moderate** on Neutron cost/cadence (company targets, not results); **moderate**
on market size (good launch counts; "contestable" is an analytic judgement).

---

## 1. Revenue trajectory — actuals, consensus, guidance

### 1.1 The actuals base

| Period | Revenue | Growth | Note | Source |
|---|---|---|---|---|
| FY2023 | ~$245M | — | | `[CITED — derived from FY2024 +38% base]` |
| FY2024 | ~$436M | — | | `[CITED — implied by FY2025 release]` |
| **FY2025** | **$602M** | **+38% YoY** | Non-GAAP gross margin 44.3% (vs 34% FY24); 21 Electron/HASTE launches, 100% success | Globe Newswire / Rocket Lab IR FY2025 release, 26 Feb 2026 |
| Q4 2025 | ~$180M | record quarter | Backlog $1.85B (+73% YoY) | Rocket Lab IR; StockTitan |
| **Q1 2026** | **$200.3M** | **+63.5% YoY** | First $200M+ quarter; beat own $185–200M guide. Split: Space Systems $136.7M, Launch $63.7M. Backlog $2.2B | CNBC; Investing.com; Motley Fool transcript, 8 May 2026 |

The FY2025 backlog of $1.85B includes an **$816M SDA Tracking Layer Tranche 3
contract** (18 satellites) — a large, multi-year, lower-margin Space Systems
award that anchors near-term revenue visibility.

### 1.2 Analyst consensus — next 1–3 fiscal years

From stockanalysis.com's compiled sell-side consensus (accessed 17 May 2026):

| Fiscal year | Analysts | Consensus (avg) | Low | High | Implied growth |
|---|---|---|---|---|---|
| **FY2026** | 22 | **~$883M** | $778M | $1.1B | ~+47% (range +29% to +79%) |
| **FY2027** | 21 | **~$1.3B** | $951M | $1.7B | ~+43% (range +8% to +91%) |
| FY2028 | n/a | not free-tier; "lowest-ranked analysts ~$1.3B" cited as a floor | — | — | — |

`[CITED — stockanalysis.com/stocks/rklb/forecast; Simply Wall St]`

EPS consensus: **FY2026 ≈ −$0.25** (range −$0.34 to −$0.05); **FY2027 ≈ +$0.03**
(range −$0.06 to +$0.15) — i.e. the Street models Rocket Lab crossing into GAAP
profitability around **2027**. Simply Wall St's compilation has the company at a
**modelled ~$176M net profit in 2028** and a **>29% revenue CAGR for 2027–2034**.
`[CITED — Simply Wall St; Zacks via search]`

> **Consensus verdict.** Next-1–3-year forward revenue: **FY2026 ~$0.78–1.1B
> (central ~$0.88B), FY2027 ~$0.95–1.7B (central ~$1.3B)**. The wide FY2027 band
> is almost entirely a **Neutron-timing bet** — analysts modelling an on-time,
> revenue-generating Q4 2026 first flight sit high; those modelling further
> slippage sit low.

### 1.3 Longer-horizon figures

There is **no official long-range company revenue target**. Third-party
narrative/model figures in circulation: **~$1.5B by 2029** and **~$2.5B by 2030**
`[CITED — search aggregation of Simply Wall St / analyst narratives]`. Treat
these as **analyst model outputs, not guidance** — flag as soft.

### 1.4 Rocket Lab's own forward guidance

Rocket Lab guides **quarterly only — it does not issue annual revenue guidance.**
From the Q1 2026 release and earnings call (8 May 2026):

| Metric | Q2 2026 guidance | Source |
|---|---|---|
| Revenue | **$225M–$240M** (≈+16% sequential at midpoint; vs $207.5M LSEG consensus) | Motley Fool transcript; CNBC |
| GAAP gross margin | 33%–35% | Motley Fool transcript |
| Non-GAAP gross margin | 38%–40% | Motley Fool transcript |
| GAAP opex | $138M–$144M | Motley Fool transcript |
| Adjusted EBITDA | loss of $20M–$26M | Motley Fool transcript |

**Stated long-term financial targets** (management, repeated across calls):
- **Corporate gross margin "around 50% or greater"** at maturity.
- **Operating margin "mid- to upper-twenties"** at maturity.
- CFO has reaffirmed the **~50% corporate gross-margin** trajectory as Neutron
  scales and Space Systems subsystems mature.

`[CITED — Motley Fool Q1 2026 transcript; ainvest / BigGo earnings coverage]`

> **Guidance verdict.** The company's only *hard* forward numbers are the Q2
> revenue range and the maturity margin targets (~50% gross, mid–upper-20s
> operating). All annual revenue figures used in the valuation model are
> **analyst consensus, not company guidance** — label them accordingly.

---

## 2. Neutron rocket economics

### 2.1 Customer price per launch

| Figure | Basis | Source |
|---|---|---|
| **~$50M** | Rocket Lab's own stated target price; "$50M launch price tag... expects 50% margins" | Search aggregation; illdefined.space; NextBigFuture |
| **~$55M** | Routinely quoted in press as the per-launch step-up "from $8.5M Electron to $55M Neutron" | Multiple press / search |
| Q1 2026 bookings | "very much in family with commercial rates"; management expects **upward price discovery** over time (as Electron drifted from $5–6M to $8.5M) | Motley Fool Q1 2026 transcript |

Rocket Lab has **not published a definitive list price**. The honest read: the
**target/quoted price is ~$50M**, press shorthand rounds to "$50–55M," and
management explicitly expects the *realised* price to **drift upward** with
demand — so $55M is a defensible *near-future* figure but $50M is the better
*current* anchor.

> **Price verdict — CORRECTION.** The project's **~$55M** is at the **top** of
> the supportable range. Recommend modelling **$50–55M, central $50M**, with a
> note that management guides toward upward price discovery (so $55M is a
> reasonable out-year figure). For comparison Neutron is positioned *below*
> Falcon 9's ~$70M list price.

### 2.2 Cost and gross-margin targets

Rocket Lab's public statements are about **margin**, not a dollar cost:

- **Launch-segment gross-margin target: 50%**, explicitly stated to be reached
  **once Neutron reaches ~24 launches/year.** `[CITED — search aggregation of
  earnings coverage]`
- At a ~$50M price and 50% gross margin, the **implied internal cost at the
  24/yr cadence is ~$25M/launch.** `[DERIVED]`
- CEO Peter Beck, on the *development* (not marginal) cost: the Neutron program's
  **labour cost is "about $15M a quarter, which we make back 4× over a single
  launch."** `[CITED — Motley Fool / Nasdaq, Nov 2025]` This is a *program
  burn-rate* statement, **not** a per-launch marginal cost — do not conflate.

> **Cost verdict — CORRECTION / FLAG.** There is **no public figure for
> Rocket Lab's marginal/internal cost per Neutron launch.** The only anchored
> public datapoint is the **50%-margin-at-24-launches/yr** target, which
> *implies* **~$25M/launch internal cost at that cadence** — i.e. **higher than
> the project's ~$15–20M estimate.** The project's $15–20M is plausible only as
> a *high-cadence, fully-reused, learning-curve-matured* figure (the
> `ambition_case.md` $20M→$10M curve) — it is **not supported as a near-term or
> 24/yr-cadence number.** Recommend: near-term internal cost ~$25M; the
> ~$15–20M figure should be explicitly labelled a high-cadence projection, not
> a current cost.

### 2.3 Payload capacity

| Mode | Payload to LEO | Source |
|---|---|---|
| Expended | **15,000 kg (33,100 lb)** | Wikipedia / Rocket Lab spec |
| Downrange booster landing (the baseline reusable mode) | **13,000 kg (28,700 lb)** | Wikipedia / Rocket Lab spec |
| Return-to-launch-site landing | **8,500 kg (18,700 lb)** | Wikipedia / Rocket Lab spec |
| **SSO** | **No official figure published** | — |

> **Payload verdict — FLAG.** LEO numbers are firm and multi-sourced. **Rocket
> Lab has not published a Neutron SSO payload figure.** As an order-of-magnitude
> roughing factor, medium-lift vehicles typically lose ~20–30% capacity going from
> LEO to SSO; that would put Neutron's SSO payload at very roughly **~9–10t
> (downrange-landing mode)** — but this is an **estimate, not a sourced figure**,
> and should be flagged as such or confirmed directly with Rocket Lab. For the
> data-center use case (single-rack node ~well under 1–2t), Neutron is
> mass-abundant in every mode.

### 2.4 Vehicle & manufacturing context

- First stage: **9 Archimedes** oxygen-rich staged-combustion methalox engines;
  second stage: **1 vacuum-optimised Archimedes** — **10 engines/vehicle**.
- First stage designed for **reuse** (downrange ocean-platform recovery);
  `ambition_case.md` cites ~15-flight amortisation.
- Manufacturing: **250,000 sq ft facility at Wallops Flight Facility, Virginia**;
  launches from **LC-3, Wallops** (pad reported "open for launch," 2025/26).
- First-customer bookings (see §4) confirm commercial demand ahead of debut.

---

## 3. Neutron launch-cadence ramp

### 3.1 The published ramp — and its slippage

Rocket Lab's stated cadence philosophy is the **"one-three-five"** ramp — the
same measured rollout it used for Electron — followed by a build toward
**"monthly" (~12/yr)**:

| Year | Original plan (when 1st flight was ~2025) | **Current plan (1st flight NET Q4 2026)** |
|---|---|---|
| First flight | 2025 | **NET Q4 2026** (test flight; soft ocean splashdown) |
| Year 1 of ops | 1 | **2027: ~1** (potentially up to 3 payload launches "dependent on Flight 1 timing") |
| Year 2 | 3 | **2028: ~3** |
| Year 3 | 5 | **2029: ~5** |
| Thereafter | "monthly" / ~12/yr | "monthly" / ~12/yr — timing pushed out ~1 year |

`[CITED — Wikipedia (Neutron); Motley Fool Q1 2026 transcript; Space.com /
NASASpaceFlight Neutron-delay coverage; search aggregation]`

The Q1 2026 call kept first flight at **"later this year"** (Q4 2026) and
declined to narrow it further ("not enough visibility to nail it down to a
couple of weeks"). Management noted **2027 could see up to three payload-carrying
launches if Flight 1 goes well** — so 2027 is best modelled as a **1–3 launch
range**, central ~1–2.

> **Cadence verdict — CORRECTION.** The project currently uses *"first flight
> NET Q4 2026, ~3 launches in 2027, ~5 in 2028, ~monthly thereafter."* The
> **2027/2028 figures are now ~1 year optimistic.** With first flight in Q4
> 2026, the supportable ramp is **2027: ~1–3 (central ~2), 2028: ~3–5, 2029:
> ~5, then a build toward ~12/yr ("monthly")**. The "~monthly thereafter"
> end-state is correct as Rocket Lab's *stated medium-term* ambition. **Net
> effect: shift the project's cadence ramp one year to the right.**

### 3.2 Implication for the data-center venture

The 50%-launch-margin target is explicitly pegged to **24 launches/year** — i.e.
*twice* the "monthly" end-state and a figure Rocket Lab has **not** put a date
on. The `ambition_case.md` requirement of **~85–110 launches/year** is **~7–9×
Rocket Lab's stated "monthly" ambition and ~4× the 24/yr margin-target cadence**
— consistent with that document's own "hard, near the edge of credible" framing.
Nothing in Rocket Lab's public roadmap targets a rate above ~24/yr.

---

## 4. Neutron commercial demand (early evidence)

| Date | Deal | Source |
|---|---|---|
| Nov 2024 | First Neutron customer: confidential constellation operator, **2 dedicated launches** from mid-2026 | Rocket Lab; SpaceNews |
| Q1 2026 | **5 dedicated Neutron bookings** signed Jan–Mar 2026 (alongside 31 Electron/HASTE) — first publicly acknowledged *commercial* Neutron bookings | NASASpaceFlight; Via Satellite |
| May 2026 | Largest launch contract in company history: confidential customer, **5 Neutron + 3 Electron**, baselined 2026–2029 | Rocket Lab IR; Globe Newswire |
| 2026 | US military **point-to-point cargo test flight** on Neutron (2026) | Space.com |

The booked Neutron manifest is therefore on the order of **~10+ dedicated
launches** spanning 2026–2029 — broadly consistent with the one-three-five ramp.
Demand is real but **modest in absolute terms**, and all commercial customers
remain confidential.

---

## 5. The addressable launch market

### 5.1 Total global orbital launches

| Year | Orbital launch attempts | Reached orbit | Source |
|---|---|---|---|
| 2023 | ~221 | ~212 | SpaceNews; illdefined.space |
| **2024** | **~254–259** | ~254 | BryceTech; SpaceNews; illdefined.space (counts vary ~254–259 by methodology) |
| **2025** | **~315–329** | ~315–321 | Aviation Week (+25% YoY); illdefined.space (**315 successful**); 329 incl. 3 Starship near-orbital tests |

2025 was a record year, up ~24–25% YoY.

### 5.2 Where the 2025 launches went

From the illdefined.space 2025 summary (315 successful launches):

| Provider / bloc | 2025 launches | Captive? |
|---|---|---|
| **SpaceX** | **165** (mostly Starlink) | Almost entirely captive (own constellation + Falcon manifest) |
| **China** (all providers) | **90** | Overwhelmingly captive (state/quasi-state) |
| Rocket Lab (Electron) | 18 | Rocket Lab's own |
| ULA | 6 | US gov / Amazon Kuiper |
| Russia | 17 | Captive (state) |
| Blue Origin | 2 | Mostly own |
| Northrop Grumman | 1 | Captive |
| Other nations (India, Japan, France, Israel, S. Korea) | ~16 | Mostly national/captive |

### 5.3 What is realistically contestable by Neutron

The honest filtering:

- **SpaceX's 165** are not contestable — Starlink self-launch plus a Falcon
  manifest Neutron cannot price against at SpaceX's marginal cost.
- **China's 90 + Russia's 17** are geopolitically closed to a US vehicle.
- **Other-nation launches (~16)** are largely national-program captive.
- That leaves the genuinely *open, commercial, medium-lift-class* segment:
  Western commercial constellation deployment, commercial GTO/GEO, smallsat
  rideshare/dedicated, and the contestable slice of US national-security launch
  — realistically on the order of **~30–50 launches/year today**, and Neutron
  competes for that against Falcon 9, ULA Vulcan, Ariane 6, Blue Origin's
  New Glenn, and emerging vehicles.
- The medium/heavy-lift launch *market by value* is independently sized at
  **~$10–17.5B in 2025** (wide range across research firms), growing to
  **~$14–16B by ~2029–30** `[CITED — Medium-Heavy Lift Launch Vehicle market
  reports, 2025–26]` — and most of *that* dollar value is SpaceX and
  government-captive.
- Rocket Lab's own framing: Peter Beck sizes the **launch TAM at $10–20B**
  (see §6) — consistent with a contestable medium-lift segment far smaller than
  the raw 315-launch headline.

> **Market verdict — the honest answer to "could Rocket Lab sell ~100 Neutrons
> a year to external customers?"** **No — not from today's addressable market.**
> The contestable, non-captive, medium-lift commercial/government segment is
> realistically **~30–50 launches/year**. Even capturing an aggressive
> ~40–60% share of that is **~15–30 Neutrons/year** to external customers —
> which lines up with Rocket Lab's *own* "monthly" (~12/yr) ambition and its
> 24/yr margin-target cadence, **not** 100/yr. Reaching ~100 external
> launches/year would require either (a) a structural expansion of total launch
> demand (new mega-constellations, a launch-cost-driven demand explosion), (b)
> displacing SpaceX at scale, or (c) — most relevant here — **a new captive
> demand source such as the orbital data-center venture itself acting as anchor
> customer.** This is exactly why `ambition_case.md` frames the ~95/yr cadence
> as *demand-pulled by the data center*, not sold into the open market. The
> data-center fleet is not competing for the contestable market — it would
> *be* the demand.

---

## 6. Rocket Lab's long-term ambition & TAM statements

Rocket Lab has **not** published a long-range revenue target, but management has
been explicit about TAM and strategic ambition:

- **Peter Beck's stated TAM framing** (three layers, "end-to-end space company"):
  - **Launch: ~$10–20B TAM**
  - **Satellites / space systems: ~$20–30B TAM**
  - **Space-based services** (communications/DirecTV-style, internet, Earth
    observation) **: ~$320B TAM** — the layer Neutron exists to unlock.
  `[CITED — Sherwood News / Payload "End-to-End Space" interview; Motley Fool
  Beck interview, Dec 2025]`
- Beck's stated goal: **"build the biggest space company in the world."** The
  strategic logic is that Neutron is not an end in itself but the **enabler for
  deploying Rocket Lab's own infrastructure and services in orbit** — the high-
  margin $320B layer.
- This is **strategically significant for the data-center thesis**: Rocket Lab's
  *own* corporate strategy is to move up the stack from launch into orbital
  infrastructure and services. An orbital data center is squarely inside the
  "space-based services" layer Beck is targeting — so the venture is
  *aligned with*, not orthogonal to, Rocket Lab's stated direction.

---

## 7. Confirm / correct summary for the valuation model

| Project's current assumption | Verdict | Recommended figure |
|---|---|---|
| Neutron customer price ~$55M | **Correct downward** | **$50–55M; central $50M** (management expects upward drift over time) |
| Neutron internal cost ~$15–20M | **Flag / correct** | No public figure. 50%-margin-at-24-launches implies **~$25M/launch at 24/yr cadence**; $15–20M is supportable only as a high-cadence, matured-reuse projection |
| First flight NET Q4 2026 | **Confirmed** | NET Q4 2026 (Rocket Lab reaffirmed Q1 2026) |
| ~3 launches 2027 | **Correct — one year optimistic** | **2027: ~1–3 (central ~2)** |
| ~5 launches 2028 | **Correct — one year optimistic** | **2028: ~3–5** |
| ~12/yr (monthly) thereafter | **Confirmed as stated ambition** | ~12/yr "monthly" is Rocket Lab's medium-term ambition; 50% margin pegged to 24/yr |
| Payload to LEO | **Confirmed** | 13t downrange-landing / 15t expended / 8.5t RTLS |
| Payload to SSO | **Not published — gap** | Estimate ~9–10t (downrange mode); confirm with Rocket Lab |
| ~100 Neutrons/yr to external customers | **Not supported by market** | Contestable external market ~30–50 launches/yr total; ~100/yr only feasible with the data-center venture as anchor demand |

---

## Sources

**Primary — Rocket Lab filings & official materials:**
- Rocket Lab Q4 & Full-Year 2025 results (record $602M revenue, +38%; $1.85B
  backlog; 44.3% non-GAAP gross margin) — Rocket Lab IR / Globe Newswire,
  26 Feb 2026: <https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-announces-fourth-quarter-and-full-year-2025-financial>
- Rocket Lab Q1 2026 earnings call transcript (Q2 guidance $225–240M; margin
  guidance; Neutron timing/cadence; long-term ~50% gross-margin target) —
  The Motley Fool, 8 May 2026:
  <https://www.fool.com/earnings/call-transcripts/2026/05/08/rocket-lab-rklb-q1-2026-earnings-transcript/>
- Rocket Lab "Biggest Launch Deal Yet" (5 Neutron + 3 Electron) — Rocket Lab IR /
  Globe Newswire, 7 May 2026:
  <https://www.globenewswire.com/news-release/2026/05/07/3290605/0/en/rocket-lab-s-biggest-launch-deal-yet-confidential-customer-books-multiple-neutron-and-electron-launches.html>
- Rocket Lab Neutron product page: <https://rocketlabcorp.com/launch/neutron/>
- Peter Beck "End-to-End Space" interview (TAM framing $10–20B / $20–30B / $320B)
  — Payload / Sherwood News:
  <https://sherwood.news/business/ceo-of-rocket-labs-biggest-pure-play-space-company/>
- Motley Fool interview with Peter Beck, Dec 2025:
  <https://www.fool.com/investing/2025/12/10/the-motley-fool-interviews-rocket-lab-ceo-peter-be/>

**Analyst consensus & financial data:**
- Rocket Lab analyst forecast (FY2026 ~$883M / FY2027 ~$1.3B consensus; EPS
  estimates) — stockanalysis.com:
  <https://stockanalysis.com/stocks/rklb/forecast/>
- Rocket Lab future outlook (CAGR, 2028 profit, narrative 2029/2030 figures) —
  Simply Wall St:
  <https://simplywall.st/stocks/us/capital-goods/nasdaq-rklb/rocket-lab/future>
- Rocket Lab Q1 2026 earnings — CNBC, 8 May 2026:
  <https://www.cnbc.com/2026/05/08/rocket-lab-rklb-q1-earnings-2026.html>
- Rocket Lab Q1 2026 slides / backlog $2.2B — Investing.com:
  <https://www.investing.com/news/company-news/rocket-lab-q1-2026-slides-record-revenue-up-64-backlog-hits-22b-93CH-4671036>

**Neutron specs, pricing & cadence:**
- Rocket Lab Neutron — Wikipedia (payload modes, cadence, manufacturing,
  Archimedes): <https://en.wikipedia.org/wiki/Rocket_Lab_Neutron>
- "Revisiting Rocket Lab and Neutron" (pricing / 50%-margin context) —
  illdefined.space: <https://www.illdefined.space/revisiting-rocket-lab-and-neutron/>
- Rocket Lab Neutron-delay coverage (cadence ramp slip; Beck's $15M/quarter
  program-cost statement) — The Motley Fool / Nasdaq, Nov 2025:
  <https://www.fool.com/investing/2025/11/16/everything-to-know-about-rocket-labs-neutron-delay/>
- US military point-to-point Neutron test flight — Space.com:
  <https://www.space.com/space-exploration/launches-spacecraft/us-military-taps-rocket-labs-new-neutron-launcher-for-point-to-point-cargo-test-flight-in-2026>
- Rocket Lab signs first Neutron customer — SpaceNews:
  <https://spacenews.com/rocket-lab-signs-first-neutron-launch-customer/>

**Launch-market size:**
- Global Orbital Launch Summary 2025 (315 successful launches; provider
  breakdown) — illdefined.space:
  <https://www.illdefined.space/the-ill-defined-space-global-orbital-launch-summary-2025/>
- "Global Orbital Launch Rate Jumped 25% in 2025" — Aviation Week:
  <https://aviationweek.com/space/launch-vehicles-propulsion/spaceops-global-orbital-launch-rate-jumped-25-2025>
- SpaceX launch surge / 2024 record — SpaceNews:
  <https://spacenews.com/spacex-launch-surge-helps-set-new-global-launch-record-in-2024/>
- Medium-Heavy Lift Launch Vehicle Global Market Report 2026 ($15.66B by 2030) —
  ResearchAndMarkets / Globe Newswire:
  <https://www.globenewswire.com/news-release/2026/01/14/3218896/0/en/Medium-Heavy-Lift-Launch-Vehicle-Global-Research-Report-2026-15-66-Bn-Market-Trends-Competitive-Landscape-Strategies-and-Opportunities-2020-2025-2025-2030F-2035F.html>

---

## Open questions

1. **Neutron's true marginal/internal cost.** Rocket Lab publishes only a
   *margin* target (50% at 24 launches/yr → ~$25M implied cost). The actual
   marginal cost — and its sensitivity to cadence and first-stage reuse maturity
   — is unpublished. The project's ~$15–20M figure is unsupported as a near-term
   number; needs either a Rocket Lab disclosure or an explicit "high-cadence
   projection" label.
2. **Neutron SSO payload.** No official figure exists. The ~9–10t estimate here
   is derived from a generic LEO→SSO penalty, not a Rocket Lab spec — confirm.
3. **FY2028+ consensus.** Free-tier data stops at FY2027; the FY2028 figure
   ("lowest analysts ~$1.3B") and the ~$1.5B-2029 / ~$2.5B-2030 narrative
   numbers are soft. A paid consensus feed (Bloomberg/Visible Alpha/FactSet)
   would firm these for the valuation model.
4. **Realised Neutron price.** $50M target vs ~$55M press shorthand vs
   management's "expect upward price discovery." The actual contracted price in
   the signed Neutron deals is confidential — the price used in the model is an
   estimate within a $50–55M band.
5. **The contestable-market number.** The ~30–50 launches/year "contestable
   medium-lift" figure is an analytic judgement built by filtering captive
   SpaceX/China/Russia/national launches out of the ~315 total — it is not a
   single published statistic. A dedicated launch-demand study (BryceTech /
   NSR / Quilty) would tighten it.
6. **When (if ever) Neutron reaches 24/yr.** Rocket Lab pegs its 50% launch
   margin to 24 launches/year but has put **no date** on that cadence. This is
   the single most important unknown for both the launch-segment margin in the
   valuation model and the cadence feasibility in `ambition_case.md`.
