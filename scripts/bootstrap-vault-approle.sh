#!/usr/bin/env bash
# scripts/bootstrap-vault-approle.sh
# Automates the creation of Vault Agent policies, AppRole authentication, and credential extraction.

set -euo pipefail

# Ensure we're at the root of the project
cd "$(dirname "$0")/.."

# Load environment variables to resolve DEFAULT_SECURITY_DIR
set +u
if [ -f .env ]; then
  # shellcheck disable=SC1091
  source .env
fi
set -u

DEFAULT_SECURITY_DIR="${DEFAULT_SECURITY_DIR:-./volumes/security}"
AGENT_DIR="${DEFAULT_SECURITY_DIR}/vault/agent"

echo "[INFO] Commencing Vault Agent AppRole bootstrap..."

echo "[INFO] Checking if Vault is running and unsealed..."
# Vault status command returns 2 if sealed
if ! docker exec vault vault status >/dev/null 2>&1; then
  # Check if it was exit code 2 (sealed) or actually unreachable
  if docker exec vault vault status | grep -q 'Sealed\s*true'; then
    echo "[ERROR] Vault is sealed. Please unseal it first before running this script."
    exit 1
  else
    echo "[ERROR] Vault container is unreachable or not running."
    exit 1
  fi
fi

echo "[INFO] Vault is unsealed. Configuring vault-agent policy..."
docker exec -i vault vault policy write vault-agent-policy - <<EOF
path "secret/data/hy-home/*" {
  capabilities = ["read", "list"]
}
EOF

echo "[INFO] Enabling AppRole authentication method..."
docker exec vault vault auth enable approle || echo "[INFO] AppRole is already enabled."

echo "[INFO] Configuring vault-agent role..."
docker exec vault vault write auth/approle/role/vault-agent \
  secret_id_ttl=0 \
  token_num_uses=0 \
  token_ttl=0 \
  token_max_ttl=0 \
  secret_id_num_uses=0 \
  token_policies="vault-agent-policy"

echo "[INFO] Retrieving role_id and generating fresh secret_id..."
ROLE_ID=$(docker exec vault vault read -field=role_id auth/approle/role/vault-agent/role-id)
SECRET_ID=$(docker exec vault vault write -f -field=secret_id auth/approle/role/vault-agent/secret-id)

if [ -z "$ROLE_ID" ] || [ -z "$SECRET_ID" ]; then
  echo "[ERROR] Failed to retrieve role_id or secret_id from Vault."
  exit 1
fi

OUT_DIR="${DEFAULT_SECURITY_DIR}/vault/out"

echo "[INFO] Injecting credentials via helper container to bypass localized permission constraints..."
# Using a temporary alpine container mounted directly to the host directories solves permission errors
# caused by restricted container environments or root-owned host directories.
docker run --rm -i -v "${AGENT_DIR}:/agent" -v "${OUT_DIR}:/out" alpine sh -c "echo '${ROLE_ID}' > /agent/role_id && echo '${SECRET_ID}' > /agent/secret_id && chmod 644 /agent/role_id /agent/secret_id && chown -R 100:1000 /agent /out 2>/dev/null || true"

echo "[INFO] Credentials successfully exported to Vault Agent."

echo "[INFO] Restarting vault-agent to pick up the new credentials..."
docker restart vault-agent >/dev/null

echo "[SUCCESS] Vault Agent AppRole bootstrap is complete. Agent should now authenticate automatically."
