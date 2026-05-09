<!-- Target: docs/09.runbooks/04-data/operational/supabase.md -->

# Supabase Platform Runbook

: Supabase Stack

> Operational procedures for common Supabase maintenance and recovery tasks.

---

## Overview (KR)

이 런북은 Supabase 플랫폼 운영 중 발생하는 일반적인 작업(재해 복구, 비밀번호 초기화, 로그 분석 등)에 대한 실행 절차를 정의한다.

## Purpose

- Provide step-by-step recovery procedures for database failure.
- Define manual management tasks for Auth and Storage.
- Standardize log troubleshooting across the stack.

## Canonical References

- `[../../02.ard/04-data/operational-data-architecture.md]`
- `[../../../infra/04-data/operational/supabase/docker-compose.yml]`

## When to Use

- Database container fails to start due to corruption.
- JWT secret rotation is required.
- Storage volume reaches capacity.

## Procedure or Checklist

### Database Recovery

1. Stop the stack: `docker compose down`.
2. Locate the last healthy backup in `${DEFAULT_DATA_DIR}/backups/supabase/`.
3. Restore the SQL dump to the database volume.
4. Restart the stack: `docker compose up -d`.

### Password Reset (Initial)

1. Access Studio at `http://localhost:3000`.
2. Navigate to Authentication -> Users.
Copyright (c) 2026. Licensed under the MIT License.

---

## Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

## Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

## Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

## Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Related Operational Documents

- [../README.md](../README.md)
- [../../08.operations/README.md](../../../08.operations/README.md)
- [../../10.incidents/README.md](../../../10.incidents/README.md)
