#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

usage() {
  cat <<'EOF'
Usage: bash scripts/validation/run-local-qa-gates.sh [--help|--changed|--full|--explain]

Run a public validation profile selected from .github/workflow-contract.yml.

Modes:
  --changed  Default. Execute suites impacted by local changes.
  --full     Execute all six public suites.
  --explain  Explain changed suite-to-validator selection without execution.

Remote-only gates such as SARIF upload, protected-branch enforcement, and
GitHub-hosted required-check status are not executed. Approved Agent all-files
QA uses only scripts/validation/run-agent-precommit-all-files.sh from an
initially clean linked worktree with tracked Task evidence and explicit
--allow-prefix values; this local runner never invokes that controlled route.
EOF
}

if [[ "$#" -gt 1 ]]; then
  usage >&2
  exit 2
fi

case "${1:---changed}" in
--changed)
  exec python3 scripts/validation/run-ci-gate.py --profile changed
  ;;
--full)
  exec python3 scripts/validation/run-ci-gate.py --profile full
  ;;
--explain)
  exec python3 scripts/validation/run-ci-gate.py --profile changed --explain
  ;;
--help | -h)
  usage
  ;;
*)
  usage >&2
  exit 2
  ;;
esac
