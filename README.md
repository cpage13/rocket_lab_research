# Rocket Lab Research

Rocket Lab Research asks one practical question: what new orbital business could
Rocket Lab build with the rockets and spacecraft it already makes? Each
candidate application gets its own honest, source-linked feasibility study.

The recurring answer across applications is not sunlight or altitude. Space
wins where it converts construction into manufacturing. Ground data centers
and ground networks are built site by site, constrained by regulations, labor
markets, grid queues, and geography. An orbital fleet is standardized units
off an assembly line, launched on a repeating cadence, the way data centers
and large communications networks already standardize their racks and cells,
applied to the whole facility. Economies of scale and repeatability are the
product; orbit is where they run.

New to Rocket Lab, Electron, or Neutron? Start with the [primer](rocket_lab_primer.md), a one-page catch-up on the company and its rockets.

## Applications

| Application | Vehicle | Status |
|---|---|---|
| Orbital AI-inference data center | Neutron | Modeled (current) |
| Communications: the Iridium model and the product case | Neutron | Modeled (current) |

Two applications are modeled today. The communications application asks what
Iridium's owned L-band could carry on a Neutron-launched next-generation fleet,
and what that network would sell. Start with
[communications/conclusion.md](communications/conclusion.md); the promoted
artifacts are under `communications/models/`. The two applications' headlines
never add: each runs as if it had the shared launch ramp to itself.

## Data Center

The first application is a Neutron-launched orbital AI-inference data center.
The operating idea is concrete: integrate GPUs and networking on the ground,
package them into rack-like orbital nodes, attach each node to a Rocket Lab bus
with solar, radiators, thermal, and communications, launch on Neutron, and
operate the result as laser-linked orbital compute.

## Data Center Bottom Line

The model ramps for years, but **2036** is the takeoff. That year Rocket Lab
launches **90 Neutron missions**, deploys **90 new orbital nodes**, and adds
about **68 MW** of new orbital compute power. That is the cadence story.

Each cohort then earns a flat **33% margin** for its full five-year life, and
the cohorts compound. The 2036 launches alone earn about **$2.5B a year** in
revenue and about **$840M of profit a year**, and the living fleet reads about
**$7.4B a year**. The build-and-launch program runs about **1.28x** the cost
of an equivalent ground data center: not parity, but a quarter more, before
any space-native design iteration.

The 1.28x stands on the architecture the industry itself validated: the model
semi-copies the deployed, double-sided, run-hot radiator SpaceX revealed on
its AI-1 satellite (June 2026), within 10 percent of AI-1's implied radiator
mass, and prices solar and thermal hardware at assembly-line scale ($20k/kW
each, investor-set with sourced directional support). Run the same model at
AI-1's full spec on the same dials and it reads about **0.91x, cheaper than
ground**. The old heavy-radiator posture at $40k/kW reads **1.92x** and is
kept as the labeled conservative exception. See
[the AI-1 comparison](data_center/ai1_comparison.md).

And the window understates the curve. The model stops at 2036 with cadence
still climbing: extended on the same dials, 2040 reads about **$17.7B a year**
(labeled extrapolation). The 2036 fleet is two tenths of a percent of the
AI-capacity market reference, and the cost dials sit flat across a decade in
which a real production line learns. The upside case, stated and labeled, is
[the structural case](data_center/structural_case.md).

## Where To Read It

The full data-center case, with every number traced to a source:

- [conclusion.md](data_center/conclusion.md): the verdict and the headline numbers.
- [data_center/structural_case.md](data_center/structural_case.md): the structural case, the pitch: the engine, what the numbers refuse to count, and the runway.
- [data_center/ai1_comparison.md](data_center/ai1_comparison.md): the AI-1 comparison, SpaceX's June 2026 satellite design run through this same model.
- [data_center/README.md](data_center/README.md): how the application works and how to run the model.
- [`models/space/default.json`](data_center/models/space/default.json): every number with its formula, units, and source.
- [Rocket Lab Primer](rocket_lab_primer.md): a one-page catch-up on Rocket Lab, Electron, and Neutron for readers new to the company.

## Communications: The Iridium Model

