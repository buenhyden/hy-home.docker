---
title: "MinIO Object Storage Health Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "superseded"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0023"
parent_ids:
- "GDE-0023"
superseded_by: "RUN-0024"
created: "2026-05-17"
---

# MinIO Object Storage Health and Recovery Runbook

## When to Use

Use for approved static diagnosis, backup planning or isolated recovery of this
exact subject. Live writes, restore, cutover, cleanup and credential changes need
a separately approved task.

## Procedure

Run from the repository root:

```bash
docker compose --env-file .env.example --profile storage config --quiet
docker compose --env-file .env.example --profile storage config --services
```

Confirm `minio`, `minio-create-buckets`, `minio-data`, `infra_net`, the four
secret references, health check and standard gateway chain. A LAB review may
render `storage-cluster`, but must not start it or reuse HOME paths.

### Planned backup procedure

1. Obtain a maintenance window and record source image, endpoint, bucket list,
   policies, IAM identities, versioning/object-lock settings and client owners.
2. Prevent bucket-policy/IAM changes during capture. For a point-in-time boundary,
   pause writers or record the accepted object-change window.
3. Use an approved S3-aware mirror/replication tool to copy every object and all
   versions required by policy to a separate encrypted destination. Do not copy
   the active `/data` tree.
4. Export or record bucket policies and IAM configuration without secret values.
   Record objects, bytes, failed transfers and sampled checksums per bucket.
5. Hash the manifest, protect it with the backup, and retain source credentials
   separately.

### Planned isolated restore

1. Provision an empty, network-isolated, compatible MinIO target with disposable
   root credentials. Do not point it at HOME or LAB data directories.
2. Recreate required application identity from protected custody, then buckets,
   versioning/retention and policies. Keep `loki-bucket`, `tempo-bucket` and
   `doc-intel-assets` private; reproduce public `cdn-bucket` only after exposure
   review.
3. Mirror objects and required versions from the backup. Compare bucket/object
   counts, bytes, version metadata and sampled checksums with the manifest.
4. With disposable clients, prove list/get/put/delete behavior and policy denial.
   Validate representative Loki and Tempo reads against the isolated endpoint
   without connecting production writers.
5. Record recovery point, elapsed time and incompatibilities. A separately
   approved cutover takes a final delta, pauses writers, switches clients and
   retains rollback.

## Evidence

Record source revision/version, scope, timestamps, manifest/checksum summary,
commands and exit status, validation result, observed recovery point/time and all
unverified gaps. Exclude secrets, raw payloads and private resolved paths.

## Rollback or Recovery

A failed cutover returns clients to the unchanged original S3 endpoint after
validation; the object backup and isolated target remain retained. Cutover occurs only after owner approval,
final consistency capture, application validation and a retained rollback window.

## Escalation

Stop on missing versions, policy drift, checksum mismatch, unexpected public
access, client incompatibility or pressure to import raw data directories. The
archived upstream status is an escalation trigger for migration planning, not a
reason to improvise a replacement.

## Traceability

- Runtime sources: [HOME MinIO Compose](../../../../../infra/04-data/lake-and-object/minio/docker-compose.yml) and [LAB cluster Compose](../../../../../infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml).
- Artifact: `RUN-0023`; parent guide: `GDE-0023`.
- Procedures are planned unless a dated verification record explicitly says they ran.

### References

- [MinIO community repository](https://github.com/minio/minio)
- [MinIO client mirror](https://github.com/minio/mc/blob/master/README.md)
- [Policy](policy.md)

## Related Documents

- [Domain catalog](../README.md)
