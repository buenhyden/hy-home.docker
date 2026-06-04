<!-- README Target: docs/05.operations/guides/06-observability/README.md -->

# Operations Guides - 06 Observability

> 서비스 사용, 설정, 온보딩 문서를 domain/service 구조로 관리한다.

## Overview

`guides/06-observability`는 Prometheus, Loki, Tempo, Alloy, Grafana, cAdvisor, Pyroscope, Alertmanager, Pushgateway guide 문서를 관리합니다. 각 guide는 현재 compose service/profile/route/storage 경계를 설명하고 반복 복구 절차는 runbook으로 handoff합니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 서비스 사용 맥락, 설정 방법, 온보딩, 일반 점검
- 현재 경로에 속한 guide 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 운영 통제 기준과 반복 실행 복구 절차
- 다른 bucket 또는 다른 stage가 담당하는 운영 지식
- secret 값, credential, token, 인증서 원문

## Structure

```text
guides/06-observability/
├── 01.lgtm-stack.md
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
3. Prometheus scrape 대상이나 exporter 버전 계열을 언급할 때는 현재 `infra/**/docker-compose*.yml` 이미지 계열과 맞춥니다.

## Contents

| Path | Purpose |
| --- | --- |
| [01.lgtm-stack.md](./01.lgtm-stack.md) | Current LGTM/Alloy/alerting/profiling stack guide |
| [alertmanager.md](./alertmanager.md) | Alertmanager Slack/SMTP routing guide |
| [alloy.md](./alloy.md) | Alloy Docker log, OTLP, Prometheus, and Pyroscope pipeline guide |
| [grafana.md](./grafana.md) | Grafana SSO, datasource, and dashboard provisioning guide |
| [loki.md](./loki.md) | Loki MinIO-backed log aggregation guide |
| [optimization-hardening.md](./optimization-hardening.md) | Gateway, health, route, and validation hardening guide |
| [prometheus.md](./prometheus.md) | Prometheus scrape, TSDB, and alert rule guide |
| [pushgateway.md](./pushgateway.md) | Pushgateway ephemeral metrics guide |
| [pyroscope.md](./pyroscope.md) | Pyroscope local profiling guide |
| [tempo.md](./tempo.md) | Tempo MinIO-backed tracing and span metrics guide |

## Related Documents

- [Operations index](../../README.md)
- [Operations Guides index](../README.md)
- [Operations Policies - 06-observability](../../policies/06-observability/README.md)
- [Operations Runbooks - 06-observability](../../runbooks/06-observability/README.md)
- [Incident records](../../incidents/README.md)
