#!/bin/sh
set -eu

require_secret() {
  if [ ! -s "$1" ]; then
    echo "missing required secret: $1" >&2
    exit 1
  fi
}

require_secret /run/secrets/n8n_db_password
require_secret /run/secrets/n8n_valkey_password
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
