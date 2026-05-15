# 02-auth Specifications

> 인증 및 권한 부여 서비스 기술 사양

## Overview

`docs/03.specs/02-auth`는 Keycloak 및 OAuth2 Proxy 기반 인증·인가 서비스의 기술 사양을 포함합니다.

## Scope

### In Scope

- 인증 흐름, 토큰 구조, OIDC 설정, OAuth2 프록시 사양
- 역할 및 클라이언트 경계 정의

### Out of Scope

- 운영 절차 (`docs/05.operations/guides/02-auth/` 담당)

## Structure

```text
02-auth/
├── spec.md      # Auth service technical specification
└── README.md    # This file
```

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [infra/02-auth/README.md](../../../infra/02-auth/README.md)
- [docs/05.operations/guides/02-auth/](../../05.operations/guides/02-auth/)
