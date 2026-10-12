# 005 - The Iridium Spectrum Bound Is Derived From Saturation; The 2,000 Cap Retires

Status: Accepted (2026-10-04, with the saturation module's strategy, Revision 4)

## Context

The Iridium model inherited a 2,000-satellite cap set for the cellular family.
Nothing derived it for Iridium's 8 MHz of owned L-band. A capacity-maximizing
fleet keeps adding useful co-channel beams over populated land until every
populated place is served by its best beam, so saturation is a knee, not a
wall. The Iridium fleet grows at the comms share of the launch cadence
(ADR 006).

## Decision

The 2,000-satellite cap is retired for Iridium. Each device class's spectrum
bound is its saturation number: the fleet at which one more satellite adds
less than 10 percent of an average satellite's capacity (the elasticity of
capacity under 0.10), measured against the N-independent maximum use,
computed per class by the `saturation` module at the 25 m^2 reference panel
and the exclusive 8 MHz, with the band in full-time use (ADR 008). It is
reported beside the launch cadence in every run, never a build target and
never a cap on the build. A fleet past a class's saturation number is read
from the curve like any other; a fleet past the curve's last computed row is
refused with an error. When a class's marker is not reached on the grid,
that class has no spectrum bound. 2,000 stays only as a reading, labeled the
retired cap, for comparison.

## Consequences

Each class's derived bound lies far beyond the fleet the all-in cadence holds
at the horizon's end and at the steady state beyond it, so the launch
cadence, not spectrum, bounds every modeled year: `saturation_curve.json`
carries the bounds, and `default.json` the fleets, each class's binding
limit and the readings. The curve is computed at 25 m^2 and 8 MHz. The panel
is one linear setting (`aperture_m2`, its default the validated Flatellite
body, 15.4 m^2): capacity per satellite scales with the panel over 25 m^2,
and the saturation numbers do not move. Satellites per launch is a direct
scenario value, no longer coupled to the panel. The coordinated 10.5 MHz,
linear in spectrum, is a conclusions note, not an input.
