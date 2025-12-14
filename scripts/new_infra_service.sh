#!/usr/bin/env bash
set -euo pipefail

# Usage: new_infra_service.sh <service-name>
SERVICE_NAME=${1:-}
if [ -z "$SERVICE_NAME" ]; then
  echo "Usage: $0 <service-name>" >&2
  exit 2
fi

ROOT_DIR=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(cd "$(dirname "$0")/.." && pwd -P)")
INFRA_DIR="$ROOT_DIR/Infra"
SECRETS_DIR="$ROOT_DIR/secrets"
SERVICE_DIR="$INFRA_DIR/$SERVICE_NAME"

COMPOSE_FILE="$INFRA_DIR/docker-compose.yml"
INCLUDE_LINE="  - ${SERVICE_NAME}/docker-compose.yml"

if [ -d "$SERVICE_DIR" ]; then
  echo "Service directory already exists: $SERVICE_DIR"
  # ensure include line exists in compose
  if ! grep -Fq "$INCLUDE_LINE" "$COMPOSE_FILE"; then
    awk -v nline="$INCLUDE_LINE" '1; /^include:/{getline; print nline; print; next}' "$COMPOSE_FILE" > "$COMPOSE_FILE.tmp" && mv "$COMPOSE_FILE.tmp" "$COMPOSE_FILE"
    echo "Added include entry to $COMPOSE_FILE"
  else
    echo "Include already present in $COMPOSE_FILE"
  fi
  exit 0
fi

mkdir -p "$SERVICE_DIR"
cat > "$SERVICE_DIR/docker-compose.yml" <<EOF
services:
  ${SERVICE_NAME}:
    image: myorg/${SERVICE_NAME}:latest
    networks:
      - infra_net
    ports:
      - "0"
EOF

# Create a placeholder secret and volume entries
mkdir -p "$SECRETS_DIR"
SECRET_FILE="$SECRETS_DIR/${SERVICE_NAME}_password.txt"
if [ ! -f "$SECRET_FILE" ]; then
  echo "your_${SERVICE_NAME}_password" > "$SECRET_FILE"
  echo "Created secret placeholder: $SECRET_FILE"
else
  echo "Secret file exists: $SECRET_FILE"
fi

# Add to Infra/docker-compose.yml include: (if not already present)
COMPOSE_FILE="$INFRA_DIR/docker-compose.yml"
INCLUDE_LINE="  - ${SERVICE_NAME}/docker-compose.yml"
if grep -Fq "$INCLUDE_LINE" "$COMPOSE_FILE"; then
  echo "Include already present in $COMPOSE_FILE"
else
  # insert after `include:` line
  awk -v nline="$INCLUDE_LINE" '1; /^include:/{getline; print nline; print; next}' "$COMPOSE_FILE" > "$COMPOSE_FILE.tmp" && mv "$COMPOSE_FILE.tmp" "$COMPOSE_FILE"
  echo "Added include entry to $COMPOSE_FILE"
fi

cat <<EOF
Created service scaffold: $SERVICE_DIR
Please open Infra/docker-compose.yml and verify entry, add volumes/secrets as required, and update Infra/README.md and README.md.
Local quick test:
  cd Infra/$SERVICE_NAME && docker compose up -d
  docker compose logs -f $SERVICE_NAME
EOF
