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

## Related References

- **Guide**: [CouchDB Guide](../../docs/07.guides/04-data/nosql/couchdb.md)
- **Operation**: [CouchDB Operation](../../docs/08.operations/04-data/nosql/couchdb.md)
- **Runbook**: [CouchDB Runbook](../../docs/09.runbooks/04-data/nosql/couchdb.md)

---
Copyright (c) 2026. Licensed under the MIT License.
