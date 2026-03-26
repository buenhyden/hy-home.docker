<!-- [ID:09-tooling:syncthing] -->
# Runbook: Syncthing Service Recovery (P2)

> Procedures for recovering from Syncthing synchronization failures and connectivity issues.

## Symptoms

- Folder status shows "Out of Sync" or "Error".
- Devices appear as "Disconnected" or "Never Seen".
- GUI inaccessible via `https://syncthing.${DEFAULT_URL}`.
- High CPU usage on small nodes during disk scanning.

## Diagnostic Steps

### 1. Check Service Status

```bash
cd ${DEFAULT_TOOLING_DIR}/syncthing
docker compose ps
docker compose logs --tail=100 -f syncthing
```

### 2. Verify Port Connectivity

Syncthing requires port `22000` (TCP/UDP) for data transfer. Use `nc` or `telnet` to verify.

```bash
# From another node
nc -zv <syncthing-node-ip> 22000
```

## Recovery Procedures

### 1. Resolving "Out of Sync" Items

If specific files fail to sync:

1. Click on the **Failed Items** link in the GUI to see error details (often permission issues).
2. Fix permissions on the host filesystem if necessary.
3. Click **Actions** -> **Rescan All**.

### 2. Repairing Corrupted Database

If the internal database is corrupted, try resetting the deltas before a full reset.

```bash
# Stop the service
docker compose stop syncthing

# Start with delta reset (Requires editing compose or temporary exec)
# Alternative: Manual removal of the index directory
sudo rm -rf ${DEFAULT_TOOLING_DIR}/syncthing/index-v0.14.0.db

# Restart service
docker compose start syncthing
```

> [!WARNING]
> Deleting the index directory will trigger a full re-scan of all synchronized folders. This may be CPU-intensive.

### 3. Resetting GUI Password

If the admin password is lost:

1. Locate the `config.xml` in `${DEFAULT_TOOLING_DIR}/syncthing`.
2. Edit the file and remove the `<user>` and `<password>` values within the `<gui>` tag.
3. Restart Syncthing; it will start without a password, and you can set a new one in the GUI.

## Escalation Policy

- **P1**: Critical sync failure for production resource data -> Notify SRE Team.
- **P2**: Intermittent connectivity or "Out of Sync" for non-critical data -> Follow manual re-scan procedures.

## Related References

- **Infrastructure**: [Syncthing Service](../../../infra/09-tooling/syncthing/README.md)
- **Guide**: [Syncthing System Guide](../../07.guides/09-tooling/syncthing.md)
- **Operation**: [Syncthing Operations Policy](../../08.operations/09-tooling/syncthing.md)
