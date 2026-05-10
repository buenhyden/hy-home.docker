<!-- Target: docs/05.operations/guides/04-data/nosql/cassandra.md -->

# Cassandra Operation Policy

> Operational standards for maintaining a high-throughput Apache Cassandra single-node instance.

---

## Overview (KR)

이 문서는 `hy-home.docker` 환경에서 Apache Cassandra의 안정적인 운영을 위한 백업, 성능 모니터링, 리소스 관리 정책을 정의한다.

## Policy Type

`operational-standard`

## Target Audience

- Operator
- SRE
- AI-Operator

## Purpose

운영자가 Cassandra의 데이터 정합성을 유지하고, 성능 병목 현상을 사전에 방지하며, 효과적인 백업 및 복구 체계를 구축할 수 있도록 한다.

## Service Level Objectives (SLO)

- **Availability**: 99.9% (Single node limitation acknowledged)
- **Read Latency**: 95th percentile < 100ms
- **Write Latency**: 95th percentile < 50ms

## Operational Procedures

### 1. Monitoring & Alerting

- **Key Metrics**:
  - `ReadLatency`, `WriteLatency`: 요청 처리 속도 감시
  - `PendingTasks`: 시스템 부하 및 스케줄링 지연 확인
  - `DiskUsage`: `/var/lib/cassandra` 볼륨 잔여 용량 체크
- **Thresholds**: Disk 사용량 80% 초과 시 경고 발생.

### 2. Backup Strategy

- **Manual Snapshots**: 주요 업그레이드 또는 데이터 이관 전 `nodetool snapshot`을 수행한다.
- **Automated Backup**: `${DEFAULT_DATA_DIR}/cassandra` 볼륨의 일일 증분 백업을 수행한다. (External Storage 연동)
- **Recovery**: [Cassandra Recovery Procedure](./cassandra.md)을 참조하여 복권 수행.

### 3. Resource Management

- **JVM Heap**: 컨테이너 메모리의 50%(최대 8GB)를 힙 메모리로 할당한다.
- **Compaction**: 가급적 부하가 적은 시간에 `SizeTieredCompactionStrategy`를 통해 수행되도록 설정한다.

## Common Pitfalls

- **Disk Space during Compaction**: 컴팩션 작업 중에는 일시적으로 데이터 파일 크기가 2배까지 늘어날 수 있으므로 충분한 여유 공간(최소 50%)이 필요하다.
- **Garbage Collection**: JVM GC 포즈로 인한 응답 지연 발생 시 GC 로그를 분석하여 힙 크기를 재조정한다.

## Related Documents

- **Infrastructure**: [Cassandra Infrastructure](../../../../../infra/04-data/nosql/cassandra/README.md)
- **Usage**: [Cassandra System Usage](./cassandra.md)
- **Procedure**: [Cassandra Recovery Procedure](./cassandra.md)

