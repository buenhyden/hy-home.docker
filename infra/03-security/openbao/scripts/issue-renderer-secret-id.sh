#!/bin/sh
# Six public args: server volume exact-image agent independent-journal-dir revision.
# Stdin: short issuer token, then separate short cleanup token. Never echo either.
set +x
set -eu
exec >/dev/null 2>&1
[ "$#" -eq 6 ] || exit 1
# Refuse an invocation alias that could select an attacker-owned adjacent helper.
[ -f "$0" ] && [ ! -L "$0" ] || exit 1
script_dir=$(CDPATH='' cd -P -- "$(/usr/bin/dirname -- "$0")" && pwd -P)
helper=$script_dir/renderer-issuance.py
[ -f "$helper" ] && [ ! -L "$helper" ] || exit 1
for trusted in "$script_dir" "$script_dir/$(/usr/bin/basename -- "$0")" "$helper"; do
  mode=$(/usr/bin/stat -c %a "$trusted")
  owner=$(/usr/bin/stat -c %u "$trusted")
  [ "$owner" = 0 ] || [ "$owner" = "$(/usr/bin/id -u)" ] || exit 1
  [ $((0$mode & 022)) -eq 0 ] || exit 1
done
# Isolated mode ignores PYTHONHOME/PYTHONPATH/user site and uses a fixed interpreter.
exec /usr/bin/python3 -I "$helper" "$@"
