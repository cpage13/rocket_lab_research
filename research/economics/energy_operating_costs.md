# Energy & Operating Costs: Terrestrial AI Rack vs. Orbital Node

*Research date: May 2026. Prepared for the orbital AI-inference data-center feasibility study (Neutron-launched node). Companion to `rack_cost_trajectory.md`, `revenue_per_watt.md`, `premium_value_case.md`.*

> **Superseded launch-cost basis (wave-9, 2026-05-17).** This document was
> written before the wave-9 launch-cost re-base and anchors its verdict, §6 and
> §7 on a **~$50–55M Neutron launch** — the *external customer price* — and on
> a stale wave-4-era "launch is ~85–90% of node cost" figure. The project has
> since adopted Rocket Lab's **internal marginal launch cost of ~$10–20M**
> (`CONCLUSION.md` Rev 4; `RESEARCH_TRACKER.md` wave-9). On the current basis,
> against a ~$45M-mid node, **launch is ~45% of node cost, not ~85–90%**, and
> the ~$1.15M of avoided 5-year opex offsets ~6% of a ~$20M launch rather than
> ~2–4% of a ~$55M one. **The qualitative verdict is unaffected** — avoided
> energy/water opex is second-order vs. launch under any of these figures, and
> orbit still replaces a small recurring opex with a far larger one-time
> solar/radiator capex. Read the launch-share percentages and the "~$50–55M"
> anchors below as stale; the energy/water analysis itself stands.

## Summary

**The founder's hypothesis — that energy/water is the dominant lifetime cost of an AI rack — does not hold.** Energy is a meaningful line item but it is secondary to the rack hardware, and far secondary to the launch.

The headline number: a single NVL72-class rack (~135 kW IT load, PUE ~1.3) draws ~175 kW of total facility power. Over 5 years at ~85% utilization and a mid-case industrial rate of $0.085/kWh, that delivers ~6.5 GWh and costs **~$0.56M in electricity** — only **~16% of the rack's ~$3.5M hardware capex**. Add water (~$0.05M direct) and maintenance (~$1.0M) and total 5-year terrestrial opex is **~$1.6M**, i.e. recurring opex is **~31% of the rack's 5-year total cost of ownership** (capex ~$3.5M + opex ~$1.6M ≈ $5.1M). Hardware capex (~69%) dominates.

**The orbital comparison then kills the thesis as a launch-justifier.** Orbit avoids essentially all of that ~$1.6M opex (electricity ≈ 0, water ≈ 0; ~$0.45M of ground-ops/maintenance residual remains). Net avoided opex ≈ **$1.15M over 5 years**. Yet the Neutron launch costs **~$50–55M** — avoided lifetime opex offsets only **~2–4% of the launch cost**. Worse, orbit must *replace* the utility bill with a one-time **solar-array + radiator capex of roughly $12–35M per rack**, which exceeds the opex it saves by an order of magnitude. Energy/water savings are a real but **second-order effect**; the orbital case must be won on revenue premium, latency, sovereignty, and — the one genuine power-related win — skipping the multi-year grid-interconnect and water-permitting queues, not on dodging the utility bill.

**Confidence: Medium-high.** IT power, PUE, electricity rates, and WUE are all well-corroborated 2025–2026 figures. Utilization and the 5-year horizon are modeling assumptions; orbital opex-avoidance is an estimate (the orbital power/thermal *capex* is itself substantial and is treated separately below).

---

## The 5-year energy cost calculation (headline)

**Formula:** `Total facility kW × 8,760 h/yr × 5 yr × utilization × $/kWh`

**Inputs (mid case):**
- IT load per rack: **135 kW** (NVL72-class; see §1)
- PUE: **1.3** → total facility power = 135 × 1.3 = **175.5 kW**
- Hours: 8,760 × 5 = **43,800 h**
- Utilization: **85%** (AI training/inference racks run hot; 80–90% typical)
- Electricity: **$0.085/kWh** (industrial/data-center blended; see §2)

**Mid-case arithmetic (step by step):**
```
Facility power      = 135 kW IT × 1.3 PUE        = 175.5 kW
Hours over 5 years  = 8,760 h/yr × 5 yr          = 43,800 h
Energy at 100% util = 175.5 kW × 43,800 h        = 7,686,900 kWh   (7.69 GWh)
Energy delivered    = 7,686,900 kWh × 0.85       = 6,533,865 kWh   (6.53 GWh)
5-year energy cost  = 6,533,865 kWh × $0.085/kWh = $555,378        (~$0.56M)
```
Sanity check: a 175.5 kW load running flat-out for one year = 1.54 GWh ≈ $131k/yr at $0.085/kWh; ×5 yr ×0.85 util ≈ $0.56M. Confirmed.

