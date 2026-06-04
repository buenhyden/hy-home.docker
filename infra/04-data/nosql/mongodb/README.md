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
| Engine     | `mongo:8.2.9-noble`        | Core Database Engine       |
| Management | `mongo-express:1-18-alpine3.19` | Web-based GUI Admin |
| Monitoring | `percona/mongodb_exporter:2.37` | Prometheus Metrics |
| Security   | Internal KeyFile Auth      | Replica Set Synchronization|

## Structure

```text
mongodb/
├── README.md             # This file
└── docker-compose.yml    # Replica set deployment file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | MongoDB Replica Set service leaf in `04-data`; optional/commented root include; services: `mongo-key-generator`, `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `MONGO_INITDB_ROOT_USERNAME`, `MONGO_INITDB_ROOT_PASSWORD_FILE`, `ME_CONFIG_MONGODB_ENABLE_ADMIN`, `ME_CONFIG_MONGODB_AUTH_DATABASE`, `ME_CONFIG_MONGODB_ADMINUSERNAME`, `ME_CONFIG_MONGODB_ADMINPASSWORD_FILE`, `ME_CONFIG_MONGODB_SERVER`, `ME_CONFIG_MONGODB_REPLICA_SET`, plus 2 more; profiles: `data`, `obs` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/nosql/mongodb/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `mongo-key:/data/configdb:rw`, `mongodb1-data:/data/db:rw`, `mongo-key:/data/configdb:ro`, `mongodb2-data:/data/db:rw`, `mongo-key`, `mongodb1-data`, `mongodb2-data`, `mongodb3-data` |
| Ports | `${MONGO_EXPRESS_PORT:-8081}`, `${MONGO_EXPORTER_PORT:-9216}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.mongo-express.rule`, `traefik.http.routers.mongo-express.entrypoints`, `traefik.http.routers.mongo-express.tls`, `traefik.http.services.mongo-express.loadbalancer.server.port`, `traefik.http.routers.mongo-express.middlewares` |
| Secret refs | names: `mongodb_root_password`, `mongo_express_basicauth_password`; mounts: `/run/secrets/mongodb_root_password`, `/run/secrets/mongo_express_basicauth_password` |
| Healthcheck | Compose healthcheck declared for `mongodb-rep1`, `mongodb-rep2`; not declared for `mongo-key-generator`, `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter` |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/nosql/mongodb.md), [Policy](../../../../docs/05.operations/policies/04-data/nosql/mongodb.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/nosql/mongodb.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. **Deployment**: 루트 compose include 상태를 확인하고 `docker compose -f docker-compose.yml -f infra/04-data/nosql/mongodb/docker-compose.yml --profile data --profile obs config`로 렌더링한다. `mongo-key-generator`가 먼저 실행되어야 한다.
2. **Initialization**: 첫 기동 시 `mongo-init` 작업이 자동으로 레플리카 셋을 구성한다.
3. **Management**: `https://mongo-express.${DEFAULT_URL}`을 통해 데이터 조회 및 관리를 수행한다.
4. **Security**: `mongo-key` named volume의 `mongodb.key` 파일은 보안상 매우 중요하므로 공유/수정 시 주의한다.

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose -f docker-compose.yml -f infra/04-data/nosql/mongodb/docker-compose.yml --profile data --profile obs config` | MongoDB 선택 스택 렌더링 |
| `docker compose logs -f mongo-init` | 레플리카 셋 초기화 로그 확인 |
| `docker exec mongodb-rep1 sh -lc 'MONGO_ROOT_PASSWORD=$(cat /run/secrets/mongodb_root_password); mongosh -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_ROOT_PASSWORD" --authenticationDatabase admin --eval "rs.status().ok"'` | Secret mount 기반 레플리카 셋 상태 확인 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `MONGODB_ROOT_USERNAME` | Yes | 전체 관리자 계정 이름 |
| `MONGO_EXPRESS_PORT` | No | UI 접속 포트 (Default: 8081) |
| `MONGO_EXPORTER_PORT` | No | exporter 포트 (Default: 9216) |
| `MONGO_EXPRESS_CONFIG_BASICAUTH_USERNAME` | Yes | Mongo Express Basic Auth 사용자 이름 |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect MongoDB.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking MongoDB documentation ready.

## Troubleshooting

- Start with `docker compose config` from this service directory to verify replica set, Mongo Express, exporter, network, and secret references render.
- If replica initialization fails, inspect `docker compose logs mongo-init` and confirm `docker exec -it mongodb-rep1 mongosh --eval "rs.status()"` reports the expected member state before changing keyfile or replica set settings.

## Related Documents

- **Guide**: [MongoDB Guide](../../../../docs/05.operations/guides/04-data/nosql/mongodb.md)
- **Policy**: [MongoDB Operation](../../../../docs/05.operations/policies/04-data/nosql/mongodb.md)
- **Runbook**: [MongoDB Runbook](../../../../docs/05.operations/runbooks/04-data/nosql/mongodb.md)

---
Copyright (c) 2026. Licensed under the MIT License.
