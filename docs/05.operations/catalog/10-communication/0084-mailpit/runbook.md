---
title: "Mailpit Runbook"
version: "0.2.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0084"
parent_ids:
- "POL-0084"
created: "2026-09-19"
---

# Mailpit Runbook

## When to Use

Use when synthetic mail is not captured, the database is locked/corrupt, the
retention limit is unexpected, or a backup/restore/upgrade is approved. Work
from the repository root and do not expose captured content in evidence.

## Procedure

1. Confirm root selection and bounded runtime state:

   ```bash
   docker compose --profile mail-dev config --quiet
   docker compose --profile mail-dev ps mailpit
   docker compose --profile mail-dev logs --tail=200 mailpit
   ```

2. Separate the failure:
   - `readyz` failure: inspect database permissions/locks and free space.
   - SMTP failure: verify the client uses service DNS from `infra_net` or the
     loopback host port; do not open the host bind.
   - UI failure: check Traefik/auth separately from SMTP capture.
3. If restart is approved, restart only Mailpit and send one synthetic message
   with a unique non-sensitive identifier. Verify capture without recording body.

### Consistent export and restore

1. Choose a protected backup directory outside Git with adequate free space.
2. Prefer a live export from the running instance. Create the dump in a temporary
   container path, copy it to the protected host directory, verify file count and
   checksum, then remove the container temporary copy. Do not log message files.
3. If the API is unhealthy, stop Mailpit and copy `mailpit.db` plus any SQLite
   `-wal`/`-shm` sidecars from the bind-backed data directory. Keep it stopped
   throughout the copy.
4. Restore into an isolated Mailpit instance/network. For exported messages, use
   `mailpit ingest` only against the isolated local SMTP listener; upstream notes
   that ingest does not support SMTP auth or TLS. Verify counts and synthetic
   samples, then obtain approval before replacing current data.

### Upgrade

1. Complete the export above and record current message count/database checksum.
2. Review release notes and database changes, update only the source pin in its
   owning change, and recreate only `mailpit`.
3. Verify `readyz`, authenticated UI, one synthetic SMTP capture, configured
   retention, and previous message count. On failure, stop the new container and
   recover into an isolated prior-version instance before any data replacement.

## Evidence

Record command exits, image/source commit, database/export checksums, message
counts, synthetic identifier, and final state. Never record recipients, headers,
bodies, attachments, or credentials.

## Rollback or Recovery

Backup/restore and upgrade rehearsal are **planned but unexecuted** here. Do not
overwrite the active SQLite database until an isolated restore succeeds and a
specific data replacement is approved.

## Escalation

Stop on suspected real-mail capture, database inconsistency, missing protected
backup, unknown SQLite sidecars, external exposure, or incompatible upgrade.

## Traceability

- [Guide](guide.md) (`GDE-0084`)
- [Policy](policy.md) (`POL-0084`)
- [Mailpit Compose](../../../../../infra/10-communication/mailpit/docker-compose.yml)

## Related Documents

- [Mailpit import/export](https://mailpit.axllent.org/docs/usage/import-export/)
- [Mailpit storage](https://mailpit.axllent.org/docs/configuration/email-storage/)
- [Operations index](../../../README.md)