### 5-year energy cost — low / mid / high

| Case | IT kW | PUE | Facility kW | Util. | $/kWh | 5-yr kWh delivered | **5-yr energy cost** |
|------|-------|-----|-------------|-------|-------|--------------------|----------------------|
| Low  | 130   | 1.2 | 156         | 80%   | $0.055 | 5,466,240 | **$0.30M** |
| Mid  | 135   | 1.3 | 175.5       | 85%   | $0.085 | 6,533,865 | **$0.56M** |
| High | 155   | 1.5 | 232.5       | 90%   | $0.130 | 9,165,150 | **$1.19M** |

**Mid-case headline: a single AI rack costs ~$0.56M in electricity over 5 years** (range $0.30M–$1.19M). Against a ~$3.5M rack hardware capex, **5-year energy is only ~16% of the rack's capex** in the mid case (9% low, 34% high). Energy is a real cost but it does not dominate even the rack itself, let alone the launch.

---

## 1. Per-rack power, including overhead

**IT load.** An NVIDIA GB200 NVL72 rack is rated at **~120–132 kW** of IT load — Supermicro lists 132 kW total / 125–135 kW operating; HPE specs 132 kW; other deployments cite ~120 kW at full load ([Sunbird DCIM](https://www.sunbirddcim.com/blog/your-data-center-ready-nvidia-gb200-nvl72), [Introl](https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled)). The newer **GB300 NVL72** pushes to **~140–150 kW** ([Sunbird, GB300](https://www.sunbirddcim.com/blog/how-much-power-does-nvidia-gb300-nvl72-need)). Vera Rubin NVL72 and later "extreme-density" racks are provisioned at **250–600 kW** ([Introl, Vera Rubin](https://introl.com/blog/nvidia-vera-rubin-gpu-600kw-racks-2027)). **For this study we use 130–155 kW IT load (mid 135 kW)** — representative of an NVL72-class rack shipping today. *Confirmed.*

**PUE (data-center overhead).** PUE = total facility power ÷ IT power; it captures cooling, power conversion (UPS/transformer losses), and networking overhead.
- Global average PUE ≈ **1.58** (Uptime Institute 2024 survey).
- Hyperscale / new builds: **1.09–1.20**; Google reported fleet-wide **1.09** in 2025 ([Google Data Centers](https://datacenters.google/efficiency/)).
- **Liquid-cooled AI racks specifically: PUE 1.10–1.20**, with the best deployments at 1.02–1.10 ([TAAL Tech](https://www.taaltech.com/high-density-data-centers-when-to-shift-from-air-cooling-to-liquid-cooling/)).
- NVL72-class racks are liquid-cooled by necessity (cold plates take ~90–100 kW; ~25 kW still goes to air).

**We adopt PUE 1.2 (low) / 1.3 (mid) / 1.5 (high).** Mid 1.3 is conservative for a modern liquid-cooled AI hall — it allows for hot climate, older shell, or partial air-cooling. *Confirmed range; 1.3 mid-point is a modeling choice.*

**Total facility power per rack (mid case): 135 kW IT × 1.3 = 175.5 kW.** Range 156–232.5 kW.

---

## 2. Electricity price

**Industrial / data-center rates ($/kWh), 2025–2026:**
- U.S. average **industrial** rate: **$0.0862/kWh** in 2025 ([Statista/EIA](https://www.statista.com/statistics/190680/us-industrial-consumer-price-estimates-for-retail-electricity-since-1970/)).
- Site Selection Group: continental-U.S. industrial range **~$0.047 to ~$0.15/kWh**; U.S. average **$0.0733/kWh** ([Site Selection Group](https://info.siteselectiongroup.com/blog/power-in-the-data-center-and-its-costs-across-the-united-states)).
- Cheap-power regions: Eastern Washington (hydro) **sub-$0.04/kWh**; large data-center deals frequently land **$0.04–0.07/kWh**.
- Expensive markets / commercial tariffs: **$0.13–0.15/kWh**.

**We adopt $0.055 (low) / $0.085 (mid) / $0.13 (high) per kWh.** *Confirmed range.*

**Trend.** Wholesale prices are rising sharply where AI load concentrates: PJM wholesale jumped from **$77.78/MWh (Q1 2025) to $136.53/MWh (Q1 2026), +75.5%**, attributed to data-center demand ([Tom's Hardware](https://www.tomshardware.com/tech-industry/ai-data-centers-trigger-massive-irreversible-76-percent-electricity-price-spike-in-largest-us-region-federal-watchdog-demands-tech-giants-pay-for-their-own-power-infrastructure)). Goldman: retail electricity +6.9% in 2025, ~2× inflation, with further rises expected through 2030 ([CNBC](https://www.cnbc.com/2026/02/12/electricity-price-data-center-ai-inflation-goldman.html)). **However**, large industrial/data-center buyers are largely insulated by long-term PPAs and special tariffs — industrial users on average pay *less* than two years ago even as residential bills climb ([Yale Climate Connections](https://yaleclimateconnections.org/2026/01/home-electricity-bills-are-skyrocketing-for-data-centers-not-so-much/)). The founder's instruction to assume prices "flat or slightly declining" for a large contracted buyer is **reasonable** — the headline spikes hit retail/residential and uncontracted wholesale, not hyperscale PPAs. We model flat. *Trend confirmed; the flat assumption for a contracted buyer is defensible.*

---

## 3. Five-year energy cost for one rack — vs. hardware capex

See the corrected table in the headline section. Restating the comparison:

| | 5-yr energy | Rack hardware capex | Energy as % of capex |
|---|---|---|---|
| Low | $0.30M | $3.5M | 9% |
| **Mid** | **$0.56M** | **$3.5M** | **16%** |
| High | $1.19M | $3.5M | 34% |

**Mid case: 5-year electricity ≈ $0.56M, ≈ 16% of the ~$3.5M rack hardware cost.** Even the high case ($1.19M) is only ~one-third of capex. Energy does **not** dominate the rack's lifetime cost at the rack level. (At the *fleet/gigawatt* level energy looms larger only because cheap-power siting and 24/7 operation aggregate it — but per-rack, against a multi-million-dollar accelerator, it is a minority line item. This matches Epoch AI's 1-GW model: servers ~60% of annual cost, energy the largest *opex* line but only ~$0.6B of a much larger total — [Epoch AI](https://epoch.ai/data-insights/ai-datacenter-cost-breakdown).)

---

## 4. Water

**Consumption.** Cooling water is measured by **WUE** (water usage effectiveness, liters per kWh of IT energy):
- Industry-standard average WUE ≈ **1.9 L/kWh**; U.S. direct water intensity 2023 ≈ **0.36 L/kWh**; best-in-class **<0.5 L/kWh**; range **1–9 L/kWh** evaporated depending on cooling type and climate ([EESI](https://www.eesi.org/articles/view/data-centers-and-water-consumption), [Apstech](https://apstechadvisors.com/data-center-water-consumption-in-the-us-challenges-trends-and-market-opportunities-for-2025-2030/)).
- Liquid-cooled AI racks with closed-loop cold plates use far less direct water than legacy evaporative air-cooled halls; NVIDIA highlights Blackwell water-efficiency gains ([Data Centre Magazine](https://datacentremagazine.com/hyperscale/how-nvidia-is-boosting-water-efficiency-with-blackwell)).

**Per-rack water, 5 years (mid case).** Direct cooling water at WUE ~1.0 L/kWh against IT energy (6.53 GWh / 1.3 PUE = 5.03 GWh IT energy delivered over 5 yr):
- 5.03 GWh = 5,026,050 kWh × 1.0 L/kWh = **~5.0 million liters ≈ 1.33 million gallons** over 5 years (~266k gal/yr).
- High case (WUE ~4 L/kWh, evaporative): ~20M L ≈ 5.3M gal over 5 yr.

**Cost.** Industrial water deals run **~$6/1,000 gal** (Google's Mesa, AZ deal: $6.08/1,000 gal — [EESI/airsys](https://airsysnorthamerica.com/how-much-water-does-a-data-center-use/)); commercial rates higher and **+43% over the past decade**.
- Mid: 1.33M gal × $6/1,000 = **~$8k over 5 yr** — *trivial as a direct line item*.
- High (evaporative + wastewater discharge fees + premium rates ~$12/1,000 gal): 5.3M gal × $12/1,000 ≈ **$64k**, round to **$0.1M** with discharge fees.

**Direct water cost is small per rack (~$10k–$100k over 5 yr).** *Confirmed — water is a minor line item financially.*

**The water issue is regulatory/ESG, not dollars.** Santa Clara County now mandates recycled water for large new data centers; Arizona, Nevada, Florida, Texas are following; HB1601-type bills demand water-impact assessments before zoning ([GRESB](https://www.gresb.com/cooling-data-centers-managing-water-use-in-the-age-of-ai-and-esg/)). A hyperscale site can evaporate ~550k gal/day (~200M gal/yr). The risk is **permitting delay, community opposition, and ESG-reporting exposure** — i.e. it can block or slow a build, not bankrupt it. *This is the genuinely interesting water angle for the orbital pitch (see §6/§7).*

---

## 5. Full terrestrial 5-year opex per rack vs. capex

**Maintenance.** Hardware procurement + maintenance is ~40–50% of data-center operating budgets; maintenance alone ~40% of opex; third-party maintenance runs 50–70% cheaper than OEM contracts ([The Network Installers](https://thenetworkinstallers.com/blog/data-center-operating-costs/)). For a ~$3.5M rack, hardware maintenance + parts + on-site labor + monitoring conservatively runs **~5–7% of capex per year → ~$0.18–0.25M/yr → ~$0.9–1.2M over 5 yr** (mid ~$1.0M). *Estimate.*

**5-year terrestrial opex per rack (mid case):**

| Line item | 5-yr cost (mid) | Basis |
|---|---|---|
| Electricity | $0.56M | §3, confirmed |
| Water (direct) | $0.05M | §4, confirmed (rounded up for discharge fees) |
| Maintenance + labor + monitoring | $1.00M | §5, estimate |
| **Total 5-yr opex** | **~$1.6M** | |

**Opex vs. capex:**
- Rack hardware capex: **~$3.5M**
- 5-yr opex: **~$1.6M** (range ~$1.1M low / ~$2.6M high)
- 5-yr total cost of ownership: **~$5.1M**
- **Recurring opex share of TCO ≈ 31%** (mid); ~25% low, ~40% high.

**Finding: at the rack level, recurring opex is roughly one-third of 5-year TCO — meaningful, but hardware capex (~69%) dominates.** Within opex, maintenance (~$1.0M) is actually the larger line, energy (~$0.56M) second, water (~$0.05M) negligible — and all three together are dwarfed by the ~$3.5M of silicon. The founder's hypothesis (energy/water = dominant lifetime cost) is **not supported**, even before the launch cost is added.

---

## 6. The orbital comparison

**What orbit avoids.** In orbit there is no utility bill and no municipal water:
- **Electricity opex → ~$0.** Power comes from solar arrays (one-time capex).
- **Water opex → ~$0.** Cooling is radiative; no evaporative make-up water. (Closed pumped-loop coolant is a one-time fill.)
- **Some opex remains:** ground-station/downlink fees, mission operations staff, station-keeping propellant, insurance, and on-orbit hardware that cannot be hand-serviced (a reliability cost, not a cash opex). Call residual orbital opex **~$0.3–0.6M over 5 yr** (ground segment + ops, allocated per rack).

**Avoided opex per rack (orbit vs. terrestrial, 5 yr, mid case):**
```
Terrestrial 5-yr opex                     ~$1.6M
Less residual orbital opex                -$0.45M
= Lifetime opex AVOIDED by going orbital  ~$1.15M  (range ~$0.7M low / ~$2.2M high)
```

**But orbit replaces opex with new capex.** Solar arrays + radiators are not free — they are bought once and launched:
- **Solar:** at ~175 kW facility-equivalent load (in orbit, no PUE cooling-overhead — radiators ARE the cooling — but power-conversion overhead remains; call it ~150–175 kW of array output needed). Modern space arrays ~200–400 W/kg; cost historically cited at **$150–800/W** ([NSS](https://nss.org/the-case-for-solar-power-from-space/)). Even at an optimistic $50–150/W for a 2028-era large array, **150 kW → $7.5M–$22M of array capex.** Mass ~0.4–0.9 t.
- **Radiators:** must reject ~135 kW of waste heat. Deployable radiators ~5–12.5 kg/kW → **~0.7–1.7 t**; cost is design-specific but easily **$5–15M** for a custom high-power deployable radiator system.
- **Combined orbital power+thermal capex: very roughly $12–35M per rack** — and it consumes launch mass (~1–2.5 t) that itself costs money to loft.

**Net comparison against the Neutron launch (~$50–55M):**
```
Avoided terrestrial opex (5 yr)            +$1.15M   (benefit)
Neutron launch cost                        -$50–55M  (cost)
Avoided opex as % of launch                 ~2–2.3%
```
Even using the **high case** ($2.2M avoided opex) it offsets only **~4%** of the launch. And that ignores the **$12–35M of orbital power/thermal capex** orbit must add — which *exceeds* the opex it saves by an order of magnitude.

**Honest read:** Avoided energy/water cost does **not** meaningfully offset the launch. It is a second-order effect — and once you account for the solar+radiator capex that orbit must buy *instead*, the "free electricity" framing is net-negative on a pure cost basis. Orbit does not save money on power; it **converts a recurring power opex (~$0.56M/5yr) into a large one-time power-and-thermal capex (~$12–35M)**. That trade only makes sense if it is bundled with reasons orbit is worth doing anyway (latency, sovereignty, no water-permitting, revenue premium, 24/7 unshaded solar in the right orbit, no grid-interconnect queue).

**The one genuine orbital opex win is non-financial:** orbit sidesteps the **water-permitting and grid-interconnection bottleneck** entirely. In 2025–26 the binding constraint on terrestrial AI build-out is not the price of power — it is *getting* power and water permits at all (multi-year interconnect queues, water-stressed-region moratoria). An orbital node needs neither. That is a *schedule/optionality* value, not a cost saving, and it belongs in the premium-value case, not the energy-cost ledger.

---

## 7. Verdict

**Energy and water are NOT the dominant lifetime cost. The founder's hypothesis is not supported.**

Pinned at the rack level, mid case:
- 5-year electricity: **~$0.56M** (16% of rack capex)
- 5-year water: **~$0.05M** (negligible in dollars)
- 5-year maintenance: **~$1.0M**
- **Total 5-year opex ~$1.6M ≈ 31% of a ~$5.1M terrestrial TCO** — real, but hardware capex (~69%) dominates.
- Against the **~$50–55M Neutron launch**, total avoided opex (~$1.15M) offsets only **~2–4%**.

**Where the truth lands:** The lifetime cost of an orbital AI node is dominated by **launch and the spacecraft hardware** (on the current ~$10–20M internal-launch basis, launch is ~45% of a ~$45M-mid node — see the superseded-basis banner above; on the retired ~$50–55M external-price basis it was ~85–90%), **then the rack hardware (~$3.5M and rising)**. Energy and water are a **third-tier line item** on every basis. Going orbital does avoid the electricity and water bills — but it must *buy and launch solar arrays and radiators instead*, and that power/thermal capex (~$12–35M) is far larger than the ~$1.2M of opex it saves. **Orbit does not win on energy economics; it roughly breaks even to net-negative on the pure power-cost trade.**

The orbital case must therefore stand on its **other** legs — revenue premium, latency, data sovereignty, and crucially the ability to **skip the grid-interconnect and water-permitting queues** that are the real 2026 bottleneck. "Free electricity in orbit" is true but financially minor; "no permitting queue" is the orbital power story actually worth telling. Recommend the synthesis **drop energy/water as a launch justifier** and re-file the water angle under regulatory/schedule advantage in `premium_value_case.md`.

---

## Sources

- [Sunbird DCIM — Is Your Data Center Ready for the NVIDIA GB200 NVL72?](https://www.sunbirddcim.com/blog/your-data-center-ready-nvidia-gb200-nvl72)
- [Sunbird DCIM — How Much Power Does a NVIDIA GB300 NVL72 Need?](https://www.sunbirddcim.com/blog/how-much-power-does-nvidia-gb300-nvl72-need)
- [Introl — GB200 NVL72 Deployment](https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled)
- [Introl — NVIDIA Vera Rubin: 600kW Racks by 2027](https://introl.com/blog/nvidia-vera-rubin-gpu-600kw-racks-2027)
- [TAAL Tech — High-Density Data Centers: Air vs. Liquid Cooling (PUE)](https://www.taaltech.com/high-density-data-centers-when-to-shift-from-air-cooling-to-liquid-cooling/)
- [Google Data Centers — Power Usage Effectiveness (fleet PUE 1.09)](https://datacenters.google/efficiency/)
- [Uptime Institute via IAEI — global average PUE ~1.58](https://iaeimagazine.org/electrical-fundamentals/how-much-electricity-does-a-data-center-use-complete-2025-analysis/)
- [Statista/EIA — U.S. industrial retail electricity price 2025 ($0.0862/kWh)](https://www.statista.com/statistics/190680/us-industrial-consumer-price-estimates-for-retail-electricity-since-1970/)
- [Site Selection Group — Power costs across the U.S.](https://info.siteselectiongroup.com/blog/power-in-the-data-center-and-its-costs-across-the-united-states)
- [Tom's Hardware — PJM 76% wholesale price spike](https://www.tomshardware.com/tech-industry/ai-data-centers-trigger-massive-irreversible-76-percent-electricity-price-spike-in-largest-us-region-federal-watchdog-demands-tech-giants-pay-for-their-own-power-infrastructure)
- [CNBC — Goldman: electricity prices keep rising on AI demand](https://www.cnbc.com/2026/02/12/electricity-price-data-center-ai-inflation-goldman.html)
- [Yale Climate Connections — data centers pay less, residential bills soar](https://yaleclimateconnections.org/2026/01/home-electricity-bills-are-skyrocketing-for-data-centers-not-so-much/)
- [EESI — Data Centers and Water Consumption (WUE)](https://www.eesi.org/articles/view/data-centers-and-water-consumption)
- [Apstech Advisors — Data Center Water Consumption in the US 2025–2030](https://apstechadvisors.com/data-center-water-consumption-in-the-us-challenges-trends-and-market-opportunities-for-2025-2030/)
- [AIRSYS — How Much Water Does a Data Center Use? (Google Mesa $6.08/1,000 gal)](https://airsysnorthamerica.com/how-much-water-does-a-data-center-use/)
- [GRESB — Cooling data centers: water use in the age of AI and ESG](https://www.gresb.com/cooling-data-centers-managing-water-use-in-the-age-of-ai-and-esg/)
- [Data Centre Magazine — NVIDIA Blackwell water efficiency](https://datacentremagazine.com/hyperscale/how-nvidia-is-boosting-water-efficiency-with-blackwell)
- [The Network Installers — Data Center Operating Costs (2026)](https://thenetworkinstallers.com/blog/data-center-operating-costs/)
- [Epoch AI — TCO of a 1-GW AI data center](https://epoch.ai/data-insights/ai-datacenter-cost-breakdown)
- [Alpha-matica — Deconstructing the data center cost structure](https://www.alpha-matica.com/post/deconstructing-the-data-center-a-look-at-the-cost-structure-1)
- [NSS — The Case for Solar Power From Space (array $/W, kg/kW)](https://nss.org/the-case-for-solar-power-from-space/)
- [Tom's Hardware — Vera Rubin NVL72 rack price up to $8.8M](https://www.tomshardware.com/tech-industry/artificial-intelligence/price-of-nvidias-vera-rubin-nvl72-racks-skyrockets-to-as-much-as-usd8-8-million-apiece-but-server-makers-margins-will-be-tight-nvidia-is-moving-closer-to-shipping-entire-full-scale-systems)

## Open questions

1. **Orbital power/thermal capex precision.** The $12–35M solar+radiator estimate is wide. A dedicated node-design costing (see `node_design/`) should pin array $/W and radiator $/kW for a 2028-era 150 kW system — this number, not the energy opex, is the real orbital power-cost story.
2. **Utilization.** 85% is assumed. Inference racks may run lower (demand-shaped) or higher (batch). A 60% vs. 95% swing moves 5-yr energy by ~$0.2M — still second-order.
3. **Maintenance in orbit.** Terrestrial maintenance (~$1.0M/5yr) is partly *avoided* in orbit (no hands-on service) but partly *replaced* by a reliability/redundancy capex penalty and ground-ops staff. Net direction is unclear; modeled as ~$0.45M residual.
4. **Rack price trajectory.** As racks rise to $7–9M (Rubin) and beyond, energy's share of TCO falls further — strengthening the conclusion that energy is not the lever.
5. **Indirect (upstream) water.** Grid power carries ~4.5 L/kWh of indirect water at the power plant. Orbit avoids this too, but it is the *utility's* cost, not the operator's — relevant only to an ESG/lifecycle narrative, not the cost ledger.
6. **Carbon pricing.** No carbon tax is modeled. A future $50–100/t CO2 price on grid power would add a modest opex line terrestrially and is a potential (small) future tailwind for the orbital case.
