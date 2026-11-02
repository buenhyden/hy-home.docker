#!/bin/sh
set -eu
port=${MNG_VALKEY_PORT-6379}
case "$port" in '' | *[!0-9]*) exit 64 ;; esac
[ "${#port}" -le 5 ] && [ "$port" -ge 1 ] && [ "$port" -le 65535 ] || exit 64
/bin/sh /usr/local/libexec/mng-valkey/render-acl.sh
exec valkey-server --aclfile /run/valkey/users.acl --appendonly yes --port "$port"
