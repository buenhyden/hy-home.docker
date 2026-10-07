#!/usr/bin/env bash
set -euo pipefail

# Runs the Conftest job exactly as declared in
# infra/11-quality/conftest/docker-compose.yml (POL-0095). The default preserves
# the combined policy-unit and corpus check; CI selects their closed modes.

mode="all"
if [[ $# -eq 2 && $1 == "--mode" ]]; then
  mode=$2
elif [[ $# -ne 0 ]]; then
  echo "usage: $0 [--mode verify|corpus|all]" >&2
  exit 2
fi
case "$mode" in
  verify|corpus|all) ;;
  *)
    echo "usage: $0 [--mode verify|corpus|all]" >&2
    exit 2
    ;;
esac

root="$(git rev-parse --show-toplevel)"
cd "$root"
compose=(docker compose -p hyhome-conftest-gate -f infra/11-quality/conftest/docker-compose.yml --profile policy-check)

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker is required for the Conftest policy check." >&2
  exit 2
fi

status=0
"${compose[@]}" run --rm conftest "$mode" || status=$?
"${compose[@]}" down --remove-orphans >/dev/null 2>&1 || true
exit "$status"
