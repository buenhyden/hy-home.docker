---
layer: infra
---
# Vault lifecycle guide (03-security)

Recurring operational tasks, backup/restore, rotation, and upgrade procedures for Vault.

## Backup and recovery

### Raft snapshot (recommended)

Vault's integrated Raft backend supports online snapshots. No downtime required.

```bash
export VAULT_TOKEN=<ROOT_OR_SNAPSHOT_TOKEN>
export VAULT_ADDR=http://localhost:${VAULT_HOST_PORT:-8200}

# Take a snapshot
vault operator raft snapshot save /tmp/vault-snap-$(date +%Y%m%d).snap

# Copy off-container
docker cp vault:/tmp/vault-snap-$(date +%Y%m%d).snap ./backups/
```

Schedule this daily. Keep at least 7 snapshots.

### Restore from snapshot

```bash
# Vault must be running and unsealed
vault operator raft snapshot restore /path/to/vault-snap.snap

# Vault will restart and re-seal — unseal again
docker exec -it vault vault operator unseal <KEY_1>
docker exec -it vault vault operator unseal <KEY_2>
docker exec -it vault vault operator unseal <KEY_3>
```

### Volume backup (cold)

For a full cold backup, stop the service, copy the host directory, then restart:

```bash
docker compose --profile core stop vault
cp -r ${DEFAULT_SECURITY_DIR}/vault ./backups/vault-cold-$(date +%Y%m%d)
docker compose --profile core start vault
# Then unseal
```

## Seal and unseal

| Event | Action needed |
| :--- | :--- |
| Container restart | Unseal (3 of 5 keys) |
| Host reboot | Unseal after `docker compose up` |
| Manual seal (security incident) | `vault operator seal`, then unseal to resume |
| Auto-unseal (future) | Configure a Transit or cloud-based unseal mechanism |

To seal manually:

```bash
vault operator seal
```

## Token and key rotation

### Root token

The root token should not stay in use after initialization. Generate a temporary one when you need elevated access:

```bash
# Generate a one-time root token
vault operator generate-root -init
# Follow the prompts — provide 3 unseal keys

# Revoke it when done
vault token revoke <TEMP_ROOT_TOKEN>
```

### Unseal key re-key

If any unseal key is compromised, generate a new key set:

```bash
vault operator rekey \
  -init \
  -key-shares=5 \
  -key-threshold=3

# Provide the current unseal keys at the prompt
# Save the new key shares
```

### AppRole Secret ID rotation

Secret IDs have a TTL and expire automatically. For manual rotation:

```bash
# Revoke an existing Secret ID
vault write auth/approle/role/myapp/secret-id/destroy secret_id=<OLD_ID>

# Generate a new one
vault write -f auth/approle/role/myapp/secret-id
```

## Vault version upgrade

1. **Snapshot**: Take a Raft snapshot before upgrading.
2. **Pull new image**: Update the image tag in `docker-compose.yml`.
3. **Check release notes**: Raft storage upgrades are usually automatic, but verify in the [Vault upgrade guide](https://developer.hashicorp.com/vault/docs/upgrading).
4. **Restart**:

```bash
docker compose --profile core pull vault
docker compose --profile core up -d vault
# Then unseal
```

5. Confirm the new version with `vault status`.

## Audit log setup

Enable the file audit device to record all API requests:

```bash
vault audit enable file file_path=/vault/logs/audit.log
```

Add a volume for `/vault/logs` if you want logs to persist outside the container. Without a persistent mount, logs are lost on container restart.

## Scaling considerations

The current setup uses a single-node Raft cluster. For a high-availability deployment:

- Add two additional Vault nodes on separate hosts.
- Configure each with a unique `node_id` in `vault.hcl` and peer cluster addresses.
- Use `vault operator raft join` to form the cluster.

This is out of scope for a single-host home-lab and is documented in the [HashiCorp Vault HA documentation](https://developer.hashicorp.com/vault/docs/concepts/ha).
