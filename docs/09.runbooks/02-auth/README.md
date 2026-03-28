# 02-Auth Runbooks

> `02-auth`(Keycloak/OAuth2 Proxy) 즉시 실행 절차 인덱스.

## Overview (KR)

이 디렉터리는 인증 장애/회귀 상황에서 운영자가 즉시 수행할 복구 절차를 제공한다.

## Structure

```text
02-auth/
├── keycloak.md      # Keycloak runtime and secret incident recovery
├── oauth2-proxy.md  # OAuth2 Proxy session loop / degraded-mode recovery
└── README.md
```

## Related Documents

- [Auth Operations](../../08.operations/02-auth/README.md)
- [Auth Plan](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- [Auth Tasks](../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)
- [Auth Guides](../../07.guides/02-auth/README.md)
- [Auth Spec](../../04.specs/02-auth/spec.md)
