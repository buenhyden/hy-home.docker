# Alloy Recovery Runbook

> Incident Response and Recovery Procedures for the Telemetry Pipeline

---

## Overview (KR)

이 런북은 `hy-home.docker`의 텔레메트리 수집 엔진인 Grafana Alloy의 장애 복구 절차를 정의한다. 데이터 수집 중단이나 파이프라인 지연 발생 시 신속하게 대응하기 위한 가이드라인이다.

## Runbook Type

`recovery | troubleshooting`

## Target Audience

- Operator
- SRE
- On-call Engineer

## Purpose

Alloy 서비스의 가용성을 유지하고, 텔레메트리 데이터 유실을 최소화하기 위한 복구 절차를 수행한다.

## Prerequisites

- [Alloy System Guide](../../07.guides/06-observability/alloy.md) 이해
- [Alloy Operational Policy](../../08.operations/06-observability/alloy.md) 숙지
- Docker Compose 권한 및 Alloy UI 접근 권한

## Step-by-step Instructions

### 1. Service Restoration

Alloy 컨테이너가 중단되었거나 응답하지 않을 경우:

1. `docker compose ps alloy`로 상태 확인.
2. `docker compose restart alloy` 실행.
3. `docker compose logs -f alloy`로 에러 메시지 확인.

### 2. Pipeline Debugging (Alloy UI)

데이터 수집은 되지만 특정 레이블이 탈락하거나 전송되지 않을 경우:

1. `https://alloy.${DEFAULT_URL}`에 접속.
2. **Graph View**에서 빨간색으로 표시된 컴포넌트 식별.
3. 해당 컴포넌트를 클릭하여 구체적인 에러 메시지(예: `connection refused to loki`) 확인.

### 3. Memory Exhaustion Mitigation

Alloy가 메모리 부족으로 재시작을 반복할 경우:

1. `config.alloy`에서 `otelcol.processor.batch`의 `send_batch_size`를 일시적으로 축소.
2. 사용량이 많은 `discovery.relabel` 규칙이 있는지 검토 및 최적화.

### 4. OTLP Connectivity Fix

앱이 데이터를 전송하지 못할 경우:

1. `nc -zv alloy 4317` (gRPC) 또는 `nc -zv alloy 4318` (HTTP)로 포트 오픈 여부 확인.
2. Alloy 컨테이너 로그에서 `otelcol.receiver.otlp` 초기화 에러 확인.

## Common Pitfalls

- **Stale Configuration**: `config.alloy` 수정 후 `restart`하지 않으면 변경 사항이 반영되지 않는다.
- **Docker Socket Disconnect**: 호스트의 `/var/run/docker.sock` 권한 문제로 discovery가 중단될 수 있다.

## Related Documents

- **Guide**: [../../07.guides/06-observability/alloy.md](../../07.guides/06-observability/alloy.md)
- **Operation**: [../../08.operations/06-observability/alloy.md](../../08.operations/06-observability/alloy.md)
- **Infrastructure**: [../../../infra/06-observability/alloy/README.md](../../../infra/06-observability/alloy/README.md)
