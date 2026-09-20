---
title: "SurrealDB Guide"
version: "0.2.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0080"
parent_ids:
- "POL-0080"
implementation_services:
  infra/04-data/specialized/surrealdb/docker-compose.yml:
  - 'surrealdb'
created: "2026-09-19"
---

# SurrealDB Guide

## Usage

### Overview

SurrealDB is an `OPTIONAL` database for Open Notebook. [The Compose implementation](../../../../../infra/04-data/specialized/surrealdb/docker-compose.yml) defines one `surrealdb` service under exact `surrealdb`, `notebook`, and `admin` profiles. The custom Dockerfile and entrypoint own the server process, `surrealdb-data` persists `/mydata`, the host port is loopback-only, and `surreal_db_password` supplies root authentication without a literal in Compose.

### Current implementation

| Field | Repository-specific decision |
| --- | --- |
| Consumer and data rationale | OPTIONAL persistent multi-model database for Open Notebook. |
| Source / updater | [Compose](../../../../../infra/04-data/specialized/surrealdb/docker-compose.yml), [Dockerfile](../../../../../infra/04-data/specialized/surrealdb/Dockerfile), and entrypoint own the process; storage compatibility review owns upgrades. |
| Services / profiles | Single `surrealdb`; exact `surrealdb`, `notebook`, `admin`. |
| Flow / exposure | Open Notebook connects on `infra_net`; host access is loopback-only to internal port 8000. |
| Persistence / environment | bind-backed `surrealdb-data:/mydata`; host-port and path inputs are Compose-owned. |
| Secrets / security | `surreal_db_password`; root/namespace/database auth scopes must match each operation. |
| Health / resources | `surreal isready` proves reachability only; the custom service uses its Compose-declared template. |
| Backup / upgrade | explicit namespace/database export/import to a fresh compatible target; failed partial import requires target disposal; follow upstream storage-format sequence. |
| License / edition | SurrealDB use must comply with the current official license terms; this document does not extend production or commercial rights. |

### Usage Type

`system-guide | operational-reference`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

Describe the current profile, exposure, persistence, authentication, namespace/database scope, and restore contract without claiming a live recovery test.

### Prerequisites

- Work from the repository root; root Compose owns inclusion.
- Prepare the `surreal_db_password` Docker Secret without printing or copying its value.
- Record the intended SurrealDB namespace and database. Export/import without this scope is not an acceptable recovery artifact.
- Treat the Compose/Dockerfile declarations as the runtime version authority and check official storage-format compatibility before upgrade.

### Step-by-step Instructions

1. Render the selected surface: `docker compose --profile surrealdb config --quiet`.
2. Check the declared service: `docker compose --profile surrealdb ps surrealdb`.
3. Check readiness without credentials or data: `docker compose exec -T surrealdb /usr/local/bin/surreal isready --conn http://127.0.0.1:8000`.
4. Use `127.0.0.1:${SURREALDB_HOST_PORT:-8000}` only from the approved host; applications on `infra_net` use `surrealdb:8000`.
5. For recovery inventory, bind every export to engine version, namespace, database, auth level, schema/data scope, checksum, retention, and an isolated restore result.

### Common Pitfalls

- Readiness proves reachability only; it does not verify authentication, namespace, database, schema, or persistence.
- Root, namespace, and database users have different auth scopes. Restore credentials must be authorized for the selected namespace/database and `OPTION IMPORT` behavior.
- Import can partially apply before an error. A failed isolated target must be discarded and recreated empty.
- Do not copy a live `/mydata` directory. Use an approved export or a separately approved quiesced storage procedure.

## Common Checks

- `docker compose --profile surrealdb config --quiet`
- `docker compose --profile surrealdb ps surrealdb`
- `docker compose exec -T surrealdb /usr/local/bin/surreal isready --conn http://127.0.0.1:8000`

## Runbook Handoff

[Runbook](runbook.md) owns health triage and the planned isolated export/import rehearsal. [Policy](policy.md) owns backup, auth, retention, upgrade, and removal controls.

## Traceability

- Declared parent: [SurrealDB Policy](policy.md) (`POL-0080`)
- Governing architecture: [AD-0004](../../../../02.architecture/descriptions/0004-data-architecture.md)
- Subject peers: [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [SurrealDB export](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/export)
- [SurrealDB import](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/import)
- [SurrealDB upgrades and patching](https://surrealdb.com/docs/manage/self-hosted/upgrades-and-patching)
- [SurrealDB authentication](https://surrealdb.com/docs/learn/security/authentication/summary)
- [SurrealDB licensing](https://surrealdb.com/license)
- [Operations index](../../../README.md)
- [Infrastructure README](../../../../../infra/04-data/specialized/surrealdb/README.md)
