# Context: Rocket Lab Research

Live terms only (an entry for what an accepted ADR decided and no code has built yet says so); use these
words in documents, code comments and notes.

## Terms

### application
One modeled orbital business with its own folder of reviewed documents and promoted JSON.
- **Avoid:** investigation, workstream, venture

### feasibility study
An application's whole case: the thesis in `research/vision/`, its research, the model, the verdict.

### engineering case
What an engineering model answers: the most its fleet carries with every seat sold (the data-center model;
for communications, the Iridium model, which sells every seat of its people classes and is read beside the
product case, never added to it).
- **Relates to:** product case, full sell-through, all-in deployment

### product case
The communications market view (ADR 012), decided and not yet built: its own model on the Iridium model's
promoted JSON, of what the network would sell (the terminals and the two IoT classes) at the investor's prices
held flat; it never feeds the engineering model.
- **Relates to:** engineering case, minimal-packet IoT, data IoT

### the Iridium model
The communications family the repository publishes: the most the L-band Rocket Lab is acquiring with Iridium
can carry, every seat of the small terminal, the mounted terminal and the phone class sold on the fleet the
launch cadence builds.
- **Avoid:** Model B, direct-to-cell model
- **Relates to:** the three lanes, device class, full sell-through, minimal-packet IoT, data IoT, saturation curve

### High-Bandwidth Cellular Pure Play model
The second communications family (cellular spectrum to phones), on hold; the equality tripwire runs it beside
the Iridium model.
- **Avoid:** Model A

### the three lanes
Cellular (phones, cellular spectrum), broadband (a dish, Ku or Ka), MSS (devices, owned L-band): no claim crosses lanes.

### space model
The data-center model of orbital capacity, cost, revenue and margin by year (the space artifact).
- **Avoid:** the calculator

### ground reference model
The cost of a ground cohort equal to the anchor year's deployed-year cohort over its service life;
the anchor year is the base year plus ten, or the window's last year.
- **Avoid:** ground truth, parity

