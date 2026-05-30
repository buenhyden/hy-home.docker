<!-- README Target: docs/05.operations/runbooks/06-observability/README.md -->

# Operations Runbooks - 06 Observability

> 복구, 검증, 반복 실행 절차를 명령과 evidence 중심으로 관리한다.

## Overview

`runbooks/06-observability`는 `docs/05.operations`의 runbook 문서를 관리합니다. 트리거 조건, 순서 있는 절차, evidence, rollback/recovery, escalation을 제공한다. guide, policy, runbook 목적을 섞지 않고 필요한 운영 지식을 빠르게 찾도록 합니다.

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
├── prometheus-recovery.md
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
| [alertmanager.md](./alertmanager.md) | Alertmanager runbook 문서 |
| [alloy.md](./alloy.md) | Alloy runbook 문서 |
| [grafana.md](./grafana.md) | Grafana runbook 문서 |
| [loki.md](./loki.md) | Loki runbook 문서 |
| [optimization-hardening.md](./optimization-hardening.md) | Optimization Hardening runbook 문서 |
| [prometheus-recovery.md](./prometheus-recovery.md) | Prometheus Recovery runbook 문서 |
| [prometheus.md](./prometheus.md) | Prometheus runbook 문서 |
| [pushgateway.md](./pushgateway.md) | Pushgateway runbook 문서 |
| [pyroscope.md](./pyroscope.md) | Pyroscope runbook 문서 |
| [tempo.md](./tempo.md) | Tempo runbook 문서 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Runbooks index](../README.md)
- [Operations Guides - 06-observability](../../guides/06-observability/README.md)
- [Operations Policies - 06-observability](../../policies/06-observability/README.md)
- [Incident records](../../incidents/README.md)
