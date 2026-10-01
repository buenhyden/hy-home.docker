#!/bin/sh
# Hand the pgBackRest repository passphrase to every pgBackRest process
# (archive_command and operator commands) without placing it in the process
# environment or the tracked config, then start the official entrypoint.
set -eu
umask 077

secret=/run/secrets/pgbackrest_cipher_pass
include=/tmp/pgbackrest/conf.d

if [ ! -f "$secret" ] || [ -L "$secret" ]; then
    echo "pgbackrest: cipher secret missing or not a regular file" >&2
    exit 64
fi
if [ "$(grep -c '' "$secret")" -gt 1 ]; then
    echo "pgbackrest: cipher secret must be a single line" >&2
    exit 64
fi
pass="$(tr -d '\r\n' <"$secret")"
case "$pass" in
    '' | *[[:space:]]*)
        echo "pgbackrest: cipher secret is empty or contains whitespace" >&2
        exit 64
        ;;
esac

mkdir -p "$include"
printf '[global]\nrepo1-cipher-pass=%s\n' "$pass" >"$include/cipher.conf"
unset pass
chown -R postgres:postgres /tmp/pgbackrest
chmod 0700 /tmp/pgbackrest "$include"
chmod 0600 "$include/cipher.conf"

# Restore the image default: the official entrypoint creates PGDATA parents as
# root and the postgres user must still traverse them.
umask 022
exec docker-entrypoint.sh "$@"
