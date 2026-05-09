# Management Database Operations Policy

> This document defines policy, controls, and approval rules for the mng-db system.

---

## Overview (KR)

이 문서는 `mng-db` (Management Database)에 대한 운영 정책을 정의한다. 플랫폼 핵심 메타데이타의 보호와 가용성을 유지하기 위한 통제 기준 및 검증 방법을 규정한다.

## Policy Scope

이 정책은 `infra/04-data/operational/mng-db` 및 해당 서비스가 제공하는 모든 논리적 데이타베이스(n8n, keycloak, airflow 등)를 대상으로 한다.

## Applies To

- **Systems**: mng-pg, mng-valkey, mng-pg-init
- **Agents**: AI Agent (자동화 관리 및 메타데이터 접근 시)
- **Environments**: 모든 구현 및 운영 환경 (dev, staging, prod)

## Controls

- **Required**:
  - 모든 패스워드는 `/run/secrets/`를 통해 주입되어야 한다.
  - 정기적인 연결 상태 점검(`pg_isready`)을 수행해야 한다.
- **Allowed**:
  - `01-gateway` 계층에서의 읽기 권한을 허용한다.
  - 메타데이타 백업 시 `shared_net`을 통한 비 HA 전송을 허용한다.
- **Internal Only**: 외부 IP에서의 직접 접근은 엄격히 금지됩니다.
- **Credential Rotation**: 90일 주기로 Secrets 변경 수행.
- **Audit Logging**: DDL 변경 사항에 대한 로그 보존 (180일).
- **Disallowed**:
  - 대규모 비즈니스 데이타의 직접 저장을 금지한다.
  - 허가되지 않은 계정의 `postgres` 루트 DB 직접 접근을 금지한다.

## Exceptions

- 긴급 복구 작업은 사후 승인 기록을 남긴다.

## Related Documents

- **Runbook**: [mng-db.md](../../../09.runbooks/04-data/operational/mng-db.md)
- **Plan**: [2026-03-26-04-data-standardization.md](../../../05.plans/2026-03-26-04-data-standardization.md)

Copyright (c) 2026. Licensed under the MIT License.

---

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
