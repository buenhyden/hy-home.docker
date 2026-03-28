# 02-Auth Operations Policies

> `02-auth` 티어(Keycloak/OAuth2 Proxy) 운영 정책 인덱스.

## Overview (KR)

이 디렉터리는 인증 계층의 운영 통제 기준을 정의한다. 기본 정책은 fail-closed이며, degraded-mode는 승인된 절차에서만 제한적으로 허용한다.

## Scope

### In Scope

- Keycloak 시크릿/헬스체크/운영 변경 통제
- OAuth2 Proxy 시크릿 주입/non-root/세션 정책 통제
- 인증 계층 변경 승인 및 검증 기준

### Out of Scope

- 즉시 복구 절차(런북)
- 구현 튜토리얼(가이드)

## Structure

```text
02-auth/
├── keycloak.md      # Keycloak operations policy
├── oauth2-proxy.md  # OAuth2 Proxy operations policy
└── README.md
```

## Related Documents

- [Auth Plan](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- [Auth Tasks](../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)
- [Auth Spec](../../04.specs/02-auth/spec.md)
- [Auth Runbooks](../../09.runbooks/02-auth/README.md)
- [Auth Guides](../../07.guides/02-auth/README.md)
- [Infra Source](../../../infra/02-auth/README.md)
