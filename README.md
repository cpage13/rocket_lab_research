# Rocket Lab Research

Rocket Lab Research asks one practical question: what new orbital business could
Rocket Lab build with the rockets and spacecraft it already makes? Each
candidate application gets its own honest, source-linked feasibility study.

New to Rocket Lab, Electron, or Neutron? Start with the [primer](rocket_lab_primer.md), a one-page catch-up on the company and its rockets.

## Applications

| Application | Vehicle | Status |
|---|---|---|
| Orbital AI-inference data center | Neutron | Modeled (current) |
| Communications: the Iridium model | Neutron | Modeled (current) |

Two applications are modeled today. The communications workstream holds model
families by communication paradigm; the first is the Iridium model, exploring
the maximum practical performance of Iridium's owned L-band spectrum on a
Neutron-launched next generation fleet. Start with
[communications/conclusion.md](communications/conclusion.md); the promoted
default output is `communications/models/iridium/default.json`.

## Data Center

The first application is a Neutron-launched orbital AI-inference data center.
The operating idea is concrete: integrate GPUs and networking on the ground,
package them into rack-like orbital nodes, attach each node to a Rocket Lab bus
with solar, radiators, thermal, and communications, launch on Neutron, and
operate the result as laser-linked orbital compute.

## Data Center Bottom Line

The model ramps for years, but **2036** is the takeoff. That year Rocket Lab
launches **90 Neutron missions**, deploys **90 new orbital nodes**, and adds
about **38 MW** of new orbital compute power. That is the cadence story.

Each cohort then earns a flat **33% gross margin** for its full five-year life,
and the cohorts compound. The 2036 launches alone earn about **$2.1B a year** in
revenue and about **$700M of gross profit a year**. The build-and-launch program
runs about **1.92x** the cost of an equivalent ground data center: not parity,
but close enough to take seriously.

And that 1.92x is the deliberately conservative floor. Run the same model at
the specs SpaceX revealed for its own AI-1 satellite (June 2026) and the 1.92x
falls to about **1.3x**. Apply the cost-downs the model already tracks and it
reads **0.91x, slightly cheaper than ground**. Each launch carries roughly
**3x the compute at today's silicon**, and the 2036 cohort alone earns about **$3.3B a year** in
revenue and **$1.1B in gross profit**, both still conservative. See
[the AI-1 comparison](data_center/ai1_comparison.md).

## Where To Read It

The full data-center case, with every number traced to a source:

- [conclusion.md](data_center/conclusion.md): the verdict and the headline numbers.
- [data_center/structural_case.md](data_center/structural_case.md): the structural case, why Rocket Lab is uniquely positioned to build this and why the numbers are a floor.
- [data_center/ai1_comparison.md](data_center/ai1_comparison.md): the AI-1 comparison, SpaceX's June 2026 satellite design run through this same model.
- [data_center/README.md](data_center/README.md): how the application works and how to run the model.
- [`models/space/default.json`](data_center/models/space/default.json): every number with its formula, units, and source.
- [Rocket Lab Primer](rocket_lab_primer.md): a one-page catch-up on Rocket Lab, Electron, and Neutron for readers new to the company.

## Communications: The Iridium Model

In June 2026 Rocket Lab agreed to acquire Iridium (closing expected
mid-2027), and with it about 8 MHz of owned, globally coordinated L-band
spectrum near 1.6 GHz. The band's position is the product: it holds through
rain, clouds, and foliage, so it carries a decent, reliable link everywhere
(voice, text, maps, photos, music, AI-agent traffic, and tens of millions of
IoT devices) rather than video-grade broadband. The model asks what that
spectrum could do on a modern Neutron-launched fleet: 25 square meter flat
panels with laser crosslinks, about 12 per launch, replacing the 66-satellite
1990s fleet that moves about 174 Mbps today, less than one home internet
connection.

The highlights, all under the same all-in deployment scenario the data-center
model uses (a modeling posture, stated as one):

- **340 satellites by 2031** (29 Neutron launches, about $725M of hardware
  and launch) serve about **10 million subscribers** at 31,200 per satellite,
  plus about **51.7 million IoT devices**.
- Kept going, the spectrum saturates near **2,000 satellites by 2035**: about
  **62 million subscribers**, the most the 8 MHz can carry.
- The published sheet reads about **$8.25B a year** at the baseline and about
  **$48.5B** at the ceiling, against **$145M** and **$835M a year** of fleet
  cost: margins near **98%** before the unmodeled operations line, under full
  sell-through at investor-set prices.
- The weakest device (a phone-class radio) gets about 1 Mbps at peak; a small
  self-orienting antenna about 3, a mounted antenna about 4. A better antenna
  does not widen the spectrum: it cleans the signal so each wave-change
  carries more bits. Phone-class service needs the band in standard chipsets;
  the antenna tiers and IoT need no one's permission.

The full case, with every number traced:

- [communications/conclusion.md](communications/conclusion.md): the verdict, the 2031 and 2035 stories, the saturation ceiling, and the business breakdown.
- [communications/assumptions.md](communications/assumptions.md): every dial with its source class, including the all-in deployment posture.
- [communications/design.md](communications/design.md): the model-family structure and how future paradigms get added.
- [`models/iridium/default.json`](communications/models/iridium/default.json): the current promoted generated output and model assumptions.

## Repository Map

```text
rklb_space_data_center/
├── README.md            # this file: the program and its applications
├── data_center/         # the data-center application (conclusion, structural case, guide, models)
├── communications/      # the communications application (Iridium model conclusion, assumptions, design, promoted models)
├── research/            # shared evidence wiki and source ledger
├── code/                # the model engine (rklb-value)
└── docs/                # architecture intent, ADRs, agent guide
```

## Running The Model

```sh
cd code
uv sync 2>&1 | tee /tmp/rklb_uv_sync.txt
uv run rklb-value scenarios/default.yaml --json 2>&1 | tee /tmp/rklb_model_output.json
uv run rklb-value --promote 2>&1 | tee /tmp/rklb_promote.txt
```

`--promote` refreshes the JSON under `data_center/models/`. It does not rewrite
the [conclusion](data_center/conclusion.md); after a model change, review the
artifacts and update the conclusion deliberately.

## Disclaimer

This is an independent research project with **no affiliation with, sponsorship
by, or endorsement from Rocket Lab**. "Rocket Lab" and "Neutron" name the
real-world company and vehicle the analysis reasons about; all trademarks belong
to their respective owners.

Nothing here is a Rocket Lab plan, guidance, or official figure. The numbers are
source-linked feasibility estimates and chosen scenario assumptions, not
predictions, forecasts, or financial projections. **Do not use this repository
as investment advice or as a basis for any investment decision.** It is provided
"as is" under the [MIT License](LICENSE), for research and discussion only.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Chris Page.
