---
title: "Management Database Health and Init Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0028"
parent_ids:
- "GDE-0028"
created: "2026-05-17"
---

# Management Database Health and Recovery Runbook

## When to Use

Use for approved static diagnosis, backup planning or isolated recovery of this
exact subject. Live writes, restore, cutover, cleanup and credential changes need
a separately approved task.

## Procedure

From the repository root:

```bash
docker compose --env-file .env.example --profile mng config --quiet
docker compose --env-file .env.example --profile mng config --services
```

Confirm both engines, init, exporters, separate persistent volumes, secret
references, health checks and `mng_data_net`. Do not print the fully rendered
configuration where environment substitutions could expose private values.

### Planned PostgreSQL backup

1. Open a consumer-aware window and inventory roles plus `postgres`, `n8n`,
   `keycloak`, `airflow`, `terrakube`, `sonarqube` and the configured application
   database. Discover additions rather than assuming this list is exhaustive.
2. Use a compatible PostgreSQL client to dump cluster globals and each database
   in a restorable logical format. Never raw-copy live `PGDATA`.
3. Record source/server and client versions, database names, sizes, dump sizes,
   exit status and hashes. Store artifacts on a separate encrypted destination;
   keep passwords out of arguments and evidence.

### Planned PostgreSQL isolated restore

1. Provision an empty isolated target at a supported compatible version with no
   application routes. Use a least-privileged restore operator.
2. Inspect the trusted dump source because `pg_restore` can execute statements
   selected by source superusers. Restore globals/roles, then create and restore
   each database in dependency-aware order.
3. Validate roles and grants, schema objects, extension availability, table/row
   counts and selected application reads. Connect disposable Keycloak, Airflow,
   n8n, Terrakube and SonarQube checks only when their owners approve.
4. Record recovery point and elapsed time. A separate cutover pauses writers,
   takes a final dump, switches consumers and retains the prior volume for rollback.

### Planned Valkey backup and restore

1. Pause or drain workflow producers/workers and document whether queued jobs will
   be replayed or discarded.
2. Create/verify an RDB checkpoint and copy the entire AOF directory and manifest
   without crossing an AOF rewrite. Record hashes and persistence configuration.
3. Restore the complete set to an empty isolated compatible Valkey target. Confirm
   clean load, key/type/TTL counts and a disposable read/write/delete test.
4. Never connect restored stale queue state to active workers without workflow
   owner approval.

## Evidence

Record source revision/version, scope, timestamps, manifest/checksum summary,
commands and exit status, validation result, observed recovery point/time and all
unverified gaps. Exclude secrets, raw payloads and private resolved paths.

## Rollback or Recovery

A failed cutover returns consumers to the validated prior HOME engines and volumes;
the isolated restore remains blocked from clients. Cutover occurs only after owner approval,
final consistency capture, application validation and a retained rollback window.

## Escalation

Stop on missing databases, dump errors, unsupported extensions, ownership drift,
AOF truncation/repair prompts, checksum mismatch or ambiguous queue semantics.
No recovery described here was executed by the documentation correction task.

## Traceability

- Artifact: `RUN-0028`; parent guide: `GDE-0028`.
- Procedures are planned unless a dated verification record explicitly says they ran.

### References

- [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)
- [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html)
- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Policy](policy.md)

## Related Documents

- [Domain catalog](../README.md)
