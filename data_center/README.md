# Data Center Workstream

This folder holds the data-center application of Rocket Lab Research: a
Neutron-launched orbital AI-inference data center, modeled end to end. For the
verdict and the numbers, read the [conclusion](conclusion.md); for why those numbers are a floor and why Rocket Lab is uniquely positioned to build this, read [the structural case](structural_case.md). This page is the
guide to what is here and how to use it.

## Operating Picture

The unit is a node. GPUs and networking are integrated and tested on the ground,
packaged into a rack-like orbital node, attached to a Rocket Lab bus with solar,
radiators, thermal, and laser communications, launched on Neutron, and operated
as laser-linked orbital compute. The model picks a frontier GPU generation each
year, fits as many packages as the Neutron mass envelope allows, computes
per-node economics, and rolls the fleet up year by year.

## Why Neutron

Neutron is the enabler: it is the Rocket Lab vehicle that can carry this node to
orbit at the modeled cadence. It is also not the bottleneck. Launch is only
about 18% of total system cost, behind compute (about 30%) and solar plus
radiator (about 22% each). Any operator, on any rocket, still has to lift the
same mass, so a launch-price war is not where this is won or lost: even halving
Neutron's launch price moves the orbital-to-ground cost ratio only from about
1.92x to about 1.75x. The real leverage is in solar, radiator, and how much
compute each launch carries.

## Worth Knowing

None of this stack has been designed or iterated for space yet. The model
translates conservative ground assumptions into orbit, so read it as a floor
that should improve as real space hardware gets built. The
[conclusion](conclusion.md) covers the other angles: the vertical-integration
upside (Rocket Lab supplies most of the stack to itself), the cost-down
sensitivities, and why a premium customer might care.

## Reading Path

| Path | What it is |
|---|---|
| [conclusion.md](conclusion.md) | The verdict and the headline numbers. Start here. |
| [structural_case.md](structural_case.md) | The structural case: why Rocket Lab is uniquely positioned to build this, and why the numbers are a floor. |
| [assumptions.md](assumptions.md) | The default-assumption ledger and source-status taxonomy. |
| [models/space/default.json](models/space/default.json) | The promoted space model: every number with formula, units, and source. |
| [models/ground/default.json](models/ground/default.json) | The ground reference for the same 2036 cohort. |
| [CURRENT_STATE.md](CURRENT_STATE.md) | Short workstream handoff. |
| [../research/README.md](../research/README.md) | The evidence wiki and source ledger. |
| [../code/README.md](../code/README.md) | How to run, promote, test, and query the model. |

## Running The Model

From the repository root:

```sh
cd code
uv run rklb-value scenarios/default.yaml --json 2>&1 | tee /tmp/rklb_model_output.json
uv run rklb-value --promote 2>&1 | tee /tmp/rklb_promote.txt
```

`--promote` refreshes `models/space/default.json` and
`models/ground/default.json`. It does not rewrite [conclusion.md](conclusion.md);
after a scenario change, review the JSON and update the conclusion deliberately.

## Querying The JSON

Use `meta.query_examples` in the space JSON before writing a custom query. Every
leaf under `physical.years` and `business.years` is a provenance cell with
`value`, `unit`, `formula`, `uses`, `sources`, and `description`, and
`inputs.assumption_index` traces each model dial back to its source. Agents
should also read [../docs/agent-guide.md](../docs/agent-guide.md).

Communications is a separate, future workstream; see
[../communications/README.md](../communications/README.md). It makes no
data-center claims in this release.
