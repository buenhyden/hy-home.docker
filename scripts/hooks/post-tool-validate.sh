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
            while preserving diff, syntax, lint, and repo checks.
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

HOOK_PAYLOAD_MODULE="$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")/../lib/hooks/tool_payload.py"
CHANGED_PATH_TEXT="$(
  python3 -c '
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(sys.argv[2]).resolve().parents[3]))
from scripts.lib.hooks.tool_payload import decode_payload, edit_targets
try:
    edits = edit_targets(pathlib.Path(sys.argv[1]), decode_payload(sys.stdin.read()))
except Exception as error:
    raise SystemExit(f"ERROR: edit payload validation failed: {error}") from error
print("\n".join(dict.fromkeys(path for path, _ in edits)))
' "$PROJECT_DIR" "$HOOK_PAYLOAD_MODULE"
)"
if [[ -z "$CHANGED_PATH_TEXT" ]]; then
  exit 0
fi
mapfile -t CHANGED_PATHS <<<"$CHANGED_PATH_TEXT"

# `.pre-commit-config.yaml` names every registered text mutator and the frozen
# archive payloads they must not rewrite. This hook performs the same
# trailing-whitespace and final-newline normalization, so it reads that one
# owner instead of restating the boundary. An owner that exists but declares no
# anchor is a misconfiguration and fails closed; an absent owner registers no
# mutator at all and therefore excludes nothing.
FROZEN_PAYLOAD_PATTERN="$(
  python3 - .pre-commit-config.yaml <<'PY'
from __future__ import annotations

import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1])
if not path.is_file():
    raise SystemExit(0)

try:
    text = path.read_text(encoding="utf-8")
except OSError as error:
    raise SystemExit(f"ERROR: formatting owner is unreadable: {error}") from error

match = re.search(
    r"^\s*exclude:\s*&frozen_archive_payloads\s+'(?P<pattern>[^']+)'\s*$",
    text,
    re.M,
)
if match is None:
    raise SystemExit(
        "ERROR: .pre-commit-config.yaml declares no frozen_archive_payloads anchor"
    )

pattern = match.group("pattern")
try:
    re.compile(pattern)
except re.error as error:
    raise SystemExit(
        f"ERROR: frozen_archive_payloads is not a regular expression: {error}"
    ) from error

print(pattern)
PY
)"

EXISTING_CHANGED_FILES=()
SHELL_STYLE_FILES=()
YAML_STYLE_FILES=()
JSON_SYNTAX_FILES=()

format_text_file_basics() {
  local file="$1"
  local frozen_pattern="$2"
  python3 - "$file" "$frozen_pattern" <<'PY'
from __future__ import annotations

import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1])
if not path.is_file():
    raise SystemExit(0)

frozen_pattern = sys.argv[2]
if frozen_pattern and re.search(frozen_pattern, path.as_posix()):
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

for rel in "${CHANGED_PATHS[@]}"; do
  if [[ -f "$rel" && "$rel" != graphify-out/* ]]; then
    EXISTING_CHANGED_FILES+=("$rel")
    if [[ "$check_only" -eq 0 ]]; then
      case "$rel" in
      *.md | *.sh | *.yml | *.yaml | *.json)
        format_text_file_basics "$rel" "$FROZEN_PAYLOAD_PATTERN"
        ;;
      esac
    fi
  fi

  if [[ "$rel" =~ \.sh$ && -f "$rel" ]]; then
    SHELL_STYLE_FILES+=("$rel")
  fi
  if [[ "$rel" =~ \.ya?ml$ && -f "$rel" ]]; then
    YAML_STYLE_FILES+=("$rel")
  fi
  if [[ "$rel" =~ \.json$ && -f "$rel" ]]; then
    JSON_SYNTAX_FILES+=("$rel")
  fi
done

# `.pre-commit-config.yaml` registers no shfmt hook, so shell files have no
# registered formatting owner and this hook runs none. See
# `.agents/governance/quality-standards.md` section 10.
if [[ "${#SHELL_STYLE_FILES[@]}" -gt 0 ]] && command -v shellcheck >/dev/null 2>&1; then
  # Severity is owned solely by the `shellcheck` hook arguments in
  # `.pre-commit-config.yaml`; `.shellcheckrc` cannot set it. Matching that
  # owner keeps this hook from rejecting what the registered gate accepts.
  shellcheck --severity=warning "${SHELL_STYLE_FILES[@]}"
fi
if [[ "${#YAML_STYLE_FILES[@]}" -gt 0 ]] && command -v yamllint >/dev/null 2>&1; then
  yamllint -c .yamllint "${YAML_STYLE_FILES[@]}"
fi
if [[ "${#EXISTING_CHANGED_FILES[@]}" -gt 0 ]]; then
  git diff --check -- "${EXISTING_CHANGED_FILES[@]}"
fi
if [[ "${#JSON_SYNTAX_FILES[@]}" -gt 0 ]]; then
  for file in "${JSON_SYNTAX_FILES[@]}"; do
    python3 -m json.tool "$file" >/dev/null
  done
fi
if [[ "${#SHELL_STYLE_FILES[@]}" -gt 0 ]]; then
  for file in "${SHELL_STYLE_FILES[@]}"; do
    bash -n "$file"
  done
fi
