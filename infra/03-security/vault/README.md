# Vault Secret Management

<!-- [ID:03-security:vault] -->
: Identity-based secrets management and encryption-as-a-service.

---

## Overview

HashiCorp Vault is the central secrets engine for the `hy-home.docker` platform. It provides a secure, audited environment for storing sensitive data and performing cryptographic operations.

### Service Details

| Service | Image | Profile | Primary Role |
| :--- | :--- | :--- | :--- |
| **vault** | `hashicorp/vault:1.21.4` | `core` | Server (Secret Engine) |
| **vault-agent** | `hashicorp/vault:1.21.4` | `core` | Sidecar (Secret Provider) |

---

## Features

- **Store Secrets**: Centralized key-value storage for infrastructure and application passwords.
- **Raft Integrated Storage**: Native storage engine with high availability and replication.
- **Transit Encryption**: Unified API for data encryption and decryption.
- **Lease & Audit**: Time-limited access with comprehensive audit logs.

## Networking

Exposed via Traefik at `vault.${DEFAULT_URL}`.

- **Internal Port**: `8200` (API/Web)
- **Cluster Port**: `8201` (Raft Internal)
- **Host Port**: `8200` (Direct CLI access)

## Persistence

Mounted from `${DEFAULT_SECURITY_DIR}/vault/`:

| Path | Mode | Purpose |
| :--- | :--- | :--- |
| `/vault/data` | `rw` | Raft state, secrets, and encrypted storage. |
| `/vault/config` | `ro` | HCL configuration (`vault.hcl`, `vault-agent.hcl`). |

---

## Operations

### Startup & Unseal Workflow

> [!IMPORTANT]
> **Vault seals itself on restart.** It must be manually unsealed before dependent services can read secrets.

```bash
# Verify status
docker exec -it vault vault status

# Unseal (requires 3 of 5 keys)
docker exec -it vault vault operator unseal <KEY_1>
docker exec -it vault vault operator unseal <KEY_2>
docker exec -it vault vault operator unseal <KEY_3>
```

### Health Verification

```bash
# Check readiness
docker exec vault wget -q -O- "http://127.0.0.1:8200/v1/sys/health"
```

## Related Documents

- **[Setup Guide](../../../docs/07.guides/03-security/01.setup.md)**
- **[Operations Policy](../../../docs/08.operations/03-security/README.md)**
- **[Security Runbook](../../../docs/09.runbooks/03-security/README.md)**
