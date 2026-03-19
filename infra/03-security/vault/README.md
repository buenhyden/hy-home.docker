# Vault

HashiCorp Vault is an identity-based secrets and encryption management system. It provides a unified backend for storing and accessing tokens, passwords, API keys, and TLS certificates.

## Services

| Service | Image | Profile | Template | Role |
| :--- | :--- | :--- | :--- | :--- |
| `vault` | `hashicorp/vault:1.21.2` | `core` | `template-stateful-med` | Central secret storage and transit encryption |

## Networking

- **Internal port**: `${VAULT_PORT:-8200}` (exposed on `infra_net`)
- **Host port**: `${VAULT_HOST_PORT:-8200}` (for direct CLI access)
- **External URL**: `https://vault.${DEFAULT_URL}` (via Traefik)

## Security

- `IPC_LOCK` capability added — prevents Vault process memory from swapping to disk.
- `no-new-privileges:true` enforced via `template-stateful-med`.
- `read_only: false` — Vault writes Raft data to `/vault/file` (intentional).
- TLS is terminated at Traefik; internal traffic over `infra_net` is plain HTTP on port 8200.

## Startup & Unseal

> **Vault seals itself after every restart.** Before any dependent service can read secrets, Vault must be unsealed.

First-time initialization (one-time per environment):

```bash
docker exec -it vault vault operator init
# Save the 5 unseal keys and root token in a secure location.
```

After each restart (requires 3 of 5 keys):

```bash
docker exec -it vault vault operator unseal <UNSEAL_KEY_1>
docker exec -it vault vault operator unseal <UNSEAL_KEY_2>
docker exec -it vault vault operator unseal <UNSEAL_KEY_3>
```

Check seal status:

```bash
docker exec -it vault vault status
```

## Persistence

| Volume / Mount | Container Path | Mode | Purpose |
| :--- | :--- | :--- | :--- |
| `vault-data` volume | `/vault/file` | `rw` | Raft integrated storage (state, secrets) |
| `./config` bind mount | `/vault/config` | `ro` | HCL configuration (`vault.hcl`) |

The `vault-data` volume maps to `${DEFAULT_SECURITY_DIR}/vault` on the host.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Service definition with Traefik labels and health check |
| `config/vault.hcl` | Vault server configuration (listener, storage, telemetry) |
| `README.md` | This document |

## Guide references

| Guide | Purpose |
| :--- | :--- |
| [vault-context.md](../../../docs/guides/03-security/vault-context.md) | Architecture, data flow, network boundaries |
| [vault-cluster-guide.md](../../../docs/guides/03-security/vault-cluster-guide.md) | Security posture, policies, AppRole setup |
| [vault-procedural.md](../../../docs/guides/03-security/vault-procedural.md) | Bootstrap, secret engine, policy creation |
| [vault-lifecycle.md](../../../docs/guides/03-security/vault-lifecycle.md) | Backup, restore, seal/unseal, upgrades |
