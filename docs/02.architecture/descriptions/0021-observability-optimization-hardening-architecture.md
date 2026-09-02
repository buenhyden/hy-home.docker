---
title: 06-Observability Optimization Hardening Architecture Description
type: architecture/description
layer: architecture
status: active
owner: "@buenhyden"
artifact_id: AD-0021
parent_ids:
  - REQ-0018
created: 2026-03-28
updated: 2026-09-01
---
# 06-Observability Optimization Hardening Architecture Description

## Context and Stakeholders

이 문서는 `06-observability` 계층의 최적화/하드닝 참조 아키텍처를 정의한다. 게이트웨이 경계 보안, health 기반 의존성, 커스텀 이미지 런타임 하드닝, 카탈로그 기반 확장 전략을 아키텍처 관점에서 정리한다.

## Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

관측성 계층은 데이터 평면(수집/저장)과 관리 평면(UI/API)을 분리해 운영한다. 관리 평면은 Traefik TLS 종료 지점에서 표준 미들웨어+SSO 체인을 적용하고, 데이터 평면은 `infra_net` 내부 통신으로 유지한다.

## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owns**:
  - 관측성 서비스 라우팅/인증 경계 계약
  - health 기반 부팅 순서 및 런타임 하드닝 계약
  - observability 하드닝 검증 자동화 계약
- **Consumes**:
  - `01-gateway` Traefik middleware chain
  - `02-auth` Keycloak 기반 SSO
  - `04-data` MinIO object storage
- **Does Not Own**:
  - 애플리케이션 계측 코드(OTel SDK)
  - 비관측성 티어 라우팅 정책
- **Non-goals**:
  - 즉시 multi-cluster/multi-region observability 도입
  - 샘플링 정책 전면 재설계

## Quality Attributes

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: 게이트웨이 표준 체인으로 burst 제어/과부하 완화
- **Security**: TLS 종료 + SSO + 비루트 컨테이너 실행
- **Reliability**: `service_healthy` 의존성으로 부팅 안정성 향상
- **Scalability**: catalog 기반 확장(샘플링/retention/long-term storage) 준비
- **Observability**: cAdvisor health, pyroscope availability, and stack health validation
- **Operability**: 스크립트 기반 회귀 차단 + runbook 표준 절차

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

- Storage/Query Plane:
  - Prometheus, Loki, Tempo, Pyroscope
- Control/Presentation Plane:
  - Grafana, Alertmanager, Pushgateway, Alloy UI, cAdvisor route, Pyroscope route
- Gateway Path:
  - Client -> Traefik(`websecure`) -> `gateway-standard-chain` + `sso-*` -> target service
- Internal Path:
  - OTLP/log/trace traffic over `infra_net`

## Data Flow

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

- **Key Entities / Flows**:
  - Metrics, logs, traces, profiles
- **Storage Strategy**:
  - Prometheus local TSDB
  - Loki/Tempo object storage via MinIO
  - Pyroscope local storage
- **Data Boundaries**:
  - 장기 보존/리텐션 정책은 operations 계층에서 관리

## Deployment View

- **Runtime / Platform**:
  - Docker Compose + `infra/common-optimizations.yml`
- **Deployment Model**:
  - single-node observability core + optional horizontal expansion
- **Operational Evidence**:
  - `scripts/hardening/check-all-hardening.sh 06-observability`
  - CI `infrastructure-hardening` job

## Catalog-aligned Expansion Targets

- Prometheus: scrape budget + remote_write 계층화
- Loki: label cardinality budget + retention/compactor 분리 운영
- Tempo: service/endpoint별 샘플링 정책 + span 폭주 보호
- Alloy: 온보딩 템플릿화 + 수집 파이프라인 모듈화

## Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [../01.requirements/0018-observability-optimization-hardening.md](../../01.requirements/0018-observability-optimization-hardening.md)
- **Spec**: [../03.specs/007-observability/spec.md](../../03.specs/0007-observability/spec.md)
- **ADR**: [../02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md](../decisions/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Guide**: [../../05.operations/guides/06-observability/optimization-hardening.md](../../05.operations/catalog/06-observability/0044-optimization-hardening/guide.md)
- **Policy**: [../../05.operations/policies/06-observability/optimization-hardening.md](../../05.operations/catalog/06-observability/0044-optimization-hardening/policy.md)
- **Runbook**: [../../05.operations/runbooks/06-observability/optimization-hardening.md](../../05.operations/catalog/06-observability/0044-optimization-hardening/runbook.md)
