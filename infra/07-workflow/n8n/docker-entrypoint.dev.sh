#!/bin/sh
set -eu

require_secret() {
  if [ ! -s "$1" ]; then
    echo "missing required secret: $1" >&2
    exit 1
  fi
}

require_secret /run/secrets/n8n_db_password
case "${N8N_VALKEY_HOST:-mng-valkey}:${N8N_VALKEY_SECRET:-mng_valkey_password}" in
  mng-valkey:mng_valkey_password|n8n-valkey:n8n_valkey_password) ;;
  *) echo "unsupported n8n broker/secret selection" >&2; exit 1 ;;
esac
require_secret "/run/secrets/${N8N_VALKEY_SECRET:-mng_valkey_password}"
require_secret /run/secrets/n8n_encryption_key
require_secret /run/secrets/n8n_runner_auth_token

if [ -d /opt/custom-certificates ]; then
  echo "Trusting custom certificates from /opt/custom-certificates."
  export NODE_OPTIONS="--use-openssl-ca ${NODE_OPTIONS:-}"
  export SSL_CERT_DIR=/opt/custom-certificates
  c_rehash /opt/custom-certificates || true
fi

if [ "$#" -gt 0 ]; then
  # Got started with arguments
  exec n8n "$@"
else
  # Got started without arguments
  exec n8n
fi
