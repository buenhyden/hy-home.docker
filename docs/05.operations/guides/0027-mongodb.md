---
title: "MongoDB Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0027"
parent_ids:
- "POL-0027"
implementation_services:
  infra/04-data/nosql/mongodb/docker-compose.yml:
  - 'mongo-express'
  - 'mongo-init'
  - 'mongo-key-generator'
  - 'mongodb-arbiter'
  - 'mongodb-exporter'
  - 'mongodb-rep1'
  - 'mongodb-rep2'
created: "2026-05-10"
---

# MongoDB Usage Guide

## Usage

### Overview

이 문서는 [MongoDB Compose 구현](../../../infra/04-data/nosql/mongodb/docker-compose.yml)의 replica set 사용 기준을 설명한다. 일곱 서비스는 모두 정확히 `mongodb` profile과 선언된 network에서 동작한다. frozen classification은 `LAB`이고 두 data-bearing member와 arbiter가 한 host에 있으므로 host-level HA가 아니다.

### Current implementation

| Field | Repository-specific decision |
| --- | --- |
| Consumer and data rationale | No confirmed HOME consumer; LAB replica-set and document-database evaluation. |
| Source / updater | [Compose](../../../infra/04-data/nosql/mongodb/docker-compose.yml) owns image sources; dependency automation proposals require compatibility review. |
| Services / profile | Key generator, two data members, arbiter, init, UI, exporter; exact `mongodb`. |
| Flow / dependency | `mongo-init` creates `MyReplicaSet`; clients address both data members; arbiter votes without data. |
| Exposure / persistence | Mongo Express via Traefik; members internal; data/key named volumes. |
| Environment / secrets | Root/UI usernames are environment identifiers; root/UI passwords are Docker Secrets; keyfile is generated into `mongo-key`. |
| Health / resources | member healthchecks, `rs.status()`, init/exporter logs; data members extend `template-stateful-high`. |
| Security | internal keyfile authentication plus secret-backed root/UI passwords; same-host topology is not DR. |
| Backup / upgrade | `mongodump --oplog` and isolated `--oplogReplay`; require tool/server compatibility and restore evidence before upgrade/removal. |
| License / edition | MongoDB Community is governed by SSPL terms; this topology claims no Enterprise backup or management capability. |

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

MongoDB replica set의 서비스명, keyfile volume, init job, Mongo Express route, exporter 경계를 현재 compose와 맞춰 사용하도록 한다.

### Prerequisites

- 루트 [docker-compose.yml](../../../docker-compose.yml)는 MongoDB 파일을 include하며 모든 서비스의 정확한 profile은 `mongodb`다.
- `MONGODB_ROOT_USERNAME`, `MONGO_EXPRESS_CONFIG_BASICAUTH_USERNAME`, `mongodb_root_password`, `mongo_express_basicauth_password`가 준비되어 있어야 한다.
- replica set 이름은 compose command에 고정된 `MyReplicaSet` 기준이다. 현재 구현에는 별도 replica-set-name 환경 변수가 없다.

### Step-by-step Instructions

1. 서비스 구성을 렌더링한다.

   ```bash
   docker compose --profile mongodb config --quiet
   ```

2. init job과 replica member 상태를 확인한다.

   ```bash
   docker compose ps mongo-key-generator mongodb-rep1 mongodb-rep2 mongodb-arbiter mongo-init
   ```

3. replica set 상태는 `mongodb-rep1` 내부 secret mount를 사용해 확인한다.

   ```bash
   docker exec mongodb-rep1 sh -lc 'MONGO_ROOT_PASSWORD=$(cat /run/secrets/mongodb_root_password | tr -d "\n"); mongosh -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_ROOT_PASSWORD" --authenticationDatabase admin --eval "rs.status().ok"'
   ```

4. 애플리케이션 연결 문자열은 내부 서비스명을 포함한다.

   ```text
   mongodb://<user>:<password>@mongodb-rep1:27017,mongodb-rep2:27017/?replicaSet=MyReplicaSet&authSource=admin
   ```

5. 관리 UI는 `mongo-express`가 제공하며 Traefik route `https://mongo-express.${DEFAULT_URL}`를 사용한다. `ME_CONFIG_BASICAUTH=true`로 basic auth가 켜져 있어야 하며(mongo-express 1.x는 이 값 없이 자격 증명을 무시한다), 직접 host port publish는 현재 compose에 없다.

### Common Pitfalls

- `mongodb-arbiter`는 투표 전용 구성원이다. 데이터 보관 노드로 설명하거나 백업 대상으로 취급하지 않는다.
- keyfile은 `mongo-key-generator`가 `mongo-key` named volume에 생성한다. repository 경로의 `configdb/` 디렉터리를 전제로 하지 않는다.
- `mongodb-rep1`과 `mongodb-rep2`에만 compose healthcheck가 있다. `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter`의 readiness는 logs와 dependency 상태로 확인한다.
- replica-set backup은 primary에서 authenticated `mongodump --oplog`로 일관성을 잡고 `mongorestore --oplogReplay`로 빈 격리 replica set에 검증한다. arbiter는 data backup 대상이 아니다.

## Common Checks

- `docker compose --profile mongodb config --quiet`
- `docker compose logs mongo-init`
- `docker exec mongodb-rep1 sh -lc 'MONGO_ROOT_PASSWORD=$(cat /run/secrets/mongodb_root_password | tr -d "\n"); mongosh -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_ROOT_PASSWORD" --authenticationDatabase admin --eval "rs.status().members.map(m => ({name:m.name,state:m.stateStr}))"'`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [MongoDB runbook](../runbooks/0027-mongodb.md)을 따른다.

## Traceability

- Declared parent: [MongoDB Operations Policy](../policies/0027-mongodb.md) (`POL-0027`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Policy](../policies/0027-mongodb.md) (`POL-0027`), [Runbook](../runbooks/0027-mongodb.md) (`RUN-0027`)

## Related Documents

- [MongoDB backup and restore tools](https://www.mongodb.com/docs/v8.0/tutorial/backup-and-restore-tools/)
- [MongoDB security hardening](https://www.mongodb.com/docs/v8.0/core/security-hardening/)
- [MongoDB Community licensing](https://www.mongodb.com/legal/licensing/community-edition)

- [Operations index](../README.md)
- [Operations policy](../policies/0027-mongodb.md)
- [Recovery runbook](../runbooks/0027-mongodb.md)
- [Infra README](../../../infra/04-data/nosql/mongodb/README.md)
- [Compose implementation: infra/04-data/nosql/mongodb/docker-compose.yml](../../../infra/04-data/nosql/mongodb/docker-compose.yml)
