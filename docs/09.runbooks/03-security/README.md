# Security Tier Runbook (03-security)

<!-- [ID:docs:09:03-security:README] -->
: Maintenance and emergency recovery procedures for HashiCorp Vault.

---

## Troubleshooting Procedures

### 1. Vault Lockout (MFA/Unseal Loss)
If quorum for unsealing is lost or the root token is missing:
1. **Quorum Check**: Verify how many keys are available. 3 of 5 are required.
2. **Key Rotation**: If a key is lost but quorum exists, initiate a **Rekey** operation immediately after unsealing.
3. **Storage Access**: If all keys are lost, the data in `${DEFAULT_SECURITY_DIR}/vault/data` is cryptographically inaccessible. You must restore from the latest snapshot.

### 2. Raft Cluster Drift
Symptoms: Vault logs `Raft quorum lost` or `Election timeout`.
1. Check resource usage on the host: `docker stats vault`.
2. Review HCL configuration for cluster address mismatches (`vault.hcl`).
3. If a single node is corrupted, remove it from the configuration and re-join it to the cluster.

### 3. Vault Agent Sync Failure
Symptoms: Dependent services log `Vault: Permission Denied` or fail to read configuration templates.
1. Check Vault Agent logs: `docker logs vault-agent`.
2. Verify the `vault-agent.hcl` configuration for correct authentication paths.
3. Ensure the Vault Agent token has not expired and the AppRole is correctly configured in Vault.

## Routine Maintenance

### Snapshot & Backup
Weekly snapshots must be verified for integrity.
```bash
# Create snapshot
docker exec vault vault operator raft snapshot save /vault/data/backup-$(date +%F).snap

# Verify file existence
ls -lh ${DEFAULT_SECURITY_DIR}/vault/data/backup-*.snap
```

### Unseal Verification
Ensure the `unseal` process is tested after every scheduled host maintenance.
1. Restart the container: `docker compose restart vault`.
2. Manually unseal using keys.
3. Confirm unsealed status: `docker exec vault vault status`.

---

## Technical Support

- **Primary Contact**: Security Support Team
- **Emergency Channel**: #incident-response
- **Vault CLI Reference**: `vault -h` or `vault <command> -h`
