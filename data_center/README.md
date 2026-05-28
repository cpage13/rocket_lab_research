# Data Center Workstream

This folder is the public home for the orbital AI-inference data-center
workstream. The question is whether Rocket Lab should seriously explore
Neutron-launched orbital compute as a business wedge: a repeatable machine for
building, launching, and operating AI-inference infrastructure in space.

The workstream estimates annual deployed capacity, living-fleet capacity, cost,
revenue, gross profit, and margin under reviewable default assumptions. It is
designed for two readers at once: a skeptical human scanning the conclusion and
an agent querying the JSON directly.

The operating picture is concrete. GPUs and networking hardware are integrated
and tested on the ground, packaged into rack-like orbital nodes, attached to a
Rocket Lab-built bus with power, thermal, and communications, launched on
Neutron, and operated as laser-linked orbital capacity. The business thesis is
that Rocket Lab's vertical integration can turn bus, solar, radiator, launch,
integration, and operations from purchased services into controlled cost,
manufacturing learning, and infrastructure leverage.

That point should be read strongly. The default model uses many lines that look
like external buy prices or customer-facing prices. A Rocket Lab-operated
program would make Rocket Lab the internal customer for much of its own stack:
bus, solar, radiator and thermal hardware, integration, Neutron launch,
operations, and possibly communications. The GPUs and some networking equipment
are the clearest outside purchases. The base case does not fully credit the
extra value of filling Rocket Lab's own factory, launch manifest, and operations
pipeline with repeatable demand.

The modeled product is inference, not frontier-model training. The default is a
conservative translation of public terrestrial AI-hardware assumptions into an
orbital setting; it should not be read as a final engineered space-optimized
architecture. Engineering-phase changes may improve the design space later, but
they are not silently baked into the current baseline model.

Neutron is the current focus because it is the relevant Rocket Lab vehicle for
this scale today. Electron is not modeled for the data-center investigation,
and future heavier-lift Rocket Lab architectures should get their own scope
once they have evidence worth modeling.

## Reading Path

| Path | What it is |
|---|---|
| [conclusion.md](conclusion.md) | Plain-English conclusion for the current baseline model. |
| [assumptions.md](assumptions.md) | Human-readable default-assumption ledger and source-status taxonomy. |
| [models/space/default.json](models/space/default.json) | Current baseline space-model JSON with inputs, outputs, provenance, validation, and query examples. |
| [models/ground/default.json](models/ground/default.json) | Current ground reference JSON for the same 2036 deployed-year cohort. |
| [CURRENT_STATE.md](CURRENT_STATE.md) | Short handoff for the current workstream state. |
| [../research/README.md](../research/README.md) | Research corpus and source ledger entry point. |
| [../code/README.md](../code/README.md) | Commands for running, promoting, testing, and querying the model. |

## Current Default In Plain English

The current baseline space model is generated from
`code/scenarios/default.yaml`. The story is a ramp, not a one-year miracle. By
the middle years, cadence has moved out of prototype territory and the central
case is already gross-margin positive. The takeoff year is **2036**: **90
launches**, **90 new nodes**, and about **38 MW** of new orbital node power
added in that year alone. That is where the model starts to look like a scaled
infrastructure business rather than a demonstration.

The revenue run-rate is a separate 2036 view. By that same year, the active
on-orbit base reaches **268 nodes** and about **112 MW**, producing roughly
**$5.94B** in annual revenue and **$1.74B** in annual gross profit at about
**29%** gross margin. Do not merge those two statements. The 90-launch cadence
is the annual deployment story; the active on-orbit base is the installed-base
revenue story.

The default also uses a block-upgrade Neutron SSO mass-envelope scenario, a
five-year service life, and a central revenue multiple anchored at 1.5x cost
that tapers to a 2036 central output near 29 percent gross margin. Those are
source-marked scenario inputs in the assumptions ledger and promoted JSON, not
loose guesses.

The important scale distinction is annual added capacity versus active on-orbit
capacity. The current default adds about **38 MW** of new orbital node power in
**2036**, rounded elsewhere to about **40 MW/year**. The active on-orbit base
in that same year is about **112 MW**. Against a rough **100 GW** market
reference, this is a small sanity-check slice, not an extreme market-capture
claim.

The model does not imply Rocket Lab has committed to this project, that the
scenario assumptions are official Rocket Lab numbers, or that exact TAM capture
has been proved.

## Ground Reference

The ground reference exists to check rough cost scale for the same 2036
deployed-year GPU cohort. It is not a precise parity model. The current ground
artifact labels the comparison `same_order_of_magnitude`
after linking each ground input to the research wiki source ledger. Its current
output says the five-year ground reference is about **$3.68B** while the
orbital build-and-launch reference is about **$7.05B**. Treat that as a
source-backed order-of-magnitude screen, not as parity or as a site-specific
ground quote.

