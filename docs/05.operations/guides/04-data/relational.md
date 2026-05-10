# Relational Databases Operations Policy

> PostgreSQL HA Cluster 운영 정책 및 데이터 보호 기준

---

## Overview (KR)

이 문서는 관계형 데이터베이스(`relational`) 계층의 운영 정책을 정의한다. 데이터 정합성 유지, 백업 주기, 보안 통제 및 가용성 보장을 위한 표준을 규정한다.

This document defines the operational policy for the Relational Database (`relational`) tier. It establishes standards for maintaining data integrity, backup cycles, security controls, and ensuring availability.

## Policy Scope

- PostgreSQL HA 클러스터(`postgresql-cluster`) 운영
- 데이터 백업 및 복구 정책
- 접근 제어 및 보안 통제

## Applies To

- **Systems**: PostgreSQL Nodes, etcd Quorum, HAProxy Router
- **Agents**: DevOps Agent, DBA Agent
- **Environments**: Production, Staging

## Controls

- **Required**:
  - 모든 클러스터는 최소 3노드(Primary 1, Replica 2) 구성을 유지해야 함.
  - 리더 선출을 위한 etcd 정족수(Quorum)는 홀수 개(최소 3개)여야 함.
  - 모든 연결은 Docker Secrets를 통한 인증을 필수적으로 수행해야 함.
  - `pg-router`를 통한 엔드포인트 접근만 허용함.
- **Allowed**:
  - 읽기 전용 트래픽의 복제본 분산 처리 (Port 15433).
  - 비정기적 수동 스냅샷 생성.
- **Disallowed**:
  - `postgres` 슈퍼유저 계정의 애플리케이션 직접 사용 금지.
  - 외부망(Public Internet)에 데이터베이스 포트 직접 노출 금지.

## Exceptions

- 단일 노드 테스트 환경: 아키텍처 팀 승인 하에 예외 허용.
- 응급 상황 시 수동 스위치오버(Switchover): 사후 Incident 기록 필수.

## Verification

- `patronictl list`를 통한 클러스터 헬스 체크.
- 정기적 백업 무결성 검증 (분기 1회).

## Review Cadence

- Quarterly

## Related Documents

