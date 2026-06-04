<!-- README Target: docs/05.operations/guides/04-data/relational/README.md -->

# Operations Guides - 04 Data / Relational

> PostgreSQL HA Cluster(Patroni/etcd/HAProxy) 사용 및 연결 가이드

## Overview

`guides/04-data/relational`는 `hy-home.docker` 인프라의 관계형 데이터베이스(`relational`) guide 문서를 관리한다. 현재는 선택 include인 PostgreSQL HA cluster의 service names, profiles, HAProxy endpoints, secret boundaries, 일반 점검, 관련 runbook handoff를 제공한다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- PostgreSQL HA 클러스터(Patroni/etcd/HAProxy) 구성 이해 및 연결 가이드
- 서비스 사용 맥락, 설정 방법, 온보딩, 일반 점검
- 현재 경로에 속한 guide 문서 인덱스

### Out of Scope

- 운영 통제 기준과 반복 실행 복구 절차
- 다른 bucket 또는 다른 stage가 담당하는 운영 지식
- secret 값, credential, token, 인증서 원문

## Architecture Overview

- **Patroni**: PostgreSQL 인스턴스의 생명주기를 관리하고 장애 시 자동 페일오버를 수행한다.
- **etcd**: 클러스터의 리더 선출 상태와 설정을 저장하는 DCS(Distributed Configuration Store) 역할을 한다.
- **HAProxy (pg-router)**: 애플리케이션의 접속 지점이며, 읽기/쓰기 트래픽을 분산한다.

### Connection Endpoints

| Endpoint Type | Host      | Port  | Notes                     |
| ------------- | --------- | ----- | ------------------------- |
| Master (RW)   | pg-router | 15432 | Primary Node Only         |
| Replica (RO)  | pg-router | 15433 | All Available Replicas    |
| HAProxy Stats | pg-router | 8404  | Read-only Stats Interface |

> 개별 노드(`pg-0`, `pg-1`, `pg-2`)에 직접 연결하면 페일오버 발생 시 가용성이 보장되지 않는다. 반드시 `pg-router`를 경유한다.

## Structure

```text
guides/04-data/relational/
├── postgresql-cluster.md
└── README.md
```

## How to Work in This Area

1. 문서 추가, 이동, 삭제 시 이 README와 관련 bucket README를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path                                             | Purpose                          |
| ------------------------------------------------ | -------------------------------- |
| [postgresql-cluster.md](./postgresql-cluster.md) | PostgreSQL HA cluster usage guide |

## Related Documents

- [Operations index](../../../README.md)
- [Operations Guides index](../../README.md)
- [Operations Policies - 04-data / relational](../../../policies/04-data/relational/README.md)
- [Operations Runbooks - 04-data / relational](../../../runbooks/04-data/relational/README.md)
- [Incident records](../../../incidents/README.md)
