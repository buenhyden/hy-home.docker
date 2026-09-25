---
title: "SurrealDB Policy"
version: "0.2.1"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0080"
parent_ids:
- "AD-0011"
created: "2026-09-19"
---

# SurrealDB Policy

## Overview

This policy governs the `OPTIONAL` single-service SurrealDB deployment used by Open Notebook within the `11-laboratory` tier.

## Policy Scope

- [Authored Compose source](../../../infra/11-laboratory/open-notebook/docker-compose.yml), Dockerfile, and entrypoint
- Service `surrealdb`; exact profiles `surrealdb`, `notebook`
- `surrealdb-data:/mydata`, loopback host mapping, `ai_net`
- `surreal_db_password` and root/namespace/database authentication scope
- Linked guide and runbook

## Controls

- **Required**: Host exposure remains loopback-only and application traffic remains on `ai_net`; broader publication requires an approved gateway change.
- **Required**: SurrealDB is pinned to v2 for Open Notebook upstream compatibility. Major upgrades to SurrealDB v3 or higher are prohibited until Open Notebook officially validates support.
- **Required**: Credentials use the Docker Secret. Documentation and evidence must not contain password values, credential-bearing URLs, raw records, or token material.
- **Required**: Every backup identifies SurrealDB version, namespace, database, auth level, schema/data scope, export options, checksum/location, retention/expiry, and isolated restore result.
- **Required**: Restore uses a fresh isolated compatible target and authorized root, namespace, or database credentials. Confirm `OPTION IMPORT` expectations before import.
- **Required**: Because import can partially succeed, any failed target is discarded and recreated empty before retry. Verify namespace/database, tables, schema, permissions, record-count invariants, and representative reads.
- **Required**: Upgrade follows upstream storage-format sequencing and requires a restore-tested export, capacity review, explicit rollback point, and approval. Removal requires retained export evidence and confirmed consumer shutdown.
- **Allowed**: Compose rendering, service state, readiness, and sanitized authenticated metadata checks.
- **Disallowed**: Changing password files to repair readiness, copying live `/mydata`, reusing a partially imported target, or presenting an unexecuted rehearsal as tested recovery.

## Exceptions

Owner `@buenhyden` must record scope, risk, expiry, exit condition, backup identifier, and rollback evidence before a deviation.

## Verification

- `docker compose --profile surrealdb config --quiet`
- Compare service/profile/mount/secret facts with the linked guide, runbook, and infra README.
- Run `python3 scripts/validation/check-document-links.py --mode all`.

## Review Cadence

Review monthly and before image, storage format, persistence, authentication, namespace/database, exposure, upgrade, or removal changes.

## Traceability

- Governing architecture: [AD-0011](../../02.architecture/descriptions/0011-laboratory-architecture.md)
- Subject peers: [Guide](../guides/0080-surrealdb.md), [Runbook](../runbooks/0080-surrealdb.md)

## Related Documents

- [SurrealDB export](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/export)
- [SurrealDB import](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/import)
- [SurrealDB upgrades and patching](https://surrealdb.com/docs/manage/self-hosted/upgrades-and-patching)
- [SurrealDB authentication](https://surrealdb.com/docs/learn/security/authentication/summary)
- [SurrealDB licensing](https://surrealdb.com/license)
- [Runtime version projection](../../../infra/tech-stack.versions.json)
- [Operations index](../README.md)
- [Infrastructure README](../../../infra/11-laboratory/open-notebook/README.md)
