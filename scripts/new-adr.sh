#!/bin/bash
set -euo pipefail

title="${1:-}"
authors="${2:-}"

if [ -z "$title" ]; then
  echo "Usage: $0 <title> [authors]"
  exit 2
fi

script_dir="$(cd "$(dirname "$0")" && pwd)"
root_dir="$(cd "$script_dir/.." && pwd)"
adr_dir="$root_dir/docs/adr"
template="$root_dir/templates/adr-template.md"

mkdir -p "$adr_dir"

max=0
shopt -s nullglob
for f in "$adr_dir"/*.md; do
  base="$(basename "$f")"
  if [[ "$base" =~ ^([0-9]{4})-.*\.md$ ]]; then
    n="${BASH_REMATCH[1]}"
    if [ "$n" -gt "$max" ]; then max="$n"; fi
  fi
done

next=$((max + 1))
num="$(printf "%04d" "$next")"

slug="$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9[:space:]-]+//g; s/[[:space:]]+/-/g; s/-{2,}/-/g; s/^-+|-+$//g')"
if [ -z "$slug" ]; then
  echo "Title '$title' cannot be converted to a valid slug."
  exit 2
fi

out="$adr_dir/${num}-${slug}.md"
if [ -f "$out" ]; then
  echo "ADR already exists: $out"
  exit 1
fi

date="$(date +%F)"

content="$(cat "$template")"
content="${content//# \[Short Title of Decision\]/# $title}"
content="$(echo "$content" | sed -E "s/\\* \\*\\*Date\\*\\*: \\[YYYY-MM-DD\\]/* **Date**: $date/")"
if [ -n "$authors" ]; then
  content="$(echo "$content" | sed -E "s/\\* \\*\\*Authors\\*\\*: \\[Name\\]/* **Authors**: ${authors//\//\\/}/")"
fi

printf "%s\n" "$content" >"$out"
echo "✅ Created ADR: $out"
