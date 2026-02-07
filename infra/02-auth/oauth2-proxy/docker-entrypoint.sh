#!/bin/sh
set -eu

if [ -f /run/secrets/valkey_password ]; then
  valkey_password="$(tr -d '\n' < /run/secrets/valkey_password)"
  export OAUTH2_PROXY_REDIS_CONNECTION_URL="redis://:${valkey_password}@oauth2-proxy-valkey:6379"
fi

exec /bin/oauth2-proxy "$@"
