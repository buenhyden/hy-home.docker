#!/bin/sh
# Validate the public port/material contract before the image launcher writes config.
set -eu
umask 077
for port in "${OPENBAO_PORT:-}" "${OPENBAO_CLUSTER_PORT:-}"; do
  case "$port" in '' | *[!0-9]*) exit 64 ;; esac
  [ "${#port}" -le 5 ] && [ "$port" -ge 1 ] && [ "$port" -le 65535 ] || exit 64
done
[ "$OPENBAO_PORT" != "$OPENBAO_CLUSTER_PORT" ] || exit 64
for path in /openbao/tls/ca.pem /openbao/tls/server.pem /openbao/tls/server-key.pem; do
  [ -f "$path" ] && [ -r "$path" ] && [ -s "$path" ] || exit 66
done
exec docker-entrypoint.sh "$@"
