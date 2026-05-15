#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

if ! command -v mkcert >/dev/null 2>&1; then
  echo "ERROR: mkcert is not installed."
  echo "Install mkcert first, then re-run this script."
  exit 1
fi

if [ ! -f .env ]; then
  echo "ERROR: .env is required. Create it from .env.example first."
  exit 1
fi

# shellcheck disable=SC1091
set -a
. ./.env
set +a

DOMAIN="${DEFAULT_URL:-127.0.0.1.nip.io}"
CERT_DIR="secrets/certs"

mkdir -p "$CERT_DIR"

echo "Installing local CA (mkcert -install)..."
mkcert -install

echo "Generating TLS cert/key for ${DOMAIN} and *.${DOMAIN} ..."
mkcert \
  -cert-file "${CERT_DIR}/cert.pem" \
  -key-file "${CERT_DIR}/key.pem" \
  "${DOMAIN}" \
  "*.${DOMAIN}"

CA_ROOT="$(mkcert -CAROOT)"
cp "${CA_ROOT}/rootCA.pem" "${CERT_DIR}/rootCA.pem"

chmod 600 "${CERT_DIR}/key.pem"
chmod 644 "${CERT_DIR}/cert.pem" "${CERT_DIR}/rootCA.pem"

echo "Generated files:"
echo "  - ${CERT_DIR}/cert.pem"
echo "  - ${CERT_DIR}/key.pem"
echo "  - ${CERT_DIR}/rootCA.pem"
