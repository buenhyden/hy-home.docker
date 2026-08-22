#!/usr/bin/env bash
set -euo pipefail

# Checks documentation traceability sync across:
# - docs/03.specs co-located execution records
# - docs/05.operations
#
# Scope:
# 1) Layer README reciprocal links (specs <-> operations)
# 2) Spec 0137 co-located Plan/Task links
# 3) Priority plan links to the operations policy catalog and operations index
# 4) Catalog OPER/RUN targets exist in the split operations taxonomy

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

spec_readme="docs/03.specs/README.md"
research_plan="docs/03.specs/0137-agentic-research-pack-rebuild/plan.md"
research_task="docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0001-rebuild.md"
ops_readme="docs/05.operations/README.md"
priority_plan="docs/04.execution/plans/2026-03-27-infra-service-optimization-priority-plan.md"
catalog="docs/05.operations/policies/00-workspace/infra-service-optimization-catalog.md"

check_file_exists "$spec_readme" || true
check_file_exists "$research_plan" || true
check_file_exists "$research_task" || true
check_file_exists "$ops_readme" || true
check_file_exists "$priority_plan" || true
check_file_exists "$catalog" || true

if [[ "$failures" -eq 0 ]]; then
  check_contains_literal "$spec_readme" "../05.operations/README.md" "03.specs README missing 05.operations link"
  check_contains_literal "$ops_readme" "../03.specs/README.md" "05.operations README missing 03.specs link"
  check_contains_literal "$research_plan" "$research_task" "Spec 0137 plan missing numbered Task path"
  check_contains_literal "$research_task" "$research_plan" "Spec 0137 Task missing co-located Plan path"

  check_contains_literal "$priority_plan" "../../05.operations/policies/00-workspace/infra-service-optimization-catalog.md" "priority plan missing operations policy catalog link"
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

echo "PASS: 03.specs execution records <-> 05.operations traceability is synchronized"
