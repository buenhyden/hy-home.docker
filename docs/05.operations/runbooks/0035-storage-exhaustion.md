---
title: "04-Data Storage Exhaustion Runbook"
version: "1.0.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-25"
layer: "operations"
artifact_id: "RUN-0035"
parent_ids: []
created: "2026-06-04"
---

# Storage Exhaustion Runbook

## When to Use

Use for approved static diagnosis, backup planning or isolated recovery of this
exact subject. Live writes, restore, cutover, cleanup and credential changes need
a separately approved task.

### Scope and safety

This runbook triages low-space conditions without deleting data. It does not
authorize `docker system prune`, volume removal, database compaction, retention
reduction, log truncation or cleanup of an unknown path. Recovery and deletion
require the affected owner, a verified backup and a separately approved action.

## Procedure

1. Identify the alerting filesystem, mount and affected service. Resolve the exact
   bind-backed volume from root-rendered Compose without publishing private path
   values. Never fall back to scanning or modifying a generic Docker volume root.
2. Record read-only filesystem capacity/inode evidence for the identified mount.
   Attribute growth to an owner: database, object store, queue, model/cache,
   observability retention or container runtime.
3. Check service health and write errors through an approved runtime observation.
   Stop additional writers if the service owner declares corruption risk.
4. Locate the service's backup/recovery policy and confirm the latest artifact,
   destination, checksum and isolated restore status. A volume copy on the same
   full filesystem is not protection.
5. Choose a reviewed remediation: expand the filesystem, move data through an
   engine-supported migration, enforce an already approved retention policy, or
   remove only proven rebuildable artifacts. Estimate reclaimed bytes and rollback.

## Evidence

Record source revision/version, scope, timestamps, manifest/checksum summary,
commands and exit status, validation result, observed recovery point/time and all
unverified gaps. Exclude secrets, raw payloads and private resolved paths.

## Rollback or Recovery

Rollback returns clients to expanded capacity or the prior unchanged state after an approved rollback. Cutover occurs only after owner approval,
final consistency capture, application validation and a retained rollback window.

## Escalation

- Management PostgreSQL/Valkey: [RUN-0028](0028-management-database.md)
- Valkey Cluster: [RUN-0022](0022-valkey-cluster.md)
- SeaweedFS: [RUN-0024](0024-seaweedfs.md)
- All HOME state owners and exceptions: [POL-0021](../policies/0021-backup-and-restore.md)

Do not delete PostgreSQL WAL/data, Valkey AOF/RDB, SeaweedFS volume
files, Kafka logs, SQLite WAL/journal files, OpenBao Raft data, Qdrant snapshots or
observability WALs through filesystem commands.

## Verification Record

### Validation and closeout

After an approved remediation, prove filesystem headroom, service health,
application reads/writes and backup continuity. Record capacity before/after,
what was changed, the approval, rollback status and any revised alert threshold.
Do not close on free-space evidence alone if data integrity remains unverified.

## Traceability

- Artifact: `RUN-0035`; parent guide: `GDE-0035`.
- Procedures are planned unless a dated verification record explicitly says they ran.

## Related Documents

- [Data backup policy](../policies/0021-backup-and-restore.md)
- [Data hardening policy](../policies/0030-data-optimization-hardening.md)
