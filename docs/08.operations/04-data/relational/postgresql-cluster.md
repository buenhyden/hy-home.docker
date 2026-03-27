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
- **Guide**: `docs/07.guides/04-data/relational/postgresql-cluster.md`
- **Runbook**: `docs/09.runbooks/04-data/relational/postgresql-cluster.md`
- **Infra**: `infra/04-data/relational/postgresql-cluster/README.md`
- **Postmortem**: `docs/11.postmortems/`
