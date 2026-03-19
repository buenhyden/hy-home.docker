# Security (03-security)

This tier manages secret storage and encryption-as-a-service for the entire platform. All other tiers that need passwords, API keys, or tokens should source them from Vault rather than environment variables.

## Services

| Service | Profile | Path | Purpose |
| :--- | :--- | :--- | :--- |
| `vault` | `core` | `./vault` | Central secret management and Raft-backed storage |

## Startup dependency

> **Vault must be manually unsealed after every restart** before dependent services can read secrets. See [vault-procedural.md](../../docs/guides/03-security/vault-procedural.md) for the bootstrap and unseal workflow.

Initialization is a one-time operation per environment. It produces 5 unseal keys and a root token — store these in a separate secrets manager or offline storage.

## Dependencies

| Dependency | Purpose |
| :--- | :--- |
| `traefik` (01-gateway) | SSL termination and routing to `vault.${DEFAULT_URL}` |
| Host filesystem | Raft data stored at `${DEFAULT_SECURITY_DIR}/vault` |

## File map

| Path | Description |
| :--- | :--- |
| `vault/` | Vault service, HCL config, and service README |
| `README.md` | This document — tier overview |

## Guides

| Guide | Purpose |
| :--- | :--- |
| [vault-context.md](../../docs/guides/03-security/vault-context.md) | Architecture, data flow, what depends on Vault |
| [vault-cluster-guide.md](../../docs/guides/03-security/vault-cluster-guide.md) | Security posture, policies, AppRole |
| [vault-procedural.md](../../docs/guides/03-security/vault-procedural.md) | Step-by-step bootstrap and configuration |
| [vault-lifecycle.md](../../docs/guides/03-security/vault-lifecycle.md) | Backup, restore, rotation, upgrade |