## Cost Premium And Upside Levers

Under the current default assumptions, the 2036 orbital cohort costs about
**1.92x** the comparable five-year ground reference. If both ground and orbital
providers target the same margin, an orbital token would need to cost roughly
90 percent more than a comparable ground token. That is not a separate
secure-compute markup. It is the modeled cost difference from launching and
supplying orbital power and thermal rejection for the same GPU/package cohort.

The default is intentionally cautious on solar and radiator cost. It uses
`$40k/kW` for solar and `$40k/kW` for radiator
(`RLDC-SOLAR-RADIATOR-COST`). Current research supports `$20k/kW` as a
plausible 2036 sensitivity for solar and as a useful, weaker sensitivity for
radiator. If both solar and radiator costs move toward `$20k/kW`, the modeled
ratio falls from about 1.92x ground to about 1.50x ground
(`RLDC-SOLAR-RADIATOR-COSTDOWN-SENSITIVITY`). In customer terms, that is roughly
a 50 percent token premium instead of roughly 90 percent.

Thermal-path improvements are a separate lever
(`RLDC-THERMAL-PACKAGE-DENSITY-SENSITIVITY`). If better chip-to-coolant and
coolant-to-radiator design allows a hotter radiator path while preserving
GPU/HBM junction reliability, the freed mass can be spent on more packages,
redundancy, or margin. A rough 2036 sensitivity suggests that adding three to
four packages per node would increase the 90-node annual cohort from 3,330
packages to roughly 3,600-3,690 packages, or about 8-11 percent more deployed
package capacity for the same launch count.

## Strategic Rationale

The reason to keep exploring is not just one model headline. This is a way to
make Rocket Lab's integration advantages matter. A steady data-center
deployment program could create repeatable Neutron demand, manufacturing
rhythm, launch operations learning, bus and thermal production learning,
supplier pressure, and customer proof. If Rocket Lab later moves the product
onto a larger vehicle, the pipeline would not start from zero.

That is a major selling point: build the cadence, build the industrial base,
earn decent revenue and margin, and keep Neutron reliably booked while Rocket
Lab consumes its own spacecraft and launch products. The model already shows a
business case without assigning a special bonus to that internal-customer
effect.

The customer story is also broader than raw compute. Space may be valuable
because it avoids some terrestrial siting fights around land, water, grid
interconnect, permitting, and local politics. Once deployed, the orbital system
runs on sunlight rather than drawing from a contested local grid. Physically
separated infrastructure may matter for sovereign, defense, high-security, or
dedicated-capacity workloads. Laser links, narrowband links, RF paths, or other
purpose-built connectivity can become part of a premium service package.

These are strategic reasons a premium customer may care. The JSON and source
ledger keep the evidence trail inspectable while the README shows the machine:
ground integration, Rocket Lab hardware, Neutron launch, orbital operations,
customer revenue, cadence learning, and a path to lower cost.

## Refinement Roadmap

The current baseline is the reference case. The next work is to sharpen and
extend it, not to rescue it. Useful follow-on passes include launch-cost and
cadence sensitivities, Neutron SSO and block-upgrade payload cases, solar and
radiator cost-down scenarios, GPU/HBM thermal-operation and reliability checks,
and radiation-shielding sizing against the much larger solar and radiator mass
stack. On the ground side, the refinement path is to split rack-side
power/networking, cooling, and operations/support scopes more cleanly while
preserving the current research-backed comparison.

## Running And Promoting

From the repository root:

```sh
cd code
uv run rklb-value scenarios/default.yaml --json 2>&1 | tee outputs/data_center/runs/default.json
uv run rklb-value --promote 2>&1 | tee /tmp/rklb_promote.txt
```

The `--promote` command refreshes `data_center/models/space/default.json` and
`data_center/models/ground/default.json`. It does not rewrite
`data_center/conclusion.md`; after a default scenario change, review the JSON
and then update the conclusion deliberately.

## Agent Notes

This is the technical audit section. Raw JSON paths are appropriate here
because the reader is checking the model directly; public-facing prose above
uses human labels and `RLDC-*` claim IDs.

Use `meta.query_examples` in the space JSON before inventing a custom query.
Every leaf value under `physical.years` and `business.years` is a provenance
cell with `value`, `unit`, `formula`, `uses`, `sources`, and `description`.
Use `inputs.assumption_index` to trace model dials back to source IDs and
rationale.

Agents should also read [../docs/agent-guide.md](../docs/agent-guide.md) for
the canonical repository navigation path and research wiki map.

Communications is related but separate. The top-level
[communications](../communications/README.md) folder is reserved for a future
researched workstream and makes no data-center model claims in this release.
