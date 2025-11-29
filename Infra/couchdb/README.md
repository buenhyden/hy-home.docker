# Apache CouchDB Cluster

## 개요

이 디렉토리는 3노드 Apache CouchDB 클러스터를 실행하기 위한 Docker Compose 구성을 포함합니다. Traefik을 통한 로드 밸런싱과 Sticky Session을 지원하며, 자동 클러스터 초기화 기능을 포함합니다.

## 서비스

- **couchdb-1, couchdb-2, couchdb-3**: CouchDB 클러스터 노드.
- **couchdb-cluster-init**: 클러스터 조인 및 초기 설정을 수행하는 일회성 컨테이너.

## 필수 조건

- Docker 및 Docker Compose 설치.
- `Docker/Infra` 루트 디렉토리에 `.env` 파일.

## 설정

이 서비스는 다음 환경 변수(`.env`에 정의됨)를 사용합니다:

- `COUCHDB_USERNAME`, `COUCHDB_PASSWORD`: 관리자 자격 증명.
- `COUCHDB_COOKIE`: Erlang 노드 간 통신을 위한 쿠키.
- `COUCHDB_PORT`: 서비스 포트 (기본 5984).

## 사용법

서비스 시작:

```bash
docker-compose up -d
```

`couchdb-cluster-init` 컨테이너가 자동으로 노드들을 연결하고 시스템 데이터베이스(`_users`, `_replicator` 등)를 생성합니다.

## 접속

Traefik을 통해 다음 도메인으로 접근 가능합니다:

- **CouchDB UI (Fauxton)**: `https://couchdb.${DEFAULT_URL}/_utils`
- **API Endpoint**: `https://couchdb.${DEFAULT_URL}`

*참고: Traefik 로드 밸런서에 Sticky Session이 설정되어 있어, UI 사용 시 세션이 유지됩니다.*

## 볼륨

- `couchdb*-data`: 각 노드의 데이터 영구 저장소.
