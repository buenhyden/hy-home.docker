# Observability Operations Policy (06-observability)

> Telemetry Governance, Retention & Alerting Standards

## Overview

이 정책은 `hy-home.docker`의 가시성 데이터 보존 기간과 알림 기준을 정의한다.

## Data Retention Policy

저장 공간의 효율적 사용을 위해 다음의 보존 기간을 준수한다.

| Data Type | Storage Period | Backend | Notes |
| :--- | :--- | :--- | :--- |
| **Metrics** | 15 Days | Prometheus TSDB | Raw metrics |
| **Logs** | 7 Days | Loki (S3) | Application & Infra logs |
| **Traces** | 3 Days | Tempo (S3) | Distributed tracing spans |
| **Profiling** | 7 Days | Pyroscope | Continous profiling data |

## Alerting Standards

### 1. Alert Severity (심각도)

- **P0 (Critical)**: 시스템 다운, 즉각적 대응 필요. (Slack + E-mail)
- **P1 (Warning)**: 임계치 근접, 작업 시간 내 조사 필요. (Slack)
- **P2 (Info)**: 일시적 이상 징후, 트렌드 분석용. (Dashboard only)

### 2. Notification Rules

- 모든 알람은 `Alertmanager`를 통해 중앙에서 라우팅된다.
- 중복 알람 방지를 위해 `group_wait` 및 `group_interval` 설정을 주기적으로 튜닝한다.

## Maintenance Checklist

- [ ] MinIO `loki`, `tempo` 버킷 용량 모니터링.
- [ ] Grafana 대시보드 백업 및 버전 관리(Git).
- [ ] Alloy 콜렉터의 CPU/Memory 부하 점검.

## Related Documents

- [07. Guides](../../docs/07.guides/06-observability/README.md)
- [09. Runbooks](../../docs/09.runbooks/06-observability/README.md)
