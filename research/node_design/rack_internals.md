# AI Rack Internals — Component & Mass Breakdown, and the Optical-Interconnect Mass Lever

*Project: RKLB Space Data Center — feasibility phase. Document date: May 2026.*
*Author: research agent. Hard numbers cross-checked against ≥2 sources where possible; estimates explicitly labeled and reasoned transparently.*

---

## Summary

This document opens up an NVL72-class AI rack — the ~1.36 t terrestrial unit the project baselines as its orbital compute payload — and asks what is physically inside it, how the ~1.36 t splits across components, and how much of that mass is copper interconnect that a shift to optics could remove.

**Headline findings:**

- An NVL72-class rack is **~1.36 t (3,000 lb)** fully populated. It contains **18 compute trays + 9 NVLink switch trays + 6–8 power shelves + a DC busbar + the NVLink spine/backplane + liquid-cooling manifolds and cold plates + the chassis/frame** ([The Register](https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/), [NVIDIA DGX GB user guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)).
- **Compute trays dominate mass** — roughly **half the rack (~600–720 kg)**. Power + cooling + structure together are most of the rest. Interconnect (NVLink spine + switch trays) is **~15–22%**.
- **The NVLink scale-up backplane uses ~2 miles (3.2 km) of copper across ~5,000–5,184 cables**, packed into **4 spine cartridges** ([The Register](https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/), [Continuum Labs](https://training.continuumlabs.ai/infrastructure/servers-and-chips/nvidia-gb200-nvl72)). NVIDIA does **not** publish the spine's mass. **Engineering estimate (this doc): ~70–110 kg of cable + connector hardware in the spine, of which ~25–45 kg is copper conductor.** Flagged as estimate — see §3.
- **Optical interconnect is the real mass lever, but a modest one.** Replacing the copper NVLink spine with co-packaged optics (CPO) / optical NVLink would plausibly remove **~50–90 kg** from the rack (the cable bundle, most spine-cartridge hardware, and some structural reinforcement that exists *only* to carry the copper). That is **~4–7% of rack mass** — real, but not transformational. NVIDIA's roadmap keeps copper *inside* the rack through Rubin/NVL144 (2026–27) and only offers optical NVLink from the **Feynman generation, ~2028** ([The Register, Apr 2026](https://www.theregister.com/2026/04/05/nvidia_optical_scale_up/), [Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date)).
- **Implication for the orbital node:** an optical-interconnect rack saves ~50–90 kg of rack mass *and* ~20 kW of interconnect power — and the power saving is the bigger prize for a space node, because ~20 kW less heat means less radiator and less solar. The direct rack-mass saving is small against Neutron's ~8.5 t budget; the *indirect* saving via reduced thermal/power load is more significant. See §5.

**Confidence: medium-low on absolute component masses (NVIDIA publishes no per-component mass breakdown — almost every line below is a reasoned estimate), medium-high on the architecture inventory and the copper-cable count/length, medium on the optical-saving magnitude.**

---

## 1. Component inventory of an NVL72-class rack

The NVL72 (GB200 and the GB300/"Blackwell Ultra" refresh) is a *rack-scale* product: NVIDIA defines the whole 19-inch cabinet as the unit. Confirmed contents ([NVIDIA DGX GB user guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html), [The Register](https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/), [Supermicro 48U datasheet](https://www.supermicro.com/datasheet/datasheet_SuperCluster_GB200_NVL72.pdf), [NVIDIA OCP contribution blog](https://developer.nvidia.com/blog/nvidia-contributes-nvidia-gb200-nvl72-designs-to-open-compute-project/)):

| Subsystem | Quantity | Function | Notes |
|---|---|---|---|
| **Compute trays** | **18** × 1U | Each holds 2 Grace-Blackwell superchips (2 CPU + 4 GPU per tray) → 72 GPUs total | Holds the GPUs, CPUs, HBM, board-level VRMs, NICs, local cold plates. Heaviest line item. |
| **NVLink switch trays** | **9** × 1U | Each holds 2 NVLink-switch ASICs; forms the scale-up fabric switching layer | Sit centrally between the two banks of compute trays so copper reach is minimized. |
| **NVLink spine / backplane** | **1** assembly, **4 cartridges** | Blind-mate passive copper cable backplane connecting all 18 compute + 9 switch trays | ~5,000–5,184 copper cables, ~2 miles / 3.2 km total. The "copper-heavy" item. See §3. |
| **Power shelves** | **6 or 8** | AC→~50 V DC conversion; each ~33 kW (six 5.5 kW PSUs, N+N redundant) | GB300 commonly 8 shelves; GB200 6. |
| **DC busbar** | **1** | Distributes ~50 V DC down the rear of the rack to all trays | Hyperscale-style solid copper/aluminum busbar, ~2.5 kA class. |
| **Liquid-cooling manifolds** | **1 set** (rack vertical supply/return) | Carry coolant up/down the rack to each tray | ~90% of heat removed by liquid in terrestrial config. |
| **Cold plates** | ~hundreds | On every GPU, CPU, and (in space mod) other hot parts | Copper or copper/aluminum; integral to trays + switch trays. |
| **Chassis / frame** | **1** | EIA-310 19-inch cabinet, 48U; structural rails, side panels, doors | Includes **>100 lb (~45 kg) of added steel reinforcement** specifically to handle component mass and ~6,000 lb blind-mate mating forces ([Spheron](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)). |
| Manifold/CDU interface, cabling (power whips, mgmt), castors, misc | — | — | CDU itself is often a separate rack terrestrially; here folded into "cooling/plumbing". |

Physical: ~600 mm W × ~1200 mm D × ~2300 mm H, 48U, **~1.36 t** ([The Register](https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/), [Supermicro](https://www.supermicro.com/en/products/system/gpu/48u/srs-gb200-nvl72)). Power ~120 kW (GB200) to ~135 kW TDP (GB300).

---

## 2. Mass breakdown — where the ~1.36 t goes

**Important caveat:** NVIDIA and its integrators (Supermicro, Lenovo, GIGABYTE, HPE) publish the **rack total (~1.36 t)** but **not a per-component mass breakdown**. The table below is a **reasoned engineering estimate** built from: (a) the confirmed total, (b) component counts, (c) known sub-facts (>100 lb steel reinforcement; 2 miles of copper; 6–8 power shelves), and (d) general server-hardware density knowledge. Treat every line except the total as an estimate with ~±30% uncertainty.

| Component group | Est. mass (kg) | % of rack | Basis / reasoning |
|---|---|---|---|
| **Compute trays** (18×) | **600 – 720** | **~45–53%** | The dense part: 72 GPUs + 36 CPUs + HBM stacks + heavy multi-layer boards + per-tray VRMs, NICs, local cold plates and heatsinks. A loaded GB-class 1U compute tray is plausibly ~33–40 kg each → 18× ≈ 600–720 kg. Single largest group. |
| **NVLink switch trays** (9×) | **130 – 190** | **~10–14%** | 9 trays, each 2 switch ASICs + boards + cold plates; lighter than compute trays but not trivial. ~15–21 kg each. |
| **NVLink spine / copper backplane** (4 cartridges) | **70 – 110** | **~5–8%** | The copper interconnect — see §3 for the derivation. ~25–45 kg copper conductor + insulation, shielding, ~10,000 connector terminations, and the cartridge structure. |
| **Power shelves** (6–8×) | **130 – 200** | **~10–15%** | Each shelf holds six 5.5 kW PSUs + sheet-metal enclosure; a 5.5 kW PSU is ~2–3 kg, a populated shelf ~18–28 kg → 6–8 shelves ≈ 130–200 kg. |
| **DC busbar + power cabling** | **40 – 70** | **~3–5%** | Solid ~2.5 kA-class copper/aluminum busbar running the rack height, plus power whips. Copper-dense per unit length but short. |
| **Liquid-cooling manifolds + cold plates + coolant** | **120 – 200** | **~9–15%** | Rack vertical supply/return manifolds, in-rack hoses/quick-disconnects, hundreds of copper cold plates (cold plates also counted partly within trays), plus resident coolant. |
| **Chassis / frame / reinforcement / panels** | **150 – 230** | **~11–17%** | EIA-310 48U cabinet + rails + doors/panels + the **>100 lb (~45 kg)** of extra steel reinforcement ([Spheron](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)). |
| **Misc** (mgmt cabling, labels, castors, fasteners) | **20 – 50** | ~2–4% | — |
| **TOTAL (anchored to published figure)** | **~1,360** | 100% | [The Register](https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/), [Sunbird DCIM](https://www.sunbirddcim.com/blog/how-much-power-does-nvidia-gb300-nvl72-need) |

**Rolled-up view (mid-point of each range, normalized to 1,360 kg):**

| Functional category | Approx. mass | Approx. share |
|---|---|---|
| **Compute** (compute trays) | ~660 kg | **~49%** |
| **Interconnect** (NVLink switch trays + copper spine) | ~250 kg | **~18%** |
| **Power** (shelves + busbar + power cabling) | ~210 kg | **~15%** |
| **Cooling** (manifolds + cold plates + coolant) | ~150 kg | **~11%** |
| **Structure** (chassis, frame, reinforcement, misc) | ~190 kg | **~14%** |

(Shares sum slightly over 100% before normalization; cold plates straddle "compute" and "cooling". The robust takeaways: **compute ≈ half; interconnect ≈ a fifth; power/cooling/structure split most of the rest.**)

---

## 3. The copper / cabling mass specifically

This is the section the brief most wants pinned down.

### What's confirmed

- The NVLink **scale-up** fabric (the in-rack, all-to-all GPU interconnect — *not* the rack power wiring) is a **passive copper cable backplane**, the "**NVLink spine**".
- It carries **"more than 2 miles (3.2 km) of copper cabling"** ([The Register](https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/), repeated across [Continuum Labs](https://training.continuumlabs.ai/infrastructure/servers-and-chips/nvidia-gb200-nvl72), [Fibermall](https://www.fibermall.com/blog/nvidia-gb200-interconnect-architecture.htm)).
- The cable count is given as **~5,000** ([The Register](https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/)) or more precisely **5,184 cables** ([Fibermall](https://www.fibermall.com/blog/nvidia-gb200-interconnect-architecture.htm), [SemiAnalysis](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)).
- They are packed into **4 vertical NVLink spine cartridges** with blind-mate, high-density connectors (Amphenol Paladin / "ExaMAX"-class, 224 Gbps lanes).
- Copper was chosen *over* optics specifically to **avoid ~20 kW of transceiver/retimer power** ([The Register](https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/)).
- The rack frame was given **>100 lb (~45 kg) of extra steel reinforcement** partly to carry this cabling and the blind-mate mating loads ([Spheron](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)).

### What is NOT published

**NVIDIA does not publish the mass of the NVLink spine or its copper.** No source located gives a kilogram figure for the spine cartridge. The eBay listings for OEM spine cartridges do not state mass. So the number below is a **transparent engineering estimate**, not a sourced fact.

### Estimate — copper mass in the NVLink spine

Method: estimate from cable physical properties.

- **Total cable length:** ~3.2 km, across ~5,184 cables → average ~0.6 m per cable (consistent with a ~2.3 m rack and central switch placement).
- **Cable type:** high-speed shielded twinaxial ("twinax") pairs for 224 Gbps-class lanes. Each NVLink cable is a thin shielded twinax assembly. A single twinax pair of this class has fine-gauge conductors (~30–34 AWG copper).
- **Copper conductor mass:** 30 AWG copper ≈ 0.057 g/m per conductor; 34 AWG ≈ 0.022 g/m. A twinax cable has 2 signal conductors plus a drain wire ≈ ~3 conductor-equivalents. Take ~0.05–0.12 g/m of *copper* per cable (heavier end allows for slightly larger gauge and the foil/braid shield, which is also copper or copper-coated).
  - 3,200 m total cable run × ~3 conductors-equiv... better to work per total length: total conductor length ≈ 3.2 km × ~3 = ~9.6 km of conductor. At ~0.04 g/m fine copper → **~0.4 kg** (clearly too low — this counts only signal wire).
  - More realistically, **the dominant copper mass is the shielding** (foil + braid wrap each cable) plus drain wires. Shielded twinax of this class masses roughly **8–20 g per meter of finished cable**, of which perhaps **40–60% is copper** (conductors + shield), the rest insulation/jacket.
  - 3.2 km × ~12 g/m finished cable ≈ **~38 kg of finished cable**, of which **~20–25 kg is copper**.
- **Connectors & cartridge hardware:** ~5,184 cables × 2 ends ≈ ~10,400 terminations, plus 4 cartridge frames, blind-mate housings, guide hardware. Estimate **~30–60 kg** of connector + cartridge structure (these high-density connectors are substantial metal/plastic assemblies; the Amphenol Paladin-class hardware is not light).

**Estimate — NVLink spine assembly: ~70–110 kg total**, of which **~25–45 kg is copper conductor + shield**, the remainder insulation, connectors and cartridge structure.

> **Confidence: low.** The "2 miles of copper" is well-sourced; converting it to kilograms required assumptions about cable gauge, shielding fraction, and connector mass that are **not sourced**. A reader should treat ~70–110 kg as an order-of-magnitude estimate. It could plausibly be as low as ~50 kg or as high as ~140 kg. What is robust: the spine is **tens of kg, low-end-of-100s at most — not hundreds of kg.** The popular framing of "miles of copper" makes it sound mass-dominant; it is not. It is ~5–8% of the rack.

### Don't forget the power copper

Separately from the NVLink signal spine, the **DC busbar and power cabling** (~40–70 kg, §2) is also copper-dense — a solid ~2.5 kA busbar is a meaningful chunk of copper. **Total "copper-ish" content of the rack** (signal spine copper + busbar + power whips + cold plates if copper) is plausibly **~90–160 kg, ~7–12% of the rack.** Only the *signal* copper (the NVLink spine) is replaceable by optics; the power busbar copper stays regardless.

---

## 4. Optical interconnect — the mass lever

### NVIDIA's roadmap (as of May 2026)

| Generation | Timing | Scale-up (NVLink) interconnect | Source |
|---|---|---|---|
| GB200 / GB300 NVL72 (Blackwell) | shipping 2024–2026 | **Copper** spine, in-rack | [The Register](https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/) |
| Vera Rubin NVL72 / NVL144 (Oberon / Kyber) | 2026–2027 | **Copper inside the rack**; optics only at the *spine/multi-rack* layer for NVL72-Oberon. NVL144 Kyber: **no CPO for scale-up — stays copper** | [The Register, Apr 2026](https://www.theregister.com/2026/04/05/nvidia_optical_scale_up/), [Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date), [SemiAnalysis](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution) |
| **Feynman** | **mid-to-late 2028** | First generation offered with **either copper or co-packaged-optical (CPO) NVLink** | [The Register, Apr 2026](https://www.theregister.com/2026/04/05/nvidia_optical_scale_up/) |

NVIDIA has already shipped **CPO in its Spectrum-X Ethernet and Quantum-X InfiniBand switches (2025–2026)** — i.e. for *scale-out* networking — and is investing heavily in the optical supply chain (~$2 B each to Coherent and Lumentum; ~$2 B to Marvell) ([The Register, Apr 2026](https://www.theregister.com/2026/04/05/nvidia_optical_scale_up/), [io-fund](https://io-fund.com/ai-stocks/nvidia-4b-optical-strategy-cpo-ai-data-centers)). The hard physical reason copper persists *inside* the rack: copper NVLink reaches only **~1–2 m**, which is exactly why all 9 switch trays sit centrally — but within that range copper is cheaper and lower-power than optics ([Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date)).

### Would optical interconnect meaningfully cut rack mass?

**Yes, but modestly. The bigger prize is power, not mass.**

If the copper NVLink spine were replaced by co-packaged optics (optical engines beside the switch ASICs, thin fiber ribbons instead of the copper cartridges):

| Mass effect | Estimate | Reasoning |
|---|---|---|
| Remove copper cable bundle + most spine-cartridge hardware | **−50 to −90 kg** | The ~70–110 kg spine (§3) shrinks to a fiber-ribbon harness. Optical fiber is dramatically lighter than shielded twinax — bare fiber is ~a few g/m vs. ~12 g/m for twinax, and a fiber ribbon carrying the same bandwidth is far thinner. Net of new optical-engine mass on the switch ASICs (small, ~grams each), the spine assembly could drop to ~15–25 kg. |
| Reduced structural reinforcement | **−10 to −25 kg** | Some of the >100 lb (~45 kg) steel reinforcement exists to carry the heavy copper cartridges and their blind-mate loads; a light fiber harness needs less. Partial saving only — most reinforcement is for trays and mating forces generally. |
| Add optical engines / lasers / external laser sources | **+5 to +15 kg** | CPO optical engines and external laser modules add some mass back, but they are small. |
| **Net rack-mass saving** | **≈ −50 to −90 kg** | ≈ **4–7% of the ~1.36 t rack.** |

**The power saving is the headline.** Copper was chosen *to avoid ~20 kW* of optics power in the NVL72 ([The Register](https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/)). But that 20 kW figure was for *pluggable* optics. **CPO cuts optical-link power by ~70%** vs. pluggables ([Network World](https://www.networkworld.com/article/4098942/what-is-co-packaged-optics-a-solution-for-surging-capacity-in-ai-data-center-networks.html), [Avnet](https://www.avnet.com/americas/resources/article/pluggable-vs-co-packaged-optics-in-ai-data-centers-power-scale-and-design-trade-offs/)). So a CPO-based NVLink fabric would add only a few kW, not 20 kW — and copper interconnect itself is not free either (driver power, retimers). The realistic outcome of going optical is roughly **power-neutral to modestly-better**, while *also* removing ~50–90 kg of mass and the in-rack-reach constraint.

> **Bottom line on the lever:** Optical interconnect is a **real but second-order mass lever** — ~50–90 kg, ~4–7% of rack mass. It is not a path to halving rack mass. The compute trays (~half the rack) and power/cooling/structure are where the mass actually is, and optics does not touch those. The strongest argument for an optical-interconnect rack in *this* project is **thermal/power**, covered in §5.

---

## 5. Implication for the orbital node

> **Superseded figure (wave-5, 2026-05-17):** the "~8.5–9 t reusable SSO budget"
> cited here is superseded — the current working figure is **~9.5 t (range
> 8.5–10.5 t)**; see `rocket_lab/neutron/payload_and_block_upgrade.md`. The
> argument in this section (optical interconnect is a second-order mass lever)
> is unaffected.

The node is mass-constrained against Neutron's ~8.5–9 t reusable SSO budget (see `node_mass_model.md`). How does the copper-vs-optical question move that?

**Direct rack-mass effect — small.** Saving ~50–90 kg of rack mass is **<1% of an ~8.5 t node**, and the rack is only ~1.5–1.74 t of that node once space-modified. By itself, optical interconnect does not change the 1-rack-per-Neutron verdict.

**Indirect effect via power and heat — more significant, and favorable.** The node's mass is *dominated* by the radiator and solar array (each ~1–2.4 t per rack in the existing model), and both scale with rack power/heat. The relevant chain:

- A copper NVLink spine is power-lean *inside the rack* (that was the whole point), so going optical does **not** save the 20 kW in the way naive reading suggests — that 20 kW was the *penalty avoided* by not using pluggable optics, not power the copper currently burns.
- However, copper interconnect at NVLink data rates still costs real power in line drivers and signal conditioning, and it caps scale-up reach at ~1–2 m. A CPO rack of the same compute could be **modestly lower total power** and is **not reach-limited**.
- **Every kW shaved off rack power cascades:** less heat → smaller radiator (~350 W/m², ~3–8 kg/m²) → less solar (~100–200 W/kg) → less deployment structure. In the existing node model these three lines are the multi-tonne drivers. A few kW of rack-power reduction is worth more node mass than the ~50–90 kg of copper removed directly.

**Net implication:**

1. **An optical-interconnect rack is mildly favorable for the orbital node** — it trims ~50–90 kg of rack mass and removes the copper spine's structural-reinforcement penalty, and it does not increase (and may slightly decrease) rack power/heat. Every kg and kW helps a mass-constrained node.
2. **But it is not a decisive lever.** Do not size the architecture around it. The node's mass problem is radiator + solar area, driven by the ~135–150 kW of *compute* power — which optics barely touches.
3. **Timing matters.** Optical NVLink is not available until **Feynman (~2028)**; Rubin-era racks (2026–27) keep copper inside the rack. A node launching on the GB300/Rubin generation **will fly the copper spine**. Budget the ~70–110 kg copper spine in the mass model now; treat the ~50–90 kg optical saving as a **future upgrade path** for a Feynman-generation node refresh, not a baseline assumption.
4. **A useful framing for the project:** the copper-vs-optical question is better treated as a **thermal/power-architecture decision** than a mass decision. If a future optical-NVLink rack lets the same compute run a few kW cooler, that buys radiator and solar mass margin worth more than the copper itself.

---

## Component / mass table (consolidated)

| Component | Qty | Est. mass (kg) | Confidence | Replaceable by optics? |
|---|---|---|---|---|
| Compute trays | 18 | 600–720 | low (estimate) | no |
| NVLink switch trays | 9 | 130–190 | low (estimate) | no (ASICs stay; gain optical engines) |
| NVLink copper spine / backplane | 1 (4 cartridges) | 70–110 (copper ~25–45) | low (estimate) | **yes — the mass lever** |
| Power shelves | 6–8 | 130–200 | low (estimate) | no |
| DC busbar + power cabling | 1 | 40–70 | low (estimate) | no (power copper stays) |
| Liquid cooling: manifolds + cold plates + coolant | — | 120–200 | low (estimate) | no |
| Chassis / frame / reinforcement / panels | 1 | 150–230 | low–med (incl. sourced ~45 kg steel) | partial (~10–25 kg) |
| Misc (mgmt cabling, fasteners, castors) | — | 20–50 | low (estimate) | no |
| **Rack total** | — | **~1,360 (3,000 lb)** | **medium-high (sourced)** | — |

---

## Sources

- NVL72 architecture, copper spine, 2-miles-of-copper, 20 kW optics avoidance, 6 power shelves, busbar — [The Register: A closer look at Nvidia's 120kW DGX GB200 NVL72](https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/)
- Component inventory (compute trays, switch trays, copper cable backplane, power shelves, busbar, manifolds) — [NVIDIA DGX GB Rack Scale Systems User Guide — Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
- 5,184 copper cables, 4 spine cartridges, interconnect architecture — [Fibermall: GB200 Interconnect Architecture](https://www.fibermall.com/blog/nvidia-gb200-interconnect-architecture.htm); [Continuum Labs: NVIDIA GB200 NVL72](https://training.continuumlabs.ai/infrastructure/servers-and-chips/nvidia-gb200-nvl72)
- GB200 hardware/BOM (cable count, no per-component mass published) — [SemiAnalysis: GB200 Hardware Architecture & Component Supply Chain](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)
- Rack reinforcement (>100 lb steel, ~6,000 lb mating force, 1,500 kg point load) — [Spheron: NVIDIA GB200 NVL72 Guide](https://www.spheron.network/blog/nvidia-gb200-nvl72-guide/)
- Rack total mass, power, 18+9 trays, power-shelf detail — [Supermicro GB200 NVL72 48U](https://www.supermicro.com/en/products/system/gpu/48u/srs-gb200-nvl72); [Supermicro SuperCluster GB200 NVL72 datasheet](https://www.supermicro.com/datasheet/datasheet_SuperCluster_GB200_NVL72.pdf); [Sunbird DCIM: GB300 NVL72 power](https://www.sunbirddcim.com/blog/how-much-power-does-nvidia-gb300-nvl72-need)
- NVIDIA OCP design contribution — [NVIDIA Technical Blog: GB200 NVL72 designs to OCP](https://developer.nvidia.com/blog/nvidia-contributes-nvidia-gb200-nvl72-designs-to-open-compute-project/)
- Optical scale-up roadmap, copper reach limits, Feynman ~2028, CPO timeline, $4B optical supply-chain investment — [The Register: Nvidia embraces optical scale-up as copper reaches limits (Apr 2026)](https://www.theregister.com/2026/04/05/nvidia_optical_scale_up/)
- Vera Rubin NVL72/NVL144, copper-inside-rack, NVLink reach ~2 m — [Tom's Hardware: Nvidia's Vera Rubin platform in depth](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date); [SemiAnalysis: Vera Rubin — Extreme Co-Design](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution)
- CPO power saving (~70%) vs. pluggables, cable-weight context — [Network World: What is co-packaged optics](https://www.networkworld.com/article/4098942/what-is-co-packaged-optics-a-solution-for-surging-capacity-in-ai-data-center-networks.html); [Avnet: Pluggable vs. co-packaged optics](https://www.avnet.com/americas/resources/article/pluggable-vs-co-packaged-optics-in-ai-data-centers-power-scale-and-design-trade-offs/)
- NVIDIA $4B optical strategy — [io-fund: Inside Nvidia's $4B Optical Strategy](https://io-fund.com/ai-stocks/nvidia-4b-optical-strategy-cpo-ai-data-centers)

---

## Open questions / uncertainties

1. **No published per-component mass breakdown.** NVIDIA/integrators publish only the ~1.36 t rack total. Every component line in §2 is an engineering estimate (~±30%). The most valuable next step is to obtain a real BOM-level mass list — possibly via OCP rack documentation (the GB200 design was contributed to OCP) or directly from an integrator (Supermicro/Lenovo). **Highest-priority unknown.**
2. **NVLink spine mass is an estimate, not a fact.** The "~2 miles of copper" is well-sourced; converting it to ~70–110 kg required unsourced assumptions about cable gauge, shield fraction, and connector mass. Could be ~50–140 kg. A teardown weight or an Amphenol cartridge datasheet would resolve this.
3. **Optical-saving magnitude (~50–90 kg) is bracketed, not measured.** It depends on how much of the spine cartridge hardware and structural reinforcement actually goes away, and how heavy CPO optical engines + external lasers are at NVLink scale. No first-party data exists yet (Feynman not until ~2028).
4. **Copper vs. optical is more a power/thermal question than a mass question for this project.** §5 argues the indirect thermal benefit outweighs the direct mass saving — but quantifying "a few kW cooler" needs a real CPO-vs-copper NVLink power comparison, which NVIDIA has not published for *scale-up* (only scale-out CPO power data exists).
5. **Compute-tray mass is the dominant uncertainty.** At ~45–53% of the rack it swings the whole breakdown; the 600–720 kg estimate (33–40 kg/tray) should be checked against any published 1U GB-tray shipping weight.
6. **Space modification interacts with this breakdown.** The space-modified rack (`node_mass_model.md` §2) adds full cold-plate coverage and launch reinforcement. A space rack that *also* goes optical would partly offset the added reinforcement by removing the copper-spine reinforcement — a small coupling worth noting in detailed design.
7. **Which silicon generation flies?** A GB300/Rubin-era node flies the copper spine; only a Feynman-era (~2028+) node could fly optical NVLink. The baseline mass model should assume copper; optical is an upgrade path.
