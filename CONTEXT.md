# Context: Rocket Lab Research

Live terms only; use these words in documents, code comments and notes.

## Terms

### application
One modeled orbital business with its own folder of reviewed documents and promoted JSON.
- **Avoid:** investigation, workstream

### feasibility study
An application's whole case: the thesis in `research/vision/`, its research, the model, the verdict.

### the Iridium model
The communications family: the most the L-band Rocket Lab is acquiring with Iridium can carry.
- **Avoid:** Model B, direct-to-cell model
- **Relates to:** the three lanes, device class, saturation

### High-Bandwidth Cellular Pure Play model
The second communications family (cellular spectrum to phones), on hold; the equality tripwire runs on its defaults.
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
The percentage of revenue left after the full build and launch cost (in communications, replacement
too) spread over the service life; a dollar figure is profit.
- **Avoid:** gross margin, gross profit

### device class
A device tier shown side by side with the others (IoT, phone class, small terminal, mounted
terminal); the engine computes three radio tiers, and IoT counts devices, never people.
- **Avoid:** phone users

### frequency versus bandwidth
Frequency is where the signal sits (about 1.6 GHz); bandwidth, the width held (about 8 MHz), sets capacity.

### coverage floor
The fewest satellites for a quality link over the populated band (95 percent coverage).

### saturation
Where the owned spectrum serves no more people in a device class; an inherited cap stands in today.
- **Avoid:** saturation cap, for a derived bound
- **Relates to:** coverage floor, device class

### treadmill
The communications fleet engine (also "build-and-hold"): build to the target, then replace each retiring cohort.

### ARPU buckets (Sheet A)
The published Iridium revenue case: four buckets (standard, premium, IoT, government) as mix shares
of one capacity pool, times investor-set prices; the buckets are not the device classes.

### full sell-through
Every seat sold: each slot the built fleet can serve is sold, so revenue rises with the fleet.
- **Avoid:** take rate, adoption, capture

### all-in deployment
A case at the full modeled Neutron cadence, run as if it had the shared launch ramp to itself.
- **Relates to:** cadence spine, full sell-through

### cadence spine
The shared Neutron launch ramp and its cadence-indexed launch cost (`code/src/common/cadence.py`).

### equality tripwire
The frozen test that, on config defaults, the Iridium family and the cellular default share one trajectory.
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

- **gross.** The `gross_profit_*` fields, their query questions, the `--brief` headline and the
  communications margin fields say gross for a full-cost figure; read as gross, margins compare wrongly.
- **workstream, application.** Folder front pages say workstream, the charter and README mostly
  application: two words split search and prose.
- **saturation.** Public prose calls the inherited 2,000 cap the spectrum's saturation; agents
  would quote a cap as physics.
- **floor.** The coverage floor sizes the Iridium fleet; the conservative floor is the most conservative
  published reading (such as the Iridium phone-class figures), shown but never leading; mixing them misreads both.
- **terminal names.** Code's `terminal_class` is the mounted terminal; the small terminal is also
  "the puck": side-by-side tables need one name per class.
- **calculator.** Code docstrings call the data-center package a calculator; agents would call the
  promoted JSON calculator output.
- **founder.** Older research says founder; agents copy it, and the person is the investor.
- **rack.** Older research calls the unit a rack; agents would size it in racks, not GPU packages.
- **fleet, in communications.** The fleet target, the built fleet (the margin's basis) and the
  living fleet differ when a build falls short; mixing them misstates the margin.
- **source class, source status.** Constants use source classes (`INVESTOR_SET`, `ESTIMATE`), the
  ledgers source statuses; they do not map one to one, so never quote one as the other.
