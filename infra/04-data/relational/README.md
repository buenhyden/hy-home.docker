# Relational Databases (04-data/relational)

> High-Availability Relational Database Clusters for Persistent Data

## Overview

이 디렉터리는 `hy-home.docker` 인프라의 관계형 데이터베이스(RDBMS) 계층을 관리한다. 현재 루트 compose에서는 `postgresql-cluster` include가 주석 처리된 선택 서비스이며, 필요 시 Patroni/etcd/PostgreSQL/HAProxy cluster compose를 명시적으로 포함해 실행한다.

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

1. 서비스 요구사항에 맞는 데이터베이스 기술 가이드는 [Relational DB Guides](../../../docs/05.operations/guides/04-data/relational/README.md)를 참조합니다.
2. 새 클러스터 추가 시 `postgresql-cluster` 구조를 템플릿으로 활용합니다.
3. 운영 정책은 [Relational Policies](../../../docs/05.operations/policies/04-data/relational/README.md)를 반드시 준수해야 합니다.
4. 장애 대응 및 복구는 [Relational Runbooks](../../../docs/05.operations/runbooks/04-data/relational/README.md)를 따릅니다.

## Available Scripts

| Command | Description |
| ------- | ----------- |
| `docker compose -f docker-compose.yml -f infra/04-data/relational/postgresql-cluster/docker-compose.yml --profile data --profile service config` | 선택 클러스터 compose 렌더링 |
| `docker compose ps` | 서비스 상태 확인 |
| `docker compose logs --tail=120 pg-router pg-0 pg-1 pg-2` | 핵심 서비스 로그 확인 |

## Tech Stack

| Category   | Technology                                | Notes                     |
| ---------- | ----------------------------------------- | ------------------------- |
| DB Engine  | `ghcr.io/zalando/spilo-17:4.0-p3`         | Patroni/PostgreSQL nodes  |
| HA Logic   | Patroni                                   | Cluster Lifecycle         |
| DCS        | etcd 3.6.12                               | Distributed Locks         |
| Router     | `haproxy:3.3.10`                          | Traffic Distribution      |
| Init Job   | `postgres:18.4-alpine`                    | Role/database sync        |

## Getting Started

```bash
docker compose -f docker-compose.yml -f infra/04-data/relational/postgresql-cluster/docker-compose.yml --profile data --profile service config
```

## Related Documents

- **Guides**: [docs/05.operations/guides/04-data/relational/README.md](../../../docs/05.operations/guides/04-data/relational/README.md)
- **Policies**: [docs/05.operations/policies/04-data/relational/README.md](../../../docs/05.operations/policies/04-data/relational/README.md)
- **Runbooks**: [docs/05.operations/runbooks/04-data/relational/README.md](../../../docs/05.operations/runbooks/04-data/relational/README.md)
- **Service Guide**: [postgresql-cluster guide](../../../docs/05.operations/guides/04-data/relational/postgresql-cluster.md)
- **ARD**: [docs/02.architecture/requirements/0004-data-architecture.md](../../../docs/02.architecture/requirements/0004-data-architecture.md)

---
Copyright (c) 2026. Licensed under the MIT License.
