---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/alloy.md -->

# Alloy Runbook

## Overview

이 런북은 `hy-home.docker`의 텔레메트리 수집 엔진인 Grafana Alloy의 장애 복구 절차를 정의한다. 데이터 수집 중단이나 파이프라인 지연 발생 시 신속하게 대응하기 위한 가이드라인이다.

## Alloy Recovery Procedure

> Incident Response and Recovery Procedures for the Telemetry Pipeline

---

### Procedure Type

`recovery | troubleshooting`

### Target Audience

- Operator
- SRE
- On-call Engineer

### Purpose

Alloy 서비스의 가용성을 유지하고, 텔레메트리 데이터 유실을 최소화하기 위한 복구 절차를 수행한다.

### Prerequisites

- [Alloy System Usage](../../guides/06-observability/alloy.md) 이해
- [Alloy Operational Policy](../../policies/06-observability/alloy.md) 숙지
- Docker Compose 권한 및 Alloy UI 접근 권한

### Step-by-step Instructions

#### 1. Service Restoration

Alloy 컨테이너가 중단되었거나 응답하지 않을 경우:

1. `docker compose ps alloy`로 상태 확인.
2. repository root에서 `docker compose --profile obs restart alloy` 실행.
3. `docker compose logs -f alloy`로 에러 메시지 확인.

#### 2. Pipeline Debugging (Alloy UI)

데이터 수집은 되지만 특정 레이블이 탈락하거나 전송되지 않을 경우:

1. `https://alloy.${DEFAULT_URL}`에 접속.
2. **Graph View**에서 빨간색으로 표시된 컴포넌트 식별.
3. 해당 컴포넌트를 클릭하여 구체적인 에러 메시지(예: `connection refused to loki`) 확인.

#### 3. Memory Exhaustion Mitigation

Alloy가 메모리 부족으로 재시작을 반복할 경우:

1. `config.alloy`에서 `otelcol.processor.batch`의 `send_batch_size`를 일시적으로 축소.
2. 사용량이 많은 `discovery.relabel` 규칙이 있는지 검토 및 최적화.

#### 4. OTLP Connectivity Fix

앱이 데이터를 전송하지 못할 경우:

1. 내부 네트워크에서 `nc -zv alloy 4317` (gRPC) 또는 `nc -zv alloy 4318` (HTTP)로 포트 오픈 여부 확인.
2. Alloy 컨테이너 로그에서 `otelcol.receiver.otlp` 초기화 에러 확인.

### Common Pitfalls

- **Stale Configuration**: `config.alloy` 수정 후 `restart`하지 않으면 변경 사항이 반영되지 않는다.
- **Docker Socket Disconnect**: 호스트의 `/var/run/docker.sock` 권한 문제로 discovery가 중단될 수 있다.

### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

## Procedure

### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

### Steps

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

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

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/alloy.md)
- [Operations policy](../../policies/06-observability/alloy.md)
