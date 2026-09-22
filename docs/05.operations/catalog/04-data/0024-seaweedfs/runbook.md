---
title: "SeaweedFS Stack Health Runbook"
version: "1.3.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
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
HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest \
  tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests
```

The rehearsal renders the real services on disposable data. It checks that
anonymous and wrong-credential requests are refused, that filer and volume
HTTP need a JWT, that gRPC requires a client certificate, the consumer S3 API,
persistence across restart, a read failing while the volume server is down,
and backup and restore into empty stores.

### First activation (approved task)

1. `bash scripts/operations/gen-secrets.sh` creates STRG-008, STRG-009 and
   STRG-010; set `SEAWEEDFS_S3_ADMIN_ACCESS_KEY` in `.env`.
2. `bash infra/04-data/lake-and-object/seaweedfs/bin/gen-grpc-certs.sh` issues
   the gRPC certificates into `secrets/certs/seaweedfs` (kept unless
   `--rotate`).
3. Create `${DEFAULT_DATA_DIR}/seaweedfs/{master,volume,filer}` owned by UID
   1000 (the host operator), then
   `docker compose --profile seaweedfs up -d --wait`.
4. Verify with the admin identity: create and delete a disposable bucket, and
   confirm an anonymous request returns 403.

### Consumer cutover from MinIO (S07, approved task)

For one consumer at a time (Loki, then Tempo, then MLflow):

1. With MinIO and the consumer still running, copy what SeaweedFS lacks (no
   overwrite, no deletion):
   `docker compose --profile storage-migration run --rm -e BUCKETS=<bucket> seaweedfs-migrate`.
2. Stop the consumer (writer and, for Loki, its compactor), then run the same
   command with `-e FINAL=1`. It overwrites changed objects, deletes objects
   MinIO no longer has, requires identical key and size listings, and writes
   `hyhome-migration/<bucket>.cutover`. A listing mismatch leaves no marker.
3. Recreate the consumer on the SeaweedFS configuration (`--build` for the
   Loki and Tempo images) and confirm health.
4. Read data from before the cutover and write new data (Loki: query old and
   new logs; Tempo: find an old and a new trace; MLflow: download an old
   artifact and log a new run). Then confirm the identity cannot reach another
   bucket.
5. The marker makes every later run for that bucket fail: a copy would replace
   objects the consumer has written since. The key and size check does not see
   a same-size content change, so keep the consumer stopped between step 2 and
   step 3. Rolling back after new writes means copying those objects back to
   MinIO first, then deleting the marker with the admin identity.

`cdn-bucket` is empty in MinIO and is not copied, so no MinIO bucket policy
can carry over.

### Backup (daily, RUN-0021)

`hyhome-backup.sh` runs, through `seaweedfs-master`:
`volume.vacuum.disable`, then `fs.meta.save -o /tmp/filer.meta /` copied to the
staging export, then Restic reads `data/seaweedfs/volume` and
`data/seaweedfs/master`, then `volume.vacuum.enable` in its EXIT trap. The
script fails the run on a non-zero `weed shell` exit or error text in its
output, on an empty export, or when only one of master and filer runs; a stale export is removed before each save. SeaweedFS not running at all
is not a failure. A run killed with SIGKILL (for example at the unit's stop
timeout) leaves vacuum off: run `volume.vacuum.enable` through
`hyhome-seaweedfs.sh shell` in `seaweedfs-master`.

### Restore (isolated first)

1. Restore the Restic snapshot's `data/seaweedfs/{volume,master}` and the
   `seaweedfs-filer.meta` export (RUN-0021 step 5) to an empty target at the
   same version, with an empty `filer` directory.
2. Start the four services and wait for health.
3. Copy the export into `seaweedfs-master` and run `fs.meta.load` through
   `hyhome-seaweedfs.sh shell`, then `volume.fsck`; objects changed during the
   backup's Restic window may be missing (POL-0024).
4. Read back objects of every bucket through S3 and compare counts and bytes
   with the manifest before any client is switched.

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
failure, security exposure or version incompatibility. Never restore volume
trees without the filer metadata export of the same snapshot.

## Traceability

- Runtime source: [SeaweedFS Compose](../../../../../infra/04-data/lake-and-object/seaweedfs/docker-compose.yml).
- Artifact: `RUN-0024`; parent guide: `GDE-0024`.
- The isolated rehearsal ran on 2026-09-22 (SPEC-0180 Task 0008 S06); HOME activation and HOME restore have not run.

### References

- [SeaweedFS data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup)
- [Policy](policy.md)

## Related Documents

- [Domain catalog](../README.md)
