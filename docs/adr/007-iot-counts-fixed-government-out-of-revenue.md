# 007 - IoT Counts Are Fixed At The Coverage Floor; Government Is Left Out Of Revenue

Status: Superseded by ADR 011 (2026-10-12)

## Context

The revenue pool anchored IoT and government to the built fleet's people
capacity. Growing the fleet for people would then multiply IoT devices,
although satellites built to carry people create no IoT customers, and a
density-based count would also move with the device class, the spectrum and
the aperture. IoT is bound by coverage and access, not capacity: even at the
coverage floor, on the default panel, it uses a small share of a beam's
uplink bits and tones, and less at larger fleets (`default.json`'s IoT check
carries the shares).

## Decision

IoT is two fixed lines, each its own revenue line (2026-10-04):
minimal-packet IoT, at the capable count (the investor, 2026-10-04): today's
model's Sheet A IoT count at the 340 coverage floor, held as a stated
assumption, not Iridium's own IoT book (COMM-617); and data IoT, at half that
count at double the price, in proportion (the investor, 2026-10-04). Each
count is a named constant rather than a setting (`default.json`'s
`fixed_books` carries them). The floor itself is
pinned at 340 on the Iridium path, since it belongs to the fixed shell and
the counts are sized at it. The counts do not scale with the fleet, the
people curve, the device class, the spectrum, the panel or satellites per
launch. Neither IoT line is ever inside a device class's margin, and both
start in the first year the living fleet reaches the coverage floor, since
IoT needs continuous coverage. Government is left out of revenue
(2026-10-04): the model carries no government count, price or line, and
the conclusions mention the EMSS contract.

## Consequences

Growing the fleet moves only the people classes, so the books stay flat
instead of rising with the fleet. The published mix no
longer holds fixed percentages over one pool, so the ARPU glossary entry is
rewritten. With government out, no view carries a government line; the
conclusions name the contract so a reader can extrapolate.
