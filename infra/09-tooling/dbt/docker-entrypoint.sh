#!/bin/sh
set -eu

export DBT_PASSWORD="$(
  tr -d '\r\n' </run/secrets/dbt_db_password
)"

exec dbt "$@"