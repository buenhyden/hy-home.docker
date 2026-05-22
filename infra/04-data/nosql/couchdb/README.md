<!-- [ID:04-data:nosql:couchdb] -->
# CouchDB Cluster

> Document-oriented NoSQL database with HTTP API and robust sync.

## Overview

CouchDB는 데이터 동기화 및 복제에 특화된 문서 지향 NoSQL 데이터베이스이다. `hy-home.docker`에서는 멀티 마스터 복제 기능과 RESTful HTTP API가 필요한 애플리케이션 데이터를 위해 가용한 3-노드 클러스터 구성을 제공한다.

## Audience

이 README의 주요 독자:

- **Developers**: PouchDB 연동 및 HTTP API 사용
- **Operators**: 클러스터 정족수(Quorum) 관리 및 노드 복구
- **AI Agents**: 데이터 동기화 구조 분석 및 상태 점검

## Scope

### In Scope

- CouchDB 3.5 3-노드 클러스터 구성 (`couchdb-1, 2, 3`)
- 클러스터 자동 부트스트랩 자동화 (`couchdb-cluster-init`)
- Traefik 기반 Sticky Session 부하 분산
- 영속성 데이터 볼륨 관리 (`${DEFAULT_DATA_DIR}/couchdb/data-{1,2,3}`)

### Out of Scope

- 단일 노드 비클러스터 구성
- 외부 네트워크 직접 노출 (Traefik Proxy 필수)
- 애플리케이션 데이터 샤딩 및 파티셔닝 상세 정책

## Tech Stack

| Category   | Technology                 | Notes                      |
| :--------- | :------------------------- | :------------------------- |
| Engine     | `couchdb:3.5.1`            | Cluster Nodes              |
| Init Job   | `curlimages/curl:8.18.0`   | Bootstrap Automation       |
| Proxy      | `traefik`                  | HTTP API & TLS Termination |
| Network    | `infra_net`                | Erlang Distribution        |

## Structure

```text
couchdb/
├── README.md             # This file
└── docker-compose.yml    # Cluster deployment file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | CouchDB Cluster service leaf in `04-data`; services: `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`; root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/nosql/couchdb/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `COUCHDB_USER`, `NODENAME`; profiles: `data` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/nosql/couchdb/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `couchdb1-data:/opt/couchdb/data:rw`, `couchdb2-data:/opt/couchdb/data:rw`, `couchdb3-data:/opt/couchdb/data:rw`, `couchdb1-data`, `couchdb2-data`, `couchdb3-data` |
| Ports | `${COUCHDB_PORT:-5984}`, `${COUCHDB_ERLANG_MAPPER_PORT:-4369}`, `${COUCHDB_ERLANG_DISTRIBUTION_PORT:-9100}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.couchdb.rule`, `traefik.http.routers.couchdb.entrypoints`, `traefik.http.routers.couchdb.tls`, `traefik.http.routers.couchdb.service`, `traefik.http.routers.couchdb.middlewares`, `traefik.http.services.couchdb-cluster.loadbalancer.server.port`, plus 2 more |
| Secret refs | names: `couchdb_password`, `couchdb_cookie`; mounts: `/run/secrets/couchdb_password`, `/run/secrets/couchdb_cookie` |
| Healthcheck | Compose healthcheck declared for `couchdb-1`, `couchdb-2`, `couchdb-3`; not declared for `couchdb-cluster-init` |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/nosql/couchdb.md), [Policy](../../../../docs/05.operations/policies/04-data/nosql/couchdb.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/nosql/couchdb.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. **Deployment**: `docker compose up -d`를 사용하여 전체 클러스터와 초기화 작업을 기동한다.
2. **Bootstrapping**: 초기 실행 시 `couchdb-cluster-init` 컨테이너가 노드 조인 및 기본 DB 생성을 자동 수행한다.
3. **Verification**: `https://couchdb.${DEFAULT_URL}/_up` 경로를 통해 클러스터 상태를 확인한다.
4. **Consistency**: 정족수 유지를 위해 항상 홀수 개의 노드(최소 3개)를 유지해야 한다.

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose up -d` | CouchDB 클러스터 스택 배포 |
| `docker compose logs -f couchdb-cluster-init` | 클러스터 초기화 로그 확인 |
| `curl -u ${USER}:${PASS} http://couchdb-1:5984/_membership` | 클러스터 멤버십 확인 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `DEFAULT_DATA_DIR` | Yes | 호스트 시스템의 데이터 저장 루트 경로 |
| `COUCHDB_USERNAME` | Yes | 관리자 계정 이름 |
| `COUCHDB_PORT` | No | HTTP API 포트 (Default: 5984) |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect CouchDB.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking CouchDB documentation ready.

## Troubleshooting

- Start with `docker compose config` to confirm CouchDB network, volume, and secret references render.
- Check CouchDB logs and the linked runbook before changing clustering, cookie, or admin-secret settings.

## Related Documents

- **Guide**: [CouchDB Guide](../../../../docs/05.operations/guides/04-data/nosql/couchdb.md)
- **Operation**: [CouchDB Operation](../../../../docs/05.operations/guides/04-data/nosql/couchdb.md)
- **Runbook**: [CouchDB Runbook](../../../../docs/05.operations/guides/04-data/nosql/couchdb.md)

---
Copyright (c) 2026. Licensed under the MIT License.
