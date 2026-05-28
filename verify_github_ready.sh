#!/usr/bin/env bash
# Final GitHub-readiness verifier for the data-center-first public release.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_DIR="$ROOT/code"
SPACE_JSON="$ROOT/data_center/models/space/default.json"
GROUND_JSON="$ROOT/data_center/models/ground/default.json"
CONCLUSION="$ROOT/data_center/conclusion.md"

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

section() {
  printf '\n== %s ==\n' "$*"
}

require_file() {
  local path="$1"
  [[ -f "$path" ]] || fail "missing required file: ${path#$ROOT/}"
}

require_no_output() {
  local label="$1"
  shift
  local output
  if ! output="$("$@" 2>&1)"; then
    printf '%s\n' "$output"
    fail "$label command failed"
  fi
  if [[ -n "$output" ]]; then
    printf '%s\n' "$output"
    fail "$label"
  fi
}

require_no_rg_match() {
  local label="$1"
  local pattern="$2"
  shift 2
  if rg -n "$pattern" "$@"; then
    fail "$label"
  fi
}

run_query_examples() {
  local artifact="$1"
  local label="$2"
  local count=0
  local name
  local expression

  while IFS=$'\t' read -r name expression; do
    [[ -n "$name" ]] || fail "$label query example is missing a name"
    [[ -n "$expression" ]] || fail "$label query example $name is missing jq_expression"
    jq "$expression" "$artifact" >/dev/null || fail "$label query example failed: $name"
    count=$((count + 1))
  done < <(jq -r '.meta.query_examples[] | [.name, .jq_expression] | @tsv' "$artifact")

  [[ "$count" -gt 0 ]] || fail "$label has no query examples"
  printf '   %s query examples executed: %s\n' "$label" "$count"
}

cd "$ROOT"

section "Required files"
require_file "$SPACE_JSON"
require_file "$GROUND_JSON"
require_file "$CONCLUSION"
require_file "$ROOT/research/SOURCE_INDEX.md"
require_file "$ROOT/communications/README.md"
[[ ! -e "$ROOT/data_center/models/model.json" ]] || fail "old data_center/models/model.json alias exists"
printf '   public artifacts are present and old model alias is absent\n'

section "Python quality gates"
(cd "$CODE_DIR" && uv run ruff check .)
(cd "$CODE_DIR" && uv run ruff format --check .)
(cd "$CODE_DIR" && uv run mypy --strict .)
(cd "$CODE_DIR" && uv run pytest)
printf '   ruff, format, mypy strict, and pytest passed\n'

section "Promotion static-conclusion guard"
(cd "$CODE_DIR" && uv run pytest tests/data_center/test_cli_promote.py::test_promote_does_not_overwrite_static_conclusion)
printf '   promotion behavior leaves data_center/conclusion.md static\n'

section "Promoted JSON contracts"
jq -e '
  .metadata.schema_version == "v8"
  and .metadata.artifact_role == "promoted_default"
  and (.inputs.assumption_index | type == "object")
  and (.inputs.assumption_index | length > 0)
  and (.physical.years | type == "object")
  and (.business.years | type == "object")
  and (.meta.query_examples | length >= 12)
  and ([.meta.validation_results[]? | select(.severity == "fail")] | length == 0)
  and .meta.source_status_summary.placeholder == 0
  and .meta.source_status_summary.stale == 0
' "$SPACE_JSON" >/dev/null
jq -e '
  .metadata.artifact_role == "promoted_ground_default"
  and .anchor.year == 2036
  and (.inputs.assumption_index | type == "object")
  and (.inputs.assumption_index | length > 0)
  and (.comparison.conclusion_label == "insufficient_source_quality")
  and (.meta.query_examples | length >= 4)
  and ([.meta.validation_results[]? | select(.severity == "fail")] | length == 0)
' "$GROUND_JSON" >/dev/null
printf '   space and ground JSON contracts passed\n'

section "Query examples"
run_query_examples "$SPACE_JSON" "space"
run_query_examples "$GROUND_JSON" "ground"
jq '.inputs.assumption_index | to_entries[] | {path: .key, status: .value.source_status}' "$SPACE_JSON" >/dev/null
jq '.business.years["2036"]' "$SPACE_JSON" >/dev/null
jq '.anchor' "$GROUND_JSON" >/dev/null
jq '.comparison' "$GROUND_JSON" >/dev/null
printf '   minimum manual jq probes executed\n'

section "Public claim hygiene"
require_no_rg_match "stale 3.6 GW default claim found" '3\.6 GW' README.md data_center docs communications research
require_no_rg_match "stale multi-GW default claim found" '(default|current model|promoted).{0,80}(5 GW|five gigawatts|multi-GW)|(5 GW|five gigawatts|multi-GW).{0,80}(default|current model|promoted)' README.md data_center docs communications research
require_no_rg_match "generated canonical conclusion wording found" 'generated human-readable conclusion' README.md data_center docs communications
require_no_rg_match "unsupported premium certainty found" 'will command a premium' README.md data_center docs communications research
require_no_rg_match "launch-cost guess wording found" '(\$13M|13 million).{0,80}guess|guess.{0,80}(\$13M|13 million)' README.md data_center docs communications research
require_no_rg_match "private lifecycle reference found" '\.agent/' README.md data_center docs research code
require_no_output "private lifecycle reference found in space JSON" jq -r '.. | strings | select(test("\\.agent/"))' "$SPACE_JSON"
require_no_output "private lifecycle reference found in ground JSON" jq -r '.. | strings | select(test("\\.agent/"))' "$GROUND_JSON"
printf '   forbidden claims and private references passed\n'

section "Critical source IDs"
for claim_id in \
  RLDC-LAUNCH-COST-2036 \
  RLDC-PAYLOAD-SSO-UPGRADE \
  RLDC-CADENCE-90 \
  RLDC-NODE-POWER-400KW \
  RLDC-SERVICE-LIFE-5Y \
  RLDC-REVENUE-MULTIPLE-1_5X \
  RLDC-MARKET-100GW-2036 \
  RLDC-GROUND-COST-BASIS; do
  rg -q "$claim_id" research data_center README.md docs || fail "missing critical claim ID: $claim_id"
  printf '   %s present\n' "$claim_id"
done

section "Public tree hygiene"
require_no_output "project repo tracks .agent files" git ls-files .agent
require_no_output "project repo tracks code/archive" git ls-files code/archive
require_no_output "project repo tracks old model alias" git ls-files data_center/models/model.json
if git ls-files -o --exclude-standard | rg -n '(^|/)(\.DS_Store|__pycache__/|[^/]+\.pyc$)'; then
  fail "unignored cache or OS junk file found"
fi
if git diff --name-only --cached | rg -n '(^|/)(\.DS_Store|__pycache__/|[^/]+\.pyc$)'; then
  fail "cache or OS junk file is staged"
fi
printf '   no tracked private/archive/legacy files and no unignored junk\n'

section "GitHub readiness"
printf 'GitHub readiness verifier PASS\n'
