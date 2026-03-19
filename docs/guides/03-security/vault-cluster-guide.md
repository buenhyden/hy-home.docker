---
layer: infra
---
# HashiCorp Vault security guide (03-security)

Vault is the secrets management backend for the entire platform. This guide covers its security posture, network topology, policy model, and AppRole configuration.

> **Component**: `vault`
> **Tier**: `03-security`
> **Internal port**: `8200` (HTTP, plain — TLS terminated at Traefik)

## CLI environment

All `vault` CLI commands in this guide assume these environment variables are set:

```bash
export VAULT_ADDR=http://localhost:${VAULT_HOST_PORT:-8200}  # or http://vault:8200 from inside infra_net
export VAULT_TOKEN=<YOUR_TOKEN>
```

Set `VAULT_ADDR` to `http://vault:8200` when running commands from another container on `infra_net`, or to `http://localhost:${VAULT_HOST_PORT:-8200}` when running from the host.

## Role and security posture

Vault stores and controls access to tokens, passwords, API keys, and TLS certificates. Access is identity-based: callers authenticate with Vault, receive a short-lived token, and use that token to read secrets. No secret is visible in environment variables or Docker Compose files.

| Mechanism | Detail |
| :--- | :--- |
| Storage backend | Raft (integrated) — no external Consul required |
| Internal API | `http://vault:8200` on `infra_net` |
| External UI | `https://vault.${DEFAULT_URL}` via Traefik |
| TLS | Terminated at Traefik; internal traffic is plain HTTP |
| Memory protection | `IPC_LOCK` capability prevents swap of sensitive data |
| `disable_mlock` | Set to `true` — safe because `IPC_LOCK` is granted via `cap_add` |

## Bootstrapping and unsealing

Vault starts in an **uninitialized and sealed** state. Initialization is a one-time operation.

### Initialization

```bash
docker exec -it vault vault operator init -key-shares=5 -key-threshold=3
```

This produces 5 unseal keys and a root token. Store them offline — Vault cannot recover them if lost.

### Unsealing after restart

Vault seals itself on every container restart. Provide 3 of the 5 keys before dependent services start reading secrets:

```bash
vault operator unseal <UNSEAL_KEY_1>
vault operator unseal <UNSEAL_KEY_2>
vault operator unseal <UNSEAL_KEY_3>
```

Confirm with `vault status` — look for `Sealed: false`.

## Access policies

Policies define what secrets a token or AppRole can read. Write one policy per application:

```hcl
# Example: read-only access to myapp secrets
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}

# Example: allow full control of myapp secrets (for CI / admin)
path "secret/data/myapp/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
```

Apply with:

```bash
vault policy write myapp-policy /path/to/policy.hcl
```

## AppRole authentication

AppRole is the right auth method for services running inside Docker on `infra_net`.

```bash
# Enable AppRole
vault auth enable approle

# Create a role
vault write auth/approle/role/myapp \
  token_ttl=20m \
  token_max_ttl=30m \
  secret_id_ttl=10m \
  policies="myapp-policy"

# Get the static Role ID (embed in container config)
vault read auth/approle/role/myapp/role-id

# Generate a dynamic Secret ID (rotate periodically)
vault write -f auth/approle/role/myapp/secret-id
```

A service logs in using both values and receives a short-lived client token:

```bash
vault write auth/approle/login \
  role_id="<ROLE_ID>" \
  secret_id="<SECRET_ID>"
```

## Storage integration

Applications read secrets via the KV v2 engine mounted at `secret/`:

```bash
# Write
vault kv put secret/myapp/db password="s3cr3t"

# Read
vault kv get secret/myapp/db

# Read in JSON (for scripting)
vault kv get -format=json secret/myapp/db | jq '.data.data.password'
```

## Audit logging

Vault records every API request and response when audit is enabled. Add the file audit device after initialization:

```bash
vault audit enable file file_path=/vault/logs/audit.log
```

To persist logs across restarts, mount a host path or Docker volume to `/vault/logs` in `docker-compose.yml`. Without a persistent mount, audit logs are lost when the container stops.

Check that audit is enabled:

```bash
vault audit list
```
