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

In June 2026 Rocket Lab agreed to buy Iridium. The deal is expected to close
in mid-2027. Iridium owns about 8 MHz of L-band radio spectrum near 1.6 GHz,
coordinated worldwide (COMM-611). That band holds through rain, clouds and
trees. It carries a decent, reliable link where higher frequencies struggle:
voice, text, maps, photos, music, AI-agent traffic and IoT devices. It is not
built for video. It is first an IoT network.

The model asks what that spectrum could do on a new fleet launched by Neutron.
Each satellite has a flat antenna panel of 15.4 square meters and laser links
to the others. Sixteen fit on one Neutron launch, with Neutron's block upgrade
assumed. Today's Iridium fleet is 66 satellites, launched 2017 to 2019.
Together they move about 174 Mbps, less than one home internet connection
(COMM-639).

The answer for FY2036, in the typical market:

| FY2036 | Amount |
|---|---:|
| Revenue a year | $13,156.2M |
| What the fleet costs a year (build, launch and replace) | $1,554.4M |
| Profit a year | $11,601.8M |
| Margin | 88.2 percent |

About four fifths of the revenue is IoT. The prices are the investor's, and
they stay flat: $10 a month for the small terminal, $50 for the mounted
terminal, and $3 and $6 for the two IoT classes.

- **The fleet.** In this case every Neutron launch carries these satellites.
  Neutron's launch rate ramps up to 90 a year by FY2036. Each satellite lasts
  five years. Nothing is sold until 340 satellites are flying, enough for
  continuous coverage where people live (the coverage floor). The fleet passes
  that in FY2031, with 528 satellites. By FY2036 it flies 4,288.
- **Two cases, never added.** The product case is what the network would
  sell. The table above is its typical market: each customer response at the
  middle of its range. It passes every test (at least a 50 percent margin, the
  terminals filled, IoT within its room, revenue rising) in 1,744 of the 2,000
  markets the model draws. The engineering case is the most the fleet could
  carry. It gives the whole fleet to one kind of customer at a time. In FY2036
  the small terminal alone would serve 24.6 million people for $2,952.8M a
  year, and the mounted terminal alone 3.5 million for $2,116.3M.
- **IoT's room.** In FY2036 the fleet's IoT capacity alone fits about 11.5
  billion minimal-packet devices. That is a capacity, not a forecast. The
  product case's devices use less than a third of it.
- **The devices.** The small terminal gets 2 Mbps while in use (about 10
  off-peak). The mounted terminal gets 5 Mbps (about 13.4 off-peak). Rocket Lab
  can build and sell both, and the IoT modules, without anyone's permission.
  Phones and voice need a phone chip that speaks this band, so they are a
  later, separate model.
- **Room to grow.** Through FY2036 the launch rate, not the spectrum, limits
  the fleet. For the small terminal, adding satellites keeps adding capacity
  until about 19,995 satellites (its saturation number).
- **Never added.** The two cases never add. Neither do the two applications:
  both use the same 301 Neutron launches through FY2036, each as if it had
  them all.

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
