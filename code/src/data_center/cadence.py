"""Re-export of the shared cadence machinery for ``data_center`` importers.

The launch-ramp and cadence-indexed launch-cost functions now live in
:mod:`common.cadence`. This module re-exports the names ``data_center`` code and
tests import from ``data_center.cadence``: the two public functions plus the
``_log_interp`` helper (used directly by ``tests/data_center/test_cadence.py``).
"""

from __future__ import annotations

from common.cadence import (
    _log_interp,
    compute_launch_cost_musd,
    compute_launches_per_year,
)

__all__ = [
    "_log_interp",
    "compute_launch_cost_musd",
    "compute_launches_per_year",
]
