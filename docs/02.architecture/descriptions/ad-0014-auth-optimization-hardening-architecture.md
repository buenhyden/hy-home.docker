---
status: active
artifact_id: ad-0014
artifact_type: architecture-description
parent_ids:
  - REQ-0014
created: 2026-03-28
updated: 2026-08-10
---
# 02-Auth Optimization Hardening Architecture Description

## Overview and Context

이 문서는 `02-auth` 계층의 최적화/하드닝 참조 아키텍처를 정의한다. Keycloak과 OAuth2 Proxy의 책임 경계를 유지하면서, 시크릿 주입 표준화와 fail-closed 운영 모델을 아키텍처 기준으로 고정한다.

## Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

`02-auth`는 중앙 IdP(Keycloak) + ForwardAuth 게이트(OAuth2 Proxy) 구조를 유지한다. 최적화의 핵심은 런타임 시크릿 주입 경로 단순화, 컨테이너 권한 최소화, 운영 검증 자동화, 그리고 문서-운영 실행 계층의 추적성 강화다.

## Boundaries and Constraints

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owns**:
  - 인증 토큰 발급/검증 경로
  - ForwardAuth 인증 진입점
  - 인증 세션 정책(만료/갱신/도메인)
- **Consumes**:
  - `04-data`의 PostgreSQL/Valkey
  - `01-gateway`의 HTTPS ingress 및 라우팅
- **Does Not Own**:
  - 애플리케이션별 인가(RBAC) 정책 세부 구현
  - 비인증 비즈니스 로직
- **Non-goals**:
  - 인증 플로우 프로토콜 자체 변경
  - 신규 인증 스택 도입

## Quality Attributes

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: 인증 오버헤드는 낮게 유지(기본 `/oauth2/auth` 경량 검증 경로).
- **Security**: 시크릿 파일 주입, non-root 실행, fail-closed 정책.
- **Reliability**: 정적 검증 스크립트 + 헬스체크 + 명시적 장애 복구 절차.
- **Scalability**: 도메인/세션 정책을 환경 변수 기반으로 표준화해 확장 용이성 확보.
- **Observability**: 컨테이너 로그/헬스 상태 중심의 증적 수집 가능 상태 유지.
- **Operability**: CI 게이트와 문서 연계를 통한 운영 변경 통제 강화.

## Architecture Views

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

- Client Request → Traefik (`01-gateway`) → OAuth2 Proxy ForwardAuth
- OAuth2 Proxy ↔ Keycloak (OIDC issuer/callback)
- Keycloak ↔ PostgreSQL (`mng-pg`)
- OAuth2 Proxy ↔ Valkey 세션 저장: root-active dev leaf는 `mng-valkey`, local/full leaf는 `oauth2-proxy-valkey` 사용

핵심 아키텍처 원칙:

- 인증 불가 상황에서 우회 허용하지 않음(fail-closed).
- 운영자가 degraded-mode 여부를 명시 절차로 판단하고 제한적으로 수행.

## Data and Infrastructure

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

- **Key Entities / Flows**:
  - Keycloak realm/user/session metadata
  - OAuth2 Proxy cookie/session state (Valkey)
- **Storage Strategy**:
  - Keycloak state: PostgreSQL
  - Proxy session: Valkey
- **Data Boundaries**:
  - 시크릿(`client_secret`, `cookie_secret`, DB password)은 `/run/secrets` 경로만 사용

## Infrastructure & Deployment

- **Runtime / Platform**:
  - Docker Compose 기반 운영
  - Keycloak: `template-infra-high` + `/run/secrets` 기반 DB/Admin secret 주입
  - OAuth2 Proxy: custom Alpine image + non-root 사용자
- **Deployment Model**:
  - root compose profile 정적 검증 후 단계적 반영(인증 계층 단위)
  - CI에서 `infrastructure-hardening` 필수 게이트 적용
- **Operational Evidence**:
  - `scripts/hardening/check-all-hardening.sh 02-auth`
  - `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
  - `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
  - 서비스별 healthcheck 결과

## AI Agent Architecture Descriptions (If Applicable)

- **Model/Provider Strategy**: N/A
- **Tooling Boundary**: 인프라/문서 변경 시 검증 스크립트 결과를 증적으로 남긴다.
- **Memory & Context Strategy**: Plan/Task/Operation/Runbook 상호 링크를 유지한다.
- **Guardrail Boundary**: 시크릿 평문 하드코딩 금지, fail-open 금지.
- **Latency / Cost Budget**: N/A

## Decision and Requirement Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [../01.requirements/0014-auth-optimization-hardening.md](../../01.requirements/0014-auth-optimization-hardening.md)
- **Spec**: [../03.specs/002-auth/spec.md](../../03.specs/spec-0002-auth/spec.md)
- **Plan**: ../04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md
- **ADR**: [../02.architecture/decisions/adr-0017-auth-hardening-runtime-and-fail-closed.md](../decisions/adr-0017-auth-hardening-runtime-and-fail-closed.md)
