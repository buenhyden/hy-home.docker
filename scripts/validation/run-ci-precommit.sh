#!/usr/bin/env bash
set -euo pipefail

# Anti-duplication (quality-standards.md section 4): the public gate is the
# dedicated route for the two local `public-validation-*` hooks, and running
# them from here would re-enter `run-ci-gate.py`, which reaches this script
# again. Skipping them is what keeps the two orchestrators from recursing, so
# this script owns the value rather than trusting a caller to supply it.
readonly GATE_OWNED_HOOKS='public-validation-changed,public-validation-full'

die() {
  echo "ERROR: $1" >&2
  exit 2
}

[[ "$#" -eq 0 ]] || die "arguments are not accepted"
[[ "${GITHUB_ACTIONS:-}" == "true" ]] || die "GITHUB_ACTIONS=true is required"
[[ "${CI:-}" == "true" ]] || die "CI=true is required"
[[ -z "${TASK_FILE+x}" ]] || die "Agent wrapper variable TASK_FILE is not accepted"
[[ -z "${ALLOW_PREFIXES+x}" ]] || die "Agent wrapper variable ALLOW_PREFIXES is not accepted"
[[ -z "${SKIP+x}" ]] || die "SKIP is owned by this script, not by its caller"

SKIP="$GATE_OWNED_HOOKS" exec pre-commit run --all-files --show-diff-on-failure
