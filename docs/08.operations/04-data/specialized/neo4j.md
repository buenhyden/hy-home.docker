# Neo4j Operations Policy

> Operations policy for Neo4j graph database within the `04-data/specialized` tier.

## Overview (KR)

이 문서는 Neo4j 그래프 데이터베이스의 운영 정책을 정의한다. JVM 메모리 튜닝, 백업 주기, 보안 통제 및 성능 모니터링 기준을 규정한다.

## Policy Scope

Neo4j Community Edition 인스턴스의 자원 할당, 데이터 보호 및 접근 권한 관리를 규정한다.

## Applies To

- **Systems**: Neo4j (Containerized)
- **Agents**: Operators (DBA), DevOps Engineers
- **Environments**: Production (Graph/Data Profile)

## Controls

### 1. Resource Allocation

- **JVM Heap**: 128MB (Initial) / 256MB (Max)로 제한한다. (`NEO4J_server_memory_heap_*`)
- **Page Cache**: 128MB를 할당하여 디스크 I/O 성능을 최적화한다.

### 2. Security Controls

- **Authentication**: `neo4j` 기본 계정의 패스워드는 Docker Secret(`neo4j_password`)을 통해 주입해야 한다.
- **Networking**: 외부 접근은 Traefik을 통한 TLS 암호화(Bolt 7687, HTTPS 7473)가 필수이다.

### 3. Backup Standards

- **Frequency**: 일간(Daily) 오프라인 덤프를 수행한다.
- **Retention**: 최소 7일간의 백업 데이터를 유지한다.

## Exceptions

- 대량의 데이터 마이그레이션 시 일시적으로 JVM Heap 확장이 허용되나, 작업 후 원상복구해야 한다. (DevOps 승인 필요)

## Verification

- `cypher-shell`을 통한 정기적인 연결성 테스트.
- Docker Healthcheck(`cypher-shell RETURN 1`) 상태 모니터링.

## Review Cadence

- 분기별(Quarterly) 리소스 사용량 및 백업 무결성 검토.

## Related Documents

- **ARD**: `[../../02.ard/0004-data-architecture.md](../../../02.ard/0004-data-architecture.md)`
- **Runbook**: `[../../09.runbooks/04-data/specialized/neo4j.md](../../../09.runbooks/04-data/specialized/neo4j.md)`
