"""rklb-value — a YAML-driven valuation calculator for Rocket Lab's orbital
AI-inference data-center venture, valued **standalone** (the data-center play
on its own, NOT Rocket Lab the whole company).

The GPU-first model drops the rack abstraction entirely and is built
around the GPU PACKAGE (NVIDIA's "as sold" unit):
each fiscal year picks a frontier generation, derives N packages that fit
under the selected Neutron SSO mass-envelope scenario, and computes per-node
economics from the package's all-in kW/kg/$/PF figures. The cycle-2 model
rolls the living fleet up by cohort (5-year cliff) and prices revenue as an
R band.

The GPU-first per-node formulas (the heart of the model):

    mass_per_pkg = kg/1000 + kW × (solar_t/kW + radiator_t/kW)
            N    = floor((mass_envelope − node_mass_fixed) / mass_per_pkg)
       node_kW   = N × kW/pkg
   compute_cost  = N × $/pkg
    node_total   = compute + bus + solar + radiator + launch_cost(cadence)
   cost_annual   = node_total / service_life
    revenue_R    = cost_annual × R(launch_year, band)

The public surface:

* :mod:`data_center.config`     — Pydantic config (gospel + slopes + v8 dial blocks).
* :mod:`data_center.generations` — `KNOWN_GENS`, `extend_generations`, `frontier_at`.
* :mod:`data_center.engine`     — the GPU-first engine + `run_valuation`.
* :mod:`data_center.output`     — typed Pydantic v8 output models.
* :mod:`data_center.json_output` — v8 output assembly + JSON serialiser.
* :mod:`data_center.text_report` — human-readable text rendering.
* :mod:`data_center.cli`        — the `rklb-value <config.yaml>` entry point.

Units: money in $M; time in project years. Year 0 = FY2026 (Neutron's
first-flight year).
"""

from __future__ import annotations

from .conclusion import render_conclusion_markdown
from .config import ValuationConfig, load_config
from .engine import run_valuation
from .output import SpaceModelOutput, ValuationOutput

__all__ = [
    "SpaceModelOutput",
    "ValuationConfig",
    "ValuationOutput",
    "load_config",
    "render_conclusion_markdown",
    "run_valuation",
]
