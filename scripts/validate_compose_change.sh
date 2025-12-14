#!/usr/bin/env bash
set -euo pipefail

# Usage: validate_compose_change.sh [service-name] [--up]
# - Runs `docker compose config` to validate Infra/docker-compose.yml
# - If service-name provided and --up supplied, attempts to `docker compose up -d --no-deps <service>` for quick smoke test

ROOT_DIR=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(cd "$(dirname "$0")/.." && pwd -P)")
COMPOSE_FILE="$ROOT_DIR/Infra/docker-compose.yml"

if [ ! -f "$COMPOSE_FILE" ]; then
  echo "Infra docker-compose not found: $COMPOSE_FILE" >&2
  exit 1
fi

echo "Validating $COMPOSE_FILE..."
docker compose -f "$COMPOSE_FILE" config >/dev/null
echo "Compose file is syntactically valid."

SERVICE_NAME=""
DO_UP=false
for arg in "$@"; do
  case "$arg" in
    --up) DO_UP=true ;;
    *) SERVICE_NAME="$arg" ;;
  esac
done

if [ -n "$SERVICE_NAME" ] && [ "$DO_UP" = true ]; then
  echo "Attempting to bring up service: $SERVICE_NAME (no deps)"
  (cd "$ROOT_DIR/Infra" && docker compose up -d --no-deps --force-recreate "$SERVICE_NAME")
  echo "Sleeping 5s to collect logs..."
  sleep 5
  docker compose -f "$COMPOSE_FILE" logs --no-color --tail 200 "$SERVICE_NAME" || true
  echo "You may want to run: curl -k https://${SERVICE_NAME}.127.0.0.1.nip.io"
fi

echo "Done."
