#!/bin/sh
set -eu

read_secret() {
  secret_file="$1"
  if [ -f "$secret_file" ]; then
    tr -d '\r\n' <"$secret_file"
  fi
}

if [ -z "${OAUTH2_PROXY_COOKIE_SECRET:-}" ] && [ -f /run/secrets/oauth2_proxy_cookie_secret ]; then
  export OAUTH2_PROXY_COOKIE_SECRET="$(read_secret /run/secrets/oauth2_proxy_cookie_secret)"
fi

if [ -z "${OAUTH2_PROXY_CLIENT_SECRET:-}" ] && [ -f /run/secrets/oauth2_proxy_client_secret ]; then
  export OAUTH2_PROXY_CLIENT_SECRET="$(read_secret /run/secrets/oauth2_proxy_client_secret)"
fi

if [ -f /run/secrets/mng_valkey_password ]; then
  valkey_password="$(read_secret /run/secrets/mng_valkey_password)"
  export OAUTH2_PROXY_REDIS_CONNECTION_URL="redis://:${valkey_password}@mng-valkey:6379"
fi

if [ "$#" -eq 0 ]; then
  set -- --config /etc/oauth2-proxy.cfg
fi

exec /bin/oauth2-proxy "$@"
