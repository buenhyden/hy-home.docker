#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

usage() {
  cat <<'EOF'
Usage: bash scripts/validation/validate-docker-compose.sh [--preflight]

Modes:
  default      CI-safe structural validation. May create temporary .env and
               dummy secret files, then remove files it created.
  --preflight  Real local prerequisite check. Does not create .env, secret
               files, cert files, or dummy data.
EOF
}

MODE="validate"
if [ "$#" -gt 1 ]; then
  usage >&2
  exit 2
fi
case "${1-}" in
  "")
    ;;
  --preflight)
    MODE="preflight"
    ;;
  --help|-h)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

ok() {
  echo "[OK] $1"
}

warn() {
  echo "[WARN] $1"
}

fail() {
  echo "[FAIL] $1"
  FAILED=1
}

check_file() {
  local path="$1"
  if [ -f "$path" ]; then
    ok "file exists: $path"
  else
    fail "missing file: $path"
  fi
}

check_dir() {
  local path="$1"
  if [ -z "$path" ]; then
    fail "required directory variable is empty"
    return
  fi
  if [ -d "$path" ]; then
    ok "dir exists: $path"
    if [ -w "$path" ]; then
      ok "dir writable: $path"
    else
      warn "dir is not writable by current user: $path"
    fi
  else
    fail "missing dir: $path"
  fi
}

is_optional_secret() {
  local path="$1"
  case "$path" in
    ./secrets/db/cassandra/cassandra_password.txt|\
    ./secrets/db/mongodb/mongodb_root_password.txt|\
    ./secrets/db/mongodb/mongo_express_basicauth_password.txt|\
    ./secrets/db/neo4j/neo4j_password.txt|\
    ./secrets/db/valkey/airflow_password.txt|\
    ./secrets/tools/syncthing_password.txt)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

compose_secret_files() {
  rg --no-filename '^[[:space:]]*file:[[:space:]]*' docker-compose.yml \
    | sed -E 's/^[[:space:]]*file:[[:space:]]*//; s/[[:space:]]+#.*$//; s/^["'"'"']|["'"'"']$//g'
}

run_preflight() {
  echo "Running Docker Compose preflight checks..."
  echo "Preflight mode does not create .env, secret files, cert files, or dummy data."

  FAILED=0

  if [ ! -f .env ]; then
    fail "missing .env (copy from .env.example first)"
  else
    ok "file exists: .env"
    # shellcheck disable=SC1091
    set -a
    . ./.env
    set +a
  fi

  check_file "./secrets/db/postgres/patroni_superuser_password.txt"
  check_file "./secrets/db/postgres/patroni_replication_password.txt"

  check_file "secrets/certs/rootCA.pem"
  check_file "secrets/certs/cert.pem"
  check_file "secrets/certs/key.pem"

  mapfile -t SECRET_FILES < <(compose_secret_files)

  local secret_file
  for secret_file in "${SECRET_FILES[@]}"; do
    if is_optional_secret "$secret_file"; then
      if [ -f "$secret_file" ]; then
        ok "optional file exists: $secret_file"
      else
        warn "optional file missing (only required for optional stacks): $secret_file"
      fi
    else
      check_file "$secret_file"
    fi
  done

  check_dir "${DEFAULT_MOUNT_VOLUME_PATH:-}"
  check_dir "${DEFAULT_AUTH_DIR:-}"
  check_dir "${DEFAULT_DATA_DIR:-}"
  check_dir "${DEFAULT_MESSAGE_BROKER_DIR:-}"
  check_dir "${DEFAULT_OBSERVABILITY_DIR:-}"

  local net
  for net in project_net kind; do
    if docker network inspect "$net" >/dev/null 2>&1; then
      ok "external network exists: $net"
    else
      warn "external network not found (optional for core boot): $net"
    fi
  done

  if [ "$FAILED" -ne 0 ]; then
    echo "Preflight checks failed."
    exit 1
  fi

  echo "Preflight checks passed."
}

if [ "$MODE" = "preflight" ]; then
  run_preflight
  exit 0
fi

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

mapfile -t SECRET_FILES < <(compose_secret_files)

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
