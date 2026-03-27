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

- **ARD**: `[../../02.ard/0004-data-architecture.md]`
- **Guide**: `[../../07.guides/04-data/relational.md]`
- **Runbook**: `[../../09.runbooks/04-data/relational.md]`
