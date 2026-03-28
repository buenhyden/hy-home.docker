# 04-Data Optimization Hardening Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 `04-data` 계층의 최적화/하드닝 참조 아키텍처를 정의한다. 현재 서비스별 단일/소규모 클러스터 운영 구조를 안정화하고, 카탈로그 기반 확장 항목(HA, lifecycle, recovery drill)을 단계적으로 수용하는 경계를 명시한다.

## Summary

04-data는 다중 엔진(관계형/NoSQL/캐시/오브젝트/분석)으로 구성되므로, 공통 제어(healthcheck, secrets, 템플릿 상속, CI 게이트)와 엔진별 확장 정책을 분리해 관리한다. 이번 단계는 즉시 회귀 위험이 높은 구성 정합성을 먼저 고정한다.

## Boundaries & Non-goals

- **Owns**:
  - `infra/04-data/*` compose 구성 계약
  - 데이터 서비스 런타임 하드닝 기준과 검증 자동화
  - 04-data 문서 추적성(01~09) 정합성
- **Consumes**:
  - `01-gateway` 라우팅/TLS 종료 정책
  - `03-security` 시크릿 관리 정책
  - `06-observability` 메트릭/로그 수집 체계
- **Does Not Own**:
  - 애플리케이션 비즈니스 스키마/쿼리 로직
  - 개별 서비스의 제품 기능 로직
- **Non-goals**:
  - 모든 데이터 서비스의 즉시 HA 재구성
  - 클라우드 데이터 플랫폼 마이그레이션

## Quality Attributes

- **Performance**: 분석/캐시/스토리지 서비스별 리소스 한계와 운영 창(window) 관리
- **Security**: 시크릿 주입 일관성, 불필요 노출 축소, 정책 기반 제어
- **Reliability**: healthcheck 기반 의존 관계 안정화, 복구 절차 표준화
- **Scalability**: 카탈로그 기준으로 엔진별 확장 옵션(HA, lifecycle, reindex) 준비
- **Observability**: 핵심 상태와 복구 증적을 runbook 명령 기반으로 확보
- **Operability**: CI gate + 운영 문서 + 실행 절차의 단일 계약 유지

## System Overview & Context

- Analytics: `influxdb`, `ksqldb`, `opensearch`, `warehouses`
- Cache & KV: `valkey-cluster`
- Lake & Object: `minio`, `seaweedfs`
- NoSQL: `cassandra`, `couchdb`, `mongodb`
- Operational: `mng-db`, `supabase`
- Relational: `postgresql-cluster`
- Specialized: `neo4j`, `qdrant`

이번 하드닝의 구조적 초점:

1. compose 계약 정합성 확보(시크릿/라벨/expose)
2. `supabase` healthcheck 공백 보강
3. 04-data 전용 정적 검증 자동화
4. 카탈로그 확장 항목의 정책/절차 연결

## Data Architecture

- **Key Entities / Flows**:
  - SQL wire protocol, Redis/Valkey protocol, S3-compatible API, Vector/Graph APIs
- **Storage Strategy**:
  - `${DEFAULT_DATA_DIR}` 기반 서비스별 독립 볼륨
- **Data Boundaries**:
  - 엔진별 데이터 경계 유지
  - 공통 비밀/자격증명은 `secrets` 계약으로 통일

## Infrastructure & Deployment

- **Runtime / Platform**:
  - Docker Compose + `infra/common-optimizations.yml`
- **Deployment Model**:
  - Phase 1: 정합성/healthcheck/CI gate 하드닝
  - Phase 2: 카탈로그 확장(예: lifecycle, failover drill, backup window) 설계 반영
  - Phase 3: 서비스별 승인된 HA 확장 실행
- **Operational Evidence**:
  - `scripts/check-data-hardening.sh`
  - `scripts/check-template-security-baseline.sh`
  - `scripts/check-doc-traceability.sh`

## AI Agent Architecture Requirements (If Applicable)

- **Model/Provider Strategy**: N/A
- **Tooling Boundary**: 04-data 변경은 하드닝/추적성 검증 통과 필수
- **Memory & Context Strategy**: 카탈로그 + Spec + Runbook 링크를 실행 컨텍스트로 고정
- **Guardrail Boundary**: 시크릿 하드코딩/무근거 포트 노출/무검증 토폴로지 변경 금지
- **Latency / Cost Budget**: 엔진별 정책 문서에서 관리

## Related Documents

- **PRD**: [../01.prd/2026-03-28-04-data-optimization-hardening.md](../01.prd/2026-03-28-04-data-optimization-hardening.md)
- **Spec**: [../04.specs/04-data/spec.md](../04.specs/04-data/spec.md)
- **Plan**: [../05.plans/2026-03-28-04-data-optimization-hardening-plan.md](../05.plans/2026-03-28-04-data-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0019-04-data-hardening-and-ha-expansion-strategy.md](../03.adr/0019-04-data-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md](../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/04-data/optimization-hardening.md](../07.guides/04-data/optimization-hardening.md)
- **Operation**: [../08.operations/04-data/optimization-hardening.md](../08.operations/04-data/optimization-hardening.md)
- **Runbook**: [../09.runbooks/04-data/optimization-hardening.md](../09.runbooks/04-data/optimization-hardening.md)
