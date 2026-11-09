#!/usr/bin/env bash
# Renovate post-upgrade step: bind the SEC01 update ledger to the Compose images
# and n8n inputs Renovate just changed.
#
# Runs scripts.lib.supply_chain.ledger_rebind in its --accept-image-updates mode.
# A routine image pin bump (same repository, full name:tag@sha256 reference, no
# new, removed or rebuilt service) is recorded as an unverified Renovate-proposed
# row; anything else exits 2, writes nothing and leaves the drift for CI to
# reject. It never contacts a registry or the network.
#
# Usage: sync-update-ledger.sh --write
#
# The source revision and timestamp come from HEAD so that a Renovate rebase of
# the same change writes the same bytes.
set -euo pipefail

if (( $# != 1 )) || [[ "$1" != "--write" ]]; then
  echo "Usage: $0 --write" >&2
  exit 2
fi

REPO_ROOT="$(cd "$(dirname "$(readlink -f -- "${BASH_SOURCE[0]}")")/../.." && pwd -P)"
cd "$REPO_ROOT"

# Same hash-locked install as sync-tech-stack-versions.sh: the Renovate image
# lacks the Python packages the Compose parser imports. Beside the checkout,
# because the container mounts /tmp noexec and the compiled rpds extension
# cannot load from there.
if ! python3 -c 'import yaml, markdown_it, jsonschema' 2>/dev/null; then
  deps_dir="$(mktemp -d -p "$(dirname -- "$REPO_ROOT")")"
  trap 'rm -rf -- "$deps_dir"' EXIT
  python3 -m pip install --quiet --no-deps --no-cache-dir --only-binary=:all: \
    --require-hashes --target "$deps_dir" -r scripts/requirements-renovate.lock
  export PYTHONPATH="$deps_dir${PYTHONPATH:+:$PYTHONPATH}"
fi

python3 -m scripts.lib.supply_chain.ledger_rebind --write --accept-image-updates \
  --source-revision "$(git rev-parse HEAD)" \
  --refreshed-at "$(git show -s --format=%cI HEAD)"
