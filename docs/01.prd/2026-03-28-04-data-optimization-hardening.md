# 04-Data Optimization & Hardening Product Requirements

## Overview (KR)

이 문서는 `infra/04-data` 전 계층(analytics, cache-and-kv, lake-and-object, nosql, operational, relational, specialized)의 최적화/하드닝 요구사항을 정의한다. 즉시 적용 가능한 구성 하드닝을 우선 반영하고, 서비스별 확장 항목은 운영 정책과 단계별 전환 계획으로 관리한다.

## Vision

`04-data`를 서비스별 장애 격리와 복구 가능성이 높은 상태로 유지하고, CI 게이트를 통해 구성 회귀를 사전에 차단하며, 카탈로그 기반 확장(HA/성능/운영성)을 안정적으로 추진한다.

## Problem Statement

- 일부 04-data 구성에 계약 불일치(시크릿 파일 경로, tier 라벨, malformed expose 토큰)가 존재해 운영 위험을 유발한다.
- `supabase` 스택은 `service_healthy` 의존 관계 대비 healthcheck 계약이 부족해 시작 순서/장애 탐지가 불안정하다.
- 04-data 전용 하드닝 검증 게이트가 없어 회귀가 PR 단계에서 누락될 수 있다.
- 문서 계층(01~09)에서 04-data 최적화/하드닝 기준과 실행 절차의 추적성이 약하다.

## Personas

- **Data Platform Operator**: 데이터 서비스의 가용성과 복구 가능성을 지속적으로 관리해야 한다.
- **DevOps Engineer**: Compose/CI 기반 하드닝 기준을 자동 검증하고 회귀를 차단해야 한다.
- **Service Developer**: 데이터 플랫폼 계약(포트/시크릿/healthcheck)에 의존해 안정적으로 서비스를 연동해야 한다.

## Key Use Cases

- **STORY-01**: 운영자는 04-data compose 변경 후 `data-hardening` 게이트 통과 여부로 배포 가능성을 판단한다.
- **STORY-02**: 엔지니어는 `supabase` 스택의 healthcheck 기반 의존 순서가 안정적으로 동작하는지 점검한다.
- **STORY-03**: 장애 대응자는 runbook 절차로 Valkey exporter, SeaweedFS expose, Supabase health 문제를 빠르게 복구한다.

## Functional Requirements

- **REQ-PRD-DATA-FUN-01**: `supabase` 핵심 서비스(`studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `analytics`, `db`, `vector`, `supavisor`)에 healthcheck 계약을 적용해야 한다.
- **REQ-PRD-DATA-FUN-02**: `valkey-cluster-exporter`는 `service_valkey_password` 시크릿 계약을 사용해야 한다.
- **REQ-PRD-DATA-FUN-03**: `seaweedfs` compose의 malformed expose 토큰(`]`)을 제거해야 한다.
- **REQ-PRD-DATA-FUN-04**: `ksql`의 tier 라벨은 `data`로 정규화해야 한다.
- **REQ-PRD-DATA-FUN-05**: 04-data 하드닝 검증 스크립트(`scripts/check-data-hardening.sh`)와 CI job(`data-hardening`)을 제공해야 한다.
- **REQ-PRD-DATA-FUN-06**: 01~09 문서 계층에서 04-data 최적화/하드닝 기준, 정책, 절차를 상호 링크로 동기화해야 한다.

## Success Criteria

- **REQ-PRD-DATA-MET-01**: `bash scripts/check-data-hardening.sh`가 실패 0건으로 통과한다.
- **REQ-PRD-DATA-MET-02**: `docker compose -f infra/04-data/operational/supabase/docker-compose.yml config`가 오류 없이 통과한다.
- **REQ-PRD-DATA-MET-03**: `valkey-cluster` exporter 시크릿 경로가 단일 계약으로 정합화된다.
- **REQ-PRD-DATA-MET-04**: 04-data Spec/Plan/Tasks/Guide/Ops/Runbook 문서가 상호 추적 링크를 포함한다.

## Scope and Non-goals

- **In Scope**:
  - `infra/04-data/operational/supabase/docker-compose.yml` healthcheck 보강
  - `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml` 시크릿 경로 정합화
  - `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml` expose 정합화
  - `infra/04-data/analytics/ksql/docker-compose.yml` tier 라벨 정규화
  - 04-data 하드닝 검증 스크립트/CI 게이트 추가
  - 01~09 문서 및 README 인덱스 갱신
- **Out of Scope**:
  - 각 데이터 엔진의 즉시 HA 토폴로지 확장(예: Cassandra multi-node 신규 구축)
  - 애플리케이션 비즈니스 로직/SQL 튜닝 구현
  - 클라우드 매니지드 DB 전환
- **Non-goals**:
  - 모든 카탈로그 확장 항목의 즉시 구현
  - 서비스 기능 변경

## Risks, Dependencies, and Assumptions

- 일부 healthcheck는 프로세스 liveness 중심으로 시작하며, 서비스 레벨 readiness는 단계적으로 보강한다.
- 04-data 카탈로그 확장 항목은 운영 승인/용량 계획/성능 검증이 필요하다.
- 런타임 검증은 로컬 Docker 실행 환경에 의존한다.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: 04-data compose/script/docs/ci 수정 및 정적 검증 실행.
- **Disallowed Actions**: 무검증 포트 노출 확대, 시크릿 하드코딩, 카탈로그 미근거 구조 변경.
- **Human-in-the-loop Requirement**: HA 확장, 보존 정책 변경, 운영 노출 정책 변경은 승인 후 수행.
- **Evaluation Expectation**: `data-hardening`, `template-security-baseline`, `doc-traceability` 통과.

## Related Documents

- **ARD**: [../02.ard/0019-data-optimization-hardening-architecture.md](../02.ard/0019-data-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/04-data/spec.md](../04.specs/04-data/spec.md)
- **Plan**: [../05.plans/2026-03-28-04-data-optimization-hardening-plan.md](../05.plans/2026-03-28-04-data-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0019-04-data-hardening-and-ha-expansion-strategy.md](../03.adr/0019-04-data-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md](../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/04-data/optimization-hardening.md](../07.guides/04-data/optimization-hardening.md)
- **Operation**: [../08.operations/04-data/optimization-hardening.md](../08.operations/04-data/optimization-hardening.md)
- **Runbook**: [../09.runbooks/04-data/optimization-hardening.md](../09.runbooks/04-data/optimization-hardening.md)
