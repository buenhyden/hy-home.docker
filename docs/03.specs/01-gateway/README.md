# 01-gateway Specifications

> API Gateway 및 리버스 프록시 서비스 기술 사양

## Overview

`docs/03.specs/01-gateway`는 Traefik 및 Nginx 기반 API 게이트웨이 서비스의 기술 사양을 포함합니다.

## Audience

이 README의 주요 독자:

- Developers
- System Architects
- QA Engineers
- AI Agents

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

## How to Work in This Area

1. 구현 또는 검증 전 [spec.md](./spec.md)를 먼저 확인합니다.
2. 상위 요구사항과 아키텍처 맥락은 Related Documents의 PRD/ARD/ADR 링크에서 추적합니다.
3. 새 child contract가 필요하면 `docs/99.templates`의 대응 템플릿을 사용하고 이 폴더 README를 함께 갱신합니다.
4. 운영 절차, 정책, runbook 내용은 `docs/05.operations/`에 두고 여기에는 구현 계약만 유지합니다.

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [infra/01-gateway/README.md](../../../infra/01-gateway/README.md)
- [docs/05.operations/guides/01-gateway/](../../05.operations/guides/01-gateway/)
