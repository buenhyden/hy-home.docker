# Registry Recovery Runbook

Runbook for recovering the local Docker registry in the `09-tooling` tier.

## Symptoms
- `Error: response from daemon: Get https://registry.hy-home.com/v2/: dial tcp ...`
- Container `registry` is in `restarting` state.

## Recovery Steps
1. Verify storage mounts: `df -h ${DEFAULT_DATA_DIR}/registry`
2. Restart service: `docker compose restart registry`
3. Verify logs: `docker compose logs -f registry`

## Related Documents
- [Operations](../../08.operations/09-tooling/registry.md)
