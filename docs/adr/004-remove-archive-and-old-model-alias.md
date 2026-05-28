# 004 - Remove Archive And Old Model Alias

Status: Accepted

## Context

The public repository used to carry stale archive material and an older flat
model alias. Those paths made it too easy for readers or agents to treat
superseded outputs as current.

## Decision

Git history is the archive. The public tree keeps only current workstream
artifacts by default. The promoted default space model lives at
`data_center/models/space/default.json`; the old flat model alias is not
restored.

## Consequences

Links and docs must use the new model paths. Removing the alias creates a clean
public contract and prevents stale path drift, at the cost of requiring older
references to be updated.
