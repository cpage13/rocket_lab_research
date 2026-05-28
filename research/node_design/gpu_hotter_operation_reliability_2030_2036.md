# GPU Hotter Operation And Reliability, 2030-2036

**Status:** draft research  
**Date:** 2026-05-27  
**Scope:** non-code research for the RKLB space data center research wiki  
**Source-status summary:** public evidence is strong that warmer liquid-cooling
loops and lower chip-to-coolant thermal resistance are industry directions.
Public evidence is weak that NVIDIA-class AI accelerator packages can safely run
their silicon junctions `+10 deg C` to `+20 deg C` hotter for five-year
high-utilization service. Exact slowdown, shutdown, recommended sustained
junction, and future Rubin/Feynman thermal limits are mostly OEM/partner data,
not public. Model implications should therefore remain scenario/sensitivity,
not default.

## Central Question

Can future AI accelerator packages safely run `10-20 deg C` hotter for sustained
high-utilization orbital data-center service, and what would that do to orbital
radiator sizing?

The answer is:

> Treat literal hotter chip operation as risky. The useful 2030-2036 lever is
> more likely lower chip-to-coolant thermal resistance, warmer coolant return,
> and hotter radiator surfaces while holding GPU/HBM junction temperatures near
> present reliability targets. A `+10 deg C` sustained junction sensitivity is
> worth studying with derating. A `+20 deg C` sustained junction assumption
> should be treated as unsafe for the default five-year orbital case until vendor
> reliability data exists.

This matters because a hotter radiator emits more heat per square meter. Under
the project radiator assumptions, moving radiator surface temperature from
`60 deg C` to `80 deg C` lowers radiator mass from about `12.33 kg/kW` to
`8.91 kg/kW`, a `27.7%` reduction. For the current `421.98 kW` 2036 node,
that is roughly `5.20 t` down to `3.76 t`, or about `1.44 t` of physical
margin. That benefit is real, but it should be achieved by thermal architecture,
not by simply running the GPU junction 20 degrees hotter.

## Definitions

**Junction temperature.** The temperature at the active silicon junctions inside
the GPU die, HBM die, or switch ASIC. This is the temperature most directly tied
to leakage, throttling, electromigration, time-dependent dielectric breakdown,
bias temperature instability, and other wear mechanisms.

