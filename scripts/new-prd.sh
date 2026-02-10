#!/bin/bash
set -euo pipefail

feature="${1:-}"
owner="${2:-}"
parent_epic="${3:-}"

if [ -z "$feature" ]; then
  echo "Usage: $0 <feature-name> [owner] [parent-epic-link]"
  exit 2
fi

script_dir="$(cd "$(dirname "$0")" && pwd)"
root_dir="$(cd "$script_dir/.." && pwd)"

slug="$(echo "$feature" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9[:space:]-]+//g; s/[[:space:]]+/-/g; s/-{2,}/-/g; s/^-+|-+$//g')"
if [ -z "$slug" ]; then
  echo "Feature name '$feature' cannot be converted to a valid slug."
  exit 2
fi

prd_template="$root_dir/templates/prd-template.md"
spec_template="$root_dir/templates/spec-template.md"

prd_dir="$root_dir/docs/prd"
mkdir -p "$prd_dir"

prd_path="$prd_dir/${slug}-prd.md"
if [ -f "$prd_path" ]; then
  echo "PRD already exists: $prd_path"
  exit 1
fi

content="$(cat "$prd_template")"
content="${content//# \[Feature\/Epic Name\] PRD/# $feature PRD}"
if [ -n "$owner" ]; then
  content="$(echo "$content" | sed -E "s/^[*-] \\*\\*Owner\\*\\*: \\[Name\\]\$/- **Owner**: ${owner//\//\\/}/")"
fi
if [ -n "$parent_epic" ]; then
  content="$(echo "$content" | sed -E "s/^[*-] \\*\\*Parent Epic\\*\\*: \\[Link to Epic PRD\\] \\(Optional\\)\$/- **Parent Epic**: ${parent_epic//\//\\/} (Optional)/")"
fi

printf "%s\n" "$content" >"$prd_path"
echo "✅ Created PRD: $prd_path"

if [ "${WITH_SPEC:-}" = "1" ]; then
  spec_dir="$root_dir/specs/$slug"
  mkdir -p "$spec_dir"
  spec_path="$spec_dir/spec.md"
  if [ -f "$spec_path" ]; then
    echo "Spec already exists: $spec_path"
    exit 1
  fi

  spec_content="$(cat "$spec_template")"
  spec_content="${spec_content//# \[Component Name\] Technical Specification/# $feature Technical Specification}"
  spec_content="$(echo "$spec_content" | sed -E "s/^- \\*\\*PRD Reference\\*\\*: \\[Link to PRD\\]\$/- **PRD Reference**: docs\\/prd\\/${slug}-prd.md/")"
  printf "%s\n" "$spec_content" >"$spec_path"
  echo "✅ Created Spec: $spec_path"
fi
