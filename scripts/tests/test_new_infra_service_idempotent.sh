#!/usr/bin/env bash
set -euo pipefail

TMPROOT=$(mktemp -d)
echo "Using temp root: $TMPROOT"
mkdir -p "$TMPROOT/Infra" "$TMPROOT/scripts" "$TMPROOT/secrets"
cat > "$TMPROOT/Infra/docker-compose.yml" <<'EOF'
networks:
  infra_net:
    name: infra_net
include:
  - kafka/docker-compose.yml
EOF

REPO_ROOT=$(pwd)
cp ../../new_infra_service.sh "$TMPROOT/scripts/"
pushd "$TMPROOT" >/dev/null
git init >/dev/null
git add . >/dev/null
git commit -m "init" >/dev/null 2>&1 || true

chmod +x scripts/new_infra_service.sh
./scripts/new_infra_service.sh mytestsvc
./scripts/new_infra_service.sh mytestsvc

# Ensure no duplicate includes
INCLUDE_COUNT=$(grep -c "mytestsvc/docker-compose.yml" Infra/docker-compose.yml || true)
if [ "$INCLUDE_COUNT" -ne 1 ]; then
  echo "Include line duplicated ($INCLUDE_COUNT)" >&2
  exit 1
fi

echo "test_new_infra_service_idempotent.sh PASSED"
popd >/dev/null
