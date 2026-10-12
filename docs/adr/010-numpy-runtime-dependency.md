# 010 - numpy Is A Runtime Dependency Of The Communications Code

Status: Accepted (2026-10-04, with the saturation module's strategy, Revision 4)

## Context

The code depended only on pyyaml and pydantic. The saturation module
allocates beams across millions of satellite-cell pairs per snapshot and ships
its population grid as a numpy archive.

## Decision

numpy is a runtime dependency. scipy is not: the exact linear-program check,
which the module's allocation matches closely, stays a one-off validation in
the saturation module's research note,
`research/direct_communication/iridium_saturation_module.md`, which records
the gap.

## Consequences

One new dependency, declared in `pyproject.toml` and pinned in `uv.lock`. It
stays confined to the saturation module: no other module under `code/src/`
imports it, and `test_numpy_stays_inside_the_saturation_module` checks that the
other communications modules load without it (ADR 012 adds one module of the
product case). The allocation stays transparent and deterministic.
