---
title: "dbt Recovery Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
artifact_id: "RUN-0090"
parent_ids:
- "GDE-0090"
created: "2026-09-21"
---

# dbt Recovery Runbook

## When to Use

Provisioning failure, connection or permission errors, a bad model run, or
credential rotation.

## Procedure

1. Inspect:

   ```bash
   docker compose --profile core --profile analytics-engineering config --quiet
   docker compose --profile core --profile analytics-engineering logs --tail=100 dbt-db-provision
   docker compose --profile core --profile analytics-engineering run --rm dbt debug
   ```

2. Provisioning exit `64` is an input problem before any change. Exit `3` names
   the refused condition: missing target database (run `mng-pg-init` first),
   missing source owner or schema, a target schema owned by another role, or a
   target equal to the source.
3. A failure after the role was created leaves the role and its `CONNECT` grant
   in place; `ON_ERROR_STOP` does not roll them back. Fix the cause and re-run
   `dbt-db-provision`; it converges.
4. For a bad model run, rebuild the affected relations with
   `run --rm dbt build --select <model>`; use `--full-refresh` only when the
   incremental state is known to be wrong.

### Credential rotation

Replace `secrets/db/postgres/dbt_password.txt` through the registered workflow,
re-run `dbt-db-provision`, then `dbt debug`.

## Evidence

Record exit codes, selected models, relation counts and the source commit; not
data values or passwords.

## Rollback or Recovery

Relations in `DBT_SCHEMA` are derived and can be rebuilt from sources; nothing
there is primary data. Dropping the schema is a data change that needs approval.

## Escalation

Stop on any request for superuser, source-schema write access, or `CREATE` on
the database.

## Traceability

- [Guide](guide.md) (`GDE-0090`)
- [Policy](policy.md) (`POL-0090`)
- [dbt Compose](../../../../../infra/09-tooling/dbt/docker-compose.yml)

## Related Documents

- [Image Dockerfile](../../../../../infra/09-tooling/dbt/Dockerfile) and [derived version projection](../../../../../infra/tech-stack.versions.json)
- [Management database runbook](../../04-data/0028-management-database/runbook.md)
