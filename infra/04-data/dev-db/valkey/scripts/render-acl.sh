#!/bin/sh
set -eu

admin_secret=${DEV_VALKEY_ADMIN_SECRET_FILE:-/run/secrets/dev_valkey_admin_password}
monitor_secret=${DEV_VALKEY_MONITOR_SECRET_FILE:-/run/secrets/dev_valkey_monitor_password}
inspector_secret=${DEV_VALKEY_INSPECTOR_SECRET_FILE:-/run/secrets/dev_valkey_inspector_password}
projects_file=${DEV_VALKEY_PROJECTS_FILE:-/etc/dev-valkey/projects.tsv}
project_secrets=${DEV_VALKEY_PROJECT_SECRETS_DIR:-/run/valkey-project-secrets}
acl_file=${DEV_VALKEY_ACL_FILE:-/run/valkey/users.acl}

fail() {
  printf '%s\n' "dev-valkey ACL: invalid input" >&2
  exit 1
}

valid_name() {
  case "$1" in
    ''|*[!a-z0-9_-]*) return 1 ;;
    *) return 0 ;;
  esac
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

[ -f "$projects_file" ] && [ ! -L "$projects_file" ] && [ -r "$projects_file" ] || fail
[ -d "$project_secrets" ] && [ ! -L "$project_secrets" ] || fail
[ -d "${acl_file%/*}" ] || fail
umask 077
tmp_file=$(mktemp "${acl_file}.XXXXXXXX") || fail
trap 'rm -f "$tmp_file"' 0
trap 'rm -f "$tmp_file"; exit 1' 1 2 3 15

# Service roles are fixed here, one row each and one secret each; projects
# come from projects.tsv. No two roles or projects may share a secret.
#   devadmin     operator superuser
#   devmonitor   exporter metrics: no key or channel pattern, no state change
#   devinspector RedisInsight: read keys and server info, no write, no
#                @dangerous command (KEYS, CONFIG, ACL, FLUSH*, DEBUG)
seen_hashes='|'
role_line() {
  role_hash=$(hash_secret "$2")
  case "$seen_hashes" in *"|$role_hash|"*) fail ;; esac
  seen_hashes="${seen_hashes}${role_hash}|"
  printf 'user %s on #%s %s\n' "$1" "$role_hash" "$3" >> "$tmp_file"
}
printf 'user default off\n' > "$tmp_file"
role_line devadmin "$admin_secret" '~* &* +@all'
role_line devmonitor "$monitor_secret" \
  '-@all +ping +info +config|get +client|list +client|info +client|setname +slowlog|get +slowlog|len +latency|latest +latency|histogram +cluster|info'
role_line devinspector "$inspector_secret" \
  '~* resetchannels -@all +@read +@connection -@dangerous +info'
seen_projects='|'
seen_users='|default|devadmin|devmonitor|devinspector|'
seen_prefixes='|'
seen_secrets='|'
while IFS='|' read -r project_id acl_user key_prefix secret_name ||
  [ -n "$project_id$acl_user$key_prefix$secret_name" ]; do
  case "$project_id" in
    ''|'#'*) continue ;;
  esac
  valid_name "$project_id" && valid_name "$acl_user" &&
    valid_name "$key_prefix" && valid_name "$secret_name" || fail
  case "$seen_projects" in *"|$project_id|"*) fail ;; esac
  case "$seen_users" in *"|$acl_user|"*) fail ;; esac
  case "$seen_prefixes" in *"|$key_prefix|"*) fail ;; esac
  case "$seen_secrets" in *"|$secret_name|"*) fail ;; esac
  project_hash=$(hash_secret "$project_secrets/$secret_name")
  case "$seen_hashes" in *"|$project_hash|"*) fail ;; esac
  seen_hashes="${seen_hashes}${project_hash}|"
  printf 'user %s on #%s ~%s:* &%s:* db=0 +@read +@write +@transaction +ping -@dangerous -@scripting -@pubsub -scan -clusterscan -keys -randomkey -dbsize -sort\n' \
    "$acl_user" "$project_hash" "$key_prefix" "$key_prefix" >> "$tmp_file"
  seen_projects="${seen_projects}${project_id}|"
  seen_users="${seen_users}${acl_user}|"
  seen_prefixes="${seen_prefixes}${key_prefix}|"
  seen_secrets="${seen_secrets}${secret_name}|"
done < "$projects_file"
chmod 600 "$tmp_file"
mv -f "$tmp_file" "$acl_file"
trap - 0 1 2 3 15
