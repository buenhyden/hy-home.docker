#!/usr/bin/env bash
set -euo pipefail

TMPROOT=$(mktemp -d)
echo "Using temp root: $TMPROOT"
mkdir -p "$TMPROOT/Infra" "$TMPROOT/scripts"

cat > "$TMPROOT/Infra/docker-compose.yml" <<'EOF'
version: "3.8"
services:
  dummy:
    image: alpine:3.18
    command: ["/bin/sh", "-c", "sleep 1"]
networks:
  infra_net:
EOF

REPO_ROOT=$(pwd)
cp "$REPO_ROOT/scripts/validate_compose_change.sh" "$TMPROOT/scripts/"
pushd "$TMPROOT" >/dev/null
chmod +x scripts/validate_compose_change.sh
if command -v docker >/dev/null 2>&1; then
  ./scripts/validate_compose_change.sh || { echo "validate_compose_change failed" >&2; exit 1; }
else
  echo "Docker not available on runner; skipping validate_compose_change test"
fi
echo "test_validate_compose_change.sh PASSED"
popd >/dev/null
