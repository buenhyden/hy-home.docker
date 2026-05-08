#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

echo "Validating Docker Compose configuration..."

COMPOSE_PROFILES="${HYHOME_COMPOSE_PROFILES:-core}"
COMPOSE_PROFILE_ARGS=()
for profile in ${COMPOSE_PROFILES//,/ }; do
  if [ -n "$profile" ]; then
    COMPOSE_PROFILE_ARGS+=(--profile "$profile")
  fi
done

if [ "${#COMPOSE_PROFILE_ARGS[@]}" -eq 0 ]; then
  echo "No Docker Compose profiles resolved for validation."
  exit 1
fi

echo "Compose profiles: $COMPOSE_PROFILES"

CREATED_FILES=()
CLEANUP_ENV=false

cleanup() {
  local file
  for file in "${CREATED_FILES[@]}"; do
    rm -f "$file"
  done
  if [ "$CLEANUP_ENV" = true ]; then
    rm -f .env
  fi
}
trap cleanup EXIT

if [ ! -f .env ]; then
  cp .env.example .env
  CLEANUP_ENV=true
fi

mapfile -t SECRET_FILES < <(
  rg --no-filename '^[[:space:]]*file:[[:space:]]*' docker-compose.yml \
    | sed -E 's/^[[:space:]]*file:[[:space:]]*//; s/[[:space:]]+#.*$//; s/^["'"'"']|["'"'"']$//g'
)

for secret_file in "${SECRET_FILES[@]}"; do
  if [ ! -f "$secret_file" ]; then
    mkdir -p "$(dirname "$secret_file")"
    printf 'dummy\n' > "$secret_file"
    CREATED_FILES+=("$secret_file")
  fi
done

if ! docker compose "${COMPOSE_PROFILE_ARGS[@]}" config > /dev/null; then
  echo "Docker Compose validation failed."
  exit 1
fi

SERVICE_COUNT="$(
  docker compose "${COMPOSE_PROFILE_ARGS[@]}" config --services \
    | sed '/^[[:space:]]*$/d' \
    | wc -l \
    | tr -d ' '
)"

if [ "$SERVICE_COUNT" -eq 0 ]; then
  echo "Docker Compose validation failed: resolved service count is 0."
  exit 1
fi

echo "Docker Compose validation passed. services_total=$SERVICE_COUNT"
