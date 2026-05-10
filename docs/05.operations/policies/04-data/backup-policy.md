# Backup Policy

Standard backup requirements for data infrastructure.

## 1. Frequency & Retention

| Database Tier | Frequency | Retention | Verification |
| :--- | :--- | :--- | :--- |
| **Critical** (PG, Supabase) | Daily | 30 Days | Monthly |
| **Cache** (Valkey) | None | N/A | N/A |
| **Object** (MinIO) | Weekly | 90 Days | Quarterly |

## 2. Tools

- **Native Utilities**: `pg_dump`, `mongodump`.
- **Restic**: Encrypted off-site snapshots to remote S3.
- **Rclone**: Syncing SeaweedFS volumes to secondary storage.

## 3. Verification

Backups are useless if they cannot be restored. Quarterly "Fire Drills" are mandatory for the **Critical** tier.

---

## Overview (KR)

이 문서는 `docs/05.operations/04-data/backup-policy.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Related Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
