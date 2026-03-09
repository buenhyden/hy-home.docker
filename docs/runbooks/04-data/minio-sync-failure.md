# Runbook: MinIO Sync and Read-Only Failures

> Recovery steps when MinIO drives max out or fail to synchronize, triggering Read-Only mode.

## Context

A standalone MinIO instance lacks distributed erasure coding across separate physical disks. Therefore, if the host OS disk reaches capacity, or standard kernel IO errors trigger, MinIO will forcefully safeguard blob corruption by placing the entire partition into a strict `Read-Only` mode. Applications that depend on it (like Tempo or Loki) will immediately begin dropping chunks and throwing `500` errors.

## Symptoms

- Attempting to publish objects to `minio.${DEFAULT_URL}` returns `507 Insufficient Storage` or `403 Forbidden`.
- MinIO console displays `Drive Read-Only Error`.
- Docker container logs (`docker logs minio`) span IO errors stating `Disk capacity reached`.

## Resolution Steps

### Method 1: Host Disk Pruning

If the failure stems strictly from storage capacities, deleting host side clutter resolves the lockout.

1. Jump securely onto the Linux Host and run metric diagnostics:

```bash
df -H
```

1. Navigate to `${DEFAULT_DATA_DIR}/minio/data` and eliminate stale environments, temporary files, or utilize `docker builder prune -a` to free raw system space.
2. Restart the MinIO service explicitly:

```bash
docker compose -f infra/04-data/minio/docker-compose.yml restart minio
```

1. Verify if read-only flags disappeared from the MinIO startup tail.

### Method 2: Handling Corrupt OS Mounts

If the filesystem is actually corrupted, you must execute a recovery block.

1. Determine if `xfs` or `ext4` tools report corruption utilizing standard linux block checks (`fsck`).
2. Remount the block into read/write format if the Linux kernel forcefully changed it.

```bash
# Verify mount states
mount | grep $(df -P ${DEFAULT_DATA_DIR} | tail -1 | awk '{print $1}')
```

1. Attempt to copy out the internal bucket structure from `${DEFAULT_DATA_DIR}/minio/data` to a secondary safe drive before completely rebuilding the container state if corruption has compromised block indices.
