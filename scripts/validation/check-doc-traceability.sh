#!/usr/bin/env bash
set -euo pipefail

# Checks documentation traceability sync across:
# - docs/04.execution/plans
# - docs/05.operations
#
# Scope:
# 1) Layer README reciprocal links (execution <-> operations)
# 2) Priority plan links to the operations policy catalog and operations index
# 3) Catalog OPER/RUN targets exist in the split operations taxonomy

failures=0
pair_total=0

fail() {
  echo "FAIL: $1"
  failures=$((failures + 1))
}

check_file_exists() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    fail "missing file: $file"
    return 1
  fi
  return 0
}

check_contains_literal() {
  local file="$1"
  local literal="$2"
  local label="$3"
  if ! grep -Fq "$literal" "$file"; then
    fail "$label (file: $file, expected literal: $literal)"
  fi
}

execution_readme="docs/04.execution/README.md"
plans_readme="docs/04.execution/plans/README.md"
tasks_readme="docs/04.execution/tasks/README.md"
ops_readme="docs/05.operations/README.md"
priority_plan="docs/04.execution/plans/2026-03-27-infra-service-optimization-priority-plan.md"
catalog="docs/05.operations/policies/infra-service-optimization-catalog.md"

check_file_exists "$execution_readme" || true
check_file_exists "$plans_readme" || true
check_file_exists "$tasks_readme" || true
check_file_exists "$ops_readme" || true
check_file_exists "$priority_plan" || true
check_file_exists "$catalog" || true

if [[ "$failures" -eq 0 ]]; then
  check_contains_literal "$execution_readme" "../05.operations/README.md" "04.execution README missing 05.operations link"
  check_contains_literal "$plans_readme" "../../05.operations/README.md" "plans README missing 05.operations link"
  check_contains_literal "$tasks_readme" "../../05.operations/README.md" "tasks README missing 05.operations link"
  check_contains_literal "$ops_readme" "../04.execution/plans/README.md" "05.operations README missing plans link"
  check_contains_literal "$ops_readme" "../04.execution/tasks/README.md" "05.operations README missing tasks link"

  check_contains_literal "$priority_plan" "../../05.operations/policies/12-infra-service-optimization-catalog.md" "priority plan missing operations policy catalog link"
  check_contains_literal "$priority_plan" "../../05.operations/README.md" "priority plan missing operations index link"

  catalog_dir="$(dirname "$catalog")"
  while IFS='|' read -r oper_rel run_rel; do
    [[ -z "$oper_rel" || -z "$run_rel" ]] && continue
    pair_total=$((pair_total + 1))

    oper_path="$(realpath -m "$catalog_dir/$oper_rel")"
    run_path="$(realpath -m "$catalog_dir/$run_rel")"

    if [[ ! -f "$oper_path" ]]; then
      fail "catalog OPER target missing: $oper_rel -> $oper_path"
      continue
    fi
    if [[ ! -f "$run_path" ]]; then
      fail "catalog RUN target missing: $run_rel -> $run_path"
      continue
    fi
  done < <(awk 'match($0, /\[OPER\]\(([^)]+)\), \[RUN\]\(([^)]+)\)/, m){print m[1]"|"m[2]}' "$catalog")
fi

echo "Doc traceability check"
echo "catalog_pairs_total=$pair_total"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: 04.execution/plans <-> 05.operations traceability is synchronized"
