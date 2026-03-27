# Relational Databases (04-data/relational)

> High-Availability Relational Database Clusters for Persistent Data

## Overview

이 디렉터리는 `hy-home.docker` 인프라의 관계형 데이터베이스(RDBMS) 계층을 관리합니다. 고가용성(HA), 데이터 정합성, 그리고 확장성을 보장하기 위해 Patroni와 etcd 기반의 클러스터 아키텍처를 표준으로 사용하며, HAProxy를 통해 애플리케이션에 안정적인 엔드포인트를 제공합니다.

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
├── postgresql-cluster/   # PostgreSQL HA Cluster (Patroni/etcd)
└── README.md             # This file
```

## How to Work in This Area

1. 서비스 요구사항에 맞는 데이터베이스 기술 가이드는 [Relational DB Guides](../../docs/07.guides/04-data/relational.md)를 참조합니다.
2. 새 클러스터 추가 시 `postgresql-cluster` 구조를 템플릿으로 활용합니다.
3. 운영 정책은 [Relational Operations](../../docs/08.operations/04-data/relational.md)를 반드시 준수해야 합니다.
4. 장애 대응 및 복구는 [Relational Runbooks](../../docs/09.runbooks/04-data/relational.md)를 따릅니다.

## Tech Stack

| Category   | Technology                                | Notes                     |
| ---------- | ----------------------------------------- | ------------------------- |
| DB Engine  | PostgreSQL 17 (Spilo)                     | Core Persistence          |
| HA Logic   | Patroni                                   | Cluster Lifecycle         |
| DCS        | etcd                                      | Distributed Locks         |
| Router     | HAProxy                                   | Traffic Distribution      |

## Getting Started

```bash
# 전체 관계형 데이터베이스 스택 시작
docker compose up -d
```

## Related References

- **Guide**: [docs/07.guides/04-data/relational.md](../../docs/07.guides/04-data/relational.md)
- **Operations**: [docs/08.operations/04-data/relational.md](../../docs/08.operations/04-data/relational.md)
- **Runbook**: [docs/09.runbooks/04-data/relational.md](../../docs/09.runbooks/04-data/relational.md)
- **ARD**: [docs/02.ard/0004-data-architecture.md](../../docs/02.ard/0004-data-architecture.md)

---
Copyright (c) 2026. Licensed under the MIT License.
