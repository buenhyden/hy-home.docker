---
title: "Open Notebook Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0073"
parent_ids:
- "AD-0011"
created: "2026-05-17"
---

# Open Notebook Operations Policy

## Overview

Open Notebook is an OPTIONAL knowledge/model workspace. Its content, database,
provider credentials, and encryption key form one recovery boundary.

## Policy Scope

Activation, UI/API exposure, app/database auth, provider/model access, content
retention, backup/restore, floating image upgrades, and removal.

## Controls

- Use `admin` or `notebook`; keep outside HOME.
- Preserve gateway/CIDR controls and separately verify the published API boundary.
  Application password and SurrealDB auth remain required.
- Keep provider keys in the app's encrypted store and protect
  `open_notebook_encryption_key` separately. Never rotate/lose it without an
  approved re-encryption/export plan.
- Treat notebooks, source documents, embeddings, chats, and provider settings as
  sensitive. Define retention and export ownership before use.
- Back up SurrealDB logically plus `/app/data`, source commit, and protected key/
  credential custody. Rehearse with provider egress disabled.
- Review release/security notes because the tracked image is intentionally
  floating. Test migrations and credential decryption before promotion.
- Export or explicitly dispose of content/provider credentials before removal;
  database and app-volume deletion are separate destructive actions.

## Exceptions

No exception may expose the API broadly, store keys in source, or restore data
without the matching encryption key and isolated verification.

## Verification

Verify UI/app auth, API boundary, DB readiness, key decryption, one synthetic
notebook, and provider access only where separately approved.

## Review Cadence

Review on release, provider/model, API route, DB schema, key, or retention changes.

## Traceability

- [Guide](guide.md) (`GDE-0073`)
- [Runbook](runbook.md) (`RUN-0073`)
- [Laboratory architecture](../../../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [Open Notebook Compose source](../../../../../infra/11-laboratory/open-notebook/docker-compose.yml)
- [Open Notebook security](https://github.com/lfnovo/open-notebook/blob/main/docs/5-CONFIGURATION/security.md)
- [SurrealDB backup and recovery](https://surrealdb.com/docs/manage/self-hosted/backups-and-recovery)
