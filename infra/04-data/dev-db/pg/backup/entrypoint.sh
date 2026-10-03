#!/bin/sh
# Keep the pgBackRest passphrase out of tracked config and the process environment.
set -eu
umask 077
secret=/run/secrets/dev_pgbackrest_cipher_pass
include=/tmp/pgbackrest/conf.d

if [ ! -f "$secret" ] || [ -L "$secret" ] || [ ! -r "$secret" ]; then
  echo "dev-pg: backup cipher secret unavailable" >&2
  exit 64
fi
if [ "$(grep -c "" "$secret")" -gt 1 ]; then
  echo "dev-pg: backup cipher secret invalid" >&2
  exit 64
fi
pass="$(cat "$secret")"
if [ -z "$pass" ] || [ "${#pass}" -gt 512 ]; then
  echo "dev-pg: backup cipher secret invalid" >&2
  exit 64
fi
case "$pass" in
  *"$(printf '\r')"* | *'
'*) echo "dev-pg: backup cipher secret invalid" >&2; exit 64 ;;
esac
mkdir -p "$include"
printf '[global]\nrepo1-cipher-pass=%s\n' "$pass" > "$include/cipher.conf"
unset pass
chown -R postgres:postgres /tmp/pgbackrest
chmod 0700 /tmp/pgbackrest "$include"
chmod 0600 "$include/cipher.conf"
umask 022
exec docker-entrypoint.sh "$@"
