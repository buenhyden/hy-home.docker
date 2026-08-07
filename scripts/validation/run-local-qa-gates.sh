#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

usage() {
  cat <<'EOF'
Usage: bash scripts/validation/run-local-qa-gates.sh [--help|--list|--script-backed|--all-profiles|--harness]

Run the typed local QA profile selected from .github/workflow-contract.yml.

Modes:
  --script-backed  Default. Execute the local-script-backed profile once.
  --all-profiles   Execute the local-all-profiles profile once.
  --harness        Execute the local-harness profile once.
  --list           List the local-script-backed profile without execution.

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

case "${1:---script-backed}" in
--script-backed)
  exec python3 scripts/validation/run-ci-gate.py \
    --profile local-script-backed \
    --all
  ;;
--all-profiles)
  exec python3 scripts/validation/run-ci-gate.py \
    --profile local-all-profiles \
    --all
  ;;
--harness)
  exec python3 scripts/validation/run-ci-gate.py \
    --profile local-harness \
    --all
  ;;
--list)
  usage
  echo
  echo "Registered local-script-backed execution order:"
  exec python3 scripts/validation/run-ci-gate.py \
    --profile local-script-backed \
    --list
  ;;
--help | -h)
  usage
  ;;
*)
  usage >&2
  exit 2
  ;;
esac
