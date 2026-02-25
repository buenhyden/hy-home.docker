#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

echo "Validating Docker Compose configuration..."

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

if [ ! -f infra/04-data/postgresql-cluster/.env.postgres ]; then
  cp infra/04-data/postgresql-cluster/.env.postgres.example infra/04-data/postgresql-cluster/.env.postgres
  CREATED_FILES+=("infra/04-data/postgresql-cluster/.env.postgres")
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

if ! docker compose config > /dev/null; then
  echo "Docker Compose validation failed."
  exit 1
fi

echo "Docker Compose validation passed."
