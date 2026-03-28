# 02-Auth Optimization & Hardening Product Requirements

## Overview (KR)

이 문서는 `infra/02-auth`(Keycloak, OAuth2 Proxy)의 최적화/하드닝 요구사항을 정의한다. 인증 경로의 안정성과 보안 기준을 강화하고, 운영 문서/실행 절차의 추적성을 일관되게 유지하는 것을 목표로 한다.

## Vision

`02-auth`를 `fail-closed` 원칙의 신뢰 가능한 인증 계층으로 운영하여, 전체 플랫폼 서비스의 SSO 진입점을 안정적으로 보호한다.

## Problem Statement

- OAuth2 Proxy 런타임 시크릿 주입이 Compose 인라인 셸에 의존하여 변경 추적과 운영 표준화가 어렵다.
- 인증 서비스의 보안/운영 기준이 문서 레이어(Plan/Task/Guide/Operation/Runbook)에 분산되어 일관성이 약하다.
- 장애 대응 시 degraded-mode 판단 기준과 롤백 절차가 명시적으로 정리되어 있지 않다.

## Personas

- **Platform Operator**: 인증 장애 시 빠르게 복구하고 근거를 남겨야 한다.
- **Infra/DevOps Engineer**: 배포/검증 자동화를 통해 변경 리스크를 줄여야 한다.
- **Service Developer**: ForwardAuth 보호 경로를 예측 가능하게 연동해야 한다.

## Key Use Cases

- **STORY-01**: 운영자는 인증 계층 변경 후 CI 게이트로 하드닝 기준 통과 여부를 즉시 확인한다.
- **STORY-02**: 장애 대응자는 OIDC 장애/세션 루프 상황에서 런북 절차로 복구하고 롤백한다.
- **STORY-03**: 개발자는 표준 가이드를 따라 신규 서비스를 SSO 경로에 안전하게 연결한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: OAuth2 Proxy 시크릿 주입은 엔트리포인트 스크립트 기반으로 표준화해야 한다.
- **REQ-PRD-FUN-02**: OAuth2 Proxy 컨테이너는 비루트(non-root) 실행을 기본값으로 해야 한다.
- **REQ-PRD-FUN-03**: Keycloak/OAuth2 Proxy 하드닝 정적 검증 스크립트를 제공하고 CI 필수 게이트로 적용해야 한다.
- **REQ-PRD-FUN-04**: `docs/01~09` 문서 레이어는 상호 참조 링크를 통해 양방향 추적성을 보장해야 한다.
- **REQ-PRD-FUN-05**: OIDC 장애 시 degraded-mode 운영 판단 및 복구 절차를 문서화해야 한다.

## Success Criteria

- **REQ-PRD-MET-01**: `bash scripts/check-auth-hardening.sh`가 로컬/CI에서 모두 성공한다.
- **REQ-PRD-MET-02**: `docs/05.plans`, `docs/08.operations`, `docs/09.runbooks` 추적성 검증이 성공한다.
- **REQ-PRD-MET-03**: 인증 경로 주요 장애 유형(세션 루프, OIDC 연결 실패, 설정 회귀)에 대한 실행 가능한 런북이 최신 상태다.

## Scope and Non-goals

- **In Scope**:
  - `infra/02-auth/keycloak/*`, `infra/02-auth/oauth2-proxy/*` 하드닝
  - `scripts/check-auth-hardening.sh`, CI 게이트 추가
  - PRD~Runbook 문서 동기화 및 README 인덱스 갱신
- **Out of Scope**:
  - 신규 인증 프로토콜 도입(SAML/LDAP 신규 통합)
  - 타 티어 서비스의 라우팅 정책 전면 변경
  - 비즈니스 애플리케이션 RBAC 로직 변경
- **Non-goals**:
  - 외부 포트/호스트 계약 변경
  - 신규 시크릿 체계 도입(Vault 마이그레이션 등)

## Risks, Dependencies, and Assumptions

- Keycloak은 상태 저장 특성으로 readonly 템플릿 전환 대상이 아니다(현행 `template-infra-med` 유지).
- OAuth2 Proxy는 fail-open이 아닌 fail-closed를 기본으로 유지한다.
- 상위 의존성(`mng-pg`, `mng-valkey`, `01-gateway`)의 가용성을 전제로 한다.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: Compose/Config 하드닝, 검증 스크립트/CI/문서 수정.
- **Disallowed Actions**: 인증 우회(fail-open) 설정 강제, 시크릿 평문 하드코딩.
- **Human-in-the-loop Requirement**: 운영 배포 전 Infra Reviewer 승인.
- **Evaluation Expectation**: 하드닝/추적성 스크립트 + Compose 정적 검증 통과.

## Related Documents

- **ARD**: [../02.ard/0014-auth-optimization-hardening-architecture.md](../02.ard/0014-auth-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/02-auth/spec.md](../04.specs/02-auth/spec.md)
- **Plan**: [../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md](../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0017-auth-hardening-runtime-and-fail-closed.md](../03.adr/0017-auth-hardening-runtime-and-fail-closed.md)
