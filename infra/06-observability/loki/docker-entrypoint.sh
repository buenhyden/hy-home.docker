#!/bin/sh
set -eu

export MINIO_APP_USER_PASSWORD="$(tr -d '\n' </run/secrets/minio_app_user_password)"

exec /usr/bin/loki "$@"
