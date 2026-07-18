<!-- README Target: docs/05.operations/guides/04-data/analytics/README.md -->

# Operations Guides - 04 Data / Analytics

> 서비스 사용, 설정, 온보딩 문서를 domain/service 구조로 관리한다.

## Overview

`guides/04-data/analytics`는 InfluxDB, ksqlDB, OpenSearch, StarRocks guide 문서를 관리합니다. 각 guide는 현재 tracked compose의 service/profile/secret/volume 경계를 설명하고, 반복 복구 절차는 runbook으로 handoff합니다.

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
guides/04-data/analytics/
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
| [influxdb.md](./influxdb.md) | InfluxDB 3 Core database/line-protocol source contract and runtime token-provisioning boundary |
| [ksqldb.md](./ksqldb.md) | ksqlDB server/CLI/datagen profile guide |
| [opensearch.md](./opensearch.md) | OpenSearch primary stack and optional cluster variant guide |
| [warehouses.md](./warehouses.md) | StarRocks FE/BE compose guide |

## Related Documents

- [Operations index](../../../README.md)
- [Operations Guides index](../../README.md)
- [Operations Policies - 04-data / analytics](../../../policies/04-data/analytics/README.md)
- [Operations Runbooks - 04-data / analytics](../../../runbooks/04-data/analytics/README.md)
- [Incident records](../../../incidents/README.md)
