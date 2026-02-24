# Runbook: HashiCorp Vault Unseal & Recovery

> **Component**: `vault`
> **Storage**: Filesystem (Encrypted)
> **Endpoint**: `/v1/sys/health`

## 1. Issue: Vault is Sealed (HTTP 503)

**Given**: Vault returns 503 "Vault is sealed" or UI shows unseal prompt.
**When**: Container restarts or storage backend fluctuates.
**Then**: Provide the unseal quorum (default 3 of 5):

```bash
# Execute for each of the 3 keys
docker exec -it vault vault operator unseal [Key_1]
docker exec -it vault vault operator unseal [Key_2]
docker exec -it vault vault operator unseal [Key_3]
```

## 2. Verification Check

**Given**: Unseal steps are performed.
**When**: Checking status.
**Then**: `vault status` must show `Sealed: false`.

```bash
docker exec -it vault vault status
```

## 3. Emergency: Total Key Loss

**Given**: All unseal keys are permanently lost.
**When**: Data is irretrievable.
**Then**: Reset the security tier (WARNING: DATA LOSS).

1. **Purge Volume**:

   ```bash
   docker compose -f infra/03-security/vault/docker-compose.yml down
   docker volume rm infra_vault-data
   ```

2. **Re-init**: Restart and run `vault operator init` to generate new keys.
