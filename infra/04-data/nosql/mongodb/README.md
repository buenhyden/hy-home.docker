<!-- [ID:04-data:nosql:mongodb] -->
# MongoDB Replica Set

> Document-oriented NoSQL database with high availability and replica set support.

## Overview

MongoDB는 유연한 스키마와 고성능을 제공하는 문서 지향 NoSQL 데이터베이스이다. `hy-home.docker`에서는 가용성과 데이터 중복성을 보장하기 위해 Primary-Secondary-Arbiter 구조의 Replica Set을 구성하여 운영한다.

## Audience

이 README의 주요 독자:

- **Developers**: 문서 데이터 모델링 및 연결 문자열 구성 참조
- **Operators**: 레플리카 셋 상태 관리, 장애 조치 및 백업 수행
- **AI Agents**: 클러스터 상태 분석 및 인증 키 관리 자동화

## Scope

### In Scope

- MongoDB 8.2 Replica Set 구성 (`mongodb-rep1, 2` + `arbiter`)
- 관리 도구: Mongo Express (Web UI)
- 성능 모니터링: MongoDB Exporter for Prometheus
- 보안 구성: KeyFile 기반 내부 인증 및 SCRAM-SHA-256

### Out of Scope

- Sharded Cluster (현재 Single Replica Set 기준)
- 외부 네트워크 직접 노출 (Traefik Proxy 필수)
- 아카이빙된 로그 보관 정책 (Centralized Logging Tier 담당)

## Tech Stack

| Category   | Technology                 | Notes                      |
| :--------- | :------------------------- | :------------------------- |
| Engine     | `mongo:8.2.3-noble`        | Core Database Engine       |
| Management | `mongo-express:1.0.2`      | Web-based GUI Admin        |
| Monitoring | `percona/mongodb_exporter` | Prometheus Metrics         |
| Security   | Internal KeyFile Auth      | Replica Set Synchronization|

## Structure

```text
mongodb/
├── README.md             # This file
├── docker-compose.yml    # Replica set deployment file
└── configdb/             # (Volume) Shared keys and configs
```

## How to Work in This Area

1. **Deployment**: `docker compose up -d`를 사용하여 전체 스택을 제어한다. `mongo-key-generator`가 먼저 실행되어야 한다.
2. **Initialization**: 첫 기동 시 `mongo-init` 작업이 자동으로 레플리카 셋을 구성한다.
3. **Management**: `https://mongo-express.${DEFAULT_URL}`을 통해 데이터 조회 및 관리를 수행한다.
4. **Security**: `configdb/` 아래의 `mongodb.key` 파일은 보안상 매우 중요하므로 공유/수정 시 주의한다.

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose up -d` | MongoDB 스택 전체 배포 |
| `docker exec -it mongodb-rep1 mongosh -u root` | Primary 노드 셸 접속 |
| `docker exec -it mongodb-rep1 mongosh --eval "rs.status()"` | 레플리카 셋 상태 확인 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `MONGODB_ROOT_USERNAME` | Yes | 전체 관리자 계정 이름 |
| `MONGO_EXPRESS_PORT` | No | UI 접속 포트 (Default: 8081) |
| `MONGODB_REPLICA_SET_NAME`| No | 레플리카 셋 명칭 (Default: MyReplicaSet) |

## Related References

- **Guide**: [MongoDB Guide](../../docs/07.guides/04-data/nosql/mongodb.md)
- **Operation**: [MongoDB Operation](../../docs/08.operations/04-data/nosql/mongodb.md)
- **Runbook**: [MongoDB Runbook](../../docs/09.runbooks/04-data/nosql/mongodb.md)

---
Copyright (c) 2026. Licensed under the MIT License.
