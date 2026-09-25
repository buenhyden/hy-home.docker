---
title: "Open Notebook Recovery Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0073"
parent_ids:
- "GDE-0073"
created: "2026-05-17"
---

# Open Notebook Recovery Runbook

## When to Use

Use for app/DB readiness failure, unreadable provider keys, missing notebook
content, API exposure concern, backup/restore, or an approved upgrade.

## Procedure

1. Validate and inspect from the root:

   ```bash
   docker compose --profile notebook config --quiet
   docker compose --profile notebook ps surrealdb open_notebook
   docker compose --profile notebook logs --tail=200 surrealdb open_notebook
   ```

2. Separate app password, encryption key, DB credential, database, app-data,
   gateway/UI, API, and provider symptoms. Never print key values or content.
3. If provider keys became unreadable, stop writes and confirm the encryption-key
   secret identity/custody. Do not overwrite/re-save keys with a replacement key.
4. Restart database first, verify readiness, then restart only the app. Keep
   provider/model egress disabled until content and credential checks pass.

### Backup and isolated restore

1. Block app writes or stop `open_notebook` while keeping SurrealDB available for
   a consistent logical export. Export the configured namespace/database to a
   protected SurrealQL file without putting the password on the command line.
2. Stop remaining writers, copy `/app/data`, and record export/app-data checksums,
   source commit, namespace/database, and protected key/credential receipt.
3. Import into isolated SurrealDB; mount a copied app-data directory; supply the
   same encryption key privately. Disable external provider/network calls.
4. Verify notebook/source/settings counts, credential decryptability as a boolean,
   and one synthetic notebook. Promote only after review.

### Upgrade

Repeat the backup, inspect release/migration/security notes, test the target image
against restored copies, and verify content plus credential decryption. On failure,
stop target and restore prior image and both data scopes.

## Evidence

Record exits, source commit, export/app-data checksums, counts, auth/decryption
booleans, API boundary, and final state. Never record content or secret values.

## Rollback or Recovery

Backup/restore and upgrade rehearsal are **planned but unexecuted**. Loss of the
encryption key is not repaired by database restore alone.

## Escalation

Stop on missing/mismatched encryption key, DB export failure, unexpected API
exposure, sensitive content leak, migration error, or unknown provider activity.

## Traceability

- [Guide](../guides/0073-open-notebook.md) (`GDE-0073`)
- [Policy](../policies/0073-open-notebook.md) (`POL-0073`)
- [Open Notebook Compose](../../../infra/11-laboratory/open-notebook/docker-compose.yml)
- [SurrealDB Operations](../guides/0080-surrealdb.md) (`GDE-0080`)

## Related Documents

- [SurrealDB export](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/export)
- [Open Notebook security](https://github.com/lfnovo/open-notebook/blob/main/docs/5-CONFIGURATION/security.md)
