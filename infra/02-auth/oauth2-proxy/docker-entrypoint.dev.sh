#!/bin/sh
set -eu

read_secret() {
  secret_file="$1"
  if [ -f "$secret_file" ]; then
    tr -d '\r\n' <"$secret_file"
  fi
}

if [ -f /run/secrets/mng_valkey_password ]; then
  valkey_password="$(read_secret /run/secrets/mng_valkey_password)"
  if [ -n "$valkey_password" ] && [ -z "${OAUTH2_PROXY_REDIS_PASSWORD:-}" ]; then
    export OAUTH2_PROXY_REDIS_PASSWORD="$valkey_password"
  fi
fi

if [ "$#" -eq 0 ]; then
  set -- --config /etc/oauth2-proxy.cfg
fi

exec /bin/oauth2-proxy "$@"