---

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/05.operations/04-data/nosql/cassandra.md` during the 2026-05-10 operations taxonomy consolidation.

### Apache Cassandra System Usage

> Distributed wide-column NoSQL database for high-throughput, highly available workloads.

---

#### Overview (KR)

이 문서는 Apache Cassandra 5.0의 시스템 아키텍처, 데이터 모델링 기본 원리 및 `hy-home.docker` 환경에서의 사용 가이드를 제공한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- Agent-tuner

#### Purpose

애플리케이션 개발자와 운영자가 Cassandra의 분산 구조를 이해하고, 효율적인 데이터 스토리지 계층으로 활용할 수 있도록 돕는다.

#### Prerequisites

- `infra/04-data/nosql/cassandra` 배포 환경 및 Docker 기반 지식
- CQL(Cassandra Query Language) 기본 문법 이해
- `${DEFAULT_DATA_DIR}/cassandra` 볼륨 접근 권한

#### Step-by-step Instructions

##### 1. Cassandra 서비스 상태 확인

Cassandra가 정상적으로 실행 중인지 `nodetool`을 통해 확인한다.

```bash
docker exec -it cassandra-node1 nodetool status
```

- `UN` (Up/Normal): 정상 상태
- `DN` (Down/Normal): 서비스는 살아있으나 노드 통신 불가

##### 2. CQLSH를 통한 데이터베이스 접속

직접 쿼리를 수행하기 위해 `cqlsh` 인터페이스를 사용한다.

```bash
docker exec -it cassandra-node1 cqlsh -u ${CASSANDRA_USER} -p ${CASSANDRA_PASSWORD}
```

##### 3. 데이터 모델링 가이드

Cassandra는 쿼리 기반 모델링(Query-driven modeling)이 권장된다.

- **Keyspace**: 데이터베이스 단위의 스키마 정의 (Replication Strategy 포함)
- **Table**: 기본 키(Partition Key + Clustering Column)를 신중히 설계하여 데이터 분산을 최적화한다.
- **SAI (Storage Attached Indexing)**: Cassandra 5.0의 신기능으로, 여러 컬럼에 대해 효율적인 인덱싱을 제공한다.

##### 4. 메트릭 모니터링 연동

Prometheus는 `cassandra-exporter` (포트 8080/8081)를 통해 메트릭을 수집한다. Grafana에서 `Cassandra Overview` 대시보드를 통해 Read/Write Latency, Compaction 상태 등을 모니터링할 수 있다.

#### Common Pitfalls

- **Single Node Limit**: 현재 단일 노드 구성이므로 클러스터 수준의 가용성(`QUORUM` 등) 테스트는 제한적이다.
- **Heavy Scan Queries**: `ALLOW FILTERING`을 사용하는 쿼리는 대규모 데이터 셋에서 성능 장애를 유발하므로 실무 환경에서는 지양한다.
- **Tombstone Accumulation**: 대량의 `DELETE` 작업은 데이터 조회 시 성능 저하를 일으키므로 TTL 기반의 자동 삭제를 권장한다.

#### Related Documents

- **Spec**: [04-data Spec](../../../../03.specs/04-data/spec.md)
- **Operation**: [Cassandra Operations Policy](./cassandra.md)
- **Procedure**: [Cassandra Recovery Procedure](./cassandra.md)

## Procedure

> Migrated from `docs/05.operations/04-data/nosql/cassandra.md` during the 2026-05-10 operations taxonomy consolidation.

### Cassandra Recovery Procedure

> Emergency recovery procedures for Apache Cassandra single-node instance.

---

#### Overview (KR)

이 문서는 Cassandra 서비스 중단, 데이터 오염 또는 노드 장애 시 신속하게 서비스를 정상화하기 위한 긴급 대응 절차를 설명한다.

#### Procedure Type

`disaster-recovery`

#### Target Audience

- On-call Engineer
- SRE
- AI-Operator

#### Purpose

Cassandra 서비스 장애 발생 시 다운타임을 최소화하고, 데이터 손실 없이 최단 시간 내에 서비스를 복구하는 것을 목표로 한다.

#### Pre-remediation Checklist

- [ ] `docker ps`를 통해 컨테이너 상태 확인
- [ ] `docker logs cassandra-node1`에서 "Error" 키워드 검색
- [ ] `${DEFAULT_DATA_DIR}/cassandra` 볼륨 접근 가능 여부 확인
- [ ] 사용 가능한 최근 백업본(Snapshot) 존재 여부 확인

#### Remediation Steps

##### Scenario 1: Service Down (Container Crash)

컨테이너가 비정상 종료된 경우 재시작을 시도한다.

1. 컨테이너 재시작:

   ```bash
   cd infra/04-data/nosql/cassandra
   docker-compose up -d
   ```

2. 시작 로그 확인 (Status 'Ready' 확인):

   ```bash
   docker logs -f cassandra-node1
   ```

##### Scenario 2: Data Corruption (Restore from Snapshot)

데이터 오염 시 스냅샷을 기반으로 복원한다.

1. 서비스 중지:

   ```bash
   docker-compose stop cassandra-node1
   ```

2. 기존 데이터 백업 (안전을 위해):

   ```bash
   mv ${DEFAULT_DATA_DIR}/cassandra/data ${DEFAULT_DATA_DIR}/cassandra/data_broken
   ```

3. 스냅샷 복사:
   (백업 스토리지에서 최근 스냅샷을 `${DEFAULT_DATA_DIR}/cassandra/data` 위치로 복구)
4. 권한 확인 및 시작:

   ```bash
   chown -R 999:999 ${DEFAULT_DATA_DIR}/cassandra/data
   docker-compose start cassandra-node1
   ```

#### Verification Steps

1. 노드 상태 확인:

   ```bash
   docker exec -it cassandra-node1 nodetool status
   ```

   (상태가 `UN`이어야 함)
2. 데이터 샘플 쿼리:

   ```bash
   docker exec -it cassandra-node1 cqlsh -u ${CASSANDRA_USER} -p ${CASSANDRA_PASSWORD} -e "SELECT * FROM system.local;"
   ```

#### Post-remediation Tasks

- 장애 원인 분석 (Post-mortem) 작성 및 공유
- 모니터링 임계값 조정 필요성 검토
- 백업 무결성 추가 점검

#### Related Documents

- **Usage**: [Cassandra System Usage](./cassandra.md)
- **Operation**: [Cassandra Operation Policy](./cassandra.md)

---

#### Canonical References

- [../README.md](../README.md)
- [../../05.operations/README.md](../../../README.md)
- [../../05.operations/README.md](../../../README.md)

#### When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

#### Procedure or Checklist

##### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

##### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

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
