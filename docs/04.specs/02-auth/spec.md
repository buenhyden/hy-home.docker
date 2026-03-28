# 02-Auth Optimization Hardening Specification

## Overview (KR)

이 문서는 `infra/02-auth`의 최적화/하드닝 구현 계약을 정의한다. Keycloak/OAuth2 Proxy 런타임 구성, 시크릿 주입 방식, fail-closed 운영 원칙, 그리고 검증/문서 추적성 기준을 명시한다.

## Strategic Boundaries & Non-goals

- 본 Spec은 인증 인프라 운영 품질과 보안 하드닝을 소유한다.
- 애플리케이션별 RBAC 비즈니스 로직, 신규 IdP 도입, 프로토콜 변경은 비범위다.

## Related Inputs

- **PRD**: [../../01.prd/2026-03-28-02-auth-optimization-hardening.md](../../01.prd/2026-03-28-02-auth-optimization-hardening.md)
- **ARD**: [../../02.ard/0014-auth-optimization-hardening-architecture.md](../../02.ard/0014-auth-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../03.adr/0002-keycloak-oauth2-proxy-choice.md](../../03.adr/0002-keycloak-oauth2-proxy-choice.md)
  - [../../03.adr/0017-auth-hardening-runtime-and-fail-closed.md](../../03.adr/0017-auth-hardening-runtime-and-fail-closed.md)

## Contracts

- **Config Contract**:
  - Keycloak: `template-infra-med`, `/run/secrets/*` 기반 DB/Admin secret 주입 유지
  - OAuth2 Proxy: `template-infra-readonly-med`, 엔트리포인트 기반 시크릿 주입
- **Data / Interface Contract**:
  - OIDC issuer: `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm`
  - Callback: `https://auth.${DEFAULT_URL}/oauth2/callback`
  - Session store: `redis://...@mng-valkey:6379`
- **Governance Contract**:
  - `scripts/check-auth-hardening.sh` 통과가 CI merge gate 조건
  - Guide/Operation/Runbook 문서는 상호 링크를 유지

## Core Design

- **Component Boundary**:
  - Keycloak: 토큰 발급/IdP 관리
  - OAuth2 Proxy: ForwardAuth 인증 게이트
- **Key Dependencies**:
  - `mng-pg` (Keycloak DB)
  - `mng-valkey` (OAuth2 session)
  - Traefik middleware/routers
- **Tech Stack**:
  - Keycloak 26.5.4
  - OAuth2 Proxy 7.14.2
  - Docker Compose + common optimization templates

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Keycloak realm/user/client는 PostgreSQL에 저장
  - OAuth2 Proxy 세션은 Valkey 키 공간에 저장
- **Migration / Transition Plan**:
  - 시크릿 주입 경로를 Compose 인라인 셸에서 엔트리포인트로 이전
  - 도메인/issuer/callback 값을 환경 변수 기반으로 표준화

## Interfaces & Data Structures

### Core Interfaces

```typescript
interface AuthHardeningContract {
  service: "keycloak" | "oauth2-proxy";
  failClosed: true;
  secretsSource: "/run/secrets";
  healthEndpoint: string;
}
```

## API Contract (If Applicable)

인증 계층은 애플리케이션 API를 직접 제공하지 않는다. 외부 노출 계약은 gateway/auth endpoint 동작으로 제한한다.

- `/oauth2/auth`
- `/oauth2/start`
- `/oauth2/callback`
- `/ping`

## Edge Cases & Error Handling

- Keycloak issuer 불가용: OAuth2 Proxy 인증 실패(기본 fail-closed)
- Cookie domain mismatch: 로그인 루프 발생
- Secret rotation 직후: 기존 세션 무효화

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: OIDC provider timeout/5xx 지속
- **Fallback**: degraded-mode 판단(정책/런북 절차에 따라 제한적 우회 또는 유지보수 안내)
- **Human Escalation**: Infra on-call + Security reviewer 동시 호출

## Verification

필수 검증 명령:

```bash
bash scripts/check-auth-hardening.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-doc-traceability.sh
docker compose config
docker compose -f infra/02-auth/keycloak/docker-compose.yml config
docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml config
```

## Success Criteria & Verification Plan

- **VAL-SPC-AUTH-001**: auth-hardening 스크립트 실패 0건
- **VAL-SPC-AUTH-002**: CI에 `auth-hardening` job이 존재하고 실행됨
- **VAL-SPC-AUTH-003**: 02-auth Guide/Operation/Runbook이 상호 링크로 연결됨

## Related Documents

- **Plan**: [../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/02-auth/README.md](../../07.guides/02-auth/README.md)
- **Operations**: [../../08.operations/02-auth/README.md](../../08.operations/02-auth/README.md)
- **Runbook**: [../../09.runbooks/02-auth/README.md](../../09.runbooks/02-auth/README.md)
