#!/usr/bin/env bash
set -euo pipefail

# Checks documentation traceability sync across:
# - docs/03.specs
# - docs/05.operations
#
# Scope:
# 1) Layer README reciprocal links (specs <-> operations)
# 2) The migrated workspace catalog is present at its subject-first target
# 3) Catalog OPER/RUN targets exist where the catalog declares them

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

specs_readme="docs/03.specs/README.md"
ops_readme="docs/05.operations/README.md"
catalog="docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md"

check_file_exists "$specs_readme" || true
check_file_exists "$ops_readme" || true
check_file_exists "$catalog" || true

if [[ "$failures" -eq 0 ]]; then
  check_contains_literal "$specs_readme" "../05.operations/README.md" "03.specs README missing 05.operations link"
  check_contains_literal "$ops_readme" "../03.specs/README.md" "05.operations README missing 03.specs link"

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

echo "PASS: 03.specs <-> 05.operations traceability is synchronized"
