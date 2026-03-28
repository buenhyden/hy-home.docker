#!/usr/bin/env bash
set -euo pipefail

# Checks documentation traceability sync across:
# - docs/05.plans
# - docs/08.operations
# - docs/09.runbooks
#
# Scope:
# 1) Layer README reciprocal links (05 <-> 08 <-> 09)
# 2) Priority plan links to operations catalog/index and runbook index
# 3) Catalog OPER/RUN pairs existence + bidirectional reference presence

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
ops_readme="docs/08.operations/README.md"
runbooks_readme="docs/09.runbooks/README.md"
priority_plan="docs/05.plans/2026-03-27-infra-service-optimization-priority-plan.md"
catalog="docs/08.operations/12-infra-service-optimization-catalog.md"

check_file_exists "$plans_readme" || true
check_file_exists "$ops_readme" || true
check_file_exists "$runbooks_readme" || true
check_file_exists "$priority_plan" || true
check_file_exists "$catalog" || true

if [[ "$failures" -eq 0 ]]; then
  # Layer README reciprocal links
  check_contains_literal "$plans_readme" "../08.operations/README.md" "05.plans README missing 08.operations link"
  check_contains_literal "$plans_readme" "../09.runbooks/README.md" "05.plans README missing 09.runbooks link"

  check_contains_literal "$ops_readme" "../05.plans/README.md" "08.operations README missing 05.plans link"
  check_contains_literal "$ops_readme" "../09.runbooks/README.md" "08.operations README missing 09.runbooks link"

  check_contains_literal "$runbooks_readme" "../05.plans/README.md" "09.runbooks README missing 05.plans link"
  check_contains_literal "$runbooks_readme" "../08.operations/README.md" "09.runbooks README missing 08.operations link"

  # Priority plan traceability links
  check_contains_literal "$priority_plan" "../08.operations/12-infra-service-optimization-catalog.md" "priority plan missing catalog link"
  check_contains_literal "$priority_plan" "../08.operations/README.md" "priority plan missing operations index link"
  check_contains_literal "$priority_plan" "../09.runbooks/README.md" "priority plan missing runbook index link"

  # Catalog OPER/RUN pair checks
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

    run_base="$(basename "$run_path")"
    oper_base="$(basename "$oper_path")"

    if ! grep -Fq "$run_base" "$oper_path"; then
      fail "OPER missing RUN reference: $oper_path (expected token: $run_base)"
    fi
    if ! grep -Fq "$oper_base" "$run_path"; then
      fail "RUN missing OPER reference: $run_path (expected token: $oper_base)"
    fi
  done < <(awk 'match($0, /\[OPER\]\(([^)]+)\), \[RUN\]\(([^)]+)\)/, m){print m[1]"|"m[2]}' "$catalog")
fi

echo "Doc traceability check"
echo "catalog_pairs_total=$pair_total"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: 05.plans <-> 08.operations <-> 09.runbooks traceability is synchronized"