In June 2026 Rocket Lab agreed to acquire Iridium (closing expected
mid-2027), and with it about 8 MHz of owned, globally coordinated L-band
spectrum near 1.6 GHz (COMM-611). The band's position is the product: it holds through
rain, clouds, and foliage, so it carries a decent, reliable link everywhere
(voice, text, maps, photos, music, AI-agent traffic, and IoT devices) rather
than video-grade broadband. It is first an IoT network. The model asks what
that spectrum could do on a modern Neutron-launched fleet: flat 15.4 square
meter panels with laser crosslinks, 16 to a launch with the Neutron block
upgrade assumed, replacing the 66-satellite Iridium NEXT fleet (launched 2017
to 2019) that moves about 174 Mbps today, less than one home internet
connection (COMM-639).

Two cases answer it, side by side and never added. The engineering case is
every seat each people class could carry, each class alone, with IoT's room
beside them. The product case is what the network would sell at the
investor's prices, held flat, in the typical market of 2,000 drawn markets.

- **The fleet.** Every Neutron launch on the shared ramp flies communications
  satellites. The fleet passes the 340-satellite coverage floor in FY2031, with
  528 flying, and reaches 4,288 in FY2036, at $1,554.4M a year.
- **The product case.** At $10 and $50 a month for the two terminals and $3
  and $6 for the two IoT classes, the network earns $2,194.6M in FY2031 and
  **$13,156.2M in FY2036 at an 88.2 percent margin**, about four fifths of it
  from IoT. That is the typical market; it sits a little below the median of
  the markets where the case works.
- **The engineering case.** Each class could fill the fleet alone. In FY2036
  the small terminal alone serves 24.6 million people ($2,952.8M a year, a
  47.4 percent own margin) and the mounted terminal alone 3.5 million
  ($2,116.3M, 26.5 percent). IoT's room fits 11.5 billion minimal-packet
  devices, that class alone: a capacity, not a forecast.
- **The spectrum bound.** Each class's saturation number is a spectrum bound
  reported beside the launch cadence, never a cap: 19,995 satellites for the
  small terminal. Inside the horizon the launch cadence binds every class.
- **The devices.** The small terminal gets 2 Mbps while active (about 10
  off-peak), the mounted terminal 5 (about 13.4). A better antenna does not
  widen the spectrum: it cleans the signal so each wave-change carries more
  bits. The terminals and IoT need no one's permission. Phones and voice are a
  later, separate model that needs a phone chip for the band.
- **Never added.** The two cases never add, and neither do the two
  applications: both fly the same 301 Neutron launches through FY2036, each as
  if it had the ramp to itself.

The full case, with every number traced:

- [communications/conclusion.md](communications/conclusion.md): the verdict, both cases side by side, IoT's room, and the plan by date.
- [communications/assumptions.md](communications/assumptions.md): every dial of both models with its source class, including the all-in deployment posture.
- [communications/design.md](communications/design.md): the model-family structure, the saturation curve, and the promotion flow.
- [`models/iridium/default.json`](communications/models/iridium/default.json) and [`models/product_case/default.json`](communications/models/product_case/default.json): the two cases' promoted artifacts.

## Repository Map

```text
rklb_space_data_center/
├── README.md            # this file: the program and its applications
├── data_center/         # the data-center application (conclusion, structural case, guide, models)
├── communications/      # the communications application (conclusion, assumptions, design, promoted artifacts)
├── research/            # shared evidence wiki and source ledger
├── code/                # the model engine (rklb-value)
├── atlas/               # the agent map: pieces, flows, invariants (start at AGENTS.md)
└── docs/                # architecture decision records (ADRs)
```

## Running The Model

```sh
cd code
uv sync 2>&1 | tee /tmp/rklb_uv_sync.txt
uv run rklb-value scenarios/default.yaml --json | tee /tmp/rklb_model_output.json
uv run rklb-value --promote 2>&1 | tee /tmp/rklb_promote.txt
```

Pipe only stdout when saving the JSON; status and errors go to stderr.
`--promote` refreshes the JSON under `data_center/models/` and refuses, writing
nothing, if any validation check fails; the name `default` belongs to
`code/scenarios/default.yaml`, and any other scenario needs its own lowercase
`--output-name`. Promotion does not rewrite the
[conclusion](data_center/conclusion.md); after a model change, review the
artifacts and update the conclusion deliberately.

The communications models promote from `code/` too, the Iridium model first
and then the product case, which reads it:

```sh
uv run python -m communications.json_output scenarios/iridium.yaml \
    communications/models/iridium/default.json
uv run python -m product_case.json_output scenarios/product_case.yaml \
    communications/models/product_case/default.json
```

The Iridium command reads the promoted saturation curve; the curve's own
command, a long run, is in [communications/README.md](communications/README.md).

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

Released under the [MIT License](LICENSE). Copyright (c) 2026.
