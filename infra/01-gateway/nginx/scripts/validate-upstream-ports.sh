#!/bin/sh
# Validate template inputs before the official entrypoint runs envsubst.
set -eu

valid_port() {
  case "$1" in '' | *[!0-9]*) return 1 ;; esac
  [ "${#1}" -le 5 ] && [ "$1" -ge 1 ] && [ "$1" -le 65535 ]
}

valid_port "${OAUTH2_PROXY_PORT:-}" || {
  printf '%s\n' 'nginx: invalid upstream port' >&2
  exit 64
}
valid_port "${KEYCLOAK_PORT:-}" || {
  printf '%s\n' 'nginx: invalid upstream port' >&2
  exit 64
}

exec /docker-entrypoint.sh "$@"
