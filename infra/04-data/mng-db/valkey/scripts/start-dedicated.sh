#!/bin/sh
# Start a dedicated broker from a protected, atomically rendered ACL file.
set -eu

fail() {
  printf '%s\n' 'Dedicated Valkey: invalid input' >&2
  exit 1
}

case "$#" in
  2|3) ;;
  *) fail ;;
esac

default_secret=$1
acl_file=$2
monitor_secret=${3-}
port=${VALKEY_PORT:-6379}

# Validate before rendering so malformed configuration never replaces an ACL.
case "$port" in
  ''|*[!0-9]*) fail ;;
esac
[ "${#port}" -le 5 ] || fail
[ "$port" -ge 1 ] 2>/dev/null || fail
[ "$port" -le 65535 ] 2>/dev/null || fail

script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd -P) || fail
renderer=$script_dir/render-monitor-acl.sh
[ -f "$renderer" ] || fail
[ ! -L "$renderer" ] || fail

if [ -n "$monitor_secret" ]; then
  /bin/sh "$renderer" "$default_secret" "$monitor_secret" "$acl_file"
else
  /bin/sh "$renderer" "$default_secret" "$acl_file"
fi

exec valkey-server --aclfile "$acl_file" --appendonly yes --port "$port"
