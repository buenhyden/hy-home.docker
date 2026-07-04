<!-- README Target: docs/05.operations/runbooks/06-observability/README.md -->

# Operations Runbooks - 06 Observability

> 복구, 검증, 반복 실행 절차를 명령과 evidence 중심으로 관리한다.

## Overview

`runbooks/06-observability`는 current observability services의 readiness, route, ingestion, alerting, and storage evidence 절차를 관리합니다. 런북은 검증 가능한 최소 조치와 escalation boundary를 제공하고 guide/policy 내용을 중복하지 않습니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 장애 복구, 정기 점검, rollback, escalation, evidence capture
- 현재 경로에 속한 runbook 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 배경 설명 중심 가이드와 장기 운영 정책
- 다른 bucket 또는 다른 stage가 담당하는 운영 지식
- secret 값, credential, token, 인증서 원문

## Structure

```text
runbooks/06-observability/
├── alertmanager.md
├── alloy.md
├── grafana.md
├── loki.md
├── optimization-hardening.md
├── prometheus.md
├── pushgateway.md
├── pyroscope.md
├── tempo.md
└── README.md
```

## How to Work in This Area

1. 문서 추가, 이동, 삭제 시 이 README와 관련 bucket README를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [alertmanager.md](./alertmanager.md) | Alertmanager readiness and notification evidence procedure |
| [alloy.md](./alloy.md) | Alloy pipeline health and OTLP evidence procedure |
| [grafana.md](./grafana.md) | Grafana SSO, datasource, and dashboard evidence procedure |
| [loki.md](./loki.md) | Loki readiness and MinIO storage evidence procedure |
| [optimization-hardening.md](./optimization-hardening.md) | Gateway/route/health hardening recovery procedure |
| [prometheus.md](./prometheus.md) | Prometheus readiness, scrape, alert rule, reload, restart, and TSDB symptom evidence procedure |
| [pushgateway.md](./pushgateway.md) | Pushgateway stale metric evidence and cleanup boundary procedure |
| [pyroscope.md](./pyroscope.md) | Pyroscope readiness and local storage evidence procedure |
| [tempo.md](./tempo.md) | Tempo readiness and trace storage evidence procedure |

## Related Documents

- [Operations index](../../README.md)
- [Operations Runbooks index](../README.md)
- [Operations Guides - 06-observability](../../guides/06-observability/README.md)
- [Operations Policies - 06-observability](../../policies/06-observability/README.md)
- [Incident records](../../incidents/README.md)
