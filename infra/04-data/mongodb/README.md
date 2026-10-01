---
title: "MongoDB Replica Set"
version: "1.0.5"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2025-11-12"
---

<!-- [ID:04-data:nosql:mongodb] -->
# MongoDB Replica Set

> 고가용성과 replica set을 지원하는 문서 지향 NoSQL 데이터베이스입니다.

## Overview

MongoDB는 유연한 스키마와 고성능을 제공하는 문서 지향 NoSQL 데이터베이스이다. `hy-home.docker`에서는 가용성과 데이터 중복성을 보장하도록 Primary-Secondary-Arbiter 구조의 Replica Set을 구성하여 운영한다.

## Audience

이 README의 주요 독자:

- **Developers**: 문서 데이터 모델링 및 연결 문자열 구성 참조
- **Operators**: 레플리카 셋 상태 관리, 장애 조치 및 백업 수행
- **AI Agents**: 클러스터 상태 분석 및 인증 키 관리 자동화

## Scope

### In Scope

- MongoDB Replica Set 구성(`mongodb-rep1, 2` + `arbiter`, 정확한 버전은 `docker-compose.yml` 참조)
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
| Engine     | Compose에 선언된 MongoDB 이미지 | 핵심 데이터베이스 엔진     |
| Management | Compose에 선언된 mongo-express 이미지 | 웹 기반 GUI 관리 |
| Monitoring | Compose에 선언된 mongodb_exporter 이미지 | Prometheus 메트릭 |
| Security   | 내부 KeyFile 인증      | Replica Set 동기화|

## Structure

```text
mongodb/
├── README.md             # 이 파일
└── docker-compose.yml    # replica set 배포 파일
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `04-data`의 MongoDB Replica Set 서비스 leaf; 무조건 root include, profile로 선택됨; services: `mongo-key-generator`, `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter` |
| Config files | `docker-compose.yml` |
| Config values | 환경 키는 Compose가 소유함; 7개 서비스 모두의 exact profile: `mongodb` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/04-data/mongodb/docker-compose.yml` |
| Networks | `edge_net`, `lab_net`, `obs_net` |
| Volumes | `mongo-key:/data/configdb:rw`, `mongodb1-data:/data/db:rw`, `mongo-key:/data/configdb:ro`, `mongodb2-data:/data/db:rw`, `mongo-key`, `mongodb1-data`, `mongodb2-data`, `mongodb3-data` |
| Ports | `${MONGO_EXPRESS_PORT:-8081}`, `${MONGO_EXPORTER_PORT:-9216}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.mongo-express.rule`, `traefik.http.routers.mongo-express.entrypoints`, `traefik.http.routers.mongo-express.tls`, `traefik.http.services.mongo-express.loadbalancer.server.port`, `traefik.http.routers.mongo-express.middlewares` |
| Secret refs | names: `mongodb_root_password`, `mongo_express_basicauth_password`; mounts: `/run/secrets/mongodb_root_password`, `/run/secrets/mongo_express_basicauth_password` |
| Healthcheck | `mongodb-rep1`, `mongodb-rep2`에 Compose healthcheck 선언됨; `mongo-key-generator`, `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter`에는 선언되지 않음 |
| Operations | Guide (`docs/05.operations/guides/0027-mongodb.md`), Policy (`docs/05.operations/policies/0027-mongodb.md`), Runbook (`docs/05.operations/runbooks/0027-mongodb.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `docker compose config --quiet`부터 시작한 뒤 서비스 로그와 연결된 운영/runbook 증거를 확인함 |

## How to Work in This Area

1. **Deployment**: 루트 compose include 상태를 확인하고 `docker compose --profile mongodb config --quiet`로 렌더링한다. `mongo-key-generator`가 먼저 실행되어야 한다.
2. **Initialization**: 첫 기동 시 `mongo-init` 작업이 자동으로 레플리카 셋을 구성한다.
3. **Management**: `https://mongo-express.${DEFAULT_URL}`을 통해 데이터 조회 및 관리를 수행한다.
4. **Security**: `mongo-key` named volume의 `mongodb.key` 파일은 보안상 매우 중요하므로 공유/수정 시 주의한다.

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose --profile mongodb config --quiet` | MongoDB 선택 스택 렌더링 |
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

Classification은 `LAB`입니다. `MyReplicaSet`은 한 호스트에 데이터 보유
member 2개와 arbiter 1개를 둡니다. 복구는 데이터 보유 member에서 인증된
`mongodump --oplog`를 사용하고 새로운 호환 replica set에 `mongorestore
--oplogReplay`로 복원합니다. arbiter는 데이터 백업이 아닙니다. 소유
artifact는 `GDE-0027`, `POL-0027`, `RUN-0027`입니다.

- MongoDB에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- MongoDB 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.

## Troubleshooting

- 이 서비스 디렉터리에서 `docker compose config --quiet`로 replica set, Mongo Express, exporter, 네트워크, secret 참조가 정상 렌더링되는지 먼저 확인합니다.
- replica 초기화가 실패하면 `docker compose logs mongo-init`을 확인하고 keyfile이나 replica set 설정을 변경하기 전에 `docker exec -it mongodb-rep1 mongosh --eval "rs.status()"`가 예상된 member 상태를 보고하는지 확인합니다.

## Related Documents

- **Guide**: MongoDB Guide (`docs/05.operations/guides/0027-mongodb.md`)
- **Policy**: MongoDB Operation (`docs/05.operations/policies/0027-mongodb.md`)
- **Runbook**: MongoDB Runbook (`docs/05.operations/runbooks/0027-mongodb.md`)
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [derived Compose 이미지 투영](../../tech-stack.versions.json)으로 drift를 검증합니다.
