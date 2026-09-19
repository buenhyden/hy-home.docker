---
title: "SeaweedFS Stack Health Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0024"
parent_ids:
- "GDE-0024"
created: "2026-05-17"
---

# SeaweedFS Stack Health and Recovery Runbook

## When to Use

Use for approved static diagnosis, backup planning or isolated recovery of this
exact subject. Live writes, restore, cutover, cleanup and credential changes need
a separately approved task.

## Procedure

From the repository root:

```bash
docker compose --env-file .env.example --profile seaweedfs config --quiet
docker compose --env-file .env.example --profile seaweedfs config --services
```

Confirm master, volume, filer and S3 services, the two distinct persistent
volumes, `infra_net`, health checks and standard gateway chain. Render
`seaweedfs-mount` separately and verify `SYS_ADMIN` and `/dev/fuse` are present
only when that privileged path is approved.

## Planned coordinated backup

1. Record image source/version, topology, volume IDs, filer stores, clients and
   object/file counts. Select a separate encrypted destination.
2. Fence all S3, filer and mount writers. Confirm the accepted recovery point.
3. Use the official `weed backup` workflow for volume data and verify its output.
   Export filer metadata with `fs.meta.save` for the same point.
4. Stop/quiesce the master before snapshotting `seaweedfs-master-data` for local
   rollback evidence; record topology/volume assignment and mark that snapshot as
   non-portable because upstream does not specify a master-state restore. Capture
   `seaweedfs-volume-data` only as supporting evidence, not as a substitute for
   engine-aware volume backup.
5. Record every artifact, engine version, time, size and checksum in one manifest.
   The official guide itself describes limitations, so mark backup status
   unverified until restore succeeds.

## Planned isolated restore

1. Provision an empty isolated target at the same SeaweedFS version with fresh
   master identity. Do not expose its S3 route or mount it on the HOME host.
2. Recreate the recorded topology, place the engine-aware volume backups on their
   intended volume servers, then load filer metadata with `fs.meta.load`. Do not
   import the source master volume unless version-specific upstream evidence first
   proves that path. Never combine artifacts from different captures.
3. Run `volume.fsck` or the current upstream consistency check, inspect master
   volume assignments, traverse filer paths and compare object/file counts.
4. Test disposable filer and S3 read/write/delete operations. Test FUSE only in an
   approved isolated environment with the same mount semantics.
5. Record recovery point and elapsed time. A separately approved cutover performs
   a final fenced capture, switches named clients and preserves rollback.

## Evidence

Record source revision/version, scope, timestamps, manifest/checksum summary,
commands and exit status, validation result, observed recovery point/time and all
unverified gaps. Exclude secrets, raw payloads and private resolved paths.

## Rollback or Recovery

A failed cutover returns clients to the preserved original cluster after validating
its write boundary; coordinated artifacts and the isolated target remain retained. Cutover occurs only after owner approval,
final consistency capture, application validation and a retained rollback window.

## Escalation

Stop for missing filer metadata, topology mismatch, orphaned volumes, checksum
failure, security exposure or version incompatibility. Do not improvise a raw
volume-only restore.

## Traceability

- Runtime source: [SeaweedFS Compose](../../../../../infra/04-data/lake-and-object/seaweedfs/docker-compose.yml).
- Artifact: `RUN-0024`; parent guide: `GDE-0024`.
- Procedures are planned unless a dated verification record explicitly says they ran.

## References

- [SeaweedFS data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup)
- [Policy](policy.md)


## Related Documents

- [Domain catalog](../README.md)
