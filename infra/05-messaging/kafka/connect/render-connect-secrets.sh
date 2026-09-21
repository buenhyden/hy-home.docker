#!/bin/bash
# Render Kafka Connect FileConfigProvider inputs, then start the worker.
#
# Connectors reference ${file:/tmp/connect-secrets/debezium.properties:password}.
# The file is regenerated on every container start from the Docker secret, is
# readable only by the worker user, and lives on the /tmp tmpfs. The provider's
# allowed.paths restricts file lookups to this directory. An absent or empty
# secret leaves the file absent: the worker still starts for non-CDC use and a
# Debezium connector then fails at configuration time instead of silently.
set -euo pipefail

dir=/tmp/connect-secrets
secret=/run/secrets/debezium_postgres_password
umask 077
mkdir -p "$dir"
rm -f "$dir/debezium.properties"

if [ -f "$secret" ] && [ -s "$secret" ]; then
  value="$(cat "$secret")"
  case "$value" in
    *$'\r'* | *$'\n'*)
      echo 'connect-secrets: debezium_postgres_password contains a line break' >&2
      exit 64
      ;;
  esac
  # java.util.Properties escaping: backslash first, then any leading blank
  # (space, tab or form feed), which Properties.load would otherwise strip.
  value="${value//\\/\\\\}"
  case "$value" in
    [[:blank:]]* | $'\f'*) value="\\${value}" ;;
  esac
  printf 'password=%s\n' "$value" >"$dir/debezium.properties.tmp"
  mv "$dir/debezium.properties.tmp" "$dir/debezium.properties"
  echo 'connect-secrets: debezium.properties rendered'
else
  echo 'connect-secrets: debezium_postgres_password absent or empty; CDC connectors cannot authenticate' >&2
fi

exec /etc/confluent/docker/run
