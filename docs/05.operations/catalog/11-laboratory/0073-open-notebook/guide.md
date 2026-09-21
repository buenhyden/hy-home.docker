---
title: "Open Notebook Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
artifact_id: "GDE-0073"
parent_ids:
- "POL-0073"
implementation_services:
  infra/11-laboratory/open-notebook/docker-compose.yml:
  - open_notebook
created: "2026-05-10"
---

# Open Notebook Usage Guide

## Usage

### Purpose and classification

Open Notebook is an OPTIONAL notebook knowledge workspace. The
`open_notebook` service belongs only to `notebook`; owner commit `d5912ab03`
removed it from the catch-all `admin` selector, and it is excluded from HOME. Its `surrealdb` dependency is co-located in the same
[Open Notebook Compose](../../../../../infra/11-laboratory/open-notebook/docker-compose.yml),
which shares those selectors and provides the persistent database.

### Current implementation and data

- [Open Notebook Compose](../../../../../infra/11-laboratory/open-notebook/docker-compose.yml)
  owns the app service, route, app-data volume, secrets, and healthcheck.
- `/app/data` stores application files. SurrealDB `/mydata` stores notebooks,
  sources, model/provider settings, and encrypted provider credentials.
- `open_notebook` upstream strictly requires SurrealDB v2; SurrealDB v3 is incompatible
  and unsupported.
- `open_notebook_password`, `open_notebook_encryption_key`, and
  `surreal_db_password` are Docker secrets. Upstream states that losing/changing
  the encryption key makes previously encrypted API keys unreadable; keep key
  custody separate from database backups.
- The API host port is bound to `127.0.0.1` only; browsers reach the web port
  through Traefik. The UI route uses the admin CIDR allowlist and the Open
  Notebook password; shared SSO was removed by owner commit `b90b74837`, so no
  gateway identity or group check applies to this route.
- Directory health proves mount availability only, not DB, provider, model, or
  notebook function.

### Normal use, backup, and upgrade

Validate `docker compose --profile notebook config --quiet`, verify both services,
and start the database before the app. Use the application password plus gateway
control; configure only approved model/provider endpoints and keys. Notebook
content, source documents, embeddings, and provider keys are sensitive. Retain
SurrealDB on v2; do not upgrade to v3.

For backup, quiesce app writes, export the configured SurrealDB namespace/database
with `surreal export`, copy `/app/data`, and retain the encryption key and DB
credential through protected custody. Restore into an isolated SurrealDB with
provider/network egress disabled, import the export, mount the app data, supply
the same encryption key privately, and verify counts plus one synthetic notebook.
Before upgrade, review floating-tag/release changes and test this restore. No
backup, restore, provider call, or upgrade ran here.

## Common Checks

- `docker compose --profile notebook config --quiet`
- `docker compose --profile notebook config --services`
- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`

## Runbook Handoff

Use the [runbook](runbook.md) for database/key/provider recovery and upgrades.

## Traceability

- [Policy](policy.md) (`POL-0073`)
- [Runbook](runbook.md) (`RUN-0073`)
- [Laboratory architecture](../../../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [Open Notebook security and encryption-key custody](https://github.com/lfnovo/open-notebook/blob/main/docs/5-CONFIGURATION/security.md)
- [Open Notebook deployment](https://github.com/lfnovo/open-notebook/blob/main/README.md)
- [SurrealDB backups and recovery](https://surrealdb.com/docs/manage/self-hosted/backups-and-recovery)
