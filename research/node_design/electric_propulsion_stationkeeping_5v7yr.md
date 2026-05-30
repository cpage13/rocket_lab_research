# Electric-Propulsion Station-Keeping: Mass Penalty for 5 vs 7 Years

*Project: RKLB Space Data Center, feasibility phase. Document date: 2026-05-29.*
*Author: research agent. Hard numbers cross-checked against 2+ independent sources where possible; estimates and extrapolations explicitly labeled. Confidence: medium-high on the headline result.*

---

## Summary / Verdict

**Holding a large, high-area compute node at low SSO against atmospheric drag is cheap in mass, and extending the hold from 5 to 7 years is nearly free.** For an ~8 t node (7-9 t band) at a baseline ~550 km dawn-dusk SSO, an electric-propulsion (EP) station-keeping system, thruster + power-processing unit (PPU) + feed + tank + propellant, totals roughly **140-185 kg (about 1.7-2.3% of the node)**, and the **marginal mass of the extra 2 years is only ~25-35 kg (about 0.3-0.5% of an 8 t node)**. The node's hundreds-of-kW solar array dwarfs the EP power draw (a few kW), so power is never the constraint, thrust is, and that is solved by running one or two ~1.5 kW Hall strings at low duty cycle. The whole system fits comfortably inside the **250-550 kg propulsion line already carried in `node_mass_model.md`** with room left for collision-avoidance and end-of-life disposal.

The dominant uncertainty is not the EP hardware: it is the **effective drag area** of the deployed node and the **solar-cycle phase**. Drag-makeup delta-v swings from a few m/s/yr (600 km, arrays feathered edge-on, solar minimum) to well over 100 m/s/yr (500 km, broadside, solar maximum), a ~30-50x spread. Even at the high end the propellant mass stays modest because EP's high specific impulse (1600-4100 s) makes the rocket-equation penalty almost linear at these low total delta-v values.

### Key-spec table (8 t node, baseline 550 km SSO, cycle-averaged drag budget)

| Quantity | 5-year | 7-year | Marginal (extra 2 yr) | Source basis |
|---|---|---|---|---|
| Station-keeping delta-v budget (incl. ~5 m/s/yr col-avoid margin) | ~175 m/s | ~245 m/s | ~70 m/s | computed, ASWA density model |
| Propellant, Hall Kr/Ar (Isp 1900 s) | ~76 kg | ~106 kg | **~30 kg** | rocket equation |
| Propellant, Hall hi-Isp/argon (Isp 2200 s) | ~65 kg | ~91 kg | **~26 kg** | rocket equation |
| Propellant, gridded ion Xe (Isp 3100 s) | ~46 kg | ~65 kg | **~18 kg** | rocket equation |
| EP hardware (2 strings + struct/gimbal, fixed) | ~67 kg | ~67 kg | 0 (paid once) | BHT-1500, Safran/NSTAR PPU |
| Tankage (~10% of propellant) | ~7 kg | ~11 kg | ~3 kg | ETS-VIII Xe tank class |
| **TOTAL EP system (Hall Kr/Ar)** | **~150 kg** | **~184 kg** | **~33 kg** | sum |
| **As fraction of 8 t node** | **~1.9%** | **~2.3%** | **~0.4%** | sum |

> Estimated (computed) values throughout. The 550 km / cycle-averaged 30 m/s/yr drag figure is a design midpoint, not a measured fact, see Section 1. Hardware masses are sourced flight-thruster numbers (Section 2).

### How altitude moves the answer (TOTAL EP system mass, Hall Kr/Ar @ Isp 1900 s)

| Orbit (cycle-avg drag dV) | 5-yr total | 7-yr total | Marginal 2-yr | % of 8 t (7-yr) |
|---|---|---|---|---|
| **600 km** (~15+5 m/s/yr) | ~114 kg | ~133 kg | ~19 kg | ~1.7% |
| **550 km** (~30+5 m/s/yr) | ~150 kg | ~184 kg | ~33 kg | ~2.3% |
| **500 km** (~60+5 m/s/yr) | ~222 kg | ~285 kg | ~63 kg | ~3.6% |

