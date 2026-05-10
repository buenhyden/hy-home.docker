<!-- Target: docs/05.operations/guides/04-data/operational/supabase.md -->

# Supabase Operations Policy

> Operational policy and governance for the Supabase platform in `hy-home.docker`.

---

## Overview (KR)

이 문서는 Supabase 플랫폼의 운영 정책을 정의한다. 데이터 백업, 보안 통제, 리소스 확장 및 규정 준수 확인 방법을 규정한다.

## Policy Scope

- Persistence layer (PostgreSQL) management.
- Authentication and JWT security.
- Asset storage and websocket realtime policies.
- Edge function deployment and runtime limits.

## Applies To

- **Systems**: Supabase Stack (db, auth, rest, storage, kong, realtime, functions).
- **Agents**: AI Agents managing or interacting with Supabase APIs.
- **Environments**: Production and Staging.

## Controls

- **Required**:
Copyright (c) 2026. Licensed under the MIT License.

---

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

- [../README.md](../README.md)
- [../../05.operations/README.md](../../../README.md)
- [../../05.operations/README.md](../../../README.md)

## Usage

> Migrated from `docs/05.operations/04-data/operational/supabase.md` during the 2026-05-10 operations taxonomy consolidation.

### Supabase Platform Usage

> Comprehensive guide for self-hosting Supabase in `hy-home.docker`.

---

#### Overview (KR)

이 문서는 `hy-home.docker` 환경에서 Supabase 플랫폼을 구성하고 운영하기 위한 가이드다. PostgreSQL 기반의 통합 백엔드 서비스(Auth, Realtime, Storage, Edge Functions)의 구조와 로컬 관리 방법을 설명한다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- Developer
- Operator
- AI Agents

#### Purpose

- Understand the Supabase stack components and their interactions.
- Provide instructions for local setup and dashboard access.
- Define service boundaries and integration points.

#### Prerequisites

- Docker and Docker Compose installed.
- Access to the `04-data/operational/supabase` directory.
- Properly configured `.env` file.

Copyright (c) 2026. Licensed under the MIT License.

---

#### Step-by-step Instructions

1. 관련 README와 기존 본문을 먼저 읽는다.
2. 실제 compose/config 경로와 문서 설명이 일치하는지 확인한다.
3. 변경이 필요하면 대응 템플릿과 상위 README 링크를 함께 갱신한다.
4. 관련 검증 스크립트 또는 문서 audit를 실행한다.

#### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

#### Related Documents

- [../README.md](../README.md)
- [../../05.operations/README.md](../../../README.md)
- [../../05.operations/README.md](../../../README.md)

## Procedure

> Migrated from `docs/05.operations/04-data/operational/supabase.md` during the 2026-05-10 operations taxonomy consolidation.

### Supabase Platform Procedure

: Supabase Stack

> Operational procedures for common Supabase maintenance and recovery tasks.

---

#### Overview (KR)

이 런북은 Supabase 플랫폼 운영 중 발생하는 일반적인 작업(재해 복구, 비밀번호 초기화, 로그 분석 등)에 대한 실행 절차를 정의한다.

#### Purpose

- Provide step-by-step recovery procedures for database failure.
- Define manual management tasks for Auth and Storage.
- Standardize log troubleshooting across the stack.

#### Canonical References

- `[../../02.architecture/requirements/04-data/operational-data-architecture.md]`
- `[../../../infra/04-data/operational/supabase/docker-compose.yml]`

#### When to Use

- Database container fails to start due to corruption.
- JWT secret rotation is required.
- Storage volume reaches capacity.

#### Procedure or Checklist

##### Database Recovery

1. Stop the stack: `docker compose down`.
2. Locate the last healthy backup in `${DEFAULT_DATA_DIR}/backups/supabase/`.
3. Restore the SQL dump to the database volume.
4. Restart the stack: `docker compose up -d`.

##### Password Reset (Initial)

1. Access Studio at `http://localhost:3000`.
2. Navigate to Authentication -> Users.
Copyright (c) 2026. Licensed under the MIT License.

---

#### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../README.md)
- [../../05.operations/README.md](../../../README.md)
- [../../05.operations/incidents/README.md](../../../incidents/README.md)
