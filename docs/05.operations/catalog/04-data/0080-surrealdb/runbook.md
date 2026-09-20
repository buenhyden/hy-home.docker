---
title: "SurrealDB Runbook"
version: "0.2.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0080"
parent_ids:
- "POL-0080"
created: "2026-09-19"
---

# SurrealDB Runbook

## Overview

This runbook provides health triage and a planned isolated export/import rehearsal. No runtime, export, import, or storage mutation was executed for this documentation change.

### Purpose

Collect safe evidence and define a repeatable recovery test that preserves namespace, database, auth scope, schema and data.

## When to Use

- `surrealdb` is missing, unhealthy, or unreachable.
- Authentication, namespace/database selection, or persistence is in question.
- An approved backup, upgrade, or isolated restore rehearsal is being planned.

## Procedure

### Checklist

- [ ] Work from repository root and record selected exact profile.
- [ ] Record configuration commit, Dockerfile/[Compose](../../../../../infra/04-data/specialized/surrealdb/docker-compose.yml) version authority and [runtime version projection](../../../../../infra/tech-stack.versions.json), namespace, database, expected schema and record invariants.
- [ ] Keep `surreal_db_password` and raw records out of evidence.
- [ ] Obtain separate approval before any export, import, stop, upgrade, or volume action.

### Steps

1. Render configuration: `docker compose --profile surrealdb config --quiet`.
2. Check state: `docker compose --profile surrealdb ps surrealdb`.
3. Check reachability: `docker compose exec -T surrealdb /usr/local/bin/surreal isready --conn http://127.0.0.1:8000`.
4. Review sanitized logs: `docker compose --profile surrealdb logs --tail=120 surrealdb`.
5. Stop after evidence capture if mount, version, namespace/database, or authentication differs from the declared state.

### Planned Isolated Restore Rehearsal

1. With approval, record source version, namespace/database, auth level, table/schema/permission inventory, record-count invariants, export options and free capacity. Use protected credential input.
2. Run the upstream `surreal export` workflow for the explicitly named namespace and database. Preserve the export with manifest, checksum, version, scope, capture time, retention and expiry. Do not export credentials into the artifact.
3. Prepare a fresh compatible target that shares no production port, network, volume, or secret. Create separate test credentials at the auth scope needed for import.
4. Confirm `OPTION IMPORT` behavior and run the upstream `surreal import` workflow against the empty target and explicit namespace/database.
5. Verify readiness, authenticated namespace/database access, tables, schema definitions, permissions, record-count invariants and representative read-only queries. Sanitize evidence.
6. If import reports any error or invariant mismatch, treat the target as partially modified, discard its volume, and recreate it empty. Never retry over that target.

### Verification Steps

- Compose render and service state match the exact source/profile.
- Export checksum and declared scope match the rehearsal input.
- The isolated target passes schema, permission, count and representative-read checks.
- No source volume, route, credential, or runtime was changed.

### Safe Rollback or Recovery Procedure

Documentation changes revert through the scoped diff. A failed rehearsal rolls back by discarding only the isolated target and its dedicated volume; the source and protected export remain unchanged.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: Stop inspection if credentials or raw data appear.
- **Eval Re-run**: Run `python3 scripts/validation/check-document-links.py --mode all`.

## Evidence

Record date, configuration commit, service/profile, source and target versions, namespace/database identifiers, backup checksum, exit statuses, sanitized invariants, and the explicit unexecuted/executed state. Never record secret values or raw database contents.

## Rollback or Recovery

Only the planned isolated rehearsal above establishes restore evidence. Production cutover, route change, secret rotation, upgrade and storage replacement require separate approval and are unexecuted here.

## Escalation

Stop and contact `@buenhyden` when credentials, version/storage-format compatibility, namespace/database scope, partial import, destructive storage changes, or unavailable backups prevent safe progress.

## Traceability

- Declared parent: [SurrealDB Policy](policy.md) (`POL-0080`)
- Governing architecture: [AD-0004](../../../../02.architecture/descriptions/0004-data-architecture.md)
- Subject peers: [Guide](guide.md), [Policy](policy.md)

## Related Documents

- [SurrealDB export](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/export)
- [SurrealDB import](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/import)
- [SurrealDB upgrades and patching](https://surrealdb.com/docs/manage/self-hosted/upgrades-and-patching)
- [SurrealDB authentication](https://surrealdb.com/docs/learn/security/authentication/summary)
- [SurrealDB licensing](https://surrealdb.com/license)
- [Operations index](../../../README.md)
- [Infrastructure README](../../../../../infra/04-data/specialized/surrealdb/README.md)
