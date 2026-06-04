<!-- README Target: docs/05.operations/policies/06-observability/README.md -->

# Operations Policies - 06 Observability

> 운영 통제, 보안/가용성 기준, 예외 승인 기준을 관리한다.

## Overview

`policies/06-observability`는 current observability compose와 config가 선언한 route, storage, secret, retention, and validation controls를 관리합니다. 각 policy는 Required/Allowed/Disallowed 상태를 guide/runbook 절차와 분리해 정의합니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 운영 controls, allowed/disallowed 상태, exception, review cadence
- 현재 경로에 속한 policy 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 사용 온보딩과 명령 순서 중심 복구 절차
- 다른 bucket 또는 다른 stage가 담당하는 운영 지식
- secret 값, credential, token, 인증서 원문

## Structure

```text
policies/06-observability/
├── 01.retention.md
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
| [01.retention.md](./01.retention.md) | Retention controls for Prometheus/Loki/Tempo/Pyroscope |
| [alertmanager.md](./alertmanager.md) | Alertmanager routing and secret boundary policy |
| [alloy.md](./alloy.md) | Alloy pipeline and Docker socket boundary policy |
| [grafana.md](./grafana.md) | Grafana SSO, datasource, and provisioning policy |
| [loki.md](./loki.md) | Loki MinIO storage and label cardinality policy |
| [optimization-hardening.md](./optimization-hardening.md) | Observability gateway, health, route, and CI validation policy |
| [prometheus.md](./prometheus.md) | Prometheus scrape and alert rule policy |
| [pushgateway.md](./pushgateway.md) | Pushgateway stale metrics policy |
| [pyroscope.md](./pyroscope.md) | Pyroscope local storage and profiling overhead policy |
| [tempo.md](./tempo.md) | Tempo trace storage and metrics generator policy |

## Related Documents

- [Operations index](../../README.md)
- [Operations Policies index](../README.md)
- [Operations Guides - 06-observability](../../guides/06-observability/README.md)
- [Operations Runbooks - 06-observability](../../runbooks/06-observability/README.md)
- [Incident records](../../incidents/README.md)
