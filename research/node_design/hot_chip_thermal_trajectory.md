# Hot AI Chips, Cooling-Loop Temperatures & the Orbital Radiator Mass Payoff

*Project: RKLB Space Data Center — feasibility phase. Document date: May 2026.*
*Author: research agent. Scope: how hot today's AI accelerators and their liquid loops run, where the industry is taking loop temperature, and what running an orbital node's radiator hotter does to the single heaviest subsystem on the node. Hard numbers cross-checked against ≥2 sources where possible; estimates flagged.*

---

> **Source status (2026-05-25):** See [SOURCE_INDEX.md](../SOURCE_INDEX.md) claim IDs THR-001, THR-003 through THR-005, and THR-011 through THR-012. The radiative physics is source-certified. The radiator areas, masses, flyability ceilings, and 70–80 °C hot-loop design point are derived model outputs that depend on sink temperature, emissivity, areal density, and chip-to-panel thermal resistance; they are not vendor product guarantees.

## Summary / Verdict

**"Run the chips hot" is a real, first-order lever on the orbital node's dominant mass problem — and the industry is already walking toward it for its own (terrestrial) reasons.**

1. **Today's chips already tolerate hot silicon.** Flagship accelerators carry a junction-temperature limit (Tjmax) of only **~83–85 °C** (H100 SXM ~83 °C; Blackwell B200 ~85 °C) — they are *not* cool-running parts, they are tightly thermally constrained. ([NVIDIA H100 / liquid-cooling analysis](https://www.formulamod.net/blogs/new/h100-water-cooling-guide-ai-research-gpu), [B200 thermal specs](https://alliancechemical.com/blogs/articles/gpu-thermal-density-b200-gb200-coolant-flow-specs))
2. **The cooling loop is being deliberately warmed.** The clear industry trajectory is **warm-water cooling**: from chilled ~17–32 °C loops toward **45 °C supply / ~65 °C return**, codified in ASHRAE's new **W40 / W45 / W+** liquid classes. NVIDIA's Vera Rubin (shipping H2 2026) is specified for **45 °C inlet water with "no chillers needed."** ([ASHRAE 5th-ed thermal guidelines](https://www.upsite.com/blog/major-changes-to-ashraes-fifth-edition-of-thermal-guidelines-part-3-liquid-cooling-chapter-updates/), [NVIDIA Rubin 45 °C](https://www.tonygrayson.ai/post/nvidia-vera-rubin-cooling-45c-no-chiller))
3. **The orbital payoff is large and follows T⁴.** Because radiated heat flux scales as absolute temperature to the 4th power, raising the radiator from a 40 °C surface to an 80 °C surface **roughly doubles heat rejection per m²** (275 → 561 W/m²) and **halves radiator area and mass — a ~51% mass cut.** For the 130 kW baseline node, that is **~2.36 t → ~1.16 t (saves ~1.2 t)**; for a 600 kW node, **~10.9 t → ~5.3 t (saves ~5.6 t)**. Pushing to a 100 °C surface saves ~63%.
4. **The catch is reliability.** Hotter silicon accelerates wear-out (Arrhenius: roughly **2× failure rate / halved life per +10 °C** for thermally-activated mechanisms), raises leakage power (exponential in T), and narrows the throttle margin. Prior project research already found **~7–9 % annual GPU failure**; running hot worsens the *useful-life* failure floor that burn-in cannot remove.
5. **Verdict — yes, it is a usable lever, and it moves the flyability ceiling.** The trick is that **chip junction temperature and radiator surface temperature are decoupled by the loop ΔT.** You do *not* have to cook the silicon to run a hot radiator — you exploit the warm-water trend the vendors are already delivering, and accept a *modest, bounded* junction-temperature rise. A realistic "hot-loop" design point — **~70–80 °C radiator surface vs. a ~40–50 °C conservative baseline** — shrinks radiator mass by **~40–55 %**. Against the prior simulation's **~214 kW baseline-Neutron flyability ceiling**, freeing ~1–3 t of radiator mass plausibly **raises that ceiling into the ~260–320 kW range** (estimate — see §5). It does not solve the 600 kW node alone, but it is one of the highest-leverage single moves available, because it attacks the heaviest subsystem with a 4th-power law.

**Confidence: medium-high** on chip/loop temperatures and the warm-water trajectory (well-sourced, multiple vendors). **Medium** on the radiator-mass arithmetic (sound physics on stated assumptions; sink temperature, emissivity and areal density carry the uncertainty). **Medium-low** on the exact new flyability ceiling (depends on the prior sim's internals, not re-run here).

> **Reconciled ceiling (wave-5, 2026-05-17):** the "~214 kW → ~260–320 kW"
> figures in this doc build on top of the *pre-wave-5* ~214 kW simulation
> ceiling, which was computed at the stale 8.5 t SSO budget. Wave 5 corrected
> the SSO budget to ~9.5 t and re-derived the baseline ceiling at ~200–250 kW
> (working ~225 kW); building the hot-loop lever on that corrected base gives a
> reconciled **~270–320 kW baseline + hot-loop (working ~300 kW)** and
> **~430–470 kW block-upgraded + hot-loop** — see `synthesis/wave5_synthesis.md`
> §2.3/§2.4. The hot-loop mass arithmetic in this doc is unchanged; only the
> ~214 kW anchor it references is superseded.

---

## Radiator area & mass vs. temperature — the headline table

**Stefan-Boltzmann:** net rejected flux per unit area `Q/A = ε·σ·(T_rad⁴ − T_sink⁴)`.
**Assumptions (held constant across the table):** emissivity `ε = 0.85`; `σ = 5.670×10⁻⁸ W·m⁻²·K⁻⁴`; effective radiative sink `T_sink = 250 K` (LEO panel with Earth-IR + albedo backload — see §3.1); one effective radiating face per m² of planform; areal density **5 kg/m²** (the "mid" deployable-radiator figure from `solar_radiator_trajectory.md` §3). `T_rad` is the **radiator surface** temperature, not the chip junction.

| Radiator surface T | T_rad (K) | T_rad⁴ | **Net flux (W/m²)** | Area @130 kW | Area @300 kW | Area @600 kW | Mass @130 kW | Mass @300 kW | Mass @600 kW |
|---|---|---|---|---|---|---|---|---|---|
| **40 °C** (conservative baseline) | 313.15 | 9.616×10⁹ | **275 W/m²** | 472 m² | 1,090 m² | 2,180 m² | **2.36 t** | **5.45 t** | **10.90 t** |
| **60 °C** | 333.15 | 1.232×10¹⁰ | **405 W/m²** | 321 m² | 740 m² | 1,480 m² | 1.60 t | 3.70 t | 7.40 t |
| **80 °C** (hot-loop target) | 353.15 | 1.555×10¹⁰ | **561 W/m²** | 232 m² | 534 m² | 1,069 m² | **1.16 t** | **2.67 t** | **5.34 t** |
| **100 °C** (aggressive) | 373.15 | 1.939×10¹⁰ | **746 W/m²** | 174 m² | 402 m² | 804 m² | 0.87 t | 2.01 t | 4.02 t |
| **120 °C** (very aggressive) | 393.15 | 2.389×10¹⁰ | **963 W/m²** | 135 m² | 311 m² | 623 m² | 0.67 t | 1.56 t | 3.11 t |

**The T⁴ leverage, explicit.** Going from a 40 °C to an 80 °C surface is only a **+40 °C / +12.8 %** rise in *absolute* temperature (313 K → 353 K), but because flux goes as T⁴ the *net* flux rises **2.04×** (275 → 561 W/m²) — slightly more than the ratio (353/313)⁴ = 1.62× because subtracting the fixed T_sink⁴ term steepens the curve. Result: **area and mass roughly halve.**

**Mass saved by running 40 °C hotter (40 °C → 80 °C radiator surface):**

| Heat load | Mass @40 °C | Mass @80 °C | **Mass saved** | **% lighter** |
|---|---|---|---|---|
| 130 kW | 2.36 t | 1.16 t | **1.20 t** | **51 %** |
| 300 kW | 5.45 t | 2.67 t | **2.78 t** | **51 %** |
| 600 kW | 10.90 t | 5.34 t | **5.56 t** | **51 %** |

Pushing all the way to a 100 °C surface saves **~63 %** vs. the 40 °C baseline (130 kW: −1.49 t; 600 kW: −6.88 t). The percentage is load-independent — area and mass are linear in watts, so the *fractional* T⁴ benefit is identical at every node size; the *absolute* tonnage saved scales with power.

---

## 1. Current operating temperatures — what today's racks actually run at

### 1.1 Chip junction / case temperature

| Accelerator | TDP | **Tjmax (junction limit)** | Typical operating Tj under good liquid cooling | Notes |
|---|---|---|---|---|
| **H100 SXM** | 700 W | **~83 °C** | ~60–70 °C | Throttles above Tjmax; liquid loops aim for ~13–23 °C of margin. ([FormulaMod H100 cooling](https://www.formulamod.net/blogs/new/h100-water-cooling-guide-ai-research-gpu), [NVIDIA dev forum](https://forums.developer.nvidia.com/t/nvidia-h100-recommended-operating-temperature/342125)) |
| **H100 PCIe** | 350 W | ~83 °C class | lower | Air- or liquid-cooled. ([NVIDIA H100 product brief](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf)) |
| **Blackwell B200** | 1000 W air / **1200 W liquid** | **~85 °C** | ~43–70 °C under spec'd DLC | "10 °C ΔT is the *full* thermal budget" on a 1000 W die — margins are tight. ([Alliance Chemical B200/GB200 specs](https://alliancechemical.com/blogs/articles/gpu-thermal-density-b200-gb200-coolant-flow-specs), [Lenovo B200 1000 W guide](https://lenovopress.lenovo.com/lp2226-thinksystem-nvidia-b200-180gb-1000w-gpu)) |
| **GB200 / GB300 (Grace+Blackwell)** | ~1,200–1,400 W per module | ~85 °C class | — | NVL72 rack rejects ~120–135 kW, ~90 % via liquid. ([ToneCooling GB200](https://tonecooling.com/nvidia-gb200-nvl72-cooling-requirements/), [ToneCooling GB300](https://tonecooling.com/gb300-liquid-cooling-requirements-2026/)) |
| **Vera Rubin (Rubin GPU)** | higher still (power rack architecture) | ~85 °C class (est.) | — | First NVIDIA platform spec'd for 45 °C warm-water DLC; ships H2 2026. ([Rubin cooling](https://www.tonygrayson.ai/post/nvidia-vera-rubin-cooling-45c-no-chiller)) |

**Key reading:** AI accelerators are **not low-temperature parts**. Tjmax sits at only ~83–85 °C and has barely moved across H100 → Blackwell → Rubin. What *has* moved is power density: 700 W → 1,000–1,200 W+ per die. The silicon is run as hot as the vendor dares; the design problem is getting the heat *out* fast enough, which is exactly the orbital radiator problem.

### 1.2 The liquid-cooling loop today

NVIDIA GB200 NVL72 direct-liquid-cooling loop, as deployed (sources vary by deployment generation — this is the spread):

- **Cold-plate / facility-water inlet:** specs range **20–25 °C (strict / chilled)** up to **30–45 °C (max)**. The widely-cited GB200 envelope is **inlet ≤ 45 °C, return ≤ 65 °C**. ([QCT Qoolrack GB200](https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf), [ToneCooling GB200](https://tonecooling.com/nvidia-gb200-nvl72-cooling-requirements/))
- **Loop ΔT:** ~10–20 °C across the rack; cold-plate ΔT on a 1000 W die can be the *entire* ~10 °C thermal budget. ([Alliance Chemical](https://alliancechemical.com/blogs/articles/gpu-thermal-density-b200-gb200-coolant-flow-specs))
- **DLC capture fraction:** direct-to-chip cold plates remove **80–95 %** of server heat into the liquid; the rest is air-side (irrelevant in vacuum — see §3.3). ([gpu.fm liquid-cooling guide](https://www.gpu.fm/blog/liquid-cooling-ai-gpu-servers-guide))

So a *current, non-aggressive* terrestrial rack already runs a coolant loop whose **return water is ~55–65 °C**. That return temperature — not the chilled inlet — is what sets how hot a radiator fed by that loop can be. Today's racks therefore *already* support a radiator surface comfortably in the 45–60 °C band; the 40 °C baseline in the headline table is genuinely conservative.

---

## 2. The trajectory — the industry is designing loops to run hotter

### 2.1 ASHRAE liquid-cooling temperature classes — the codified roadmap

ASHRAE's *Thermal Guidelines for Liquid-Cooled Data Processing Environments* defines facility-water supply classes by maximum entering temperature. The classes were **renamed and extended upward in the 2022 / 5th-edition update**, explicitly to accommodate hotter operation ([ASHRAE 5th-ed update](https://www.upsite.com/blog/major-changes-to-ashraes-fifth-edition-of-thermal-guidelines-part-3-liquid-cooling-chapter-updates/), [Dallas ASHRAE guidelines deck](https://dallas-ashrae.org/images/meeting/041625/the_ashrae_thermal_guidelines_for_data_centers_____past__present_and_future.pdf)):

| Class (new name) | Old name | Max supply water temp | Cooling approach |
|---|---|---|---|
| W17 | W1 | 17 °C | Chiller + cooling tower |
| W27 | W2 | 27 °C | Chiller + tower |
| W32 | W3 | 32 °C | Often chiller-free |
| **W40** | *new in 2022* | **40 °C** | Chiller-free in most climates |
| **W45** | W4 | **45 °C** | Chiller-free — free cooling |
| **W+** | W5 | **>45 °C** | Chiller-free, max efficiency |

The very existence of **W40 and W+ being added** is the roadmap statement: the standards body is making room for loops *hotter than anything previously classed*. Compliance requires **full, unthrottled ITE operation across the whole class** — i.e. the chips must keep up at the hotter loop temperature.

### 2.2 Why the industry wants hotter loops (terrestrial drivers)

- **Free cooling.** At ~45 °C supply, a data center can reject heat with ambient air alone (dry coolers) across most of the U.S., **eliminating mechanical chillers** — a large capex and opex cut. At 35 °C it cannot. ([DCD hot-water/cold-water](https://www.datacenterdynamics.com/en/analysis/hot-water-cold-water/), [Network World — raising the temp](https://www.networkworld.com/article/4135239/raising-the-temp-on-liquid-cooling.html))
- **Heat reuse.** Warmer return water (~60–65 °C) is useful for district heating; cold waste heat is worthless.
- **Rising rack power density forces it.** As racks climb past 100–150 kW, the only way to move that much heat in a sane flow rate is a bigger loop ΔT, which pushes return — and often supply — temperatures up.

### 2.3 Vendor roadmap statements — where loops are heading

- **NVIDIA Vera Rubin (H2 2026):** spec'd for **45 °C warm-water single-phase DLC**, with NVIDIA's stated claim that **"no water chillers are necessary."** Supply ~45 °C, return up to ~65 °C. The Rubin "power rack" architecture moves to **100 % liquid coverage**. ([Rubin 45 °C / no-chiller](https://www.tonygrayson.ai/post/nvidia-vera-rubin-cooling-45c-no-chiller), [GenAI Tech — Rubin no-chiller](https://www.genaitech.net/p/rubins-no-chiller-shock-who-loses), [Nautilus — Rubin high-temp cooling](https://nautilusdt.com/news-updates/nvidias-rubin-platform-accelerates-the-shift-to-higher-temperature-liquid-cooling-in-ai-data-centers-and-what-that-means-for-the-industry/))
- **NVIDIA's own framing:** "Supercomputers can stay chill with hot water" — NVIDIA has publicly noted its chips **run at ~85–90 °C and that this *enables* ~45 °C inlet water**. The hot chip is a *feature* for the cooling system, not a bug. ([Fierce Network — NVIDIA hot water](https://www.fierce-network.com/cloud/nvidia-has-no-chill))
- **Cooling-vendor ecosystem:** DCX announced an **8 MW CDU optimized for 45 °C warm-water Vera Rubin deployments** (Jan 2026); LiquidStack, Supermicro, Vertiv, Schneider have all announced 40–45 °C support across 2024–2025. ([DCX 45 °C CDU](https://www.businesswire.com/news/home/20260123068139/en/DCX-Liquid-Cooling-Systems-Announces-New-8MW-Coolant-Distribution-Unit-Optimized-for-45C-Warm-Water-Cooling-in-Next-Gen-NVIDIA-Vera-Rubin-AI-Deployments), [DCD analysis](https://www.datacenterdynamics.com/en/analysis/hot-water-cold-water/))

**The realistic ceiling — and the founder's "~80 °C" instinct.** The founder's intuition that loops are heading toward ~80 °C is **directionally correct and partially confirmed**: *return* water already reaches ~60–65 °C today and Rubin pushes *supply* to 45 °C. But there is a near-term brake: Schneider Electric's cooling lead has stated that **50–60 °C supply water is "highly unlikely," especially for training loads**, because Tjmax is only ~85 °C and the loop ΔT plus cold-plate ΔT eats the margin. ([CoolIT — warm water still needs chillers](https://www.coolitsystems.com/resources/news/warm-water-cooling-and-ai-the-future-is-here-but-its-not-chiller-free/), [DCD](https://www.datacenterdynamics.com/en/analysis/hot-water-cold-water/))

**Reconciling this for the orbital case:** terrestrially, "loop temperature" usually means *supply*. For sizing a radiator, what matters is the temperature of the fluid arriving *at the radiator* — i.e. the **rack return / hot-side temperature**, which is already ~60–65 °C and trending up. An orbital node can also legitimately push the return leg hotter than a terrestrial site would, because (a) there is no chiller to protect and (b) the radiator surface is a few °C *below* the fluid feeding it. A **radiator surface of 70–80 °C is consistent with a ~80–90 °C hot-side coolant**, which is consistent with a ~85 °C Tjmax *if* you accept thin junction margin. So 80 °C is an aggressive-but-not-fantasy radiator target; 100–120 °C would require silicon that does not yet exist (see §4) or a two-phase loop.

---

## 3. The orbital radiator payoff — quantified

### 3.1 Method and assumptions

A compute node must reject **~100 % of rack electrical power as heat** — silicon converts essentially all input power to heat. In vacuum the *only* heat-rejection path is **thermal radiation** (no convection, no conduction to ambient). Radiator performance is governed by Stefan-Boltzmann:

`Q/A = ε·σ·(T_rad⁴ − T_sink⁴)`

- `ε = 0.85` — emissivity of a good radiator coating (white paint / OSR class). [FLAG: assumption; range 0.8–0.92.]
- `σ = 5.670374×10⁻⁸ W·m⁻²·K⁻⁴` — Stefan-Boltzmann constant (confirmed physical constant).
- `T_sink = 250 K` — effective radiative sink for a LEO panel. Deep space is ~3 K, but a real LEO radiator sees Earth IR (~240 K equivalent) and reflected albedo on part of its field of view, raising the *effective* sink to ~250 K. [FLAG: assumption consistent with `solar_radiator_trajectory.md` and `node_mass_model.md`; a dawn-dusk SSO orbit with edge-on Earth view does better, a worse attitude does worse. This is the single biggest swing variable in the model.]
- One effective radiating face per m² of planform (a two-sided panel with one face partially blocked nets out near this). [FLAG: assumption.]
- Areal density **5 kg/m²** — the "mid" figure for a large pumped-loop deployable radiator including panel, headers, fluid and deployment structure (`solar_radiator_trajectory.md` §3 range: 3 low / 5 mid / 8 high).

### 3.2 Worked arithmetic (showing the 80 °C / 130 kW cell)

Net flux at an 80 °C surface:
- `T_rad = 80 + 273.15 = 353.15 K`
- `T_rad⁴ = 353.15⁴ = 1.5554×10¹⁰ K⁴`
- `T_sink⁴ = 250⁴ = 3.9063×10⁹ K⁴`
- `Q/A = 0.85 × 5.670374×10⁻⁸ × (1.5554×10¹⁰ − 0.39063×10¹⁰)`
- `Q/A = 0.85 × 5.670374×10⁻⁸ × 1.1648×10¹⁰ = 561.4 W/m²`

Area for 130 kW: `A = 130,000 W ÷ 561.4 W/m² = 232 m²`
Mass: `232 m² × 5 kg/m² = 1,158 kg ≈ 1.16 t`

Same arithmetic at 40 °C gives `Q/A = 275 W/m²` → `A = 472 m²` → `2.36 t`.
**Mass saved by the 40 °C → 80 °C move at 130 kW = 2.36 − 1.16 = 1.20 t (51 % lighter).** Full grid in the headline table above.

### 3.3 Why the orbital payoff is even better than terrestrial

Terrestrially, warm water mostly buys *energy efficiency*. In orbit it buys **mass directly**, and mass is the binding launch constraint. Two amplifiers:

1. **No air-side path exists in vacuum.** Every watt the chip produces must leave via the radiator. There is no "the other 5–20 % goes to room air" — the radiator carries 100 %. That makes radiator sizing absolutely load-bound and makes the T⁴ lever worth its full value.
2. **T⁴ vs. the linear solar array.** From `solar_radiator_trajectory.md`, the radiator is the *heaviest* single subsystem and improves only slowly on areal density. Loop/surface temperature is the one radiator lever with a **4th-power** payoff — nothing else on the node has that exponent.

### 3.4 The catch in the orbital geometry

- **The 100 °C and 120 °C columns are mostly theoretical** with today's silicon: a 120 °C radiator surface implies hot-side coolant well above 120 °C, which is incompatible with an ~85 °C Tjmax single-phase loop. Reaching them needs either future high-temp silicon, a **two-phase / pumped-two-phase loop** (which can hold a high, near-isothermal radiator temperature while the chip stays cooler), or accepting that the node simply cannot use those columns. **The realistically reachable band with 2026-class chips is the 40–80 °C surface range.**
- **T_sink sensitivity.** If the effective sink is 270 K instead of 250 K (worse Earth view), all areas grow ~10–20 %; if it is 230 K (excellent dawn-dusk SSO, edge-on Earth), they shrink similarly. The *fractional* hot-vs-cold benefit is robust; the absolute areas are not.

---

## 4. The catch — reliability & performance tradeoffs of hot silicon

Running the **radiator** hot is nearly free. Running the **silicon** hot is not. The two are linked by the loop+cold-plate ΔT, so a hotter radiator pulls junction temperature up unless you spend ΔT budget you may not have.

### 4.1 Arrhenius — failure rate climbs with temperature

Thermally-activated wear-out mechanisms (electromigration, dielectric breakdown / TDDB, intermetallic growth, corrosion) follow the **Arrhenius model**: rate `∝ exp(−Ea / kT)`. Practical consequences ([Electronics Cooling — the 10 °C rule](https://www.electronics-cooling.com/2017/08/10c-increase-temperature-really-reduce-life-electronics-half/), [JetCool — temperature & MTTF](https://jetcool.com/post/semiconductor-lifetime-how-temperature-affects-mean-time-to-failure-device-reliability/), [NoMTBF — 0.7 eV](https://nomtbf.com/2012/08/where-does-0-7ev-come-from/)):

- **Rule of thumb: every +10 °C roughly doubles failure rate / halves useful life** for Arrhenius-governed mechanisms (this corresponds to Ea ≈ 0.7 eV near 100 °C).
- A concrete published example: a processor at **90 °C effective Tj has ~2× the useful life of the same part at 105 °C.** ([JetCool](https://jetcool.com/post/semiconductor-lifetime-how-temperature-affects-mean-time-to-failure-device-reliability/))
- **Important nuance — Arrhenius is not the whole story.** It governs *wear-out*. Two of this node's biggest real-world failure drivers — **thermal-cycling solder/HBM fatigue** and **package-to-board interconnect fatigue** — are *not* Arrhenius-governed; they are driven by ΔT *swing*, not absolute T. ([Electronics Cooling](https://www.electronics-cooling.com/2017/08/10c-increase-temperature-really-reduce-life-electronics-half/)) So "+10 °C = ½ life" overstates the hit if applied to *all* failures. It applies cleanly to electromigration/TDDB.

### 4.2 Leakage power rises exponentially with temperature

Subthreshold leakage current is **exponential in temperature** ([arXiv — leakage vs temperature](https://arxiv.org/pdf/1809.03147), [Mudge — leakage & static power](https://tnm.engin.umich.edu/wp-content/uploads/sites/353/2017/12/2003.12.Leakage-Current-Moores-Law-Meetings-Static-Power_Computer.pdf)). Hotter silicon → more static power → *more* heat to reject → a partial **positive-feedback loop** that erodes some of the radiator saving and, in the worst case, causes thermal runaway if the loop is marginal. The effect is real but second-order at the ~10–30 °C junction deltas under discussion (single-digit-percent extra power), not a showstopper — but it must be in the node power/thermal budget.

### 4.3 Throttling — the performance hit

Tjmax (~83–85 °C) is a hard throttle line. Run the junction near it and any transient — a flow wobble, a partial cold-plate blockage, a hot orbital-noon excursion — pushes the chip into **thermal throttling: typically 10–20 % loss of throughput** ([bottleneckcheck — throttling](https://bottleneckcheck.com/thermal-throttling-fix/), and `reliability_failure_handling.md`'s NVL72 degradation finding). A hot-loop orbital node therefore *trades thermal margin for radiator mass* — and thin margin is dangerous on an un-serviceable node.

### 4.4 The tradeoff, characterized

| Lever | Radiator-mass benefit | Reliability / performance cost |
|---|---|---|
| Hotter **radiator surface**, junction held constant (spend loop ΔT, two-phase loop, better cold plates) | Full T⁴ benefit (up to ~51 % at 40→80 °C) | **~Free** on reliability — silicon temperature unchanged. Cost is loop hardware (two-phase, bigger ΔT) and pumping. **This is the move to make.** |
| Hotter radiator achieved by letting **junction temperature rise** ~+10 °C | Full T⁴ benefit | ~2× wear-out failure rate for EM/TDDB; on a prior ~7–9 % AFR baseline this could push the wear-out component up materially; +leakage; thinner throttle margin. |
| Hotter radiator via **+20–30 °C junction** | Full T⁴ benefit | Junction near/over Tjmax — chronic throttling, sharply higher AFR, unacceptable for a 3-year un-serviceable node. |

**The design rule:** capture the radiator-mass win by raising the *loop/radiator* temperature, and **defend the junction**. Decoupling is done by ΔT budget — colder cold plates, higher coolant flow, or a two-phase loop that holds a hot, near-isothermal radiator while the evaporator at the chip stays cooler. The reliability cost is acceptable only for the slice of "hotness" that does *not* land on the silicon.

---

## 5. Verdict — does this move the flyability ceiling?

**Is "run it hot" a real lever on the dominant mass problem?** **Yes — clearly the highest-exponent lever available.** The radiator is the heaviest subsystem on the node and improves only slowly on areal density (`solar_radiator_trajectory.md`). Surface temperature is the *one* radiator parameter with a 4th-power payoff. Everything else (areal density, deployability) is linear or sub-linear.

**How much radiator mass can an aggressive-but-realistic hot-loop design save?**
- Realistic design move: shift the **radiator surface from a conservative ~40–50 °C baseline to a hot-loop ~70–80 °C**, riding the warm-water trend the vendors are already delivering (45 °C supply / 60–65 °C return today; Rubin pushing further).
- At 130 kW: radiator drops from ~2.0–2.4 t to ~1.2–1.5 t — **save ~0.7–1.2 t.**
- At 300 kW: from ~4.4–5.5 t to ~2.7–3.3 t — **save ~1.5–2.8 t.**
- At 600 kW: from ~8.7–10.9 t to ~5.3–6.5 t — **save ~3.3–5.6 t.**
- As a fraction: **~40–55 % lighter radiator** for the 40→80 °C move; ~30–40 % for a more cautious 50→75 °C move.

**Does it raise the flyability ceiling?** The prior simulation found a baseline-Neutron node **stops flying at ~214 kW rack power**. The radiator is a large part of what consumes the mass budget at that ceiling. Freeing **~1–3 t** of radiator mass (the realistic hot-loop saving in the 130–300 kW range) is a meaningful fraction of a Neutron reusable payload (~8.5 t). Re-spending that freed mass on more rack power:

- **Estimate: the ceiling plausibly rises from ~214 kW into the ~260–320 kW range** with an aggressive-but-realistic hot-loop design. [FLAG: estimate — the prior sim was not re-run here; the exact figure depends on how radiator mass trades against rack and bus mass inside that sim. The *direction and rough magnitude* are robust; the precise number is not.]
- It does **not**, by itself, make a 600 kW single-node mission fly on a reusable Neutron — that still needs multi-launch assembly or node-power capping (`solar_radiator_trajectory.md` §4). But combined with the other levers (advanced low-areal-density radiators, GaAs arrays, expendable Neutron), hot-loop operation is one of the few moves that **shifts the ceiling rather than just nibbling at it.**

**Bottom line for the founder.** The instinct is right: future chips and (more importantly) their *loops* are being designed to run hotter, and that is directly bankable as orbital radiator mass. But the saving comes from running the **coolant loop and radiator** hot — not from cooking the silicon. Tjmax has barely moved (~83–85 °C) and the reliability penalty for hot *junctions* is real (Arrhenius ~2×/+10 °C). The winning design **rides the warm-water trajectory (45 °C+ loops), pushes the radiator surface to ~70–80 °C, holds the junction near today's ~70 °C with ΔT budget / two-phase cooling, and banks a ~40–55 % radiator-mass cut** — enough to move the flyability ceiling up by an estimated ~50–100 kW of rack power.

---

## Sources

**Chip & loop temperatures (current)**
- [FormulaMod — H100 water-cooling guide (Tjmax ~83 °C, 60–70 °C operating)](https://www.formulamod.net/blogs/new/h100-water-cooling-guide-ai-research-gpu)
- [FormulaMod — H100/H200/B200 liquid cooling](https://www.formulamod.net/blogs/new/ai-server-gpu-water-cooling-why-liquid-cooling-matters-for-h100-h200-and-b200)
- [NVIDIA Developer Forum — H100 recommended operating temperature](https://forums.developer.nvidia.com/t/nvidia-h100-recommended-operating-temperature/342125)
- [NVIDIA H100 PCIe product brief](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf)
- [Alliance Chemical — B200/GB200/MI300 thermal density & coolant flow (B200 ~85 °C junction)](https://alliancechemical.com/blogs/articles/gpu-thermal-density-b200-gb200-coolant-flow-specs)
- [Lenovo Press — ThinkSystem NVIDIA HGX B200 180GB 1000 W](https://lenovopress.lenovo.com/lp2226-thinksystem-nvidia-b200-180gb-1000w-gpu)
- [ToneCooling — GB200 NVL72 cooling requirements (inlet ≤45 °C, return ≤65 °C)](https://tonecooling.com/nvidia-gb200-nvl72-cooling-requirements/)
- [ToneCooling — GB300 liquid cooling requirements 2026](https://tonecooling.com/gb300-liquid-cooling-requirements-2026/)
- [QCT Qoolrack — advanced liquid cooling for GB200 NVL72](https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf)
- [gpu.fm — liquid cooling AI GPU servers guide (DLC 80–95 % heat capture)](https://www.gpu.fm/blog/liquid-cooling-ai-gpu-servers-guide)

**The trajectory toward hotter loops**
- [Upsite — ASHRAE 5th-ed thermal guidelines, liquid-cooling chapter (W17–W+ classes)](https://www.upsite.com/blog/major-changes-to-ashraes-fifth-edition-of-thermal-guidelines-part-3-liquid-cooling-chapter-updates/)
- [Dallas ASHRAE — Thermal Guidelines past/present/future](https://dallas-ashrae.org/images/meeting/041625/the_ashrae_thermal_guidelines_for_data_centers_____past__present_and_future.pdf)
- [ASHRAE — 30 °C coolant: a durable roadmap](https://ashrae.org.vn/wp-content/uploads/2024/12/30%C2%B0C-Coolant-A-Durable-Roadmap-for-the-Future-REV1_0.pdf)
- [DCD — what's the right temperature for water in liquid-cooled data centers?](https://www.datacenterdynamics.com/en/analysis/hot-water-cold-water/)
- [Network World — raising the temp on liquid cooling](https://www.networkworld.com/article/4135239/raising-the-temp-on-liquid-cooling.html)
- [CoolIT — warm-water cooling: the future is here but it's not chiller-free](https://www.coolitsystems.com/resources/news/warm-water-cooling-and-ai-the-future-is-here-but-its-not-chiller-free/)
- [Tony Grayson — NVIDIA Vera Rubin 45 °C, no chiller](https://www.tonygrayson.ai/post/nvidia-vera-rubin-cooling-45c-no-chiller)
- [GenAI Tech — Rubin's no-chiller shock](https://www.genaitech.net/p/rubins-no-chiller-shock-who-loses)
- [Nautilus — NVIDIA Rubin & the move to high-temperature liquid cooling](https://nautilusdt.com/news-updates/nvidias-rubin-platform-accelerates-the-shift-to-higher-temperature-liquid-cooling-in-ai-data-centers-and-what-that-means-for-the-industry/)
- [Fierce Network — "Supercomputers can stay chill with hot water," NVIDIA](https://www.fierce-network.com/cloud/nvidia-has-no-chill)
- [BusinessWire — DCX 8 MW CDU optimized for 45 °C warm-water Vera Rubin](https://www.businesswire.com/news/home/20260123068139/en/DCX-Liquid-Cooling-Systems-Announces-New-8MW-Coolant-Distribution-Unit-Optimized-for-45C-Warm-Water-Cooling-in-Next-Gen-NVIDIA-Vera-Rubin-AI-Deployments)

**Reliability / Arrhenius / leakage / throttling**
- [Electronics Cooling — does +10 °C really halve life?](https://www.electronics-cooling.com/2017/08/10c-increase-temperature-really-reduce-life-electronics-half/)
- [JetCool — semiconductor lifetime vs temperature (90 °C vs 105 °C → 2× life)](https://jetcool.com/post/semiconductor-lifetime-how-temperature-affects-mean-time-to-failure-device-reliability/)
- [NoMTBF — where 0.7 eV comes from](https://nomtbf.com/2012/08/where-does-0-7ev-come-from/)
- [arXiv 1809.03147 — is leakage power a linear function of temperature?](https://arxiv.org/pdf/1809.03147)
- [Mudge — leakage current: Moore's law meets static power](https://tnm.engin.umich.edu/wp-content/uploads/sites/353/2017/12/2003.12.Leakage-Current-Moores-Law-Meetings-Static-Power_Computer.pdf)
- [BottleneckCheck — thermal throttling (10–20 % FPS/throughput loss)](https://bottleneckcheck.com/thermal-throttling-fix/)

**Prior project documents**
- `node_design/solar_radiator_trajectory.md` — radiator areal density, sink assumptions, 130/300/600 kW scaling
- `node_design/node_mass_model.md` — 214 kW class flyability framing, radiator sizing assumptions
- `node_design/reliability_failure_handling.md` — ~7–9 % GPU AFR, thermal-cycling fatigue, NVL72 degradation

---

## Open questions

1. **Effective radiative sink temperature.** The 250 K T_sink assumption is the single largest swing variable. A dedicated orbit/attitude thermal model (dawn-dusk SSO, Earth-IR + albedo backload by season) would tighten every area/mass figure by ±15–20 %.
2. **Re-run the flyability sim.** The "~214 kW → ~260–320 kW" ceiling shift is an estimate. The prior simulation should be re-run with the hot-loop radiator mass curve from §3 substituted in, to get a defensible new ceiling.
3. **Two-phase loop trade.** Reaching 100 °C+ radiator surfaces while keeping the junction at ~70 °C likely needs a pumped-two-phase loop. What is its mass, reliability, and complexity penalty vs. the radiator mass it saves? This is the gateway to the 100/120 °C columns.
4. **Quantify the leakage feedback.** How many extra kW does a +10–20 °C junction add at the 130/300/600 kW points, and does that erode enough of the radiator saving to matter?
5. **Wear-out vs. cycling split.** Of this node's ~7–9 % AFR, what fraction is Arrhenius-governed wear-out (worsened by hot operation) vs. thermal-cycling fatigue (driven by ΔT swing, not absolute T)? Only the former is penalized by hot-loop operation; the split decides the true reliability cost.
6. **Rubin-class Tjmax.** Confirm whether Rubin/Vera silicon raises Tjmax above ~85 °C — if vendors push Tjmax up, the whole hot-loop band shifts and the 100 °C column becomes single-phase-reachable.
