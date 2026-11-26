#!/bin/sh
# MNG Valkey ACL. n8n, OAuth2 Proxy and Airflow authenticate as their own
# named roles, each limited to its key prefix and DB 0; the default user keeps
# mng_valkey_password for administration, health checks, backup and rollback.
# Named service roles get their own secrets, and no two roles may share one.
set -eu

default_secret=${MNG_VALKEY_DEFAULT_SECRET_FILE:-/run/secrets/mng_valkey_password}
monitor_secret=${MNG_VALKEY_MONITOR_SECRET_FILE:-/run/secrets/mng_valkey_monitor_password}
inspector_secret=${MNG_VALKEY_INSPECTOR_SECRET_FILE:-/run/secrets/mng_valkey_inspector_password}
acl_file=${MNG_VALKEY_ACL_FILE:-/run/valkey/users.acl}
n8n_enabled=${MNG_VALKEY_N8N_ENABLED-0}
n8n_secret=${MNG_VALKEY_N8N_SECRET_FILE:-/run/secrets/mng_valkey_n8n_password}
oauth2_proxy_secret=${MNG_VALKEY_OAUTH2_PROXY_SECRET_FILE:-/run/secrets/mng_valkey_oauth2_proxy_password}
airflow_secret=${MNG_VALKEY_AIRFLOW_SECRET_FILE:-/run/secrets/mng_valkey_airflow_password}

fail() {
  printf '%s\n' "mng-valkey ACL: invalid input" >&2
  exit 1
}

case "$n8n_enabled" in 0|1) ;; *) fail ;; esac
if [ "$n8n_enabled" = 1 ]; then
  [ -f "$n8n_secret" ] && [ ! -L "$n8n_secret" ] && [ -r "$n8n_secret" ] || fail
  metadata=$(stat -c '%u %g %a %h' "$n8n_secret") || fail
  set -- $metadata
  [ "$4" = 1 ] || fail
  case "$3" in
    400|600) [ "$1" = "$(id -u)" ] || fail ;;
    440|640)
      case " $(id -G) " in *" $2 "*) ;; *) fail ;; esac ;;
    *) fail ;;
  esac
fi

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
trap 'rm -f "$tmp_file"' 0
trap 'rm -f "$tmp_file"; exit 1' 1 2 3 15

seen_hashes='|'
role_line() {
  role_hash=$(hash_secret "$2")
  case "$seen_hashes" in *"|$role_hash|"*) fail ;; esac
  seen_hashes="${seen_hashes}${role_hash}|"
  printf 'user %s on #%s %s\n' "$1" "$role_hash" "$3" >> "$tmp_file"
}
: > "$tmp_file"
role_line default "$default_secret" '~* &* +@all'
role_line mngmonitor "$monitor_secret" \
  '-@all +ping +info +command|info +slowlog|len +commandlog|len'
role_line mnginspector "$inspector_secret" \
  '~* resetchannels -@all +@read +@connection -@dangerous +info'
if [ "$n8n_enabled" = 1 ]; then
  # Bull queue grants plus the n8n 2.43 cache store (mget mset getdel hexists
  # hkeys hvals), instance-registry Lua (pexpire) and the LPOP loop n8n's
  # patched Bull uses to return claimed jobs; keys, scan and flushdb stay denied.
  role_line n8n "$n8n_secret" \
    '~n8n:* &n8n:* db=0 -@all +ping +info +auth +select +quit +client|setname +client|setinfo +script|load +eval +evalsha +del +exists +get +hdel +hget +hgetall +hincrby +hmget +hmset +hset +incr +lindex +linsert +llen +lpush +lrange +lrem +lset +ltrim +psetex +pttl +publish +rename +rpoplpush +brpoplpush +rpush +sadd +scard +set +sismember +smembers +srem +type +zadd +zcard +zcount +zrange +zrangebyscore +zrem +zremrangebyrank +zremrangebyscore +zrevrange +zrevrangebyscore +zscore +expire +subscribe +unsubscribe +psubscribe +punsubscribe +multi +exec +mget +mset +getdel +hexists +hkeys +hvals +pexpire +lpop'
fi
# OAuth2 Proxy session tickets are "<cookie_name>-<ticket>" plus a ".lock"
# key that its lock library sets through Lua (oauth2-proxy.cfg cookie_name).
role_line oauth2proxy "$oauth2_proxy_secret" \
  '~__Secure-sso-cookie-* resetchannels db=0 -@all +ping +auth +hello +select +quit +client|setname +client|setinfo +script|load +eval +evalsha +get +set +del +exists +expire +pexpire +pttl'
# Celery with kombu global_keyprefix "airflow:" prefixes keys and channels.
# PSUBSCRIBE patterns are matched literally, so the pidbox and event patterns
# the worker and event receivers subscribe to are listed as they are sent.
role_line airflow "$airflow_secret" \
  '~airflow:* &airflow:* &airflow:/0.celery.pidbox &airflow:/0.celeryev/* &airflow:/0.celeryev/worker.* db=0 -@all +ping +auth +hello +select +quit +client|setname +client|setinfo +script|load +eval +evalsha +multi +exec +discard +watch +unwatch +get +set +del +exists +expire +pexpire +pttl +llen +lpush +rpush +lpop +brpop +lrange +lrem +sadd +srem +smembers +scard +hset +hget +hdel +hgetall +zadd +zrem +zrangebyscore +zrevrangebyscore +zcard +publish +subscribe +unsubscribe +psubscribe +punsubscribe'
chmod 600 "$tmp_file"
mv -f "$tmp_file" "$acl_file"
trap - 0 1 2 3 15
