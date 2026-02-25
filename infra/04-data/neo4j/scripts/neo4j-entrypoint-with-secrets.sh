#!/bin/sh
set -eu

PASSWORD_FILE="/run/secrets/neo4j_password"

if [ ! -f "$PASSWORD_FILE" ]; then
  echo "neo4j-entrypoint-with-secrets: missing $PASSWORD_FILE" >&2
  exit 1
fi

NEO4J_PASSWORD="$(tr -d '\n' < "$PASSWORD_FILE")"
NEO4J_USER="${NEO4J_USERNAME:-neo4j}"

if [ -z "$NEO4J_PASSWORD" ]; then
  echo "neo4j-entrypoint-with-secrets: secret neo4j_password is empty" >&2
  exit 1
fi

export NEO4J_AUTH="${NEO4J_USER}/${NEO4J_PASSWORD}"
exec /startup/docker-entrypoint.sh neo4j
