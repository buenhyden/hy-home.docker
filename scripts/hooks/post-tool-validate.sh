#!/usr/bin/env bash
# post-tool-validate.sh — provider-neutral post-edit repository validation.
set -euo pipefail

PROJECT_DIR="${CODEX_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}}"
cd "$PROJECT_DIR"

if [[ -f scripts/operations/use-qa-ci-tools.sh ]]; then
  # shellcheck source=../operations/use-qa-ci-tools.sh
  source scripts/operations/use-qa-ci-tools.sh >/dev/null 2>&1 || true
fi

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

EXISTING_CHANGED_FILES=()
SHELL_STYLE_FILES=()

format_text_file_basics() {
  local file="$1"
  python3 - "$file" <<'PY'
from __future__ import annotations

import pathlib
import sys

path = pathlib.Path(sys.argv[1])
if not path.is_file():
    raise SystemExit(0)

data = path.read_bytes()
try:
    text = data.decode("utf-8")
except UnicodeDecodeError:
    raise SystemExit(0)

if "\x00" in text:
    raise SystemExit(0)

lines = text.splitlines()
formatted = "\n".join(line.rstrip(" \t") for line in lines)
if formatted or text.endswith(("\n", "\r")):
    formatted += "\n"

new_data = formatted.encode("utf-8")
if new_data != data:
    path.write_bytes(new_data)
PY
}

run_compose=0
run_governance=0
run_json=0
run_bash=0
run_style=0

for path in "${CHANGED_PATHS[@]}"; do
  if [[ "$path" = /* && "$path" != "$PROJECT_DIR"/* ]]; then
    continue
  fi

  rel="${path#"$PROJECT_DIR"/}"
  rel="${rel#./}"

  if [[ -f "$rel" && "$rel" != graphify-out/* ]]; then
    EXISTING_CHANGED_FILES+=("$rel")
    run_style=1
    case "$rel" in
    *.md | *.sh | *.yml | *.yaml | *.json)
      format_text_file_basics "$rel"
      ;;
    esac
  fi

  case "$rel" in
  *docker-compose*.yml | *docker-compose*.yaml | infra/* | .env.example)
    run_compose=1
    ;;
  esac

  case "$rel" in
  AGENTS.md | CLAUDE.md | GEMINI.md | README.md | llms.txt | docs/* | .github/* | .claude/* | .codex/* | .agents/* | scripts/* | infra/tech-stack.versions.json)
    run_governance=1
    ;;
  esac

  case "$rel" in
  .claude/settings.json | .codex/hooks.json | infra/tech-stack.versions.json)
    run_json=1
    ;;
  esac

  if [[ "$rel" =~ ^(\.claude/hooks|scripts)/.*\.sh$ ]]; then
    run_bash=1
    if [[ -f "$rel" ]]; then
      SHELL_STYLE_FILES+=("$rel")
    fi
  fi
done

if [[ "${#SHELL_STYLE_FILES[@]}" -gt 0 ]] && command -v shfmt >/dev/null 2>&1; then
  shfmt -w "${SHELL_STYLE_FILES[@]}"
fi

if [[ "$run_style" -eq 1 ]]; then
  if [[ "${#SHELL_STYLE_FILES[@]}" -gt 0 ]] && command -v shfmt >/dev/null 2>&1; then
    shfmt -d "${SHELL_STYLE_FILES[@]}"
  fi
  git diff --check -- "${EXISTING_CHANGED_FILES[@]}"
fi

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
  bash scripts/validation/validate-docker-compose.sh
fi

if [[ "$run_governance" -eq 1 ]]; then
  bash scripts/validation/check-repo-contracts.sh
  bash scripts/validation/check-doc-traceability.sh
fi
