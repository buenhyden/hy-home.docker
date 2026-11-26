#!/bin/sh
set -eu

read_secret() {
  secret_file="$1"
  if [ -f "$secret_file" ]; then
    tr -d '\r\n' <"$secret_file"
  fi
}

# Session store login: the named oauth2proxy role (default) or the shared
# default user as rollback. Any other pairing stops before oauth2-proxy runs.
valkey_user=${OAUTH2_PROXY_VALKEY_USERNAME-oauth2proxy}
valkey_secret=${OAUTH2_PROXY_VALKEY_SECRET:-mng_valkey_oauth2_proxy_password}
case "$valkey_user:$valkey_secret" in
  oauth2proxy:mng_valkey_oauth2_proxy_password|:mng_valkey_password) ;;
  *) echo "unsupported oauth2-proxy session store selection" >&2; exit 1 ;;
esac
valkey_password="$(read_secret "/run/secrets/$valkey_secret")"
if [ -z "$valkey_password" ]; then
  echo "missing required secret: /run/secrets/$valkey_secret" >&2
  exit 1
fi
if [ -z "${OAUTH2_PROXY_REDIS_PASSWORD:-}" ]; then
  export OAUTH2_PROXY_REDIS_PASSWORD="$valkey_password"
fi
if [ -n "$valkey_user" ]; then
  export OAUTH2_PROXY_REDIS_USERNAME="$valkey_user"
fi
unset valkey_password

if [ "$#" -eq 0 ]; then
  set -- --config /etc/oauth2-proxy.cfg
fi

exec /bin/oauth2-proxy "$@"
