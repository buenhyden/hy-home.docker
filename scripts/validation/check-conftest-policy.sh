#!/usr/bin/env bash
set -euo pipefail

# Runs the Conftest job exactly as declared in
# infra/09-tooling/conftest/docker-compose.yml (POL-0095): policy unit tests,
# then every Compose leaf and Dockerfile under infra/. Exit 0 only when no
# deny fires. The job has no network and mounts infra/ read-only.

root="$(git rev-parse --show-toplevel)"
cd "$root"
compose=(docker compose -p hyhome-conftest-gate -f infra/09-tooling/conftest/docker-compose.yml --profile policy-check)

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker is required for the Conftest policy check." >&2
  exit 2
fi

status=0
"${compose[@]}" run --rm conftest || status=$?
"${compose[@]}" down --remove-orphans >/dev/null 2>&1 || true
exit "$status"
