# postgresql-cluster

> Patroni 및 etcd를 이용한 고가용성(HA) PostgreSQL 17 관계형 데이터베이스 클러스터

## Overview

`postgresql-cluster`는 지속성과 가용성이 핵심인 서비스들을 위한 관계형 데이터베이스 인프라입니다. Spilo(Zalando) 이미지를 기반으로 Patroni가 클러스터 생명주기를 관리하며, etcd를 DCS(Distributed Configuration Store)로 사용하여 리더 선출 및 장애 복구를 자동화합니다. HAProxy(`pg-router`)를 통해 애플리케이션에 단일 접속 지점 및 읽기/쓰기 분산 기능을 제공합니다.

## Audience

이 README의 주요 독자:

- 데이터베이스 연결이 필요한 **Developers**
- 클러스터 상태 및 백업을 관리하는 **Operators**
- 인프라 무결성을 확인하는 **AI Agents**

## Scope

### In Scope

- 3노드 PostgreSQL 하드웨어/소프트웨어 스택 구성
- etcd 기반의 분산 설정 및 리더 락(Leader Lock) 관리
- HAProxy 기반의 읽기(15433)/쓰기(15432) 가용성 라우팅
- Prometheus 엑스포터를 통한 노드 및 클러스터 메트릭 노출

### Out of Scope

- 개별 서비스 애플리케이션의 데이터 스네마(Schema) 정의
- 외부망 직접 노출 (반드시 `infra_net` 내부망 사용)
- 클러스터 외부 수동 백업 저장소 관리

## Structure

```text
postgresql-cluster/
├── config/
│   └── haproxy.cfg           # HAProxy 라우팅 설정
├── init-scripts/
│   └── init_users_dbs.sql    # 초기 데이터베이스 및 사용자 생성 스크립트
├── scripts/
│   └── spilo-entrypoint.sh   # Spilo 엔트리포인트 래퍼
├── docker-compose.yml        # 클러스터 오케스트레이션 정의
└── README.md                 # This file
```

## How to Work in This Area

1. 클러스터 아키텍처 및 연결 방법은 [Technical Guide](../../../../docs/07.guides/04-data/relational.md)를 먼저 확인합니다.
2. 로컬 테스트를 위해 `docker compose up -d`를 실행한 후 `patronictl list`로 상태를 모니터링합니다.
3. 운영 변경 사항은 반드시 [Operations Policy](../../../../docs/08.operations/04-data/relational.md) 준수 여부를 확인합니다.
4. 장애 대응 절차는 [Recovery Runbook](../../../../docs/09.runbooks/04-data/relational.md)를 참조합니다.

## Available Scripts

| Command                               | Description               |
| ------------------------------------- | ------------------------- |
| `docker compose up -d`                | 클러스터 전체 스택 시작   |
| `patronictl list`                     | 클러스터 상태 및 역할 확인|
| `docker compose logs -f`              | 실시간 로그 모니터링      |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :--- | :--- |
| `SCOPE` | Yes | 클러스터 이름 (Default: `pg-ha`) |
| `PATRONI_SUPERUSER_USERNAME` | Yes | 슈퍼유저 계정명 (Default: `postgres`) |
| `ETCD3_HOSTS` | Yes | etcd 엔드포인트 리스트 |

## Getting Started

```bash
# 클러스터 및 데이터 저장소 시작
docker compose up -d

# 클러스터 상태 및 노드 역할(Leader/Replica) 확인
docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml list
```

## Related References

- **Guide**: [docs/07.guides/04-data/relational.md](../../../../docs/07.guides/04-data/relational.md)
- **Operations**: [docs/08.operations/04-data/relational.md](../../../../docs/08.operations/04-data/relational.md)
- **Runbook**: [docs/09.runbooks/04-data/relational.md](../../../../docs/09.runbooks/04-data/relational.md)
- **ARD**: [docs/02.ard/0004-data-architecture.md](../../../../docs/02.ard/0004-data-architecture.md)

---
Copyright (c) 2026. Licensed under the MIT License.
