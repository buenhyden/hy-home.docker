#!/usr/bin/env bash
set -euo pipefail

# Checks documentation traceability sync across:
# - docs/05.plans
# - docs/07.operations
#
# Scope:
# 1) Layer README reciprocal links (05 <-> 07.operations)
# 2) Priority plan links to operations catalog/index
# 3) Catalog targets exist under the consolidated operations stage

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

plans_readme="docs/05.plans/README.md"
ops_readme="docs/07.operations/README.md"
priority_plan="docs/05.plans/2026-03-27-infra-service-optimization-priority-plan.md"
catalog="docs/07.operations/12-infra-service-optimization-catalog.md"

check_file_exists "$plans_readme" || true
check_file_exists "$ops_readme" || true
check_file_exists "$priority_plan" || true
check_file_exists "$catalog" || true

if [[ "$failures" -eq 0 ]]; then
  # Layer README reciprocal links
  check_contains_literal "$plans_readme" "../07.operations/README.md" "05.plans README missing 07.operations link"

  check_contains_literal "$ops_readme" "../05.plans/README.md" "07.operations README missing 05.plans link"

  # Priority plan traceability links
  check_contains_literal "$priority_plan" "../07.operations/12-infra-service-optimization-catalog.md" "priority plan missing catalog link"
  check_contains_literal "$priority_plan" "../07.operations/README.md" "priority plan missing operations index link"

  # Catalog target checks. OPER/RUN labels are kept for history, but both now
  # resolve into the consolidated docs/07.operations stage.
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

echo "PASS: 05.plans <-> 07.operations traceability is synchronized"
