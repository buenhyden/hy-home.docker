# postgresql-cluster Operations Policy

> Patroni 기반 PostgreSQL 클러스터의 데이터 무결성 및 가용성 운영 표준
> Operational Standards for Data Integrity and Availability of Patroni-based PostgreSQL Clusters

---

## Overview (KR/EN)

### KR

이 문서는 `postgresql-cluster` 운영 정책을 정의한다. Patroni 기반 클러스터의 데이터 무결성 보호, 가용성 보장, 그리고 장애 대응 성능 유지를 위한 통제 기준과 검증 방법을 규정한다.

### EN

This document defines the operational policy for `postgresql-cluster`. It establishes control standards and verification methods for protecting data integrity, ensuring availability, and maintaining incident response performance of the Patroni-based cluster.

## Policy Scope

- Patroni 클러스터 생명주기 및 리더십 관리
- etcd DCS 쿼럼(Quorum) 유지
- HAProxy 라우팅 정합성 및 헬스체크 정책
- 백업 수행 및 복구 유효성 검증

## Applies To

- **Systems**: `postgresql-cluster`, `etcd-cluster`, `pg-router`
- **Agents**: Infrastructure Operator, DBA, SRE, AI Agent (Operation Scope)
- **Environments**: Production-ready local/staging nodes

## Controls

- **Required**:
  - 최소 3개 노드의 etcd 쿼럼 유지 (DCS 가용성 확보)
  - 일일 전체 백업 및 실시간 WAL 아카이빙 수행
  - 모든 애플리케이션 연결은 반드시 `pg-router`를 통과
- **Allowed**:
  - `patronictl switchover`를 이용한 계획된 리더 변경
  - 읽기 부하 분산을 위한 15433(RO) 포트 활용
- **Disallowed**:
  - 개별 PostgreSQL 노드(pg-0/1/2)에 직접 쓰기 시도
  - etcd 정족수 이하에서의 강제 클러스터 부트스트랩 (데이터 손실 위험)

## Exceptions

- 재해 복구(DR) 상황에서의 수동 클러스터 재구성 (Lead SRE 승인 필요)

## Verification

- `patronictl list`를 통한 리더십 정합성 실시간 확인
- Prometheus 엑스포터를 이용한 복제 지연(Replication Lag) 모니터링 (> 100MB 경고)
- 매월 1회 백업 데이터를 이용한 복구 시뮬레이션 수행

## Review Cadence

- Quarterly (분기별 운영 정책 및 임계치 검토)

## Related Documents

- **ARD**: `docs/02.ard/0004-data-architecture.md`
- **Usage**: `docs/07.operations/04-data/relational/postgresql-cluster.md`
- **Procedure**: `docs/07.operations/04-data/relational/postgresql-cluster.md`
- **Infra**: `infra/04-data/relational/postgresql-cluster/README.md`
- **Postmortem**: `docs/10.incidents/`

---

## Overview (KR)

이 문서는 `docs/07.operations/04-data/relational/postgresql-cluster.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/07.operations/04-data/relational/postgresql-cluster.md` during the 2026-05-10 operations taxonomy consolidation.

### postgresql-cluster Usage

> Patroni 및 etcd 기반 고가용성(HA) PostgreSQL 클러스터 가이드
> High-Availability (HA) PostgreSQL Cluster Usage based on Patroni and etcd

---

#### Overview (KR/EN)

##### KR

이 문서는 `postgresql-cluster`의 아키텍처를 이해하고, 데이타베이스 노드 상태 확인 및 애플리케이션 연결 방법을 익히기 위한 시스템 가이드다. Patroni와 etcd가 어떻게 협력하여 고가용성을 유지하는지, 그리고 HAProxy(`pg-router`)를 통한 트래픽 라우팅 원리를 설명한다.

##### EN

This document is a system guide for understanding the architecture of `postgresql-cluster` and learning how to check database node status and connect applications. It explains how Patroni and etcd work together to maintain high availability and the principles of traffic routing through HAProxy (`pg-router`).

#### Usage Type

`system-guide`

#### Target Audience

- Developer (연결 및 쿼리 테스트)
- Operator (클러스터 상태 점검 및 유지보수)
- AI Agent (인프라 무결성 검증 및 사고 대응 보조)

#### Purpose

- Patroni HA 아키텍처의 동작 원리 이해
- etcd DCS(Distributed Configuration Store)의 역할 파악
- `pg-router`(HAProxy)를 이용한 읽기/쓰기 분산 연결 방법 습득

#### Prerequisites

- `infra_net` 네트워크에 대한 이해 및 접근 권한
- Docker Secrets(`patroni_superuser_password`)에 대한 인지
- `patronictl` CLI 도구 기본 사용법 숙지

#### Step-by-step Instructions

##### 1. 클러스터 상태 모니터링

Patroni CLI를 사용하여 현재 리더(Leader) 노드와 복제본(Replica) 노드들의 상태를 확인한다.

```bash
### pg-0 노드에서 클러스터 리스트 확인
docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml list
```

##### 2. 애플리케이션 연결 정의

모든 애플리케이션은 개별 PostgreSQL 노드 주소가 아닌, `pg-router` 엔드포인트를 사용해야 한다.

