"""Shared code imported by both the `data_center` and `communications` models.

The provenance/cell vocabulary and its strict unwrap (:mod:`common.provenance`),
the cadence spine (:mod:`common.cadence`: the launch ramp, the launch cost, their
dial blocks and defaults), the generic cohort cliff, the cold-reader contract
types, the file boundary (:mod:`common.file_io`: the one YAML loader, the one
artifact serializer, artifact writes that roll back on failure, the
source-checkout anchor, and the ``ModelFileError`` they raise), and the
command-line conventions (:mod:`common.cli`).

Downstream code imports from the submodule path (`from common.provenance import
...`, `from common.cohort import ...`), the codebase-consistent pattern; this
package `__init__` deliberately re-exports nothing.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
