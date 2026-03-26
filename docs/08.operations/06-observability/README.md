# Observability Operations Policy

> Telemetry Governance, Retention & Alerting Standards.

## Overview (KR)

이 정책은 `hy-home.docker`의 가시성 데이터 보존 기간(Retention)과 알림(Alerting) 기준을 정의한다. 시스템 안정성과 비용 효율성을 고려하여 데이터를 관리한다.

## Data Retention Policy

| Data Type | Storage Period | Backend | Notes |
| :--- | :--- | :--- | :--- |
| **Metrics** | 15 Days | Prometheus TSDB | Raw metrics |
| **Logs** | 7 Days | Loki (MinIO) | Application & Infra logs |
| **Traces** | 3 Days | Tempo (MinIO) | Distributed tracing spans |
| **Profiling** | 7 Days | Pyroscope | Continous profiling data |

## Alerting Standards

- **P0 (Critical)**: 시스템 다운, 즉각적 대응 필 (Slack + E-mail)
- **P1 (Warning)**: 임계치 근접, 작업 시간 내 조사 (Slack)
- **P2 (Info)**: 일시적 이상 징후, 트렌드 분석 (Dashboard)

## Related Documents

- **Guides**: `[../../07.guides/06-observability/README.md]`
- **Runbooks**: `[../../09.runbooks/06-observability/README.md]`
