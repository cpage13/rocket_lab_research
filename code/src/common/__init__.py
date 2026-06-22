"""Shared code imported by both the `data_center` and `communications` models.

The provenance/cell vocabulary, the cadence machinery, the generic cohort cliff,
and the cold-reader contract types.

Downstream code imports from the submodule path (`from common.provenance import
...`, `from common.cohort import ...`), the codebase-consistent pattern; this
package `__init__` deliberately re-exports nothing.
"""
