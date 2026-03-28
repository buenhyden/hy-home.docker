# 01-Gateway Operations Policies

> `01-gateway` 티어(Traefik/Nginx) 운영 정책 인덱스.

## Overview (KR)

이 디렉터리는 `infra/01-gateway`의 운영 통제 기준을 정의한다. 기본 진입점은 Traefik이며, Nginx는 특수 경로 프록시로 운용한다.

## Scope

### In Scope

- Traefik 라우터/미들웨어 표준 정책
- Nginx readonly/timeout/failover 정책
- 변경 승인 및 검증 기준

### Out of Scope

- 즉시 실행 절차(런북)
- 튜토리얼/온보딩 가이드

## Structure

```text
01-gateway/
├── traefik.md   # Traefik primary gateway operations policy
├── nginx.md     # Nginx special-path proxy operations policy
└── README.md
```

## Related Documents

- [Gateway Plan](../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
- [Gateway Tasks](../../06.tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)
- [Gateway Runbooks](../../09.runbooks/01-gateway/README.md)
- [Gateway Guides](../../07.guides/01-gateway/README.md)
- [Infra Source](../../../infra/01-gateway/README.md)
