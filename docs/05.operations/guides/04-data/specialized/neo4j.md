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

- **ARD**: `[../../02.architecture/requirements/0004-data-architecture.md](../../../../02.architecture/requirements/0004-data-architecture.md)`
- **Procedure**: `[../../05.operations/04-data/specialized/neo4j.md](./neo4j.md)`

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/05.operations/04-data/specialized/neo4j.md` during the 2026-05-10 operations taxonomy consolidation.

### Neo4j Graph Database Usage

> Technical guide for understanding and using Neo4j within the `04-data/specialized` tier.

#### Overview (KR)

이 문서는 Neo4j 그래프 데이터베이스에 대한 기술 가이드다. 관계 중심 데이터 모델을 위한 그래프 저장소의 특성과 로컬 환경에서의 브라우저 UI 및 Bolt 프로토콜 활용 방법을 설명한다.

#### Usage Type

`system-guide`

#### Target Audience

- Backend Developers
- Data Architects
- Operators
- AI Agents

#### Purpose

이 가이드는 Neo4j의 아키텍처를 이해하고, Cypher 쿼리 언어를 사용하며, 로컬 서비스를 효율적으로 관리하는 것을 돕는다.

#### Prerequisites

- Docker 및 Docker Compose 설치
- `neo4j` 데이터 프로필 활성화
- 기본 Cypher 쿼리 문법 이해

#### Step-by-step Instructions

##### 1. Accessing Neo4j Browser

Neo4j Browser는 시각적 쿼리 도구이다.

1. 웹 브라우저에서 `https://neo4j.${DEFAULT_URL}` 접속
2. 인증 정보 입력 (사용자: `neo4j`, 비밀번호: Docker Secret `neo4j_password`)

##### 2. Basic Cypher Operations

데이터를 탐색하거나 생성할 때 Cypher를 사용한다.

```cypher
// Node 생성
CREATE (p:Person {name: 'Alice', role: 'Dev'})
RETURN p;

// Relationship 생성
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:COLLEAGUE]->(b);
```

##### 3. Connection via Bolt

애플리케이션 드라이버는 Bolt 프로토콜을 사용한다.

- **URL**: `bolt://neo4j.${DEFAULT_URL}:7687`
- **TLS**: 활성화 권장 (Traefik을 통한 암호화)

#### Common Pitfalls

- **Memory OOM**: Heap 크기(`NEO4J_server_memory_heap_max__size`)가 너무 작으면 복잡한 그래프 연산 시 장애가 발생할 수 있다.
- **Password Policies**: 초기 비밀번호 변경 필요 시, `cypher-shell`을 통해 수행해야 할 수 있다.

#### Related Documents

- **Spec**: `[infra/04-data/specialized/neo4j/README.md](../../../../../infra/04-data/specialized/neo4j/README.md)`
- **Operation**: `[../../05.operations/04-data/specialized/neo4j.md](./neo4j.md)`
- **Procedure**: `[../../05.operations/04-data/specialized/neo4j.md](./neo4j.md)`

## Procedure

> Migrated from `docs/05.operations/04-data/specialized/neo4j.md` during the 2026-05-10 operations taxonomy consolidation.

### Neo4j Recovery Procedure

: Neo4j Graph Database

> Procedure for database backup/restore and password management for Neo4j within the `04-data/specialized` tier.

#### Overview (KR)

이 런북은 Neo4j 데이터베이스의 백업 추출, 복구 및 관리자 패스워드 재설정 절차를 정의한다. 장애 발생 시 운영자가 즉시 실행할 수 있는 명령어를 제공한다.

#### Purpose

데이터 유실 방지를 위한 백업 수행 및 서비스 중단 시 빠른 데이터 복구를 지원한다.

#### Canonical References

- `[../../02.architecture/requirements/0004-data-architecture.md](../../../../02.architecture/requirements/0004-data-architecture.md)`
- `[../../../05.operations/04-data/specialized/neo4j.md](./neo4j.md)`
- `[infra/04-data/specialized/neo4j/README.md](../../../../../infra/04-data/specialized/neo4j/README.md)`

#### When to Use

- 정기적인 데이터 백업(Dump)이 필요할 때.
- 기존 백업 수단으로부터 데이터를 복구해야 할 때.
- 관리자 패스워드 분실 또는 유출로 인한 재설정이 필요할 때.

#### Procedure or Checklist

##### 1. Database Dump (Backup)

Neo4j Community Edition은 인스턴스를 중지한 후 오프라인 덤프를 수행해야 한다.

1. 인스턴스 중지: `docker compose stop neo4j`
2. 덤프 생성:

   ```bash
   docker run --rm \
     --volumes-from neo4j \
     -v $(pwd)/backups:/backups \
     neo4j:5.26.23-community \
     neo4j-admin database dump neo4j --to-path=/backups
   ```

3. 인스턴스 시작: `docker compose start neo4j`

##### 2. Database Load (Restore)

1. 인스턴스 중지: `docker compose stop neo4j`
2. 데이터 복구:

   ```bash
   docker run --rm \
     --volumes-from neo4j \
     -v $(pwd)/backups:/backups \
     neo4j:5.26.23-community \
     neo4j-admin database load neo4j --from-path=/backups --overwrite-destination=true
   ```

3. 인스턴스 시작: `docker compose start neo4j`

##### 3. Password Rotation

1. 승인된 secret rotation 절차로 Docker Secret `neo4j_password`를 갱신한다. 값은 문서나 로그에 남기지 않는다.
2. 서비스 재시작: `docker compose up -d --force-recreate neo4j`

#### Verification Steps

- [ ] `docker compose ps` 결과 `neo4j` 상태가 `Up (healthy)`인지 확인.
- [ ] 아래 방식으로 secret 값을 history에 남기지 않고 연결 확인.

  ```bash
  read -rsp "Neo4j password: " NEO4J_PASSWORD; echo
  cypher-shell -u neo4j -p "$NEO4J_PASSWORD" "RETURN 1;"
  unset NEO4J_PASSWORD
  ```

#### Observability and Evidence Sources

- **Signals**: Docker logs (`docker compose logs -f neo4j`), `/data/logs/neo4j.log`.
- **Evidence to Capture**: 덤프 파일 파일명 및 크기, 복구 로그 텍스트.

#### Safe Rollback or Recovery Procedure

- 복구 실패 시, 기존 `neo4j-data` 볼륨의 백업 디렉토리를 보존하고 이전 시점의 덤프 파일을 사용하여 재시도한다.

---

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../README.md)
- [../../05.operations/README.md](../../../README.md)
- [../../05.operations/incidents/README.md](../../../incidents/README.md)
