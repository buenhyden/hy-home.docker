---
layer: infra
---
# Vault procedural guide (03-security)

Step-by-step procedures for initializing, configuring, and operating Vault in this environment.

## First-time initialization

Vault starts uninitialized. Run this once per environment — never again unless Raft storage is wiped.

```bash
# 1. Start the service (from the project root)
docker compose -f infra/03-security/vault/docker-compose.yml --profile core up -d

# 2. Initialize with 5 key shares, threshold of 3
docker exec -it vault vault operator init -key-shares=5 -key-threshold=3

# 3. Save the 5 unseal keys and Initial Root Token somewhere safe.
#    These cannot be recovered if lost.
```

## Unseal after restart

Vault automatically seals after any restart. Run before any service that reads from Vault:

```bash
docker exec -it vault vault operator unseal <UNSEAL_KEY_1>
docker exec -it vault vault operator unseal <UNSEAL_KEY_2>
docker exec -it vault vault operator unseal <UNSEAL_KEY_3>

# Verify
docker exec -it vault vault status
# Sealed: false  →  ready
```

## Enable the KV v2 secret engine

```bash
# Set these before running any vault CLI commands
export VAULT_ADDR=http://localhost:${VAULT_HOST_PORT:-8200}
export VAULT_TOKEN=<ROOT_TOKEN>

# Enable KV v2 at the path "secret/"
vault secrets enable -path=secret kv-v2

# Write a test secret
vault kv put secret/test/app password="hunter2"

# Read it back
vault kv get secret/test/app
```

## Define an access policy

Policies limit what a token or AppRole can read. Create one per application or service group.

```bash
# Ensure VAULT_ADDR and VAULT_TOKEN are exported (see "Enable KV v2" above)

# Write a policy that allows reading secrets under secret/myapp/
vault policy write myapp-policy - <<EOF
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}
EOF

# Verify
vault policy list
vault policy read myapp-policy
```

## Configure AppRole authentication

AppRole is the recommended way for services on `infra_net` to authenticate with Vault.

```bash
# Enable the AppRole auth method
vault auth enable approle

# Create a role for your service
vault write auth/approle/role/myapp \
  secret_id_ttl=10m \
  token_num_uses=10 \
  token_ttl=20m \
  token_max_ttl=30m \
  policies="myapp-policy"

# Retrieve the Role ID (static, embed in container config)
vault read auth/approle/role/myapp/role-id

# Generate a Secret ID (dynamic, rotate periodically)
vault write -f auth/approle/role/myapp/secret-id
```

A service authenticates using both values:

```bash
vault write auth/approle/login \
  role_id="<ROLE_ID>" \
  secret_id="<SECRET_ID>"
# Returns a client_token valid for token_ttl
```

## Log analysis

```bash
# Container log (startup, listener, errors)
docker logs vault

# Audit log (if enabled — see vault-cluster-guide.md)
docker exec -it vault cat /vault/logs/audit.log | jq .

# Common errors to look for:
# "core: vault is sealed"  → needs unseal
# "error authenticating"   → wrong token or expired secret-id
# "lease not found"        → token TTL expired, re-authenticate
```