- **Write (Master)**: `pg-router:15432` (리더 노드 자동 연결)
- **Read (Replica)**: `pg-router:15433` (레플리카들 간 라운드 로빈 분산)

##### 3. 초기화 작업 (pg-cluster-init)

시스템 구동 시 `pg-cluster-init` 컨테이너가 자동으로 실행되어 서비스에 필요한 기본 DB와 사용자를 생성한다. 수동 재실행이 필요한 경우:

```bash
docker compose up pg-cluster-init
```

#### Common Pitfalls

- **etcd Quorum Loss**: 3개 etcd 노드 중 2개 이상 장애 시 리더 선출이 중단되며 클러스터는 `Read-Only` 상태로 전환될 수 있다.
- **Connection Limits**: HAProxy 포트가 열려 있어도 각 노드의 `max_connections` 설정에 따라 연결이 거부될 수 있으므로 커넥션 풀 사용을 권장한다.

#### Related Documents

- **Spec**: `docs/04.specs/04-data/spec.md`
- **Operation**: `docs/07.operations/04-data/relational/postgresql-cluster.md`
- **Procedure**: `docs/07.operations/04-data/relational/postgresql-cluster.md`
- **Infra**: `infra/04-data/relational/postgresql-cluster/README.md`

---

#### Overview (KR)

이 문서는 `docs/07.operations/04-data/relational/postgresql-cluster.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

## Procedure

> Migrated from `docs/07.operations/04-data/relational/postgresql-cluster.md` during the 2026-05-10 operations taxonomy consolidation.

### postgresql-cluster Procedure

: PostgreSQL Cluster High-Availability Recovery

> Patroni 및 etcd 기반 PostgreSQL 클러스터 장애 복구 및 유지보수 실행 지침
> Operational Procedures for Fault Recovery and Maintenance of Patroni and etcd-based PostgreSQL Clusters

---

#### Overview (KR/EN)

##### KR

이 런북은 `postgresql-cluster` 장애 시 신속한 복구 및 유지보수 작업을 위한 실행 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 단계와 검증 기준을 제공하여 서비스 중단을 최소화하는 것을 목적으로 한다.

##### EN

This runbook defines operational procedures for rapid recovery and maintenance in the event of a `postgresql-cluster` failure. It provides step-by-step instructions and verification criteria that operators can follow immediately to minimize service disruption.

#### Purpose

- etcd 쿼럼 소실 시 클러스터 복구
- PostgreSQL 마스터 장애 시 수동 페일오버 및 상태 복구
- `pg-cluster-init`을 이용한 데이터베이스 초기화 재수행

#### Canonical References

- **ARD**: `docs/02.ard/0004-data-architecture.md`
- **Spec**: `docs/04.specs/04-data/spec.md`
- **Operation**: `docs/07.operations/04-data/relational/postgresql-cluster.md`

#### When to Use

- `patronictl list` 결과에서 리더가 없거나 쿼럼이 깨진 경우
- 계획된 점검을 위해 리더 노드를 변경(Switchover)해야 하는 경우
- `pg-router`를 통한 DB 접속이 불가능한 경우

#### Procedure or Checklist

##### Checklist

- [ ] `docker compose ps`로 etcd 및 pg 노드 컨테이너 생존 확인
- [ ] `docker compose logs`로 에러 메시지 확인
- [ ] 데이터 볼륨(`DEFAULT_DATA_DIR`)의 디스크 여유 공간 확인

##### Procedure

###### 1. 클러스터 수동 리더 변경 (Switchover)

```bash
docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml switchover
```

###### 2. etcd 쿼럼 복구 (전체 장애 시)

1. 모든 PostgreSQL 노드 정지: `docker compose stop pg-0 pg-1 pg-2`
2. etcd 데이터 초기화 (필요시): `rm -rf ${DEFAULT_DATA_DIR}/etcd/*`
3. etcd 서비스 재시작: `docker compose up -d etcd-1 etcd-2 etcd-3`
4. PostgreSQL 노드 순차 가동: `docker compose up -d pg-0` (이후 순차)

###### 3. 초기화 작업(pg-cluster-init) 재실행

```bash
docker compose rm -f pg-cluster-init
docker compose up pg-cluster-init
```

#### Verification Steps

- [ ] `docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml list` 실행 후 `Leader` 존재 확인
- [ ] `pg_isready -h localhost -p 15432 -U postgres` 명령으로 쓰기 포트 가용성 확인

#### Observability and Evidence Sources

- **Signals**: Grafana PostgreSQL Dashboard, `pg-router` HAProxy Stats
- **Evidence to Capture**: `patronictl list` 출력 결과, `docker compose logs`

#### Safe Rollback or Recovery Procedure

- [ ] 기존 클러스터 상태 보존을 위한 볼륨 백업 권장
- [ ] etcd 강제 무력화 전 반드시 데이터 무결성 검토

#### Related Operational Documents

- **Incident examples**: `docs/10.incidents/`
- **Postmortem examples**: `docs/10.incidents/`

---

#### Overview (KR)

이 런북은 `docs/07.operations/04-data/relational/postgresql-cluster.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