**Case or lid temperature.** The temperature at the package exterior, lid, or
case surface where heat leaves the package through a thermal interface material
into a heat sink or cold plate. ASHRAE describes case temperature as the
externally measurable top-of-chip temperature that vendors correlate to internal
critical chip temperatures
([ASHRAE liquid-cooling white paper](https://www.ashrae.org/file%20library/technical%20resources/bookstore/emergence-and-expansion-of-liquid-cooling-in-mainstream-data-centers_wp.pdf)).

**HBM temperature.** The temperature of the high-bandwidth-memory stacks. HBM is
not thermally passive; it is tightly coupled to the GPU package and can throttle
or degrade performance if hot. NVIDIA's H100 PCIe product brief reports HBM
thermal telemetry separately from GPU average temperature and lists thermal
qualification at `HBM THBM = 95 deg C`
([NVIDIA H100 PCIe product brief](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf)).

**Hotspot.** The hottest local temperature on a die, package, memory stack, or
board, which may be meaningfully above average reported GPU temperature.

**Throttle threshold.** The temperature or thermal-limit margin at which the
device reduces clocks or power to protect itself. NVIDIA's public `nvidia-smi`
documentation defines slowdown and maximum operating thresholds, but explains
that supported products may report them as margins from a thermal limit rather
than simple absolute temperatures
([NVIDIA nvidia-smi documentation](https://docs.nvidia.com/deploy/nvidia-smi/index.html)).

**Shutdown threshold.** The thermal condition at which hardware shuts down to
protect the device. NVIDIA's public tooling documents shutdown telemetry, but
future GPU absolute values are not generally public
([NVIDIA nvidia-smi documentation](https://docs.nvidia.com/deploy/nvidia-smi/index.html)).

**Recommended sustained operating temperature.** The temperature band a vendor
or system OEM recommends for long-duration operation without undue throttling or
reliability degradation. This is different from absolute maximum or shutdown.

**Coolant inlet.** The liquid temperature entering the cold plate or technology
cooling loop. Facility-water temperature is not always the same as the IT-side
coolant entering the cold plate; a CDU can add approach temperature between
loops.

**Coolant return.** The liquid temperature leaving the cold plate after
absorbing chip heat. This is closer to the hot-side temperature available to an
orbital radiator, but still not identical to radiator surface temperature.

**Radiator surface temperature.** The temperature of the emitting radiator
surface used in Stefan-Boltzmann heat-rejection math. It is downstream of the
chip and coolant and can be lower than hot-side coolant after radiator internal
resistance and nonuniformity.

## Current Evidence

### Public NVIDIA/OEM Thermal Limits

Public NVIDIA and OEM documents expose power, cooling architecture, and some
thermal telemetry, but they do not publish a clean future `Tjmax` trajectory.

| Product / class | Public thermal evidence | Interpretation |
|---|---|---|
| H100 PCIe | NVIDIA's H100 PCIe product brief lists `350 W` maximum/default board power in the main PCIe mode, reports `TAVG`, `TLIMIT`, and `THBM`, and lists thermal qualification at `GPU TAVG = 87 deg C` and `HBM THBM = 95 deg C`; slowdown/shutdown are expressed relative to `TLIMIT` (`-2 deg C` slowdown and `-5 deg C` shutdown margins in that document) ([NVIDIA H100 PCIe product brief](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf)). | Current public H100 data supports high internal temperature tolerance, but it is not a blank check for five-year higher-junction operation. |
| H100 / DGX systems | An NVIDIA forum answer says maximum stable operating temperature, recommended range, throttling threshold, and shutdown threshold are available to NVIDIA partners/OEMs rather than being answered publicly in that forum thread ([NVIDIA developer forum](https://forums.developer.nvidia.com/t/nvidia-h100-recommended-operating-temperature/342125)). | The exact values needed for a public orbital model are not generally public. |
| B200 | Lenovo's public B200 product guide lists the SXM6 B200 as a `1000 W` GPU with `180 GB HBM3e`; the same page notes liquid-cooled and air-cooled server variants depending on system design ([Lenovo B200 product guide](https://lenovopress.lenovo.com/lp2226-thinksystem-nvidia-b200-180gb-1000w-gpu)). | Power density is rising sharply. Public package power is available; sustained junction recommendations are not. |
| GB200 NVL72 | HPE's GB200 NVL72 product page lists `72` Blackwell GPUs, `36` Grace CPUs, `13.5 TB` total HBM3E, `132 kW` rack power, `115 kW` liquid cooled, and `17 kW` air cooled ([HPE GB200 NVL72 product page](https://buy.hpe.com/us/en/Compute/Rack-Scale-System/Nvidia-NVL-System/Nvidia-NVL-System/NVIDIA-GB200-NVL72-by-HPE/p/1014890104)). | AI rack heat is mostly liquid-captured already, but public rack data does not publish chip junction margin. |
| GB300 / Blackwell Ultra | The local corpus already records GB300 as a `72`-GPU rack-scale Blackwell Ultra system and treats rack power as OEM-specific around `132-155 kW`; public NVIDIA/OEM sources are stronger on rack configuration than on chip thermal thresholds ([ai_hardware.md](../ai_hardware/ai_hardware.md), [gpu_generational_roadmap.md](../ai_hardware/gpu_generational_roadmap.md)). | Use source-status guards. Do not infer safe hotter sustained junctions from rack power. |
| Rubin / GB300 successor class | Public reporting and industry cooling commentary support `45 deg C` water as a near-term warm-water direction, but exact future junction/reliability limits are not public. CoolIT explicitly warns that warm-water operation reduces chiller dependency but does not eliminate heat rejection needs ([CoolIT](https://www.coolitsystems.com/resources/news/warm-water-cooling-and-ai-the-future-is-here-but-its-not-chiller-free/)). | Strong evidence for warmer liquid cooling; weak evidence for higher safe junction temperature. |

### Public HBM Evidence

HBM deserves separate treatment because the project unit is a GPU package, not a
bare compute die.

Micron's public HBM3E product brief lists an operating temperature range of
`0 deg C <= TOPER <= +105 deg C`
([Micron HBM3E product brief](https://www.micron.com/content/dam/micron/global/public/documents/products/product-flyer/hbm3e-product-brief.pdf)).
Samsung says its HBM3E improves thermal resistance by `11%` versus its
predecessor using advanced thermal-compression non-conductive film
([Samsung HBM3E](https://semiconductor.samsung.com/dram/hbm/hbm3e/)).
SK hynix announced iHBM on 2026-05-26, claiming integrated cooling elements in
the HBM package reduce thermal resistance by `30%` for next-generation products
including HBM5
([SK hynix newsroom](https://news.skhynix.com/ihbm-solution/),
[Tom's Hardware summary](https://www.tomshardware.com/tech-industry/semiconductors/sk-hynix-unveils-ihbm-thermal-architecture-that-cools-ai-memory-at-the-source-integrated-cooling-elements-inside-HBM-interface-cut-thermal-resistance-by-30-percent-target-next-gen-HBM5-accelerators-and-dense-AI-data-centers)).

These sources support a 2030-2036 trajectory toward better thermal extraction
from HBM packages. They do not prove the whole GPU/HBM package should run
`+20 deg C` hotter. They point more naturally to the opposite design: improve
thermal resistance so the same junction/HBM temperature can support higher heat
flux and warmer coolant/radiator operation.

### Data-Center Liquid-Cooling Practice

ASHRAE's liquid-cooling classes now include `W17`, `W27`, `W32`, `W40`, `W45`,
and `W+`. The ASHRAE reference card lists `W40` at `40 deg C`, `W45` at
`45 deg C`, and `W+` above `45 deg C`; it also states W45/W+ are typically
operated without chillers to improve energy efficiency, although some locations
may not be suitable for dry coolers
([ASHRAE reference card](https://www.ashrae.org/file%20library/technical%20resources/bookstore/supplemental%20files/therm-gdlns-5th-r-e-refcard.pdf)).
A 2025 ASHRAE presentation separately lists Technology Cooling System classes up
to `S50`, or `50 deg C`, and warns that liquid-cooling flow loss can overheat IT
equipment within seconds
([Dallas ASHRAE 2025 presentation](https://dallas-ashrae.org/images/meeting/041625/the_ashrae_thermal_guidelines_for_data_centers_____past__present_and_future.pdf)).

Data Center Dynamics reports that some high-end processors and accelerators can
be cooled at facility-water supply temperatures up to `40-45 deg C`, while also
flagging that as chip powers rise, operators may still need lower inlet
temperatures or better cold plates
([DCD hot-water analysis](https://www.datacenterdynamics.com/en/analysis/hot-water-cold-water/)).
Fierce Network quotes NVIDIA cooling commentary that chips around `85-90 deg C`
make `45 deg C` water feasible, while also noting that operators often prefer
lower GPU temperatures to preserve clock speed
([Fierce Network](https://www.fierce-network.com/cloud/nvidia-has-no-chill)).

This is the strongest public evidence base for the project. It supports warmer
coolant and hot-loop architecture. It does not support calling a hotter GPU
junction default.

## Reliability Mechanisms

Running the silicon hotter is not just a radiator equation. It changes device
physics, packaging stress, control margins, and five-year mission risk.

### Leakage Power

Semiconductor leakage generally rises with temperature. Hotter silicon can
consume more static power, which then becomes more heat to reject. For a
spacecraft node already sized around solar and radiator mass, this is a feedback
loop: hotter junctions can reduce radiator area per watt only if the extra
leakage and derating losses do not give the wattage back.

### Electromigration

Electromigration in metal interconnects is commonly modeled with Black's
equation. Cadence summarizes Black's equation as an empirical Arrhenius-based
relationship involving current density and interconnect temperature, while also
warning that it assumes constant temperature and one dominant diffusion process
([Cadence Black's equation explainer](https://resources.system-analysis.cadence.com/blog/msa2020-blacks-equation-for-mttf-due-to-electromigration)).

The project implication is straightforward: higher sustained temperature tends
to reduce interconnect lifetime, especially under high current density. Derating
voltage/current and avoiding thermal hotspots are therefore first-order orbital
reliability tools.

### Time-Dependent Dielectric Breakdown

Time-dependent dielectric breakdown is an aging mechanism where dielectric
materials fail under electric field over time. Temperature and voltage stress are
central in accelerated lifetime modeling. IBM-affiliated TDDB work on low-k
interlevel dielectric reports time-dependent failure distributions in copper
metallization / low-k dielectric structures and field-dependent kinetics, which
is enough for this project-level conclusion: oxide/dielectric lifetime is a
stress-and-temperature reliability problem, not a single published GPU `Tjmax`
number
([IBM Research TDDB paper page](https://research.ibm.com/publications/time-dependent-dielectric-breakdown-in-a-low-k-interlevel-dielectric)).

The project implication is that hotter operation cannot be assessed from a
single `Tjmax` number. Voltage, current density, package materials, and duty
cycle matter.

### Bias Temperature Instability

Bias temperature instability is a transistor-aging mechanism that worsens under
bias and elevated temperature. Reviews of NBTI describe it as a major
reliability issue in scaled CMOS and connect it to elevated temperature and
electric fields
([Microelectronics Reliability NBTI review](https://www.sciencedirect.com/science/article/pii/S002627140600374X),
[circuit perspective review](https://www.sciencedirect.com/science/article/pii/S0026271417305644)).

The orbital implication is that a cooler, derated inference service may be a
better fit than training-like peak operation. Inference can accept lower clocks
or lower voltage in exchange for lower aging stress.

### Solder, Interposer, HBM, And Packaging Fatigue

GPU/HBM packages are mechanically complex: large silicon, interposers, HBM
stacks, solder bumps, underfill, cold plates, and thermal interface materials.
Thermal cycling drives fatigue through coefficient-of-thermal-expansion mismatch.
Absolute steady temperature and cyclic temperature swing are different stressors.

The local reliability memo already flags thermal cycling, HBM/NVLink failures,
launch vibration, and coolant-loop reliability as important space-specific
concerns
([reliability_failure_handling.md](reliability_failure_handling.md)).
For this research question, that means a steady `+10 deg C` junction may worsen
wear-out while a `+20 deg C` orbit day/night swing would be worse still. A good
orbital design should keep the silicon thermally stable even if the radiator
environment changes.

### Pumps, Cold Plates, And TIM Degradation

If hotter operation is achieved by pushing the coolant loop harder, the
reliability burden shifts to pumps, manifolds, cold plates, seals, fluids, and
thermal interface materials. ASHRAE's 2025 presentation warns that loss of
liquid flow can overheat IT equipment within seconds
([Dallas ASHRAE 2025 presentation](https://dallas-ashrae.org/images/meeting/041625/the_ashrae_thermal_guidelines_for_data_centers_____past__present_and_future.pdf)).
Redwire similarly warns that active pumped loops add pump reliability, plumbing,
fluid-management, startup, control, and parasitic-power challenges as orbital
thermal systems scale
([Redwire ODC white paper](https://rdw.com/wp-content/uploads/2026/05/RDW26-053-ODC-Power-Thermal-Study-White-Paper-R11-Digital.pdf)).

The design goal should be to spend complexity where it preserves junction
reliability, not to treat hotter silicon as free mass savings.

## Quantitative Literature And The `+10 deg C` Rule

The common rule says every `+10 deg C` roughly doubles failure rate or halves
life. Electronics Cooling explains that this is an Arrhenius-based rule of thumb
for specific thermally activated mechanisms, not a universal law for all
electronics failures
([Electronics Cooling](https://www.electronics-cooling.com/2017/08/10c-increase-temperature-really-reduce-life-electronics-half/)).

Using the Arrhenius acceleration ratio:

```text
rate factor = exp(Ea / k * (1 / T_old - 1 / T_new))
```

where `Ea` is activation energy and `k` is Boltzmann's constant in eV/K, a
`+10 deg C` or `+20 deg C` shift near AI-chip operating temperatures gives:

| Starting junction | Delta | Ea = 0.5 eV | Ea = 0.7 eV | Ea = 0.8 eV | Ea = 1.0 eV |
|---:|---:|---:|---:|---:|---:|
| `70 deg C` | `+10 deg C` | `1.61x` | `1.95x` | `2.15x` | `2.61x` |
| `70 deg C` | `+20 deg C` | `2.54x` | `3.68x` | `4.44x` | `6.44x` |
| `80 deg C` | `+10 deg C` | `1.57x` | `1.88x` | `2.06x` | `2.47x` |
| `80 deg C` | `+20 deg C` | `2.41x` | `3.43x` | `4.09x` | `5.82x` |
| `85 deg C` | `+10 deg C` | `1.55x` | `1.85x` | `2.02x` | `2.41x` |
| `85 deg C` | `+20 deg C` | `2.36x` | `3.32x` | `3.94x` | `5.55x` |

This table is not a forecast of total GPU annual failure rate. It is a warning:
for the subset of mechanisms governed by Arrhenius-like thermal activation,
`+20 deg C` can easily mean several times faster wear-out. Some field failures
are not governed by this equation. Thermal-cycling fatigue, workmanship defects,
random failures, firmware/software hangs, radiation events, and pump failures
need separate models. But the direction is clear enough for the default model:
do not assume hotter sustained junction operation is harmless.

## Data-Center Practice

Operators often run below absolute thermal limits for four reasons:

1. **Boost and throttling margin.** Running near the thermal limit leaves no
margin for transients, clogged filters, flow imbalance, local hotspots, or
workload spikes. NVIDIA's public tooling distinguishes current temperature,
maximum operating, slowdown, and shutdown telemetry
([NVIDIA nvidia-smi documentation](https://docs.nvidia.com/deploy/nvidia-smi/index.html)).

2. **Performance.** Fierce Network quotes a Dell'Oro analyst noting that
operators have preferred slightly lower GPU temperatures to maximize clock speed
([Fierce Network](https://www.fierce-network.com/cloud/nvidia-has-no-chill)).

3. **Useful life.** Long-duration service economics care about sustained
capacity, not just survival at an absolute maximum. For an unserviceable orbital
node, a device that survives but throttles or ages rapidly is still a business
problem.

4. **System reliability.** Liquid loops introduce pump, CDU, leak, sensor, and
control failure modes. A hotter design with thinner margin makes those failures
more severe.

The analogy to ground data centers matters. Ground operators can replace
hardware. Orbit cannot. That pushes the project toward more derating, not less.

## 2030-2036 Trajectory

### What Looks Plausible

**Warmer coolant classes.** ASHRAE has already formalized `W45` and `W+` liquid
classes, and technology-cooling-system guidance reaches `S50`
([ASHRAE reference card](https://www.ashrae.org/file%20library/technical%20resources/bookstore/supplemental%20files/therm-gdlns-5th-r-e-refcard.pdf),
[Dallas ASHRAE 2025 presentation](https://dallas-ashrae.org/images/meeting/041625/the_ashrae_thermal_guidelines_for_data_centers_____past__present_and_future.pdf)).

**Better HBM thermal extraction.** Samsung reports improved HBM3E thermal
resistance, Micron's HBM3E operates up to `105 deg C`, and SK hynix is targeting
future HBM generations with integrated cooling elements and `30%` lower thermal
resistance
([Samsung HBM3E](https://semiconductor.samsung.com/dram/hbm/hbm3e/),
[Micron HBM3E product brief](https://www.micron.com/content/dam/micron/global/public/documents/products/product-flyer/hbm3e-product-brief.pdf),
[SK hynix newsroom](https://news.skhynix.com/ihbm-solution/)).

**Better cold plates and thermal interfaces.** ASHRAE says rising socket power
and lowering case-temperature requirements are driving a shift from air to
liquid cooling and lower thermal resistance
([ASHRAE liquid-cooling white paper](https://www.ashrae.org/file%20library/technical%20resources/bookstore/emergence-and-expansion-of-liquid-cooling-in-mainstream-data-centers_wp.pdf)).
This supports a 2030-2036 sensitivity where the same junction temperature can
support warmer coolant return and a hotter radiator surface.

**Derated orbital inference.** Inference can be run steadier and more
partitioned than training. The project can plausibly derate voltage/frequency,
accept lower peak throughput, and size revenue around sustained capacity. That
is more believable than assuming full-power training-like duty at hotter
junction temperatures.

### What Does Not Look Safe Yet

**A certified future `+20 deg C` junction lift.** No public source found in this
pass says B200, GB300, Rubin, or future Feynman-class packages can sustain
`+20 deg C` higher junction temperature for five years at high utilization.

**Training workloads at hotter junctions.** Training is peak-power,
interconnect-heavy, synchronized, and less forgiving of failures. If a
temperature sensitivity is used, it should be tied to derated inference first.

**A simple one-temperature model.** `T_junction`, HBM temperature, cold-plate
inlet, coolant return, and radiator surface are separate. A model that lifts one
number called `Tjmax` will hide the actual engineering constraint.

## Space-Specific Considerations

### No Servicing

Ground clusters can replace bad GPUs, pumps, cold plates, and racks. An orbital
node cannot. The same absolute temperature that is tolerable on the ground may
be unacceptable if it shortens field life or narrows recovery margin.

### Radiation

Radiation adds single-event upsets, latch-up risk, and cumulative dose to a
commercial part that was not designed as a rad-hard spacecraft component. The
local reliability file treats radiation as manageable in the target orbit but
not zero. Hotter silicon can worsen some leakage and aging margins, so it should
not be stacked casually on top of radiation and launch risk.

### Thermal Cycling

A high, steady temperature and a large cyclic temperature swing are different
problems. Thermal cycling can fatigue solder, bumps, interposers, HBM stacks,
connectors, and cold plates. Orbit should try to keep GPU/HBM temperatures
stable even if the radiator environment cycles.

### Launch Vibration

Launch vibration can create latent mechanical defects. A hotter post-launch
operating point may accelerate the failure of already-weakened solder,
interconnect, or package interfaces.

### Vacuum-Compatible Materials

Coolants, seals, TIMs, underfills, potting, conformal coatings, and pump
materials must be compatible with vacuum, radiation, and five-year life. The
thermal architecture cannot simply import a terrestrial water loop unchanged.

### Pump And Loop Reliability

The thermal loop is a possible whole-node killer. Hotter operation usually means
less thermal margin when flow is reduced. The project should treat N+1 or
partitioned coolant paths as part of the reliability solution, not optional
polish.

### Derating And Graceful Degradation

The best orbital path is likely: derated inference, partitioned GPU fault
domains, redundant thermal loops, and business assumptions based on end-of-life
capacity. That is compatible with warmer radiator operation. It is not
compatible with a casual "run the chips 20 degrees hotter" default.

## Model Implication

The current project should **not** model a literal `Tjmax` lift as the default.
It should model:

1. assumed GPU/HBM sustained junction design target;
2. assumed case/lid temperature;
3. chip-to-coolant thermal resistance;
4. coolant inlet and return temperature;
5. coolant-to-radiator or transport-loop temperature drop;
6. radiator surface temperature;
7. effective sink temperature, emissivity, face credit, and areal density;
8. derived radiator `kg/kW` and area;
9. derating or reliability penalty if junction temperature rises.

### How To Treat A `+10 deg C` Chip Assumption

Use as a **named sensitivity**, not a default. It should carry explicit
conditions:

- inference workload, not training;
- voltage/frequency derating;
- junction held below vendor slowdown margin in expected transients;
- mission economics sized around possible reliability hit;
- thermal loop redundancy and fault detection included.

Research label: `scenario`, with unresolved vendor support.

### How To Treat A `+20 deg C` Chip Assumption

Treat as **unsafe for the default** and only as an aggressive stress/upside case
if paired with vendor data or strong derating. Under Arrhenius-like mechanisms,
`+20 deg C` near `70-85 deg C` can accelerate wear-out by about `2.4x` to
`6.4x`, depending on activation energy. That is too large for an unserviceable
five-year node unless the system is intentionally underclocked, over-redundant,
or the thermal improvement is mostly lower resistance rather than higher
junction temperature.

### Preferred Modeling Language

Use:

> hot-loop / chip-to-coolant thermal-resistance improvement

Do not use:

> Tjmax lift

unless the model truly has a vendor-sourced higher sustained junction target.

## Radiator Sizing Implication

If hotter chip operation, lower thermal resistance, or two-phase transport
allows a hotter radiator surface, the radiator benefit is meaningful. Under the
project's current simplified radiator assumptions (`epsilon = 0.85`,
`T_sink = 250 K`, one effective face, `5 kg/m2`):

| Radiator surface | Radiator mass | Change vs `60 deg C` | Change vs `40 deg C` |
|---:|---:|---:|---:|
| `40 deg C` | `18.17 kg/kW` | worse by `47.4%` | baseline |
| `60 deg C` | `12.33 kg/kW` | baseline | `32.1%` lower |
| `70 deg C` | `10.42 kg/kW` | `15.5%` lower | `42.7%` lower |
| `80 deg C` | `8.91 kg/kW` | `27.7%` lower | `50.9%` lower |
| `90 deg C` | `7.69 kg/kW` | `37.6%` lower | `57.7%` lower |

For the current `421.98 kW` 2036 node:

| Radiator surface | Mass per node | Physical interpretation |
|---:|---:|---|
| `60 deg C` | `5.20 t` | Close to current `0.012 t/kW` default (`5.06 t/node`). |
| `80 deg C` | `3.76 t` | Saves about `1.30-1.44 t/node`, depending on whether compared with current default or idealized `60 deg C`. |
| `90 deg C` | `3.25 t` | More aggressive; likely requires better thermal resistance, two-phase transport, or higher chip margin. |

This tells us why the user's intuition partly works and partly needs a guard:
an `80 deg C` radiator is valuable, but the project may already be giving
partial credit for a warm radiator through the `0.012 t/kW` default. The open
question is not "can metal radiators sit at 80 deg C?" They can. The question is
whether the GPU/HBM-to-radiator temperature ladder can support that surface
temperature while preserving five-year useful life.

## Public-Safe Claims

Safe:

- Modern AI accelerator packages already operate with high internal thermal
  limits; NVIDIA's public H100 PCIe brief lists thermal qualification at
  `GPU TAVG = 87 deg C` and `HBM THBM = 95 deg C`.
- Exact recommended sustained operating temperatures, throttling thresholds, and
  shutdown thresholds for H100-class systems are not fully public; NVIDIA points
  users to OEM/partner channels for that information.
- ASHRAE liquid-cooling classes and public data-center cooling commentary
  support warmer coolant operation, including `45 deg C` facility water and
  above-45 classes.
- HBM vendors are actively reducing thermal resistance; SK hynix's iHBM claim
  of `30%` lower thermal resistance is directly relevant to 2030-2036 package
  thermal extraction, but it is not proof of a higher safe GPU junction default.
- A hotter radiator surface can reduce radiator mass through Stefan-Boltzmann
  physics.
- The project should model warmer coolant/radiator operation separately from
  hotter chip junction operation.

Unsafe:

- "Future GPUs can safely run `20 deg C` hotter for five years."
- "An `80 deg C` radiator means the GPU junction can run at `80 deg C` without
  reliability penalty."
- "HBM3E operating to `105 deg C` proves the whole GPU package should be run
  hotter."
- "The `10 deg C halves life` rule applies exactly to total GPU annual failure
  rate."
- "Hotter chips close the orbital premium by themselves."
- "Tjmax lift is the right model parameter" unless backed by vendor data.

## Unresolved Questions

- What are the vendor-certified sustained junction, case, HBM, slowdown, and
  shutdown thresholds for B200, GB300, Rubin, and Feynman-class packages?
- What junction temperatures do NVIDIA/OEMs recommend for 24/7 high-utilization
  service over three to five years?
- What is the chip-to-coolant thermal resistance for 2030-2036 AI accelerator
  packages, including HBM stacks and interposer hot spots?
- Can future HBM cooling elements and package designs lower thermal resistance
  enough to support an `80 deg C` radiator surface while holding junction
  temperatures near current reliability targets?
- What is the reliability penalty of a `+10 deg C` sustained orbital inference
  mode after voltage/frequency derating?
- How much of the project GPU AFR should be modeled as thermally activated
  wear-out versus random failure, launch latent damage, thermal-cycling fatigue,
  radiation, firmware, or loop failures?
- Can a space-qualified two-phase or heat-pipe architecture support the desired
  temperature ladder with acceptable pump/fluid/material reliability?

## Sources

Local project sources:

- [gpu_temperature_cooling_limits.md](gpu_temperature_cooling_limits.md)
- [radiator_costdown_2030_2036.md](radiator_costdown_2030_2036.md)
- [reliability_failure_handling.md](reliability_failure_handling.md)
- [SOURCE_INDEX.md](../SOURCE_INDEX.md) claims `THR-017` through `THR-020`

External sources:

- [NVIDIA H100 PCIe product brief](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf), public GPU/HBM thermal qualification and slowdown/shutdown reference.
- [NVIDIA SMI documentation](https://docs.nvidia.com/deploy/nvidia-smi/index.html), public temperature-reporting semantics.
- [Lenovo ThinkSystem NVIDIA B200 180GB 1000W GPU](https://lenovopress.lenovo.com/lp2226-thinksystem-nvidia-b200-180gb-1000w-gpu) and [HPE GB200 NVL72 product page](https://buy.hpe.com/us/en/Compute/Rack-Scale-System/Nvidia-NVL-System/Nvidia-NVL-System/NVIDIA-GB200-NVL72-by-HPE/p/1014890104), current OEM high-power accelerator context.
- [ASHRAE liquid-cooling white paper](https://www.ashrae.org/file%20library/technical%20resources/bookstore/emergence-and-expansion-of-liquid-cooling-in-mainstream-data-centers_wp.pdf), [ASHRAE thermal-guidelines reference card](https://www.ashrae.org/file%20library/technical%20resources/bookstore/supplemental%20files/therm-gdlns-5th-r-e-refcard.pdf), and [Dallas ASHRAE 2025 presentation](https://dallas-ashrae.org/images/meeting/041625/the_ashrae_thermal_guidelines_for_data_centers_____past__present_and_future.pdf), liquid-cooling temperature-class context.
- [SK hynix iHBM announcement](https://news.skhynix.com/ihbm-solution/), [Samsung HBM3E](https://semiconductor.samsung.com/dram/hbm/hbm3e/), and [Micron HBM3E product brief](https://www.micron.com/content/dam/micron/global/public/documents/products/product-flyer/hbm3e-product-brief.pdf), HBM thermal-resistance and operating-temperature context.
- [Electronics Cooling 10 C reliability-rule discussion](https://www.electronics-cooling.com/2017/08/10c-increase-temperature-really-reduce-life-electronics-half/), [Cadence Black's equation explainer](https://resources.system-analysis.cadence.com/blog/msa2020-blacks-equation-for-mttf-due-to-electromigration), [IBM TDDB paper](https://research.ibm.com/publications/time-dependent-dielectric-breakdown-in-a-low-k-interlevel-dielectric), and the cited Microelectronics Reliability papers for temperature-accelerated failure-mechanism caution.

## Proposed Tracker / Library / Source-Index Entry Text

Suggested `LIBRARY.md` row under Node Design:

| File | What it is | Key takeaway |
|---|---|---|
| [gpu_hotter_operation_reliability_2030_2036.md](gpu_hotter_operation_reliability_2030_2036.md) | GPU/HBM hotter-operation and reliability research for 2030-2036. | Public evidence supports warmer coolant, lower thermal resistance, and hotter radiator surfaces more strongly than it supports a literal `+10-20 deg C` sustained GPU junction lift; `+20 deg C` should remain unsafe for the default five-year orbital model. |

Suggested `RESEARCH_TRACKER.md` row under Node Design:

| File | Status | Key finding / purpose | Source audit note |
|---|---|---|---|
| [gpu_hotter_operation_reliability_2030_2036.md](gpu_hotter_operation_reliability_2030_2036.md) | draft | Tests whether future AI GPU/HBM packages can safely run `10-20 deg C` hotter for sustained orbital service and what that would mean for radiator sizing. | Public sources support warmer liquid cooling and HBM thermal-resistance improvements; exact future GPU/HBM sustained junction limits are not public, and `+20 deg C` hotter junction operation should be a stress sensitivity, not a default. |

Suggested `SOURCE_INDEX.md` claim additions:

| Claim ID | Claim text | Source status | Role | Links or internal references | Uncertainty notes |
|---|---|---|---|---|---|
| `THR-017` | H100 PCIe public thermal qualification includes `GPU TAVG = 87 deg C` and `HBM THBM = 95 deg C`, with slowdown/shutdown expressed as margins to `TLIMIT`. | `certified` | Supporting source claim | [NVIDIA H100 PCIe product brief](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf) | Applies to H100 PCIe, not all future GPU packages or orbital service. |
| `THR-018` | Public evidence supports warmer liquid-cooling classes up to `45 deg C` facility water and above-45 classes, but facility water, cold-plate inlet, coolant return, and radiator surface are distinct. | `certified` | Thermal-model support | [ASHRAE reference card](https://www.ashrae.org/file%20library/technical%20resources/bookstore/supplemental%20files/therm-gdlns-5th-r-e-refcard.pdf); [Dallas ASHRAE 2025 presentation](https://dallas-ashrae.org/images/meeting/041625/the_ashrae_thermal_guidelines_for_data_centers_____past__present_and_future.pdf) | Do not infer radiator surface temperature directly from facility-water class. |
| `THR-019` | HBM thermal-resistance improvements are a credible 2030-2036 direction; SK hynix announced an iHBM approach claiming `30%` lower thermal resistance for next-generation HBM products. | `sourced_estimate` | Thermal-trajectory support | [SK hynix newsroom](https://news.skhynix.com/ihbm-solution/); [Samsung HBM3E](https://semiconductor.samsung.com/dram/hbm/hbm3e/); [Micron HBM3E product brief](https://www.micron.com/content/dam/micron/global/public/documents/products/product-flyer/hbm3e-product-brief.pdf) | Supports lower thermal resistance, not a certified hotter GPU junction default. |
| `THR-020` | A sustained `+10 deg C` or `+20 deg C` GPU junction increase materially accelerates temperature-sensitive reliability mechanisms and should not be a default assumption without vendor data. | `sourced_estimate` | Public wording guard and sensitivity support | [Electronics Cooling 10 deg C rule](https://www.electronics-cooling.com/2017/08/10c-increase-temperature-really-reduce-life-electronics-half/); [Cadence Black's equation explainer](https://resources.system-analysis.cadence.com/blog/msa2020-blacks-equation-for-mttf-due-to-electromigration); this document | Rule is heuristic and mechanism-specific; total GPU AFR needs a separate model. |
