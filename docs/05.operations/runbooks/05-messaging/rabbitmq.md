---
status: active
---
<!-- Target: docs/05.operations/runbooks/05-messaging/rabbitmq.md -->

# RabbitMQ Runbook

## Overview (KR)

이 런북은 RabbitMQ 서비스 장애 시 장애 복구 절차를 정의한다. 메시지 누적(Message Backlog), 메모리 부족(Memory Alarm), 서비스 응답 없음 등의 상황에서 즉각적인 복구 단계를 제공한다.

## RabbitMQ Recovery Procedure

> Scope: Emergency procedures for RabbitMQ service failures.

---

### Purpose

- RabbitMQ 메시지 처리 성능 회복
- 장애 노드 복구 및 데이터 정합성 유지
- 메시지 폭주 상황에서의 시스템 보호

### Canonical References

- [../../../../infra/05-messaging/rabbitmq/README.md](../../../../infra/05-messaging/rabbitmq/README.md)
- [../../policies/05-messaging/rabbitmq.md](../../policies/05-messaging/rabbitmq.md)

## When to Use

- "Message Backlog": 큐에 메시지가 수만 개 이상 쌓여 처리가 지연될 때.
- "Memory Alarm": RabbitMQ가 메모리 부족으로 인해 퍼블리셔 차단 상태일 때.
- "Service Down": 컨테이너 장애로 인해 서비스에 접속할 수 없을 때.

## Procedure

### Checklist

- [ ] RabbitMQ Management UI 접속 가능 여부 확인.
- [ ] `docker exec rabbitmq rabbitmqctl list_queues` 명령으로 큐 상태 확인.

### Steps

1. **Service Downtime (서비스 중단 시)**
   - 컨테이너 상태 확인: `docker compose ps rabbitmq`
   - 로그 확인: `docker compose logs -f rabbitmq`
   - 서비스 재시작: `docker compose restart rabbitmq`

2. **Memory Alarm (메모리 경고 시)**
   - 메모리 소모가 심한 큐 식별.
   - 불필요한 연결 강제 종료: UI 또는 `rabbitmqctl close_connection [connection-name]`
   - 중요도가 낮은 큐의 메시지 퍼지(Purge) 검토: `rabbitmqctl purge_queue [queue-name]`

3. **High CPU / Message Backlog (메처리 지연 시)**
   - Consumer 수 확인 및 확장 검토.
   - 메시지 처리 로직의 병목 지점(DB connection, external API call 등) 확인.
   - `x-max-priority` 설정이 있는 큐의 우선순위 처리 상태 점색.

### Verification Steps

- [ ] `rabbitmq-diagnostics check_running`: 서비스 정상 실행 확인.
- [ ] `rabbitmqctl status`: 메모리 및 디스크 알람 해제 여부 확인.
- [ ] 웹 콘솔 (`https://rabbitmq.${DEFAULT_URL}`) 접속 및 대시보드 정상 출력 확인.

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

- [Operations index](../../README.md)
- [Usage guide](../../guides/05-messaging/rabbitmq.md)
- [Operations policy](../../policies/05-messaging/rabbitmq.md)
