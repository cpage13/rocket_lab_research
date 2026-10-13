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

The modules, as built so far: :mod:`product_case.constants` (the named constants, the enums
and the formula catalog), :mod:`product_case.config` (the frozen scenario config, its loader
and each input's cell spec), :mod:`product_case.engineering` (the one reader of the
engineering artifact, and the network it gives each reported year) and
:mod:`product_case.offers` (the choice grid, and each choice's prices, usage, service and
per-device loads, before any market). The scenario is ``code/scenarios/product_case.yaml``; its
values are labeled in ``research/SOURCE_INDEX.md``, rows COMM-722 to COMM-726.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
