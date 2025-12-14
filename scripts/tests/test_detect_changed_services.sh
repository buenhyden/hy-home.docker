#!/usr/bin/env bash
set -euo pipefail

TMPROOT=$(mktemp -d)
pushd "$TMPROOT" >/dev/null
git init -q
mkdir -p Infra/foo Infra/bar
echo "initial" > Infra/foo/a.txt
git add . && git commit -m "initial" -q

git checkout -b feature
mkdir -p Infra/newsvc
echo "x" > Infra/newsvc/b.txt
git add . && git commit -m "feat: add newsvc" -q

# Simulate a change to top-level Infra files (should not be detected as a service)
echo "top-level change" > Infra/docker-compose.yml
git add Infra/docker-compose.yml && git commit -m "chore: update infra compose" -q

BASE=master
CHANGED_FILES=$(git diff --name-only $BASE...HEAD || true)
# Only match files under Infra/<service>/... so we don't include top-level infra files
SERVICES=$(echo "$CHANGED_FILES" | grep -E '^Infra/[^/]+/' | awk -F'/' '{print $2}' | sort -u | tr '\n' ' ')

if [[ "$SERVICES" != *newsvc* ]]; then
  echo "Failed to detect newsvc in changed services: $SERVICES" >&2
  exit 1
fi

if [[ "$SERVICES" == *docker-compose.yml* ]]; then
  echo "Detected top-level infra file as a service: $SERVICES" >&2
  exit 1
fi

echo "test_detect_changed_services.sh PASSED"
popd >/dev/null
