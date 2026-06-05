# Security Tier (03-security)

> Centralized secret management, encryption-as-a-service, and identity-based access.

## Overview

The `03-security` tier serves as the platform's root of trust. It provides HashiCorp Vault for secure secret storage, ensuring that sensitive data like passwords, API keys, and certificates are encrypted at rest and never exposed in version control. This tier manages the lifecycle of secrets and provides identity-based access control for all platform components.

## Audience

이 README의 주요 독자:

- Security Officers (Governance & Audit)
- Infrastructure Engineers (Vault Operations)
- Application Developers (Secret Injection)
- AI Agents (Automated secret rotation)

## Scope

### In Scope

- HashiCorp Vault Server (Raft Storage)
- Vault Agent (Secret injection sidecar)
- Unseal protocols and key management policies
- Identity-based access policies (AppRole, Userpass)

### Out of Scope

- Identity Provider (handled by `02-auth` Keycloak)
- Certificate Authority (handled by `01-gateway` via Let's Encrypt/ACME)
- Physical hardware security (TSM/HSM)

## Structure

```text
03-security/
├── vault/              # Vault server and agent configuration
└── README.md           # This file
```

## How to Work in This Area

1. Read the [Vault Operations Guide](../../docs/05.operations/guides/03-security/vault.md) for initialization and AppRole bootstrap boundaries.
2. Follow the [Operations Policy](../../docs/05.operations/policies/03-security/README.md) for unseal protocols.
3. Use the [Security Runbook](../../docs/05.operations/runbooks/03-security/README.md) for emergency recovery.
4. Vault must be manually unsealed after each restart.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Secret Mgmt | HashiCorp Vault               | `hashicorp/vault:2.0.1`   |
| Storage    | Raft (Integrated)              | Single-node current state; HA expansion planned |
| Injection  | Vault Agent                    | Sidecar pattern           |
| OS         | Alpine Linux (Container)       | Minimal surface area      |

## Configuration

### Environment Variables

| Variable | Required | Description |
| --------- | -------: | ----------- |
| `VAULT_ADDR` | Yes | Local API address for CLI |
| `DEFAULT_URL` | Yes | Root domain for Vault UI (`vault.${DEFAULT_URL}`) |
| `VAULT_PORT` | No | Listener port (default: 8200) |

## Testing

```bash
# Validate the root security profile and 03-security hardening contract
HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 03-security

# Runtime-only checks after the security profile is already running
docker compose --profile security exec vault vault status
docker compose --profile security exec vault wget -q -O- "http://127.0.0.1:8200/v1/sys/health"
```

## Change Impact

- Re-sealing Vault will break all secret fetching for dependent services.
- Policy changes may revoke access for critical infrastructure components.
- Raft configuration changes require 쿼럼 validation before applying.

## Related Documents

- [02-auth](../02-auth/README.md) - Integrating Vault with OIDC.
- [01-gateway](../01-gateway/README.md) - Vault UI ingress routing.
- [docs/05.operations/03-security](../../docs/05.operations/guides/03-security/README.md) - Governance standards.

## AI Agent Guidance

1. Never log unseal keys or the root token in plaintext.
2. Use `vault-agent` for secret injection instead of direct API calls where possible.
3. Ensure all new policies follow the `hy-home-{service}-policy` naming schema.
4. Verify the `sealed` state before attempting to read any secrets.
