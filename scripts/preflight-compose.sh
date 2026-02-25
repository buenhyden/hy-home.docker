#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

FAILED=0

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

echo "Running Docker Compose preflight checks..."

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

mapfile -t SECRET_FILES < <(
  rg --no-filename '^[[:space:]]*file:[[:space:]]*' docker-compose.yml \
    | sed -E 's/^[[:space:]]*file:[[:space:]]*//; s/[[:space:]]+#.*$//; s/^["'"'"']|["'"'"']$//g'
)

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
