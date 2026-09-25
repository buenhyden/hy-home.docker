---
title: "Valkey Cluster Health Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0022"
parent_ids:
- "GDE-0022"
created: "2026-05-17"
---

# Valkey Cluster Health and Recovery Runbook

## When to Use

Use for approved static diagnosis, backup planning or isolated recovery of this
exact subject. Live writes, restore, cutover, cleanup and credential changes need
a separately approved task.

### Scope

Static validation is safe to perform in this documentation task. Starting the
cluster, writing data, taking a live backup, restoring or changing membership is
planned operator work and was not executed.

## Procedure

From the repository root:

```bash
docker compose --env-file .env.example --profile valkey-cluster config --quiet
docker compose --env-file .env.example --profile valkey-cluster config --services
```

Confirm six node services, the init job and exporter; six distinct data volumes;
`lab_net`; the password secret; node health checks; and the 6379–6384 client and
16379–16384 bus mappings. Stop if rendered paths are empty or unexpected.

### Planned backup procedure

1. Open an approved maintenance window and identify the application writers.
2. Record engine/image source, cluster node IDs, slot ownership, primary/replica
   relationships and persistence mode. Pause writes or establish an explicitly
   accepted consistency point.
3. On each primary, request and verify an RDB checkpoint. Copy the complete RDB
   and, when enabled, every AOF base/increment file plus its manifest as one set.
   Do not copy an AOF while it is being rewritten.
4. Include configuration and a diagnostic copy of cluster metadata, but mark
   `nodes.conf` as source identity rather than a file to reuse.
5. Write a manifest of node role, timestamp, file size and checksum. Transfer the
   sets to a separate encrypted destination under restricted custody.

### Planned isolated restore

1. Provision an empty, network-isolated six-node target at a persistence-compatible
   Valkey version with disposable credentials. Do not connect application clients.
2. Recreate the intended three-primary/three-replica topology with fresh cluster
   identity. Map each primary backup to the documented slot owner; never merge
   unrelated node sets.
3. With target nodes stopped, place each complete persistence set in its empty
   data directory with correct ownership. Do not reuse live `nodes.conf`.
4. Start only the isolated target. Confirm AOF loading completes without truncation
   or repair, `cluster_state` is healthy, all slots are covered, and replicas are
   attached to the intended primaries.
5. Compare per-slot/key counts and selected values with the manifest, then run a
   disposable cluster-aware client read/write/delete test.
6. Record observed recovery point and elapsed time. A separate approved cutover
   must pause writers, take a final backup, switch clients, validate, and retain
   the previous state for rollback.

## Evidence

Record source revision/version, scope, timestamps, manifest/checksum summary,
commands and exit status, validation result, observed recovery point/time and all
unverified gaps. Exclude secrets, raw payloads and private resolved paths.

## Rollback or Recovery

A failed cutover returns clients to the preserved original cluster after validating
its identity and write boundary; backup sets and the isolated target remain retained. Cutover occurs only after owner approval,
final consistency capture, application validation and a retained rollback window.

## Escalation

Stop for missing AOF segments, checksum mismatch, unexpected identity, uncovered
slots, replica drift or any prompt to repair/truncate persistence. Preserve logs
without secret values and escalate to the data owner.

## Traceability

- Runtime source: [Valkey Cluster Compose](../../../infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml).
- Artifact: `RUN-0022`; parent guide: `GDE-0022`.
- Procedures are planned unless a dated verification record explicitly says they ran.

### References

- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Valkey Cluster tutorial](https://valkey.io/topics/cluster-tutorial/)
- [Policy](../policies/0022-valkey-cluster.md)

## Related Documents

- [Domain catalog](../README.md)
