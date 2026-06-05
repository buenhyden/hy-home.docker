---
status: active
---
<!-- Target: docs/05.operations/runbooks/05-messaging/rabbitmq.md -->

# RabbitMQ Runbook

## Overview

이 런북은 RabbitMQ 서비스 장애 시 비파괴 점검, evidence capture, 서비스 재시작, escalation 절차를 정의한다. Queue purge/delete/rebind 같은 메시지 손실 가능 작업은 일반 복구 단계가 아니라 승인된 escalation으로만 처리한다.

## RabbitMQ Recovery Procedure

> Scope: Emergency procedures for RabbitMQ service failures.

---

### Purpose

- RabbitMQ service health와 queue backlog 상태를 빠르게 확인한다.
- secret 값을 노출하지 않고 evidence를 캡처한다.
- 비파괴 재시작으로 복구 가능한 장애와 데이터 영향 조치가 필요한 장애를 분리한다.

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
   - 메모리 소모가 심한 큐와 connection을 식별한다.
   - 연결 강제 종료가 필요하면 영향 connection, owner, 승인자를 evidence에 기록한 뒤 실행한다.
   - Queue purge/delete는 메시지 손실 가능 작업이므로 이 단계에서 실행하지 않고 `## Escalation`으로 전환한다.

3. **High CPU / Message Backlog (메처리 지연 시)**
   - Consumer 수 확인 및 확장 검토.
   - 메시지 처리 로직의 병목 지점(DB connection, external API call 등) 확인.
   - `x-max-priority` 설정이 있는 큐의 우선순위 처리 상태를 점검.

### Verification Steps

- [ ] `docker exec rabbitmq rabbitmq-diagnostics -q check_running`: 서비스 정상 실행 확인.
- [ ] `docker exec rabbitmq rabbitmqctl status`: 메모리 및 디스크 알람 해제 여부 확인.
- [ ] 웹 콘솔 (`https://rabbitmq.${DEFAULT_URL}`) 접속 및 대시보드 정상 출력 확인.

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Safe Rollback or Recovery Procedure

- [ ] compose 또는 route 변경 직후 발생한 장애라면 변경 전후 diff와 root profile render를 비교한다.
- [ ] 비파괴 복구는 `docker compose restart rabbitmq`와 health 재검증으로 제한한다.
- [ ] Queue contents, definition import/export, vhost/user permission mutation은 별도 승인 절차로 분리한다.

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

N/A - no verified generic RabbitMQ data rollback procedure is documented yet. Use this runbook for inspection, evidence capture, and non-destructive restart only. Escalate before queue purge/delete, definition import/export, vhost/user mutation, or message replay.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/05-messaging/rabbitmq.md)
- [Operations policy](../../policies/05-messaging/rabbitmq.md)
