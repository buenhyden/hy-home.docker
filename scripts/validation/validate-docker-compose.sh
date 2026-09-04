#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

usage() {
  cat <<'EOF'
Usage: bash scripts/validation/validate-docker-compose.sh [--preflight]

Modes:
  default      CI-safe structural validation. May create temporary .env and
               dummy secret files, then remove files it created. Renders every
               declared profile one at a time and fails when one profile
               selects two services that publish the same host port.
  --preflight  Real local prerequisite check. Does not create .env, secret
               files, cert files, or dummy data.

Environment:
  HYHOME_COMPOSE_PROFILES  Space- or comma-separated profile names to validate
                           as one selection. When unset, the default mode
                           validates every profile Compose declares and
                           preflight uses `core`.
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
--help | -h)
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
  echo "FAIL: $1"
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
  ./secrets/db/cassandra/cassandra_password.txt | \
    ./secrets/db/mongodb/mongodb_root_password.txt | \
    ./secrets/db/mongodb/mongo_express_basicauth_password.txt | \
    ./secrets/db/neo4j/neo4j_password.txt | \
    ./secrets/db/valkey/airflow_password.txt | \
    ./secrets/messaging/rabbitmq_user.txt | \
    ./secrets/messaging/rabbitmq_password.txt | \
    ./secrets/tools/syncthing_password.txt)
    return 0
    ;;
  *)
    return 1
    ;;
  esac
}

compose_secret_files() {
  docker compose "${PROFILE_ARGS[@]}" config 2>/dev/null |
    sed -nE 's/^[[:space:]]*file:[[:space:]]*//p' |
    sed -E 's/[[:space:]]+#.*$//; s/^["'"'"']|["'"'"']$//g' |
    while IFS= read -r secret_file; do
      case "$secret_file" in
      "$BASE_DIR"/*)
        printf './%s\n' "${secret_file#"$BASE_DIR"/}"
        ;;
      *)
        printf '%s\n' "$secret_file"
        ;;
      esac
    done |
    sort -u
}

profile_args_from() {
  local names="$1"
  local profile
  PROFILE_ARGS=()
  for profile in ${names//,/ }; do
    if [ -n "$profile" ]; then
      PROFILE_ARGS+=(--profile "$profile")
    fi
  done
}

# Preflight keeps its historical default so a local prerequisite check does not
# start demanding the secrets of every optional stack.
PREFLIGHT_PROFILES="${HYHOME_COMPOSE_PROFILES:-core}"

# Resolving every declared profile renders the model, which needs a usable
# .env. Validate mode creates one first, so the enumeration happens there.
resolve_validate_selections() {
  if [ -n "${HYHOME_COMPOSE_PROFILES:-}" ]; then
    SELECTION_MODE="named"
    VALIDATE_SELECTIONS=("$HYHOME_COMPOSE_PROFILES")
  else
    SELECTION_MODE="every-declared"
    mapfile -t VALIDATE_SELECTIONS < <(docker compose config --profiles | sed '/^[[:space:]]*$/d')
  fi

  if [ "${#VALIDATE_SELECTIONS[@]}" -eq 0 ]; then
    echo "No Docker Compose profiles resolved for validation."
    exit 1
  fi
}

# Every service a single profile selects must publish a distinct host port.
# Compose only reports a collision at `up`, so the check is static here.
report_port_collisions() {
  docker compose "${PROFILE_ARGS[@]}" config --format json |
    python3 -c '
import collections, json, sys

model = json.load(sys.stdin)
bindings = collections.defaultdict(list)
for name, body in (model.get("services") or {}).items():
    for port in (body.get("ports") or []):
        published = port.get("published")
        if published:
            key = (port.get("host_ip", "0.0.0.0"), str(published), port.get("protocol", "tcp"))
            bindings[key].append(name)

collisions = {key: names for key, names in bindings.items() if len(names) > 1}
for (host, published, protocol), names in sorted(collisions.items()):
    print(f"{host}:{published}/{protocol} <- {", ".join(sorted(names))}")
sys.exit(1 if collisions else 0)
'
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

  profile_args_from "$PREFLIGHT_PROFILES"

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

resolve_validate_selections
echo "Selection mode: $SELECTION_MODE"
echo "Selections: ${VALIDATE_SELECTIONS[*]}"

# Discover secrets across every selection at once, so a stack validated later
# in the loop does not fail on a secret file the earlier scan never saw.
profile_args_from "${VALIDATE_SELECTIONS[*]}"

mapfile -t SECRET_FILES < <(compose_secret_files)

for secret_file in "${SECRET_FILES[@]}"; do
  if [ ! -f "$secret_file" ]; then
    mkdir -p "$(dirname "$secret_file")"
    printf 'dummy\n' >"$secret_file"
    CREATED_FILES+=("$secret_file")
  fi
done

VALIDATION_FAILED=0
SERVICE_TOTAL=0

for selection in "${VALIDATE_SELECTIONS[@]}"; do
  profile_args_from "$selection"

  if ! docker compose "${PROFILE_ARGS[@]}" config >/dev/null; then
    echo "FAIL: $selection: Compose configuration did not render."
    VALIDATION_FAILED=1
    continue
  fi

  selection_count="$(
    docker compose "${PROFILE_ARGS[@]}" config --services |
      sed '/^[[:space:]]*$/d' |
      wc -l |
      tr -d ' '
  )"

  if [ "$selection_count" -eq 0 ]; then
    echo "FAIL: $selection: resolved service count is 0."
    VALIDATION_FAILED=1
    continue
  fi

  if ! collisions="$(report_port_collisions)"; then
    echo "FAIL: $selection: two selected services publish the same host port."
    printf '  %s\n' "$collisions"
    VALIDATION_FAILED=1
    continue
  fi

  SERVICE_TOTAL=$((SERVICE_TOTAL + selection_count))
  echo "[OK] $selection: services=$selection_count"
done

if [ "$VALIDATION_FAILED" -ne 0 ]; then
  echo "Docker Compose validation failed."
  exit 1
fi

echo "Docker Compose validation passed. selections=${#VALIDATE_SELECTIONS[@]} services_total=$SERVICE_TOTAL"
