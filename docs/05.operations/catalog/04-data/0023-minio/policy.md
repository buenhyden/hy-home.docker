---
title: "MinIO Object Storage Operations Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0023"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# MinIO Object Storage Operations Policy

## Overview

This policy binds current source configuration to data protection, security,
resource, lifecycle and independently verifiable operator controls.

## Policy Scope

The current single-node service remains HOME because named consumers depend on
its buckets. The distributed same-host topology remains LAB. The archived
community upstream creates a migration-evaluation obligation, not permission to
replace or delete current storage.

## Controls

- Select services through root profiles: `storage`, `obs`, `logs`, `tracing` or
  `nginx` for HOME, and `storage-cluster` only for a named LAB exercise.
- Keep root and application identities in the four declared Docker secrets. Do
  not disclose values in commands, evidence or documentation.
- Preserve `infra_net`, health checks, resource limits and the standard gateway
  chain. Record that internal S3 is HTTP and no KMS/server-side encryption is
  declared in current Compose.
- Review the public-read `cdn-bucket` policy and all additional policy changes as
  exposure decisions. Buckets for logs/traces are never public.
- Treat four nodes on one host as a distribution test, not host availability.

## Backup and recovery

Back up objects through an S3-aware mirror or supported replication to a distinct
encrypted target. Preserve bucket names, policies, users, versioning, retention
and object metadata in a manifest. Retain daily recovery sets for 30 days and weekly sets for 90 days. The planning
objective is RPO 24 hours and RTO 8 hours; no rehearsal currently proves either.
Shared resource limits remain mandatory; removal requires proven client migration,
complete export, isolated restore and rollback.

Restore only to a fresh isolated compatible target. Recreate identities from
protected custody, recreate bucket controls, restore objects, compare counts,
bytes, checksums and version metadata, then test Loki/Tempo and other named
clients. Production cutover, lifecycle deletion and credential rotation require
separate approval.

## Upgrade and migration

Every image update or replacement requires official source/release review,
license review, client/API compatibility, a current export, an isolated restore,
and rollback. AIStor and SeaweedFS remain unselected candidates until a migration
spec proves semantics and recovery.

## Exceptions

The LAB cluster may be absent; HOME MinIO remains until an approved migration. Exceptions do not authorize runtime mutation, plaintext secrets, raw active
storage copies or same-host availability claims.

## Verification

Verify root configuration and scoped static policy checks, then require an
isolated compatible restore with application-level acceptance before promotion or
cutover. Record unverified runtime properties explicitly.

## Review Cadence

Review after profile, image, volume, credential, consumer, retention or upstream
lifecycle change and at least annually while retained.

## Traceability

- Runtime sources: [HOME MinIO Compose](../../../../../infra/04-data/lake-and-object/minio/docker-compose.yml) and [LAB cluster Compose](../../../../../infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml).
- Artifact: `POL-0023`; parent: `AD-0004`.
- Runtime authority remains the linked Compose/source files; exact pins stay there.

## References

- [Community repository and license](https://github.com/minio/minio)
- [MinIO client](https://github.com/minio/mc)
- [Backup policy](../0021-backup-and-restore/policy.md)
- [Runbook](runbook.md)


## Related Documents

- [Domain catalog](../README.md)
