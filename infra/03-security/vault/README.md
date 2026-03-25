# Vault Secret Management

> Identity-based secrets management and encryption-as-a-service.

## Overview

HashiCorp Vault is the central secrets engine for the `hy-home.docker` platform. It provides a secure, audited environment for storing sensitive data and performing cryptographic operations. It utilizes the Raft integrated storage for high availability and consistency.

## Audience

이 README의 주요 독자:

- SRE (Scaling & Maintenance)
- Security Engineers (Policy & Audit)
- AI Agents (Automated unsealing & monitoring)

## Scope

### In Scope

- Vault Server configuration (`vault.hcl`)
- Vault Agent configuration (`vault-agent.hcl`)
- Raft storage management and snapshots
- Health protocols and monitoring integration

### Out of Scope

- Application-level business logic
- Secret content generation (only management is in scope)
- Network firewalling between services

## Structure

```text
vault/
├── config/             # Vault & Agent configuration files
├── docker-compose.yml  # Vault & Agent orchestration
└── README.md           # This file
```

## How to Work in This Area

1. Consult the [Vault Setup Guide](../../../docs/07.guides/03-security/01.setup.md) for bootstrapping.
2. Check `config/vault.hcl` for specific storage and listener settings.
3. Use the [Security Runbook](../../../docs/09.runbooks/03-security/README.md) for Raft recovery.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Binary     | Vault (Go)                     | v1.21.4                   |
| Persistence| Raft                           | Integrated Storage        |
| Framework  | Alpine                         | Container Runtime         |

## Configuration

### Environment Variables

| Variable | Required | Description |
| --------- | -------: | ----------- |
| `VAULT_API_ADDR` | Yes | Internal API address for agents |
| `SKIP_SETCAP` | No | Disable Linux capability setting (default: true) |

## Testing

```bash
# Verify Raft cluster status
docker exec vault vault operator raft list-peers

# Test unseal state
docker exec vault vault status | grep "Sealed"
```

## Change Impact

- Modifying `vault.hcl` requires a container restart and subsequent manual unseal.
- Snapshot operations may briefly impact I/O performance.
- Changing listener addresses will break communication for Vault Agents.

## Related References

- [03-security](../README.md) - Parent tier overview.
- [01-gateway](../../01-gateway/README.md) - Ingress for Vault UI.
- [docs/09.runbooks/03-security](../../../docs/09.runbooks/03-security/README.md) - Operational runbooks.

## AI Agent Guidance

1. Always check the `sealed` status before performing any management tasks.
2. Automated scripts must handle the `429` (rate limited) response from Vault gracefully.
3. Follow the [Security Ops Policy](../../../docs/08.operations/03-security/README.md) for data retention.
