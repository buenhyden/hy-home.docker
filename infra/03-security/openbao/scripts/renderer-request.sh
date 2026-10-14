#!/bin/sh
# Public argv: internal timeout, then exact Bao operation/options/path.
# Stdin: one selected short token line, followed by the optional JSON request.
set +x
set -eu
PATH=/bin:/usr/bin
export PATH
case "${BAO_ADDR:-}" in https://127.0.0.1:*) ;; *) exit 1;; esac
port=${BAO_ADDR#https://127.0.0.1:}
case "$port" in ""|*[!0-9]*) exit 1;; esac
[ "$port" -gt 0 ] && [ "$port" -le 65535 ] || exit 1
[ "${BAO_CACERT:-}" = /openbao/tls/ca.pem ] && [ -r "$BAO_CACERT" ] || exit 1
[ "${BAO_TLS_SERVER_NAME:-}" = openbao ]
# Clear every ambient CLI/proxy/header/config variable before receiving token bytes.
# shellcheck disable=SC2016 # The receiving shell expands the private script.
exec /usr/bin/env -i PATH=/bin:/usr/bin BAO_ADDR="$BAO_ADDR" \
    BAO_CACERT="$BAO_CACERT" BAO_TLS_SERVER_NAME=openbao /bin/sh -c '
set +x
set -eu
umask 077
unset PWD OLDPWD
[ -d /dev/shm ] && [ ! -L /dev/shm ] || exit 1
[ "$(stat -f -c %T /dev/shm)" = tmpfs ]
private=$(mktemp -d /dev/shm/renderer-issuance.XXXXXX)
case "$private" in /dev/shm/renderer-issuance.??????) ;; *) exit 125;; esac
child=
cleanup() {
    result=$?
    trap - EXIT HUP INT TERM
    if [ -n "$child" ]; then
        kill -TERM "$child" 2>/dev/null || :
        wait "$child" 2>/dev/null || :
    fi
    rm -f "$private/token" || result=125
    rmdir "$private" || result=125
    exit "$result"
}
trap cleanup EXIT
trap "exit 124" HUP INT TERM
[ -d "$private" ] && [ ! -L "$private" ] || exit 1
[ "$(stat -c %a:%u "$private")" = "700:$(id -u)" ]
[ "$(stat -f -c %T "$private")" = tmpfs ]
[ "$(stat -c %d "$private")" = "$(stat -c %d /dev/shm)" ]
# noclobber and a fresh private directory prevent opening a pre-existing inode.
(set -C; : >"$private/token")
[ -f "$private/token" ] && [ ! -L "$private/token" ] || exit 1
[ "$(stat -c %a:%h:%u "$private/token")" = "600:1:$(id -u)" ]
IFS= read -r token
printf %s "$token" >"$private/token"
unset token
export HOME="$private" BAO_TOKEN_PATH="$private/token"
limit=$1
shift
for argument do
    case "$argument" in auth/approle/role/hy-home-renderer/secret-id-accessor/destroy) exec >/dev/null;; esac
done
# The CLI deadline expires before the receiving-shell deadline and Docker timeout.
# timeout stays as the child supervisor and forwards termination to the CLI.
exec 3<&0
timeout -s TERM -k 1 "$limit" bao "$@" <&3 3<&- &
child=$!
exec 3<&-
result=0
wait "$child" || result=$?
child=
exit "$result"
' renderer-request "$@"
