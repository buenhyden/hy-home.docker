#!/usr/bin/env bash
# post-tool-validate.sh — provider-neutral post-edit repository validation.
set -euo pipefail

check_only=1
while [[ "$#" -gt 0 ]]; do
  case "$1" in
  --check)
    check_only=1
    ;;
  --write)
    check_only=0
    ;;
  -h | --help)
    cat <<'EOF'
Usage: post-tool-validate.sh [--check | --write]

Consumes a hook JSON payload on stdin and validates changed files. The default
is non-mutating validation: diff, syntax, lint, and repo checks only, and it
reports a changed text file that --write would normalize.

Options:
  --check   Non-mutating validation (the default).
  --write   Normalize trailing whitespace and final newlines in the changed
            files. An explicit fix command; the runtime hook passes --check.
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

EXISTING_CHANGED_FILES=()
SHELL_STYLE_FILES=()
YAML_STYLE_FILES=()
JSON_SYNTAX_FILES=()

format_text_file_basics() {
  local file="$1"
  local mode="$2"
  python3 - "$file" "$mode" <<'PY'
from __future__ import annotations

import io
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

# Mirror pre-commit-hooks trailing-whitespace and end-of-file-fixer: lines
# split on LF only, a CRLF ending is kept for mixed-line-ending, and every
# trailing ASCII whitespace byte goes. A form feed or U+2028 inside a line
# stays where it is. This hook never removes extra final blank lines.
def strip_line(line: bytes) -> bytes:
    if line.endswith(b"\r\n"):
        return line[:-2].rstrip() + b"\r\n"
    if line.endswith(b"\n"):
        return line[:-1].rstrip() + b"\n"
    return line.rstrip()


new_data = b"".join(strip_line(line) for line in io.BytesIO(data).readlines())
if new_data and not new_data.endswith((b"\n", b"\r")):
    new_data += b"\n"
if new_data != data:
    if sys.argv[2] == "check":
        raise SystemExit(
            f"{path}: trailing whitespace or a missing final newline; "
            "fix it, or run post-tool-validate.sh --write"
        )
    path.write_bytes(new_data)
PY
}

for rel in "${CHANGED_PATHS[@]}"; do
  if [[ -f "$rel" && "$rel" != graphify-out/* ]]; then
    EXISTING_CHANGED_FILES+=("$rel")
    case "$rel" in
    *.md | *.sh | *.yml | *.yaml | *.json)
      if [[ "$check_only" -eq 0 ]]; then
        format_text_file_basics "$rel" write
      else
        format_text_file_basics "$rel" check
      fi
      ;;
    esac
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
if [[ "${#SHELL_STYLE_FILES[@]}" -gt 0 ]]; then
  if command -v shellcheck >/dev/null 2>&1; then
    # Severity is owned solely by the `shellcheck` hook arguments in
    # `.pre-commit-config.yaml`; `.shellcheckrc` cannot set it. Matching that
    # owner keeps this hook from rejecting what the registered gate accepts.
    shellcheck --severity=warning "${SHELL_STYLE_FILES[@]}"
  else
    printf '%s\n' 'SKIPPED shellcheck (missing tool)' >&2
  fi
fi
if [[ "${#YAML_STYLE_FILES[@]}" -gt 0 ]]; then
  if command -v yamllint >/dev/null 2>&1; then
    yamllint -c .yamllint "${YAML_STYLE_FILES[@]}"
  else
    printf '%s\n' 'SKIPPED yamllint (missing tool)' >&2
  fi
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
