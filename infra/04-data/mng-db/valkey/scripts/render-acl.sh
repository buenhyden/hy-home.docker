#!/bin/sh
# MNG Valkey ACL. The shared consumers (OAuth2 Proxy, n8n, Airflow, Gatus)
# keep authenticating as the default user with mng_valkey_password, exactly
# as with requirepass before. Named service roles get their own secrets, and
# no two roles may share one; their rules match the DEV roles.
set -eu

default_secret=${MNG_VALKEY_DEFAULT_SECRET_FILE:-/run/secrets/mng_valkey_password}
inspector_secret=${MNG_VALKEY_INSPECTOR_SECRET_FILE:-/run/secrets/mng_valkey_inspector_password}
acl_file=${MNG_VALKEY_ACL_FILE:-/run/valkey/users.acl}

fail() {
  printf '%s\n' "mng-valkey ACL: invalid input" >&2
  exit 1
}

hash_secret() {
  secret_path=$1
  [ -f "$secret_path" ] && [ ! -L "$secret_path" ] && [ -r "$secret_path" ] || fail
  [ "$(awk 'END { print NR }' "$secret_path")" -eq 1 ] || fail
  if LC_ALL=C grep -q '[[:cntrl:]]' "$secret_path"; then fail; fi
  [ "$(tr -d '\n' < "$secret_path" | wc -c)" -gt 0 ] || fail
  digest=$(tr -d '\n' < "$secret_path" | sha256sum)
  printf '%s\n' "${digest%% *}"
}

[ -d "${acl_file%/*}" ] || fail
umask 077
tmp_file=$(mktemp "${acl_file}.XXXXXXXX") || fail
trap 'rm -f "$tmp_file"' 0 1 2 3 15

seen_hashes='|'
role_line() {
  role_hash=$(hash_secret "$2")
  case "$seen_hashes" in *"|$role_hash|"*) fail ;; esac
  seen_hashes="${seen_hashes}${role_hash}|"
  printf 'user %s on #%s %s\n' "$1" "$role_hash" "$3" >> "$tmp_file"
}
: > "$tmp_file"
role_line default "$default_secret" '~* &* +@all'
role_line mnginspector "$inspector_secret" \
  '~* resetchannels -@all +@read +@connection -@dangerous +info'
chmod 600 "$tmp_file"
mv -f "$tmp_file" "$acl_file"
trap - 0 1 2 3 15
