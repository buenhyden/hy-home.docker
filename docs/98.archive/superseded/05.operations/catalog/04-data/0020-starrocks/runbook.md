---
title: "StarRocks Recovery Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "superseded"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "operations"
artifact_id: "RUN-0020"
parent_ids:
- "GDE-0020"
superseded_by: "RUN-0094"
created: "2026-05-17"
---

# StarRocks Recovery Runbook

## Overview

> Scope: StarRocks FE/BE readiness, BE registration evidence, and load retry boundaries.

이 런북은 `starrocks-fe` 또는 `starrocks-be` healthcheck가 실패하거나 BE registration/load job 상태 확인이 필요할 때 사용한다. 현재 compose는 단일 FE/BE pair를 제공한다.

### Purpose

- FE/BE service status를 current compose hostnames로 확인한다.
- BE registration command와 healthcheck evidence를 보존한다.
- load retry와 metadata mutation을 owner approval 없이 수행하지 않는다.

## When to Use

- `SHOW FRONTENDS` or `SHOW BACKENDS` health evidence fails
- `starrocks-be` fails to register with FE
- stream load retry is required

## Procedure

### Checklist

- [ ] root Compose renders the exact `starrocks` profile.
- [ ] FE and BE logs are preserved before restart.
- [ ] load retry or metadata changes have owner approval.

### Steps

1. Compose file과 repo-local 문서 계약을 확인한다.

   ```bash
   test -f infra/04-data/analytics/starrocks/docker-compose.yml
   python3 scripts/validation/check-document-links.py --mode all
   ```

2. FE/BE health evidence를 확인한다.

   ```bash
   mysql -u root -h starrocks-fe -P 9030 -e "SHOW FRONTENDS;"
   mysql -u root -h starrocks-fe -P 9030 -e "SHOW BACKENDS;"
   ```

3. Logs를 확인한다.

   ```bash
   docker compose --profile starrocks logs --tail 100 starrocks-fe starrocks-be
   ```

4. Restart is a runtime mutation. If separately approved, use the root project and exact service: `docker compose --profile starrocks restart starrocks-be`.

### Verification Steps

- [ ] `SHOW FRONTENDS` reports FE alive.
- [ ] `SHOW BACKENDS` reports `starrocks-be` alive.
- [ ] final evidence records whether restart or escalation was used.

### Observability and Evidence Sources

- **Logs**: `starrocks-fe` and `starrocks-be` logs
- **Metrics**: N/A - no separate exporter is declared in current compose.
- **Evidence**: FE/BE SQL status, logs summary, compose command class

### Planned isolated backup and restore

This procedure is documented from upstream behavior and **was not executed in this task**.

1. Record databases/tables/partitions, FE/BE health, source version, repository name and storage class, backup role, encryption state, free space, and an approval that covers the remote repository operation.
2. Create or select a remote StarRocks repository with credentials supplied outside documentation. Grant only `REPOSITORY` at system scope and `EXPORT` on the intended objects. Submit a named `BACKUP`, wait for `SHOW BACKUP` success, and record the snapshot timestamp; do not copy live bind paths as a shortcut.
3. Provision a fresh isolated FE/BE pair on a compatible version with empty volumes and no shared host publications. Register the repository and restore into a new database or renamed tables using the recorded snapshot timestamp and a replication count suitable for the one-BE rehearsal.
4. Wait for `SHOW RESTORE` success. Compare database/table inventory, row counts, representative queries, materialized views/UDFs that were in scope, FE/BE health, and checksums where the workload provides them.
5. If an asynchronous job fails or validation differs, cancel only the isolated job if needed, discard the fresh volumes, and retry. Do not drop/re-register the active backend or overwrite the active database.
6. Cutover, backend membership changes, or cleanup require separate approval. Until this succeeds, restore capability remains unverified.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: rerun docs validation after docs-only changes.

## Evidence

- Capture FE/BE status, service logs summary, restart decision, and any load label involved.

## Rollback or Recovery

Keep the source FE/BE pair and repository snapshot unchanged through validation. Rollback from a failed rehearsal is disposal of the isolated pair; rollback after an approved cutover must name the retained source or a second verified snapshot.

## Escalation

Escalate when FE metadata appears inconsistent, BE registration repeatedly fails, load retry may duplicate data, or destructive data/metadata changes are required.

## Traceability

- Declared parent: [StarRocks Usage Guide](guide.md) (`GDE-0020`)
- Governing authority: [Analytics Tier Architecture Description](../../../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](guide.md) (`GDE-0020`), [Policy](policy.md) (`POL-0020`)

## Related Documents

- [StarRocks backup and restore statements](https://docs.starrocks.io/docs/sql-reference/sql-statements/backup_restore/)
- [StarRocks RESTORE reference and privileges](https://docs.starrocks.io/docs/sql-reference/sql-statements/backup_restore/RESTORE/)
- [Compose implementation](../../../../../infra/04-data/analytics/starrocks/docker-compose.yml)

- [Operations runbooks index](../../../README.md)
- [Usage guide](guide.md)
- [Operations policy](policy.md)
