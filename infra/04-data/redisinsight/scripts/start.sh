#!/bin/sh
# RedisInsight entrypoint: load the DEV and MNG inspector passwords and the stored
# connection encryption key from secret files into the environment the image
# reads, then start the image's own entrypoint. Values never reach argv.
set -eu

read_secret() {
  [ -f "$1" ] && [ ! -L "$1" ] && [ -r "$1" ] || {
    echo "redisinsight: secret $1 is missing or unreadable" >&2
    exit 64
  }
  value=$(tr -d '\r\n' < "$1")
  [ "${#value}" -ge 16 ] || {
    echo "redisinsight: secret $1 must be at least 16 characters" >&2
    exit 64
  }
  printf '%s' "$value"
}

RI_REDIS_PASSWORD1=$(read_secret /run/secrets/dev_valkey_inspector_password)
RI_REDIS_PASSWORD2=$(read_secret /run/secrets/mng_valkey_inspector_password)
RI_ENCRYPTION_KEY=$(read_secret /run/secrets/redisinsight_encryption_key)
export RI_REDIS_PASSWORD1 RI_REDIS_PASSWORD2 RI_ENCRYPTION_KEY
cd /usr/src/app
exec ./docker-entry.sh node redisinsight/api/dist/src/main
