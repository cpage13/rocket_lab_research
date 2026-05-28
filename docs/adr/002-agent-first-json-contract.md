# 002 - Agent-First JSON Contract

Status: Accepted

## Context

The repository is meant to be read by humans and agents. A promoted model that
only exposes final numbers forces agents to reverse-engineer formulas, units,
sources, and assumptions from code.

## Decision

Promoted JSON is the canonical machine-readable artifact. It must carry typed
inputs, outputs, provenance cells, source statuses, validation metadata, data
dictionaries, formula definitions, and query examples.

## Consequences

The JSON is larger than a simple report, but a cold reader can inspect it
without reading code. Public docs can cite stable JSON paths instead of copying
untraceable numbers.
