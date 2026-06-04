<!-- README Target: docs/05.operations/runbooks/04-data/analytics/README.md -->

# Operations Runbooks - 04 Data / Analytics

> 복구, 검증, 반복 실행 절차를 명령과 evidence 중심으로 관리한다.

## Overview

`runbooks/04-data/analytics`는 InfluxDB, ksqlDB, OpenSearch, StarRocks 장애 대응 절차를 관리합니다. 각 runbook은 current compose service names와 검증 가능한 evidence를 우선 사용하고, 검증되지 않은 rollback/data mutation은 escalation으로 넘깁니다.

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
runbooks/04-data/analytics/
├── influxdb.md
├── ksqldb.md
├── opensearch.md
├── warehouses.md
└── README.md
```

## How to Work in This Area

1. 문서 추가, 이동, 삭제 시 이 README와 관련 bucket README를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [influxdb.md](./influxdb.md) | InfluxDB readiness and token mount recovery |
| [ksqldb.md](./ksqldb.md) | ksqlDB readiness and Kafka dependency recovery |
| [opensearch.md](./opensearch.md) | OpenSearch HTTPS health and variant recovery |
| [warehouses.md](./warehouses.md) | StarRocks FE/BE readiness and load boundary recovery |

## Related Documents

- [Operations index](../../../README.md)
- [Operations Runbooks index](../../README.md)
- [Operations Guides - 04-data / analytics](../../../guides/04-data/analytics/README.md)
- [Operations Policies - 04-data / analytics](../../../policies/04-data/analytics/README.md)
- [Incident records](../../../incidents/README.md)
