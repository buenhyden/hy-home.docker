#!/bin/sh
# Render plan.ndjson for DEFAULT_URL and apply it as the recovery admin. Every
# operation is an upsert, update or reconcile, so a re-run converges.
set -eu
secret=/run/secrets/stalwart_password
[ -f "$secret" ] || { echo 'stalwart-config: admin secret missing' >&2; exit 64; }
STALWART_PASSWORD="$(tr -d '\r\n' <"$secret")"
[ -n "$STALWART_PASSWORD" ] || { echo 'stalwart-config: admin secret empty' >&2; exit 64; }
: "${DEFAULT_URL:?}" "${STALWART_URL:?}" "${STALWART_USER:?}"
case "$DEFAULT_URL" in *[!A-Za-z0-9.-]*|'') echo 'stalwart-config: DEFAULT_URL is not a host name' >&2; exit 64 ;; esac
export STALWART_PASSWORD
sed "s/__DOMAIN__/$DEFAULT_URL/g" /opt/hyhome/plan.ndjson >/tmp/plan.ndjson
exec stalwart-cli apply --file /tmp/plan.ndjson
