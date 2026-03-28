#!/usr/bin/env bash
set -euo pipefail

# Checks:
# 1) Template adoption: every infra compose file references common-optimizations.yml
# 2) Required security controls on resolved root compose services:
#    - no-new-privileges:true
#    - cap_drop includes ALL
#
# Exceptions are loaded from infra/common-optimizations.exceptions.json.

if ! command -v jq >/dev/null 2>&1; then
  echo "ERROR: jq is required for baseline checks." >&2
  exit 2
fi

exceptions_file="infra/common-optimizations.exceptions.json"
if [[ ! -f "$exceptions_file" ]]; then
  echo "ERROR: exceptions registry not found: $exceptions_file" >&2
  exit 2
fi

required_ref="$(
  jq -r '.template_adoption.required_reference // "common-optimizations.yml"' "$exceptions_file"
)"
template_file_exceptions="$(
  jq -c '.template_adoption.file_exceptions // []' "$exceptions_file"
)"
nnp_exceptions="$(
  jq -c '.security_baseline.no_new_privileges_exceptions // [] | map(.service // .)' "$exceptions_file"
)"
capdrop_exceptions="$(
  jq -c '.security_baseline.cap_drop_all_exceptions // [] | map(.service // .)' "$exceptions_file"
)"

mapfile -t compose_files < <(
  find infra -type f \( -name 'docker-compose.yml' -o -name 'docker-compose.*.yml' -o -name 'docker-compose-*.yml' \) | sort
)

template_violations=()
for f in "${compose_files[@]}"; do
  is_exception="$(
    jq -r --arg f "$f" 'if index($f) then "yes" else "no" end' <<<"$template_file_exceptions"
  )"
  if [[ "$is_exception" == "yes" ]]; then
    continue
  fi
  if ! rg -q "$required_ref" "$f"; then
    template_violations+=("$f")
  fi
done

tmp_json="$(mktemp)"
trap 'rm -f "$tmp_json"' EXIT
docker compose config --format json >"$tmp_json"

nnp_violations="$(
  jq -r --argjson ex "$nnp_exceptions" '
    .services
    | to_entries[]
    | .key as $name
    | select(
        ((.value.security_opt // []) | map(tostring) | any(contains("no-new-privileges:true")) | not)
        and
        (($ex | index($name)) | not)
      )
    | $name
  ' "$tmp_json"
)"

capdrop_violations="$(
  jq -r --argjson ex "$capdrop_exceptions" '
    .services
    | to_entries[]
    | .key as $name
    | select(
        ((.value.cap_drop // []) | map(tostring) | any(. == "ALL") | not)
        and
        (($ex | index($name)) | not)
      )
    | $name
  ' "$tmp_json"
)"

total_files="${#compose_files[@]}"
template_fail_count="${#template_violations[@]}"
nnp_fail_count="$(wc -w <<<"$nnp_violations" | tr -d ' ')"
capdrop_fail_count="$(wc -w <<<"$capdrop_violations" | tr -d ' ')"

echo "Template & security baseline check"
echo "compose_files_total=$total_files"
echo "template_adoption_missing=$template_fail_count"
echo "missing_no_new_privileges=$nnp_fail_count"
echo "missing_cap_drop_all=$capdrop_fail_count"

if [[ "$template_fail_count" -gt 0 || "$nnp_fail_count" -gt 0 || "$capdrop_fail_count" -gt 0 ]]; then
  echo
  echo "FAILED: baseline violations detected"
  if [[ "$template_fail_count" -gt 0 ]]; then
    echo "- template adoption missing:"
    printf '  - %s\n' "${template_violations[@]}"
  fi
  if [[ "$nnp_fail_count" -gt 0 ]]; then
    echo "- no-new-privileges missing:"
    while IFS= read -r s; do
      [[ -n "$s" ]] && echo "  - $s"
    done <<<"$nnp_violations"
  fi
  if [[ "$capdrop_fail_count" -gt 0 ]]; then
    echo "- cap_drop ALL missing:"
    while IFS= read -r s; do
      [[ -n "$s" ]] && echo "  - $s"
    done <<<"$capdrop_violations"
  fi
  exit 1
fi

echo
echo "PASS: template adoption + required security controls enforced"
