#!/bin/sh
set -eu

export SURREAL_USER="${SURREALDB_USERNAME:?SURREALDB_USERNAME is required}"

SURREAL_PASS="$(tr -d '\n' < /run/secrets/surreal_db_password)"
export SURREAL_PASS

exec /usr/local/bin/surreal start \
  --bind 0.0.0.0:8000 \
  rocksdb:/mydata/db.db
