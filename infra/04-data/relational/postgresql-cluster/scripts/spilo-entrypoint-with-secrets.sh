#!/usr/bin/env sh
set -eu

read_secret() {
  # usage: read_secret <path>
  # outputs secret to stdout without trailing newlines
  if [ ! -f "$1" ]; then
    echo "ERROR: missing secret file: $1" >&2
    exit 1
  fi

  value="$(tr -d '\n' < "$1")"
  if [ -z "$value" ]; then
    echo "ERROR: empty secret file: $1" >&2
    exit 1
  fi

  printf '%s' "$value"
}

require_env() {
  # usage: require_env <VAR_NAME>
  var_name="$1"
  eval "var_value=\${$var_name:-}"
  if [ -z "$var_value" ]; then
    echo "ERROR: ${var_name} is required" >&2
    exit 1
  fi
}

# -------------------------------------------------------------------
# Required usernames for Patroni/Spilo native bootstrap
# -------------------------------------------------------------------
require_env PATRONI_SUPERUSER_USERNAME
require_env PATRONI_REPLICATION_USERNAME

# -------------------------------------------------------------------
# Optional custom username for downstream SQL init job
# (not consumed natively by Patroni/Spilo)
# -------------------------------------------------------------------
require_env PATRONI_EXPORTER_USERNAME

# -------------------------------------------------------------------
# Read secrets
# -------------------------------------------------------------------
PATRONI_SUPERUSER_PASSWORD="$(read_secret /run/secrets/patroni_superuser_password)"
PATRONI_REPLICATION_PASSWORD="$(read_secret /run/secrets/patroni_replication_password)"
PATRONI_EXPORTER_PASSWORD="$(read_secret /run/secrets/patroni_exporter_password)"

export PATRONI_SUPERUSER_PASSWORD
export PATRONI_REPLICATION_PASSWORD
export PATRONI_EXPORTER_PASSWORD

# -------------------------------------------------------------------
# Compatibility env vars for existing scripts / ops conventions
# -------------------------------------------------------------------
export PGUSER_SUPERUSER="$PATRONI_SUPERUSER_USERNAME"
export PGPASSWORD_SUPERUSER="$PATRONI_SUPERUSER_PASSWORD"

export PGUSER_STANDBY="$PATRONI_REPLICATION_USERNAME"
export PGPASSWORD_STANDBY="$PATRONI_REPLICATION_PASSWORD"

# Exporter credentials are exported only for downstream init/ops usage.
# Patroni/Spilo does not natively create this role.
export PGUSER_EXPORTER="$PATRONI_EXPORTER_USERNAME"
export PGPASSWORD_EXPORTER="$PATRONI_EXPORTER_PASSWORD"

# -------------------------------------------------------------------
# Execute original Spilo entrypoint
# -------------------------------------------------------------------
for candidate in /launch.sh /docker-entrypoint.sh /entrypoint.sh; do
  if [ -x "$candidate" ]; then
    echo "INFO: starting Spilo entrypoint via $candidate" >&2
    exec "$candidate" "$@"
  fi
done

echo "ERROR: could not locate Spilo entrypoint (tried /launch.sh, /docker-entrypoint.sh, /entrypoint.sh)" >&2
exit 1
