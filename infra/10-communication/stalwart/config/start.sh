#!/bin/sh
# The recovery admin comes from the Docker secret into this process only.
set -eu
secret=/run/secrets/stalwart_password
[ -f "$secret" ] || { echo 'stalwart: admin secret missing' >&2; exit 64; }
password="$(tr -d '\r\n' <"$secret")"
[ -n "$password" ] || { echo 'stalwart: admin secret empty' >&2; exit 64; }
STALWART_RECOVERY_ADMIN="${STALWART_ADMIN_USER:?}:$password"
export STALWART_RECOVERY_ADMIN
unset password
exec /usr/local/bin/stalwart --config /etc/stalwart/config.json