### node
The data-center unit: GPU packages (NVIDIA's as-sold unit) and their hardware on a bus, one per launch.
- **Avoid:** rack

### deployed-year cohort versus living fleet
A cohort is one year's deployment; the living fleet is the cohorts still in service, each retiring
at once when its life ends (the cohort cliff).

### revenue multiple (R)
The data-center rule: a cohort's revenue is its annualized full cost times R, so R sets the margin.

### margin
The percentage of revenue left after the full build and launch cost spread over the service life (in
communications, each class's own revenue against the year's whole living fleet's annualized cost); a dollar
figure is profit.
- **Avoid:** gross margin, gross profit

### device class
A tier of devices shown side by side with the others, never phone-first: the small terminal, the mounted
terminal and the phone class are the Iridium model's people classes (`DeviceClass`), and minimal-packet IoT and
data IoT are two more (ADR 011); IoT counts devices, never people, and no model sells every IoT seat (ADR 011).
- **Avoid:** phone users
- **Relates to:** minimal-packet IoT, data IoT

### minimal-packet IoT
The IoT device class that sends short messages only; with data IoT, a capacity in the engineering case, which
the Iridium artifact publishes (ADR 011), and a market in the product case (ADR 012), decided and not yet built.
- **Relates to:** data IoT, device class, engineering case, product case

### data IoT
The IoT device class that sends bursts of data beside its messages; with minimal-packet IoT, a capacity in the
engineering case, which the Iridium artifact publishes (ADR 011), and a market in the product case (ADR 012),
decided and not yet built.
- **Relates to:** minimal-packet IoT, device class, engineering case, product case

### frequency versus bandwidth
Frequency is where the signal sits (about 1.6 GHz); bandwidth, the width held (about 8 MHz), sets capacity.

### coverage floor
The fewest satellites for a quality link over the populated band (95 percent coverage); on the Iridium path it
is pinned at 340 and gates every sale (nothing is sold in a year whose living fleet is below it), while the
launch cadence sizes the fleet.
- **Relates to:** readings

### saturation
Where the owned spectrum serves few more people of a class (the small terminal, the mounted terminal or the
phone class) per added satellite: a knee, not a wall, measured by the class's saturation number.
- **Avoid:** saturation cap, the 2,000 cap (a reading: the retired cap)
- **Relates to:** saturation number, saturation curve, coverage floor

### saturation number
The spectrum bound of a people class (the small terminal, the mounted terminal or the phone class): the fleet
at which its elasticity of capacity first falls under 0.10 on the saturation curve, reported beside the launch
cadence and never a build target or a cap; a class whose rows never reach it has none, and the curve names the
last midpoint at which its rows measure the elasticity, the fleet it is not reached by
(`saturation_not_reached_by`).
- **Relates to:** saturation, saturation curve, maximum use

### saturation curve
The promoted `communications/models/iridium/saturation_curve.json`: for each of the three people classes, the
useful beams and capacity a shell of each fleet keeps lit over the places people live, computed once with the
band in full-time use at the 25 m^2 reference panel; the Iridium model reads its people from it.
- **Relates to:** useful beams, maximum use, ocean factor, panel factor, downlink share

### useful beams
L: the co-channel beams a fleet keeps lit over inhabited cells, a snapshot mean on a curve row; beams over ocean
and empty land carry no one.
- **Relates to:** ocean factor, maximum use

### maximum use
A people class's fleet-independent upper bound on useful beams, every inhabited cell served by the best
satellite the shell can ever offer it and capped by its people; reported beside the saturation number, it
places only the 90 percent marker.
- **Relates to:** useful beams, saturation number

### ocean factor
U: the share of a fleet's beams that land over people, its useful beams over all its beams (U = L / (N x B)).
- **Relates to:** useful beams

### panel factor
The scenario's panel area over the curve's 25 m^2 reference panel: it scales people, useful beams, capacity and
maximum use linearly, never the saturation numbers, the ocean factor or satellites per launch (ADR 005).
- **Relates to:** saturation curve

### downlink share
d: the share of the time-division duplex frame the downlink holds, a scenario setting (ADR 008); each people
figure and each class's downlink pool scale with it, each class's off-peak per-user rate follows the pool only
where the pool caps it, and the satellite's peak and each class's busy-hour per-user rate do not move with d. The
uplink holds the rest of the frame, 1 - d: IoT's uplink, payload and single-tone rooms scale with 1 - d and its
random-access room with neither (ADR 011). The curve is computed at d = 1.
- **Relates to:** saturation curve

### readings
The Iridium model's people, revenue and margin at four reported fleets: the coverage floor, 2,000 (the retired
cap, kept for comparison), the horizon-end full-cadence reach and the steady state beyond the horizon.
- **Relates to:** coverage floor, saturation

### marginal interval
A people class's interval between two of the curve's rows, with the people one more satellite adds there and
their revenue a satellite-year against a satellite-year's cost; the first interval below cost is where the
next satellite first stops paying for that class.

### treadmill
The cellular family's deployment rule (also "build-and-hold"): build to the fleet target, then replace each
retiring cohort; the Iridium model has no target and flies every launch its cadence share allows.

### full sell-through
Every seat sold: each year the small terminal, the mounted terminal and the phone class each serve every person
the living fleet carries, at the class's flat price, so revenue rises with the fleet; each class's column is the
whole fleet sold to that class alone, never summed (ADR 006).
- **Avoid:** take rate, adoption, capture

### all-in deployment
A case at the full modeled Neutron cadence, run as if it had the shared launch ramp to itself.
- **Relates to:** cadence spine, full sell-through

### cadence spine
The shared Neutron launch ramp and its cadence-indexed launch cost (`code/src/common/cadence.py`).

### equality tripwire
The test (`test_iridium_and_cellular_runs_share_the_fleet_and_cost_records`) that an Iridium run and a cellular
run whose fleet never reaches its target produce one shared fleet-and-cost record, its values frozen, so the
shared loop stays family-neutral and a change that moves both families alike fails.
- **Avoid:** parity test (the data-center golden trajectory's name)

### investor-set
A value the investor chose as a model input, labeled apart from sourced fact (status `scenario`).
- **Avoid:** investor-selected, creator-selected

### default scenario
The scenario a model publishes as `default`, sourced values and investor-set dials together.

### assumptions ledger
An application's stated assumptions (the investor's "assumptions document"): a row per dial in
communications; in the data center, a row per release-critical default or public claim.

### promoted JSON
A model output file (the code's "artifact") that promotion writes into `data_center/models/` or `communications/models/`.
- **Avoid:** promoted model, model JSON

### provenance cell
The wrapper on a data-center output value: value, unit, formula, uses, sources, status, description.

### claim ID
A row ID in `research/SOURCE_INDEX.md`, the source ledger (`RLDC-*`, `NTR-*`, `COMM-*` and others).
- **Avoid:** claim ledger, source index (for the file)
- **Relates to:** source status

### source status
The public evidence class of a claim or input; public documents never cite `placeholder` or `stale`.

## Ambiguities

- **gross.** The `gross_profit_*` fields, their query questions, the `--brief` headline and the cellular
  record's margin fields (`arpu_gross_margin_pct`, `cost_plus_gross_margin_pct`) say gross for a full-cost
  figure; read as gross, margins compare wrongly.
- **workstream, venture, application.** Folder front pages say workstream, docstrings and two test file names
  say venture, the charter and README mostly application: three words split search and prose.
- **saturation.** The public documents, until their rewrite, call the retired 2,000 cap the point where the
  spectrum saturates; in code 2,000 is only a reading and each people class's saturation number is derived,
  so agents would quote a cap as physics.
- **Sheet A, ARPU buckets.** Retired with the four-bucket revenue case (mix shares of one pool, a government
  bucket among them) yet still in the communications documents until their rewrite; the built model sells
  every seat of each people class at its own price.
- **floor.** The coverage floor (which gates every Iridium sale; the cadence sizes the fleet), the conservative
  floor (the most conservative published reading, shown but never leading), the phone class's price floor (no
  price haircut goes below it), the margin floors (rule V3 in the data center; the investor's floor on the
  whole communications business) and the product case's floors (ADR 012) are different things; name which.
- **terminal names.** Code's `mounted_terminal_class` is the mounted terminal and `small_terminal_class` the
  small terminal, which older prose calls "the puck": side-by-side tables need one name per class.
- **calculator.** Code docstrings call the data-center package a calculator; agents would call the
  promoted JSON calculator output.
- **founder.** Older research says founder; agents copy it, and the person is the investor.
- **rack.** Older research calls the unit a rack; agents would size it in racks, not GPU packages.
- **fleet, in communications.** The cellular family's fleet target, the readings' reported fleets and a year's
  living fleet (whose annualized cost is every Iridium margin's basis) differ, and the Iridium model has no
  target: name which fleet, or a margin is misstated.
- **source class, source status.** Constants use source classes (`INVESTOR_SET`, `ESTIMATE`), the
  ledgers source statuses; they do not map one to one, so never quote one as the other.
