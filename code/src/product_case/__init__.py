"""The product case: what the communications network would sell, its own model (ADR 012).

The investor's "Phase B": a separate case, beside the engineering case and never added to it,
of what the network the Iridium model builds would sell at the investor's prices held flat:
the small terminal, the mounted terminal, minimal-packet IoT and data IoT, side by side, never
phone-first. It reads only the engineering model's promoted artifact
(``communications/models/iridium/default.json``, schema ``iridium-v7``), as JSON, its schema
pinned and its SHA-256 recorded; nothing it computes feeds the engineering model. It imports
``common`` alone, never ``communications`` or ``data_center``.

What it is not: never an input to the engineering model; IoT's customers always from the
demand curve in every market and year, never a set count; never a price lower than the
investor's in the case it adopts (lower prices appear only as context).

**The method, nine steps** (each a formula of :data:`~product_case.constants.FORMULA_CATALOG`;
t a reported year, c a class):

1. The network (:mod:`product_case.engineering`): the class split s from today's terminal mix
   as beams; the seats S_small = s x P_small(t) and S_mounted = (1 - s) x P_mounted(t); the
   network's scale k(t) = (S_small + S_mounted) / 418,100; IoT's rooms R(t), A(t), T(t) and the
   phone class's beams L(t), as published.
2. The offers (:mod:`product_case.offers`): each price on its line from the start price, the
   candidates holding every start price; each IoT usage path x its scale's line factor, rounded
   half up; the service v_c(t); the per-device loads.
3. The demand curve, D_c = N_c x k^gamma x (A_c / p_c)^epsilon x v_c^eta, anchored on Iridium's
   customers and ARPU today (COMM-617, COMM-618; data IoT beside them, COMM-726).
4. Sold: a terminal floor(min(D, S)); an IoT class floor(D), uncapped.
5. A year's numbers: the beams filled, revenue, the margin against the fleet's annual cost,
   profit, IoT's uplink, access and single-tone uses, the GB carried and the cost per GB.
6. Usable: every year's fill and margin at their floors, every IoT use at most 1, revenue
   strictly rising; a market records each test it fails.
7. Each choice over the drawn markets (:mod:`product_case.monte_carlo`): its usable draws, the
   medians of its summed and last-year revenue, its central market's revenue.
8. The fronts and the pick: the highest median among the candidates usable in at least the
   robust floor's share of the markets, else the most usable candidate, warned, else no pick.
9. The headline, the pick at the central market (each response at the middle of its range),
   and the pick's spreads over its usable draws and all draws, with the headline's rank.

**What stops the usage.** Every candidate shares the terminals' fill, so IoT's own failures may
take only the markets between the fill's share and the robust floor: the pick's usage rises
while its median rises and its share holds above the floor, and stops at whichever comes
first; it can move in steps with a price or a terminal change, never the prices.

**The investor's words that set the rules**, verbatim and dated. The method's own rules: the
case kept apart from the engineering model (2026-10-05: "you don't want to mix your market with
your engineering and your production ... Keep it separate"); the demand curve on cost and
service (2026-10-06: "This will be a curve based on cost and on what kind of service you are
giving them"); the four classes side by side (2026-10-06 18:26: "There is a small terminal, there
are two classes of IoT, and then there is the mounted terminal"); the usage raised until the
network is used, the Pareto front and the Monte Carlo (2026-10-06 18:26: "If we barely use any of
the network, then we just increase usage as is, right? Right. So we just do a Pareto. That is why
we do the Monte Carlo and see what makes sense"); IoT uncapped (2026-10-06 16:58: "Would I cap the
data IoT? No, I don't think so. ... I don't think there's any reason to cap the data"). The
values: the prices held flat (2026-10-06 19:38: "The prices will not go down, but they will not go
up"); IoT at $3 and $6 (2026-10-06 19:52: "Let's go with the three and six for now"); the
terminals at $10 and $50 (2026-10-07: "Yes, let's use the $10 and $50. Let's do that"); the margin
floor (2026-10-07: "I think about a 50% floor for margin"); the FY2036 usage (2026-10-12 15:56: "go
with 9 GB, 90 GB and 13 bursts"). And this documentation (2026-10-06: "As long as we have all of
this documented clearly in the code section, with the Monte Carlo documented based on the
guidelines of the repository, we can proceed"). Each other value's basis and words are in its
constant's docstring and its row (COMM-722 to COMM-726).

**How to run it**, from ``code/`` (:mod:`product_case.json_output`; the engineering artifact is
promoted first, then the product case, every time):

    uv run python -m product_case.json_output scenarios/product_case.yaml \\
        communications/models/product_case/default.json [--version-stamp STAMP]

or, in code, ``run_product_case(load_product_case_config(path), view)``
(:mod:`product_case.engine`).

**Where each number goes:** the inputs to ``inputs`` (scenario values, constants, the values read
from ``iridium-v7``); the network to ``network``; each choice's summary to ``choices``; the
fronts and the pick to ``fronts`` and ``pick``; the headline's numbers to ``headline``, each a
provenance cell; the spreads to ``spreads``; the formulas, the checks (:mod:`product_case.checks`),
the data dictionary and the worked queries to ``meta``; the stated assumptions to
``assumptions``.

**Determinism.** The same scenario and engineering artifact give the same bytes on this
platform: the draws are the standard library's promised stream, and numpy's float64 power
equals Python's here; another platform's vectorized power could move a floor at a near-whole
demand by one (the module docstring of :mod:`product_case.monte_carlo` says how).

The modules: :mod:`product_case.constants` (the named constants, the enums and the formula
catalog), :mod:`product_case.config` (the frozen scenario config, its loader and each input's
cell spec), :mod:`product_case.engineering` (the one reader of the engineering artifact, and the
network it gives each reported year), :mod:`product_case.offers` (the choice grid, and each
choice's prices, usage, service and per-device loads, before any market),
:mod:`product_case.monte_carlo` (the markets drawn, each choice judged over them and at the
central market, the fronts, the pick and its spreads: the one module that imports numpy),
:mod:`product_case.checks` (believability, the warnings and the invariants),
:mod:`product_case.engine` (the entry) and :mod:`product_case.json_output` (the artifact and the
command). The scenario is ``code/scenarios/product_case.yaml``; its values are labeled in
``research/SOURCE_INDEX.md``, rows COMM-722 to COMM-726.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