- **ARD**: `[../../02.architecture/requirements/0004-data-architecture.md]`
- **Usage**: `[../../05.operations/04-data/relational.md]`
- **Procedure**: `[../../05.operations/04-data/relational.md]`

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/05.operations/04-data/relational.md` during the 2026-05-10 operations taxonomy consolidation.

### Relational Databases Usage

> PostgreSQL HA Cluster (Patroni/etcd) 사용 및 연결 가이드

---

#### Overview (KR)

이 문서는 `hy-home.docker` 인프라의 관계형 데이터베이스(`relational`) 계층에 대한 가이드다. Patroni와 etcd를 이용한 고가용성(HA) 클러스터 구조를 이해하고, 애플리케이션에서 안전하게 연결하는 방법과 관리 절차를 제공한다.

This document serves as a guide for the Relational Database (`relational`) tier of the `hy-home.docker` infrastructure. It provides an understanding of the High Availability (HA) cluster structure using Patroni and etcd, along with instructions for secure application connection and management procedures.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- AI Agent

#### Purpose

애플리케이션 개발자가 PostgreSQL HA 클러스터에 연결하고, 운영자가 클러스터 상태를 확인하며 관리하는 방법을 설명한다.

#### Prerequisites

- `docker` 및 `docker compose` 설치
- 인프라 네트워크(`infra_net`)에 대한 이해
- PostgreSQL 기본 지식

#### Step-by-step Instructions

##### 1. 클러스터 아키텍처 이해

- **Patroni**: PostgreSQL 인스턴스의 생명주기를 관리하고 장애 시 자동 페일오버를 수행한다.
- **etcd**: 클러스터의 리더 선출 상태와 설정을 저장하는 DCS(Distributed Configuration Store) 역할을 한다.
- **HAProxy (pg-router)**: 애플리케이션의 접속 지점이며, 읽기/쓰기 트래픽을 분산한다.

##### 2. 애플리케이션 연결 방법

- **Write (Primary)**: `pg-router:15432`로 연결한다. 리더 노드로 트래픽이 전달된다.
- **Read (Replica)**: `pg-router:15433`으로 연결한다. 가용한 모든 복제본 노드로 라운드 로빈 분산된다.

| Endpoint Type | Host      | Port  | Notes                      |
| ------------- | --------- | ----- | -------------------------- |
| Master (RW)   | pg-router | 15432 | Primary Node Only          |
| Replica (RO)  | pg-router | 15433 | All Available Replicas     |
| HAProxy Stats | pg-router | 8404  | Read-only Stats Interface  |

##### 3. 클러스터 상태 확인

```bash
### pg-0 노드에서 patronictl 실행
docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml list
```

#### Common Pitfalls

- **직접 연결 지양**: 개별 노드(`pg-0`, `pg-1`, `pg-2`)에 직접 연결하면 페일오버 발생 시 가용성을 보장받을 수 없다. 반드시 `pg-router`를 경유한다.
- **네트워크 격리**: 데이터베이스는 `infra_net` 내부망에서만 접근 가능하다. 외부 노출이 필요한 경우 API 게이트웨이를 통한다.

#### Related Documents

- **ARD**: `[../../02.architecture/requirements/0004-data-architecture.md]`
- **Spec**: `[../../03.specs/04-data/spec.md]`
- **Operation**: `[../../05.operations/04-data/relational.md]`
- **Procedure**: `[../../05.operations/04-data/relational.md]`

## Procedure

> Migrated from `docs/05.operations/04-data/relational.md` during the 2026-05-10 operations taxonomy consolidation.

### Relational Databases Procedure

: PostgreSQL HA Cluster Recovery Procedures

---

#### Overview (KR)

이 런북은 PostgreSQL HA 클러스터(`relational`)에서 발생할 수 있는 장애 상황에 대한 긴급 대응 및 복구 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 단계와 검증 기준을 제공한다.

This runbook defines emergency response and recovery procedures for potential failure scenarios in the PostgreSQL HA cluster (`relational`). it provides step-by-step instructions and verification criteria for immediate operational action.

#### Purpose

데이터베이스 노드 장애, etcd 정족수 상실, 또는 하이퍼바이저 장애 발생 시 서비스 가용성을 복구하고 데이터를 보존한다.

#### Canonical References

- `[../../02.architecture/requirements/0004-data-architecture.md]`
- `[../../02.architecture/decisions/0004-postgresql-ha-patroni.md]`
- `[../../05.operations/04-data/relational.md]`
- `[../../03.specs/04-data/postgresql-cluster/spec.md]`

#### When to Use

- PostgreSQL 리더(Leader) 노드 다운 및 페일오버 실패 시
- etcd 클러스터 가용성 상실 시
- 노드 데이터 오염 또는 저장 공간 부족 시

#### Procedure or Checklist

##### Checklist

- [ ] 현재 리더 노드 식별: `docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml list`
- [ ] etcd 엔드포인트 헬스 체크: `docker exec -it etcd-1 etcdctl endpoint health`
- [ ] 호스트 디스크 여유 공간 확인: `df -h`

##### Procedure

###### 1. 노드 재시작 (Minor Failure)

1. 장애 노드 확인: `docker compose ps`
2. 컨테이너 재시작: `docker compose restart [node-name]`
3. 상태 복구 대기: `patronictl list`로 리플리케이션 상태 확인

###### 2. etcd 정족수 복구

1. 모든 etcd 노드 상태 확인: `etcdctl endpoint health --cluster`
2. 과반수 미만 가동 시 클러스터 재구성 (스냅샷/백업 활용)

###### 3. 수동 페일오버 (Switchover)

1. 리더 교체가 필요한 경우: `docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml switchover`
2. 대상 노드 선택 및 실행 컨펌

#### Verification Steps

- [ ] `patronictl list`에서 모든 노드가 `running` 상태이고 `Leader`가 존재하는지 확인
- [ ] `pg-router` 트래픽 라우팅 확인 (Write on 15432, Read on 15433)
- [ ] 애플리케이션 로그에서 DB 연결 오류(`Connection refused`) 해소 확인

#### Safe Rollback or Recovery Procedure

- [ ] 장애 이전 시점의 백업 스냅샷 확인
- [ ] 볼륨 복구: `${DEFAULT_DATA_DIR}/pg/` 데이터 복원 및 컨테이너 재생성

#### Related Operational Documents

- **Operation**: `[../../05.operations/04-data/relational.md]`
- **Usage**: `[../../05.operations/04-data/relational.md]`
- **Incident examples**: `[../../05.operations/incidents/]`

---

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
