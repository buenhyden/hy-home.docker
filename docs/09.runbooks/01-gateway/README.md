# 01-Gateway Runbooks

> `01-gateway`(Traefik/Nginx) 즉시 실행 절차 인덱스.

## Overview (KR)

이 디렉터리는 게이트웨이 장애/회귀 상황에서 운영자가 즉시 수행할 복구 절차를 제공한다.

## Structure

```text
01-gateway/
├── traefik.md   # Traefik middleware/auth/route recovery
├── nginx.md     # Nginx readonly/tmpfs/config recovery
└── README.md
```

## Related Documents

- [Gateway Operations](../../08.operations/01-gateway/README.md)
- [Gateway Plan](../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
- [Gateway Tasks](../../06.tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)
- [Gateway Guides](../../07.guides/01-gateway/README.md)
