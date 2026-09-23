---
title: "Lakehouse Recovery Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0094"
parent_ids:
- "GDE-0094"
created: "2026-09-23"
---

# Lakehouse Recovery Runbook

## When to Use

A Spark job fails, the catalog returns an error, access is denied, or a table
needs rollback after a bad write.

## Procedure

1. Inspect:

   ```bash
   docker compose --profile lakehouse config --quiet
   docker compose --profile lakehouse logs --tail=100 seaweedfs-table-bucket seaweedfs-s3
   docker compose --profile lakehouse run --rm spark
   ```

   The last command lists namespaces and proves catalog access end to end.
2. Exit `64` from the wrapper means the `lakehouse` secret is missing or empty.
3. `table bucket … not found` means the table bucket is missing or belongs to
   another account: re-run `seaweedfs-table-bucket`, which recreates the bucket,
   policy and namespaces idempotently.
   (`seaweedfs-table-bucket` is the job; it also resets a hand-edited policy.)
4. `ForbiddenException` or `AccessDenied` means the identity line in
   `s3-identities.conf` or the table bucket policy is missing; both are
   restored by recreating `seaweedfs-s3` and re-running `seaweedfs-table-bucket`.
5. For a bad write, list snapshots and roll back:

   ```sql
   SELECT snapshot_id, committed_at, operation FROM dev.t.snapshots;
   CALL lakehouse.system.rollback_to_snapshot('dev.t', <snapshot_id>);
   ```

   Rollback works only while the snapshot has not been expired.

## Evidence

Record namespaces, table names, snapshot IDs, row counts, exit codes and the
source commit; never data values or the secret.

## Rollback or Recovery

Table metadata and data are SeaweedFS objects, covered by the SeaweedFS
recovery set (RUN-0024). Losing the filer metadata loses the catalog. Tables in
`dev` and `test` are reproducible and are not separately backed up.

## Escalation

Stop on any request to use the admin identity from an engine, to expose the
catalog beyond `object_net`, or to expire snapshots on a table without a named
reason.

## Traceability

- [Guide](guide.md) (`GDE-0094`)
- [Policy](policy.md) (`POL-0094`)
- [SeaweedFS runbook](../0024-seaweedfs/runbook.md)

## Related Documents

- [Spark package README](../../../../../infra/04-data/lakehouse/spark/README.md)
- [Iceberg maintenance](https://iceberg.apache.org/docs/latest/maintenance/)
