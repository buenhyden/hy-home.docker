#!/bin/sh
set -eu

MINIO_APP_USER_PASSWORD="$(tr -d '\n' </run/secrets/minio_app_user_password)"
export MINIO_APP_USER_PASSWORD

exec /usr/bin/tempo "$@"
