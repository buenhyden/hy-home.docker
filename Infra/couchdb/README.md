# CouchDB Cluster Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 3개의 노드(`couchdb-1`, `couchdb-2`, `couchdb-3`)로 구성된 CouchDB 클러스터를 정의합니다. Traefik을 통해 로드밸런싱되며, Sticky Session이 설정되어 있어 데이터 일관성을 유지합니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **couchdb-1, 2, 3** | Database Node | CouchDB 클러스터의 각 노드입니다. |
| **couchdb-cluster-init** | Initializer | 컨테이너 시작 시 자동으로 노드들을 서로 연결하고 클러스터를 구성하는 스크립트 실행 컨테이너입니다. |

## 3. 구성 및 설정 (Configuration)

### 클러스터 구성
- **Nodes**: 3 Node Cluster
- **Cluster Setup**: `couchdb-cluster-init` 컨테이너가 `curl` 명령어를 통해 각 노드의 `_cluster_setup` 엔드포인트를 호출하여 클러스터를 자동 구성합니다.
- **Port**: 내부적으로 `5984` (HTTP), `4369` (Erlang Mapper), `9100` (Erlang Distribution) 포트를 사용합니다.

### 로드밸런싱 (Traefik)
- **URL**: `https://couchdb.${DEFAULT_URL}` (라운드 로빈 + Sticky Session)
- **Sticky Session**: `couchdb_sticky` 쿠키를 사용하여 클라이언트가 동일한 노드에 지속적으로 연결되도록 보장합니다.

### 데이터 볼륨
- `couchdb1-data`, `couchdb2-data`, `couchdb3-data`: 각 노드의 데이터 영속성을 위한 볼륨

### 환경 변수
- `COUCHDB_USER`, `COUCHDB_PASSWORD`: 관리자 계정
- `COUCHDB_COOKIE`: 클러스터 노드 간 통신 인증을 위한 Erlang 쿠키
