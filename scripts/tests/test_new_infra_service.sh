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
cp "$REPO_ROOT/scripts/new_infra_service.sh" "$TMPROOT/scripts/"
pushd "$TMPROOT" >/dev/null
git init >/dev/null
git add . >/dev/null
git commit -m "init" >/dev/null 2>&1 || true

chmod +x scripts/new_infra_service.sh
./scripts/new_infra_service.sh mytestsvc

if [ ! -d "Infra/mytestsvc" ]; then
  echo "Infra/mytestsvc not created" >&2
  exit 1
fi
if [ ! -f "secrets/mytestsvc_password.txt" ]; then
  echo "Secret file not created" >&2
  exit 1
fi
if ! grep -q "mytestsvc/docker-compose.yml" "Infra/docker-compose.yml"; then
  echo "Include line not added to Infra/docker-compose.yml" >&2
  exit 1
fi

echo "test_new_infra_service.sh PASSED"
popd >/dev/null
