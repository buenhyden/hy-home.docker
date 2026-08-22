---
profile_id: architecture-description
status: active
artifact_id: AD-0019
artifact_type: architecture-description
parent_ids:
  - REQ-0016
created: 2026-03-28
updated: 2026-08-10
---
# 04-Data Optimization Hardening Architecture Description

## Context and Stakeholders

이 문서는 `04-data` 계층의 최적화/하드닝 참조 아키텍처를 정의한다. 현재 서비스별 단일/소규모 클러스터 운영 구조를 안정화하고, 카탈로그 기반 확장 항목(HA, lifecycle, recovery drill)을 단계적으로 수용하는 경계를 명시한다.

## Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

04-data는 다중 엔진(관계형/NoSQL/캐시/오브젝트/분석)으로 구성되므로, 공통 제어(healthcheck, secrets, 템플릿 상속, CI 게이트)와 엔진별 확장 정책을 분리해 관리한다. 이번 단계는 즉시 회귀 위험이 높은 구성 정합성을 먼저 고정한다.

## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owns**:
  - `infra/04-data/*` compose 구성 계약
  - 데이터 서비스 런타임 하드닝 기준과 검증 자동화
  - 04-data Stage 01-05 문서 추적성 정합성
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

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: 분석/캐시/스토리지 서비스별 리소스 한계와 운영 창(window) 관리
- **Security**: 시크릿 주입 일관성, 불필요 노출 축소, 정책 기반 제어
- **Reliability**: healthcheck 기반 의존 관계 안정화, 복구 절차 표준화
- **Scalability**: 카탈로그 기준으로 엔진별 확장 옵션(HA, lifecycle, reindex) 준비
- **Observability**: 핵심 상태와 복구 증적을 runbook 명령 기반으로 확보
- **Operability**: CI gate + 운영 문서 + 실행 절차의 단일 계약 유지

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

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

## Data Flow

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

- **Key Entities / Flows**:
  - SQL wire protocol, Redis/Valkey protocol, S3-compatible API, Vector/Graph APIs
- **Storage Strategy**:
  - `${DEFAULT_DATA_DIR}` 기반 서비스별 독립 볼륨
- **Data Boundaries**:
  - 엔진별 데이터 경계 유지
  - 공통 비밀/자격증명은 `secrets` 계약으로 통일

## Deployment View

- **Runtime / Platform**:
  - Docker Compose + `infra/common-optimizations.yml`
- **Deployment Model**:
  - Phase 1: 정합성/healthcheck/CI gate 하드닝
  - Phase 2: 카탈로그 확장(예: lifecycle, failover drill, backup window) 설계 반영
  - Phase 3: 서비스별 승인된 HA 확장 실행
- **Operational Evidence**:
  - `scripts/hardening/check-all-hardening.sh 04-data`
  - `scripts/validation/check-template-security-baseline.sh`
  - `scripts/validation/check-document-links.py --mode traceability`

## AI Agent Architecture Descriptions (If Applicable)

- **Model/Provider Strategy**: N/A
- **Tooling Boundary**: 04-data 변경은 하드닝/추적성 검증 통과 필수
- **Memory & Context Strategy**: 카탈로그 + Spec + Runbook 링크를 실행 컨텍스트로 고정
- **Guardrail Boundary**: 시크릿 하드코딩/무근거 포트 노출/무검증 토폴로지 변경 금지
- **Latency / Cost Budget**: 엔진별 정책 문서에서 관리

## Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [../01.requirements/0016-data-optimization-hardening.md](../../01.requirements/0016-data-optimization-hardening.md)
- **Spec**: [../03.specs/004-data/spec.md](../../03.specs/0004-data/spec.md)
- **Plan**: ../04.execution/plans/2026-03-28-04-data-optimization-hardening-plan.md
- **ADR**: [../02.architecture/decisions/0019-04-data-hardening-and-ha-expansion-strategy.md](../decisions/0019-04-data-hardening-and-ha-expansion-strategy.md)
- **Tasks**: ../04.execution/tasks/2026-03-28-04-data-optimization-hardening-tasks.md
- **Guide**: [../../05.operations/guides/04-data/optimization/optimization-hardening.md](../../05.operations/catalog/04-data/ops-0030-optimization-hardening/guide.md)
- **Policy**: [../../05.operations/policies/04-data/optimization/optimization-hardening.md](../../05.operations/catalog/04-data/ops-0030-optimization-hardening/policy.md)
- **Runbook**: [../../05.operations/runbooks/04-data/optimization/optimization-hardening.md](../../05.operations/catalog/04-data/ops-0030-optimization-hardening/runbook.md)
