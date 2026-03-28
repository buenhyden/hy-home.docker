# ADR-0017: 02-Auth Runtime Hardening and Fail-closed Policy

## Overview (KR)

이 문서는 `02-auth` 계층의 런타임 하드닝 방식과 인증 장애 시 fail-closed 정책을 결정한 기록이다.

## Context

`infra/02-auth`의 OAuth2 Proxy는 시크릿 주입을 Compose 인라인 셸로 처리하고 있었다. 이 방식은 변경 추적/재사용성이 낮고, 운영 표준(최소 권한 런타임, 명확한 엔트리포인트 계약)과 맞지 않았다. 또한 인증 장애 시 우회 허용 여부가 문서적으로 명확히 고정되지 않았다.

## Decision

- OAuth2 Proxy 시크릿 주입은 `docker-entrypoint.sh`로 일원화한다.
- OAuth2 Proxy 컨테이너는 non-root 사용자(`oauth2proxy`)로 실행한다.
- 인증 장애 기본 동작은 fail-closed를 유지한다.
- degraded-mode는 정책/런북 절차에 의해 제한적으로만 수행하고, 사후 원복을 필수화한다.
- Keycloak은 상태 저장 특성을 고려해 `template-infra-med`를 유지한다(readonly 강제 전환하지 않음).

## Explicit Non-goals

- Keycloak/OAuth2 Proxy 외 인증 스택 추가 또는 교체
- fail-open 기본 정책 도입
- 신규 시크릿 백엔드 도입(Vault 강제 마이그레이션)

## Consequences

- **Positive**:
  - 시크릿 주입 경로가 단일화되어 감사/검증이 쉬워진다.
  - 최소 권한 실행으로 컨테이너 런타임 공격면이 축소된다.
  - 운영자가 장애 시 정책/절차에 따라 일관되게 대응할 수 있다.
- **Trade-offs**:
  - 엔트리포인트 스크립트 유지보수 책임이 생긴다.
  - fail-closed로 인해 IdP 장애 시 사용자 영향이 즉시 드러날 수 있다.

## Alternatives

### Compose 인라인 셸 유지

- Good:
  - 즉시 적용이 쉽다.
- Bad:
  - 시크릿 처리 로직이 선언형 파일에 혼재되어 추적성이 낮다.
  - 재사용/테스트 포인트 분리가 어렵다.

### fail-open 예외를 기본값으로 채택

- Good:
  - IdP 장애 시 단기 가용성은 높아질 수 있다.
- Bad:
  - 인증 우회 리스크가 커지고 보안 경계가 무너진다.

## Agent-related Example Decisions (If Applicable)

- Tool gating: `scripts/check-auth-hardening.sh`를 CI 필수 게이트로 사용
- Guardrail strategy: 시크릿 평문/우회 정책 금지

## Related Documents

- **PRD**: [../01.prd/2026-03-28-02-auth-optimization-hardening.md](../01.prd/2026-03-28-02-auth-optimization-hardening.md)
- **ARD**: [../02.ard/0014-auth-optimization-hardening-architecture.md](../02.ard/0014-auth-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/02-auth/spec.md](../04.specs/02-auth/spec.md)
- **Plan**: [../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md](../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- **Related ADR**: [./0002-keycloak-oauth2-proxy-choice.md](./0002-keycloak-oauth2-proxy-choice.md)
