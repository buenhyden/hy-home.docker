---
title: "SurrealDB Guide"
version: "0.2.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
artifact_id: "GDE-0080"
parent_ids:
- "POL-0080"
implementation_services:
  infra/11-laboratory/open-notebook/docker-compose.yml:
  - 'surrealdb'
created: "2026-09-19"
---

# SurrealDB Guide

## Usage

### Overview

SurrealDB is an `OPTIONAL` database for Open Notebook pinned to SurrealDB v2 for upstream compatibility. [The Compose implementation](../../../../../infra/11-laboratory/open-notebook/docker-compose.yml) defines one `surrealdb` service under exact `surrealdb` and `notebook` profiles; `admin` no longer selects it. The custom Dockerfile and entrypoint own the server process, `surrealdb-data` persists `/mydata`, and `surreal_db_password` supplies root authentication without a literal in Compose.

### Current implementation

| Field | Repository-specific decision |
| --- | --- |
| Consumer and data rationale | OPTIONAL persistent multi-model database for Open Notebook; pinned to SurrealDB v2 due to upstream compatibility constraints. |
| Source / updater | [Compose](../../../../../infra/11-laboratory/open-notebook/docker-compose.yml), [Dockerfile](../../../../../infra/11-laboratory/open-notebook/surrealdb/Dockerfile), and entrypoint own the process; base image is pinned to SurrealDB v2. |
| Services / profiles | Single `surrealdb`; exact `surrealdb`, `notebook`. |
| Flow / exposure | Open Notebook connects on `infra_net`; host access is internal port 8000 via Compose exposure. |
| Persistence / environment | bind-backed `surrealdb-data:/mydata`; host-port and path inputs are Compose-owned. |
| Secrets / security | `surreal_db_password`; root/namespace/database auth scopes must match each operation. |
| Health / resources | `surreal is-ready` proves reachability only; the custom service uses its Compose-declared template. |
| Backup / upgrade | explicit namespace/database export/import to a fresh compatible target; failed partial import requires target disposal; follow upstream storage-format sequence within v2. |
| License / edition | SurrealDB use must comply with the current official license terms; this document does not extend production or commercial rights. |

### Usage Type

`system-guide | operational-reference`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

Describe the current profile, exposure, persistence, authentication, namespace/database scope, version constraints (v2 only), and restore contract without claiming a live recovery test.

### Prerequisites

- Work from the repository root; root Compose owns inclusion.
- Prepare the `surreal_db_password` Docker Secret without printing or copying its value.
- Record the intended SurrealDB namespace and database. Export/import without this scope is not an acceptable recovery artifact.
- Treat the Compose/Dockerfile declarations as the runtime version authority (pinned to SurrealDB v2); upgrades to v3 are unsupported by Open Notebook.

### Step-by-step Instructions

1. Render the selected surface: `docker compose --profile surrealdb config --quiet`.
2. Check the declared service: `docker compose --profile surrealdb ps surrealdb`.
3. Check readiness without credentials or data: `docker compose exec -T surrealdb /usr/local/bin/surreal is-ready --endpoint http://127.0.0.1:8000`.
4. Applications on `infra_net` connect via `ws://surrealdb:8000/rpc`.
5. For recovery inventory, bind every export to engine version, namespace, database, auth level, schema/data scope, checksum, retention, and an isolated restore result.

### Common Pitfalls

- Readiness proves reachability only; it does not verify authentication, namespace, database, schema, or persistence.
- Open Notebook upstream does not support SurrealDB v3. Upgrading this container to SurrealDB v3 will cause protocol and query failures.
- Root, namespace, and database users have different auth scopes. Restore credentials must be authorized for the selected namespace/database and `OPTION IMPORT` behavior.
- Import can partially apply before an error. A failed isolated target must be discarded and recreated empty.
- Do not copy a live `/mydata` directory. Use an approved export or a separately approved quiesced storage procedure.

## Common Checks

- `docker compose --profile surrealdb config --quiet`
- `docker compose --profile surrealdb ps surrealdb`
- `docker compose exec -T surrealdb /usr/local/bin/surreal is-ready --endpoint http://127.0.0.1:8000`

## Runbook Handoff

[Runbook](runbook.md) owns health triage and the planned isolated export/import rehearsal. [Policy](policy.md) owns backup, auth, retention, upgrade, and removal controls.

## Traceability

- Declared parent: [SurrealDB Policy](policy.md) (`POL-0080`)
- Governing architecture: [AD-0011](../../../../02.architecture/descriptions/0011-laboratory-architecture.md)
- Subject peers: [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [SurrealDB export](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/export)
- [SurrealDB import](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/import)
- [SurrealDB upgrades and patching](https://surrealdb.com/docs/manage/self-hosted/upgrades-and-patching)
- [SurrealDB authentication](https://surrealdb.com/docs/learn/security/authentication/summary)
- [SurrealDB licensing](https://surrealdb.com/license)
- [Operations index](../../../README.md)
- [Infrastructure README](../../../../../infra/11-laboratory/open-notebook/README.md)
