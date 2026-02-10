#!/usr/bin/env bash
set -euo pipefail

force=0
if [ "${1:-}" = "--force" ]; then
  force=1
  shift
fi

feature="${1:-}"
slug="${2:-}"
owner="${3:-}"
stack="${4:-node}"

if [ -z "$feature" ] || [ -z "$slug" ]; then
  echo "Usage: $0 [--force] <feature-name> <slug> [owner] [stack(node|python)]" >&2
  exit 2
fi

if [ -z "$owner" ]; then
  owner="${USER:-}"
fi
if [ -z "$owner" ]; then
  owner="unknown"
fi

if [ "$stack" != "node" ] && [ "$stack" != "python" ]; then
  echo "Invalid stack: $stack (expected: node|python)" >&2
  exit 2
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"

template_path="$repo_root/templates/plans/plan.template.md"
if [ ! -f "$template_path" ]; then
  echo "Plan template not found: $template_path" >&2
  exit 2
fi

out_dir="$repo_root/specs/$slug"
out_path="$out_dir/plan.md"
mkdir -p "$out_dir"

if [ -f "$out_path" ] && [ "$force" -ne 1 ]; then
  echo "Plan already exists: $out_path (use --force to overwrite)" >&2
  exit 1
fi

date="$(date +%F)"

yaml_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  printf "%s" "$s"
}

goal="Implement $feature"
goal_esc="$(yaml_escape "$goal")"
owner_esc="$(yaml_escape "$owner")"

content="$(cat "$template_path")"
content="${content//goal: \"[TBD: one sentence outcome]\"/goal: \"${goal_esc}\"}"
content="${content//date_created: \"YYYY-MM-DD\"/date_created: \"${date}\"}"
content="${content//last_updated: \"YYYY-MM-DD\"/last_updated: \"${date}\"}"
content="${content//owner: \"[TBD: name]\"/owner: \"${owner_esc}\"}"
content="$(echo "$content" | sed -E "s/^stack: \".*\" # node\\|python\$/stack: \"${stack}\" # node|python/")"
content="${content//# \[Feature\/Component\] Implementation Plan/# ${feature} Implementation Plan}"

printf "%s\n" "$content" >"$out_path"
echo "✅ Created Plan: $out_path"
