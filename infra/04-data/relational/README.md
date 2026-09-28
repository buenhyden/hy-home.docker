---
title: "Relational Databases (04-data/relational)"
version: "1.0.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-03-27"
---

# Relational Databases (04-data/relational)

> 영속 데이터를 위한 고가용성 관계형 데이터베이스 클러스터입니다.

## Overview

이 디렉터리는 `hy-home.docker` 인프라의 관계형 데이터베이스(RDBMS) 계층을 관리한다. 루트 compose는 `postgresql-cluster` compose 파일을 무조건 include하며, 기동 여부는 선택한 profile이 결정한다. etcd, Patroni/PostgreSQL 노드, `pg-router`, exporter는 모두 `postgres-ha` profile에 속한다.

## Audience

이 README의 주요 독자:

- 데이터베이스 인프라를 프로비저닝하는 **DevOps Engineers**
- RDBMS 엔드포인트가 필요한 **Backend Developers**
- 클러스터 구성을 분석하는 **AI Agents**

## Scope

### In Scope

- PostgreSQL HA 클러스터 구성 및 관리 (`postgresql-cluster`)
- etcd 기반의 분산 설정 저장소(DCS) 통합
- HAProxy 기반의 읽기/쓰기 분산 라우터 구성
- 데이터베이스 초기화 및 사용자 권한 관리 스크립트

### Out of Scope

- NoSQL 데이터베이스 관리 (-> `04-data/nosql`)
- 인프라 외부의 원격 백업 저장소 관리
- 특정 서비스의 도메인 데이터 스키마 설계

## Structure

```text
relational/
├── postgresql-cluster/   # PostgreSQL HA Cluster(Patroni/etcd)
└── README.md             # 이 파일
```

## How to Work in This Area

| Package | Classification | Exact profile | Stage 05 subject |
| --- | --- | --- | --- |
| [PostgreSQL cluster](postgresql-cluster/README.md) | `LAB` | `postgres-ha` | `0031-postgresql-cluster` |

1. 서비스 요구사항에 맞는 데이터베이스 기술 가이드는 Relational DB Guides (`docs/05.operations/guides/README.md`)를 참조합니다.
2. 새 클러스터 추가 시 `postgresql-cluster` 구조를 템플릿으로 활용합니다.
3. 운영 정책은 Relational Policies (`docs/05.operations/policies/README.md`)를 반드시 준수해야 합니다.
4. 장애 대응 및 복구는 `docs/05.operations/guides/0031-postgresql-cluster.md`의 Guide/Policy/Runbook을 따릅니다.

## Available Scripts

| Command | Description |
| ------- | ----------- |
| `docker compose --env-file .env.example --profile postgres-ha config --quiet` | 선택 클러스터 compose 렌더링 |
| `docker compose ps` | 서비스 상태 확인 |
| `docker compose logs --tail=120 pg-router pg-0 pg-1 pg-2` | 핵심 서비스 로그 확인 |

## Tech Stack

실행 이미지와 init job 선언의 원본은 [postgresql-cluster/](postgresql-cluster/)의
compose 파일입니다.

| Category   | Technology                                | Notes                     |
| ---------- | ----------------------------------------- | ------------------------- |
| DB Engine  | Spilo                                     | Patroni/PostgreSQL 노드  |
| HA Logic   | Patroni                                   | 클러스터 생명주기         |
| DCS        | etcd(Compose 소스)                        | 분산 lock                |
| Router     | HAProxy(Compose 소스)                     | 트래픽 분산               |
| Init Job   | postgresql-cluster 자신의 compose         | Role/database 동기화      |

## Getting Started

```bash
docker compose --env-file .env.example --profile postgres-ha config --quiet
```

## Related Documents

- **Guides**: `docs/05.operations/guides/README.md`
- **Policies**: `docs/05.operations/policies/README.md`
- **Service Guide**: postgresql-cluster Guide/Policy/Runbook (`docs/05.operations/guides/0031-postgresql-cluster.md`)
- **ARD**: `docs/02.architecture/descriptions/0004-data-architecture.md`
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [derived Compose 이미지 투영](../../tech-stack.versions.json)은 drift를 검증합니다.
