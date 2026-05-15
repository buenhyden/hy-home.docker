# 01-gateway Specifications

> API Gateway 및 리버스 프록시 서비스 기술 사양

## Overview

`docs/03.specs/01-gateway`는 Traefik 및 Nginx 기반 API 게이트웨이 서비스의 기술 사양을 포함합니다.

## Scope

### In Scope

- 게이트웨이 서비스 인터페이스, 라우팅, TLS, 인증 미들웨어 사양
- 서비스 경계 및 네트워크 정책

### Out of Scope

- 운영 절차 (`docs/05.operations/guides/01-gateway/` 담당)
- 구현 실행 계획 (`docs/04.execution/plans/` 담당)

## Structure

```text
01-gateway/
├── spec.md      # Gateway service technical specification
└── README.md    # This file
```

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [infra/01-gateway/README.md](../../../infra/01-gateway/README.md)
- [docs/05.operations/guides/01-gateway/](../../05.operations/guides/01-gateway/)
