---
title: "Management Database Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0028"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# Management Database Operations Policy

## Overview

This policy binds current source configuration to data protection, security,
resource, lifecycle and independently verifiable operator controls.

## Policy Scope

The five `mng-db` services are HOME. They are shared dependencies, so database,
role, broker or credential changes require consumer-aware maintenance and
rollback.

## Controls

- Operate through the root project with `mng`, `core`, `dev`, or `local`; do not
  run the leaf Compose file independently.
- Keep PostgreSQL and Valkey on separate bind-backed volumes and preserve
  `mng_data_net`, health checks, secret files and shared resource limits.
- Keep `mng_db_password`, `mng_valkey_password` and service database credentials
  in Docker secret custody. Dumps and evidence must not contain plaintext values.
- Treat `mng-pg-init` as idempotent provisioning, not restore. Review its complete
  role/database list before rerun. It must not read optional-capability secrets
  or run their DDL; those belong to feature provisioning jobs, which refuse
  administrator role names and foreign-owned databases or schemas.
- Every psql variable the init SQL reads must be passed by its runner; the
  contract test in `tests/validation/test_compose_baseline_gates.py` enforces it.
- Replication slots are CDC recovery state; do not drop them to reclaim space
  without the CDC resynchronization approval in `POL-0036`.
- Treat Valkey as workflow broker state, not a disposable cache. Restoring stale
  queues can duplicate or reorder work.

### Backup and restore

Capture PostgreSQL globals and each current database with logical tools to a
separate encrypted destination. Capture Valkey's complete AOF set and manifest
plus an RDB checkpoint at a documented quiesced point. Retain PostgreSQL daily sets for 30 days and weekly sets for 90 days; retain
Valkey broker sets daily for 7 days. Planning objectives are RPO 24 hours and RTO
4 hours; no HOME rehearsal proves them. Shared resource-template limits remain
mandatory. Removal or consolidation requires every consumer, schema, credential
and queue to be migrated and rollback-tested.

Restore PostgreSQL globals before databases on a fresh isolated compatible
cluster. Treat every dump as untrusted executable SQL, restrict restore rights,
and validate roles, schemas, row counts and named consumer health. Restore Valkey
only after workflow owners approve queue replay semantics. Production cutover or
data replacement requires separate approval.

### Upgrade policy

Review official release notes, extension/client compatibility and rollback for
every pin change. A PostgreSQL major upgrade requires isolated logical
restore/rehearsal; direct `PGDATA` reuse is prohibited. Preserve the prior volume
until acceptance and rollback expiry.

## Exceptions

No cache-only exception applies to workflow queue state. Exceptions do not authorize runtime mutation, plaintext secrets, raw active
storage copies or same-host availability claims.

## Verification

Verify root configuration and scoped static policy checks, then require an
isolated compatible restore with application-level acceptance before promotion or
cutover. Record unverified runtime properties explicitly.

## Review Cadence

Review after profile, image, volume, credential, consumer, retention or upstream
lifecycle change and at least annually while retained.

## Traceability

- Artifact: `POL-0028`; parent: `AD-0004`.
- Runtime authority remains the linked Compose/source files; exact pins stay there.

### References

- [PostgreSQL backup](https://www.postgresql.org/docs/current/backup.html)
- [pg_restore security and options](https://www.postgresql.org/docs/current/app-pgrestore.html)
- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Runbook](runbook.md)

## Related Documents

- [Domain catalog](../README.md)
