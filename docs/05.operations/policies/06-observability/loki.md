---
tier: 05.operations
component: 06-observability
title: Loki Operational Policy
status: active
runtime_state: production
updated: 2026-03-26
---
<!-- Target: docs/05.operations/policies/06-observability/loki.md -->

# Loki Operational Policy Operations Policy

> Operational standards for the Loki log aggregation system.

## 1. Data Retention Policy

To balance storage costs and operational needs, the following retention periods are enforced:

- **Standard Application Logs**: 7 Days (168h).
- **Security & Audit Logs**: 30 Days.
- **System Infrastructure Logs**: 7 Days.

> [!IMPORTANT]
> Retention is enforced by the Loki Compactor. Data older than the specified period is permanently deleted from MinIO.

## 2. Label Governance (Cardinality)

High cardinality labels can degrade Loki performance and increase storage costs.

- **Mandatory Labels**: `service_name`, `env`, `stream` (stdout/stderr).
- **Prohibited Labels**: User IDs, IP addresses, Request IDs, or any high-cardinality dynamic data.
- **Best Practice**: Use `LogQL` parsers (e.g., `| json`) to extract dynamic fields at query time instead of using them as labels.

## 3. Performance & Resource Standards

- **Batching**: Alloy must batch log entries (min 1s or 256KB) before pushing to Loki.
- **Ingester Memory**: `infra-loki` container is limited to 2GB RAM. Monitor `loki_ingester_memory_chunks_bytes` to prevent OOM.
- **Compaction**: The compactor runs every 10 minutes to optimize chunk storage in MinIO.

## 4. Backup & Disaster Recovery

- **Config Backup**: `infra/06-observability/loki/config/` is version-controlled.
- **Data Persistence**: MinIO buckets should be backed up using bucket replication or snapshots if long-term audit compliance is required.

---
[System Usage](../../guides/06-observability/loki.md) | [Recovery Procedure](../../runbooks/06-observability/loki.md)

---

## Overview

이 문서는 `docs/05.operations/policies/06-observability/loki.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

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

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/loki.md)
- [Recovery runbook](../../runbooks/06-observability/loki.md)
