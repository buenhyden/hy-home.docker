#!/usr/bin/env bash
# post-tool-validate.sh — PostToolUse hook: run path-aware repository validation.
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
cd "$PROJECT_DIR"

INPUT="$(cat || true)"
mapfile -t CHANGED_PATHS < <(
  printf '%s' "$INPUT" | python3 -c '
import json
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
    AGENTS.md|CLAUDE.md|GEMINI.md|docs/00.agent-governance/*|docs/90.references/docker/*|.github/*|.claude/*|.codex/*|scripts/README.md|scripts/check-repo-contracts.sh|infra/tech-stack.versions.json)
      run_governance=1
      ;;
  esac

  case "$rel" in
    .claude/settings.json|.codex/hooks.json|infra/tech-stack.versions.json)
      run_json=1
      ;;
  esac

  case "$rel" in
    .claude/hooks/*.sh|scripts/check-repo-contracts.sh)
      run_bash=1
      ;;
  esac
done

if [[ "$run_json" -eq 1 ]]; then
  python3 -c 'import json, pathlib; [json.loads(pathlib.Path(p).read_text()) for p in [".claude/settings.json", ".codex/hooks.json", "infra/tech-stack.versions.json"]]'
fi

if [[ "$run_bash" -eq 1 ]]; then
  bash -n .claude/hooks/*.sh scripts/check-repo-contracts.sh
fi

if [[ "$run_compose" -eq 1 ]]; then
  bash scripts/validate-docker-compose.sh
fi

if [[ "$run_governance" -eq 1 ]]; then
  bash scripts/check-repo-contracts.sh
  bash scripts/check-doc-traceability.sh
fi
