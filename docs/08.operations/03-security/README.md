# Operations Policy: Security Tier (03-security)

<!-- [ID:docs:08:03-security:README] -->
: Governance and operational standards for HashiCorp Vault.

---

## Security Governance

### 1. Seal/Unseal Management
- **Key Custodians**: 5 unseal keys must be held by different, authorized operators (if available).
- **Manual Control**: Auto-unseal is disabled in the `hy-home.docker` core tier to ensure a "human-in-the-loop" security model after every restart.
- **Root Token Policy**: The initial root token must be used only for bootstrapping and emergency recovery. It is NEVER used for daily operations.

### 2. Secret Lifecycle
- **Dynamic Secrets**: Prefer dynamic secrets (database credentials, AWS tokens) over static KV values where possible.
- **TTL (Time-To-Live)**: Maximum TTL for all tokens must be enforced. Default lease duration: 24h.
- **Audit Logging**: Audit logging to `file` or `syslog` must be enabled and reviewed periodically.

## Availability & Performance

- **SLO**: 99.9% availability for the API when unsealed.
- **Raft Health**: The Raft cluster quorum must be maintained.
- **Dependency Map**:
  - `vault` -> Host Filesystem (Raft)
  - All services -> `vault` (Secret Sourcing)

## Backup & Residency

- **Data Locality**: All Raft data resides in `${DEFAULT_SECURITY_DIR}/vault/data`.
- **Snapshots**: Weekly Raft snapshots are required for disaster recovery.
  ```bash
  vault operator raft snapshot save vault-backup.snap
  ```

---

## Review Cadence

| Item | Frequency | Responsibility |
| :--- | :--- | :--- |
| **Unseal Key Rotation** | Annually | Security Lead |
| **Audit Log Review** | Monthly | Security Ops |
| **Policy Audit** | Quarterly | Admin |
