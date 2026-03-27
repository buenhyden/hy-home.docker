#!/usr/bin/env sh
set -eu

read_secret() {
  # usage: read_secret <path>
  # outputs secret to stdout without trailing newlines
  if [ ! -f "$1" ]; then
    echo "ERROR: missing secret file: $1" >&2
    exit 1
  fi
  # tr is present in alpine/busybox; tolerate a trailing newline.
  cat "$1" | tr -d '\n'
}

if [ -z "${PATRONI_SUPERUSER_USERNAME:-}" ]; then
  echo "ERROR: PATRONI_SUPERUSER_USERNAME is required" >&2
  exit 1
fi
if [ -z "${PATRONI_REPLICATION_USERNAME:-}" ]; then
  echo "ERROR: PATRONI_REPLICATION_USERNAME is required" >&2
  exit 1
fi

PATRONI_SUPERUSER_PASSWORD="$(read_secret /run/secrets/patroni_superuser_password)"
PATRONI_REPLICATION_PASSWORD="$(read_secret /run/secrets/patroni_replication_password)"

export PATRONI_SUPERUSER_PASSWORD
export PATRONI_REPLICATION_PASSWORD

# Compatibility env vars used by existing init/ops scripts and patterns.
export PGUSER_SUPERUSER="$PATRONI_SUPERUSER_USERNAME"
export PGPASSWORD_SUPERUSER="$PATRONI_SUPERUSER_PASSWORD"
export PGUSER_STANDBY="$PATRONI_REPLICATION_USERNAME"
export PGPASSWORD_STANDBY="$PATRONI_REPLICATION_PASSWORD"

for candidate in /launch.sh /docker-entrypoint.sh /entrypoint.sh; do
  if [ -x "$candidate" ]; then
    exec "$candidate" "$@"
  fi
done

echo "ERROR: could not locate Spilo entrypoint (tried /launch.sh, /docker-entrypoint.sh, /entrypoint.sh)" >&2
exit 1
