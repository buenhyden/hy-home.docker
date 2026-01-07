# CouchDB Cluster

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: JSON 도큐먼트 기반의 분산 NoSQL 데이터베이스입니다.  
Seamless Multi-Master Replication을 지원하여 높은 가용성과 데이터 내구성을 보장합니다.

## 2. 주요 기능 (Key Features)
- **Multi-Master Replication**: 클러스터 내 모든 노드가 읽기/쓰기 작업을 처리하며 상호 동기화.
- **RESTful API**: 데이터베이스의 모든 기능을 HTTP API로 제어 가능.
- **Fauxton UI**: 직관적인 웹 기반 관리 인터페이스 제공.
- **Conflict Resolution**: 분산 환경에서의 데이터 충돌 감지 및 해결 메커니즘.

## 3. 기술 스택 (Tech Stack)
- **Image**: `couchdb:3.4.2`
- **Cluster Size**: 3 Nodes (`couchdb-1`, `couchdb-2`, `couchdb-3`)
- **Protocol**: Erlang Distribution Protocol (Clustering), HTTP/JSON (Client)

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 시스템 구조
1.  **Node 구성**: 3개의 독립적인 CouchDB 컨테이너가 하나의 클러스터로 묶여 있습니다.
2.  **초기화**: `couchdb-cluster-init` 컨테이너가 시작 시 각 노드의 API를 호출하여 클러스터 조인(Join) 프로세스를 자동화합니다.
3.  **로드 밸런싱**: Traefik이 `couchdb-cluster`라는 논리적 서비스로 트래픽을 분산합니다.
    - **Sticky Session**: `couchdb_sticky` 쿠키를 사용하여 클라이언트가 일관된 노드와 통신하도록 보장합니다.

### 워크플로우
1.  User -> Traefik (`https://couchdb.${DEFAULT_URL}`) -> CouchDB Node (RR/Sticky).
2.  CouchDB Node에 데이터 기록 시, 설정된 복제 계수(N=3, W=2 등)에 따라 내부적으로 다른 노드에 데이터 복제.

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **참고**: 컨테이너 실행 후 `couchdb-cluster-init` 서비스가 완료될 때까지(약 10~20초) 대기해야 클러스터가 정상 동작합니다.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 Fauxton UI 사용
웹 브라우저를 통해 손쉽게 데이터를 관리할 수 있습니다.
1.  **접속**: `https://couchdb.${DEFAULT_URL}/_utils`
2.  **로그인**: `admin` / `password` (환경변수 설정값)
3.  **기요 기능**:
    - **Databases**: DB 생성/삭제/권한 설정.
    - **Active Tasks**: 복제 및 인덱싱 작업 상태 확인.
    - **Setup**: 클러스터 구성 확인 (`Single Node` vs `Cluster`).

### 6.2 CLI (cURL) 사용법
모든 작업은 REST API로 수행 가능합니다.

**서버 상태 및 버전 확인**:
```bash
curl http://localhost:5984/
```

**데이터베이스 생성**:
```bash
curl -X PUT http://admin:password@localhost:5984/mydb
```

**문서(Document) 생성**:
```bash
curl -X POST http://admin:password@localhost:5984/mydb \
  -H "Content-Type: application/json" \
  -d '{"title": "My Document", "content": "Hello via API"}'
```

**Mango Query (JSON 쿼리 검색)**:
```bash
curl -X POST http://admin:password@localhost:5984/mydb/_find \
  -H "Content-Type: application/json" \
  -d '{"selector": {"title": "My Document"}}'
```

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `COUCHDB_USER`: 관리자 ID (기본: `admin`)
- `COUCHDB_PASSWORD`: 관리자 PW (기본: `password`)
- `COUCHDB_COOKIE`: 클러스터 노드 간 인증을 위한 Erlang Magic Cookie. 모든 노드가 동일해야 함.
- `NODENAME`: 클러스터 내에서 식별되는 노드 이름 (예: `couchdb-1.infra_net`).

### 네트워크 포트 (Ports)
- **5984**: HTTP API (외부 서비스용)
- **4369**: EPMD (Erlang Port Mapper Daemon)
- **9100-9200**: Erlang Distribution (노드 간 통신)

## 8. 통합 및 API 가이드 (Integration Guide)
**Sticky Session**:
- Traefik 로드밸런서에 `sticky.cookie` 설정이 활성화되어 있습니다.
- 클러이언트가 `Set-Cookie: couchdb_sticky=...` 헤더를 받으면, 이후 요청에 해당 쿠키를 포함하여 일관된 노드와 통신하는 것이 좋습니다 (특히 변경 사항 피드 구독 시).

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- 각 노드는 `/_up` 엔드포인트를 통해 실행 상태를 보고합니다.
- `/_membership` 엔드포인트를 호출하여 현재 클러스터에 조인된 노드 목록(`cluster_nodes`)과 활성 노드(`all_nodes`)를 확인할 수 있습니다.

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- **Volume Backup**: 각 노드의 `/opt/couchdb/data` 경로를 볼륨 스냅샷 등으로 백업.
- **Replication**: CouchDB 내장 Replication 기능을 사용하여 별도의 백업용 CouchDB 인스턴스로 데이터를 실시간 복제.

## 11. 보안 및 강화 (Security Hardening)
- **System DB Access**: `_users`, `_replicator` 데이터베이스는 보안에 민감하므로 접근 제어 목록(ACL)을 확인하세요.
- **Cookie Security**: `ERL_FLAGS`의 쿠키 값은 프로덕션 환경에서 반드시 강력한 난수로 변경해야 합니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Cluster Split-Brain**: 네트워크 문제로 노드 간 통신이 끊어지면 데이터 불일치가 발생할 수 있습니다. `_membership` 확인 후 재조인 필요.
- **Permission Denied**: 데이터 볼륨의 소유권(UID/GID)을 확인하세요 (CouchDB 컨테이너 내부 사용자 `couchdb`).

**진단 명령어**:
```bash
# 클러스터 멤버십 확인
docker exec -it couchdb-1 curl -u admin:password http://localhost:5984/_membership
```

---
**공식 문서**: [https://docs.couchdb.org/en/stable/](https://docs.couchdb.org/en/stable/)
