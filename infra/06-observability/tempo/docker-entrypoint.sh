#!/bin/sh
set -eu

[ -r /run/secrets/minio_app_user_password ] || {
  echo "missing secret: /run/secrets/minio_app_user_password" >&2
  exit 1
}

MINIO_APP_USER_PASSWORD="$(tr -d '\n' </run/secrets/minio_app_user_password)"
export MINIO_APP_USER_PASSWORD

exec /usr/bin/tempo "$@"
