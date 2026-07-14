# Project Context Glossary

This glossary defines the terms agents should use when working in this
repository. It is deliberately short and operational: use these words in docs,
code comments, source ledgers, and execution notes unless a future ADR changes
the language.

## Core Terms

**Rocket Lab Research** - The repository-level umbrella for Rocket Lab-focused
research, modeling, communications, and future rocket-related investigations.
Two applications are modeled: the data-center investigation and the
communications application (the Iridium model). Avoid: treating "data center"
as the repository name or full scope.

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

**default scenario** - The investor-selected assumption set in
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

## Communications Terms

**communications application** - The second modeled application: model
families organized by communication paradigm under `communications/`. The
first family is the Iridium model. Avoid: "Model B" except as a historical
alias.

**the Iridium model** - The maximum practical performance of Iridium's owned
L-band on a Neutron-launched next-generation fleet: the promoted default is
`communications/models/iridium/default.json`. Avoid: calling it a
direct-to-cell or unmodified-phone model; it is the MSS lane.

**High-Bandwidth Cellular Pure Play model** - The kept second family (formerly
Model A): phones on cellular spectrum versus ground. Its defaults are the
shared config defaults; the equality tripwire test rides them.

**the three lanes** - Cellular (unmodified phones on cellular spectrum),
broadband (a dish on Ku/Ka), and MSS (purpose-built or in-chipset devices on
Iridium's owned L-band). Never blur them; a claim true in one lane is not a
claim about another.

**frequency versus bandwidth** - Frequency is where the signal sits on the
dial (~1.6 GHz for Iridium); bandwidth is the width held (~8 MHz exclusive,
10.5 coordinated). Capacity comes from the width, reach from the position.
Avoid: quoting either number as if it were the other.

**beam pool** - The per-beam data pool (bandwidth times spectral efficiency,
5.2 Mbps at phone class on 8 MHz) and the hard per-person ceiling. The
satellite total (about 150 beam reuses) multiplies people served, never one
person's rate.

**subscribers versus IoT devices** - Subscribers are people; IoT are devices.
They are counted separately and never summed. With the ARPU case on, the
published IoT count derives from the revenue mix.

**ARPU buckets (Sheet A)** - The published four-bucket revenue case (standard
personal, premium tier, IoT devices, government): investor-set mix percentages
over one capacity-anchored pool plus investor-set prices, all scaling with the
satellite count. The premium tier is a price tier, never a platform adoption
claim.

**equality tripwire** - The frozen test asserting the Iridium baseline and the
cellular default share the same trajectory on config defaults. It proves the
shared machinery; scenario overrides (the flat cost dials) deliberately do not
touch it.
