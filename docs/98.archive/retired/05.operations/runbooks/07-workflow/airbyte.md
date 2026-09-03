---
status: active
---
<!-- Target: docs/05.operations/runbooks/07-workflow/airbyte.md -->

# Airbyte Runbook

## Overview (KR)

이 런북은 Airbyte 동기화 실패 또는 워커 장애 발생 시 즉시 실행할 복구 절차를 정의한다. 현재 저장소의 tracked runtime에는 `infra/07-workflow/airbyte/` 실행 자산이 없으므로, Airbyte는 도입 전/backlog 상태로 취급하고 실행 전 자산 존재 여부를 먼저 확인한다.

## Airbyte Procedure

> Scope: Airbyte / Workflow Tier

---

### Purpose

- Airbyte Sync 실패 원인을 신속히 분류하고 복구한다.
- 장애 증적을 표준 형식으로 수집한다.
- 안전한 원복 절차를 통해 데이터 불일치 위험을 최소화한다.

### Canonical References

- [2026-03-26-07-workflow.md](../../../01.requirements/2026-03-26-07-workflow.md)
- [0007-workflow-architecture.md](../../../02.architecture/requirements/0007-workflow-architecture.md)
- [0007-airflow-n8n-hybrid-workflow.md](../../../02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md)
- [07-workflow/spec.md](../../../03.specs/07-workflow/spec.md)
- [2026-03-26-07-workflow-standardization.md](../../../04.execution/plans/2026-03-26-07-workflow-standardization.md)

## When to Use

- Connector Sync가 연속 실패하는 경우
- Worker가 비정상 종료되거나 재시작 루프에 들어간 경우
- 스키마 변경 후 Sync가 중단된 경우
- 배포 직후 Connection이 실행되지 않는 경우

## Procedure

### Checklist

- [ ] `infra/07-workflow/airbyte/` 디렉터리와 `docker-compose.yml` 존재 여부 확인
- [ ] 장애 Connection ID, 영향 데이터셋, 첫 실패 시각 확보
- [ ] 최근 설정 변경(Connector/권한/네트워크) 여부 확인

### Steps

1. 실행 자산 존재 여부를 점검한다.

   ```bash
   test -d infra/07-workflow/airbyte && echo "dir:present" || echo "dir:missing"
   test -f infra/07-workflow/airbyte/docker-compose.yml && echo "compose:ok" || echo "compose:missing"
   ```

2. 디렉터리 또는 Compose 자산이 없는 경우, 런타임 명령을 실행하지 말고 운영 티켓을 생성한 뒤 수동 복구 절차로 전환한다.
   - 영향 범위 기록
   - 데이터 소스/타깃 직접 동기화 여부 검토
   - 승인된 우회 절차만 수행

3. 디렉터리와 Compose 자산이 모두 있는 경우에만 서비스 상태를 확인한다.

   ```bash
   docker compose -f infra/07-workflow/airbyte/docker-compose.yml ps
   ```

4. 장애 서비스 로그를 확인한다.

   ```bash
   docker compose -f infra/07-workflow/airbyte/docker-compose.yml logs --tail=200
   ```

5. 원인별로 조치한다.
   - 인증/권한 오류: Connector credential 교체 후 단건 Sync 재실행
   - 스키마 드리프트: 스키마 refresh 후 full/incremental 전략 재선택
   - 리소스 부족: Worker 리소스 상향 후 재시작

6. 복구 후 대상 Connection을 재실행하고 결과를 기록한다.

### Verification Steps

- [ ] 실패하던 Connection이 1회 이상 성공 완료됨
- [ ] Source/Destination 레코드 카운트가 허용 오차 내 일치
- [ ] 동일 에러가 30분 내 재발하지 않음

### Observability and Evidence Sources

- **Signals**:
  - Sync failure rate
  - Worker restart count
  - Connection latency
- **Evidence to Capture**:
  - 장애 시점 전후 로그 200줄
  - 설정 변경 이력(Connector/Connection diff)
  - 복구 실행자, 실행 시각, 검증 결과

### Safe Rollback or Recovery Procedure

- [ ] 장애 유발 Connector 변경을 이전 버전으로 복원
- [ ] 승인 없는 Full Refresh 실행은 중단
- [ ] 필요 시 마지막 정상 스냅샷 기준으로 재동기화 범위를 축소

### Agent Operations (If Applicable)

- **Prompt Rollback**: 자동화 에이전트 프롬프트를 직전 안정 버전으로 되돌린다.
- **Model Fallback**: 정책 평가 실패 시 보수적 모델/규칙셋으로 전환한다.
- **Tool Disable / Revoke**: Connector 변경 권한을 일시적으로 차단한다.
- **Eval Re-run**: 복구 완료 후 정책 위반 시나리오를 재검증한다.
- **Trace Capture**: 에이전트 실행 추적과 승인 이벤트를 Incident에 첨부한다.

## Evidence

- Capture command output, timestamps, and operator/agent actions for any execution of this runbook.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/07-workflow/airbyte.md)
- [Operations policy](../../policies/07-workflow/airbyte.md)
