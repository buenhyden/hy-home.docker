#!/usr/bin/env bash
# post-tool-validate.sh — provider-neutral post-edit repository validation.
set -euo pipefail

PROJECT_DIR="${CODEX_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}}"
cd "$PROJECT_DIR"

INPUT="$(cat || true)"
mapfile -t CHANGED_PATHS < <(
  printf '%s' "$INPUT" | python3 -c '
import json
import re
import sys

raw = sys.stdin.read()
try:
    data = json.loads(raw) if raw.strip() else {}
except Exception:
    data = {}

tool_input = data.get("tool_input", {}) if isinstance(data, dict) else {}
paths = []

def add(value):
    if isinstance(value, str) and value:
        paths.append(value)

if isinstance(tool_input, dict):
    for key in ("file_path", "path"):
        add(tool_input.get(key))

    for key in ("files", "paths"):
        value = tool_input.get(key)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    add(item)
                elif isinstance(item, dict):
                    add(item.get("file_path") or item.get("path"))

    edits = tool_input.get("edits")
    if isinstance(edits, list):
        for edit in edits:
            if isinstance(edit, dict):
                add(edit.get("file_path") or edit.get("path"))

for match in re.finditer(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", raw, re.M):
    add(match.group(1).strip())
for match in re.finditer(r"^\*\*\* Move to: (.+)$", raw, re.M):
    add(match.group(1).strip())

seen = set()
for path in paths:
    if path not in seen:
        seen.add(path)
        print(path)
'
)

if [[ "${#CHANGED_PATHS[@]}" -eq 0 ]]; then
  exit 0
fi

run_compose=0
run_governance=0
run_json=0
run_bash=0

for path in "${CHANGED_PATHS[@]}"; do
  rel="${path#"$PROJECT_DIR"/}"
  rel="${rel#./}"

  case "$rel" in
    *docker-compose*.yml|*docker-compose*.yaml|infra/*|.env.example)
      run_compose=1
      ;;
  esac

  case "$rel" in
    AGENTS.md|CLAUDE.md|GEMINI.md|README.md|llms.txt|docs/*|.github/*|.claude/*|.codex/*|scripts/*|infra/tech-stack.versions.json)
      run_governance=1
      ;;
  esac

  case "$rel" in
    .claude/settings.json|.codex/hooks.json|infra/tech-stack.versions.json)
      run_json=1
      ;;
  esac

  if [[ "$rel" =~ ^(\.claude/hooks|scripts)/.*\.sh$ ]]; then
    run_bash=1
  fi
done

if [[ "$run_json" -eq 1 ]]; then
  python3 -m json.tool .claude/settings.json >/dev/null
  python3 -m json.tool .codex/hooks.json >/dev/null
  python3 -m json.tool infra/tech-stack.versions.json >/dev/null
fi

if [[ "$run_bash" -eq 1 ]]; then
  shopt -s nullglob globstar
  bash_files=(.claude/hooks/*.sh scripts/*.sh scripts/**/*.sh)
  shopt -u nullglob globstar
  if [[ "${#bash_files[@]}" -gt 0 ]]; then
    bash -n "${bash_files[@]}"
  fi
fi

if [[ "$run_compose" -eq 1 ]]; then
  bash scripts/validate-docker-compose.sh
fi

if [[ "$run_governance" -eq 1 ]]; then
  bash scripts/check-repo-contracts.sh
  bash scripts/check-doc-traceability.sh
fi
