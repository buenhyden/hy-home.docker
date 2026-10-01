#!/bin/sh
# Shared input handling for feature-owned mng-pg provisioning jobs.
#
# Each capability (MLflow, dbt, Debezium) owns its SQL, grants and Compose job;
# this runner only validates inputs, waits for the server and runs that SQL.
#
# Environment contract:
#   PGHOST, PGPORT, PGUSER, PGDATABASE  administrator connection (libpq)
#   PROVISION_ADMIN_PASSWORD_FILE       administrator password secret file
#   PROVISION_SQL                       feature SQL file
#   PROVISION_IDENTIFIERS               names of env vars holding SQL identifiers
#   PROVISION_SECRETS                   NAME=<secret file path> pairs
#
# Secret values never appear on a command line: they are exported to the psql
# process environment and read with \getenv. Every missing or malformed input
# fails here, before any connection or DDL.
set -eu

fail() {
  printf 'provision: %s\n' "$1" >&2
  exit 64
}

read_secret() {
  # $1 = file. Rejects non-regular, unreadable, empty, multi-line or oversized
  # values; command substitution drops trailing newlines written by an editor.
  if [ ! -f "$1" ] || [ -L "$1" ]; then
    fail "secret is not a regular file: $1"
  fi
  [ -r "$1" ] || fail "secret is not readable: $1"
  value="$(cat "$1")"
  [ -n "$value" ] || fail "secret is empty: $1"
  case "$value" in
    *"$(printf '\r')"* | *"
"*) fail "secret contains a line break: $1" ;;
  esac
  [ "${#value}" -le 512 ] || fail "secret exceeds 512 characters: $1"
  printf '%s' "$value"
}

if [ -z "${PROVISION_SQL:-}" ] || [ ! -f "$PROVISION_SQL" ]; then
  fail "PROVISION_SQL is not a file"
fi
for name in PGHOST PGPORT PGUSER PGDATABASE PROVISION_ADMIN_PASSWORD_FILE; do
  eval "v=\${$name:-}"
  [ -n "$v" ] || fail "$name is required"
done

for name in ${PROVISION_IDENTIFIERS:-}; do
  printf '%s' "$name" | grep -Eq '^[A-Z][A-Z0-9_]*$' || fail "bad identifier variable name: $name"
  eval "v=\${$name:-}"
  case "$v" in
    *"
"*) fail "$name must be a single line" ;;
  esac
  printf '%s' "$v" | grep -Eq '^[a-z_][a-z0-9_]{0,62}$' \
    || fail "$name must match ^[a-z_][a-z0-9_]{0,62}$"
done

for pair in ${PROVISION_SECRETS:-}; do
  name="${pair%%=*}"
  file="${pair#*=}"
  printf '%s' "$name" | grep -Eq '^[A-Z][A-Z0-9_]*$' || fail "bad secret variable name: $name"
  value="$(read_secret "$file")" || exit $?
  export "$name=$value"
done

PGPASSWORD="$(read_secret "$PROVISION_ADMIN_PASSWORD_FILE")" || exit $?
export PGPASSWORD

tries=0
until pg_isready -q; do
  tries=$((tries + 1))
  [ "$tries" -lt 90 ] || fail "server $PGHOST:$PGPORT not ready after 180 seconds"
  sleep 2
done

exec psql -X -v ON_ERROR_STOP=1 -f "$PROVISION_SQL"
