# Security Tier (03-security)

<!-- [ID:03-security:root] -->
: Centralized secret management, encryption-as-a-service, and identity-based access.

---

## Navigation Map

### Infrastructure
- **[Vault](./vault/README.md)**: Central secret storage and Raft-backed persistence.
- **[Vault Agent](./vault/README.md)**: Sidecar for secret injection and auto-auth.

### Documentation (Golden 5)
- **[Guides](../../docs/07.guides/03-security/README.md)**: Setup, bootstrapping, and unseal workflows.
- **[Context](../../docs/07.guides/03-security/README.md)**: Architecture, data flow, and threat model.
- **[Operations](../../docs/08.operations/03-security/README.md)**: Seal/unseal protocols and security governance.
- **[Runbooks](../../docs/09.runbooks/03-security/README.md)**: Emergency recovery and lost key procedures.

---

## Tier Overview

The `03-security` tier is the platform's root of trust. It provides HashiCorp Vault as the primary secrets engine, ensuring that sensitive data like passwords, API keys, and certificates are never stored in plain text or exposed in version control.

### Service Matrix

| Service | Role | Data Store | Profile |
| :--- | :--- | :--- | :--- |
| **Vault** | Server (Root of Trust) | Raft | `core` |
| **Vault Agent** | Sidecar / Consumer | Local File / Memory | `core` |

## Core Principles

1.  **Encryption at Rest**: All secrets stored in Vault are encrypted using AES-256-GCM.
2.  **Identity-Based Access**: Access to secrets is governed by Vault policies linked to AppRoles or User IDs.
3.  **Manual Unseal**: To ensure security, Vault must be manually unsealed by authorized operators after every restart.
4.  **No Plaintext Secrets**: Infrastructure components must fetch secrets JIT (Just-In-Time) from Vault.

---

## Support & Governance

- **Maintainer**: Security Operations
- **SLA**: 99.9% availability for the unsealed state.
- **Audit**: All requests to Vault are logged and audited for compliance.
