---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/nosql/mongodb.md -->

# MongoDB Usage Guide

## Usage

### Overview

이 문서는 `infra/04-data/nosql/mongodb/docker-compose.yml`에 정의된 MongoDB replica set 사용 기준을 설명한다. 현재 루트 compose에서는 MongoDB include가 주석 처리된 선택 서비스이며, 활성화 시 `mongo-key-generator`, `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter`가 `data`/`obs` 프로파일과 `infra_net`에서 동작한다.

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

MongoDB replica set의 서비스명, keyfile volume, init job, Mongo Express route, exporter 경계를 현재 compose와 맞춰 사용하도록 한다.

### Prerequisites

- `infra/04-data/nosql/mongodb/docker-compose.yml`와 루트 [docker-compose.yml](../../../../../docker-compose.yml)의 선택 include 상태를 확인한다.
- `MONGODB_ROOT_USERNAME`, `MONGO_EXPRESS_CONFIG_BASICAUTH_USERNAME`, `mongodb_root_password`, `mongo_express_basicauth_password`가 준비되어 있어야 한다.
- replica set 이름은 compose command에 고정된 `MyReplicaSet` 기준이다. 현재 구현에는 별도 replica-set-name 환경 변수가 없다.

### Step-by-step Instructions

1. 서비스 구성을 렌더링한다.

   ```bash
   docker compose -f docker-compose.yml -f infra/04-data/nosql/mongodb/docker-compose.yml --profile data --profile obs config
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

5. 관리 UI는 `mongo-express`가 제공하며 Traefik route `https://mongo-express.${DEFAULT_URL}`를 사용한다. 직접 host port publish는 현재 compose에 없다.

### Common Pitfalls

- `mongodb-arbiter`는 투표 전용 구성원이다. 데이터 보관 노드로 설명하거나 백업 대상으로 취급하지 않는다.
- keyfile은 `mongo-key-generator`가 `mongo-key` named volume에 생성한다. repository 경로의 `configdb/` 디렉터리를 전제로 하지 않는다.
- `mongodb-rep1`과 `mongodb-rep2`에만 compose healthcheck가 있다. `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter`의 readiness는 logs와 dependency 상태로 확인한다.

## Common Checks

- `docker compose -f docker-compose.yml -f infra/04-data/nosql/mongodb/docker-compose.yml --profile data --profile obs config`
- `docker compose logs mongo-init`
- `docker exec mongodb-rep1 sh -lc 'MONGO_ROOT_PASSWORD=$(cat /run/secrets/mongodb_root_password | tr -d "\n"); mongosh -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_ROOT_PASSWORD" --authenticationDatabase admin --eval "rs.status().members.map(m => ({name:m.name,state:m.stateStr}))"'`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [MongoDB runbook](../../../runbooks/04-data/nosql/mongodb.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/nosql/mongodb.md)
- [Recovery runbook](../../../runbooks/04-data/nosql/mongodb.md)
- [Infra README](../../../../../infra/04-data/nosql/mongodb/README.md)
