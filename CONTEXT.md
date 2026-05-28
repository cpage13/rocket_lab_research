# Project Context Glossary

This glossary defines the terms agents should use when working in this
repository. It is deliberately short and operational: use these words in docs,
code comments, source ledgers, and execution notes unless a future ADR changes
the language.

## Core Terms

**Rocket Lab Research** - The repository-level umbrella for Rocket Lab-focused
research, modeling, communications, and future rocket-related investigations.
The current first investigation is data-center focused, but the repository scope
is broader. Avoid: treating "data center" as the repository name or full scope.

**data-center investigation** - The current first Rocket Lab Research
investigation, focused on Neutron-launched orbital AI inference as a business
wedge. Avoid: using this term for future communications or rocket research
tracks.

**space model** - The model estimating orbital AI-inference data-center
capacity, cost, revenue, and margin under default or scenario assumptions.
Avoid: "the calculator" when the public artifact or model contract is meant.

**ground reference model** - A comparison model estimating the five-year cost of
an equivalent ground data-center cohort. Avoid: "ground truth"; this is a
reference model, not a factual baseline.

**deployed-year cohort** - The new capacity deployed in a single year, used as
the anchor for the ground comparison. Do not confuse this with the living fleet
or with total market capacity.

**living fleet** - The active on-orbit installed base after accounting for
service life. It is cumulative active capacity, not same-year deployment.

**node** - The modeled compute payload unit. A node contains GPU packages plus
the supporting hardware it needs, but it is not the spacecraft bus. Avoid using
"rack" for the product unit unless discussing historical research wording.

**bus** - The spacecraft platform supporting the node, including power,
thermal, communications, and orbital service functions as modeled.

**default scenario** - The creator-selected assumption set in
`code/scenarios/default.yaml`. It is reviewable, replaceable, and not a claim
that Rocket Lab has announced those values.

**Neutron-centered scenario** - A data-center investigation scenario that uses
Neutron because it is the relevant Rocket Lab medium-lift vehicle for this
scale today. Electron is not modeled for the data-center case because it is not
a plausible fit for the required payload scale.

**promoted model** - The reviewed JSON artifact copied into
`data_center/models/...` for public use. The current default space artifact is
`data_center/models/space/default.json`.

**source status** - The evidence classification attached to claims and inputs.
The public taxonomy is `certified`, `sourced_estimate`, `derived_estimate`,
`projection`, `extrapolation`, `scenario`, `placeholder`, and `stale`.

**static conclusion** - The human-reviewed conclusion tied to the current
promoted default JSON. If the default scenario or promoted model changes, the
static conclusion must be reviewed before it is treated as current.

## Capacity Language

Use "deployed-year cohort" for a year's new orbital capacity, "living fleet"
for active installed orbital capacity, and "market reference" for external data
center capacity. Do not describe the modeled deployment as a market-share
thesis. The default 2036 deployment is a small annual cohort measured against a
large external market reference so readers can sanity-check scale.
