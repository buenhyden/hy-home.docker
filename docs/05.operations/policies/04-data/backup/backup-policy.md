---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/backup/backup-policy.md -->

# 04-Data Backup Policy

## Overview

이 문서는 `04-data` 계층의 백업 주기, 보존 기준, 검증 책임을 정의한다. 데이터 엔진별 중요도와 현재 운영 계약에 맞춰 백업을 적용하고, 복구 가능성은 정기 검증 evidence로 관리한다.

## Policy Scope

- **Systems**: PostgreSQL/Supabase 계열 critical data, Valkey cache data, MinIO/SeaweedFS object data, MongoDB/Cassandra/CouchDB/Neo4j/Qdrant/OpenSearch 등 `infra/04-data` 서비스의 persistent data surface
- **Tools**: native backup utilities, encrypted off-site snapshot tooling, object-storage sync tooling
- **Agents**: repo-local governance를 따르는 AI agents and operators handling backup documentation or validation
- **Environments**: local, development, homelab operations, and production-like rehearsals

## Controls

- **Required**: critical relational and Supabase data must have daily backups with 30-day retention and monthly verification evidence.
- **Required**: object storage backups must have weekly snapshots or sync evidence with 90-day retention and quarterly verification.
- **Required**: every backup drill must record target service, backup source, retention window, verification result, and operator or agent evidence.
- **Allowed**: cache-only Valkey data may be excluded from scheduled backup when the service contract treats it as reconstructable cache.
- **Allowed**: encrypted off-site snapshots and object sync jobs may use service-specific tooling when evidence is recorded.
- **Disallowed**: plaintext secret values, unencrypted off-site backup artifacts, and unverified claims that a backup is restorable.

## Exceptions

Backup exceptions require explicit owner approval and evidence showing why the data is reconstructable, intentionally ephemeral, or covered by another current policy. Exceptions must be reviewed again when service persistence, retention, or recovery objectives change.

## Verification

- Confirm the target service has a documented persistence boundary in `infra/04-data/**/README.md` or its paired operations documents.
- Confirm backup evidence records the service, retention window, command or job class, and verification outcome without exposing secret values.
- Run repository documentation checks after policy or link changes:
  - `bash scripts/validation/check-doc-implementation-alignment.sh`
  - `bash scripts/validation/check-repo-contracts.sh`

## Review Cadence

- Monthly for critical relational and Supabase backup evidence.
- Quarterly for object storage backup drills.
- On material change for persistence paths, service topology, retention policy, or recovery objectives.

## Related Documents

- [Operations index](../../../README.md)
- [04-data policies index](../README.md)
- [Storage exhaustion runbook](../../../runbooks/04-data/storage/storage-exhaustion.md)
- [04-data guides index](../../../guides/04-data/README.md)
