---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/operational/supabase.md -->

# Supabase Runbook

## Overview (KR)

이 런북은 Supabase 플랫폼 운영 중 발생하는 일반적인 작업(재해 복구, 비밀번호 초기화, 로그 분석 등)에 대한 실행 절차를 정의한다.

## Supabase Platform Procedure

> Scope: Supabase Stack

> Operational procedures for common Supabase maintenance and recovery tasks.

---

### Purpose

- Provide step-by-step recovery procedures for database failure.
- Define manual management tasks for Auth and Storage.
- Standardize log troubleshooting across the stack.

### Canonical References

- [../../../../02.architecture/requirements/0004-data-architecture.md](../../../../02.architecture/requirements/0004-data-architecture.md)
- `[../../../infra/04-data/operational/supabase/docker-compose.yml]`

## When to Use

- Database container fails to start due to corruption.
- JWT secret rotation is required.
- Storage volume reaches capacity.

## Procedure

### Checklist

- [ ] 관련 policy, guide, runbook handoff를 확인한다.
- [ ] 현재 상태와 변경 범위를 기록한다.

### Database Recovery

1. Stop the stack: `docker compose down`.
2. Locate the last healthy backup in `${DEFAULT_DATA_DIR}/backups/supabase/`.
3. Restore the SQL dump to the database volume.
4. Restart the stack: `docker compose up -d`.

#### Password Reset (Initial)

1. Access Studio at `http://localhost:3000`.
2. Navigate to Authentication -> Users.
Copyright (c) 2026. Licensed under the MIT License.

---

### Steps

1. 이 runbook의 trigger와 checklist를 확인한다.
2. 기존 절차가 문서에 포함되어 있으면 그 순서대로 수행한다.
3. 실행 중 생성된 명령 출력과 판단 근거를 evidence로 남긴다.
4. 검증 실패, secret exposure 위험, 파괴적 변경 필요 시 즉시 중단하고 `## Escalation`으로 이동한다.

### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/operational/supabase.md)
- [Operations policy](../../../policies/04-data/operational/supabase.md)
