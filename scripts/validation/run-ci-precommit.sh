#!/usr/bin/env bash
set -euo pipefail

die() {
  echo "ERROR: $1" >&2
  exit 2
}

[[ "$#" -eq 0 ]] || die "arguments are not accepted"
[[ "${GITHUB_ACTIONS:-}" == "true" ]] || die "GITHUB_ACTIONS=true is required"
[[ "${CI:-}" == "true" ]] || die "CI=true is required"
[[ -z "${TASK_FILE+x}" ]] || die "Agent wrapper variable TASK_FILE is not accepted"
[[ -z "${ALLOW_PREFIXES+x}" ]] || die "Agent wrapper variable ALLOW_PREFIXES is not accepted"
[[ "${SKIP:-}" == "eslint-nextjs" ]] || die "SKIP=eslint-nextjs is required"

exec pre-commit run --all-files --show-diff-on-failure
