# CouchDB Cluster

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: JSON 도큐먼트 기반의 분산 NoSQL 데이터베이스입니다. 멀티 마스터 복제와 강력한 동기화 기능을 제공합니다.

**주요 기능 (Key Features)**:
- **Multi-Master Replication**: 노드 간 양방향 데이터 동기화.
- **RESTful API**: HTTP/JSON 기반의 직관적인 API.

**기술 스택 (Tech Stack)**:
- **Image**: `couchdb:3.4.2`
- **Cluster**: 3 Nodes

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
**시스템 구조도**:
- 3개의 CouchDB 노드(`couchdb-1`, `2`, `3`)가 Erlang 배포 프로토콜로 연결됨.
- `couchdb-cluster-init` 컨테이너가 API를 호출하여 클러스터 조인 수행.

## 3. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
(초기화 컨테이너가 자동으로 클러스터를 구성합니다.)

## 4. 환경 설정 명세 (Configuration Reference)
**환경 변수**:
- `COUCHDB_USER`, `COUCHDB_PASSWORD`: 관리자 계정.
- `COUCHDB_COOKIE`: 클러스터 노드 간 인증 키(Erlang Cookie).

**네트워크 포트**:
- **API**: 5984
- **Cluster**: 5986, 4369, 9100-9200 (내부 통신용)
- **External**: `https://couchdb.${DEFAULT_URL}` (Traefik)

## 5. 통합 및 API 가이드 (Integration Guide)
**Sticky Session**:
- Traefik 로드밸런서 설정에 `sticky.cookie`가 활성화되어 있습니다. 클라이언트는 세션 일관성을 위해 쿠키를 유지해야 할 수 있습니다.

**엔드포인트**: `https://couchdb.${DEFAULT_URL}/_utils` (Fauxton UI)

## 6. 가용성 및 관측성 (Availability & Observability)
**상태 확인**: `/_up` 엔드포인트.

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- 각 노드의 `/opt/couchdb/data` 볼륨 백업.
- Replication 프로토콜을 이용해 백업 서버로 실시간 복제본 유지 가능.

## 8. 보안 및 강화 (Security Hardening)
- `_users`, `_replicator` 등 시스템 DB에 대한 접근 제어 확인.

## 9. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Cluster Split-Brain**: 네트워크 단절 시 발생 가능. 노드 재조인 필요.
- **Membership Error**: `_membership` 엔드포인트로 클러스터 상태 확인.

**진단 명령어**:
```bash
curl -u admin:password http://localhost:5984/_membership
```
