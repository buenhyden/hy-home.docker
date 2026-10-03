#!/bin/sh
set -eu

secret=/run/secrets/lab_valkey_password
[ -s "$secret" ] || { echo "LAB Valkey password is missing" >&2; exit 1; }
password=$(cat "$secret")
case "$password" in
  ''|*[!A-Za-z0-9_+./=:@#%-]*)
    echo "LAB Valkey password contains unsupported config characters" >&2
    exit 1
    ;;
esac

node_name=${NODE_NAME:-$(hostname)}
port=${PORT:-6379}
case "$node_name:$port" in
  *[!A-Za-z0-9:-]*|'') echo "Invalid LAB Valkey node or port" >&2; exit 1 ;;
esac
case "$port" in ''|*[!0-9]*) echo "Invalid LAB Valkey port" >&2; exit 1 ;; esac
[ "$port" -ge 1024 ] && [ "$port" -le 55535 ] || { echo "Invalid LAB Valkey port" >&2; exit 1; }

umask 077
config=/run/valkey-lab.conf
cat /usr/local/etc/valkey/valkey.conf > "$config"
printf '\nport %s\nrequirepass "%s"\nmasterauth "%s"\ncluster-announce-ip %s\ncluster-announce-port %s\ncluster-announce-bus-port %s\nappendonly yes\n' \
  "$port" "$password" "$password" "$node_name" "$port" "$((port + 10000))" >> "$config"
unset password
exec valkey-server "$config"
