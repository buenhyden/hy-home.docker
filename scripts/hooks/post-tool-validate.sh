#!/usr/bin/env bash
# post-tool-validate.sh — provider-neutral post-edit repository validation.
set -euo pipefail

check_only=0
while [[ "$#" -gt 0 ]]; do
  case "$1" in
  --check)
    check_only=1
    ;;
  -h | --help)
    cat <<'EOF'
Usage: post-tool-validate.sh [--check]

Consumes a hook JSON payload on stdin and validates changed files.

Options:
  --check   Run non-mutating validation only. This disables whitespace writes
            and shfmt -w while preserving diff, syntax, and repo checks.
EOF
    exit 0
    ;;
  *)
    printf 'ERROR: unknown option: %s\n' "$1" >&2
    exit 2
    ;;
  esac
  shift
done

case "${POST_TOOL_VALIDATE_CHECK_ONLY:-0}" in
1 | true | TRUE | yes | YES)
  check_only=1
  ;;
esac

PROJECT_DIR="${CODEX_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}}"
cd "$PROJECT_DIR"

INPUT="$(cat || true)"
mapfile -d '' -t CHANGED_PATHS < <(
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
        sys.stdout.buffer.write(path.encode("utf-8") + b"\0")
'
)

if [[ "${#CHANGED_PATHS[@]}" -eq 0 ]]; then
  exit 0
fi

python3 - "$PROJECT_DIR" "${CHANGED_PATHS[@]}" <<'PY'
from __future__ import annotations

import os
import pathlib
import stat
import sys


def fail(value: str, reason: str) -> None:
    raise SystemExit(f"ERROR: unsafe changed path {value!r}: {reason}")


root_input = pathlib.Path(sys.argv[1])
try:
    root = root_input.resolve(strict=True)
    root_metadata = root_input.lstat()
except OSError as error:
    raise SystemExit(f"ERROR: unsafe project root: {error}") from error
if root_input.absolute() != root or not stat.S_ISDIR(root_metadata.st_mode):
    raise SystemExit("ERROR: project root must be a canonical physical directory")

for value in sys.argv[2:]:
    if not value or any(ord(character) < 32 or ord(character) == 127 for character in value):
        fail(value, "empty or control-character path")
    if "\\" in value:
        fail(value, "backslash path is noncanonical")
    candidate = pathlib.PurePosixPath(value)
    if candidate.is_absolute():
        fail(value, "absolute paths are unsupported")
    if candidate.as_posix() != value or any(part in {"", ".", ".."} for part in candidate.parts):
        fail(value, "path is noncanonical or traverses a parent")
    target = root.joinpath(*candidate.parts)
    try:
        if os.path.commonpath((str(root), str(target))) != str(root):
            fail(value, "path escapes the repository")
    except ValueError:
        fail(value, "path escapes the repository")
    current = root
    for index, part in enumerate(candidate.parts):
        current = current / part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            break
        except OSError as error:
            fail(value, f"path cannot be inspected: {error}")
        if stat.S_ISLNK(metadata.st_mode):
            fail(value, "symlink components are unsupported")
        final = index == len(candidate.parts) - 1
        if not final and not stat.S_ISDIR(metadata.st_mode):
            fail(value, "parent component is not a directory")
        if final and not stat.S_ISREG(metadata.st_mode):
            fail(value, "changed target is not a regular file")
        if final and metadata.st_nlink != 1:
            fail(value, "changed target must have exactly one hard link")
PY

if [[ -f scripts/operations/use-qa-ci-tools.sh ]]; then
  # shellcheck source=../operations/use-qa-ci-tools.sh
  source scripts/operations/use-qa-ci-tools.sh >/dev/null 2>&1 || true
fi

EXISTING_CHANGED_FILES=()
SHELL_STYLE_FILES=()
YAML_STYLE_FILES=()

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
run_provider_registry=0
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
    if [[ "$check_only" -eq 0 ]]; then
      case "$rel" in
      *.md | *.sh | *.yml | *.yaml | *.json)
        format_text_file_basics "$rel"
        ;;
      esac
    fi
  fi

  case "$rel" in
  *docker-compose*.yml | *docker-compose*.yaml | infra/* | .env.example)
    run_compose=1
    ;;
  esac

  case "$rel" in
  AGENTS.md | CLAUDE.md | README.md | llms.txt | docs/* | .github/* | .claude/* | .codex/* | .agents/* | scripts/* | infra/tech-stack.versions.json)
    run_governance=1
    ;;
  esac

  case "$rel" in
  .claude/settings.json | .codex/hooks.json | infra/tech-stack.versions.json)
    run_json=1
    ;;
  esac

  case "$rel" in
  docs/00.agent-governance/providers/registry.yaml)
    run_provider_registry=1
    ;;
  esac

  if [[ "$rel" =~ ^(\.claude/hooks|scripts)/.*\.sh$ ]]; then
    run_bash=1
    if [[ -f "$rel" ]]; then
      SHELL_STYLE_FILES+=("$rel")
    fi
  fi
  if [[ "$rel" =~ \.ya?ml$ && -f "$rel" ]]; then
    YAML_STYLE_FILES+=("$rel")
  fi
done

if [[ "$check_only" -eq 0 && "${#SHELL_STYLE_FILES[@]}" -gt 0 ]] && command -v shfmt >/dev/null 2>&1; then
  shfmt -w "${SHELL_STYLE_FILES[@]}"
fi

if [[ "$run_style" -eq 1 ]]; then
  if [[ "${#SHELL_STYLE_FILES[@]}" -gt 0 ]] && command -v shfmt >/dev/null 2>&1; then
    shfmt -d "${SHELL_STYLE_FILES[@]}"
  fi
  if [[ "${#SHELL_STYLE_FILES[@]}" -gt 0 ]] && command -v shellcheck >/dev/null 2>&1; then
    shellcheck "${SHELL_STYLE_FILES[@]}"
  fi
  if [[ "${#YAML_STYLE_FILES[@]}" -gt 0 ]] && command -v yamllint >/dev/null 2>&1; then
    yamllint -c .yamllint "${YAML_STYLE_FILES[@]}"
  fi
  git diff --check -- "${EXISTING_CHANGED_FILES[@]}"
fi

if [[ "$run_json" -eq 1 ]]; then
  python3 -m json.tool .claude/settings.json >/dev/null
  python3 -m json.tool .codex/hooks.json >/dev/null
  python3 -m json.tool infra/tech-stack.versions.json >/dev/null
fi

if [[ "$run_provider_registry" -eq 1 ]]; then
  python3 scripts/validation/check-agent-governance-contract.py --section providers
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
  python3 scripts/validation/check-document-links.py --mode traceability
fi
