#!/bin/sh
set -eu

# DBT_ENV_SECRET_* values are redacted by dbt in logs and error output.
DBT_ENV_SECRET_PASSWORD="$(tr -d '\r\n' </run/secrets/dbt_db_password)"
if [ -z "$DBT_ENV_SECRET_PASSWORD" ]; then
  echo 'dbt: dbt_db_password secret is empty' >&2
  exit 64
fi
export DBT_ENV_SECRET_PASSWORD

exec dbt "$@"
