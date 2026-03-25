# Runbook: Storage Exhaustion (P0)

Emergency response for when data volumes reach 100% capacity.

## Symptoms

- Database services crashing with "No space left on device".
- Write operations failing across the stack.
- Monitoring alerts for `NodeDiskSpaceFilled`.

## Immediate Actions

### 1. Identify Bloat

```bash
# Check volume sizes
docker system df -v
# Find largest directories in data root
du -ah ${DEFAULT_DATA_DIR} | sort -rn | head -n 20
```

### 2. Emergency Cleanup

```bash
# Prune unused docker objects
docker system prune -a --volumes
# Clear logs
sudo journalctl --vacuum-time=1d
```

### 3. Service-Specific Truncation

- **PostgreSQL**: Vacuum full (requires temporary overhead).
- **Valkey**: Flush volatile keys if not persistent.
- **SeaweedFS**: Run garbage collection.

## Long-term Resolution

- Expand physical disk volume.
- Implement stricter retention policies.
