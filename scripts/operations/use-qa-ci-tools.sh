#!/usr/bin/env sh
# Source this file before running local QA/CI commands from restricted agent shells.

qa_ci_prepend_path() {
  case "${PATH:-}" in
  "$1" | "$1":*) ;;
  *) PATH="$1${PATH:+:$PATH}" ;;
  esac
}

qa_ci_node_bin="${QA_CI_NODE_BIN:-$HOME/.nvm/versions/node/v24.14.0/bin}"

if [ -d "$qa_ci_node_bin" ]; then
  qa_ci_prepend_path "$qa_ci_node_bin"
fi

if [ -d "$HOME/go/bin" ]; then
  qa_ci_prepend_path "$HOME/go/bin"
fi

if [ -d "$HOME/.local/bin" ]; then
  qa_ci_prepend_path "$HOME/.local/bin"
fi

export PATH

qa_ci_is_sourced=0
if [ -n "${ZSH_EVAL_CONTEXT:-}" ]; then
  case "$ZSH_EVAL_CONTEXT" in
  *:file) qa_ci_is_sourced=1 ;;
  esac
elif [ -n "${BASH_SOURCE:-}" ] && [ "${BASH_SOURCE:-}" != "$0" ]; then
  qa_ci_is_sourced=1
fi

if [ "$qa_ci_is_sourced" -eq 0 ]; then
  missing=0
  for tool in git bash python3 docker jq node npm pnpm pre-commit zizmor yamllint markdownlint-cli2 shellcheck shfmt actionlint hadolint gitleaks check-jsonschema cz; do
    if command -v "$tool" >/dev/null 2>&1; then
      printf '%s=%s\n' "$tool" "$(command -v "$tool")"
    else
      printf '%s=MISSING\n' "$tool"
      missing=1
    fi
  done
  exit "$missing"
fi
