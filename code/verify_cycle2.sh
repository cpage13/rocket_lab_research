#!/usr/bin/env bash
# =============================================================================
# verify_cycle2.sh — end-of-cycle verification gauntlet for the v8 calculator
# =============================================================================
#
# Run from the calculator directory:  bash verify_cycle2.sh
#
# This is the reconciled end-of-cycle script for the v8 calculator, with the
# final cycle-2 validation corrections applied:
#
#   * The CLI is positional — `python -m data_center.cli scenarios/X.yaml`,
#     NOT `--scenario scenarios/X.yaml` (there is no --scenario flag).
#   * The V15 rule name is `volume_fits_horizon` — the ValidationCheck.name
#     values are descriptive, not `V<n>_`-prefixed.
#   * The greppable-enforcement block checks for the *actual defects*, not
#     blunt substring matches that trip on legitimate prose:
#       - `annual_rev_per_node_musd` — the dead cycle-1 field. The defect is
#         the FIELD existing (a Pydantic field definition / assignment), not
#         the name appearing in a docstring that documents the D25 rename.
#       - `r_revenue_cost` — the dropped legacy scalar. The defect is the
#         SCALAR config field existing, not the name appearing in V11's code
#         (V11 must name the literal string it forbids) or in docstrings.
#       - `cohort` — the defect is cohort *logic* (the `Cohort` class) leaking
#         out of fleet.py. `engine.py` legitimately orchestrates cohorts
#         (compute_fleet_trajectory; moving it to fleet.py would create a
#         circular import — Deviation D12). The lowercase domain word
#         "cohort" appears in many field descriptions and formula texts and
#         is not a defect.
#
# Exit 0 = "Cycle 2 PASS".
# =============================================================================
set -euo pipefail

cd "$(dirname "$0")"

SCENARIOS=(default conservative ambitious upside_7yr with_premium volume_stress)
NORMAL=(default conservative ambitious upside_7yr with_premium)

echo "== 1. Regenerate all 6 scenarios =="
for s in "${SCENARIOS[@]}"; do
  uv run python -m data_center.cli "scenarios/$s.yaml" --json > "outputs/data_center/runs/$s.json"
  echo "   $s.json"
done

echo "== 2. All V-rules pass on the 5 normal scenarios =="
for s in "${NORMAL[@]}"; do
  fails=$(jq '[.meta.validation.rules[] | select(.pass_check == false)] | length' "outputs/data_center/runs/$s.json")
  [ "$fails" = "0" ] || { echo "FAIL: $s has $fails failing V-rules"; exit 1; }
  echo "   $s: 0 failing rules"
done

echo "== 3. V15 (volume_fits_horizon) fires on volume_stress =="
v15=$(jq '.meta.validation.rules[] | select(.name == "volume_fits_horizon") | .pass_check' outputs/data_center/runs/volume_stress.json)
[ "$v15" = "false" ] || { echo "FAIL: volume_fits_horizon should fire on volume_stress"; exit 1; }
echo "   volume_fits_horizon pass_check=false (fires as designed)"

echo "== 4. All 12 query_examples execute on default =="
for name in headline_2036_revenue_central headline_2036_profit_central \
            margin_band_2036 trajectory_revenue_central trajectory_launches \
            living_fleet_per_year cumulative_revenue_to_2036_central \
            gen_mix_by_year mass_binding_check volume_binding_check \
            trace_a_cell validation_pass_fail; do
  expr=$(jq -r ".meta.query_examples[] | select(.name == \"$name\") | .jq" outputs/data_center/runs/default.json)
  [ -n "$expr" ] || { echo "FAIL: query_examples.$name missing"; exit 1; }
  jq "$expr" outputs/data_center/runs/default.json > /dev/null || { echo "FAIL: query_examples.$name jq errored"; exit 1; }
done
echo "   12/12 query_examples execute"

echo "== 5. mypy --strict + ruff + format =="
uv run mypy --strict src/
uv run ruff check src/
uv run ruff format --check src/

echo "== 6. Test count (strategy F9 target: >= 220) =="
count=$(uv run pytest --collect-only -q 2>&1 | tail -1 | awk '{print $1}')
[ "$count" -ge 220 ] || { echo "FAIL: test count $count < 220"; exit 1; }
echo "   $count tests collected"

echo "== 7. Greppable enforcement (reconciled — genuine defects only) =="

# 7a — no CYCLE-1-LEGACY markers anywhere (hard rule, unchanged).
if grep -rn --include='*.py' "CYCLE-1-LEGACY" src/; then
  echo "FAIL: CYCLE-1-LEGACY marker found"; exit 1
fi
echo "   7a no CYCLE-1-LEGACY markers"

# 7b — no bare `Any` import lacking a `typing-acceptable` justification.
if grep -rn --include='*.py' "from typing import.*Any" src/ | grep -v "typing-acceptable"; then
  echo "FAIL: unjustified bare Any import (add a # typing-acceptable comment)"; exit 1
fi
echo "   7b every Any import is typing-acceptable-tagged"

# 7c — the dead cycle-1 field `annual_rev_per_node_musd` must not exist as a
#      Pydantic field / assignment. A docstring documenting the D25 rename is
#      fine; a real field definition is the defect.
if grep -rnE --include='*.py' '^\s*annual_rev_per_node_musd\s*[:=]' src/; then
  echo "FAIL: annual_rev_per_node_musd exists as a field/assignment (D25 — renamed)"; exit 1
fi
echo "   7c no live annual_rev_per_node_musd field (D25 rename holds)"

# 7d — the dropped legacy scalar `r_revenue_cost` must not exist as a config
#      field / assignment. V11's code names the literal string to *detect* it,
#      and config.py's docstring documents its removal — neither is a defect.
if grep -rnE --include='*.py' '^\s*r_revenue_cost\s*[:=]' src/; then
  echo "FAIL: r_revenue_cost exists as a config field/assignment (D18 — R is a band)"; exit 1
fi
echo "   7d no live r_revenue_cost scalar (R-band-only, D18)"

# 7e — cohort *logic* (the `Cohort` class) must not leak out of fleet.py.
#      fleet.py owns the class; engine.py is the orchestration layer that
#      builds cohort lists (D12 — circular import bars moving it). The
#      lowercase domain word "cohort" in field descriptions / formula text
#      is glossary vocabulary, not a defect.
if grep -rnE --include='*.py' '\bCohort\b' src/ \
     | grep -v 'src/data_center/fleet.py' \
     | grep -v 'src/data_center/engine.py'; then
  echo "FAIL: Cohort class referenced outside fleet.py / engine.py"; exit 1
fi
echo "   7e cohort logic confined to fleet.py + engine.py"

echo
echo "Cycle 2 PASS"