**Read:** even the high-drag 500 km case keeps the 7-year EP system under ~290 kg (3.6% of node) and the marginal 2-year cost under ~65 kg. The choice of 5 vs 7 years is a rounding error against the node's ~8 t mass and its ~1.3-2.7 t radiator line.

---

## 1. Drag force and required drag-makeup delta-v

### 1.1 The physics

A satellite in a circular orbit at speed `v` through air of density `ρ` feels a drag force ([Australian Space Weather Agency, *Satellite Orbital Decay Calculations*](https://www.sws.bom.gov.au/Category/Educational/Space%20Weather/Space%20Weather%20Effects/SatelliteOrbitalDecayCalculations.pdf)):

```
D = ½ · ρ · v² · A · Cd
```

where `A` is the cross-sectional (ram) area facing the flow and `Cd` is the drag coefficient. For LEO satellites a **drag coefficient Cd ≈ 2.2** is the long-standing standard for compact shapes ([ScienceDirect, ballistic-coefficient review](https://www.sciencedirect.com/science/article/abs/pii/S0273117723001138); [arXiv 2508.19549, orbital-decay modeling](https://arxiv.org/html/2508.19549v1)). To hold altitude, the thruster must supply an equal and opposite impulse continuously; the **drag-makeup delta-v per year** is the drag acceleration integrated over a year:

```
ΔV_yr = (D / m_sat) · t_year = ½ · ρ · v² · Cd / (m/A) · t_year
```

The single governing ratio is **(m/A)**, the mass-to-area ratio (its inverse times Cd is the ballistic coefficient). A node with big solar arrays and radiators has a **low m/A**, exactly the "high drag for its mass" regime flagged in `orbits_environment.md` and `orbit_types_primer.md` ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0273117723001138)).

### 1.2 Atmospheric density at 500-600 km

Density is the largest lever and it varies by ~2 orders of magnitude across the 11-year solar cycle at these altitudes ([ScienceDirect, atmospheric-density overview](https://www.sciencedirect.com/topics/physics-and-astronomy/atmospheric-density); [Wiley, future thermospheric density](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021JD034589)). I use the empirical [Australian Space Weather Agency (ASWA) model](https://www.spaceacademy.net.au/watch/debris/atmosmod.htm) (valid 180-500 km; extended to 600 km with a caveat):

```
T   = 900 + 2.5·(F10.7 − 70) + 1.5·Ap          [K]
m   = 27 − 0.012·(h − 200)                      [molecular-mass proxy], h in km
H   = T / m                                     [km, scale height]
ρ   = 6×10⁻¹⁰ · exp(−(h − 175)/H)               [kg/m³]
```

Computed densities (this analysis):

| Altitude | Solar min (F10.7=70) | Solar mean (F10.7=150) | Solar max (F10.7=230) |
|---|---|---|---|
| 400 km | 1.3×10⁻¹² | 4.2×10⁻¹² | 9.1×10⁻¹² |
| 500 km | 1.3×10⁻¹³ | 6.5×10⁻¹³ | 1.9×10⁻¹² |
| 550 km* | 4.5×10⁻¹⁴ | 2.8×10⁻¹³ | 9.3×10⁻¹³ |
| 600 km* | 1.7×10⁻¹⁴ | 1.3×10⁻¹³ | 4.8×10⁻¹³ |

\* 550-600 km extrapolated beyond the model's stated 500 km validity ceiling; treat as order-of-magnitude. Units kg/m³.

**Independent cross-check:** literature places 500 km solar-maximum density at **~2.4×10⁻¹² to 5.7×10⁻¹² kg/m³** ([arXiv 2508.19549](https://arxiv.org/html/2508.19549v1)) and 400 km mean density at **~4×10⁻¹³ to 4×10⁻¹² kg/m³** ([ScienceDirect overview](https://www.sciencedirect.com/topics/physics-and-astronomy/atmospheric-density)). My 500 km solar-max value (1.9×10⁻¹²) sits just below that band, i.e. the ASWA model is **mildly conservative-low at solar max**, so the drag delta-v figures below if anything understate the solar-max peak slightly; the design margins absorb this. Solar-max-vs-min density ratio of ~15x at 500 km is consistent with the literature's "~2 orders of magnitude over 500-800 km" ([ScienceDirect overview](https://www.sciencedirect.com/topics/physics-and-astronomy/atmospheric-density)).

### 1.3 Drag-makeup delta-v per year (computed)

Circular velocity: 7.61 km/s @ 500 km, 7.59 @ 550, 7.56 @ 600 (from `√(μ/r)`, μ=3.986×10¹⁴). For an **8 t node**, bracketing the **effective drag area** (the deployed solar ~500-900 m² and radiator ~300 m² are not all broadside at once; in dawn-dusk SSO arrays can be feathered closer to edge-on):

| Altitude | A_eff | m/A (kg/m²) | Solar min | Solar mean | Solar max |
|---|---|---|---|---|---|
| **500 km** | 100 m² (edge-on) | 80 | 3 | 17 | 48 |
| | 300 m² (partial) | 27 | 10 | 49 | **144** |
| | 600 m² (broadside) | 13 | 19 | 99 | 288 |
| | 900 m² (flat-on) | 9 | 29 | 148 | 432 |
| **550 km** | 300 m² (partial) | 27 | 3 | 21 | 70 |
| **600 km** | 300 m² (partial) | 27 | 1 | 9 | 36 |

Values are ΔV in **m/s per year**, Cd=2.2.

**Reading the table:**
- **Altitude matters enormously:** moving 500 to 600 km cuts drag delta-v ~4x (density drops ~4x).
- **Solar cycle matters ~15x:** solar max vs min at fixed altitude/area.
- **Effective area (attitude/feathering) matters ~9x** across the bracket.
- **Cross-check against a real mission class:** a *compact* satellite (high m/A) at 400-500 km needs **<25 m/s/yr** for drag makeup ([Ray, AMOS 2022, *Impact of space weather on VLEO satellites*](https://amostech.com/TechnicalPapers/2022/Atmospherics_Space-Weather/Ray.pdf), as indexed). Our high-area node has a much lower m/A, so it lands higher, consistent with the table's tens-of-m/s/yr "partial exposure" rows. For Starlink at 550 km, drag makeup via electric propulsion is explicitly noted as a dominant delta-v line that justifies high-Isp EP ([arXiv 1807.08109](https://arxiv.org/pdf/1807.08109); [Wikipedia, Starlink](https://en.wikipedia.org/wiki/Starlink)).

**Design budget adopted (cycle-averaged):** a real mission averages propellant use across the solar cycle while sizing the *thruster* for the solar-max peak. For the 550 km baseline with active area management I adopt a **cycle-averaged ~30 m/s/yr** drag budget (peaks ~70 at solar max), and bracket with **~60 m/s/yr @ 500 km** and **~15 m/s/yr @ 600 km**. I add **~5 m/s/yr** for collision-avoidance maneuvers and momentum management. These are clearly labeled estimates that fold the table above into a single planning number.

---

## 2. EP options: Hall vs gridded ion

Both Hall-effect thrusters (HETs) and gridded ion engines are flight-proven for LEO/GEO station-keeping. Sourced specifications:

| Thruster | Type | Isp (s) | Thrust (mN) | Power (kW) | Thruster mass | PPU mass | Propellant | Source |
|---|---|---|---|---|---|---|---|---|
| **Busek BHT-1500** | Hall | 1710 (Xe), +140-190 (Kr) | 101 nom (68-179) | 1.5 (1.0-2.7) | **6.3 kg** (+0.3 cathode) | n/a on sheet | Xe / Kr / I | [Busek BHT-1500 datasheet](https://www.busek.com/bht1500); [SatCatalog PDF](https://satcatalog.s3.amazonaws.com/components/941/SatCatalog_-_Busek_-_BHT-1500_-_Datasheet.pdf?lastmod=20211014052542) |
| **SPT-100** | Hall | 1600 | 83 | 1.35 | ~5 kg | ~10.4 kg (PPU+TSU) | Xe | [Wikipedia, Hall-effect thruster](https://en.wikipedia.org/wiki/Hall-effect_thruster); [Safran/Alcatel PPU](https://electricrocket.org/IEPC/0067-0303iepc-full.pdf) |
| **PPS-1350** | Hall | ~1660 | 88 | 1.5 | ~5.3 kg | ~10.4-10.9 kg | Xe | [Wikipedia, PPS-1350](https://en.wikipedia.org/wiki/PPS-1350); [Safran](https://www.safran-group.com/products-services/ppsr1350-stationary-plasma-thruster) |
| **XR-5 / BPT-4000** | Hall | up to ~2200 | ~250-290 | 4.5 | **12.3 kg** (+cathode) | ~0.36 kW/kg class | Xe | [SatCatalog XR-5](https://www.satcatalog.com/component/xr-5-hall-thruster/); [Aerojet 30-yr EP review](https://electricrocket.org/IEPC/7vc5f5xg.pdf) |
| **Starlink V1/V1.5** | Hall | ~1500-1600 | ~60 | ~1-2 | (proprietary) | (proprietary) | Krypton | [Wikipedia, Starlink](https://en.wikipedia.org/wiki/Starlink) |
| **Starlink V2-mini** | Hall | up to ~2200 | ~170 | (higher) | (proprietary) | (proprietary) | Argon | [Wikipedia, Starlink](https://en.wikipedia.org/wiki/Starlink) |
| **NSTAR** | Gridded ion | 1900-3100 | 19-92 | 0.5-2.3 | **8.2 kg** | **14.77 kg** (+DCIU 2.51 kg) | Xe | [NASA GRC, NSTAR](https://www.grc.nasa.gov/www/ion/past/90s/nstar.htm); [JPL DS1 IPS report](https://pdssbn.astro.umd.edu/holdings/ds1-c-micas-3-rdr-visccd-borrelly-v1.0/document/doc_Apr04/int_reports/IPS_Integrated_Report.pdf) |
| **T6 (QinetiQ)** | Gridded ion | 4120-4300 | 143 | 4.5 | ~ (heavier) | (heavier) | Xe | [NASA NTRS, T6 evaluation](https://ntrs.nasa.gov/citations/20150008918) |

**Hall vs gridded ion, for this job:**
- **Hall (HET):** moderate Isp (1600-2200 s), higher thrust-to-power, simpler/lighter PPU, lower cost. Best fit for LEO drag makeup where modest thrust at low duty cycle is fine and propellant mass is already small. Krypton and argon (Starlink's choices) trade ~5-8% efficiency for far cheaper propellant: argon is ~100x cheaper than krypton and ~1000x cheaper than xenon ([Wikipedia, Starlink](https://en.wikipedia.org/wiki/Starlink); [Busek BHT-1500 krypton results, IEPC 2017](https://electricrocket.org/IEPC/IEPC_2017_26.pdf)).
- **Gridded ion:** higher Isp (3100-4300 s) cuts propellant ~30-50% vs Hall, but the PPU is heavier and more complex and thrust-to-power is lower. Worth it only if propellant mass (not hardware) dominates, which it does *not* here at the 5-7 yr / tens-of-m/s/yr scale. For a deep-throttling, ultra-low-thrust drag-cancellation role, GOCE famously used gridded ion at 1-20 mN ([ESA, GOCE drag-free](https://www.esa.int/Applications/Observing_the_Earth/FutureEO/GOCE/GOCE_achieves_drag-free_perfection)).

**PPU mass / power density:** a flight 1.5 kW Hall PPU (with thruster-switching unit) masses **~10.4-10.9 kg**, i.e. ~0.14 kW/kg at the unit level ([Safran/Alcatel PPU, IEPC](https://electricrocket.org/IEPC/0067-0303iepc-full.pdf)). Current commercial flight PPUs sit near **~0.36 kW/kg**; Busek is developing a GaN-based PPU targeting **~1 kW/kg** at >97% efficiency ([NASA SBIR, Busek GaN PPU](https://sbir.gsfc.nasa.gov/SBIR/abstracts/18/sbir/phase1/SBIR-18-1-S3.03-1064.html)). I size with present-day ~10-11 kg/string PPUs (conservative).

**Power budget confirmation (the node has abundant power):** one 1.5 kW Hall string draws ~1.8 kW including PPU losses; two strings ~3.6 kW; a 4.5 kW XR-5 or T6 ~5 kW. Against the node's **~200-250 kW array** (`node_mass_model.md` §3), EP draws **~1.5-2.5% of available power**. Power is a non-issue. The real limiter is **thrust**: at 2×100 mN on an 8 t node the acceleration is ~0.025 mm/s², so making up ~35 m/s/yr needs ~16 days of thrusting per year, a **~4% duty cycle**. Entirely feasible, and there is ample power headroom to run more strings or throttle up during solar-max peaks.

---

## 3. Propellant mass for 5 vs 7 years (rocket equation, work shown)

Propellant follows the Tsiolkovsky rocket equation. With exhaust velocity `ve = Isp · g₀` (g₀ = 9.80665 m/s²) and node dry mass `m_dry`:

```
m_prop = m_dry · ( exp(ΔV_total / ve) − 1 )
ΔV_total = (drag dV/yr + margin) · years
```

Worked example, **550 km baseline, Hall Kr/Ar Isp 1900 s, 8 t node, 35 m/s/yr**:
- ve = 1900 × 9.80665 = **18 633 m/s**
- 5-yr: ΔV = 35 × 5 = 175 m/s → m_prop = 8000 × (e^(175/18633) − 1) = 8000 × (e^0.00939 − 1) = **~75.5 kg**
- 7-yr: ΔV = 35 × 7 = 245 m/s → m_prop = 8000 × (e^(245/18633) − 1) = 8000 × (e^0.01315 − 1) = **~105.9 kg**
- **Marginal 2-yr propellant = ~30.4 kg**

Because ΔV/ve is small (~0.01-0.025), `exp(x) ≈ 1 + x`, so **propellant scales almost linearly with years** and the rocket-equation curvature is negligible. Full results:

| Orbit (dV/yr incl. margin) | EP option (Isp) | Prop 5-yr | Prop 7-yr | **Marginal 2-yr** |
|---|---|---|---|---|
| **550 km (35)** | Hall Xe (1600) | 89.7 kg | 125.9 kg | 36.2 kg |
| | Hall Kr/Ar (1900) | 75.5 kg | 105.9 kg | **30.4 kg** |
| | Hall hi-Isp/argon (2200) | 65.2 kg | 91.4 kg | 26.2 kg |
| | Gridded ion Xe (3100) | 46.2 kg | 64.7 kg | 18.5 kg |
| | Gridded ion T6 (4100) | 34.9 kg | 48.9 kg | 14.0 kg |
| **500 km (65)** | Hall Kr/Ar (1900) | 140.8 kg | 197.8 kg | **57.0 kg** |
| | Gridded ion Xe (3100) | 86.0 kg | 120.6 kg | 34.7 kg |
| **600 km (20)** | Hall Kr/Ar (1900) | 43.1 kg | 60.3 kg | **17.3 kg** |
| | Gridded ion Xe (3100) | 26.4 kg | 36.9 kg | 10.6 kg |

Krypton/argon vs xenon: same Isp band, the propellant *mass* is nearly identical (Isp is what matters for mass); the win from Kr/Ar is **cost and supply**, not mass ([Wikipedia, Starlink](https://en.wikipedia.org/wiki/Starlink); [Busek krypton results](https://electricrocket.org/IEPC/IEPC_2017_26.pdf)).

---

## 4. Total added mass and the marginal cost of 2 extra years

**Fixed EP hardware (paid once, independent of mission length):**

| Item | Mass | Basis |
|---|---|---|
| Thruster head ×2 (1.5 kW Hall class) | ~14 kg | BHT-1500 6.3 kg each |
| PPU ×2 | ~22 kg | Safran/NSTAR-class ~10-11 kg each |
| DCIU / filter / cabling ×2 | ~6 kg | NSTAR DCIU 2.51 kg |
| Feed system, flow control, valves ×2 | ~10 kg | feed-system estimate |
| Structure, gimbals, hold-downs | ~15 kg | estimate |
| **Total fixed hardware** | **~67 kg** | sum |

Two strings give redundancy and let thrust scale at solar max. Tankage is taken at **~10% of propellant mass** (xenon/krypton COPV; the ETS-VIII flight xenon tank was ~30 kg for a large xenon load, and high-pressure Xe COPVs run ~8-15% tank fraction, [ETS-VIII xenon tank, ResearchGate](https://www.researchgate.net/publication/269237920_Design_and_manufacture_of_the_ETS_VIII_xenon_tank); [RSC, adsorbed-xenon storage tankage](https://pubs.rsc.org/en/content/articlehtml/2021/ma/d1ma00167a)).

**Total EP system = fixed hardware + propellant + tank:**

| Orbit | EP option | 5-yr total | 7-yr total | **Marginal 2-yr (prop+tank)** | 7-yr as % of 8 t |
|---|---|---|---|---|---|
| **550 km** | Hall Kr/Ar (1900 s) | **~150 kg** | **~184 kg** | **~33 kg (0.42%)** | 2.3% |
| | Hall hi-Isp/argon (2200 s) | ~139 kg | ~168 kg | ~29 kg (0.36%) | 2.1% |
| | Gridded ion Xe (3100 s) | ~118 kg | ~138 kg | ~20 kg (0.26%) | 1.7% |
| **500 km** | Hall Kr/Ar (1900 s) | ~222 kg | ~285 kg | ~63 kg (0.78%) | 3.6% |
| | Gridded ion Xe (3100 s) | ~162 kg | ~200 kg | ~38 kg (0.48%) | 2.5% |
| **600 km** | Hall Kr/Ar (1900 s) | ~114 kg | ~133 kg | ~19 kg (0.24%) | 1.7% |
| | Gridded ion Xe (3100 s) | ~96 kg | ~108 kg | ~12 kg (0.15%) | 1.3% |

### The headline answers

1. **Total added mass for station-keeping** (baseline 550 km, 8 t node, Hall Kr/Ar): **~150 kg for 5 years, ~184 kg for 7 years.** As a fraction of a 7-9 t node: **~1.7-2.6% (5-yr), ~2.0-3.0% (7-yr)** across the 7-9 t range.
2. **Marginal mass for the extra 2 years: ~25-35 kg at 550 km baseline (~0.3-0.5% of an 8 t node).** Even in the high-drag 500 km case it is ~40-65 kg (~0.5-0.8%); in the low-drag 600 km case ~12-19 kg (~0.2%).
3. **Why so cheap:** the fixed thruster+PPU hardware (~67 kg) is paid once and dominates the 5-year number; additional years add only propellant, which scales almost linearly (rocket-equation curvature negligible at these low delta-v) and benefits from EP's high Isp. Going 5→7 years is **~+22% on the EP system mass** but only **~+0.4% on the node mass**.

### Reconciliation with `node_mass_model.md`

The node mass model carries a **propulsion / station-keeping line of 250-500 kg (1-rack)** and explicitly flags LEO drag makeup at 500-600 km on a multi-hundred-m² array as uncertain (§6, Open Question 7). This analysis **lands inside that envelope**: the full 7-year EP system is ~133-285 kg depending on altitude, leaving headroom within the 250-500 kg line for collision-avoidance propellant and an end-of-life deorbit budget (the 5-year disposal rule, `orbits_environment.md` §5). The model's 250-550 kg allocation is **confirmed as adequate, even generous**, for station-keeping alone. The 5-vs-7-year choice does not stress the mass budget.

---

## Sources

Atmosphere, drag, decay:
- [Australian Space Weather Agency, *Satellite Orbital Decay Calculations* (Kennewell)](https://www.sws.bom.gov.au/Category/Educational/Space%20Weather/Space%20Weather%20Effects/SatelliteOrbitalDecayCalculations.pdf) - density model, drag equation, Cd≈2, worked decay
- [Space Academy AU, *Earth Atmosphere Density Approximations*](https://www.spaceacademy.net.au/watch/debris/atmosmod.htm) - same density model, exospheric-temperature scenarios
- [arXiv 2508.19549, *Modeling Orbital Decay of LEO Satellites*](https://arxiv.org/html/2508.19549v1) - Cd=2.2, 500 km solar-max density ~2.4-5.7×10⁻¹²
- [ScienceDirect, *Atmospheric Density* overview](https://www.sciencedirect.com/topics/physics-and-astronomy/atmospheric-density) - 400 km density, solar-cycle variation
- [Wiley JGR, *Future Decreases in Thermospheric Neutral Density*](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021JD034589) - thermospheric density and solar activity
- [ScienceDirect, ballistic-coefficient estimation in LEO](https://www.sciencedirect.com/science/article/abs/pii/S0273117723001138) - ballistic coefficient, Cd=2.2, area-to-mass
- [Ray, AMOS 2022, *Impact of space weather on VLEO satellites*](https://amostech.com/TechnicalPapers/2022/Atmospherics_Space-Weather/Ray.pdf) - drag dV <25 m/s/yr at 400-500 km (compact sat)
- [arXiv 1807.08109, LEO constellation station-keeping](https://arxiv.org/pdf/1807.08109) - drag makeup as dominant EP delta-v
- [ESA, *GOCE achieves drag-free perfection*](https://www.esa.int/Applications/Observing_the_Earth/FutureEO/GOCE/GOCE_achieves_drag-free_perfection) - gridded ion 1-20 mN drag cancellation

Electric propulsion hardware:
- [Busek BHT-1500 product page](https://www.busek.com/bht1500) and [datasheet PDF](https://satcatalog.s3.amazonaws.com/components/941/SatCatalog_-_Busek_-_BHT-1500_-_Datasheet.pdf?lastmod=20211014052542) - 6.3 kg thruster, 101 mN, 1710 s, throttle table
- [Busek BHT-1500 krypton characterization, IEPC 2017](https://electricrocket.org/IEPC/IEPC_2017_26.pdf) - krypton +140-190 s Isp, −7-8% efficiency
- [Wikipedia, Hall-effect thruster](https://en.wikipedia.org/wiki/Hall-effect_thruster) - SPT-100 83 mN / 1600 s
- [Safran PPS-1350](https://www.safran-group.com/products-services/ppsr1350-stationary-plasma-thruster) and [Wikipedia, PPS-1350](https://en.wikipedia.org/wiki/PPS-1350) - 88 mN, 1.5 kW
- [Safran/Alcatel high-power PPU, IEPC](https://electricrocket.org/IEPC/0067-0303iepc-full.pdf) - 1.5-1.6 kW PPU+TSU ~10.4-10.9 kg
- [SatCatalog XR-5 Hall thruster](https://www.satcatalog.com/component/xr-5-hall-thruster/) and [Aerojet 30-yr EP flight review](https://electricrocket.org/IEPC/7vc5f5xg.pdf) - 12.3 kg, 4.5 kW, ~2200 s
- [NASA GRC, NSTAR ion thruster](https://www.grc.nasa.gov/www/ion/past/90s/nstar.htm) - 19-92 mN, 1900-3100 s, 0.5-2.3 kW
- [JPL Deep Space 1 IPS integrated report](https://pdssbn.astro.umd.edu/holdings/ds1-c-micas-3-rdr-visccd-borrelly-v1.0/document/doc_Apr04/int_reports/IPS_Integrated_Report.pdf) - NSTAR thruster 8.2 kg, PPU 14.77 kg, DCIU 2.51 kg
- [NASA NTRS, T6 ion engine evaluation](https://ntrs.nasa.gov/citations/20150008918) - 143 mN, 4120-4300 s, 4.5 kW, 64% eff
- [NASA SBIR, Busek GaN PPU](https://sbir.gsfc.nasa.gov/SBIR/abstracts/18/sbir/phase1/SBIR-18-1-S3.03-1064.html) - target 1 kW/kg, present commercial ~0.36 kW/kg
- [Wikipedia, Starlink](https://en.wikipedia.org/wiki/Starlink) - krypton then argon Hall thrusters, Isp/thrust, propellant cost
- [ResearchGate, ETS-VIII xenon tank design](https://www.researchgate.net/publication/269237920_Design_and_manufacture_of_the_ETS_VIII_xenon_tank) - flight xenon tank class
- [RSC Materials Advances, adsorbed-xenon storage tankage](https://pubs.rsc.org/en/content/articlehtml/2021/ma/d1ma00167a) - xenon stored at 75-300 bar, tankage fraction

Project baseline (read, not modified):
- `research/orbital/orbits_environment.md`, `research/orbital/orbit_types_primer.md`, `research/node_design/node_mass_model.md`

---

## Open questions / uncertainties

1. **Effective drag area is the biggest unknown.** The deployed node has ~500-900 m² solar + ~300 m² radiator, but the *ram* area depends on attitude and feathering. In dawn-dusk SSO the arrays track a nearly fixed Sun, so the broadside-to-velocity area can be partially controlled, but it is not yet modeled. The drag delta-v (hence propellant) spans ~9x across the area bracket. **A proper deployed-geometry + attitude model is needed to collapse the 100-900 m² range to a design value.** This is the same open item flagged in `orbits_environment.md` and `node_mass_model.md` (Open Q7).
2. **Density model extrapolated above 500 km.** The ASWA model is validated to 500 km; the 550-600 km densities are extrapolations. They cross-check to literature order-of-magnitude but a NRLMSIS-2.0 / DTM-2020 run for the exact orbit and epoch would firm them up, especially the solar-max peak the thruster must be sized for.
3. **Solar-cycle phasing vs mission window.** A node launched into a rising solar cycle sees a worse 5-7 year average than one launched at solar max declining. The cycle-averaged 30 m/s/yr (550 km) is a mid value; worst-case launch timing could roughly double the average. Sizing for the solar-max *peak* (thruster) is separate from sizing propellant for the mission *average*.
4. **Thruster lifetime / total impulse.** The BHT-1500 predicted total impulse is >6.5 MN-s. A 7-year, ~106 kg-propellant Kr/Ar mission at 1900 s delivers ~2.0 MN-s, well within one thruster's life, but throttle hours, cycling, and erosion over 7 years (plus collision-avoidance burns) should be checked against qualified life, and the 2-string redundancy assumed here defends against a single-thruster wear-out.
5. **Tank fraction for krypton/argon vs xenon.** Krypton and argon are less dense than xenon and need larger or higher-pressure tanks for the same mass; the flat ~10% tank factor (xenon-derived) may understate Kr/Ar tankage by a few kg. Minor at this scale but worth refining if argon (Starlink-style) is selected for cost.
6. **Collision-avoidance and deorbit delta-v are folded in only coarsely** (~5 m/s/yr margin). The end-of-life disposal burn (5-year rule) is a separate, larger one-time delta-v at 600 km (natural decay may not suffice from 600 km within 5 years); that belongs in a dedicated disposal-budget analysis, not this station-keeping doc.
