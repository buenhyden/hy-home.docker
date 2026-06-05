---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/nosql/couchdb.md -->

# CouchDB Usage Guide

## Usage

### Overview

이 문서는 `infra/04-data/nosql/couchdb/docker-compose.yml`에 정의된 CouchDB 3노드 클러스터 사용 기준을 설명한다. 현재 루트 compose에서는 CouchDB include가 주석 처리된 선택 서비스이며, 활성화 시 `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`가 `data` 프로파일과 `infra_net`에서 동작한다.

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

CouchDB HTTP API, cluster-init job, Traefik sticky routing, Docker Secret 기반 admin/cookie 설정을 현재 compose 이름과 맞춰 사용할 수 있게 한다.

### Prerequisites

- `infra/04-data/nosql/couchdb/docker-compose.yml`와 루트 [docker-compose.yml](../../../../../docker-compose.yml)의 선택 include 상태를 확인한다.
- `DEFAULT_DATA_DIR`, `DEFAULT_URL`, `COUCHDB_USERNAME`, `couchdb_password`, `couchdb_cookie`가 준비되어 있어야 한다.
- 로컬 점검은 가능하면 `couchdb-1` 내부에서 secret mount를 읽어 수행한다.

### Step-by-step Instructions

1. 서비스 구성을 렌더링한다.

   ```bash
   docker compose -f docker-compose.yml -f infra/04-data/nosql/couchdb/docker-compose.yml --profile data config
   ```

2. 클러스터와 init job 상태를 확인한다.

   ```bash
   docker compose ps couchdb-1 couchdb-2 couchdb-3 couchdb-cluster-init
   ```

3. 로컬 컨테이너 기준 health endpoint를 확인한다.

   ```bash
   docker exec couchdb-1 sh -lc 'COUCHDB_PASSWORD=$(cat /run/secrets/couchdb_password); curl -fsS "http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@localhost:${COUCHDB_PORT:-5984}/_up"'
   ```

4. membership은 primary route 또는 `couchdb-1` 내부에서 확인한다.

   ```bash
   docker exec couchdb-1 sh -lc 'COUCHDB_PASSWORD=$(cat /run/secrets/couchdb_password); curl -fsS "http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@localhost:${COUCHDB_PORT:-5984}/_membership"'
   ```

5. 외부 접근은 Traefik route `https://couchdb.${DEFAULT_URL}`와 sticky cookie 설정을 전제로 한다. 직접 host port publish는 현재 compose에 없다.

### Common Pitfalls

- 서비스명은 `couchdb-1`, `couchdb-2`, `couchdb-3`이다. 예전 node-style 이름을 현재 서비스명처럼 사용하지 않는다.
- Erlang cookie는 legacy shared-secret env var가 아니라 `/run/secrets/couchdb_cookie`에서 읽어 `ERL_FLAGS`에 주입된다.
- 클러스터 init은 `curlimages/curl:8.20.0` 기반 일회성 job이며, 반복 실패 시 재조인 절차를 임의로 실행하기 전에 runbook evidence를 남겨야 한다.

## Common Checks

- `docker compose -f docker-compose.yml -f infra/04-data/nosql/couchdb/docker-compose.yml --profile data config`
- `docker compose logs couchdb-cluster-init`
- `docker exec couchdb-1 sh -lc 'COUCHDB_PASSWORD=$(cat /run/secrets/couchdb_password); curl -fsS "http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@localhost:${COUCHDB_PORT:-5984}/_membership"'`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [CouchDB runbook](../../../runbooks/04-data/nosql/couchdb.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/nosql/couchdb.md)
- [Recovery runbook](../../../runbooks/04-data/nosql/couchdb.md)
- [Infra README](../../../../../infra/04-data/nosql/couchdb/README.md)
