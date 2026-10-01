---
title: "CouchDB Cluster"
version: "1.0.4"
type: "common/package-readme"
status: "review"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2025-11-12"
---

<!-- [ID:04-data:nosql:couchdb] -->
# CouchDB Cluster

> HTTP API와 견고한 동기화를 갖춘 문서 지향 NoSQL 데이터베이스입니다.

## Overview

CouchDB는 데이터 동기화 및 복제에 특화된 문서 지향 NoSQL 데이터베이스이다. `hy-home.docker`에서는 멀티 마스터 복제 기능과 RESTful HTTP API가 필요한 애플리케이션 데이터를 위해 가용한 3-노드 클러스터를 구성한다.

## Audience

이 README의 주요 독자:

- **Developers**: PouchDB 연동 및 HTTP API 사용
- **Operators**: 클러스터 정족수(Quorum) 관리 및 노드 복구
- **AI Agents**: 데이터 동기화 구조 분석 및 상태 점검

## Scope

### In Scope

- CouchDB 3-노드 클러스터 구성(`couchdb-1, 2, 3`, 정확한 버전은 `docker-compose.yml` 참조)
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
| Engine     | Compose에 선언된 CouchDB 이미지 | Cluster 노드             |
| Init Job   | Compose에 선언된 curl 이미지    | 부트스트랩 자동화      |
| Proxy      | `traefik`                  | HTTP API와 TLS 종료 |
| Network    | `edge_net`, `lab_net` | Erlang distribution        |

## Structure

```text
couchdb/
├── README.md             # 이 파일
└── docker-compose.yml    # cluster 배포 파일
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `04-data`의 CouchDB Cluster 서비스 leaf; 무조건 root include, profile로 선택됨; services: `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `COUCHDB_USER`, `NODENAME`; profiles: `couchdb` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/04-data/couchdb/docker-compose.yml` |
| Networks | `edge_net`, `lab_net` |
| Volumes | `couchdb1-data:/opt/couchdb/data:rw`, `couchdb2-data:/opt/couchdb/data:rw`, `couchdb3-data:/opt/couchdb/data:rw`, `couchdb1-data`, `couchdb2-data`, `couchdb3-data` |
| Ports | `${COUCHDB_PORT:-5984}`, `${COUCHDB_ERLANG_MAPPER_PORT:-4369}`, `${COUCHDB_ERLANG_DISTRIBUTION_PORT:-9100}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.couchdb.rule`, `traefik.http.routers.couchdb.entrypoints`, `traefik.http.routers.couchdb.tls`, `traefik.http.routers.couchdb.service`, `traefik.http.routers.couchdb.middlewares`, `traefik.http.services.couchdb-cluster.loadbalancer.server.port` 등 2개 더 |
| Secret refs | names: `couchdb_password`, `couchdb_cookie`; mounts: `/run/secrets/couchdb_password`, `/run/secrets/couchdb_cookie` |
| Healthcheck | `couchdb-1`, `couchdb-2`, `couchdb-3`에 Compose healthcheck 선언됨; `couchdb-cluster-init`에는 선언되지 않음 |
| Operations | Guide (`docs/05.operations/guides/0026-couchdb.md`), Policy (`docs/05.operations/policies/0026-couchdb.md`), Runbook (`docs/05.operations/runbooks/0026-couchdb.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `docker compose config --quiet`부터 시작한 뒤 서비스 로그와 연결된 운영/runbook 증거를 확인함 |

## How to Work in This Area

1. **Deployment**: 루트 compose include 상태를 확인하고 `docker compose --profile couchdb config --quiet`로 렌더링한다.
2. **Bootstrapping**: 초기 실행 시 `couchdb-cluster-init` 컨테이너가 노드 조인 및 기본 DB 생성을 자동 수행한다.
3. **Verification**: `https://couchdb.${DEFAULT_URL}/_up` 경로를 통해 클러스터 상태를 확인한다.
4. **Consistency**: 정족수를 지키려면 항상 홀수 개의 노드(최소 3개)를 유지해야 한다.

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose --profile couchdb config --quiet` | CouchDB 선택 스택 렌더링 |
| `docker compose logs -f couchdb-cluster-init` | 클러스터 초기화 로그 확인 |
| `docker exec couchdb-1 sh -lc 'COUCHDB_PASSWORD=$(cat /run/secrets/couchdb_password); curl -fsS "http://${COUCHDB_USER}:${COUCHDB_PASSWORD}@localhost:${COUCHDB_PORT:-5984}/_membership"'` | Secret mount 기반 클러스터 멤버십 확인 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `DEFAULT_DATA_DIR` | Yes | 호스트 시스템의 데이터 저장 루트 경로 |
| `COUCHDB_USERNAME` | Yes | 관리자 계정 이름 |
| `COUCHDB_PORT` | No | HTTP API 포트 (Default: 5984) |
| `COUCHDB_ERLANG_MAPPER_PORT` | No | Erlang port mapper 포트 (Default: 4369) |
| `COUCHDB_ERLANG_DISTRIBUTION_PORT` | No | Erlang distribution 포트 (Default: 9100) |

## Validation

Classification은 `LAB`입니다. 한 호스트의 3개 member는 host-level HA를
제공하지 않습니다. 복구는 새로운 호환 cluster로 replication하는 방식을 우선합니다.
파일 복구는 configuration, `_dbs`, system database, shard, index를 포함한
정지된(quiesced) 일관 세트가 필요하며 index를 database 파일보다 먼저
복원해야 합니다. 소유 artifact는 `GDE-0026`, `POL-0026`, `RUN-0026`입니다.

- CouchDB에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- CouchDB 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.

## Troubleshooting

- `docker compose config --quiet`로 CouchDB 네트워크, volume, secret 참조가 정상 렌더링되는지 먼저 확인합니다.
- clustering, cookie, admin-secret 설정을 변경하기 전에 CouchDB 로그와 연결된 runbook을 확인합니다.

## Related Documents

- **Guide**: CouchDB Guide (`docs/05.operations/guides/0026-couchdb.md`)
- **Policy**: CouchDB Operation (`docs/05.operations/policies/0026-couchdb.md`)
- **Runbook**: CouchDB Runbook (`docs/05.operations/runbooks/0026-couchdb.md`)
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [derived Compose 이미지 투영](../../tech-stack.versions.json)으로 drift를 검증합니다.
